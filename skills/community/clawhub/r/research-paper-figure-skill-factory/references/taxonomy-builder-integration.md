# Taxonomy Builder Integration — v1.10

This guide integrates the `figure-taxonomy-skill-builder` method as an active **Skill Builder layer**, not merely a background reference.

## 1. Literature-to-specialized-skill route

Before using a taxonomy for concrete paper figure production, the complete workflow should convert literature evidence into a specialized figure-making skill for a chosen figure class.

The builder sequence is:

1. define target figure class, audience, output use, constraints, and acquisition policy;
2. lawfully discover/acquire a pilot corpus;
3. create paper cards and extract figure patterns with reliability labels;
4. build taxonomy axes and figure-type cards;
5. draft a specialized skill blueprint from the taxonomy;
6. generate the specialized skill package;
7. test the skill with startup, state, recommendation, visual-board, rendering-boundary, and next-question checks;
8. lock the generated specialized skill for production;
9. only then route concrete target-paper figure needs through that generated skill.

Do not collapse this into `taxonomy -> direct figure` unless the user explicitly requests full fast-track production. In that case, record skipped steps and the fallback skill/taxonomy.

## 2. Self-contained taxonomy knowledge

The generated specialized skill must be useful without external image examples, scripts, or local corpora. Therefore every figure type includes:

- purpose;
- reader effect;
- best paper slot;
- structural priorities;
- text strategy;
- typical misuse;
- refinement cues;
- provenance and reliability limitations.

## 3. Standard axes

The routing system keeps these axes:

- reader question;
- logical gap;
- narrative role / function;
- visual rhetoric;
- visual grammar / style;
- evidence type;
- density / layout;
- editing lever;
- paper slot.

## 4. Validation standard

A generated specialized skill is not complete unless it states:

- which figure class it serves;
- which corpus or source basis produced its taxonomy;
- what full texts/figures were inspected versus caption-only or metadata-only items;
- which workflows, prompts, templates, examples, and review rubrics it includes;
- which tests passed or failed;
- what limitations remain.

A concrete figure plan produced by the generated skill is not complete unless it answers:

- what kind of figure is needed;
- why that type fits the paper logic;
- where it belongs in the paper;
- how panels should be structured;
- what usually goes wrong;
- which refinement levers are most useful;
- what default route the user can accept without extra comparison.

## 5. Packaging standard

Generated specialized skills keep MIT-0 licensing, ClawHub/OpenClaw-friendly metadata, a concise `SKILL.md`, and richer reference files. The generated package must be treated as an artifact, not merely a description.

## v1.9 specialized-skill output target

Taxonomy construction is not the final output. In the default workflow it feeds a specialized figure-making skill: taxonomy axes become routing criteria, pattern cards become references, style/panel observations become prompt and visual-board protocols, and failure modes become the review rubric. The next deliverable after taxonomy is the specialized skill blueprint and package, not a concrete target-paper figure.


## v1.10 generic library boundary

`figure-type-library.md` and `figure-taxonomy-routing.md` are generic fallback scaffolds. They are useful for initial routing or full production fast-track, but they are not a substitute for the class-specific taxonomy produced in B5.

A generated specialized skill must include its own class-specific taxonomy and pattern library. If the workflow uses only generic libraries, record this as a limitation and keep `generated_skill.status` below `locked` unless the user explicitly accepts a fallback skill.
