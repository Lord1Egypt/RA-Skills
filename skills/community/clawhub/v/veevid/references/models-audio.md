# Audio models

Text-to-speech, music, speech-to-text and audio cleanup. Results: `video_url` is the audio file; `media_kind` is "audio".

All of these are called with `POST /api/generate-video` using the `mode` and `generation_type` shown. Params marked 💲 change the price — get the exact cost with `POST /api/quote` before generating. Defaults are what the API uses when the field is omitted (not always what the website preselects).

## Index

- Grok TTS — `grok-tts`: `text-to-speech`
- Eleven v4 — `eleven-v4`: `text-to-speech`
- Eleven v4 Turbo — `eleven-v4-turbo`: `text-to-speech`
- Lyria 3.5 (Text to Music) — `lyria-music`: `text-to-music`
- Lyria 3.5 (Image to Music) — `lyria-music`: `text-to-music`
- Scribe V2 — `scribe-v2`: `speech-to-text`
- VEED Clean Audio — `veed-clean-audio`: `remove-background-noise`

## Grok TTS — `grok-tts`

### `grok-tts` · `text-to-speech`

Converts text to speech with xAI Grok TTS, with selectable voice, language and output codec.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** 💲 | string | 1–15000 |  | Text to speak (sent as-is, never auto-translated). Length is counted in characters. |
| `duration` | string | "0" | "0" | Send "0" (audio has no duration input). |
| `voice` | string | "carina", "zagan", "helix", "orion", "luna", "iris", "altair", "zenith", "perseus", "helios", "lux", "kepler", "rigel", "cosmo", "celeste", "ursa", "sirius", "lumen", "castor", "naksh", "atlas", "aurora", "liora", "ara", "eve", "leo", "rex", "sal" | "eve" | Voice name. |
| `language` | string | "auto", "en", "zh", "ja", "ko", "fr", "de", "it", "es-ES", "es-MX", "pt-BR", "pt-PT", "ru", "tr", "vi", "id", "hi", "bn", "ar-EG", "ar-SA", "ar-AE" | "auto" | BCP-47 language; 'auto' = auto-detect. |
| `audio_codec` | string | "mp3", "wav", "pcm", "mulaw", "alaw" | "mp3" | Output format. pcm/mulaw/alaw are headerless raw data (download only, not playable in a browser). |
| `sample_rate` | number | 8000, 16000, 22050, 24000, 44100, 48000 | 24000 | Output sample rate in Hz. |
| `bit_rate` | number | 32000, 64000, 96000, 128000, 192000 | 128000 | Only applies when audio_codec is mp3. The maximum depends on sample_rate: up to 8000 Hz → 64000, up to 24000 Hz → 160000 (so 128000 is the highest allowed value), above → 192000. |
| `seed` | number |  |  | Accepted for backward compatibility; can be omitted. |

Rules:
- prompt is required and must be non-empty after trim; max 15000 characters.
- generation_type must be 'text-to-speech'; text-to-speech only accepts modes eleven-v4-turbo, eleven-v4, grok-tts.
- voice, language, audio_codec, sample_rate and bit_rate must be one of the listed values when provided, else 400.
- bit_rate above the max for the sample_rate (sample_rate defaults to 24000 when omitted) is rejected with 400.
- Eleven-only fields (stability, similarity_boost, audio_output_format, text_normalization, timestamps=true) are rejected with 400.

Result: Async: POST returns {generation_id, status:'processing'}. Poll GET /api/video-generation/{id}/status; when status='completed', video_url is the generated audio file, media_kind is 'audio', and video_metadata gives content_type/file_name/file_size. No lyrics/transcript/timestamps.

Example body:

```json
{"mode": "grok-tts", "generation_type": "text-to-speech", "prompt": "Welcome to Veevid. Let's make something amazing today.", "duration": "0", "voice": "eve", "language": "auto", "audio_codec": "mp3", "sample_rate": 24000, "bit_rate": 128000}
```

## Eleven v4 — `eleven-v4`

### `eleven-v4` · `text-to-speech`

