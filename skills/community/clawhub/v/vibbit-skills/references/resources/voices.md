# Voices

There is no public standalone voice-listing or voice-cloning command. Ordinary speech generation uses a text prompt and does not require a voice ID. Audio references influence generation; they do not create a reusable voice asset.

Video translation preserves original voices by default. For an explicit replacement request, follow [voice intent and scope](../capabilities/processing/video-translation.md#voice-intent-and-scope) and explain unified versus targeted changes. At creation, default_voice.reference_audio_url accepts an MP3 URL from generic upload, not audio_id or a video-level override. Existing tasks can also use their task-scoped audio uploader for speaker bindings.

Digital-human listing may return `voice`, but its public fields include no voice-preview URL and audio generation accepts no `voice_id`. Do not treat that field as a selectable TTS voice or reference material. Show a genuine existing preview when supplied with established meaning. Audio generation accepts an uploaded object_url directly in reference_audio_urls, without material registration; real audio-library IDs remain supported.

For an existing translation task, [translation voice revisions](../api/translation-revision.md) bind a reference MP3 or real audio_id to an ASR speaker. Preserve all other bindings, retry affected speech and render only the needed language. This does not create or list reusable voice assets and does not replace the visible performer.

Reuse existing audio when the user wants to preserve it. For an explicitly supplied voice resource, retain its real fields and ID. Prefer an existing preview to generating an extra paid sample; additional generation needs appropriate authorization. See [audio generation](../capabilities/generation/audio-generation.md).
