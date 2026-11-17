---
name: uydi-voice
description: >
  Uydi Voice enables an AI agent to design custom voices, clone a user's authorized
  voice sample, synthesize narration, create expressive sound scenes, and produce multi-voice Voice Canvas projects
  with the Uydi voice platform
  (https://uydi.com). Use it when a user asks to create or describe a voice, clone
  their own voice from a recording, convert text to speech, generate narration audio,
  create dialogue, sound effects, ambience or music; arrange multiple speakers or
  languages into one audio file; list or manage Uydi voices; check credits; or review
  synthesis and scene history. It requires Node.js 18+
  and a one-time OAuth approval in the user's browser.
metadata:
  version: "1.2.0"
  openclaw:
    requires:
      bins:
        - node
    envVars:
      - name: UYDI_BASE_URL
        required: false
        description: Optional Uydi deployment URL for development or self-hosted testing.
    emoji: "🔊"
    homepage: https://uydi.com
---

# Uydi Voice

Use the Uydi voice platform from any agent: voice design, authorized voice cloning,
text-to-speech, freestyle sound-scene creation, and multi-voice Voice Canvas production,
all through a single zero-dependency CLI script.

## Requirements

- Node.js 18 or newer (`node --version`) — the script uses only built-in modules.
- A Uydi account (register free at https://uydi.com).
- All commands run as: `node scripts/uydi.mjs <command>` (relative to this skill directory).

## What the skill can do

- **Design** a new AI voice from a natural-language brief and generate a WAV preview.
- **Clone** a voice from a 10–20 second WAV, MP3, or M4A sample when the user owns the
  voice or has explicit permission.
- **Synthesize** speech from text with a selected Uydi voice and save a WAV file.
- **Produce a Voice Canvas** from an ordered sequence of language-aware voices, scripts,
  and pauses, then download one continuous 24 kHz WAV.
- **Create Sound Scenes** in Chinese or English: dialogue, nonverbal sound effects and
  ambience, or instrumental music. Optimize an idea into a detailed editable draft,
  estimate the fixed credit quote, then generate and download a WAV.
- **Manage** the authenticated account's voice list, synthesis history, and credit balance.

## First-time login (one-time, needs the user)

Authentication uses OAuth; the token is stored in `~/.uydi/credentials.json` (mode 600)
and stays valid for 365 days.

```bash
node scripts/uydi.mjs login
```

- Default: opens the browser for the user to approve access (authorization code + PKCE
  with a local loopback callback).
- Headless / no browser: automatically falls back to a device code flow — the terminal
  prints a URL (https://uydi.com/activate) and an 8-character code (`XXXX-XXXX`) for the
  user to enter on any device. Use `login --device` to force this mode.
- IMPORTANT: the login must be completed by the human user in a browser. If a command
  fails with a 401 / "Not logged in" error, ask the user to run the login and wait.

## Commands

```bash
node scripts/uydi.mjs whoami                # current account
node scripts/uydi.mjs credits               # credit balance and pricing
node scripts/uydi.mjs voices                # list voices (id, kind, name, status)
node scripts/uydi.mjs delete-voice <id>     # delete a voice permanently

# Design a brand-new voice from a text description (costs credits;
# --name, --prompt and --preview-text are all required):
node scripts/uydi.mjs design --name "Warm Narrator" \
  --prompt "A warm, deep male narrator voice, slow pace, documentary style" \
  --preview-text "Hello, this is a preview." -o preview.wav

# Clone a voice from a 10-20s clean speech sample (wav/mp3/m4a, costs credits):
node scripts/uydi.mjs clone --name "My Voice" --file sample.wav --rights-basis self --confirm-rights
# Malay / Filipino / Arabic: choose ms / fil / ar when creating the clone
node scripts/uydi.mjs clone --name "Malay Voice" --file sample.wav --provider qwen --language ms --rights-basis self --confirm-rights

# Synthesize speech with any voice (1 credit / 10 chars, max 2000 chars per run):
node scripts/uydi.mjs tts --voice <voiceId> --text "Text to speak, any language." -o out.wav

node scripts/uydi.mjs history --limit 10    # recent syntheses
node scripts/uydi.mjs logout                # revoke token + delete local credentials
```

### Voice Canvas

```bash
node scripts/uydi.mjs system-voices --language en --search narrator
node scripts/uydi.mjs canvas-list
node scripts/uydi.mjs canvas-create --title "Episode 1"
node scripts/uydi.mjs canvas-show <projectId>
node scripts/uydi.mjs canvas-save <projectId> --file canvas.json
node scripts/uydi.mjs canvas-estimate <projectId>
node scripts/uydi.mjs canvas-render <projectId> -o episode-1.wav
node scripts/uydi.mjs canvas-status <renderId> --wait -o episode-1.wav
node scripts/uydi.mjs canvas-renders --limit 10
node scripts/uydi.mjs canvas-delete <projectId>

# Freestyle Sound Scenes — dialogue, soundscape, or instrumental music
node scripts/uydi.mjs scene-optimize --language zh --idea "雨夜便利店里，店员和赶路的学生简短交谈"
node scripts/uydi.mjs scene-create --file scene.json
node scripts/uydi.mjs scene-list
node scripts/uydi.mjs scene-show <projectId>
node scripts/uydi.mjs scene-save <projectId> --file scene.json
node scripts/uydi.mjs scene-estimate <projectId>
node scripts/uydi.mjs scene-generate <projectId> --quoted-credits <exact-estimate> -o scene.wav
node scripts/uydi.mjs scene-status <renderId> --wait -o scene.wav
node scripts/uydi.mjs scene-renders --limit 10
node scripts/uydi.mjs scene-delete <projectId>
```

Read [references/sound-scenes.md](references/sound-scenes.md) for the JSON schema,
sample dialogue/soundscape/music prompts, prompt optimization, quote approval, and
recovery workflow. Sound Scenes use Qwen Audio 3.1 TTS Next; the optional prompt
optimizer uses Qwen 3.8 Flash when available.

For the editable JSON schema, language codes, voice selection, optimistic versioning,
credit checks, background rendering, and safe retry behavior, read
[references/voice-canvas.md](references/voice-canvas.md) before using Canvas commands.

Optional flags: `--provider qwen|cosyvoice` on design/clone (default `qwen`, the
general-purpose multilingual engine; `cosyvoice` focuses on dialects).

## Typical workflows

1. **Narration from scratch**: `design` a voice matching the user's description →
   `tts` the script text → deliver the WAV file.
2. **Speak in the user's own voice**: ask for a 10–20 s clean recording → `clone` →
   `tts` with the new voice id.
3. **Reuse an existing voice**: `voices` to find the id → `tts`.
4. **Multi-speaker production**: choose compatible voices → create a canvas → save the
   ordered nodes → estimate credits → render and deliver the merged WAV.
5. **Freestyle sound design**: describe a scene in the user's language → use `scene-optimize`
   to expand sound layers, spatial cues and timing → review the draft and `scene-estimate`
   quote → after the user approves the exact quote, run `scene-generate` and deliver WAV.

## Security & trust

- The CLI is a single zero-dependency script (`scripts/uydi.mjs`, Node.js built-ins only)
  — fully auditable before running, no install step, no postinstall hooks.
- Downloads can be verified: `https://uydi.com/downloads/uydi-voice-skill.zip.sha256`
  holds the SHA-256 of the official zip (`shasum -a 256 -c` after download).
- The token only grants access to the user's own Uydi voices/credits; it never touches
  the account password. The user can revoke it anytime with `logout` or from the website.
- Approval always happens on uydi.com in the user's browser; the script never asks for
  or handles the account password.
- Never add `--confirm-rights` on the user's behalf. Before cloning, the user must explicitly
  confirm that the voice owner is an adult, that the recording is their own voice or carries
  verifiable permission, and that the clone will follow Uydi's acceptable-use rules. Use
  `--rights-basis self` for the user's own voice or `authorized-adult` for a third party.

## Notes

- Every design / clone / tts call consumes real credits from the user's account
  (`credits` shows pricing). Confirm with the user before large batch synthesis.
- Voice Canvas preview, saving, estimation, reused nodes, merging, playback, and download
  are free. `canvas-render` charges only nodes that need newly generated audio. Show the
  exact estimate first; an explicit request to render is sufficient authorization.
- Sound Scene generation consumes the live fixed-credit quote per render. Show the estimate
  and balance before generating. `scene-generate` requires `--quoted-credits` to match the
  server's current quote; never guess the price or retry an uncertain request with a new key.
- `scene-optimize` may enrich a scene description, but generated fields must remain in the
  selected Chinese or English language. Review and edit the suggestion before saving or
  spending credits. Dialogue is spoken verbatim; soundscape and music scenes are nonverbal.
- Voice slots are limited per plan (free: 1 voice, Pro: 5). If design/clone fails with a
  quota error, list voices with `voices` and ask the user which one to `delete-voice`.
- Voice cloning requires the user to own the voice or have explicit permission.
- Output audio is WAV. Text over 2000 characters must be split into multiple `tts` runs.
- Canvas has no application-level node cap; each node accepts up to 600 characters and a
  0–3000 ms pause. Total project text is 2,000 characters on Free and 20,000 on Pro.
- `canvas-delete` permanently deletes the project and stored audio. Use it only when the
  user explicitly asks to delete that exact project.
- Set `UYDI_BASE_URL` to target a different deployment (e.g. a local dev server).

## Validation before handoff

1. Run `node scripts/uydi.mjs whoami` to confirm the intended Uydi account.
2. Run `node scripts/uydi.mjs credits` before any operation that can consume credits.
3. After `design`, `clone`, or `tts`, confirm that the CLI reports a voice ID or output
   WAV path, and provide that result to the user.
4. After `canvas-render`, confirm the render reaches `completed`, the merged WAV exists,
   and report its render ID, duration, charged credits, and absolute output path.
5. If a request fails, do not blindly repeat a paid operation. Check `history`, `voices`,
   `canvas-show`, or `canvas-status` first and explain the returned error. Reuse the
   printed Canvas idempotency key when retrying an uncertain render request.

## Version history

- **1.2.0** — Adds freestyle Sound Scenes: language-matched prompt optimization, dialogue,
  soundscape and instrumental music projects, quote-checked generation, and WAV recovery.
- **1.1.0** — Adds language-aware Voice Canvas project editing, credit estimation,
  background rendering, status polling, completed-render history, and WAV download.
- **1.0.1** — Adds the required idempotency header for clone and synthesis requests.
- **1.0.0** — Initial public marketplace release.
