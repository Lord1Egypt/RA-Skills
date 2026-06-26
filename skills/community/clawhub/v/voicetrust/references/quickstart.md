# VoiceTrust Quickstart

This guide is for the first time you set up VoiceTrust after unpacking `VoiceTrust.zip`.
After extraction, the package root should be `VoiceTrust/`.

Install `VoiceTrust/` into an OpenClaw skill directory.
It may be used as either:
- a workspace skill under `~/.openclaw/workspace/skills/VoiceTrust/`
- a global skill under `~/.openclaw/skills/VoiceTrust/`

It explains how to register the local usage convention, prepare the runtime, collect the owner audio, prepare the local model assets, enroll the owner voiceprint, and verify that the skill is ready for normal use.

For normal day-to-day use, you should not need this file.

---

## Package layout

This quickstart assumes you are already inside the `VoiceTrust/` directory.

Relevant paths in this package:

- `SKILL.md`
- `references/quickstart.md`
- `scripts/demo.py`
- `scripts/ensure_models.py`
- `runtime/`

The actual VoiceTrust runtime lives under `runtime/`.
The package intentionally stays lightweight:
- source code and setup docs are included
- large SpeechBrain checkpoint files are not bundled
- model assets are fetched on demand from the canonical VoiceTrust repository when needed
- owner enrollment data is local-only and should never be distributed

---

## Runtime note

VoiceTrust uses an owner-focused scoring model and a command-gating decision model:
- `speaker_match` is the primary identity signal
- `confidence` is a derived stability signal
- `identity_score` summarizes owner similarity
- `overall_trust` is a penalty-adjusted trust summary for operator visibility
- `decision` is the command-gating result

For normal message handling:
- use STT for content
- use VoiceTrust for owner verification
- use `decision` only for command execution gating, not for blocking ordinary non-command replies

---

## 1. Register the local voice-message convention in `TOOLS.md`

Before runtime setup, register the local voice-handling rule in `TOOLS.md`.

Recommended wording:

```md
## Incoming Voice Message
- Do STT.
- Also run VoiceTrust.
- Merge both before replying.
- If this is a voice command, execute only when `decision == "allow_command"`.
- If this is not a command, low trust does not automatically block normal content handling.
- Music / non-speech / non-command audio must not enter the command-execution path.
```

Keep this section short.
Put local behavior conventions in `TOOLS.md`, not in the skill itself.

---

## 2. Collect the owner audio first

Before real use, decide whose voice will be treated as the owner.
VoiceTrust is not useful until the owner voiceprint is enrolled.

Required preparation:
- choose the owner identity first
- prepare 3 to 5 owner voice samples before enrollment
- keep all samples from the same person
- prefer natural speech in the owner's usual speaking voice
- avoid heavy background noise, music, or overlapping speakers
- prefer clips in the rough 3-10 second range

Recommended `speaker_id`:
- `owner`

If you do not have the owner audio yet, stop here and gather it first.

---

## 3. Enter the runtime directory

From the package root:

```bash
cd runtime
```

All setup commands below are run from inside `runtime/`.

---

## 4. Create the virtual environment

```bash
uv venv .venv
```

---

## 5. Install dependencies

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

---

## 6. Install ffmpeg

VoiceTrust may use local `ffmpeg` as a fallback decoder for formats that `soundfile` cannot read directly.
Ensure `ffmpeg` is installed locally.

### macOS

Homebrew:

```bash
brew install ffmpeg
```

### Linux

Debian / Ubuntu:

```bash
sudo apt update
sudo apt install -y ffmpeg
```

Fedora:

```bash
sudo dnf install -y ffmpeg
```

Arch:

```bash
sudo pacman -S ffmpeg
```

### Windows

Recommended options:
- install via `winget`
- or install via `choco`
- or download a prebuilt binary and add it to `PATH`

Examples:

```powershell
winget install Gyan.FFmpeg
```

```powershell
choco install ffmpeg
```

After installation, confirm it is available:

```bash
ffmpeg -version
```

