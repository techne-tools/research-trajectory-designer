"""
Research Trajectory Designer v2 — Framework-Registry Plugin

A generalised version of the PaR trajectory designer. Instead of hardcoding
Robin Nelson's framework, it loads framework definitions from YAML files,
making it adaptable to any Practice-as-Research paradigm.

Usage:
    /trajectory start [name] --framework <framework>  — begin a new trajectory
    /trajectory resume [name]                          — continue an existing trajectory
    /trajectory status [name]                          — show current trajectory state
    /trajectory list                                   — list all trajectories
    /trajectory export [name]                          — generate the trajectory map
    /trajectory frameworks                             — list available frameworks
    /trajectory help                                   — show this help

Framework YAML files live in the 'frameworks/' directory alongside this plugin.
Each file defines dimensions, spheres, output categories, cycle steps, and
conversation principles for a specific PaR framework.
"""

from __future__ import annotations

import json
import os
import re
import yaml
from datetime import datetime
from pathlib import Path

PLUGIN_NAME = "research-trajectory-designer-v2"
PLUGIN_VERSION = "2.0.0"

# --- Paths ---

# The directory where this plugin lives (for finding frameworks/)
_PLUGIN_DIR = Path(__file__).parent.resolve()

# Framework definitions
_FRAMEWORKS_DIR = _PLUGIN_DIR / "frameworks"

# Trajectory state files
TRAJECTORY_DIR = os.path.expanduser(
    "~/Documents/Files/Personal/Obsidian/black-wish/06 - Research/Trajectories"
)

# Default framework if none specified
_DEFAULT_FRAMEWORK = "nelson"


# --- Framework Loading ---

def _load_framework(name: str) -> dict | None:
    """Load a framework definition from YAML."""
    # Try exact name
    path = _FRAMEWORKS_DIR / f"{name}.yaml"
    if not path.exists():
        # Try with .yml extension
        path = _FRAMEWORKS_DIR / f"{name}.yml"
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def _list_frameworks() -> list[dict]:
    """List all available frameworks with metadata."""
    frameworks = []
    for f in sorted(_FRAMEWORKS_DIR.glob("*.yaml")):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            frameworks.append({
                "name": data.get("name", f.stem),
                "display": data.get("display", f.stem.replace("-", " ").title()),
                "description": data.get("description", ""),
                "dimensions": len(data.get("dimensions", [])),
                "spheres": len(data.get("spheres", [])),
                "output_categories": len(data.get("output_categories", [])),
                "cycle_steps": len(data.get("cycle_steps", [])),
            })
        except (yaml.YAMLError, OSError):
            continue
    return frameworks


def _format_framework_help(framework: dict) -> str:
    """Format a framework description for display."""
    lines = [
        f"**{framework['display']}**",
        f"_{framework.get('description', '').strip()}_",
        "",
    ]
    ref = framework.get("reference", "")
    if ref:
        lines.append(f"Reference: {ref}")
        lines.append("")

    dims = framework.get("dimensions", [])
    if dims:
        lines.append("**Dimensions:**")
        for d in dims:
            lines.append(f"  • **{d['label']}** — {d['description']}")
        lines.append("")

    spheres = framework.get("spheres", [])
    if spheres:
        lines.append("**Spheres:**")
        for s in spheres:
            lines.append(f"  • **{s['label']}** — {s['description']}")
        lines.append("")

    cats = framework.get("output_categories", [])
    if cats:
        lines.append("**Output categories:**")
        for c in cats:
            lines.append(f"  • **{c['label']}** — {c['description']}")
        lines.append("")

    steps = framework.get("cycle_steps", [])
    if steps:
        lines.append("**Cycle:** " + " → ".join(s["label"] for s in steps))

    return "\n".join(lines)


# --- Trajectory State Management ---

def _get_trajectory_path(name: str) -> str:
    """Get the path for a trajectory state file."""
    os.makedirs(TRAJECTORY_DIR, exist_ok=True)
    safe_name = re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")
    return os.path.join(TRAJECTORY_DIR, f".{safe_name}-state.json")


