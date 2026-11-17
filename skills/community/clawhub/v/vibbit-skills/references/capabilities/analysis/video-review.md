# Video review and focused revisions

Review the real selected file and version with the host's available viewing/listening tools. Server completion, file existence, a source preview, or a quality score does not establish that the video satisfies the request.

For a short video, inspect it end to end when possible. For a long one, cover the opening, key claims/actions, text, changed intervals and adjacent transitions, and ending. State the actual coverage. Probe the exported file's duration, dimensions, tracks, and transparency where relevant.

Check:
- Intent, product facts, identity, appearance, and selected script.
- Motion, visual continuity, and reference adherence.
- Audible speech, pronunciation, subtitle timing, lip sync, and levels.
- Information order, pacing, layout, readability, and output specifications.

A transcript supports text review, stills support appearance review, and neither proves motion or lip synchronization. Do not claim to have watched or listened when those tools were unavailable. Paid analysis is not an automatic prerequisite.

## Reuse checks across stages

Bind conclusions to the media version and actual coverage. Reuse unchanged speech, avatar-selection, and metadata checks; references to this review from multiple workflows do not require separate full reviews. Do not download, probe, or transcribe the same unchanged asset repeatedly. Final composition still needs checks for new captions/visuals, volume changes, and audio/video relationships; earlier checks cannot prove a new export is correct.

ASR identifies passages to investigate. Listen before distinguishing recognition mistakes from actual omissions or repetition; agreement between recognizers is not listening evidence. When listening is unavailable, report the gap instead of regenerating solely on recognition results. Routine work uses [existing transcription](speech-transcription.md) and host capabilities, without installing another model just to cross-check.

After a necessary review identifies a concrete defect, repair the affected object and recheck it and adjacent transitions. Deliver once requirements and necessary checks pass; do not add validation or aesthetic iterations without a concrete unresolved issue. Conversely, a nominal review-count limit is no reason to hide a remaining defect.

## Revise the responsible layer

Tie each issue to its actual version, time, and evidence. Distinguish an execution failure, a content defect, and a new preference. Revise the responsible layer: creative structure/script; voice and dependent lip sync/subtitles; local caption/volume/crop/trim; or the affected generated asset. Baked-in subtitles may require removal or regeneration and are not guaranteed lossless.

Reuse existing production records, inputs, and approved unaffected parts. Preserve the prior version until a replacement is usable. Proceed with authorized routine revisions; additional paid generations must stay within the authorized count and budget. Recheck the changed portion and its neighbors for regressions. Stop when the requested result is achieved or report the concrete capability/authorization blocker. Do not infer expected views from a subjective review score.

## Prefer localized repairs to conserve credits

For revisions of an existing video, minimize rework across all video workflows while meeting the requested quality and user-specified model, resolution, and product fidelity. Default paid regeneration to 720p under [paid video settings](../generation/video-generation.md#paid-video-settings). A 1080p base or old request is not a user requirement and must not automatically raise the generation resolution.

1. **Fix the selected version and locate every occurrence.** Identify the affected object, observed source times/frames, and preserved elements in the currently adopted video. Check the same defect in close-ups, wide shots, turns, and occlusions. Reuse adopted references, product evidence, and task records; do not revert to an unadopted version.
2. **Prefer reliable local processing when feasible.** Available source projects or tools may handle captions, volume, cut points, localized color correction, or logo removal. Check representative frames or a short sample for edges, occlusion, and continuity. Change approach when repair artifacts are evident rather than repeatedly polishing an ineffective technique. Blur, concealment, or damaged product details do not establish a successful repair. Use a supported alternative when tools are unavailable without requiring installation.
3. **Generate only affected intervals.** Cut the faulty intervals from the current video with necessary context. Merge nearby issues when that reduces requests or generated duration while preserving continuity; handle distant issues separately when appropriate. Reuse acceptable footage. Expand the scope only for a global change or a concrete limit of localized repair, and explain the reason. Continue within existing authorization; ask only when expanding beyond the authorized changes or cost, without confirming each already specified defect.
4. **Separate input context from adopted replacement intervals.** Respect the selected model's real minimum and maximum clip lengths and use suitable cuts or action pauses. Seedance 2.5 edit requires at least four seconds of input; see the [API](../../api/seedance.md) for full constraints. A brief defect may need a longer context clip, but only the needed portion must be adopted. Probe the exported clip's actual duration, frame count, and streams instead of trusting trim arguments. Extend an undersized input with real adjacent footage rather than inventing context. Record source start/end frames or times, submitted context, adopted interval, final placement, and a separate task journal for each repair.
5. **Limit visual and audio changes.** State exactly what changes, each reference's role, and which person, other product details, scene, actions, and shots remain. Keep the user's selected model and resolve resolution under the paid settings above, recording it separately from local assembly dimensions. For visual-only changes, follow [precise replacement audio routing](../../workflows/one-to-one-remake.md): submit a genuinely silent clip, preserve the complete original soundtrack, assemble the visuals, then restore that soundtrack once on its source timeline. Do not regenerate sound or restart music per segment. For requested dialogue or voice changes, update the affected sound, lip sync, and caption dependencies while preserving the rest; do not overwrite adopted new sound with the original.
6. **Align and splice into the full video.** Inspect actual generated duration and action timing, map the adopted interval to the source timeline, and join it to unaffected footage. Match codecs, aspect ratio, frame rate, and time base as needed; stream-copy cuts may be constrained by keyframes. Recheck movement, mouth timing, opening, and ending after necessary localized picture alignment. Do not hide mismatches with `-shortest` or arbitrary stretching of the original audio. Retain results and resolve specific differences when alignment is unreliable rather than declaring success. See [local composition](../processing/local-composition.md).
7. **Review and deliver the complete result.** Check all relevant appearances of the repair, the requested color/text/object correction, and person, fabric, action, brightness, and sound continuity around each join. Verify final specifications, duration, ending coverage, and audio tracks. Deliver the assembled final video when that is requested, preserving prior versions and reusable clips. State actual review coverage when only stills are available; task completion does not prove visual acceptance.

Use existing production records for actual inputs, task IDs, adopted outputs, request counts, and generated duration. Recover uncertain tasks through their original [journals](../../runtime/task-lifecycle.md) rather than submitting a new ID after a timeout. Investigate failed or inadequate segments, retain successful ones, and avoid blind batch retries within the existing count, budget, and revision authorization.

Reduce the scope and number of paid generations first. Ordinary trimming and joining require no additional Vibbit generation calls. Report actual repair counts and submitted duration when useful, but do not convert a duration ratio or local processing into an exact credit saving without real billing evidence.

See [creative handoff](../../contracts/creative-handoff.md) and [production planning](../../contracts/production-plan.md).

[Speech difference reports](../../runtime/transcript-tools.md) provide listening leads; text agreement is not acoustic acceptance. Reuse recognition and verified review scope by source version. Caption files, candidate ranges, and reuse reports do not establish that the final video is synchronized or cut.