Converts text to speech with ElevenLabs Eleven v4, the higher-quality tier.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** 💲 | string | 1–5000 |  | Text to speak (not auto-translated). Max 5000 characters. |
| `duration` | string | "0" | "0" | Send "0". |
| `voice` | string | "Rachel", "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", "Callum", "River", "Liam", "Charlotte", "Alice", "Matilda", "Will", "Jessica", "Eric", "Chris", "Brian", "Daniel", "Lily", "Bill" | "Rachel" | Preset voice name (case-sensitive). |
| `language` | string | "auto", "en", "zh", "yue", "es", "pt", "fr", "de", "it", "ja", "ko", "hi", "ar", "ru", "af", "as", "ast", "az", "be", "bg", "bn", "bs", "ca", "ceb", "cs", "cy", "da", "el", "et", "fa", "fi", "fil", "gl", "gu", "ha", "he", "hr", "hu", "hy", "id", "is", "jv", "ka", "kk", "kn", "ky", "lb", "ln", "lt", "lv", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "oc", "or", "pa", "pl", "ps", "ro", "sd", "sk", "sl", "so", "sr", "sv", "sw", "ta", "te", "tg", "th", "tr", "uk", "ur", "uz", "vi" | "auto" | ISO 639-1 code (a few 3-letter codes: yue, ast, ceb, fil); 'auto' = let the model detect. |
| `stability` | number | 0–1 | 0.5 | Lower = more expressive, higher = more stable. |
| `similarity_boost` | number | 0–1 | 0.75 | Higher = closer to the original voice. |
| `seed` | number | 0–4294967295 |  | Integer seed; omit for a random seed. |
| `audio_output_format` | string | "mp3_22050_32", "mp3_44100_32", "mp3_44100_64", "mp3_44100_96", "mp3_44100_128", "mp3_44100_192", "opus_48000_32", "opus_48000_64", "opus_48000_96", "opus_48000_128", "opus_48000_192", "pcm_8000", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100", "pcm_48000", "ulaw_8000", "alaw_8000" | "mp3_44100_128" | codec_samplerate_bitrate. opus -> .ogg; pcm/ulaw/alaw are headerless raw files (.pcm/.ulaw/.alaw). |
| `text_normalization` | string | "auto", "on", "off" | "auto" | Whether numbers/dates/abbreviations are expanded before synthesis. |
| `timestamps` | boolean |  | false | Return per-character timestamps in the status response. |

Rules:
- prompt is required and non-empty after trim; max 5000 characters.
- generation_type must be 'text-to-speech'.
- Grok-only fields audio_codec / sample_rate / bit_rate are rejected with 400 (use audio_output_format).
- voice, language, audio_output_format and text_normalization must be one of the listed values when provided, else 400.
- stability and similarity_boost must be finite numbers in [0,1]; seed must be an integer in [0, 4294967295].

Result: Async: poll GET /api/video-generation/{id}/status. On completed, video_url is the generated audio file and media_kind is 'audio'. If timestamps:true was sent, the response also has 'timestamps': an array of word groups like {characters:[...], character_start_times_seconds:[...], character_end_times_seconds:[...]} (only present when non-empty).

Example body:

```json
{"mode": "eleven-v4", "generation_type": "text-to-speech", "prompt": "Welcome to Veevid. Let's make something amazing today.", "duration": "0", "voice": "Rachel", "language": "auto", "stability": 0.5, "similarity_boost": 0.75, "audio_output_format": "mp3_44100_128", "text_normalization": "auto", "timestamps": false}
```

## Eleven v4 Turbo — `eleven-v4-turbo`

### `eleven-v4-turbo` · `text-to-speech`

Converts text to speech with ElevenLabs Eleven v4 Turbo: half the price of Eleven v4, with lower latency.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** 💲 | string | 1–5000 |  | Text to speak (not auto-translated). Max 5000 characters. |
| `duration` | string | "0" | "0" | Send "0". |
| `voice` | string | "Rachel", "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", "Callum", "River", "Liam", "Charlotte", "Alice", "Matilda", "Will", "Jessica", "Eric", "Chris", "Brian", "Daniel", "Lily", "Bill" | "Rachel" | Preset voice name (case-sensitive). |
| `language` | string | "auto", "en", "zh", "yue", "es", "pt", "fr", "de", "it", "ja", "ko", "hi", "ar", "ru", "af", "as", "ast", "az", "be", "bg", "bn", "bs", "ca", "ceb", "cs", "cy", "da", "el", "et", "fa", "fi", "fil", "gl", "gu", "ha", "he", "hr", "hu", "hy", "id", "is", "jv", "ka", "kk", "kn", "ky", "lb", "ln", "lt", "lv", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "oc", "or", "pa", "pl", "ps", "ro", "sd", "sk", "sl", "so", "sr", "sv", "sw", "ta", "te", "tg", "th", "tr", "uk", "ur", "uz", "vi" | "auto" | Same language list as eleven-v4. |
| `stability` | number | 0–1 | 0.5 |  |
| `similarity_boost` | number | 0–1 | 0.75 |  |
| `seed` | number | 0–4294967295 |  | Integer seed; omit for a random seed. |
| `audio_output_format` | string | "mp3_22050_32", "mp3_44100_32", "mp3_44100_64", "mp3_44100_96", "mp3_44100_128", "mp3_44100_192", "opus_48000_32", "opus_48000_64", "opus_48000_96", "opus_48000_128", "opus_48000_192", "pcm_8000", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100", "pcm_48000", "ulaw_8000", "alaw_8000" | "mp3_44100_128" |  |
| `text_normalization` | string | "auto", "on", "off" | "auto" |  |
| `timestamps` | boolean |  | false | Return per-character timestamps in the status response. |

