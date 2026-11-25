# Video localization

For specified library videos or historical works, use [material reuse](../resources/materials.md) to find, batch-check and read the adopted source URL, supplying its real material_id to translation when available. Keep source material/visual version → child task/language → actual output/material relations. Revisions resume the original translation task; a material ID alone is not a reason to create another full batch.

Distinguish text translation, automatic dubbed video, reviewed translation before rendering, and broader market adaptation. Reuse adopted media and languages without automatically adding assets or variants.

Acquire platform links through [shared video input](../runtime/external-video.md). Preserve each original voice by default. For an explicit replacement, follow [voice intent and scope](../capabilities/processing/video-translation.md#voice-intent-and-scope), select a global default or targeted mappings and explain actual coverage before submission.

- Text only: translate through the host, with no media-generation job.
- Dubbed video with optional captions/lip sync: [video translation](../capabilities/processing/video-translation.md), explicitly `auto_translate: true`.
- Review first: the same capability with false, using actual public review content/stage before update/confirm.
- Change translated voices or correct a few sentences: [translation revisions](../api/translation-revision.md), preserving all speaker bindings still needed, retrying affected speech and rendering only that language.
- Replace people/objects/scenes and translate: [1:1 remake](one-to-one-remake.md), then the adopted edited video and correct source audio.
- Additional visuals/animation/assembly after translation: get the final translated output, then [hybrid production](hybrid-video.md).
- Target audio and timed captions already exist: reuse them directly for postproduction.

Never send the original visual version after a replacement has been adopted. Adding a language reuses the current visual version; changing a person after translation requires new lip-sync/visual review. Translation can bind voices to ASR speakers; it does not create standalone voice assets, replace the visible performer or edit projects. Language rendering assembles existing valid audio and does not fill missing TTS.

Upload local video to a readable URL instead of passing a file path. For text-only translation of speech, transcription can supply the source.

Check languages, terminology/brand names, caption choices, original-caption removal, and lip sync. Translation can directly produce a final video without an extra compose task. Use real ordinary packaging IDs with template_type=0 if needed, avoiding duplicate packaging. Dynamic subtitle templates are temporarily unavailable.

Deliver source → language → final video mappings. Check every requested child/language/final URL, preserve successes, and report failures separately. Only authorized missing portions need new tasks. Review accuracy, pronunciation, timing, lip sync, readability, and visuals; completion state is not quality acceptance.

For a revised render, resume its operation journal and match the exact child, language and business request_id receipt. A completed parent or old video is not a new delivery. Continue authorized review/postproduction after the new final output arrives. Use delivered language captions/snapshots rather than an edited draft as evidence for old media.

For a Meta ad's market/persuasion adaptation, use [VB-07](../platforms/meta/localization.md#localization) to establish evidence and a change table before choosing translation or recreation. Plain language replacement does not require the full advertising method suite.

Do not force additional ASR when the complete video translation task handles target speech/captions. For audio-only input, use [audio content workflows](audio-content.md): recognition, host translation/adopted speech, new audio, then checks/caption export as needed. New-language audio needs its own timing. For source/target subtitle files alone, use [transcript tools](../runtime/transcript-tools.md) without first producing another video.
