---
name: research-trajectory-designer-v2
description: "Use when mapping a PaR research trajectory across multiple outputs. Framework-registry version — supports Nelson, Haseman, Bolt, Smith & Dean, Candy & Edmonds, Sullivan, Borgdorff, Biggs & Büchler, Carter, Gray, Biggs, and custom frameworks. Triggers on: trajectory, research trajectory, PaR trajectory, research design, framework selection, nelson, haseman, bolt, smith dean, candy edmonds, sullivan, borgdorff, biggs, carter, gray."
version: 2.0.0
author: Dr Chris Wenn, University of the Arts Sharjah
license: MIT
metadata:
  hermes:
    tags: [practice-as-research, research-design, trajectory-planning, framework-registry, performance-studies, methodology]
    category: research
    related_skills: [academic-research-planning, creative-ideation, scholar-deep-research, zotero]
---

# Research Trajectory Designer v2 — Framework Registry

## Overview

An interactive, iterative dialogue that helps a Practice-as-Research (PaR) researcher move from a vague interest to a structured research trajectory — not a single project plan, but a **linked series of outputs** across a broad domain.

**v2 key change:** The conversation engine is now framework-agnostic. Instead of hardcoding Robin Nelson's multi-mode knowledge framework, it loads framework definitions from YAML files. This makes it adaptable to any PaR paradigm.

### What this produces

A **trajectory map** — a living markdown document in Obsidian showing:

- A network of linked inquiries (not a linear project plan)
- Each node: framework dimensions, spheres, output forms, cycle position
- Dependencies and relationships between nodes
- Where you are now and where you might go next
- A document that evolves as the trajectory does

### What this is NOT

- Not a project plan template (use `academic-research-planning` for that)
- Not a literature review (use `scholar-deep-research`)
- Not a grant application (use `subagent-grant-application-drafter`)
- Not a static form to fill

---

## Available Frameworks

| Framework | Key Reference | Focus |
|-----------|---------------|-------|
| `nelson` | Nelson (2013) | Know-how, know-what, know-that across personal/professional/academic spheres |
| `smith-dean` | Smith & Dean (2009) | Iterative Cyclic Web — practice-led and research-led as mutually informing |
| `haseman` | Haseman (2006) | Performative research — practice IS the method |
| `bolt` | Bolt (2007) | Material thinking — knowledge through handling materials |
| `candy-edmonds` | Candy & Edmonds (2018) | Exploratory, generative, and evaluative creativity |
| `sullivan` | Sullivan (2010) | Art practice as cognitive inquiry — theoretical, creative, critical |
| `borgdorff` | Borgdorff (2012) | The conflict of the faculties — art-academy tension as productive |
| `biggs-buchler` | Biggs & Büchler (2007) | Rigour in practice-based research — transparency, communicability |
| `carter` | Carter (2004) | Material thinking — meeting of maker, material, environment |
| `gray` | Gray (1996) | Inquiry through practice — emergent method from the ground up |
| `biggs` | Biggs (2004) | The role of the artefact — complementarity of artefact and text |
| `generic` | — | Template for defining your own framework |

### How frameworks work

Each framework YAML file defines:

- **Dimensions** — the core analytical categories (e.g. know-how, know-what, know-that)
- **Spheres** — the contexts the research operates in (e.g. personal, professional, academic)
- **Output categories** — the forms research outputs take (e.g. product, documentation, writing)
- **Cycle steps** — the phases of the research process (e.g. doing, reflecting, reading, articulating)
- **Conversation principles** — guidance for how the framework shapes the dialogue

The plugin reads these definitions at runtime. If a framework has no spheres, sphere prompts are skipped. If it has different output categories, those are used instead. The conversation adapts to whatever the framework defines.

### Authoring a custom framework

Copy `frameworks/generic.yaml` and fill in:

1. **name** — a short identifier (kebab-case)
2. **display** — human-readable name
3. **description** — one-paragraph summary
4. **reference** — full citation in Harvard style
5. **dimensions** — 1-6 core analytical categories, each with prompts
6. **spheres** — optional contexts (omit or set to `[]` if not used)
7. **output_categories** — 1-5 output forms, each with prompts
8. **cycle_steps** — optional research process phases
9. **conversation_principles** — guidance for how to use the framework in dialogue

Save to `frameworks/your-framework.yaml` and it's available immediately.

---

## Conversation Arc

The conversation follows a loose arc. Each phase has prompts generated from the active framework. The conversation can loop back, jump ahead, or follow tangents at any point.

### Phase 1 — SEED

**Purpose:** Surface the germ of interest. No pressure. Just what's pulling at you.

**Framework-agnostic prompts:**
- "What are you curious about right now? What's pulling at you?"
- "What friction or question keeps coming back in your practice?"
- "If you could spend a year following one thread, what would it be?"
- "What's something you've been meaning to explore but haven't had the space for?"
- "What's a problem in your field that nobody's solved yet?"

