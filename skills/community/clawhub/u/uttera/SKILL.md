---
name: uttera
description: Work with audio and voice through Uttera (https://uttera.ai) — transcribe, summarize, make a signed verifiable PDF report, translate (to text or to spoken audio), diarize (who speaks when), analyze pronunciation, synthesize speech from text, clone a voice from a sample, generate sound effects / music / sound scenes, report what the last call cost, and verify a signed report. Use this whenever the user attaches an audio file (wav, mp3, m4a, ogg, opus, flac, webm, aac, amr…) and asks to transcribe/summarize/translate/report/diarize/analyze it, OR asks to read text aloud, clone a voice, or generate a sound or music. Billable: each action spends credits from the user's Uttera account. The bundled script uploads the file to Uttera and returns the result — do NOT try to transcribe, summarize or decode the audio yourself, you cannot.
version: 1.4.0
author: Uttera
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["python3"], "env": ["UTTERA_API_KEY"] },
        "network": ["api.uttera.ai"],
        "tags": ["audio", "voice", "transcription", "summary", "translation", "sound-effects", "music", "pronunciation", "diarization", "voice-cloning"]
      }
  }
---

# Uttera — audio & voice

Uttera is a voice-AI API: speech ⇄ text, summaries, signed reports, translation,
diarization, pronunciation scoring, text-to-speech and voice cloning. This skill
uploads the user's attached file to Uttera and returns the result. **The audio bytes
go from the file straight to Uttera; they never pass through you** (you can't decode
audio), so never try to transcribe, summarize or describe the audio yourself — always
run the script.

## Actions

Run the bundled script once per request with one of these actions. "Input" says what
the user must attach or provide.

| Action | Input | What it does | Output | Plan |
|--------|-------|--------------|--------|------|
| `transcribe` | audio | Literal speech-to-text. | plain text | Free+ |
| `summarize` | audio | Transcript **+** structured summary (what it is, key points, data, to-dos, who spoke, tone). | text | Professional+ |
| `report` | audio | Same analysis as a **signed PDF report with an evidence graph** anyone can verify. | saves a **PDF** + prints the summary | Developer+ (graph: Professional+) |
| `translate` | audio + target language | Translate the recording into another language, as **text**. | text | Startup+ |
| `translate-voice` | audio + target language `[voice|original]` | Translate **and speak it**: a catalogue `voice`, or `original` to keep the speaker's own (cloned) voice. | saves an **audio** file | paid |
| `diarize` | audio | Who speaks and when (segments with speaker + timestamps). | JSON | Free+ |
| `pronunciation` | audio + reference text `[language]` | Score how well the recording pronounces the reference sentence: accuracy, IPA expected vs heard, grouped errors. | JSON | paid |
| `clone` | voice-sample audio + text to say `[language]` | Speak the given text in the sampled voice. | saves an **audio** file | paid |
| `speak` | text `[voice] [language]` | Text-to-speech. | saves an **audio** file | Free+ |
| `sfx` | description `[seconds]` | A sound effect from a description (a door, rain, footsteps), up to 30 s. | saves an **audio** file | paid |
| `music` | description `[seconds] [steps]` | A finished piece of music from a description, up to 380 s. ⚠ cost = length × steps. | saves an **audio** file | paid |
| `scene` | description `[seconds]` | Plan timed sound events from a description and mix them into one scene. | saves an **audio** file | paid |
| `voices` | — | List the available TTS voices (and the language each speaks). | JSON | Free+ |
| `cost` | — | What the last call cost. | JSON | Free+ |
| `verify` | a report's `.json` | Verify a signed Uttera report (Ed25519) is genuine and unmodified. | JSON verdict | Free+ |

If the account's plan doesn't include an action, Uttera replies **403** and the script
prints the plan message — tell the user they'd need to upgrade at
https://app.uttera.ai/billing. Don't silently fall back to doing it yourself.

## How to run it

The script is at `scripts/uttera.py` inside this skill's folder. In the code sandbox
the user's attached files are real files — pass the real path.

```
python <this-skill-folder>/scripts/uttera.py <action> <arg1> [arg2] [arg3]
```

- **Audio-input actions** (`transcribe`, `summarize`, `report`, `translate`,
  `translate-voice`, `diarize`, `pronunciation`, `clone`): `<arg1>` is the audio path.
