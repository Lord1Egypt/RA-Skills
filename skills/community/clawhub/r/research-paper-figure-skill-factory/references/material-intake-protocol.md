# Material Intake Protocol

## Preferred inputs

The best inputs are, in order:

1. paper draft or LaTeX source;
2. paper deep-reading report in Markdown;
3. abstract + contribution list;
4. method description or module list;
5. reviewer comment or figure critique;
6. existing figure draft;
7. sample/reference figures/images, optionally multiple images with per-image attribute preferences;
8. target venue or paper slot.

Preferred does not mean required. If the user provides incomplete material, infer cautiously and continue.

## Intake fields

Collect or infer:

- `paper_title_or_topic`
- `target_venue_or_style_expectation`
- `target_paper_slot`: intro / method / results / analysis / appendix / rebuttal / slides
- `core_claim`
- `main_problem_gap`
- `method_or_contribution`
- `must_explain`
- `must_not_include`
- `audience`: expert / mixed / broad / reviewer-sensitive
- `desired_output`: scheme / prompt / image batch / critique / caption
- `reference_image_status`
- `sample_reference_images`: list of images and per-image preferred attributes to borrow
- `existing_figure_status`

## Reference figure prompt

At intake or major visual decisions, ask briefly whether reference figures are available. Generated specialized skills must allow the user to provide one or more sample images and specify what to borrow from each image. Use this meaning, not necessarily this exact phrasing:

> 如果你有样例图/参考图，可以一次发一张或多张。我会先问你希望每张图主要参考什么：风格、布局骨架、panel 节奏、信息密度、内容细节程度、标签位置、颜色语义或箭头/标注方式。比如“图1参考布局，图2参考风格，图3参考信息密度”。如果没有，也可以继续按论文逻辑推进。

When sample images are provided, record:

- image id or filename;
- whether it is a positive reference or negative reference;
- preferred attributes to borrow;
- attributes to avoid copying;
- priority if multiple references conflict.

## Handling missing information

Do not block unless the figure would be unsafe or impossible to route. Instead:

- mark assumptions;
- give a default route;
- ask only one optional clarification if it materially changes the next step;
- continue with best-effort diagnosis.

## Intake output shape

After intake, produce:

- what material was available;
- what was inferred;
- what remains optional;
- initial figure need diagnosis;
- default next action.

## v1.4 literature-first note

In the v1.9 specialized-skill-first workflow, target-paper material intake is P1 and normally happens after the specialized skill has been generated and locked. If the user already has a corpus or taxonomy, record a partial builder shortcut such as skipped B2-B5; if the user wants immediate concrete figure production, record a full production fast-track with skipped B1-B9 and a fallback skill/taxonomy.

## v1.9 two-layer shortcut clarification

In v1.10, material intake belongs to the **Figure Production layer** and normally happens after a specialized figure-making skill has been generated, tested, and locked.

There are two different shortcut types; do not merge them:

1. **Partial builder shortcut**: skip only literature/corpus/taxonomy work because the user already has a corpus, taxonomy, or domain-specific evidence. Typical skipped steps: B2-B5. The assistant should still produce or refine the specialized skill in B6-B9.
2. **Full production fast-track**: skip the entire Skill Builder layer because the user wants immediate concrete figure production. Typical skipped steps: 1-9. The assistant must record the fallback specialized skill and fallback taxonomy used.

State must record:

- `workflow_shortcut.skipped_steps`;
- `workflow_shortcut.skip_reason`;
- `workflow_shortcut.fallback_skill_used`;
- `workflow_shortcut.fallback_taxonomy_used`;
- limitations caused by skipping any builder steps.

Never say a specialized skill was generated if the user chose full fast-track production.

## v1.9 production lock

Target-paper material intake belongs to P1 and must not be requested as the default next action while the builder layer is still generating the specialized skill. If the user has just chosen a target figure class, ask for literature/source inputs, seed papers, search scope, or permission to use open-access sources — not for a concrete target manuscript — unless they explicitly choose full production fast-track.
