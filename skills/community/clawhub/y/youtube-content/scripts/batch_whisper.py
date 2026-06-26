#!/usr/bin/env python3
"""Batch Whisper transcription: processes MP3 files sequentially, one at a time.

Loads the model ONCE, then transcribes each file in order. Skips files that
already have a .txt output (resume-safe). Prints progress with timing.

Usage:
  python3 batch_whisper.py file1.mp3 file2.mp3 ... [options]

Options:
  --language zh       Language code (default: zh)
  --model medium      Model name: base/small/medium/large-v3 (default: medium)
  --device cpu        Device: cpu or cuda (default: cpu)
  --compute-type int8 Compute type: int8 (cpu) or float16 (gpu) (default: int8)
  --beam-size 5       Beam search width (default: 5)

Output: Creates {VIDEO_ID}.txt for each input file in the same directory.

Designed for: Processing 10-40 YouTube videos sequentially without manual
intervention. Run as a single background process with notify_on_complete=true.
"""
import sys
import os
import time
import argparse


def main():
    parser = argparse.ArgumentParser(description="Batch Whisper transcription (sequential)")
    parser.add_argument("files", nargs="+", help="MP3 files to transcribe")
    parser.add_argument("--language", default="zh", help="Language code")
    parser.add_argument("--model", default="medium", help="Model name")
    parser.add_argument("--device", default="cpu", help="Device (cpu/cuda)")
    parser.add_argument("--compute-type", default="int8", help="Compute type")
    parser.add_argument("--beam-size", type=int, default=5, help="Beam size")
    args = parser.parse_args()

    from faster_whisper import WhisperModel

    print(f"Loading model '{args.model}' on {args.device} ({args.compute_type})...", flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    print(f"Model loaded. Queue: {len(args.files)} files.", flush=True)

    total = len(args.files)
    completed = 0
    skipped = 0
    failed = 0
    total_audio_seconds = 0

    for i, filepath in enumerate(args.files, 1):
        video_id = os.path.splitext(os.path.basename(filepath))[0]
        out_path = os.path.join(os.path.dirname(os.path.abspath(filepath)), f"{video_id}.txt")

        # Resume: skip if output already exists
        if os.path.exists(out_path):
            print(f"[{i}/{total}] SKIP {video_id} (already exists: {out_path})", flush=True)
            skipped += 1
            continue

        if not os.path.exists(filepath):
            print(f"[{i}/{total}] MISSING {video_id} ({filepath} not found)", flush=True)
            failed += 1
            continue

        print(f"[{i}/{total}] START {video_id}", flush=True)
        start = time.time()
        try:
            segments, info = model.transcribe(
                filepath,
                language=args.language,
                beam_size=args.beam_size,
                vad_filter=True,
            )
            elapsed = time.time() - start

            with open(out_path, "w") as f:
                for seg in segments:
                    f.write(seg.text.strip() + "\n")

            # Check for empty output (known silent failure mode)
            if os.path.getsize(out_path) == 0:
                os.remove(out_path)
                print(f"[{i}/{total}] WARN {video_id} | empty output, removed — needs re-run", flush=True)
                failed += 1
                continue

            # Check coverage (truncated transcription detection)
            coverage = seg.end / max(info.duration, 1) * 100
            if coverage < 90:
                print(f"[{i}/{total}] WARN {video_id} | coverage={coverage:.0f}% (may be truncated)", flush=True)

            total_audio_seconds += info.duration
            completed += 1
            print(
                f"[{i}/{total}] DONE {video_id} | "
                f"lang={info.language}({info.language_probability:.2f}) "
                f"dur={info.duration:.0f}s "
                f"elapsed={elapsed:.0f}s "
                f"ratio={elapsed / max(info.duration, 1):.1f}x",
                flush=True,
            )
        except Exception as e:
            failed += 1
            print(f"[{i}/{total}] FAILED {video_id} | {e}", flush=True)

    print(f"\n=== BATCH COMPLETE ===", flush=True)
    print(
        f"Completed: {completed} | Skipped: {skipped} | Failed: {failed} | "
        f"Total audio: {total_audio_seconds / 60:.1f}min",
        flush=True,
    )


if __name__ == "__main__":
    main()
