import argparse
import array
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any

from services.tts_base import TTSProvider
from services.tts_factory import build_tts_provider as build_configured_tts_provider


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
STRUCTURED_DIR = PROJECT_ROOT / "data" / "structured"
TTS_DIR = PROJECT_ROOT / "data" / "tts"
DUBBED_AUDIO_DIR = PROJECT_ROOT / "data" / "dubbed_audio"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
VIDEO_META_DIR = PROJECT_ROOT / "data" / "state" / "video_meta"
INTRO_GAP_SECONDS = 0.2
INTRO_WINDOW_SECONDS = 10.0


def ensure_directories() -> None:
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    DUBBED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_tts_provider(structured_path: Path | None = None) -> TTSProvider:
    voice_type = None
    if structured_path is not None:
        meta_path = VIDEO_META_DIR / f"{structured_path.stem}.json"
        if meta_path.exists():
            payload = json.loads(meta_path.read_text(encoding="utf-8"))
            settings = payload.get("settings", {})
            voice_type = str(settings.get("voice_type", "")).strip() or None
    return build_configured_tts_provider(voice_type=voice_type)


def load_structured_items(structured_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(structured_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Structured JSON must be a list: {structured_path}")
    return payload


def save_structured_items(structured_path: Path, items: list[dict[str, Any]]) -> None:
    structured_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def synthesize_missing_tts(
    structured_path: Path,
    items: list[dict[str, Any]],
    tts_provider: TTSProvider,
) -> list[dict[str, Any]]:
    base_name = structured_path.stem
    updated = False

    for index, item in enumerate(items):
        zh_text = str(item.get("zh", "")).strip()
        tts_text = str(item.get("tts_text", zh_text)).strip()
        tts_file = item.get("tts_file", "")
        tts_duration = float(item.get("tts_duration", 0.0) or 0.0)
        desired_tts_path = (TTS_DIR / f"{base_name}_{index:04d}.mp3").resolve()
        if tts_file:
            existing_tts_path = (PROJECT_ROOT / Path(tts_file)).resolve()
        else:
            existing_tts_path = desired_tts_path

        if existing_tts_path == desired_tts_path and desired_tts_path.exists():
            actual_duration = get_audio_clip_duration(desired_tts_path)
            item["tts_file"] = desired_tts_path.relative_to(PROJECT_ROOT).as_posix()
            item["tts_duration"] = round(actual_duration, 3)
            updated = True
            continue

        if (not desired_tts_path.exists()) or tts_duration <= 0 or existing_tts_path != desired_tts_path:
            print(f"[INFO] Generating TTS for sentence {index + 1}/{len(items)}")
            generated_file, generated_duration = tts_provider.synthesize(
                tts_text,
                desired_tts_path,
            )
            tts_path = Path(generated_file).resolve()
            item["tts_file"] = tts_path.relative_to(PROJECT_ROOT).as_posix()
            item["tts_duration"] = round(float(generated_duration), 3)
            updated = True

    updated = adjust_intro_timing(items) or updated

    if updated:
        save_structured_items(structured_path, items)

    return items


def adjust_intro_timing(items: list[dict[str, Any]]) -> bool:
    if len(items) < 2:
        return False

    first_item = items[0]
    second_item = items[1]
    first_start = float(first_item.get("start", 0.0) or 0.0)
    first_tts_duration = float(first_item.get("tts_duration", 0.0) or 0.0)
    second_start = float(second_item.get("start", 0.0) or 0.0)
    second_end = float(second_item.get("end", 0.0) or 0.0)
    if first_tts_duration <= 0 or second_end <= second_start:
        return False

    desired_second_start = round(first_start + first_tts_duration + INTRO_GAP_SECONDS, 3)
    desired_second_start = min(desired_second_start, INTRO_WINDOW_SECONDS)
    new_second_start = min(second_start, desired_second_start)
    new_second_start = max(first_start, new_second_start)
    if second_end - new_second_start < 0.5:
        new_second_start = max(first_start, round(second_end - 0.5, 3))

    current_first_end = float(first_item.get("end", 0.0) or 0.0)
    if abs(new_second_start - second_start) < 0.001 and abs(current_first_end - new_second_start) < 0.001:
        return False

    first_item["end"] = round(new_second_start, 3)
    second_item["start"] = round(new_second_start, 3)
    return True


def get_audio_clip_duration(path: Path) -> float:
    if path.suffix.lower() == ".wav":
        with wave.open(str(path), "rb") as wav_file:
            frames = wav_file.getnframes()
            frame_rate = wav_file.getframerate()
            if frame_rate > 0:
                return frames / float(frame_rate)
    return get_media_duration(path)


def get_media_duration(path: Path) -> float:
    try:
        ffprobe_command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
        ffprobe_result = subprocess.run(ffprobe_command, capture_output=True, text=True)
        if ffprobe_result.returncode == 0 and ffprobe_result.stdout.strip():
            return float(ffprobe_result.stdout.strip())
    except FileNotFoundError:
        pass

    ffmpeg_result = subprocess.run(["ffmpeg", "-i", str(path)], capture_output=True, text=True)
    duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", ffmpeg_result.stderr)
    if duration_match:
        hours = int(duration_match.group(1))
        minutes = int(duration_match.group(2))
        seconds = float(duration_match.group(3))
        return hours * 3600 + minutes * 60 + seconds

    raise RuntimeError(f"Unable to determine media duration for {path}")


def build_dubbed_audio(
    structured_path: Path,
    items: list[dict[str, Any]],
    video_path: Path,
) -> Path:
    output_audio_path = DUBBED_AUDIO_DIR / f"{structured_path.stem}_zh_male.wav"
    if output_audio_path.exists():
        print(f"[INFO] Skip existing dubbed audio: {output_audio_path.relative_to(PROJECT_ROOT)}")
        return output_audio_path

    video_duration_ms = int(get_media_duration(video_path) * 1000)
    end_marks = [
        int(max(float(item["end"]), float(item["start"]) + float(item.get("tts_duration", 0.0))) * 1000)
        for item in items
    ]
    total_duration_ms = max([video_duration_ms, *end_marks]) if end_marks else video_duration_ms

    print(f"[INFO] Building dubbed timeline audio: {structured_path.stem}")
    total_samples = max(int(total_duration_ms * 16), 1)
    mixed_samples = array.array("i", [0]) * total_samples

    for index, item in enumerate(items, start=1):
        tts_path = (PROJECT_ROOT / Path(item["tts_file"])).resolve()
        start_sample = max(int(float(item["start"]) * 16000), 0)
        clip_samples = decode_audio_to_pcm_samples(tts_path)

        for sample_index, sample in enumerate(clip_samples):
            mix_index = start_sample + sample_index
            if mix_index >= total_samples:
                break
            mixed_samples[mix_index] += sample

    output_samples = array.array("h")
    for sample in mixed_samples:
        if sample > 32767:
            output_samples.append(32767)
        elif sample < -32768:
            output_samples.append(-32768)
        else:
            output_samples.append(sample)

    with wave.open(str(output_audio_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(output_samples.tobytes())

    print(f"[INFO] Dubbed audio saved to: {output_audio_path.relative_to(PROJECT_ROOT)}")
    return output_audio_path


def decode_audio_to_pcm_samples(path: Path) -> array.array:
    command = [
        "ffmpeg",
        "-v",
        "error",
        "-i",
        str(path),
        "-f",
        "s16le",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-",
    ]
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="ignore").strip()
        raise RuntimeError(stderr or f"ffmpeg failed to decode audio: {path}")

    samples = array.array("h")
    samples.frombytes(result.stdout)
    return samples


def resolve_video_path(structured_path: Path) -> Path:
    candidates = [
        PROCESSED_DIR / f"{structured_path.stem}.mp4",
        RAW_DIR / f"{structured_path.stem}.mp4",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Matching video not found for structured JSON: {structured_path.name}")


def mux_video_with_audio(video_path: Path, audio_path: Path) -> Path:
    output_video_path = OUTPUT_DIR / f"{video_path.stem}_zh_male.mp4"
    if output_video_path.exists():
        print(f"[INFO] Skip existing dubbed video: {output_video_path.relative_to(PROJECT_ROOT)}")
        return output_video_path

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        str(output_video_path),
    ]
    print(f"[INFO] Muxing dubbed video: {video_path.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg video mux failed")

    print(f"[INFO] Dubbed video saved to: {output_video_path.relative_to(PROJECT_ROOT)}")
    return output_video_path


def generate_dubbed_video(structured_path: Path, tts_provider: TTSProvider | None = None) -> Path:
    ensure_directories()
    structured_path = structured_path.resolve()
    tts_provider = tts_provider or build_tts_provider(structured_path)
    items = load_structured_items(structured_path)
    items = synthesize_missing_tts(structured_path, items, tts_provider)
    video_path = resolve_video_path(structured_path)
    dubbed_audio_path = build_dubbed_audio(structured_path, items, video_path)
    return mux_video_with_audio(video_path, dubbed_audio_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Chinese TTS audio and a dubbed video.")
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Optional single structured JSON path. If omitted, scan data/structured/*.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        ensure_directories()
        tts_provider = build_tts_provider()
        if args.input_path:
            structured_files = [Path(args.input_path).resolve()]
        else:
            structured_files = [path.resolve() for path in sorted(STRUCTURED_DIR.glob("*.json"))]

        if not structured_files:
            print("[WARN] No structured subtitle JSON files found. Nothing to process.")
            return 0

        for structured_path in structured_files:
            try:
                generate_dubbed_video(structured_path, tts_provider)
            except Exception as exc:
                print(f"[ERROR] Failed to generate dubbed video: {structured_path}", file=sys.stderr)
                print(f"[ERROR] Reason: {exc}", file=sys.stderr)
    except Exception as exc:
        print(f"[ERROR] Failed to run dubbing pipeline: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
