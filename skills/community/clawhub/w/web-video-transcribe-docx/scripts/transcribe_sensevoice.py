#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import wave
from pathlib import Path

try:
    import numpy as np
    import sherpa_onnx
except ImportError as exc:
    raise SystemExit(
        "Missing transcription dependencies. Run `python scripts/bootstrap_env.py` first."
    ) from exc

from pipeline_common import ensure_sensevoice_model, format_seconds, segment_media
from transcript_to_docx import write_docx_from_text


NORMALIZE_REPLACEMENTS = {
    "事频": "视频",
    "势频": "视频",
    "谋选": "毛选",
    "某选": "毛选",
    "神做": "神作",
    "立经": "历经",
    "正聋发聩": "振聋发聩",
    "阵聋发聩": "振聋发聩",
    "前数年": "前苏联",
    "造猫画虎": "照猫画虎",
    "辅持": "扶持",
    "时间那位到": "时间回到",
}


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"\s+", "", text)
    for old, new in NORMALIZE_REPLACEMENTS.items():
        cleaned = cleaned.replace(old, new)
    return cleaned.strip()


def load_wav(path: Path) -> tuple[int, np.ndarray, float]:
    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        frame_count = wav_file.getnframes()
        data = wav_file.readframes(frame_count)
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    duration = frame_count / float(sample_rate)
    return sample_rate, samples, duration


def build_recognizer(model_dir: Path, threads: int, language: str) -> sherpa_onnx.OfflineRecognizer:
    return sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=str(model_dir / "model.int8.onnx"),
        tokens=str(model_dir / "tokens.txt"),
        num_threads=threads,
        language=language,
        use_itn=True,
    )


def transcribe_media(
    input_path: Path,
    *,
    segment_seconds: int = 600,
    threads: int = 4,
    language: str = "zh",
    model_dir: Path | None = None,
) -> str:
    resolved_model_dir = ensure_sensevoice_model(model_dir)
    recognizer = build_recognizer(resolved_model_dir, threads, language)
    temp_root = Path(tempfile.mkdtemp(prefix="web-video-transcribe-docx-"))
    try:
        segments = segment_media(input_path, temp_root / "segments", segment_seconds=segment_seconds)
        if not segments:
            raise RuntimeError("No audio segments were created from the input media.")

        cursor = 0.0
        lines: list[str] = []
        for segment in segments:
            sample_rate, samples, duration = load_wav(segment)
            stream = recognizer.create_stream()
            stream.accept_waveform(sample_rate, samples)
            recognizer.decode_stream(stream)
            text = normalize_text(stream.result.text)
            start_text = format_seconds(cursor)
            end_text = format_seconds(cursor + duration)
            stamp = f"[{start_text}-{end_text}]"
            lines.append(stamp if not text else f"{stamp} {text}")
            cursor += duration
        return "\n\n".join(lines).strip() + "\n"
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run offline SenseVoice transcription on a local media file.")
    parser.add_argument("--input", required=True, help="Input local media file")
    parser.add_argument("--output-txt", required=True, help="Transcript output path")
    parser.add_argument("--output-docx", help="Optional DOCX output path")
    parser.add_argument("--title", help="Optional document title for DOCX")
    parser.add_argument("--segment-seconds", type=int, default=600, help="Segment length for ffmpeg splitting")
    parser.add_argument("--threads", type=int, default=4, help="Number of ASR threads")
    parser.add_argument(
        "--language",
        default="zh",
        choices=["auto", "zh", "en", "ja", "ko", "yue"],
        help="SenseVoice language hint",
    )
    parser.add_argument("--model-dir", help="Optional pre-downloaded model directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_txt = Path(args.output_txt)
    model_dir = Path(args.model_dir) if args.model_dir else None

    text = transcribe_media(
        input_path,
        segment_seconds=args.segment_seconds,
        threads=args.threads,
        language=args.language,
        model_dir=model_dir,
    )
    output_txt.write_text(text, encoding="utf-8")
    print(f"Saved transcript: {output_txt.resolve()}")

    if args.output_docx:
        output_docx = Path(args.output_docx)
        write_docx_from_text(text, output_docx, title=args.title or input_path.stem)
        print(f"Saved DOCX: {output_docx.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