- `translate` / `translate-voice`: `<arg2>` is the **target** language code
  (`en`, `es`, `fr`, `de`, `zh`, `no`…). For `translate-voice`, `<arg3>` is optionally a
  voice name, or the word `original` to keep the original speaker's voice.
- `pronunciation`: `<arg2>` is the **reference text** (what the speaker was meant to
  say), `<arg3>` optional language (default `es`). Use a short clip.
- `clone`: `<arg1>` is the **voice sample** (≈6–12 s), `<arg2>` is the **text to speak**,
  `<arg3>` optional language.
- `speak`: `<arg1>` is the **text**, `<arg2>` optional voice (default `dora`), `<arg3>`
  optional language.
- `voices` takes no argument; `verify` takes a report `.json` path.

Show the script's stdout to the user. When it prints a saved path (PDF for `report`,
audio for `translate-voice` / `clone` / `speak`), surface that file to the user as a
download.

### Examples

- «transcribe this» on `call.m4a`: `python scripts/uttera.py transcribe "/path/call.m4a"`
- «summarize this meeting»: `python scripts/uttera.py summarize "/path/meeting.mp3"`
- «signed PDF report of this call»: `python scripts/uttera.py report "/path/call.wav"`
- «translate this to English»: `python scripts/uttera.py translate "/path/audio.ogg" en`
- «say it in English, keep my voice»: `python scripts/uttera.py translate-voice "/path/audio.ogg" en original`
- «who speaks when»: `python scripts/uttera.py diarize "/path/audio.ogg"`
- «how good is my French pronunciation of this sentence»: `python scripts/uttera.py pronunciation "/path/me.ogg" "Bonjour, comment allez-vous" fr`
- «read this aloud»: `python scripts/uttera.py speak "Hello world" dora en`
- «say this in her voice» (sample + text): `python scripts/uttera.py clone "/path/her.wav" "Texto a decir" es`
- «make a 10-second rain sound effect»: `python scripts/uttera.py sfx "rain on a tin roof" 10`
- «compose 1 minute of lo-fi»: `python scripts/uttera.py music "lo-fi hip hop, 90 bpm, warm piano" 60`
- «build a forest-at-dawn soundscape»: `python scripts/uttera.py scene "a forest at dawn: birds, a stream, distant wind" 20`
- «what did that last call cost»: `python scripts/uttera.py cost`

For `sfx`, `music` and `scene` the description works best in English; `music` cost is
length × steps, so keep both modest unless the user wants a long piece.

## Requirements & notes

- **API key:** the script reads it from `scripts/key.txt` (bundled in this skill), or
  the `UTTERA_API_KEY` environment variable, or `~/.uttera/api_key`. Calls are billed to
  that Uttera account. If you downloaded this skill from app.uttera.ai while signed in,
  your key is already inside. Otherwise get one at https://app.uttera.ai.
- **Network (Claude):** the code sandbox can only reach a fixed allowlist of domains.
  On a **Team or Enterprise** org, an **admin** must allow `api.uttera.ai`:
  **Organization settings → Capabilities → Allow network egress**, then add
  `api.uttera.ai` to the **Domain allowlist**. On **individual plans (Free/Pro)** this
  step isn't needed — the skill reaches `api.uttera.ai` without any allowlist change. A
  network error from the script on a Team/Enterprise account almost always means the
  domain hasn't been allowed yet. Other LLMs with a code sandbox have an equivalent
  setting.
- **Voice cloning — consent required.** `clone`, and `translate-voice … original`, build
  a voice from a sample. A voice is **biometric, personal data**: only use a sample of
  the user's **own** voice, or one the speaker has **explicitly consented** to clone.
  Never clone a third party's voice to impersonate them — it enables fraud, social
  engineering and defamation and is illegal in many places. If the user hasn't confirmed
  consent, ask before cloning.
- **Where the data goes.** The script sends the file and your API key (Bearer header)
  only to `api.uttera.ai` over HTTPS; the `UTTERA_API_BASE` override is restricted to
  `*.uttera.ai`, so the key can't be redirected elsewhere.
- All generated audio carries an inaudible watermark required by the EU AI Act
  (Article 50(2)); it cannot be disabled.
- Files up to the sandbox upload limit (≈30 MB). For bigger files use the Uttera web app
  or the API directly.
