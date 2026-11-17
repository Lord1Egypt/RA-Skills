# Digital human video

Use an existing digital human ID and actual audio URL with [digital_human_video](../../api/digital_human_video.md). A local file must first be uploaded to obtain an object URL; a local path or upload credential is not media input.

Reuse an accessible supplied URL or audio already generated in this task. Do not force transcription, voice selection, cloning, or new speech when the user wants the original audio. For text-only requests, use [talking-head production](../../workflows/oral-broadcast.md) to generate the selected script's audio first.

When script checking or caption timing is needed, use [audio transcription](../analysis/speech-transcription.md) on that audio URL. Resolve speech-check uncertainties before rendering; reuse unchanged approved audio and applicable transcripts.

A complete valid resource ID can be used without listing resources. A uniquely matched name can proceed; resolve ambiguous names. Keep 64-bit IDs as strings. A tryout does not imply a new avatar or platform project.

For a list selection, bind the original record's name, ID, and cover and verify the match once before submission; do not reconstruct the mapping manually. Adopt audio before submission and resolve known speech defects first. Reuse applicable checks, while inspecting the actual output's identity and lip sync through [review](../analysis/video-review.md).

Resume an existing task by its ID and inspect the actual result for appearance and lip sync. See [task lifecycle](../../runtime/task-lifecycle.md).

When captions or speech checks are needed, use [transcript tools](../../runtime/transcript-tools.md) to preserve one adopted-audio record, export captions, or compare speech. Reuse an applicable saved result and listen before choosing a correction scope.
