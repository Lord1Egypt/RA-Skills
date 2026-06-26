# Literature-to-Taxonomy Builder Workflow

Version: 1.0.0

This file integrates the `figure-taxonomy-skill-builder` method into the two-layer guide. Its output is not merely a taxonomy for immediate figure routing; it is the evidence base for a **specialized figure-making skill**.

## Steps

1. Define target figure class and skill objective.
2. Build corpus plan: domain, venues, keywords, seed papers, inclusion/exclusion rules.
3. Acquire only legal/open/user-authorized sources.
4. Inspect figures where available; otherwise record captions-only or metadata-only limitations.
5. Create paper cards with figure inventory and visual patterns.
6. Build taxonomy axes: reader question, logical gap, narrative role, visual rhetoric, visual grammar, evidence type, layout/density, editing lever, paper slot.
7. Convert observed patterns into figure-type cards and anti-patterns.
8. Draft specialized skill workflow and state contract.
9. Draft prompt templates, visual style candidates, reference-image protocol, visual-board protocol, and review rubric.
10. Generate specialized skill artifacts and test them.

## Reliability labels

Every taxonomy claim should be traceable to one of:

- full figure inspection;
- caption-only evidence;
- metadata/abstract-only inference;
- user-provided reference image;
- built-in general taxonomy fallback.

## v1.12 evidence dependency rule

Do not build taxonomy directly from the B3 retrieval manifest. The manifest proves acquisition status only. Taxonomy construction must use B4 extracted evidence artifacts, especially `evidence_map.json`, `figure_inventory`, `caption_inventory`, `paper_cards`, `panel_structure_notes`, and `visual_pattern_observations`.

Each taxonomy claim must include evidence lineage:

- claim text;
- supporting paper IDs;
- supporting figure IDs;
- supporting caption or panel evidence;
- observed pattern;
- confidence level;
- limitation or fallback note.
