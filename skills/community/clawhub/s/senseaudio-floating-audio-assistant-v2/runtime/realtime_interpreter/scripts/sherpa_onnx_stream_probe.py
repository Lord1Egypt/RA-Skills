#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import time
import wave
from array import array
from pathlib import Path

import sherpa_onnx


SCRIPT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = SCRIPT_DIR / "models" / "sherpa-onnx-streaming-zipformer-small-ctc-zh-int8-2025-04-01"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe sherpa-onnx streaming ASR behavior.")
    parser.add_argument(
        "--wav",
        default=str(MODEL_DIR / "test_wavs" / "0.wav"),
        help="16-bit mono wav path",
    )
    parser.add_argument("--chunk-ms", type=int, default=160)
    parser.add_argument("--sleep", action="store_true", help="Sleep between chunks to simulate realtime")
    parser.add_argument("--threads", type=int, default=2)
    return parser.parse_args()


def load_wave_samples(path: Path) -> tuple[int, list[float]]:
    with wave.open(str(path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise SystemExit("Only 16-bit mono wav is supported for this probe.")
        sample_rate = wf.getframerate()
        pcm = array("h")
        pcm.frombytes(wf.readframes(wf.getnframes()))
    return sample_rate, [sample / 32768.0 for sample in pcm]


def make_recognizer(num_threads: int) -> sherpa_onnx.OnlineRecognizer:
    return sherpa_onnx.OnlineRecognizer.from_zipformer2_ctc(
        tokens=str(MODEL_DIR / "tokens.txt"),
        model=str(MODEL_DIR / "model.int8.onnx"),
        num_threads=num_threads,
        provider="cpu",
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=1.2,
        rule2_min_trailing_silence=0.5,
        rule3_min_utterance_length=8.0,
    )


def print_result(prefix: str, result_json: str) -> None:
    payload = json.loads(result_json)
    text = payload.get("text", "").strip()
    if not text:
        return
    segment = payload.get("segment")
    is_final = payload.get("is_final")
    start_time = payload.get("start_time")
    print(f"{prefix} segment={segment} final={is_final} start={start_time:.2f} text={text}", flush=True)


def main() -> int:
    args = parse_args()
    wav_path = Path(args.wav).expanduser().resolve()
    if not wav_path.exists():
        raise SystemExit(f"Wave file not found: {wav_path}")

    sample_rate, samples = load_wave_samples(wav_path)
    chunk_size = max(1, math.floor(sample_rate * args.chunk_ms / 1000.0))
    recognizer = make_recognizer(args.threads)
    stream = recognizer.create_stream()

    print(f"[probe] wav={wav_path}")
    print(f"[probe] sample_rate={sample_rate} samples={len(samples)} chunk_size={chunk_size}")

    last_json = ""
    chunk_count = 0
    started_at = time.monotonic()

    def drain_ready(reason: str) -> None:
        nonlocal last_json
        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)
            current_json = recognizer.get_result_as_json_string(stream)
            if current_json != last_json:
                print_result(f"[{reason}]", current_json)
                last_json = current_json
            if recognizer.is_endpoint(stream):
                print(f"[endpoint] chunk={chunk_count}", flush=True)
                recognizer.reset(stream)
                last_json = ""

    for offset in range(0, len(samples), chunk_size):
        piece = samples[offset : offset + chunk_size]
        chunk_count += 1
        stream.accept_waveform(sample_rate, piece)
        drain_ready("partial")
        if args.sleep:
            time.sleep(args.chunk_ms / 1000.0)

    stream.input_finished()
    drain_ready("tail")
    final_json = recognizer.get_result_as_json_string(stream)
    if final_json != last_json:
        print_result("[final]", final_json)

    elapsed = time.monotonic() - started_at
    duration = len(samples) / sample_rate
    print(f"[probe] elapsed={elapsed:.2f}s audio={duration:.2f}s rtf={elapsed / duration:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