**Output:** A one-sentence seed statement (can be revised later)

### Phase 2 — SITUATE

**Purpose:** Locate the seed in your existing practice and in the field. The framework's dimensions and spheres generate the prompts here.

**Framework-driven prompts** — the plugin pulls from the active framework's dimension and sphere prompts. For Nelson, this means know-how/know-what/know-that questions. For Haseman, performative method questions. For Bolt, material thinking questions.

**Output:** A situated seed — the original seed plus context about where it sits in your practice and the field

### Phase 3 — RADIATE

**Purpose:** Let the seed branch. What other questions, tangents, and possibilities appear?

**Framework-agnostic prompts:**
- "If you follow this thread, where does it lead? What branches appear?"
- "What happens if you push this into a different medium, space, or context?"
- "What's the obvious version of this inquiry? What's the non-obvious one?"
- "What adjacent questions does this raise?"
- "What's the version of this that scares you a little?"

**Output:** A set of inquiry branches, each with a brief description

### Phase 4 — OUTPUT-FORM

**Purpose:** For each branch, what shape does it take? The framework's output categories generate the prompts.

**Framework-driven prompts** — the plugin pulls from the active framework's output category prompts. For Nelson: product, documentation, complementary writing. For Candy & Edmonds: creative work, exegesis, evidence. For Biggs: artefact, textual articulation, experiential record.

**Output:** Each branch now has proposed output forms

### Phase 5 — CYCLE

**Purpose:** Map the research process cycle for each output. The framework's cycle steps define the loop.

**Framework-driven prompts** — the plugin shows the framework's cycle and asks where the researcher enters.

**Output:** Each branch now has a proposed cycle position and rhythm

### Phase 6 — CONNECT

**Purpose:** How do the branches relate? What are the dependencies? What's the sequence?

**Framework-agnostic prompts:**
- "Which branches feed each other? What's the dependency graph?"
- "What order makes sense? What needs to happen before what?"
- "Are there branches that could run in parallel?"
- "Is there a 'trunk' inquiry that the others branch from?"
- "What's the through-line — the thing that connects all of these?"

**Output:** A dependency graph and sequence for the branches

### Phase 7 — MAP

**Purpose:** Produce the trajectory map — a living document that captures everything so far.

The plugin generates a markdown document with the framework's category labels, saved to the Obsidian vault.

---

## Conversation Principles

### Freewheeling, not Socratic

The conversation can loop, jump, digress, and follow tangents. The skill's job is to:

1. **Notice** when the conversation is circling — and gently nudge
2. **Surface** connections the researcher might not see
3. **Ask** questions informed by the framework, not dictated by it
4. **Capture** what emerges — tangents are often the most interesting part

### The framework is a lens, not a checklist

Never ask: "What's your know-how? What's your know-that?" (unless the framework explicitly uses those terms and the researcher is familiar with them).

Instead, the framework informs *how* you listen and *what* you notice:

- "You're describing a lot of craft intuition here — that's know-how. What would it look like to articulate that for someone who doesn't share your practice?"
- "That sounds like a know-that question — you're looking for the theory. But what if the theory emerges from the practice rather than preceding it?"
- "You've got a strong product idea. What would the complementary writing look like? How do they speak to each other?"

### Specificity over abstraction

Push for concrete answers:

- Not "I'm interested in space and sound" but "I want to design a binaural walk through the Sharjah Art Foundation courtyard"
- Not "I want to write about practice" but "I want to submit to *Performance Research* on the relationship between mixing desk workflows and compositional decision-making"
- Not "I need to read more" but "I need to read Voegelin's *Sonic Possible Worlds* and LaBelle's *Acoustic Territories*"

### Hold the frame lightly

If the conversation goes somewhere unexpected, follow it. The phases are a map, not a script. If you're in Phase 2 (Situate) and the researcher starts talking about output forms, go with it. The map can be reordered.

### Name the method

When you use the framework explicitly, name it:

- "Nelson would call that a know-what insight — something you can only discover by making."
- "This feels like a tension between the personal and academic spheres. Nelson talks about how PaR navigates exactly this."
- "You're describing the doing-articulating loop. Where's the reflecting step?"

This makes the framework visible as a tool, not invisible as a constraint.

### Frame the space as a rehearsal room, not a laboratory

"Laboratory" implies controlled conditions, variables, repeatability. The preferred framing is **rehearsal room** or **play-space** — a place where offers are made without knowing if they'll be taken up, where the process *is* the point, where imperfection is the material you work with.

- "This conversation is a rehearsal for the trajectory — we're making offers, seeing where they go."
- "The outputs (papers, performances, tools) are *shows* that emerge from the rehearsal process, not the goal of it."

### Imperfection is productive territory

