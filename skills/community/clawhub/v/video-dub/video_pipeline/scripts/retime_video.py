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


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
STRUCTURED_DIR = PROJECT_ROOT / "data" / "structured"
DUBBED_AUDIO_DIR = PROJECT_ROOT / "data" / "dubbed_audio"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
RETIME_PLAN_DIR = PROJECT_ROOT / "data" / "state" / "retime_plans"

MIN_SPEED = 0.7
MAX_SPEED = 1.6
PADDING_SECONDS = 0.05
MIN_SEGMENT_SECONDS = 0.5
NO_CHANGE_LOWER = 0.95
NO_CHANGE_UPPER = 1.02
NO_CHANGE_LOWER = 0.98
MAX_SLOWDOWN_DELTA = 1.8
MAX_SPEEDUP_DELTA: float | None = None
EPSILON = 0.001


def ensure_directories() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RETIME_PLAN_DIR.mkdir(parents=True, exist_ok=True)


def load_structured_items(structured_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(structured_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Structured JSON must be a list: {structured_path}")
    return payload


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


def resolve_video_path(structured_path: Path) -> Path:
    candidates = [
        PROCESSED_DIR / f"{structured_path.stem}.mp4",
        RAW_DIR / f"{structured_path.stem}.mp4",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Matching video not found for structured JSON: {structured_path.name}")


def resolve_audio_path(structured_path: Path) -> Path:
    candidates = [
        DUBBED_AUDIO_DIR / f"{structured_path.stem}_zh_male.wav",
        DUBBED_AUDIO_DIR / f"{structured_path.stem}_zh.wav",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Matching dubbed audio not found for structured JSON: {structured_path.name}")


def create_gap_entry(start: float, end: float) -> dict[str, Any]:
    duration = round(end - start, 3)
    return {
        "kind": "gap",
        "start": round(start, 3),
        "end": round(end, 3),
        "orig_duration": duration,
        "tts_duration": 0.0,
        "target_duration": duration,
        "speed": 1.0,
        "applied_speed": 1.0,
        "skip_reason": "gap",
    }


def create_speech_entry(item: dict[str, Any]) -> dict[str, Any]:
    start = float(item["start"])
    end = float(item["end"])
    orig_duration = max(end - start, 0.0)
    tts_duration = float(item.get("tts_duration", 0.0) or 0.0)
    target_duration = tts_duration + PADDING_SECONDS if tts_duration > 0 else orig_duration
    speed = orig_duration / target_duration if target_duration > 0 else 1.0
    applied_speed = speed
    skip_reason = ""

    if orig_duration < MIN_SEGMENT_SECONDS:
        applied_speed = 1.0
        target_duration = orig_duration
        skip_reason = "segment_too_short"
    elif tts_duration <= 0:
        applied_speed = 1.0
        target_duration = orig_duration
        skip_reason = "missing_tts_duration"
    elif NO_CHANGE_LOWER <= speed <= NO_CHANGE_UPPER:
        applied_speed = 1.0
        target_duration = orig_duration
        skip_reason = "within_tolerance"
    else:
        applied_speed = min(MAX_SPEED, max(MIN_SPEED, speed))
        clamped_target = orig_duration / applied_speed
        if clamped_target - orig_duration > MAX_SLOWDOWN_DELTA:
            clamped_target = orig_duration + MAX_SLOWDOWN_DELTA
            applied_speed = orig_duration / clamped_target
            skip_reason = "limited_by_max_slowdown"
        elif MAX_SPEEDUP_DELTA is not None and orig_duration - clamped_target > MAX_SPEEDUP_DELTA:
            clamped_target = orig_duration - MAX_SPEEDUP_DELTA
            applied_speed = orig_duration / clamped_target
            skip_reason = "limited_by_max_speedup"
        elif abs(applied_speed - speed) > EPSILON:
            skip_reason = "clamped_to_speed_range"
        target_duration = clamped_target

    return {
        "kind": "speech",
        "start": round(start, 3),
        "end": round(end, 3),
        "orig_duration": round(orig_duration, 3),
        "tts_duration": round(tts_duration, 3),
        "target_duration": round(target_duration, 3),
        "speed": round(speed, 3),
        "applied_speed": round(applied_speed, 3),
        "skip_reason": skip_reason,
        "en": item.get("en", ""),
        "zh": item.get("zh", ""),
    }


def build_retime_plan(items: list[dict[str, Any]], video_duration: float) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    cursor = 0.0

    for item in items:
        start = float(item["start"])
        end = float(item["end"])
        if start - cursor > EPSILON:
            plan.append(create_gap_entry(cursor, start))
        plan.append(create_speech_entry(item))
        cursor = max(cursor, end)

    if video_duration - cursor > EPSILON:
        plan.append(create_gap_entry(cursor, video_duration))

    output_cursor = 0.0
    for segment in plan:
        segment["output_start"] = round(output_cursor, 3)
        output_cursor += float(segment["target_duration"])
        segment["output_end"] = round(output_cursor, 3)

    return plan


def save_retime_plan(structured_path: Path, plan: list[dict[str, Any]], audio_duration: float, video_duration: float) -> Path:
    output_path = RETIME_PLAN_DIR / f"{structured_path.stem}.json"
    payload = {
        "source_video": str((RAW_DIR / f"{structured_path.stem}.mp4").relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "source_audio": str((DUBBED_AUDIO_DIR / f"{structured_path.stem}_zh.wav").relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "source_video_duration": round(video_duration, 3),
        "dubbed_audio_duration": round(audio_duration, 3),
        "rules": {
            "min_speed": MIN_SPEED,
            "max_speed": MAX_SPEED,
            "padding_seconds": PADDING_SECONDS,
            "min_segment_seconds": MIN_SEGMENT_SECONDS,
            "no_change_range": [NO_CHANGE_LOWER, NO_CHANGE_UPPER],
            "max_slowdown_delta": MAX_SLOWDOWN_DELTA,
            "max_speedup_delta": MAX_SPEEDUP_DELTA,
        },
        "segments": plan,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] Retime plan saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def build_retimed_audio(structured_path: Path, plan: list[dict[str, Any]]) -> Path:
    output_audio_path = DUBBED_AUDIO_DIR / f"{structured_path.stem}_zh_retimed_v4.wav"
    total_duration = max(float(segment["output_end"]) for segment in plan) if plan else 0.0
    total_samples = max(int(total_duration * 16000), 1)
    mixed_samples = array.array("i", [0]) * total_samples

    for segment in plan:
        if segment["kind"] != "speech":
            continue
        tts_file = segment.get("tts_file")
        if not tts_file:
            continue
        tts_path = (PROJECT_ROOT / Path(tts_file)).resolve()
        output_start_sample = max(int(float(segment["output_start"]) * 16000), 0)
        clip_samples = decode_audio_to_pcm_samples(tts_path)

        for sample_index, sample in enumerate(clip_samples):
            mix_index = output_start_sample + sample_index
            if mix_index >= total_samples:
                break
            mixed_samples[mix_index] += sample

    print(f"[INFO] Building retimed dubbed audio: {structured_path.stem}")
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

    print(f"[INFO] Retimed dubbed audio saved to: {output_audio_path.relative_to(PROJECT_ROOT)}")
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


def retime_video(structured_path: Path, plan: list[dict[str, Any]], video_path: Path, audio_path: Path) -> Path:
    output_path = OUTPUT_DIR / f"{structured_path.stem}_zh_retimed_v4.mp4"

    command = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path)]
    filter_lines: list[str] = []
    concat_inputs: list[str] = []

    for index, segment in enumerate(plan):
        start = float(segment["start"])
        end = float(segment["end"])
        if end - start <= EPSILON:
            continue
        speed = float(segment["applied_speed"])
        setpts_factor = 1.0 / speed if speed > 0 else 1.0
        filter_lines.append(
            f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts={setpts_factor:.6f}*(PTS-STARTPTS)[v{index}]"
        )
        concat_inputs.append(f"[v{index}]")

    if not concat_inputs:
        raise ValueError("No valid segments available for retiming.")

    filter_lines.append(f"{''.join(concat_inputs)}concat=n={len(concat_inputs)}:v=1:a=0[outv]")

    with tempfile.NamedTemporaryFile("w", suffix=".ffscript", delete=False, encoding="utf-8") as fp:
        fp.write(";\n".join(filter_lines))
        filter_script_path = Path(fp.name)

    command.extend(
        [
            "-filter_complex_script",
            str(filter_script_path),
            "-map",
            "[outv]",
            "-map",
            "1:a:0",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "23",
            "-threads",
            "4",
            "-x264-params",
            "ref=1:rc-lookahead=0",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(output_path),
        ]
    )

    print(f"[INFO] Rendering retimed video: {video_path.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(command, capture_output=True, text=True)
    try:
        filter_script_path.unlink(missing_ok=True)
    except Exception:
        pass
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed to render retimed video")

    print(f"[INFO] Retimed video saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def process_file(structured_path: Path) -> tuple[Path, Path]:
    structured_path = structured_path.resolve()
    items = load_structured_items(structured_path)
    video_path = resolve_video_path(structured_path)
    _ = resolve_audio_path(structured_path)
    video_duration = get_media_duration(video_path)
    audio_duration = get_media_duration(resolve_audio_path(structured_path))

    plan = build_retime_plan(items, video_duration)
    plan_path = save_retime_plan(structured_path, plan, audio_duration, video_duration)
    for segment, item in zip((s for s in plan if s["kind"] == "speech"), items):
        segment["tts_file"] = item.get("tts_file", "")
    retimed_audio_path = build_retimed_audio(structured_path, plan)
    output_path = retime_video(structured_path, plan, video_path, retimed_audio_path)
    return plan_path, output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retimed local video segments to better fit Chinese dubbing duration.")
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Optional single structured JSON path. If omitted, scan data/structured/*.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_directories()

    if args.input_path:
        structured_files = [Path(args.input_path).resolve()]
    else:
        structured_files = [path.resolve() for path in sorted(STRUCTURED_DIR.glob("*.json"))]

    if not structured_files:
        print("[WARN] No structured JSON files found. Nothing to process.")
        return 0

    had_error = False
    for structured_path in structured_files:
        try:
            process_file(structured_path)
        except Exception as exc:
            had_error = True
            print(f"[ERROR] Failed to retime video for: {structured_path}", file=sys.stderr)
            print(f"[ERROR] Reason: {exc}", file=sys.stderr)

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
