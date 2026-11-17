# Voices

There is no public standalone voice-listing or voice-cloning command. Ordinary speech generation uses a text prompt and does not require a voice ID. Audio references influence generation; they do not create a reusable voice asset.

Digital-human listing may return `voice`, but its public fields include no voice-preview URL and audio generation accepts no `voice_id`. Do not treat that field as a selectable TTS voice or reference material. Show a genuine existing preview when supplied with established meaning. For a voice reference, use a real audio-library ID; a local-file upload only returns an object URL and does not register it as reference material.

Reuse existing audio when the user wants to preserve it. For an explicitly supplied voice resource, retain its real fields and ID. Prefer an existing preview to generating an extra paid sample; additional generation needs appropriate authorization. See [audio generation](../capabilities/generation/audio-generation.md).
