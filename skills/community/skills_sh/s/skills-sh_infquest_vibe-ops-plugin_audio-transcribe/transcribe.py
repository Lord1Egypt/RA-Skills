#!/usr/bin/env -S uv run --script --python 3.12
# /// script
# requires-python = "==3.12.*"
# dependencies = [
#     "torch==2.3.1",
#     "torchaudio==2.3.1",
#     "whisperx==3.3.1",
#     "pyannote.audio==3.3.2",
#     "transformers==4.44.0",
#     "matplotlib",
# ]
# ///

"""
Audio transcription using WhisperX with word-level timestamps.

Usage:
    uv run transcribe.py <audio_file> [options]

Examples:
    uv run transcribe.py audio.mp3
    uv run transcribe.py audio.mp3 --model medium --language zh
    uv run transcribe.py audio.mp3 --no-align --output transcript.json
"""

import argparse
import json
import os
from dataclasses import asdict, dataclass
from typing import List, Optional


@dataclass
class TranscriptWord:
    """A single word with timestamp."""

    word: str
    start: float
    end: float
    score: float


@dataclass
class TranscriptSegment:
    """A transcript segment with optional word-level timestamps."""

    start_at: float
    end_at: float
    text: str
    words: List[TranscriptWord]


def transcribe_audio(
    audio_path: str,
    model_name: str = "base",
    language: Optional[str] = None,
    batch_size: int = 8,
    align: bool = True,
    device: str = "cpu",
    vad_filter: bool = True,
) -> List[TranscriptSegment]:
    """Transcribe audio file using WhisperX with optional word-level timestamps.

    Args:
        audio_path: Path to the audio file to transcribe.
        model_name: Whisper model size ("tiny", "base", "small", "medium", "large-v2").
        language: Language code (e.g., "en", "zh"). If None, auto-detect.
        batch_size: Batch size for processing.
        align: If True, perform word-level forced alignment.
        device: Device to use ("cpu" or "cuda").
        vad_filter: If True, use VAD to filter non-speech segments.

    Returns:
        List of TranscriptSegment objects.
    """
    import whisperx

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    compute_type = "int8" if device == "cpu" else "float16"
    asr_options = {"suppress_numerals": False}

    print(f"Loading WhisperX model: {model_name} (device={device})")

    # VAD options - lower onset/offset = more sensitive (catches more speech)
    vad_options = None
    if not vad_filter:
        # Very low thresholds to catch almost everything
        vad_options = {"vad_onset": 0.1, "vad_offset": 0.1}

    model = whisperx.load_model(
        model_name,
        device=device,
        compute_type=compute_type,
        asr_options=asr_options,
        vad_options=vad_options,
    )

    print(f"Transcribing: {audio_path}")
    if not vad_filter:
        print("VAD filter disabled - processing all audio segments")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=batch_size, language=language)

    detected_language = result.get("language", "en")
    print(f"Detected language: {detected_language}")
    print(f"Found {len(result['segments'])} segments")

    # Convert to TranscriptSegment (without word-level timestamps)
    segments: List[TranscriptSegment] = []
    for seg in result["segments"]:
        segments.append(
            TranscriptSegment(
                start_at=float(seg["start"]),
                end_at=float(seg["end"]),
                text=seg["text"].strip(),
                words=[],
            )
        )

    # Perform word-level alignment if requested
    if align:
        segments = align_segments(segments, audio_path, detected_language, device)

    return segments


