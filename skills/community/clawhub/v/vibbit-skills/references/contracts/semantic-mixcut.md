# Editing templates and audiovisual plans

Use with [Agent semantic editing](../workflows/semantic-mixcut.md). These are private file conventions, **not OpenAPI or website project schemas**. The Agent analyzes/matches, while final editing defaults to cloud compose.

## Template extension

Keep the [creative-library contract](creative-library.md): `kind=script_template`, stable ID, revision, sources, assets and payload. Existing templates remain valid. Editing templates add tags and optional `payload.editing`; they are not cloud packaging templates.

| editing field | Meaning |
| --- | --- |
| version | Extension version 1 |
| render_target / matching_executor | vibbit_cloud / agent |
| reference_times_are_output_timing | false; source times are evidence |
| beats | Stable id, purpose, visual_need, audio_mode, cut_trigger, material_requirements; relate to script segments |
| audio_rules | Primary speech, original sound/ambience, music ducking and avatar continuity |
| selection_rules | Pool constraints, observation, repetition and missing-asset handling |
| variables / applicability | Product/language/person variables and conditions; may reuse existing payload definitions |

sources retain actual reference identity, observation scope, breakdown task IDs, subtask status and private analysis files. Failed/unobserved analysis stays incomplete. Save original speech/time separately from reusable rules. [mixcut-template.json](../../examples/mixcut-template.json) is a fictional draft, not a verified viral case.

Use host file tools to write a revision, update library.json and read both back. Pin ID+revision for production. Usable status is not a performance guarantee. Saving a template does not upload every reference. Durable media references use real material IDs/account scope or persistent files rather than only expiring signatures.

## Production plan

Save the plan alongside existing project/run/receipt records, reusing authoritative script and output references. [mixcut-plan.json](../../examples/mixcut-plan.json) demonstrates original sound, narration, avatars and B-roll. Its URLs/IDs are placeholders, not production inputs.

- Top-level version=1, kind=semantic_mixcut, render_target=vibbit_cloud, matching_executor=agent; account_site is cn/global and duration_seconds is the actual intended duration.
- Optional template_ref pins id+revision. material_scope.material_ids bounds directly selected library media; newly generated outputs use generated origin rather than pretending to belong to the original pool.
- Each asset has stable id, media_type VIDEO/IMAGE/AUDIO, origin material/generated/upload and a real url. Video/audio also has measured duration_seconds. Material origin requires a real material_id within the pool. Runtime account checks remain necessary; the validator never queries accounts.
- audio_clips have id, asset_id, role speech/ambience/music, source_kind original/narration/provided, source_in/source_out, final start/end and gain (linear volume intent). Sources can be audio or a video's audio stream. The latter requires supported cloud audio routing; do not invent an extracted audio_url.
- visual_clips have id, kind material/avatar/image, asset_id, final start/end, purpose, selection_reason and evidence. Videos have source_in/source_out; images have no source time.
- Each visual declares embedded_audio=mute. Every wanted sound is explicitly listed in audio_clips, including original video sound. This local representation prevents duplicate playback; it is **not a new cloud field**. A verified cloud implementation may instead retain embedded audio once when that exactly implements the declared route.
- Avatar visuals reference the audible speech clip using speech_audio_id. The avatar asset's driven_by identifies the driver audio asset_id and offset_seconds (driver time corresponding to avatar video time zero). Inspect/measure the actual output mapping instead of assuming zero. Validation compares declared timing; it does not verify lip sync.
- captions have id, audio_clip_id, start/end and text, bound to actual audible speech. The Agent/transcription checks text; the validator only checks ranges. Original speech and narration captions refer to their own audio clips.

The helper supports one contiguous primary picture track, 1x source intervals and nonoverlapping primary speech; music/ambience may overlap. Validate complex overlays, speed changes, crossfades or intentional overlapping dialogue separately against supported cloud contracts. Do not falsify a simple plan to pass. Recheck actual media/timing after trimming or speed changes.

```bash
node "$VIBBIT_SKILL_DIR/scripts/mixcut.js" check --input /absolute/path/mixcut-plan.json
```

plan_valid only reports basic consistency of supplied data and lists required_cloud_features. submitted, cloud_request_verified, media_checked and semantic_quality_checked remain false. The tool reads the plan only: no media inspection, semantic search, template persistence, network, rendering or cloud payload compilation. It does not establish truthful provenance. Correct real records identified by issues rather than deleting required shots to bypass validation.

## Cloud handoff and versions

Construct supported packing_origin and video_packing_template separately, preserving official field casing. Check required_cloud_features against actual fields or applicable validated requests, retaining the evidence and scope. A valid local plan does not establish cloud executability. Dry-run, submit compose within the existing scope, and query the original journal until actual media is available.

Retain template revision, adopted script/speech, media/segments, source/final times, observation evidence, cloud request and task/render references. Preserve durable IDs and recoverable sources; URLs can refresh. A B-roll change does not invalidate unchanged audio; a voice change affects captions, lip sync and downstream placement. Save reusable template revisions separately from production instances.
