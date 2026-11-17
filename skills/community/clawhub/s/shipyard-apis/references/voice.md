# Voice: speech to text (Deepgram) and text to speech (ElevenLabs)

Shipyard's video skill already uses Deepgram and OpenAI voices for narration (`video-voice.mjs`), so the keys and checks are proven. Using them inside an app's own routes is **new, untested in production**.

## Speech to text: Deepgram (`DEEPGRAM_API_KEY`)

- Pre-recorded audio: `POST https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&language=<code>`, header `Authorization: Token <key>` (Token, not Bearer), body = the audio bytes with its `Content-Type`. Text is at `results.channels[0].alternatives[0].transcript`.
- Cheaper fallback with a free tier: Groq Whisper (`POST https://api.groq.com/openai/v1/audio/transcriptions`, OpenAI format, model `whisper-large-v3-turbo`).
- Live microphone streaming needs a WebSocket and a short-lived token made on the server; never send the main key to the browser.

## Text to speech: ElevenLabs (`ELEVENLABS_API_KEY`)

- `POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>?output_format=mp3_44100_128`, header `xi-api-key: <key>`, JSON `{"text": "...", "model_id": "eleven_multilingual_v2"}`. The answer is the MP3 bytes. List voices with `GET /v1/voices`.
- Charged per character: cap text length per request (for example 1,000 characters) and cache the audio for repeated text (Supabase Storage).

## Rules

- Both run in a server route: signed-in user, rate limit, size limit (audio at most about 25 MB or a few minutes).
- Say in the privacy page that audio or text is sent to Deepgram or ElevenLabs (`legal-generate.mjs` after adding the keys).
- If the key is missing or the call fails, the app shows the text box or the written text instead.