def align_segments(
    segments: List[TranscriptSegment],
    audio_path: str,
    language: str,
    device: str = "cpu",
) -> List[TranscriptSegment]:
    """Align transcript segments to get word-level timestamps.

    Args:
        segments: List of TranscriptSegment objects to align.
        audio_path: Path to the audio file.
        language: Language code.
        device: Device to use.

    Returns:
        List of TranscriptSegment with word-level timestamps.
    """
    import whisperx

    print("Loading alignment model...")
    model_a, metadata = whisperx.load_align_model(language_code=language, device=device)

    # Convert to whisperx format
    whisperx_segments = [
        {"start": seg.start_at, "end": seg.end_at, "text": seg.text} for seg in segments
    ]

    print("Aligning transcription for word-level timestamps...")
    audio = whisperx.load_audio(audio_path)
    aligned_result = whisperx.align(
        whisperx_segments,
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    # Convert back to TranscriptSegment with words
    aligned_segments: List[TranscriptSegment] = []
    for seg in aligned_result["segments"]:
        words = []
        for w in seg.get("words", []):
            if "start" in w and "end" in w:
                words.append(
                    TranscriptWord(
                        word=w["word"],
                        start=float(w["start"]),
                        end=float(w["end"]),
                        score=float(w.get("score", 0.0)),
                    )
                )

        aligned_segments.append(
            TranscriptSegment(
                start_at=float(seg["start"]),
                end_at=float(seg["end"]),
                text=seg["text"].strip(),
                words=words,
            )
        )

    total_words = sum(len(seg.words) for seg in aligned_segments)
    print(f"Aligned {total_words} words")

    return aligned_segments


def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def format_srt(segments: List[TranscriptSegment]) -> str:
    """Format segments as SRT subtitle format."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg.start_at).replace(".", ",")
        end = format_timestamp(seg.end_at).replace(".", ",")
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg.text)
        lines.append("")
    return "\n".join(lines)


def format_vtt(segments: List[TranscriptSegment]) -> str:
    """Format segments as WebVTT subtitle format."""
    lines = ["WEBVTT", ""]
    for seg in segments:
        start = format_timestamp(seg.start_at)
        end = format_timestamp(seg.end_at)
        lines.append(f"{start} --> {end}")
        lines.append(seg.text)
        lines.append("")
    return "\n".join(lines)


def format_txt(segments: List[TranscriptSegment]) -> str:
    """Format segments as plain text with timestamps."""
    lines = []
    for seg in segments:
        start = format_timestamp(seg.start_at)
        end = format_timestamp(seg.end_at)
        lines.append(f"[{start} - {end}] {seg.text}")
    return "\n".join(lines)


def format_json(segments: List[TranscriptSegment]) -> str:
    """Format segments as JSON."""
    data = []
    for seg in segments:
        seg_dict = {
            "start": seg.start_at,
            "end": seg.end_at,
            "text": seg.text,
        }
        if seg.words:
            seg_dict["words"] = [asdict(w) for w in seg.words]
        data.append(seg_dict)
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio using WhisperX with word-level timestamps"
    )
    parser.add_argument("audio_file", help="Path to audio file")
    parser.add_argument(
        "--model",
        "-m",
        default="base",
        choices=["tiny", "base", "small", "medium", "large-v2"],
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--language",
        "-l",
        default=None,
        help="Language code (e.g., en, zh). Auto-detect if not specified",
    )
    parser.add_argument(
        "--no-align", action="store_true", help="Skip word-level alignment (faster)"
    )
    parser.add_argument(
        "--no-vad",
        action="store_true",
        help="Disable VAD filtering (use if transcription has gaps/missing segments)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path. Format determined by extension (.srt, .vtt, .txt, .json)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default=None,
        choices=["srt", "vtt", "txt", "json"],
        help="Output format (overrides extension detection)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to use (default: cpu)",
    )

    args = parser.parse_args()

    # Transcribe
    segments = transcribe_audio(
        audio_path=args.audio_file,
        model_name=args.model,
        language=args.language,
        align=not args.no_align,
        device=args.device,
        vad_filter=not args.no_vad,
    )

    # Determine output format
    output_format = args.format
    if output_format is None and args.output:
        ext = os.path.splitext(args.output)[1].lower()
        output_format = ext[1:] if ext else "txt"
    output_format = output_format or "txt"

    # Format output
    if output_format == "srt":
        output = format_srt(segments)
    elif output_format == "vtt":
        output = format_vtt(segments)
    elif output_format == "json":
        output = format_json(segments)
    else:
        output = format_txt(segments)

    # Write or print output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nTranscript saved to: {args.output}")
    else:
        print("\n" + "=" * 50)
        print("TRANSCRIPT")
        print("=" * 50)
        print(output)


if __name__ == "__main__":
    main()