VoiceTrust resolves ffmpeg in this order:
1. `FFMPEG_BIN` environment variable
2. `ffmpeg` on `PATH`
3. `/opt/homebrew/bin/ffmpeg` fallback on Homebrew macOS

---

## 7. Prepare the local model assets

Before enrollment or verification, run:

```bash
uv run --python .venv/bin/python ../scripts/ensure_models.py
```

Expected model directory:

```text
runtime/assets/models/ecapa_voxceleb/
```

Required files:
- `hyperparams.yaml`
- `classifier.ckpt`
- `embedding_model.ckpt`
- `label_encoder.ckpt`
- `mean_var_norm_emb.ckpt`

The downloader reports the canonical repository, source URLs, file sizes, and SHA256 values for local verification.

---

## 8. Verify that the runtime starts

```bash
uv run --python .venv/bin/python ../scripts/demo.py --list-speakers
```

If this is the first setup, it is normal to see that no enrolled speaker exists yet.

---

## 9. Enroll the owner voiceprint

```bash
uv run --python .venv/bin/python ../scripts/demo.py \
  --audio /path/to/owner_sample_01.wav \
  --speaker owner \
  --enroll-sample \
  --json
```

Repeat with additional owner samples.

Recommended minimum:
- 3 samples

Recommended comfortable baseline:
- 5 samples

This will create owner-profile data under:

```text
data/owners/owner/
```

This data is local runtime state.
Do not publish it.

---

## 10. Run a real verification test

```bash
uv run --python .venv/bin/python ../scripts/demo.py \
  --audio /path/to/test_audio.wav \
  --speaker owner \
  --json
```

Expected output fields include:
- `speaker_match`
- `audio_quality`
- `overall_trust`
- `confidence`
- `identity_score`
- `trust_label`
- `decision`
- `decision_reasons`
- `speech_duration`
- `speech_ratio`
- `vad_status`
- `failure_reason`

---

## 11. Command gating rule

For voice command execution:
- use the normal path when `speech_duration >= 3.0`
- allow a short voice sample only when all of the following are true:
  - `speech_duration >= 1.2`
  - `speaker_match >= 85`
  - `confidence >= 85`
- in all cases, command execution still requires:
  - `speaker_match >= 78`
  - `confidence >= 80`
  - `identity_score >= 82`
  - `vad_status == "ok"`
  - `failure_reason == null`

Interpretation:
- `decision == "allow_command"` means the sample may be used for voice-command execution
- `decision != "allow_command"` means do not execute commands from the sample
- non-command voice content may still be handled normally through STT + reply flow

---

## 12. Sanity-check examples

- owner-like long speech should typically produce high `identity_score` and `decision = "allow_command"`
- short but very strong owner matches may still be allowed
- music, non-speech, or non-command audio should not enter the command-execution path even if processed
- low-trust or inconclusive command audio should not be executed

---

## Local biometric data and privacy

VoiceTrust performs local owner verification and may create local enrollment artifacts for the enrolled speaker.

What may be stored locally:
- owner enrollment audio samples provided by the operator
- derived local owner profiles / voiceprint artifacts used for speaker verification

Typical local paths:
- `runtime/data/owners/`
- `runtime/data/voiceprints/`

What VoiceTrust does not do:
- it does not upload owner enrollment data to the VoiceTrust repository
- it does not send biometric enrollment data to a remote verification service
- it does not require biometric enrollment data for installation
- `scripts/ensure_models.py` only prepares public model assets and does not upload or collect owner enrollment data

Operator guidance:
- treat these directories as sensitive local biometric data
- do not publish, share, or casually sync them to other systems
- protect them with appropriate local filesystem permissions
- review backup and sync destinations if your machine automatically copies local folders to cloud storage

Removal:
- delete the relevant speaker data under `runtime/data/owners/` and `runtime/data/voiceprints/` to remove local enrollment artifacts
- after deletion, that speaker must be enrolled again before verification can resume

Privacy design summary:
- local-only
- user-initiated
- not required for installation
- removable by deleting local enrollment artifacts

