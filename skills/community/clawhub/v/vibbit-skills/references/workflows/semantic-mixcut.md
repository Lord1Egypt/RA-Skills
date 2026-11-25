# Agent semantic editing and cloud composition

Use to assemble library footage, learn a reference edit, save/reuse a viral-style editing template, or coordinate original sound, avatars, narration and B-roll. A request for one B-roll shot, analysis, or template saving ends at that deliverable. Continue adopted templates/scripts/productions from their missing step. The Agent makes semantic and editorial decisions; material APIs supply media and existing analysis; final trimming, audiovisual assembly, captions, packaging and rendering default to Vibbit `compose`. Do not require a local editor installation or a locally rendered body. Honor explicit local execution and existing local projects.

## Entry and execution requirements

| Available input | Start here |
| --- | --- |
| A finished edit to learn from | Analyze the reference, save a reusable template when requested, produce within the authorized scope |
| Saved editing template | Pin its ID/revision, read applicability, reuse existing analysis |
| Adopted script and material pool | Plan sound/picture, prepare speech, select shots |
| B-roll request only | Find, inspect and deliver the selected shot without producing a full video |
| Existing task or revision | Query its task and selections; update affected dependencies only |

For a new editing style, suggest one finished video the customer likes. Do not ask again for an existing reference or make references mandatory. Without one, design from the brief. Customer media, templates and task records stay in private storage outside the Skill.

Reuse [authentication](../runtime/authentication.md) before actual API operations; planning/local record maintenance needs no key. Before paid intermediates, check that cloud composition can express required source ranges, placement, original sound, separate audio and captions. Follow the public [composition contract](../capabilities/processing/media-composition.md); website-only editing, TTS and timeline endpoints are not public OpenAPI. Preserve exact missing requirements and continue independent preparation without silently rendering locally, dropping original speech or changing presentation.

## Reference edit to reusable template

1. **Resolve the reference and existing evidence.** Fetch library detail, use [external acquisition](../runtime/external-video.md) for share links, and reuse valid direct URLs. Pin the source version. Reuse sufficient saved analysis rather than repeating paid breakdown.
2. **Analyze the editing method.** Use `breakdown` with `hot` for structure, `transition` for shots/cut logic and `asr` for speech and segment timing. A complete new reference normally needs these three; submit only missing relevant analyses. Add `bgm` only when music identification matters. Inspect each sub_result under [breakdown](../capabilities/analysis/video-breakdown.md), retaining task IDs, successes and gaps. Recover the original task instead of resubmitting the entire analysis. Analysis clip URLs are evidence, not newly produced videos.
3. **Derive actionable rules in the Agent.** Inspect actual picture/sound to identify sequence, cut triggers, complete actions, sound across cuts, original speech versus ambience, avatar/B-roll placement, captions and ending. Separate observations, interpretations and template rules. Mark unobserved relationships as missing rather than claiming the API analyzed them.
4. **Save the template.** Use the [creative library](creative-library.md) and [editing records](../contracts/semantic-mixcut.md), keeping `kind=script_template` with new `payload.editing` rules. For an authorized save, persist the revision, update/read back the index, and report its name, ID, revision, location and completeness. Analysis-only requests do not automatically authorize long-term saving. A user's “viral” label is not verified performance data.
5. **Make substitutions explicit.** Product facts, person, language, material pool and actual speech come from the new job. Store relationships such as “show the demonstration while explaining the benefit; cut after the action finishes.” Keep reference seconds as evidence, not new speech/caption timing. Preserve explicitly fixed rhythms separately. An editing template is distinct from a cloud typography/layout template and does not create a server template_id or editable project.

Use the existing CLI: save the real video_url and `sub_tasks:["hot","transition","asr"]` in a request, then run `vibbit.js breakdown --input REQUEST.json`. Existing tasks resume through their original journals.

## Plan speech and picture separately

Inspect what the pool can support before designing the script. Preserve a supplied script and identify its gaps. Plan meaning units: one speech block may use several shots, and one shot may cross caption sentences. Record purpose, adopted speech, speaker, sound source, visual need and material constraints. Keep one authoritative script version.

| Intent | Execution |
| --- | --- |
| Original speech and picture | Select a coherent source interval from real transcription, listen and preserve audiovisual sync; do not add duplicate narration |
| Original speech with B-roll | Keep the original audio and cover appropriate picture intervals without changing the speaker's context |
| Narration with B-roll/images | Reuse or generate adopted narration; mute incidental source speech, declaring any wanted ambience separately |
| Avatar on screen | Drive a real digital_human_id with adopted audio; retain only one audible copy between embedded sound and independent speech |
| Avatar to B-roll and back | Continue the same speech while changing picture; do not regenerate narration or a full performance at every cut |
| Action/ambient sound | Listen to the source; pause or reduce narration according to intent. A caption does not prove the sound exists |

Original sound and narration are audio sources; avatars are visual sources. Do not make them mutually exclusive whole-video modes. Normally keep one primary speech track at a time, with separate music/ambience. Verify cloud support for intentional overlapping dialogue or complex mixing. Lock necessary original speech/action relationships while allowing B-roll to change independently.

Prepare narration in natural speech blocks, not per cut. `generate_audio` can supply clean narration; reuse existing speech. Keep speech, music and effects separate when independent control is needed. The public audio generation command does not expose the website TTS voice_id contract; neither a library person ID nor a voice ID is an undocumented replacement parameter. Check actual reading against the adopted text and obtain real sentence/word timing through [transcript tools](../runtime/transcript-tools.md), without equal character spacing.

