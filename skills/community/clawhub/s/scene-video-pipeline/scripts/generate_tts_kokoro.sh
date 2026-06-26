#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   generate_tts_kokoro.sh <module_dir> [voice] [speed]
# Expects:
#   <module_dir>/tts/manifest.csv with columns: slide,audio_file,text
# Produces:
#   <module_dir>/tts/audio/*.mp3

MODULE_DIR="${1:?module_dir required}"
VOICE="${2:-af_sarah}"
SPEED="${3:-1.0}"
MANIFEST="$MODULE_DIR/tts/manifest.csv"
KOKORO_PY="/Users/loki/.kokoro-venv/bin/python3"

if [ ! -x "$KOKORO_PY" ]; then
  echo "Kokoro runtime missing: $KOKORO_PY"
  exit 1
fi

"$KOKORO_PY" - "$MANIFEST" "$MODULE_DIR" "$VOICE" "$SPEED" <<'PY'
import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

manifest = Path(sys.argv[1])
module_dir = Path(sys.argv[2])
voice = sys.argv[3]
speed = float(sys.argv[4])

if not manifest.exists():
    raise SystemExit(f"Manifest not found: {manifest}")

lang_code = voice[0] if voice and voice[0] in 'abefhijpz' else 'a'
pipeline = KPipeline(lang_code=lang_code, repo_id='hexgrad/Kokoro-82M')

with manifest.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    slide = row['slide'].strip()
    rel_out = row['audio_file'].strip()
    text = row['text'].strip()

    mp3_out = module_dir / 'tts' / rel_out
    wav_out = mp3_out.with_suffix('.wav')
    mp3_out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating slide {slide} -> {mp3_out}")

    chunks = []
    for _, _, audio in pipeline(text, voice=voice, speed=speed):
        chunks.append(audio)

    if not chunks:
        raise RuntimeError(f"No audio generated for slide {slide}")

    combined = np.concatenate(chunks)
    sf.write(str(wav_out), combined, 24000)

    subprocess.run([
        'ffmpeg', '-y', '-i', str(wav_out), '-codec:a', 'libmp3lame', '-b:a', '192k', str(mp3_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    wav_out.unlink(missing_ok=True)

print(f"TTS generation complete: {module_dir / 'tts' / 'audio'}")

# Avoid intermittent torch teardown SIGBUS after successful generation.
import os
os._exit(0)
PY
