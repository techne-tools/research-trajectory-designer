"""Dry-run load test for research-trajectory-designer-v2 register() entry point.

Verifies the plugin wires up correctly WITHOUT a live Hermes session:
- tool names, toolset, parameters-wrapped schemas (pitfall 25)
- command name + args_hint
- handlers actually run and return valid output (JSON for tools)

Usage:
    python3 tests/test_dry_run_load.py

Stdlib only — no Hermes install needed.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN_SRC = REPO / "plugin" / "__init__.py"
FRAMEWORKS_DIR = REPO / "frameworks"

_spec = importlib.util.spec_from_file_location("rtd_v2_plugin", PLUGIN_SRC)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Could not load {PLUGIN_SRC}")
plugin = importlib.util.module_from_spec(_spec)
sys.modules["rtd_v2_plugin"] = plugin
_spec.loader.exec_module(plugin)


class FakeCtx:
    """Minimal stand-in for PluginContext — captures every registration call."""

    def __init__(self) -> None:
        self.tools: list[dict] = []
        self.commands: list[dict] = []
        self.hooks: list[tuple[str, object]] = []

    def register_tool(self, name, toolset, schema, handler, **kw) -> None:
        self.tools.append({"name": name, "toolset": toolset, "schema": schema, "handler": handler, **kw})

    def register_command(self, name, handler, description="", args_hint="", **kw) -> None:
        self.commands.append({"name": name, "handler": handler, "description": description, "args_hint": args_hint, **kw})

    def register_hook(self, hook_name: str, callback) -> None:
        self.hooks.append((hook_name, callback))


def main() -> int:
    errors: list[str] = []

    # Point the plugin at the repo's frameworks/ (the plugin dir has none)
    plugin._FRAMEWORKS_DIR = FRAMEWORKS_DIR

    # Isolate trajectory state in a temp dir
    tmp = tempfile.mkdtemp(prefix="rtd-v2-test-")
    plugin.TRAJECTORY_DIR = tmp

    ctx = FakeCtx()
    plugin.register(ctx)

    # --- Registration wiring ---
    if not ctx.tools:
        errors.append("no tools registered")
    if not ctx.commands:
        errors.append("no commands registered")

    for t in ctx.tools:
        schema = t["schema"]
        if "parameters" not in schema:
            errors.append(f"{t['name']}: schema missing 'parameters' key")
        elif "properties" in schema:
            errors.append(f"{t['name']}: 'properties' at top level (must be under parameters)")
        if not callable(t["handler"]):
            errors.append(f"{t['name']}: handler not callable")
        if not t.get("toolset"):
            errors.append(f"{t['name']}: missing toolset")

    for c in ctx.commands:
        if not callable(c["handler"]):
            errors.append(f"/{c['name']}: handler not callable")
        if not c.get("args_hint"):
            errors.append(f"/{c['name']}: missing args_hint")

    # --- Exercise handlers ---
    cmd = next(c for c in ctx.commands if c["name"] == "trajectory")
    handle = cmd["handler"]
    tools = {t["name"]: t["handler"] for t in ctx.tools}

    # help
    out = handle("help")
    if "Research Trajectory Designer v2" not in out:
        errors.append("help output missing plugin title")

    # frameworks — must find all 12 YAMLs
    out = handle("frameworks")
    if "Available Frameworks" not in out:
        errors.append("frameworks output missing header")
    if out.count("•") < 12:
        errors.append(f"frameworks output lists fewer than 12 frameworks ({out.count('•')} found)")

    # framework details
    out = handle("framework nelson")
    if "Nelson" not in out:
        errors.append("framework nelson output missing display name")

    # start with a framework
    out = handle("start test-trajectory --framework haseman")
    if "Trajectory: test-trajectory" not in out:
        errors.append(f"start output unexpected: {out[:120]}")

    # duplicate start rejected
    out = handle("start test-trajectory --framework haseman")
    if "already exists" not in out:
        errors.append("duplicate start not rejected")

    # tool: update
    out = tools["trajectory_update"]({"name": "test-trajectory", "updates": '{"seed": "a seed", "phase": "situate"}'})
    data = json.loads(out)
    if not data.get("success"):
        errors.append(f"trajectory_update failed: {out}")

    # tool: add note
    out = tools["trajectory_add_note"]({"name": "test-trajectory", "note": "a note"})
    data = json.loads(out)
    if not data.get("success"):
        errors.append(f"trajectory_add_note failed: {out}")

    # tool: update on missing trajectory → error JSON, not crash
    out = tools["trajectory_update"]({"name": "nope", "updates": "{}"})
    data = json.loads(out)
    if "error" not in data:
        errors.append("trajectory_update on missing trajectory should return error")

    # status
    out = handle("status test-trajectory")
    if "a seed" not in out:
        errors.append("status output missing updated seed")

    # export → writes markdown
    out = handle("export test-trajectory")
    if "Trajectory map generated" not in out:
        errors.append(f"export output unexpected: {out[:120]}")
    md_path = os.path.join(tmp, "test-trajectory.md")
    if not os.path.exists(md_path):
        errors.append("export did not write markdown file")
    else:
        with open(md_path) as fh:
            if "a seed" not in fh.read():
                errors.append("exported markdown missing seed")

    # list
    out = handle("list")
    if "test-trajectory" not in out:
        errors.append("list output missing test trajectory")

    # unknown subcommand
    out = handle("bogus")
    if "Unknown subcommand" not in out:
        errors.append("unknown subcommand not handled")

    if errors:
        print("\n".join(f"❌ {e}" for e in errors))
        return 1
    print("✅ ALL CHECKS PASSED")
    print(f"   tools: {[t['name'] for t in ctx.tools]}")
    print(f"   commands: {[c['name'] for c in ctx.commands]}")
    print(f"   frameworks found: {len(list(FRAMEWORKS_DIR.glob('*.yaml')))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
