#!/usr/bin/env python3
from __future__ import annotations

import argparse
import signal
import subprocess
import sys
import time
from array import array
from pathlib import Path

import sherpa_onnx


SCRIPT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = SCRIPT_DIR / "models" / "sherpa-onnx-streaming-zipformer-small-ctc-zh-int8-2025-04-01"
MIC_BINARY = SCRIPT_DIR / "mic_pcm_stream"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live system-audio probe for sherpa-onnx.")
    parser.add_argument("--device-name", default="BlackHole 2ch")
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--chunk-ms", type=int, default=160)
    parser.add_argument("--duration-seconds", type=float, default=20.0)
    parser.add_argument("--threads", type=int, default=2)
    return parser.parse_args()


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


def pcm_bytes_to_floats(data: bytes) -> list[float]:
    ints = array("h")
    ints.frombytes(data[: len(data) - (len(data) % 2)])
    return [sample / 32768.0 for sample in ints]


def main() -> int:
    args = parse_args()
    if not MIC_BINARY.exists():
        raise SystemExit(f"Capture binary not found: {MIC_BINARY}")

    recognizer = make_recognizer(args.threads)
    stream = recognizer.create_stream()
    chunk_bytes = args.sample_rate * 2 * args.chunk_ms // 1000
    command = [
        str(MIC_BINARY),
        "--sample-rate",
        str(args.sample_rate),
        "--device-name",
        args.device_name,
    ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    assert process.stderr is not None

    start = time.monotonic()
    pending = bytearray()
    last_text = ""
    last_segment = None
    print(f"[live] device={args.device_name} chunk_ms={args.chunk_ms} duration={args.duration_seconds}s", flush=True)

    try:
        while time.monotonic() - start < args.duration_seconds:
            chunk = process.stdout.read(chunk_bytes)
            if not chunk:
                break
            pending.extend(chunk)
            while len(pending) >= chunk_bytes:
                piece = bytes(pending[:chunk_bytes])
                del pending[:chunk_bytes]
                stream.accept_waveform(args.sample_rate, pcm_bytes_to_floats(piece))
                while recognizer.is_ready(stream):
                    recognizer.decode_stream(stream)
                    result = recognizer.get_result_all(stream)
                    text = result.text.strip()
                    if text and (text != last_text or result.segment != last_segment):
                        print(
                            f"[partial] segment={result.segment} final={result.is_final} "
                            f"start={result.start_time:.2f} text={text}",
                            flush=True,
                        )
                        last_text = text
                        last_segment = result.segment
                    if recognizer.is_endpoint(stream):
                        print(f"[endpoint] segment={result.segment}", flush=True)
                        recognizer.reset(stream)
                        last_text = ""
                        last_segment = None
    finally:
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        stderr_text = process.stderr.read().decode("utf-8", errors="replace").strip()
        if stderr_text:
            print(stderr_text, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
