# Zvukogram API — agent reference

Source (official): https://zvukogram.com/node/api/

This doc is the **practical contract** for calling Zvukogram HTTP API. It focuses on what an agent needs: which endpoint to pick, key parameters, limits, and response fields.

Base URL:

- `https://zvukogram.com/index.php?r=api`

Endpoints used most:

- `POST/GET .../text`
- `POST/GET .../longtext`
- `POST/GET .../subs`
- `POST/GET .../result`
- `GET .../voices`
- `POST/GET .../balance`
- `POST/GET .../delete`

## 1) Authentication (required everywhere)

Every request must include:

- `token` — your API key (from личный кабинет)
- `email` — account email

Transport formats supported (pick any):

1) `POST application/x-www-form-urlencoded` (most common)
2) `POST application/json`
3) `GET` query params

## 2) Which method to use: /text vs /longtext vs /subs

### `/text` (1 step)

Use when:
- You need **fast** results for **short text**.

Hard limit:
- `text` max **1000 characters** per request.

Behavior:
- Response is JSON with a direct `file` URL immediately.

### `/longtext` (2 steps)

Use when:
- Text is **long** (up to **1,000,000 characters**) OR you want server-side chunking/queue.

Behavior:
1) Send to `/longtext` → get `id`, `status=0`
2) Poll `/result` with that `id` until `status=1` (ready) or `status=-1` (error)

Polling guidance from docs:
- every **2s** for short texts
- every **5s** for very long texts (books)

### `/subs` (2 steps + subtitles/timecodes)

Use when:
- You need **timed cuts** / subtitles alignment for video/presentations.

Works like `/longtext`, but `/result` additionally includes:
- `cuts` — array of fragments (links) when using `/subs` (also mentioned with “obrezka” tag in docs)

Extra params specific to `/subs`:
- `speed_type` (int: 1 or 2)
- `speed_floor` (int)

If you don’t need timecodes, prefer `/text` or `/longtext`.

## 3) Common request parameters

### Required

- `token`
- `email`
- `voice` — voice name, e.g. `Matthew plus`, `Мартын` (see `/voices`)
- `text` — input text (plain text or SSML-inline text)

### Voice / expressiveness

- `speed` (float, default `1`): **0.1 … 2.0**
  - 0.8 slower, 1.3 faster
- `pitch` (int, default `0`): **-20 … 20**
- `style` (string): voice style (not supported by all voices)
  - docs mention examples like `newscast`, `cheerful`, `sad`
  - legacy name `emotion` still works
- `styledegree` (string/number): intensity of the style; works only with `style`
- `role` (string): voice role, e.g. `YoungAdultMale`, `OlderAdultFemale` (voice-dependent)

### Pauses and loudness (API-level controls)

These are useful when you **don’t** want to insert SSML `<break>` everywhere.

- `pause_sentence` (int ms): pause between sentences
- `pause_paragraph` (int ms): pause between paragraphs
- `volume` (int, default `100`): **10 … 200**
- `effect` (string): audio effect (voice-dependent), example in docs: `car`

### Output format / quality

- `format` (string, default `mp3`): `mp3`, `wav`, `ogg`, `opus`, `flac`
- `sample_rate` (int Hz): `24000`, `44100`, `48000`, …
- `bitrate` (int kbps): **6 … 320** (for lossy: mp3/ogg/opus)
- `channels` (int): `1` mono, `2` stereo

Compatibility note from docs:
- historically `bitrate` sometimes behaved like **sample rate (Hz)**; now fixed.
- if `sample_rate` is not specified and `bitrate` looks like `48000`, server may interpret it as `sample_rate` for backward compatibility.

### Background music

- `music` (int): music ID from catalog
- `musik_volume` (int): 5 … 200
- `musik_loop` (int): `1` loop music under entire speech, `0` no loop

## 4) Responses and fields

### `/text` success example (status=1)

```json
{
  "id": "2870459",
  "status": 1,
  "file": "https://zvukogram.com/texttomp3/20260114/p_2870459_342.mp3",
  "file_cors": "https://zvukogram.com/index.php?r=site/download&prj=2870459&cors=...",
  "parts": "1",
  "parts_done": "1",
  "duration": 3,
  "format": "mp3",
  "error": "",
  "balans": "11563.364",
  "cost": 0.042
}
```

Important fields:

- `status`: `1` ready, `0` in progress, `-1` error
- `file`: direct download URL
- `file_cors`: browser-friendly URL if you fetch from JS (CORS)
- `duration`: seconds
- `balans`: remaining balance
- `cost`: tokens charged
- `error`: non-empty on errors

### `/longtext` creation response (status=0)

```json
{
  "id": "4153594",
  "status": 0,
  "parts": "5",
  "parts_done": "0",
  "format": "mp3",
  "error": "",
  "balans": "3331.272",
  "cost": 0.00
}
```

While processing, `cost` may grow and `parts_done` increments.

## 5) Utility endpoints

### `/voices`

- `GET https://zvukogram.com/index.php?r=api/voices`
- Optional filter: `&langs=en,ru`

Use it to validate the `voice` string.

### `/balance`

- `POST/GET .../balance` with `token`, `email`.

### `/delete`

- `POST/GET .../delete` with `token`, `email`, `id`.
- Deletes the generated project/audio from server.

## 6) Practical agent notes

- For **podcasts**: use `speed` (e.g. `1.1–1.3`) + `pause_sentence`/`pause_paragraph` to shape rhythm consistently across many chunks.
- If you need immediate output for long text: chunk client-side into <=1000 char parts and call `/text` sequentially, then merge (see `chunking-and-method-choice.md`).
- Always treat `voice` and `style` as runtime-validated: capabilities vary by voice.
