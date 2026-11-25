---
name: subclip-tts
description: Generate persistent speech audio with Subclip AI using live model and voice discovery. Use for narration, voiceover, spoken dialogue, or revisiting generated speech in AI Generations.
---

# Subclip Text to Speech

Follow `$subclip-ai-generation` for quota, credits, async completion, history, and deletion.

For synchronized translation of an existing timeline source, including multi-speaker or temporary voice-clone work, use `$subclip-dubbing`. Do not approximate dubbing with one un-timed narration file.

## Let the creator choose the voice

The creator cannot hear a voice from its name. Unless they named a voice, told you to pick, or the project already has an approved voice, offer samples before generating any voice-over:

1. Call `get_voice_samples` with the voice-over `language` (code or name). `source` is `local` (offline, free to use), `cloud` (Subclip voices; using them spends credits) or `both` (default). Narrow with `gender`, `style`, `voiceIds` and `limit` (default 6, max 12). `text` sets the sentence the offline samples speak, for example one line of the real script. Samples are free: offline ones are made on this computer and cloud ones use Subclip's free preview.
2. Each sample has `voiceId`, `sample.filePath` (a file on the computer running Subclip), sometimes `sample.url` (a temporary link), and inline audio when you pass `includeAudio: true`. Present them however your client can: play them, attach the files, or share the links. List the voices by name and id so the creator can answer with one.
3. If the result says `status: running`, call `get_voice_samples` again with only the `jobId`. Nothing is downloaded by default: when the offline model is not installed, `local.offlineModelMissing` names it (about 190 MB for English, 400 MB for the 31-language model) and the result still has the cloud samples. Downloading uses disk and network, so ask the creator first; if they agree, call again with `downloadModels: true` (`local.downloading` then shows progress; come back in a minute for the offline samples).
   - If a gender or style filter returns nothing, read `notes` and `droppedByFilter`: offline voices carry little gender or style data (English offline voices none), so these filters mostly narrow the cloud voices.
   - With `includeAudio: true`, at most 450 kB per sample and 1.5 MB in total (raw audio bytes) come inline; `inlineAudio.leftOut` lists the voices that did not fit. Their `sample.filePath` still works. Every sample reports `sample.durationSeconds`.
4. When the creator has chosen, call `set_approved_voice` (voiceId, source, modelId, name, language). It is saved with the project and its work trail, and later calls to `get_voice_samples` return it as `approvedVoice`. Keep using that voice; do not choose again.
5. Generate with the tool and arguments in the chosen sample's `use`.

## Cloud speech

1. Call `list_ai_models` with `kind: audio`. Default to the provider/model and voice selected in Subclip system settings. Honor an explicit creator choice; if no selection exists, use the live catalog default. Do not recommend an outside provider or request its API key.
2. Call `list_ai_voices` with the selected `modelId` and useful language, gender, accent, age, source, or search filters. Use the returned stable Subclip voice ID. Never substitute another model because it appeared in an older skill or tool schema.
   - If the creator names Qwen 3, select `qwen3-tts`. It supports preset voices without reference audio; use the live catalog default when the creator has no voice preference.
   - `subclip-voice-clone` is the private saved-voice workflow; keep its provider name out of creator-facing copy. It must not replace ordinary preset speech.
3. Call `generate_speech` once with the exact script. Pass `confirmed: true` when the current request explicitly says to build, create, generate, or regenerate speech with those exact details; that request is confirmation and must not trigger another question. If you propose a different model, voice, or script, show that change and obtain confirmation first. Do not poll.
4. Import completed speech as a normal AudioPanel item. Preserve the operation ID so the creator can regenerate, download, or delete it later.

Only report an approval-policy failure when `generate_speech` itself returns that concrete error. Never infer a block merely because generation consumes credits.

## Offline speech (no credits)

Use this path when the creator does not want to spend credits, or is offline. It runs on this computer with the offline voice model.

1. Call `list_local_voices`. Check `status`: when `installed` is false, call `download_local_voice` (or just call `generate_local_speech`, which starts the download and asks you to retry; about 190 MB). When `speechReady` is false, offline speech is not enabled in this build yet, so use `generate_speech` with a cloud voice and say so. Cloning still works.
2. Pick a voice `id` from the list: a built-in voice such as `alba`, or a cloned voice (`clone:...`) the creator made on this computer.
3. Call `generate_local_speech` with the exact script and `voice`. For a language other than English pass `modelId: "subclip-local-supertonic"` and `language` (31 languages, voices `M1` to `M5` and `F1` to `F5`); `get_voice_samples` returns these arguments ready to use. It needs no confirmation and uses no credits. It returns the WAV `filePath`. Do not poll.
4. Tell the creator where the file is and that it was made offline. Use `generate_speech` only when the creator asks for a cloud voice or a different model.

Cloned voices are made from the AI Assets speech picker (Clone a voice offline): 3 to 30 seconds of clear speech from one speaker, with the creator's permission. Never clone a voice for someone who has not given permission.

## Current model capabilities

Read [model selection and pricing](references/model-selection.md) when selecting a model, quoting credits, supplying references or comparing quality tiers. Live discovery overrides historical model lists.
