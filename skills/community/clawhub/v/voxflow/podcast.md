
# VoxFlow Podcast Skill

Generate multi-speaker AI podcasts entirely from the command line. Sister skills:

- Simple TTS / narration / voice search → `voxflow` (hub)
- Short videos / AI clips / knowledge cards → [video.md](video.md)
- Transcribe / translate subtitles / dub → [transcribe.md](transcribe.md)

## Prerequisites

- Node.js `^20.19.0 || >=22.12.0`
- `npm install -g voxflow` then `voxflow login`
- VoxFlow account (free tier: 10K quota/month)

**No API keys needed** — all auth goes through `voxflow login`.

## Quick Start

```bash
# 1. Login (one-time, opens browser)
voxflow login

# 2. Generate a podcast
voxflow podcast --topic "AI 时代的程序员出路"

# 3. Output: podcast-2026-03-20T12-00-00.wav + .txt
```

## Full Workflow

### Step 1: Generate Script Only

```bash
voxflow podcast \
  --topic "量子计算入门" \
  --template tutorial \
  --colloquial medium \
  --speakers 2 \
  --language zh-CN \
  --format json \
  --no-tts
```

Outputs: `podcast-<ts>.txt` + `podcast-<ts>.podcast.json`

### Step 2: Review & Edit

Open `.podcast.json` — it contains structured dialogue, speaker info, quality scores, and voice mappings. Edit as needed.

### Step 3: Synthesize from File

```bash
voxflow podcast --input podcast-2026-03-20.podcast.json --output final.wav
```

### One-Shot (generate + synthesize)

```bash
voxflow podcast \
  --topic "Web3 的未来" \
  --engine ai-sdk \
  --colloquial high \
  --speakers 3 \
  --output web3-podcast.wav
```

## Parameters

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--topic` | text | tech trends | Podcast topic or prompt |
| `--engine` | auto, legacy, ai-sdk | auto (→ ai-sdk) | Generation engine |
| `--template` | interview, discussion, news, story, tutorial | interview | Podcast template |
| `--colloquial` | low, medium, high | medium | Conversational tone level |
| `--speakers` | 1, 2, 3 | 2 | Number of speakers |
| `--language` | zh-CN, en, ja | zh-CN | Output language |
| `--length` | short, medium, long | medium | Script length |
| `--format` | json | — | Also output .podcast.json |
| `--input` | file path | — | Load .podcast.json for synthesis |
| `--no-tts` | flag | false | Script only, skip TTS |
| `--speed` | 0.5-2.0 | 1.0 | TTS playback speed |
| `--silence` | 0-5.0 | 0.5 | Gap between segments (sec) |
| `--output` | file path | auto | Output file path |

## Engine Comparison

| Feature | legacy | ai-sdk |
|---------|--------|--------|
| Structured output | No | Yes (JSON) |
| Quality scoring | No | Yes (1-10) |
| Colloquial control | No | 3 levels |
| Intent tagging | No | Yes |
| Speaker metadata | Partial | Full |
| Multi-language | Chinese only | zh/en/ja |

## Templates

- **interview** — Host + Guest deep conversation
- **discussion** — Roundtable multi-person discussion
- **news** — Professional news briefing
- **story** — Multi-character story narration
- **tutorial** — Teacher + Student educational dialogue

## Quota Cost

| Operation | Cost |
|-----------|------|
| Script generation (medium, ~16 turns) | 2,000 |
| TTS per turn (native pause voice) | 50 |
| TTS per chunk (splice fallback voice) | 50 |

**Per-turn TTS call count depends on voice**: voices flagged `nativePauseSupported: true` (most podcast voices) take 1 TTS call per turn — TRTC honors `<|break|>` / `<|s_break|>` markers natively (~250-430ms inserted). Voices that haven't been verified (e.g. 旁白 narration voices) fall back to client-side splice = N calls per turn.

Typical medium podcast (16 turns, all native voices) ≈ 16 × 50 + 2,000 = 2,800 quota — Free tier (10K/month) covers ~3 medium podcasts. **Tip**: if you already have a script, pass `--script my.json` to skip the 2,000 LLM step entirely. Mixed-voice podcasts cost slightly more if they include non-native voices.

## Examples

```bash
# English tech podcast
voxflow podcast --topic "AI ethics debate" --language en --template discussion

# Quick news briefing (short)
voxflow podcast --topic "本周科技新闻" --template news --length short

# Casual chat with high colloquial level
voxflow podcast --topic "程序员加班那些事" --colloquial high

# JSON export for editing
voxflow podcast --topic "创业故事" --format json --no-tts

# Synthesize edited script
voxflow podcast --input edited-podcast.podcast.json --speed 1.1
```

## Rules

1. **Check quota first** — medium podcast ≈ 5K. Run `voxflow status` before generation.
2. **Iterate on the script** — use `--no-tts --format json` to inspect dialogue before paying for TTS.
3. **Voice mapping** — for ai-sdk engine, the .podcast.json includes per-speaker voice IDs. Edit them before re-running with `--input`.
4. **Auto-play** when done: `open podcast-*.wav`.

