## AudioClaw ASR player loop

Use this when the world should react to what the player says, not just to pre-authored state.

Official findings confirmed from AudioClaw-aligned sources:

- AudioClaw exposes a public speech recognition workspace at `/workspace/speech-recognition`.
- The official HTTP API endpoint is `POST https://api.senseaudio.cn/v1/audio/transcriptions`.
- Official open API models are `sense-asr-lite`, `sense-asr`, `sense-asr-pro`, `sense-asr-deepthink`.
- Open API request fields include `file`, `model`, optional `language`, and optional `response_format`.
- Official open API `response_format` supports `json` and `text`.
- The official HTTP API page states a `10MB` file limit.
- The web client uses `/audio/transcriptions` on `https://platform.senseaudio.cn/api`.
- The official web page estimates `30 * durationInSeconds` points for transcription.

Model choice for this skill:

- Default to `sense-asr-deepthink`.
- Reason: this skill benefits from slightly cleaner language understanding for player intent detection, and this model passed real API tests for the current key.

Recommended interactive loop:

1. Player speaks.
2. Run `scripts/senseaudio_asr.py`.
3. Run `scripts/build_npc_reply_from_player.py` on the transcript.
4. Synthesize reply lines with `scripts/batch_tts_scene.py`.

Good fit:

- quest acceptance confirmation
- player asks for clues
- player pushes for urgency
- relation-aware NPC follow-up