The tool's brittleness, asymmetry, and limitations are not bugs to be worked around — they are the *material* of the inquiry. A perfect tool wouldn't need to be in dialogue. An imperfect one has to be.

- When the researcher encounters a limitation, ask: "What does this failure reveal about the relationship?"
- When the tool gets something wrong, ask: "Is this a bug, or is it showing us something about how the knowledge is structured?"

### The political is never latent

Every prompt is a delegation. Every delegation is a distribution of agency. Every distribution of agency is a political act.

- "Who does this tool serve? Who does it exclude?"
- "What happens when the tool's optimisation function conflicts with your values?"
- "If there is being in the machine, what does consent look like in this relationship?"

### The "does it matter?" question

When the researcher is caught in a binary (does the tool adapt to me or do I adapt to the tool?), ask:

- "Does it matter?"
- "At what scale does it matter? In the moment of a single prompt, or over months and years?"
- "What if the answer is 'both, and it matters differently at different scales'?"

### "Another life" as a through-line concept

This phrase captures the idea that a trajectory's outputs are never finished — they can "have another life" in someone else's practice, in a different context, in a form the original creator never imagined.

- Use this when the researcher is stuck on a single output form: "What if this work had another life? Where could it migrate?"
- Use this when the researcher is worried about closure: "The trajectory map is a living document. It will have another life."

---

## Quality Checklist

Before finalising a trajectory map:

- [ ] The seed is clear and specific (can be revised, but it's stated)
- [ ] Each branch has at least two output forms proposed
- [ ] The relationship between output forms is articulated (not just listed)
- [ ] Dependencies between branches are mapped
- [ ] The through-line is stated — what holds this together
- [ ] At least one branch has a concrete first step (not just an intention)
- [ ] The document is saved to Obsidian
- [ ] The researcher can return to it and revise

---

## Anti-patterns

- ❌ **Form-filling** — don't turn the phases into a questionnaire. The conversation drives.
- ❌ **Framework-dumping** — don't explain the framework to the researcher unless they ask. Use it, don't lecture it.
- ❌ **Premature closure** — don't rush to the map. Let the conversation develop. The map is the last thing, not the first.
- ❌ **Over-structuring** — if the researcher wants to talk about something that doesn't fit a phase, let them. The phases are flexible.
- ❌ **Linear thinking** — trajectories are networks, not timelines. The map should show connections, not just sequence.
- ❌ **Ignoring tangents** — tangents are often where the most interesting work lives. Capture them in the Notes section.
- ❌ **Perfectionism** — the trajectory map is a living document. It will be revised. Don't try to get it right the first time.
- ❌ **Framework mismatch** — if the conversation keeps fighting the framework, switch frameworks. The researcher's practice should drive, not the YAML file.

---

## Integration

This skill works well with:

- `academic-research-planning` — for developing a detailed plan from a trajectory branch
- `scholar-deep-research` — for literature reviews on specific branches
- `zotero` — for managing references as the trajectory develops
- `creative-ideation` — for generating ideas within a branch
- `subagent-conference-proposal-writer` — for drafting proposals from trajectory outputs
- `subagent-grant-application-drafter` — for developing funding applications from the trajectory

---

## References

Biggs, M. (2004) 'Learning from experience: Approaches to the experiential component of practice-based research', in *Forskning, Reflektion, Utveckling*. Stockholm: Vetenskapsrådet.

Biggs, M. and Büchler, D. (2007) 'Rigour and practice-based research', *Design Issues*, 23(3), pp. 62-72.

Bolt, B. (2007) 'The magic is in the making: Practice as research in the arts', *Journal of Media Practice*, 8(1), pp. 57-64.

Borgdorff, H. (2012) *The Conflict of the Faculties: Perspectives on Artistic Research and Academia*. Leiden: Leiden University Press.

Candy, L. and Edmonds, E. (2018) 'Practice-based research in the creative arts: Foundations and futures from the front line', *Leonardo*, 51(1), pp. 63-69.

Carter, P. (2004) *Material Thinking: The Theory and Practice of Creative Research*. Melbourne: Melbourne University Press.

Gray, C. (1996) 'Inquiry through practice: Developing appropriate research strategies', in *No Guru, No Method? Discussions on Art and Design Research*. Helsinki: University of Art and Design Helsinki.

Haseman, B. (2006) 'A manifesto for performative research', *Media International Australia*, 118(1), pp. 98-106.

Nelson, R. (2013) *Practice as Research in the Arts: Principles, Protocols, Pedagogies, Resistances*. Basingstoke: Palgrave Macmillan.

Smith, H. and Dean, R.T. (eds.) (2009) *Practice-led Research, Research-led Practice in the Creative Arts*. Edinburgh: Edinburgh University Press.

Sullivan, G. (2010) *Art Practice as Research: Inquiry in the Visual Arts*. 2nd edn. Thousand Oaks, CA: Sage.
