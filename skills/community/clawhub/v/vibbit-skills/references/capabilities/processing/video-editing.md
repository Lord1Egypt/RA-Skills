# Video slicing, editing, and extension

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Video slicing](#video-slicing)
- [Video editing and extension](#video-segment-edit)

<a id="video-slicing"></a>

## Video slicing

Determine whether the user supplied exact start/end times or wants content-based selection. There is no standalone cloud slicing command.

[Breakdown](../analysis/video-breakdown.md) ASR/transitions can support proposed intervals, titles, and reasons. Actual clip files require available local media tools or verified [composition](media-composition.md) configuration. Keep the number within the user's scope.

If only candidate intervals are ready, deliver a slicing plan. Do not claim clip creation, library storage, or completion of an unsupported platform semantic-slicing task.

Speech-based selections can reuse [audio/video recognition](../analysis/speech-transcription.md) and sentence candidates from [keyword location](../../runtime/transcript-tools.md). Captions and candidate clips share source evidence. The host performs semantic selection, followed by listening/viewing boundary checks; supplied cut times without content-analysis needs require no extra ASR.

<a id="video-segment-edit"></a>

## Video editing and extension

Distinguish generative editing, continuation, and precise replacement of a selected platform-project clip. The first two use public Seedance 2.5; project selection/version writeback is not publicly defined.

For an existing-video correction, first use [video review](../analysis/video-review.md) to choose reliable local processing or generation of affected intervals, then splice the result into the complete video to conserve credits. Input clips may include necessary model-compliant context; record the adopted replacement interval separately. Prompted second ranges do not trim the actual input.

Default paid editing, extension, and localized regeneration to 720p under [paid video settings](../generation/video-generation.md#paid-video-settings). Higher-resolution bases or old requests do not raise generation resolution; reuse an explicit user requirement without asking again.

For facial-feature/hair changes or an unchanged-face report, prepare the target appearance and anonymized motion reference through [facial identity replacement](../../workflows/face-identity-replacement.md), then retain the current editing, sound, and splitting requirements instead of merely strengthening the old prompt.

For person, product, or scene replacement, use [1:1 remake](../../workflows/one-to-one-remake.md). Skip repeated selection when inputs are already clear, but still follow its audio and splitting rules: submit real silent video for unchanged dialogue/BGM and restore the original audio afterward; preserve audible source video for audio changes; split videos over 30 seconds into separate 4–30-second edits and then assemble. Continue subsequent language changes through that workflow using the adopted visual version.

Follow [2.5 editing/extension](../../models/seedance-2.5.md#editing-and-extension) and [Seedance API](../../api/seedance.md). For edit, supply the original video and explicit changes while respecting ratio/duration constraints. For extend, define direction, new content, and added-versus-total duration. Inspect whether the actual output includes the original; do not fabricate combined URLs.

Prompted second ranges remain generative guidance, not frame-accurate project editing. Without a supported project/work save contract, deliver new media or a plan and do not claim platform writeback or lossless preservation.
