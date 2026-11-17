# Creative handoff and revisions

Use this lightweight local/session convention when saving planning, connecting modules, reusing material across platforms, or revising a result. It is not a platform project format and does not itself save anything to Vibbit. Simple answers need no full record.

## Common envelope

| Field | Meaning |
| --- | --- |
| `artifact_id`, `revision` | Stable local ID and revision, such as `hook-01`; not a platform resource ID |
| `kind` | Current creative type, such as `brand_master`, `audience_motives`, `hooks`, `storyboard`, `role_sheet`, `keyframes`, or `localization` |
| `context` | Relevant platform, market, language, placement, and product references; omit or flag unknowns |
| `method` | Method ID/version, such as `meta:VB-03`; record distribution platform and generation model separately |
| `source_artifact_ids`, `selected_ids` | Actual upstream sources and selected candidates; do not fabricate user selection |
| `facts`, `assumptions`, `open_questions` | Known information, creative assumptions, and consequential gaps |
| `payload` | The chosen module's complete structure, including role/world/shot-specific fields |
| `production` | Actual steps, media inputs, request/task/result references, review issues, and remaining work |

Facts may include a claim, source URL/asset, observation date, applicable product/market/time, and status: `user_provided`, `source_checked`, `inferred`, or `unverified`. Reading a marketing claim does not independently validate it. A source-check date is not a campaign measurement date.

Store records in the user's project or conversation context, outside the skill. Report platform updates only after a real supported save.

For reusable scripts, talent, or scenes across productions, use [private library records](creative-library.md) and the [save/reuse workflow](../workflows/creative-library.md). The library owns templates and revisions; the current project owns this production's adopted script and selections. Library persistence is not automatic synchronization to a platform project.

## One current basis for production

When [project/run/receipt records](production-plan.md) are useful, keep ownership clear:
- Creative handoff owns facts, reference observations, and the reasons for retaining/replacing elements.
- The project owns the current selected script, production settings, and output dependencies.
- Run selections identify the specific adopted receipts.
- Receipts own file identity, hashes, and declared input fingerprints.
- One existing production/render record owns review coverage, issues, and fixes, linked to the exact receipt/version.

Do not keep independently editable copies of the official script. Audio, storyboards, captions, and API requests derive from the current adopted version. When original audio is the main input, its transcript is derived material and must not replace the original based on recognition errors. Captions follow selected audio and final editing, not estimated reading speed. Independent titles may summarize but must preserve facts. Maintain separate adopted language versions with their source revision.

Selecting “character v2” and “script v3” does not establish compatibility if that performance speaks an older script. Validate the selected combination.

## Creative IDs and media IDs

A `role_id` describes a role; `digital_human_id` comes from an actual resource. A `frame_id` describes a design; asset references identify actual media. A `shot_id` describes editing logic; `task_id` comes from the server.

Record real input/output references and preserve generated/source/analysis_segment/reference/project artifact roles. Unsubmitted work has no task ID or success state. Method names and local stages are not server chat types, step IDs, or task types.

Keep full creative text in the creative/project record. Do not add prompts, full media URLs, or scripts to the redacted client journal. Resume actual tasks/files from current records instead of replaying calls.

## Continuing and revising

Distinguish generated, reviewed, and adopted results, and whether the overall work is complete. Record whether adoption was the user's choice or an authorized creative decision. Keep failed, pending-review, affected, and reusable portions distinct.

Find the original version, requested change, and preserved content. Caption styling usually affects postproduction; a spoken line can affect voice, lip sync, timing, and captions; a character change affects shots using that identity. Preserve previous media until a replacement is usable.

For episodic drama, retain adopted characters, story time, the previous ending, and unresolved events. For reference adaptation, retain actual references and preservation scope. For talking heads, retain identity, tone, script/original audio. Avoid demanding a complete project form for a simple task.

For [novel-to-comic adaptation](../workflows/novel-comic.md), retain stable page/panel IDs, source chapter ranges, exact text types and attribution, character/setting/prop designs, and current story states. Associate each page with reference versions, actual tasks, and adopted images. Revising a page does not renumber IDs or overwrite other pages; comic text does not require speech timing, frame rates, or ASR conventions.

Cross-platform work shares real facts and assets but keeps each platform's brief, placement, hooks, role expression, and revisions distinct. If borrowing a method from another platform, retain its provenance. A missing platform method is not an installed method. Selection fields record decisions; they do not require repeated user approval when autonomous creation is already authorized.

For local rendering, associate the real [template](render-template.md), engine/project, [artifact](render-artifact.md), and review. Local process IDs are not Vibbit task IDs. Only actual cloud steps have cloud task records.
