---
name: realtime-transcription
description: Real-time audio transcription with automatic summarization and archival. Supports system audio (via BlackHole on macOS) and microphone input. When transcription stops (manually or via idle timeout), generates a title and structured summary, then archives as a dated Markdown file. Triggers: "开始转录", "启动转录", "停止", "转录内容", "transcribe", "start recording", "stop recording", "check transcription deps".
allowed-tools: Bash(python3 realtime_asr.py:*), Bash(python3 -c:*), Read(*), Write(*), Bash(kill:*), Bash(cat:*), Bash(mkdir:*), Bash(cp:*), Bash(mv:*)
---

# Real-time Transcription Skill

Capture any audio, get a structured summary. Real-time transcription powered by SenseVoice/FunASR.

## Features

- **Real-time transcription** — stream audio from system (BlackHole) or microphone
- **Auto summary** — on stop, generate title + structured summary
- **Date-based archival** — results saved to `archive/YYYY/MM/DD-HHMM-title.md`
- **Idle detection** — auto-stops after 60s of silence (configurable)

## Skill Location

All files are in `~/.openclaw/skills/realtime-transcription/`:

```
realtime-transcription/
├── SKILL.md                 # This file
├── realtime_asr.py          # Background transcription process
├── summary_prompt.py        # LLM prompt builder & response parser
├── archiver.py              # Markdown archival module
├── references/
│   └── module-reference.md  # Module API reference
├── .tmp/                    # Runtime temp files
└── archive/                 # Archived outputs
```

## Prerequisites

### Python Dependencies

```bash
pip3 install sounddevice librosa funasr torch numpy
```

Or use the built-in installer with progress output:

```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --install-deps
```

### System Audio (optional, macOS)

For macOS system audio capture, install BlackHole: `brew install blackhole-2ch`

### ASR Model

Download the SenseVoice model: `modelscope download --model gongjy/SenseVoiceSmall --local_dir ./model/SenseVoiceSmall`

## Quick Start

### Check Dependencies

```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --check-deps
```

Expected output:

```
✅ 所有依赖已安装。
   sounddevice — PyAudio binding for microphone/system audio capture
   librosa — Audio resampling and preprocessing
   funasr — SenseVoice ASR model framework
   torch — PyTorch deep learning runtime
   numpy — Numerical array processing
```

If dependencies are missing, run `python3 realtime_asr.py --install-deps` to install them one by one with progress output.

### Start Transcription

**System audio (BlackHole):**
```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --source blackhole
```

**Microphone:**
```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --source mic
```

**With custom idle timeout (5 minutes):**
```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --source mic --idle-timeout 300
```

**Disable idle timeout:**
```bash
cd ~/.openclaw/skills/realtime-transcription
python3 realtime_asr.py --source mic --idle-timeout 0
```

### Stop Transcription

Press `Ctrl+C` in the terminal, or:
```bash
kill $(cat .tmp/asr.pid 2>/dev/null) 2>/dev/null; rm -f .tmp/asr.pid
```

## After Stopping — Summary & Archive

1. Read the transcript: `cat .tmp/transcript.txt`
2. Build the LLM prompt:
   ```bash
   cd ~/.openclaw/skills/realtime-transcription
   python3 -c "
from summary_prompt import build_summary_prompt
print(build_summary_prompt(open('.tmp/transcript.txt').read()))
   "
   ```
3. Send the prompt to yourself (the LLM) to generate TITLE + SUMMARY
4. Parse and archive:
   ```bash
   cd ~/.openclaw/skills/realtime-transcription
   python3 -c "
from summary_prompt import parse_summary_response
from archiver import archive
transcript = open('.tmp/transcript.txt').read()
result = parse_summary_response('YOUR_LLM_RESPONSE_HERE')
path = archive(transcript, result['title'], result['summary'], 'blackhole')
print(f'Archived to: {path}')
   "
   ```

## CLI Reference

| Flag | Default | Description |
|---|---|---|
| `--source` | `blackhole` | `blackhole` (system) or `mic` |
| `--output` | `.tmp/transcript.txt` | Transcript file path |
| `--state` | `.tmp/asr.pid` | PID file for process management |
| `--model` | `./model/SenseVoiceSmall` | SenseVoice model directory |
| `--idle-timeout` | `60` | Auto-stop after N seconds of silence (0=disable) |
| `--device` | auto | Audio device ID override |
| `--check-deps` | — | Check dependencies and exit |
| `--install-deps` | — | Install missing dependencies with progress output |
| `--list-devices` | — | List available audio input devices |

## Trigger Words

| User says | Action |
|---|---|
| "开始转录" / "transcribe" / "启动转录" | Check deps → ask source → start |
| "停止" / "stop" | Stop process → summary → archive |
| "当前转录内容" | Show `.tmp/transcript.txt` |
| "检查依赖" | Run `--check-deps` |

## Output Format

### Transcript (`.tmp/transcript.txt`)
```
[14:30:00] 你好今天我们来讨论一下AI的发展
[14:30:05] AI技术在各个领域都有广泛应用
```

### Archive (`archive/YYYY/MM/DD-HHMM-title.md`)
```markdown
---
title: "AI发展趋势讨论"
date: 2025-05-16
time: "14:30 - 14:38"
source: blackhole
duration: 8m
---

## 摘要

- AI在医疗、金融、教育领域广泛应用
- 未来将更智能和普及

## 完整转录

[14:30:00] 你好今天我们来讨论一下AI的发展
...
```

## Error Handling

| Scenario | Behavior |
|---|---|
| Missing dependencies | Refuse to start, show install instructions |
| BlackHole not found | Suggest `--source mic` |
| Process crashes | PID file gone → offer to recover |
| Empty transcript | Warn user, skip summary, no archive |
| No sound for N seconds | Exit code 42, ask user to continue |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Normal stop |
| 1 | Dependency check failed |
| 42 | Idle timeout — ask user: "⏸️ 已 N 秒没有检测到声音，是否继续录音？(y/n)" |