Rules:
- Same validation rules as eleven-v4; only the price differs.

Result: Same as eleven-v4: video_url is the generated audio file; optional 'timestamps' array when timestamps:true.

Example body:

```json
{"mode": "eleven-v4-turbo", "generation_type": "text-to-speech", "prompt": "Welcome to Veevid. Let's make something amazing today.", "duration": "0", "voice": "Rachel", "language": "auto", "stability": 0.5, "similarity_boost": 0.75, "audio_output_format": "mp3_44100_128", "text_normalization": "auto", "timestamps": false}
```

## Lyria 3.5 (Text to Music) — `lyria-music`

### `lyria-music` · `text-to-music`

Generates a music track (about 1-2 minutes, vocals or instrumental) from a text prompt with Google Lyria 3.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string | 1–5000 |  | Music description (style, mood, instruments, tempo, structure). There is no duration parameter; length can only be described in the prompt (observed minimum ~60s). |
| `duration` | string | "0" | "0" | Send "0". |
| `image` | string |  |  | Optional single reference image https URL. |

Input files:
- `image`: Optional, 1 image https URL (jpeg/png/webp, max 10MB; upload it with `POST /api/storage/upload`). Only one image is used.

Upload folders (`folder` for `POST /api/storage/upload`): image → `lyria-music`

Rules:
- prompt is required and non-empty after trim; max 5000 characters.
- generation_type must be 'text-to-music' (and text-to-music only accepts lyria-music).
- image and every entry of images, if provided, must start with https://.
- Prompts imitating real singers or copyrighted lyrics are rejected by the model; unused credits are refunded automatically.

Result: Async: poll GET /api/video-generation/{id}/status. On completed, video_url is the generated music audio file and media_kind is 'audio'. 'lyrics' (string) is present only when the track has vocals; it is raw Lyria markup (section tags like [[A0]], line timing like [12.0:]), so clean it before displaying.

Example body:

```json
{"mode": "lyria-music", "generation_type": "text-to-music", "prompt": "Upbeat lo-fi hip hop with warm piano chords, soft vinyl crackle and a relaxed 80 BPM groove. About two minutes long.", "duration": "0"}
```

## Lyria 3.5 (Image to Music) — `lyria-music`

### `lyria-music` · `text-to-music`

Generates music that matches the mood of a reference image plus a text prompt with Google Lyria 3.5 (image-to-music).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string | 1–5000 |  | Still required. Example: 'Instrumental background music that matches the mood of this image. About one minute long.' |
| `image` | string |  |  | Reference image https URL; the main input for image-to-music (optional at the API level). |
| `duration` | string | "0" | "0" | Send "0". |

Input files:
- `image`: 1 image https URL (jpeg/png/webp, max 10MB; upload it with `POST /api/storage/upload`). Only one image is used.

Upload folders (`folder` for `POST /api/storage/upload`): image → `lyria-music`

Rules:
- Same mode, generation_type, validation and price as the text-to-music entry; there is no separate 'image-to-music' generation_type.
- image must be https; a prompt is still required.

Result: Same as text-to-music: video_url is the music audio file; optional 'lyrics'.

Example body:

```json
{"mode": "lyria-music", "generation_type": "text-to-music", "prompt": "Instrumental background music that matches the mood of this image. About one minute long.", "duration": "0", "image": "https://cdn.veevid.ai/image-to-music/i2m-sample-coffee.webp"}
```

## Scribe V2 — `scribe-v2`

### `scribe-v2` · `speech-to-text`

Transcribes an audio file to text with speaker diarization and audio-event tags using ElevenLabs Scribe V2.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `audio` **required** | string |  |  | https URL of the audio file to transcribe. |
| `input_audio_duration` **required** 💲 | number | 0–3600 |  | Audio length in seconds (must be > 0, max 3600); send the actual length. Billing basis: ceil(seconds/60) minutes, min 1. |
| `duration` | string | "0" | "0" | Send "0". |
| `diarize` | boolean |  | true | Identify speakers. |
| `tag_audio_events` | boolean |  | true | Tag non-speech events like [laughter]. |
| `keyterms` 💲 | array<string> |  |  | Proper nouns/brand names to bias recognition; max 100 items, each non-empty and <=50 chars. Send it only when non-empty; keyterms raise the price. |

