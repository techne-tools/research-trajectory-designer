# Research Trajectory Designer v2 — Framework Registry

A generalised, framework-registry version of the PaR trajectory designer. Instead of hardcoding a single theoretical framework, it loads framework definitions from YAML files, making it adaptable to any Practice-as-Research paradigm.

## Architecture

```
research-trajectory-designer-v2/
├── SKILL.md              # Documentation, conversation principles, anti-patterns
├── plugin/
│   ├── __init__.py       # Python plugin — conversation engine + framework loader
│   └── plugin.yaml       # Plugin metadata
├── frameworks/
│   ├── nelson.yaml       # Robin Nelson — Multi-Mode Knowledge
│   ├── smith-dean.yaml   # Smith & Dean — Iterative Cyclic Web
│   ├── haseman.yaml      # Haseman — Performative Research
│   ├── bolt.yaml         # Bolt — Material Thinking
│   ├── candy-edmonds.yaml# Candy & Edmonds — Practice-Based Research
│   ├── sullivan.yaml     # Sullivan — Art Practice as Research
│   ├── borgdorff.yaml    # Borgdorff — The Conflict of the Faculties
│   ├── biggs-buchler.yaml# Biggs & Büchler — Rigour in Practice-Based Research
│   ├── carter.yaml       # Carter — Material Thinking
│   ├── gray.yaml         # Gray — Inquiry Through Practice
│   ├── biggs.yaml        # Biggs — The Role of the Artefact
│   └── generic.yaml      # Template for custom frameworks
├── templates/
│   (future: Jinja-style output templates)
└── references/
    └── test-drive-session.md  # Anonymised reference session
```

## How it works

1. **Framework YAML files** define dimensions, spheres, output categories, cycle steps, and conversation principles
2. **The plugin** loads the chosen framework at runtime and generates prompts dynamically
3. **The conversation** follows a 7-phase arc (Seed → Situate → Radiate → Output-Form → Cycle → Connect → Map)
4. **The trajectory map** is rendered using the framework's category labels

## Usage

```
/trajectory start my-trajectory                    # Default: Nelson
/trajectory start my-trajectory --framework haseman # Specific framework
/trajectory resume my-trajectory                   # Continue existing
/trajectory status my-trajectory                   # Show state
/trajectory list                                   # List all trajectories
/trajectory export my-trajectory                   # Generate map
/trajectory frameworks                             # List available frameworks
/trajectory framework nelson                       # Show framework details
```

## Adding a framework

Copy `frameworks/generic.yaml` and fill in the fields. Save as `frameworks/your-name.yaml`. It's available immediately — no plugin reload needed.

## Staged development

This lives in `~/Development/` to avoid breaking the current v1 implementation at `~/.hermes/plugins/research-trajectory-designer/`. When ready, the plugin goes to `~/.hermes/plugins/research-trajectory-designer-v2/` and the skill to `~/.hermes/skills/research/research-trajectory-designer-v2/`.

## Key differences from v1

| v1 | v2 |
|----|----|
| Nelson framework hardcoded in SKILL.md and plugin | Framework definitions in YAML files |
| Single framework | 11 frameworks + generic template |
| Framework-specific prompts in SKILL.md | Prompts generated dynamically from YAML |
| Fixed output categories | Output categories from active framework |
| Fixed cycle steps | Cycle steps from active framework |
| Chris-specific reference file | Anonymised reference file |
