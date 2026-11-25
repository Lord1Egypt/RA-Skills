---
name: subclip-avatar-generation
description: Generate a persistent talking-avatar video with Subclip AI from a saved avatar, a Subclip AI Actor, or a project portrait, speaking a typed script or supplied speech audio. Also saves custom avatars. Use for presenter, spokesperson, UGC or character avatar requests that should appear in AI Assets.
---

# Subclip Video Avatar Generation

Follow `$subclip-ai-generation` for quota, credits, async completion, history, import, and deletion.

## Choose who appears

1. Call `list_ai_avatars`. It returns the user's saved avatars (custom presenters with looks) and Subclip AI Actors. Every actor has the same looks: `home`, `selfie`, `greenscreen-vertical` (9:16) and `office`, `desk`, `side` (45° second camera), `greenscreen-horizontal` (16:9). Match the look's aspect ratio to the project.
2. Pass the choice to `generate_ai_media` as `avatar: { actorId, lookId }` or `avatar: { avatarId, lookId }`. Do not also attach a portrait image.
3. To use a portrait that is already in the project instead, resolve it with `list_editor_assets` and pass it in `sourceAssets` with role `reference`.
4. To keep a presenter for later, call `create_ai_avatar` with a project image (`sourceFileId`) or an AI Actor copy (`actorId`) and a name, with `confirmed: true` only when the user asked to save it. Saved avatars sync with subclip.app.

## Choose what they say

- Script: pass `speech: { text, modelId, voiceId, languageCode }`. Get `modelId` and the stable `voiceId` from `list_ai_voices` (expanded models such as ElevenLabs, Gemini, MiniMax, Inworld TTS 2, or the user's saved voices with `subclip-voice-clone`). An actor's `defaultVoice` is a good default. The server speaks the script, then animates the avatar in the same job, so nothing is lost if the editor reloads.
- Supplied audio: attach a speech track in `sourceAssets` with role `audio_reference` and omit `speech`.
- `prompt` always describes movement and expression, never the spoken words.

## Models and credits

Call `list_ai_models` with `kind: avatar` and choose an available model. Pruna AI P-Video Avatar is the default and most affordable; HeyGen Avatar IV, Kling Avatar v2 and OmniHuman 1.5 animate a portrait with speech; Kling Lip Sync needs an existing video plus audio. Read [model selection and pricing](references/model-selection.md). A script's credits are the voiceover plus the video at the voiceover's length; the server reserves a padded estimate and settles at the real length.

Avatar creation is asynchronous. After the operation is accepted, preserve its operation ID and end the turn without polling. Import the completed result as a normal MediaPanel video.