Use [digital_human_video](../api/digital_human_video.md) with actual audio_url and avatar ID. Generate needed natural blocks or reuse a complete performance. Partial generation requires real accessible partial audio and a supported preparation path; do not invent trim fields on the avatar API. Check the resulting audio origin and lip sync against the driver rather than assuming zero delay. Keep speech, ASR, avatar tasks and adopted outputs related but separate.

## Agent material matching

1. **Bound the pool.** Retain account site, selected material IDs/groups and exclusions. Batch-check references and read lists/details to build a usable inventory. Unanalyzed files can still be inspected and used; do not wait indefinitely or reimport to trigger analysis.
2. **Inspect progressively.** Read existing descriptions, transcripts, scenes and segments for candidates; inspect selected picture and listen to original-sound candidates. Analysis text cannot prove identity, product variant, action or sound. Cache details/observations and refresh expired addresses only.
3. **Compare in the Agent.** Judge what must actually be visible: entity/variant, action/evidence, usable duration, framing, burned-in captions, context and repetition. Record selection reasons and alternatives rather than inventing universal confidence percentages. If required evidence is missing, adapt the expression or obtain material; generate only authorized missing assets.
4. **Search is optional.** `search_materials` may retrieve candidates; lists, batch lookup and details also support Agent matching within a selected pool. The backend need not make editing decisions. Search has no material_ids filter: intersect results with the allowed IDs, then inspect the pool directly when necessary. An empty intersection does not establish no match, and increasing top_k does not exhaust the pool. No search result also says nothing about unanalyzed files.
5. **Review the whole edit.** Lock required original speech/actions and adopted identity before assigning flexible shots. Check repetition, continuity, product consistency, shot variety and transitions. A 3-second clip for 7 seconds of narration needs another suitable visual or a design change, not automatic looping, freezing or speech speed changes.

Retain material ID, actual media, source interval, role, reason and evidence for each shot. A derived clip's zero point differs from the original source. Use the original file with source times, or verify the derived clip's offset; never apply original timestamps twice to an already trimmed clip.

For large pools, narrow candidates by this task's purpose and allowed groups/tags, read paginated summaries, then inspect a manageable shortlist in detail. Record coverage and unchecked items rather than loading the whole library or claiming a limited comparison is globally optimal. Selection reasons come from the Agent's semantic and visual judgments; a server search score is not an editing-quality score.

## Timeline to cloud render

Finalize timing from adopted audio, separating reference time, estimates and real timing. Follow [editing records](../contracts/semantic-mixcut.md) for independent visuals, sound and captions. `mixcut.js check` checks a basic sequential picture track, 1x source ranges, audio routing and avatar references offline. It does not match materials, compile cloud requests or verify quality.

```bash
node "$VIBBIT_SKILL_DIR/scripts/mixcut.js" check --input /absolute/path/mixcut-plan.json
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" compose --input /absolute/path/compose-request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" compose --input /absolute/path/compose-request.json --state /absolute/path/compose-task.json
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" resume --state /absolute/path/compose-task.json
```

The Agent constructs a separate compose request from supported contracts: real URLs, source ranges, target placement, audio choices, ordinary captions and actual template configuration in `packing_origin` and `video_packing_template`. Local plan fields such as gain, embedded_audio and template beats are not API fields. Verify required effects against documented fields or applicable validated configurations, especially embedded sound selection, per-clip muting, audio placement and gain. Global original_volume does not establish per-clip control. CLI dry-run checks only known structure, not live support. Dynamic subtitle templates remain disabled.

When essential track support is missing, preserve the plan/media and identify the precise gap and available deliverables. Do not submit an approximation that loses original sound or doubles speech, or switch to private website endpoints. Local JSON calculations and template files do not require local rendering. Honor an explicit local route through [production paths](hybrid-video.md), retaining the same audiovisual intent.

Resume the original cloud journal through completion. Inspect the final video for semantic fit, original speech continuity, avatar sync, B-roll cuts, captions, levels, black frames and duplicate voices. Task completion is not quality acceptance. Archive adopted versions through [material reuse](../resources/materials.md) without reimporting already registered media.

For requested Jianying drafts, follow [desktop draft handoff](jianying-draft.md) for the current OpenAPI Job-ID gap and client installation guidance. Without a separate valid ID, retain the adopted output/plan and report export blocked. Only a real ID enables task-prefilled launch and a user save. Track templates, cloud output and local drafts separately; task_id is not a substitute for an editing Job ID.

## Reuse, revisions and recovery

For a new product, pin template ID/revision and supply new facts/pool. Reuse analysis/rules and prepare only the new script, sound, selections and timeline. Templates remain private records; cloud materials/renders do not establish an editable platform project. Each production links template revision, plan, tasks and adopted output. Save an improved method as a new revision when requested; one production must not overwrite the reusable template.

| Change | Scope |
| --- | --- |
| Replace B-roll | Reselect/verify that picture and cloud render; reuse speech and avatars |
| Change a line or voice | Update the affected natural audio block, timing, captions and required lip sync; preserve other assets |
| Insert original sound or change length | Keep valid source ranges, recompute subsequent global placements/captions |
| Change caption style or packaging | Reuse media and timing; change presentation |
| Apply to a new product | Reuse rules and analysis; recheck facts, identity roles, pool and actual audio |

Query existing task IDs before retrying. Save-only work ends at successful readback. Without persistent file tools, deliver template content without claiming long-term storage.
