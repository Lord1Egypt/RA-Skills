#!/usr/bin/env python3
"""N-speaker diarization via pyannote-audio. Outputs JSON array to stdout."""
import json
import sys
import torch
from pyannote.audio import Pipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: diarize.py <audio_path> [speaker_count]", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    num_speakers = None
    if len(sys.argv) > 2:
        try:
            val = int(sys.argv[2])
            if val > 0:
                num_speakers = val
        except ValueError:
            print(f"Error: speaker count must be an integer, got '{sys.argv[2]}'", file=sys.stderr)
            sys.exit(1)

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=True
        )
    except Exception:
        print("Error: Failed to load pyannote model. Run `huggingface-cli login` and accept pyannote/speaker-diarization-3.1 terms at https://huggingface.co/pyannote/speaker-diarization-3.1", file=sys.stderr)
        sys.exit(1)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    pipeline.to(device)

    if num_speakers is not None:
        diarization = pipeline(audio_path, num_speakers=num_speakers)
    else:
        diarization = pipeline(audio_path)

    segments = []
    speaker_map = {}
    label_idx = 0

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if speaker not in speaker_map:
            speaker_map[speaker] = f"Speaker_{label_idx}"
            label_idx += 1
        segments.append({
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "speaker": speaker_map[speaker]
        })

    print(json.dumps(segments, ensure_ascii=False))

if __name__ == "__main__":
    main()