def _load_trajectory(name: str) -> dict | None:
    """Load trajectory state from file."""
    path = _get_trajectory_path(name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def _save_trajectory(state: dict) -> None:
    """Save trajectory state to file."""
    path = _get_trajectory_path(state["name"])
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def _list_trajectories() -> list[dict]:
    """List all trajectory state files."""
    os.makedirs(TRAJECTORY_DIR, exist_ok=True)
    trajectories = []
    for f in os.listdir(TRAJECTORY_DIR):
        if f.startswith(".") and f.endswith("-state.json"):
            name = f[1:-11]
            path = os.path.join(TRAJECTORY_DIR, f)
            try:
                with open(path) as fh:
                    state = json.load(fh)
                trajectories.append({
                    "name": name,
                    "seed": state.get("seed", ""),
                    "phase": state.get("phase", "seed"),
                    "framework": state.get("framework", _DEFAULT_FRAMEWORK),
                    "updated": state.get("updated", ""),
                    "branches": len(state.get("branches", [])),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return sorted(trajectories, key=lambda t: t["updated"], reverse=True)


# --- Phase Descriptions (framework-agnostic) ---

_PHASE_DESCRIPTIONS = {
    "seed": "Surfacing the germ of interest — what's pulling at you",
    "situate": "Locating the seed in your practice and the field",
    "radiate": "Letting the seed branch into multiple inquiries",
    "output-form": "What shape does each branch take?",
    "cycle": "Mapping the research process cycle",
    "connect": "How branches relate — dependencies, sequence, through-line",
    "map": "Producing the trajectory map document",
}


def _phase_description(phase: str) -> str:
    return _PHASE_DESCRIPTIONS.get(phase, "Exploring the trajectory")


# --- Prompt Generation ---

def _get_phase_prompts(framework: dict, phase: str) -> list[str]:
    """Get framework-appropriate prompts for a given phase."""
    prompts = []

    if phase == "seed":
        # Seed prompts are framework-agnostic
        return [
            "What are you curious about right now? What's pulling at you?",
            "What friction or question keeps coming back in your practice?",
            "If you could spend a year following one thread, what would it be?",
            "What's something you've been meaning to explore but haven't had the space for?",
            "What's a problem in your field that nobody's solved yet?",
        ]

    if phase == "situate":
        # Collect prompts from all dimensions
        for dim in framework.get("dimensions", []):
            dim_prompts = dim.get("prompts", [])
            if dim_prompts:
                prompts.append(f"**[{dim['label']}]** {dim_prompts[0]}")
                if len(dim_prompts) > 1:
                    prompts.append(f"  _{dim_prompts[1]}_")
        # Add sphere prompts
        for sphere in framework.get("spheres", []):
            sphere_prompts = sphere.get("prompts", [])
            if sphere_prompts:
                prompts.append(f"**[{sphere['label']}]** {sphere_prompts[0]}")

    elif phase == "radiate":
        # Radiate prompts are framework-agnostic
        return [
            "If you follow this thread, where does it lead? What branches appear?",
            "What happens if you push this into a different medium, space, or context?",
            "What's the obvious version of this inquiry? What's the non-obvious one?",
            "What adjacent questions does this raise?",
            "What's the version of this that scares you a little?",
        ]

    elif phase == "output-form":
        for cat in framework.get("output_categories", []):
            cat_prompts = cat.get("prompts", [])
            if cat_prompts:
                prompts.append(f"**[{cat['label']}]** {cat_prompts[0]}")
                if len(cat_prompts) > 1:
                    prompts.append(f"  _{cat_prompts[1]}_")

    elif phase == "cycle":
        steps = framework.get("cycle_steps", [])
        if steps:
            step_labels = " → ".join(s["label"] for s in steps)
            prompts.append(f"The cycle for this framework is: **{step_labels}**")
            prompts.append("Where do you enter the cycle for this branch?")
            prompts.append("What's the rhythm — do you cycle fast (weekly) or slow (monthly)?")
            prompts.append("Where are the moments of critical reflection built in?")
        else:
            prompts.append("What's the rhythm of your research process?")
            prompts.append("How do you move between making and reflecting?")

    elif phase == "connect":
        return [
            "Which branches feed each other? What's the dependency graph?",
            "What order makes sense? What needs to happen before what?",
            "Are there branches that could run in parallel?",
            "Is there a 'trunk' inquiry that the others branch from?",
            "What's the through-line — the thing that connects all of these?",
        ]

    return prompts


# --- Trajectory Map Generation ---

def _generate_trajectory_map(state: dict) -> str:
    """Generate a trajectory map markdown document from state."""
    framework_name = state.get("framework", _DEFAULT_FRAMEWORK)
    framework = _load_framework(framework_name) or {}

    lines = [
        f"# {state['name']}\n",
        f"**Seed:** {state.get('seed', 'Not yet defined')}",
        f"**Framework:** {framework.get('display', framework_name)}",
        f"**Date created:** {state.get('created', 'unknown')[:10]}",
        f"**Last updated:** {state.get('updated', 'unknown')[:10]}",
        f"**Status:** Living document — return to revise as the trajectory evolves\n",
        "---\n",
        "## Trajectory Map\n",
    ]

    through_line = state.get("through_line", "")
    if through_line:
        lines.append("### Through-line")
        lines.append(through_line + "\n")

    branches = state.get("branches", [])
    if branches:
        lines.append("### Branches\n")
        for i, b in enumerate(branches, 1):
            lines.append(f"#### Branch {i}: {b.get('title', 'Untitled')}\n")

            # Dimensions (framework-agnostic — stored as key-value pairs)
            dims = b.get("dimensions", {})
            if dims:
                for dim_key, dim_value in dims.items():
                    # Try to find the dimension label from the framework
                    dim_label = dim_key
                    for d in framework.get("dimensions", []):
                        if d["id"] == dim_key:
                            dim_label = d["label"]
                            break
                    lines.append(f"- **{dim_label}:** {dim_value}")

            # Spheres
            sphere = b.get("sphere", "")
            if sphere:
                # Try to find the sphere label
                sphere_label = sphere
                for s in framework.get("spheres", []):
                    if s["id"] == sphere:
                        sphere_label = s["label"]
                        break
                lines.append(f"- **Sphere:** {sphere_label}")

            # Output forms
            outputs = b.get("output_forms", {})
            if outputs:
                lines.append("- **Output forms:**")
                for form_key, form_desc in outputs.items():
                    # Try to find the category label
                    form_label = form_key
                    for c in framework.get("output_categories", []):
                        if c["id"] == form_key:
                            form_label = c["label"]
                            break
                    if form_desc:
                        lines.append(f"  - **{form_label}:** {form_desc}")

            # Dependencies
            deps = b.get("dependencies", [])
            if deps:
                lines.append(f"- **Dependencies:** {', '.join(deps)}")

            # Status
            status = b.get("status", "seed")
            lines.append(f"- **Status:** {status}")
            lines.append("")
    else:
        lines.append("*No branches yet — the conversation is still in the seed phase.*\n")

    # Notes
    notes = state.get("notes", [])
    if notes:
        lines.append("---\n")
        lines.append("## Notes\n")
        for n in notes:
            ts = n.get("timestamp", "")[:10]
            text = n.get("text", "")
            lines.append(f"- *({ts})* {text}")

    lines.append("")
    lines.append("---")
    lines.append(f"**Tags:** #research-trajectory #par #{framework_name}")

    return "\n".join(lines)


# --- Plugin Registration ---

def register(ctx) -> None:
    """Register this plugin with the Hermes agent."""

    def _handle_trajectory(raw_args: str = "", **kwargs) -> str:
        """Run the research trajectory designer.

        Subcommands:
          start [name] --framework <fw>  — begin a new trajectory
          resume [name]                  — continue an existing trajectory
          status [name]                  — show current trajectory state
          list                           — list all trajectories
          export [name]                  — generate the trajectory map
          frameworks                     — list available frameworks
          framework <name>               — show details of a framework
          help                           — show this help
        """
        parts = raw_args.strip().split()
        if not parts:
            return _handle_trajectory("help")

        subcommand = parts[0].lower()

        if subcommand == "help":
            return (
                "**Research Trajectory Designer v2**\n\n"
                "A framework-registry tool for mapping PaR research trajectories.\n\n"
                "**Commands:**\n"
                "  `/trajectory start [name]` — begin a new trajectory (default: Nelson)\n"
                "  `/trajectory start [name] --framework <fw>` — begin with a specific framework\n"
                "  `/trajectory resume [name]` — continue an existing trajectory\n"
                "  `/trajectory status [name]` — show current trajectory state\n"
                "  `/trajectory list` — list all trajectories\n"
                "  `/trajectory export [name]` — generate the trajectory map document\n"
                "  `/trajectory frameworks` — list available frameworks\n"
                "  `/trajectory framework <name>` — show framework details\n\n"
                "**Available frameworks:**\n"
                + "\n".join(
                    f"  • `{fw['name']}` — {fw['display']}"
                    for fw in _list_frameworks()
                )
                + "\n\n"
                "**What this does:**\n"
                "A freewheeling, iterative conversation that helps you map a research trajectory — "
                "a linked series of outputs across a broad PaR domain. The framework you choose "
                "shapes the prompts, categories, and structure of the conversation.\n\n"
                "The conversation moves through: Seed → Situate → Radiate → Output-Form → "
                "Cycle → Connect → Map. But it can loop, digress, and follow tangents at any point."
            )

        if subcommand == "frameworks":
            frameworks = _list_frameworks()
            if not frameworks:
                return "No frameworks found. Check that framework YAML files exist."
            lines = ["**Available Frameworks:**\n"]
            for fw in frameworks:
                lines.append(
                    f"• **{fw['name']}** — {fw['display']}\n"
                    f"  {fw['description'][:120]}…\n"
                    f"  _{fw['dimensions']} dimensions, {fw['spheres']} spheres, "
                    f"{fw['output_categories']} output categories_\n"
                )
            lines.append("\nUse `/trajectory framework <name>` for details.")
            return "\n".join(lines)

        if subcommand == "framework":
            fw_name = parts[1] if len(parts) > 1 else ""
            if not fw_name:
                return "Specify a framework name: `/trajectory framework <name>`"
            framework = _load_framework(fw_name)
            if not framework:
                return f"Framework '{fw_name}' not found. Use `/trajectory frameworks` to see available frameworks."
            return _format_framework_help(framework)

        if subcommand == "list":
            trajectories = _list_trajectories()
            if not trajectories:
                return "No trajectories found. Start one with `/trajectory start`."
            lines = ["**Saved Trajectories:**\n"]
            for t in trajectories:
                lines.append(
                    f"• **{t['name']}** [{t['framework']}] — {t['seed'][:60]}… "
                    f"(phase: {t['phase']}, {t['branches']} branches, updated {t['updated'][:10]})"
                )
            return "\n".join(lines)

        if subcommand == "start":
            # Parse name and optional --framework flag
            name = ""
            framework_name = _DEFAULT_FRAMEWORK
            remaining = parts[1:] if len(parts) > 1 else []

            # Check for --framework flag
            fw_idx = -1
            for i, p in enumerate(remaining):
                if p == "--framework":
                    fw_idx = i
                    if i + 1 < len(remaining):
                        framework_name = remaining[i + 1]
                    break

            if fw_idx >= 0:
                # Remove --framework and its value from the name parts
                name_parts = remaining[:fw_idx] + remaining[fw_idx + 2:]
            else:
                name_parts = remaining

            name = " ".join(name_parts).strip() if name_parts else ""

            if not name:
                fw_list = "\n".join(
                    f"  • `{fw['name']}` — {fw['display']}"
                    for fw in _list_frameworks()
                )
                return (
                    "Give your trajectory a name:\n"
                    "  `/trajectory start my-research-trajectory`\n"
                    "  `/trajectory start my-research-trajectory --framework haseman`\n\n"
                    "**Available frameworks:**\n" + fw_list
                )

            # Validate framework
            framework = _load_framework(framework_name)
            if not framework:
                return (
                    f"Framework '{framework_name}' not found. "
                    f"Use `/trajectory frameworks` to see available frameworks."
                )

            existing = _load_trajectory(name)
            if existing:
                return (
                    f"A trajectory named '{name}' already exists. "
                    f"Use `/trajectory resume {name}` to continue, "
                    f"or choose a different name."
                )

            state = {
                "name": name,
                "framework": framework_name,
                "seed": "",
                "phase": "seed",
                "branches": [],
                "through_line": "",
                "notes": [],
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
            }
            _save_trajectory(state)

            return (
                f"**Trajectory: {name}**\n"
                f"**Framework:** {framework.get('display', framework_name)}\n\n"
                "Let's start with the seed. What are you curious about? "
                "What's pulling at you right now?\n\n"
                "No pressure — just the germ. Could be a friction, a question, "
                "a material, a space, a frustration, a fascination. "
                "Tell me what's on your mind."
            )

        if subcommand == "resume":
            name = " ".join(parts[1:]).strip() if len(parts) > 1 else ""
            if not name:
                trajectories = _list_trajectories()
                if not trajectories:
                    return "No trajectories to resume. Start one with `/trajectory start`."
                lines = ["Which trajectory? Choose one:\n"]
                for t in trajectories:
                    lines.append(f"  • `{t['name']}` [{t['framework']}] — {t['seed'][:60]}…")
                lines.append("\nThen: `/trajectory resume <name>`")
                return "\n".join(lines)

            state = _load_trajectory(name)
            if not state:
                return (
                    f"No trajectory named '{name}' found. "
                    f"Use `/trajectory list` to see available trajectories, "
                    f"or `/trajectory start {name}` to create one."
                )

            framework_name = state.get("framework", _DEFAULT_FRAMEWORK)
            framework = _load_framework(framework_name) or {}
            phase = state.get("phase", "seed")
            branch_count = len(state.get("branches", []))

            # Get phase prompts from the framework
            phase_prompts = _get_phase_prompts(framework, phase)
            prompt_sample = ""
            if phase_prompts:
                prompt_sample = "\n".join(f"  • {p}" for p in phase_prompts[:3])

            return (
                f"**Resuming: {name}**\n"
                f"Framework: {framework.get('display', framework_name)}\n"
                f"Phase: {phase} | {branch_count} branches\n"
                f"Seed: {state.get('seed', 'not yet defined')[:100]}\n\n"
                f"Where would you like to pick up? We were working on:\n"
                f"- **{phase.capitalize()}** — {_phase_description(phase)}\n\n"
                f"Some questions to get us moving:\n{prompt_sample}\n\n"
                "Tell me what you're thinking, or I can ask a question."
            )

        if subcommand == "status":
            name = " ".join(parts[1:]).strip() if len(parts) > 1 else ""
            if not name:
                trajectories = _list_trajectories()
                if not trajectories:
                    return "No trajectories found."
                lines = ["**Trajectories:**\n"]
                for t in trajectories:
                    lines.append(
                        f"• **{t['name']}** [{t['framework']}] — "
                        f"phase: {t['phase']}, {t['branches']} branches"
                    )
                return "\n".join(lines)

            state = _load_trajectory(name)
            if not state:
                return f"No trajectory named '{name}' found."

            framework_name = state.get("framework", _DEFAULT_FRAMEWORK)
            framework = _load_framework(framework_name) or {}

            lines = [
                f"**Trajectory: {name}**\n",
                f"**Framework:** {framework.get('display', framework_name)}",
                f"**Seed:** {state.get('seed', 'not defined')}",
                f"**Phase:** {state.get('phase', 'seed')}",
                f"**Through-line:** {state.get('through_line', 'not yet articulated')}",
                f"**Branches:** {len(state.get('branches', []))}",
                f"**Created:** {state.get('created', 'unknown')[:16]}",
                f"**Updated:** {state.get('updated', 'unknown')[:16]}",
            ]

            branches = state.get("branches", [])
            if branches:
                lines.append("\n**Branches:**")
                for i, b in enumerate(branches, 1):
                    outputs = b.get("output_forms", {})
                    output_str = " / ".join(
                        f"{v[:40]}" for v in outputs.values() if v
                    ) if outputs else "?"
                    lines.append(f"  {i}. **{b.get('title', 'untitled')}** — {output_str}")

            notes = state.get("notes", [])
            if notes:
                lines.append(f"\n**Notes:** {len(notes)} captured")

            return "\n".join(lines)

        if subcommand == "export":
            name = " ".join(parts[1:]).strip() if len(parts) > 1 else ""
            if not name:
                trajectories = _list_trajectories()
                if not trajectories:
                    return "No trajectories to export."
                lines = ["Which trajectory? Choose one:\n"]
                for t in trajectories:
                    lines.append(f"  • `{t['name']}` — {t['seed'][:60]}…")
                lines.append("\nThen: `/trajectory export <name>`")
                return "\n".join(lines)

            state = _load_trajectory(name)
            if not state:
                return f"No trajectory named '{name}' found."

            doc = _generate_trajectory_map(state)
            doc_path = os.path.join(TRAJECTORY_DIR, f"{name}.md")

            with open(doc_path, "w") as f:
                f.write(doc)

            return (
                f"**Trajectory map generated:** `{doc_path}`\n\n"
                f"Open it in Obsidian to view, edit, and develop further.\n"
                f"The map is a living document — return to it as the trajectory evolves."
            )

        return (
            "Unknown subcommand. Use:\n"
            "  `/trajectory start [name]`\n"
            "  `/trajectory resume [name]`\n"
            "  `/trajectory status [name]`\n"
            "  `/trajectory list`\n"
            "  `/trajectory export [name]`\n"
            "  `/trajectory frameworks`\n"
            "  `/trajectory framework <name>`\n"
            "  `/trajectory help`"
        )

    def _handle_trajectory_update(args: dict, **kwargs) -> str:
        """Update the state of a research trajectory during a conversation."""
        name = args.get("name", "")
        updates_raw = args.get("updates", "{}")

        state = _load_trajectory(name)
        if not state:
            return json.dumps({"error": f"No trajectory named '{name}' found."})

        try:
            data = json.loads(updates_raw)
        except json.JSONDecodeError:
            return json.dumps({"error": "updates must be valid JSON"})

        if "seed" in data:
            state["seed"] = data["seed"]
        if "phase" in data:
            state["phase"] = data["phase"]
        if "through_line" in data:
            state["through_line"] = data["through_line"]
        if "branches" in data:
            state["branches"] = data["branches"]
        if "notes" in data:
            state["notes"].extend(data["notes"])

        state["updated"] = datetime.now().isoformat()
        _save_trajectory(state)

        return json.dumps({
            "success": True,
            "message": f"Trajectory '{name}' updated (phase: {state['phase']})"
        })

    def _handle_trajectory_add_note(args: dict, **kwargs) -> str:
        """Add a note to the current trajectory conversation."""
        name = args.get("name", "")
        note = args.get("note", "")

        state = _load_trajectory(name)
        if not state:
            return json.dumps({"error": f"No trajectory named '{name}' found."})

        state["notes"].append({
            "text": note,
            "timestamp": datetime.now().isoformat(),
        })
        state["updated"] = datetime.now().isoformat()
        _save_trajectory(state)

        return json.dumps({"success": True, "message": f"Note added to '{name}'"})

    ctx.register_command(
        "trajectory",
        handler=_handle_trajectory,
        description="Framework-registry PaR trajectory mapping. Supports Nelson, Haseman, Bolt, Smith & Dean, and custom frameworks.",
        args_hint="start|resume|status|list|export|frameworks|framework|help",
    )

    ctx.register_tool(
        name="trajectory_update",
        toolset="research-trajectory-designer-v2",
        schema={
            "type": "object",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The trajectory name",
                    },
                    "updates": {
                        "type": "string",
                        "description": "JSON string with fields to update. Fields: seed, phase, branches, through_line, notes (appended)",
                    },
                },
                "required": ["name", "updates"],
            },
        },
        handler=_handle_trajectory_update,
        description="Update the state of a research trajectory during a conversation.",
    )

    ctx.register_tool(
        name="trajectory_add_note",
        toolset="research-trajectory-designer-v2",
        schema={
            "type": "object",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The trajectory name",
                    },
                    "note": {
                        "type": "string",
                        "description": "The note text to append",
                    },
                },
                "required": ["name", "note"],
            },
        },
        handler=_handle_trajectory_add_note,
        description="Add a note to the current trajectory conversation.",
    )
