# Project definition, execution intent, and selected artifacts

Use this local convention for multi-step production, focused rework, and reproducible reuse. Simple generation does not need a project. It extends [creative handoff](creative-handoff.md); it is not a Vibbit API schema or platform project format.

| Record | Responsibility |
| --- | --- |
| `project.json` | Current adopted script, semantic events, production configuration, outputs, and dependencies |
| `run.json` | Project reference, current targets, selected historical artifacts, media placement, and word-timing evidence |
| `receipt.json` | A real artifact, declared provenance, file hash, and fingerprint of its declared inputs |

Names are flexible. Store files in the creative project, outside the skill. One project can have separate preparation, preview, and final-export runs.

## Project

Use `version: 1` and a stable local `id`.

- `script`: segments keyed by ID; `speech` contains actual spoken text, with optional separate `display` text.
- `direction`: current performance, style, model/template, and other project-specific settings.
- `frame_rate`: positive frame rate used for event conversion, matching the renderer.
- `events`: stable `id`, `segment`, exact `quote`, `type: moment/range`; repeated phrases use one-based `occurrence`; moments may specify `edge: start/end` and `offset_seconds`.
- `outputs`: maps output IDs to definitions.

Each output declares `kind` (video/audio/image/data), `uses` (actual project field paths), `depends_on` (upstream output IDs), `files` (request JSON, render code, template config, events, and other actual local dependencies), and `recipe`. Recipes use `tool: vibbit` with an existing `command`, or `tool: local` with a concrete `instruction`. The planner neither executes code nor submits requests.

Separate script dependencies from visual styling so styling changes can preserve performance. File contents are hashed. Declare fonts, code, configuration, and external inputs that affect output; the tool cannot infer undeclared dependencies from prose or replace the engine's build system and lockfile.

## Run and receipts

Use `version: 1`, a project path relative to the run, unique `targets`, and `selections` mapping output IDs to exact receipt paths. Never silently select the newest file.

[The local tool](../runtime/local-production.md) creates receipts from real files, retaining project/output IDs, fingerprint, path/hash/size, and optional real task/result provenance. Supplied provenance does not establish server verification or quality acceptance. Match the selected file to the actual returned result.

Review before adoption. Recording creates a candidate, not a selection. Write new receipt/revision files and preserve old media. Record and select the upstream artifacts actually used before recording downstream output.

Downstream fingerprints include upstream input fingerprints and selected file hashes. Changed scripts, settings, declared files, or selected media invalidate affected selections. Report conflicts and revise selections within authorization; never silently restart paid generation.

New receipts contain an `input_manifest` of declared field, file, dependency, and output-definition hashes, not copied scripts/prompts. Older receipts can still be reused by fingerprint, but missing historical summaries cannot be reconstructed. `explain` reports reuse/execute/blocked and propagates blocking dependencies without clearing selections. Normal `plan` still rejects invalid selections or missing files; cycles and invalid references are structural errors.

If existing media remains suitable despite a changed description, inspect it and create a new adoption record for current inputs with the reason. Do not edit an old fingerprint to bypass checks.

## Timing

`run.timing` maps script segment IDs to an adopted `output`, a local word-timing `evidence` file matching its media hash, and explicit `at_seconds` placement.

Binding currently supports shifting complete segments, not post-binding trimming, speed changes, crossfades, or mixed clocks. Prepare the final selected segment and obtain fresh evidence first when those changes are needed. Segment-level ASR is not word evidence. See [script and timing](../creation/script-and-timing.md).

## Execution and recovery

An existing task ID or local running process must be checked before resubmission. The planner only knows local declarations, not unrecorded account tasks.

`plan` lists reuse and execution needed for the targets. The host verifies the plan, calls existing CLI/render tools, records actual outputs, and continues downstream. It is not a background scheduler and does not guarantee shutdown recovery or automatic retries. Fingerprint validity does not replace [media review](../capabilities/analysis/video-review.md).
