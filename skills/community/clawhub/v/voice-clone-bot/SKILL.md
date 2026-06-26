---
name: voice-clone-bot
description: Synthesize speech by cloning a user's voice from a reference audio sample, then reading generated text aloud in that cloned voice. Use this skill whenever the user sends a voice message and expects an audio reply, asks to "speak", "clone my voice", "read this aloud", "reply with audio", or any context where a spoken voice response is appropriate. Also use when the user wants to switch into "voice mode" for conversation. Even if the user doesn't explicitly say "voice clone", use this skill if they send audio input and the natural response would be spoken.
---

# Voice Clone Skill

A self-initializing, zero-configuration voice cloning skill. It manages a background TTS daemon that keeps heavy model weights in memory for fast inference. Supports multiple engines and unlimited text length.

## Quick reference

| Item | Value |
| --- | --- |
| Entry script | `bash scripts/run_tts.sh --text "..." --ref_audio "..." [--speed 1.0] [--output_dir "..."]` |
| Output | Single line: absolute path to generated `.ogg` file |
| Attachment format | `MEDIA:<output_path>` |
| Default engine | F5-TTS (env `TTS_BACKEND=f5`) |
| Host/Port config | `.env` (`TTS_SERVER_HOST`, `TTS_SERVER_PORT`) |

## When to use this skill

- The user sends a voice memo or audio file and you need to reply with audio.
- The user says "read this aloud", "speak to me", "use my voice", "voice mode".
- The conversation context implies a spoken reply is expected.
- The user provides a reference audio and asks you to mimic their voice.

## Step-by-step usage

### 1. Identify inputs

You need two things:

- **`ref_audio`**: The absolute local path to the user's reference audio file (the voice to clone). This is typically the audio file the user just sent, saved by the ASR system (e.g., openai-whisper).
- **`text`**: The text content you want to speak. Generate this as you normally would — think of your reply, then voice it.

### 2. Run the synthesis

Execute this command:

```bash
bash scripts/run_tts.sh --text "Your reply text here." --ref_audio "/absolute/path/to/reference.ogg"
```

Optional parameters:
- `--speed 1.2` — Speak faster. Range: 0.5 to 2.0. Default: 1.0.
- `--output_dir "/tmp/"` — Save the generated audio file to a specific absolute folder path. Default: `server/generated_audio/`.

**Example with all options:**
```bash
bash scripts/run_tts.sh \
  --text "很高兴认识你，这是我克隆后的声音。" \
  --ref_audio "/tmp/user_voice_msg.ogg" \
  --speed 0.9
```

### 3. Handle the output

The script prints a single absolute path on stdout (e.g., `/path/to/reply_a1b2c3d4.ogg`).
Append it to your response using the attachment format:

```
MEDIA:/path/to/reply_a1b2c3d4.ogg
```

### 4. Important constraints

- **Do NOT** manually start `python app.py` or manage the backend. The `run_tts.sh` script auto-detects, auto-installs, and auto-starts everything.
- **First run is slow** (~30-60 seconds) because it downloads model weights and loads them into memory. Subsequent calls are fast.
- **Long texts work automatically.** The engine splits text into sentences, synthesizes each chunk, and stitches them seamlessly. No length limit.

## Controlling voice characteristics

### Speed (all engines)

The `--speed` parameter adjusts speaking rate:

| Value | Effect |
| --- | --- |
| `0.7` | Slow, deliberate, suitable for elderly listeners |
| `1.0` | Natural conversational speed (default) |
| `1.3` | Brisk, suitable for news or briefings |
| `1.5+` | Fast, compressed delivery |

F5-TTS supports speed natively. Other engines use ffmpeg post-processing (atempo filter), which gives good results but may slightly affect quality at extreme values.

### Emotion and tone

These models use **acoustic feature extraction** from the reference audio — they do not accept text-based emotion tags like `[happy]` or `[sad]`.

**The emotion of the output is determined entirely by the reference audio.**

To control emotion, select or prepare reference audio that carries the desired tone:

| Desired tone | Reference audio strategy |
| --- | --- |
| Calm, neutral | Use a reference clip where the speaker talks normally |
| Excited, happy | Use a reference clip where the speaker sounds enthusiastic |
| Angry, intense | Use a reference clip with raised voice and sharp intonation |
| Sad, melancholic | Use a reference clip with slow, downcast delivery |
| Whispering | Use a reference clip where the speaker whispers |

**Practical approach for Agents:** If the user has sent multiple voice messages, choose the one whose emotional tone best matches the context of your reply. If only one reference is available, use it as-is — the model will approximate the speaker's general style.

**ChatTTS Specifics:** This engine supports inline emotion tags in text: `[laugh]`, `[uv_break]` (pause). It also supports voice cloning when a reference audio is provided.

## Available engines

| Engine | ID | Install | Size | Clone | Speed support | Best for |
| --- | --- | --- | --- | :---: | --- | --- |
| **F5-TTS** | `f5` | `bash scripts/auto_installer.sh` | ~1.5GB | ✅ | Native | Highest quality cloning |
| **CosyVoice** | `cosyvoice` | `bash scripts/install_cosyvoice.sh` | ~1.5GB | ✅ | ffmpeg | Natural Chinese prosody |
| **ChatTTS** | `chattts` | `bash scripts/install_chattts.sh` | ~400MB | ✅ | ffmpeg | Dialogue with emotion tags |
| **OpenVoice** | `openvoice` | `bash scripts/install_openvoice.sh` | ~300MB | ✅ | ffmpeg | Ultra fast, tiny footprint |

Switch engines by setting the environment variable before the server starts:
```bash
export TTS_BACKEND=cosyvoice
```

## Uninstalling

```bash
# Remove everything (venv, daemon, registration)
bash scripts/uninstall.sh

# Remove only one engine's source code
bash scripts/uninstall.sh --engine cosyvoice

# Remove everything INCLUDING downloaded model weights (several GB)
bash scripts/uninstall.sh --purge
```

## File structure

```
scripts/
├── run_tts.sh              # Main entry point (auto-heals, auto-starts daemon)
├── tts_client.py            # HTTP client that talks to the backend
├── auto_installer.sh        # Install F5-TTS (default) + register skill
├── install_cosyvoice.sh     # Install CosyVoice engine
├── install_chattts.sh       # Install ChatTTS engine
├── install_openvoice.sh     # Install OpenVoice engine
└── uninstall.sh             # Cleanup script
server/
├── app.py                   # FastAPI daemon (auto-managed, do not start manually)
├── core_tts.py              # Multi-engine factory + long text chunking
└── requirements.txt         # Base dependencies
```


## References

- Read `references/architecture.md` for system architecture and design rationale.
