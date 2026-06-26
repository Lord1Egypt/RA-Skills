---
name: sensevoice-transcribe
description: Transcribe audio files (WAV/MP3/M4A/FLAC) to timestamped text using SenseVoice-Small + FSMN-VAD. Supports single-file and batch mode with VAD-anchored per-segment timestamps (~15s granularity). Use when the user wants to transcribe speech/audio, run batch transcription on daylog recordings, or re-transcribe specific dates. Replaces the old whisper-transcribe skill.
---

# SenseVoice Transcribe

Transcribe audio to timestamped text using FunASR's `iic/SenseVoiceSmall` model with `fsmn-vad` for timestamp anchoring.

## Pipeline

1. **FSMN-VAD** segments audio into speech regions (~258 segments for 30min file)
2. **SenseVoice-Small** transcribes full audio with `merge_vad=True`
3. Raw text is split by `<|zh|>` tags → cleaned via `rich_transcription_postprocess()`
4. Text segments are **proportionally mapped** to VAD timestamps
5. Output: `[HH:MM:SS] text` per line, ~15s granularity

## Environment

```
Venv: ~/.openclaw/venvs/sensevoice/
Python: 3.12
Key packages: funasr==1.3.1, modelscope, onnxruntime
Model cache: ~/.cache/modelscope/hub/models/iic/SenseVoiceSmall
VAD cache: ~/.cache/modelscope/hub/models/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch
```

### First-time Setup

```bash
python3 -m venv ~/.openclaw/venvs/sensevoice
source ~/.openclaw/venvs/sensevoice/bin/activate
pip install funasr modelscope onnxruntime
# Models auto-download on first run (~234MB SenseVoice + ~4MB VAD)
```

## Usage

### Single File

```bash
source ~/.openclaw/venvs/sensevoice/bin/activate
python3 -c "
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from datetime import datetime, timedelta
import re

wav = '<WAV_PATH>'
# Parse start time from filename: TX01_MIC015_20260308_124130_orig.wav
m = re.search(r'(\d{8})_(\d{6})', wav)
start_dt = datetime.strptime(m.group(1)+m.group(2), '%Y%m%d%H%M%S') if m else None

vad_model = AutoModel(model='fsmn-vad', disable_update=True)
model = AutoModel(model='iic/SenseVoiceSmall', vad_model='fsmn-vad',
                  vad_kwargs={'max_single_segment_time': 30000}, device='cpu')

vad_segs = vad_model.generate(input=wav)[0].get('value', [])
res = model.generate(input=wav, cache={}, language='zh', use_itn=True,
                     batch_size_s=60, merge_vad=True)

texts = [rich_transcription_postprocess(s).strip()
         for s in re.split(r'<\|zh\|>', res[0]['text']) if s.strip()]
texts = [s for s in texts if len(s) > 1]

ratio = len(vad_segs) / len(texts) if texts else 1
for i, t in enumerate(texts):
    vi = min(int(i * ratio), len(vad_segs)-1)
    ts = (start_dt + timedelta(milliseconds=vad_segs[vi][0])).strftime('%H:%M:%S') if start_dt else f'{vad_segs[vi][0]//1000:.0f}s'
    print(f'[{ts}] {t}')
"
```

### Batch Mode (daylog)

The bundled `scripts/batch_transcribe.py` handles the full daylog pipeline:

```bash
source ~/.openclaw/venvs/sensevoice/bin/activate
cd ~/Documents/dec/daylog

# Dry run — see what would be transcribed
python3 scripts/batch_transcribe.py --dry-run

# Transcribe all new files
python3 scripts/batch_transcribe.py

# Re-transcribe specific dates (deletes existing, then re-runs)
python3 scripts/batch_transcribe.py --force-dates 2026-03-07,2026-03-08

# With progress file + Discord webhook
python3 scripts/batch_transcribe.py \
  --progress-file /tmp/daylog-progress.json \
  --discord-webhook https://discord.com/api/webhooks/...
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--dry-run` | Preview without writing |
| `--engine sensevoice\|whisper` | Engine (default: sensevoice) |
| `--force-dates YYYY-MM-DD,...` | Delete & re-transcribe these dates |
| `--progress-file PATH` | Write JSON progress for monitoring |
| `--discord-webhook URL` | Post start/milestone/finish to Discord |

**Directory layout:**
```
daylog/
├── raw/                          # WAV input (DJI MIC 3, 48kHz/32bit, ~247MB/30min)
│   ├── TX01_MIC009_20260308_094129_orig.wav
│   └── ...
├── transcripts/                  # Output, grouped by date
│   └── 2026-03-08/
│       ├── 000_TX01_MIC009_20260308_094129_orig.txt
│       └── ...
└── notes/                        # Compiled daily notes (separate step)
    └── 2026-03-08.md
```

**Behavior:**
- Groups WAV files by date extracted from filename (`YYYYMMDD`)
- Sorts by timestamp within each date for correct chronological order
- Skips already-transcribed files unless `--force-dates`
- Indexed output filenames (`000_`, `001_`, ...) for sort order
- Discord milestones every 25% progress

## Output Format

```
[录音开始: 09:41:29]
[09:41:35] 到了，我们下车吧。
[09:41:48] 武康大楼，人好多啊。
[09:42:04] 你帮我在这里拍一张。
...
```

## Performance (Apple M4, 10-core CPU)

| Metric | Value |
|--------|-------|
| RTF | ~0.04 (25x realtime) |
| CPU | ~1.2 cores (12%) |
| RAM | ~1.5GB |
| 30min WAV | ~73s transcription + ~4s VAD |
| Accuracy | 92% keyword accuracy (vs Whisper-medium 23%, turbo 38%) |
| Hallucinations | 0 (vs Whisper hundreds per session) |
| Model size | 234MB (vs Whisper-large-v3-turbo 1.5GB) |

## vs Old Whisper Skill

| | Whisper (old) | SenseVoice (new) |
|---|---|---|
| Model | mlx-whisper-medium | SenseVoice-Small (234MB) |
| Accuracy | 23-38% | 92% |
| Hallucinations | Hundreds per session | 0 |
| Timestamp | Per-word (~2-4s) | VAD-anchored (~15s) |
| Duplicate lines | ~23% | <0.2% |
| Chinese support | Weak | Native (Mandarin-optimized) |

## Emoji Note

SenseVoice appends emotion tags (😊😔😡😮) to segments. These are **model artifacts** reflecting detected speech emotion, not literal emoji in the audio. Downstream consumers (note compilation) should ignore or strip them.
