# Digital human video

Use an existing digital human ID and actual audio URL with [digital_human_video](../../api/digital_human_video.md). A local file must first be uploaded to obtain an object URL; a local path or upload credential is not media input.

Reuse an accessible supplied URL or audio already generated in this task. Do not force transcription, voice selection, cloning, or new speech when the user wants the original audio. For text-only requests, use [talking-head production](../../workflows/oral-broadcast.md) to generate the selected script's audio first.

Library audio can also drive the avatar: use [material reuse](../../resources/materials.md) to read its actual URL and verify content, format, and voice before passing audio_url. A selected ID needs detail, not another search, upload, or speech generation. When only the vocal style is reused for new lines, generate and adopt the new speech from that reference first.

A library avatar video already matching the current identity, lines, and sound can be reused without regeneration. Retain it for caption/B-roll/music edits under [talking-head material reuse](../../workflows/oral-broadcast.md#material-reuse-for-avatar-only-and-avatar-with-b-roll-videos); avatar-only requests do not gain mandatory inserts. A person material_id is not digital_human_id, and a video URL is not the driver audio URL.

When script checking or caption timing is needed, use [audio transcription](../analysis/speech-transcription.md) on that audio URL. Resolve speech-check uncertainties before rendering; reuse unchanged approved audio and applicable transcripts.

A complete valid resource ID can be used without listing resources. A uniquely matched name can proceed; resolve ambiguous names. Keep 64-bit IDs as strings. A tryout does not imply a new avatar or platform project.

For a list selection, bind the original record's name, ID, and cover and verify the match once before submission; do not reconstruct the mapping manually. Adopt audio before submission and resolve known speech defects first. Reuse applicable checks, while inspecting the actual output's identity and lip sync through [review](../analysis/video-review.md).

Resume an existing task by its ID and inspect the actual result for appearance and lip sync. See [task lifecycle](../../runtime/task-lifecycle.md).

When captions or speech checks are needed, use [transcript tools](../../runtime/transcript-tools.md) to preserve one adopted-audio record, export captions, or compare speech. Reuse an applicable saved result and listen before choosing a correction scope.