Input files:
- `audio`: 1 audio https URL; .mp3, .wav, .m4a, .ogg, .flac, .aac only (video files such as mp4 are not supported). Max 60 minutes; upload with `POST /api/storage/upload` (max 100MB).

Upload folders (`folder` for `POST /api/storage/upload`): audio → `speech-to-text/audio`

Rules:
- generation_type must be 'speech-to-text' and vice versa.
- audio is required and must be an https URL; audios (array) is rejected - single file only.
- If the URL has a file extension it must be one of .mp3 .wav .m4a .ogg .flac .aac; URLs without an extension are accepted.
- input_audio_duration is required, > 0 and <= 3600 seconds.
- keyterms: max 100, each non-empty and <= 50 characters after trim.
- Send `input_audio_duration` equal to the actual audio length (seconds); if it is under-declared, the difference is charged after transcription.
- Failed transcriptions are refunded automatically.
- To quote, send the https `audio` URL and `input_audio_duration` (the quote checks the URL but does not download it).

Result: Async and fast (poll GET /api/video-generation/{id}/status, e.g. every 4s). On completed: 'transcript' object {v:1, language (ISO 639-3 e.g. 'eng', or null), duration (seconds, end of last word), speakers (count), text (full text), cues: [{s: start_sec, e: end_sec, p: speaker_index_or_null, t: text}]}. Note: video_url here is the original source audio URL (not a result file) and is kept for 14 days. media_kind 'audio'.

Example body:

```json
{"mode": "scribe-v2", "generation_type": "speech-to-text", "duration": "0", "audio": "https://example.com/interview.mp3", "input_audio_duration": 95.4, "diarize": true, "tag_audio_events": true}
```

## VEED Clean Audio — `veed-clean-audio`

### `veed-clean-audio` · `remove-background-noise`

Removes background noise from an audio or video file and returns a cleaned, loudness-normalized audio file with VEED Clean Audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `audio` **required** | string |  |  | https URL of the audio OR video file to clean (video: only the audio track is used). |
| `input_audio_duration` **required** 💲 | number | 0–1800 |  | Media length in seconds (must be > 0, max 1800); send the actual length. |
| `duration` | string | "0" | "0" | Send "0". |
| `strength` | number | 0–1 | 0.874 | How much of the original background is kept under speech; suppression floor = 1 - strength (0.874 = -18 dB). Silence between words is always cleaned. |
| `target_lufs` | number\|null | -40–-8 | -19 | Output integrated loudness (LUFS). null = disable loudness normalization (keep original volume); omitted = -19. Gain only, peak capped at -1.1 dBTP so high targets may not be reached. |
| `audio_output_format` | string | "flac", "wav" | "flac" | Output is always 48kHz mono 16-bit |

Input files:
- `audio`: 1 https URL; audio .mp3 .wav .m4a .aac .ogg .opus .flac or video .mp4 .mov .m4v .webm. Max 30 minutes and 512MB (upload it with `POST /api/storage/presign-upload`, see File Uploads). Video without an audio track fails and credits are refunded automatically.

Rules:
- generation_type must be 'remove-background-noise' and vice versa.
- audio is required and must be an https URL; audios (array) is rejected - single file only.
- If the URL has a file extension it must be one of .mp3 .wav .m4a .aac .ogg .opus .flac .mp4 .mov .m4v .webm; URLs without an extension are accepted.
- input_audio_duration is required, > 0 and <= 1800 seconds (30 minutes).
- strength must be in [0,1]; target_lufs must be null or in [-40,-8]; audio_output_format must be flac or wav.
- Send `input_audio_duration` equal to the actual media length (seconds); if it is under-declared, the difference is charged after processing.
- Failed generations (e.g. 'File has no audio track') are refunded automatically.
- To quote, send the https `audio` URL and `input_audio_duration` (the quote checks the URL but does not download it).

Result: Async (processing takes about 0.2-0.35x the media length; poll GET /api/video-generation/{id}/status). On completed, video_url is the cleaned audio file (.flac or .wav) and media_kind is 'audio'. No lyrics/transcript/timestamps.

Example body:

```json
{"mode": "veed-clean-audio", "generation_type": "remove-background-noise", "duration": "0", "audio": "https://example.com/noisy-recording.mp3", "input_audio_duration": 162.3, "strength": 0.874, "target_lufs": -19, "audio_output_format": "flac"}
```
