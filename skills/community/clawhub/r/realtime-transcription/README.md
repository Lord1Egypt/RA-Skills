# Real-time Transcription Skill

> Capture any audio, get a structured summary. Real-time transcription powered by SenseVoice/FunASR.

## Features

- **Real-time transcription** — stream audio from system (BlackHole) or microphone, see text appear live
- **Auto summary** — on stop, the LLM generates a title and structured summary from the transcript
- **Date-based archival** — results saved as dated Markdown files in `archive/YYYY/MM/`
- **Idle detection** — auto-stops after N seconds of silence, prompts whether to continue
- **Dependency check** — refuses to start if missing packages, with install instructions
- **LLM-agnostic** — works with any LLM that supports the Skill protocol

## Directory Structure

```
skills/realtime-transcription/
├── README.md                # This file
├── skill.yaml               # Skill definition (triggers, commands, instructions)
├── realtime_asr.py          # Background transcription process
├── summary_prompt.py        # LLM prompt builder & response parser
├── archiver.py              # Markdown archival module
├── .tmp/                    # Runtime temporary files (gitignored)
└── archive/                 # Archived transcriptions (tracked)
```

## Prerequisites

### Python Packages

```bash
pip3 install sounddevice librosa funasr torch numpy
```

Or use the built-in installer with progress output:

```bash
cd skills/realtime-transcription
python3 realtime_asr.py --install-deps
```

### System Audio (optional)

For macOS system audio capture, install BlackHole:

```bash
brew install blackhole-2ch
```

After installing, set up a Multi-Output Device in macOS Audio MIDI Setup that includes both your speakers and BlackHole, and set it as the system output.

### ASR Model

Download the SenseVoice model:

```bash
modelscope download --model gongjy/SenseVoiceSmall --local_dir ./model/SenseVoiceSmall
```

## Quick Start

### Standalone Usage

```bash
cd skills/realtime-transcription

# Check dependencies
python3 realtime_asr.py --check-deps

# Install missing dependencies (if any)
python3 realtime_asr.py --install-deps

# Start transcription (system audio)
python3 realtime_asr.py --source blackhole

# Start transcription (microphone)
python3 realtime_asr.py --source mic

# Start transcription with custom idle timeout (5 minutes)
python3 realtime_asr.py --source blackhole --idle-timeout 300

# Disable idle timeout
python3 realtime_asr.py --source mic --idle-timeout 0

# Stop
# Press Ctrl+C, or the idle timeout will auto-stop
```

### CLI Reference

| Flag | Default | Description |
|---|---|---|
| `--source` | `blackhole` | Input source: `blackhole` (system) or `mic` |
| `--output` | `.tmp/transcript.txt` | Transcript file path |
| `--state` | `.tmp/asr.pid` | PID file for process management |
| `--model` | `./model/SenseVoiceSmall` | SenseVoice model directory |
| `--idle-timeout` | `60` | Auto-stop after N seconds of silence (0 to disable) |
| `--device` | auto | Audio device ID (overrides auto-detection) |
| `--check-deps` | — | Check dependencies and exit |
| `--install-deps` | — | Install missing dependencies with progress output |
| `--list-devices` | — | List available audio input devices |

### Skill Protocol

When used as an LLM Skill, the following triggers activate it:

| User says | Action |
|---|---|
| "开始转录" / "transcribe" | Check deps → start transcription (ask source) |
| "停止" / "stop" | Stop process → LLM summary → archive |
| "当前转录内容" | Show current transcript |
| "检查依赖" | Run `--check-deps` and report |

## Output Format

### Transcript File (`.tmp/transcript.txt`)

```
[14:30:00] 你好今天我们来讨论一下AI的发展
[14:30:05] AI技术在各个领域都有广泛应用
[14:30:10] 特别是在医疗金融和教育领域
```

### Archive File (`archive/YYYY/MM/DD-HHMM-title.md`)

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
[14:30:05] AI技术在各个领域都有广泛应用
...
```

## Error Handling

| Scenario | Behavior |
|---|---|
| Missing dependencies | Prints error + install instructions, refuses to start |
| BlackHole not installed | Reports error, suggests `--source mic` |
| Process crashes mid-transcription | PID file gone → skill detects and offers to recover |
| Empty transcript on stop | Warns user, skips summary, no archive created |
| LLM summary fails | Saves raw transcript with auto-generated title from timestamp |
| No sound for N seconds | Auto-stops with exit code 42, prompts to continue |

## Architecture

```
User ──→ LLM Skill ──→ Start/Stop Background Transcription Process
                            │
                            ├── realtime_asr.py
                            │     └── Writes to .tmp/transcript.txt
                            │
                            └── After Stop
                                  ├── summary_prompt.py → LLM → title + summary
                                  └── archiver.py → archive/YYYY/MM/DD-HHMM-title.md
```

## Competitive Analysis

Similar tools exist but differ significantly in approach and quality:

| | Whisper MCP (various) | SiliconFlow SenseVoice MCP | **This Skill** |
|---|---|---|---|
| **Model** | Whisper (English-optimized) | SenseVoice (cloud API) | SenseVoice (local) |
| **Deployment** | Local or cloud | Cloud API only | Fully local, no network |
| **Chinese accuracy** | Moderate | Good | Good + no API latency |
| **Idle detection** | No | No | Yes (60s silence auto-stop) |
| **Auto summary** | Some (meeting notes) | No | LLM-generated title + structured summary |
| **Archival** | Plain text or basic file | No | Date-based (`archive/YYYY/MM/`) with YAML frontmatter |
| **Integration** | MCP server | MCP server | LLM Skill protocol (lighter) |
| **Privacy** | Depends on config | Audio sent to cloud | 100% local, zero data leaves machine |

**Key differentiators:**
- **Chinese-first recognition** — SenseVoice outperforms Whisper on Mandarin speech
- **Complete pipeline** — transcription → summary → archive, not just "audio to text"
- **Privacy by design** — no API calls, no audio data leaves the machine
- **Zero dependencies on external services** — works offline once model is downloaded

## License

MIT
