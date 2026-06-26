import argparse
import array
import json
import os
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any

from services.edge_tts_provider import EdgeTTSProvider
from services.tts_base import TTSProvider
from services.tts_factory import build_tts_provider as build_configured_tts_provider


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REVERSE_DIR = PROJECT_ROOT / "data" / "reverse"
REVERSE_DUBBED_AUDIO_DIR = REVERSE_DIR / "dubbed_audio"
REVERSE_OUTPUT_DIR = REVERSE_DIR / "output"
REVERSE_RETIME_PLAN_DIR = REVERSE_DIR / "retime_plans"
REVERSE_SUBTITLE_DIR = REVERSE_DIR / "subtitles"
REVERSE_TRANSLATION_DIR = REVERSE_DIR / "translations"
REVERSE_TRANSCRIPT_DIR = REVERSE_DIR / "transcripts"

MIN_SPEED = 0.7
MAX_SPEED = 1.6
PADDING_SECONDS = 0.05
MIN_SEGMENT_SECONDS = 0.5
NO_CHANGE_LOWER = 0.98
NO_CHANGE_UPPER = 1.02
MAX_SLOWDOWN_DELTA = 1.8
MAX_SPEEDUP_DELTA: float | None = None
EPSILON = 0.001
DEFAULT_EDGE_EN_VOICE = "en-US-GuyNeural"


def ensure_directories() -> None:
    REVERSE_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_DUBBED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_RETIME_PLAN_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_TRANSLATION_DIR.mkdir(parents=True, exist_ok=True)
    REVERSE_TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    return " ".join(str(text).strip().split())


def format_srt_timestamp(seconds: float) -> str:
    total_ms = max(int(round(seconds * 1000)), 0)
    hours = total_ms // 3_600_000
    minutes = (total_ms % 3_600_000) // 60_000
    secs = (total_ms % 60_000) // 1000
    millis = total_ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(entries: list[dict[str, Any]], output_path: Path) -> Path:
    lines: list[str] = []
    for index, entry in enumerate(entries, start=1):
        text = normalize_text(str(entry.get("text", "")))
        start = float(entry["start"])
        end = float(entry["end"])
        if not text or end <= start:
            continue
        lines.extend(
            [
                str(index),
                f"{format_srt_timestamp(start)} --> {format_srt_timestamp(end)}",
                text,
                "",
            ]
        )
    output_path.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[INFO] Subtitle file saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


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
        ffprobe_result = subprocess.run(
            ffprobe_command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        if ffprobe_result.returncode == 0 and ffprobe_result.stdout.strip():
            return float(ffprobe_result.stdout.strip())
    except FileNotFoundError:
        pass

    ffmpeg_result = subprocess.run(
        ["ffmpeg", "-i", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", ffmpeg_result.stderr or "")
    if duration_match:
        hours = int(duration_match.group(1))
        minutes = int(duration_match.group(2))
        seconds = float(duration_match.group(3))
        return hours * 3600 + minutes * 60 + seconds

    raise RuntimeError(f"Unable to determine media duration for {path}")


def resolve_source_video_path(stem: str) -> Path:
    candidates = [
        PROCESSED_DIR / f"{stem}.mp4",
        RAW_DIR / f"{stem}.mp4",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Matching source video not found for stem: {stem}")


def load_translation_items(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"Translation JSON must be a list: {path}")
    items: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        text = normalize_text(str(item.get("en", "")))
        if not text:
            continue
        items.append(
            {
                "start": round(float(item.get("start", 0.0) or 0.0), 3),
                "end": round(float(item.get("end", 0.0) or 0.0), 3),
                "text": text,
            }
        )
    if not items:
        raise ValueError(f"No translatable items found in: {path}")
    return items


def build_tts_provider() -> TTSProvider:
    provider_name = (os.getenv("TTS_PROVIDER") or "edge").strip().lower()
    if provider_name == "edge":
        voice = os.getenv("REVERSE_EDGE_TTS_VOICE", DEFAULT_EDGE_EN_VOICE)
        return EdgeTTSProvider(voice=voice)
    return build_configured_tts_provider(provider_name=provider_name)


def synthesize_missing_tts(
    base_name: str,
    items: list[dict[str, Any]],
    tts_provider: TTSProvider,
) -> list[dict[str, Any]]:
    updated = False
    for index, item in enumerate(items):
        text = normalize_text(str(item.get("text", "")))
        desired_tts_path = REVERSE_DUBBED_AUDIO_DIR / f"{base_name}_{index:04d}.mp3"
        if desired_tts_path.exists():
            item["tts_file"] = desired_tts_path.relative_to(PROJECT_ROOT).as_posix()
            item["tts_duration"] = round(get_media_duration(desired_tts_path), 3)
            continue

        print(f"[INFO] Generating English TTS {index + 1}/{len(items)}")
        generated_file, generated_duration = tts_provider.synthesize(text, desired_tts_path)
        tts_path = Path(generated_file).resolve()
        item["tts_file"] = tts_path.relative_to(PROJECT_ROOT).as_posix()
        item["tts_duration"] = round(float(generated_duration), 3)
        updated = True

    if updated:
        return items
    return items


def build_dubbed_audio(base_name: str, items: list[dict[str, Any]], video_path: Path) -> Path:
    output_audio_path = REVERSE_DUBBED_AUDIO_DIR / f"{base_name}_dubbed.wav"
    if output_audio_path.exists():
        print(f"[INFO] Skip existing dubbed audio: {output_audio_path.relative_to(PROJECT_ROOT)}")
        return output_audio_path

    video_duration_ms = int(get_media_duration(video_path) * 1000)
    end_marks = [
        int(max(float(item["end"]), float(item["start"]) + float(item.get("tts_duration", 0.0))) * 1000)
        for item in items
    ]
    total_duration_ms = max([video_duration_ms, *end_marks]) if end_marks else video_duration_ms

    print(f"[INFO] Building dubbed timeline audio: {base_name}")
    total_samples = max(int(total_duration_ms * 16), 1)
    mixed_samples = array.array("i", [0]) * total_samples

    for item in items:
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


def mux_video_with_audio(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    if output_path.exists():
        print(f"[INFO] Skip existing dubbed video: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

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
        str(output_path),
    ]
    print(f"[INFO] Muxing dubbed video: {video_path.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg video mux failed")

    print(f"[INFO] Dubbed video saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


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
        "en": item.get("text", ""),
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


def save_retime_plan(base_name: str, plan: list[dict[str, Any]], audio_duration: float, video_duration: float) -> Path:
    output_path = REVERSE_RETIME_PLAN_DIR / f"{base_name}.json"
    payload = {
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


def build_retimed_audio(base_name: str, plan: list[dict[str, Any]]) -> Path:
    output_audio_path = REVERSE_DUBBED_AUDIO_DIR / f"{base_name}_retimed_v4.wav"
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

    print(f"[INFO] Building retimed dubbed audio: {base_name}")
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


def render_retimed_video(video_path: Path, plan: list[dict[str, Any]], output_audio_path: Path, output_path: Path) -> Path:
    if output_path.exists():
        print(f"[INFO] Skip existing retimed video: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

    command = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(output_audio_path)]
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


def process_reverse_translation(translation_path: Path, tts_provider: TTSProvider) -> tuple[Path, Path]:
    translation_path = translation_path.resolve()
    base_name = translation_path.stem
    if base_name.endswith("_en"):
        source_stem = base_name[:-3]
    else:
        source_stem = base_name

    source_video = resolve_source_video_path(source_stem)
    video_duration = get_media_duration(source_video)
    items = load_translation_items(translation_path)
    items = synthesize_missing_tts(base_name, items, tts_provider)

    transcript_path = REVERSE_TRANSCRIPT_DIR / f"{base_name}_items.json"
    transcript_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] Saved reverse transcript items: {transcript_path.relative_to(PROJECT_ROOT)}")

    normal_srt = REVERSE_SUBTITLE_DIR / f"{base_name}.srt"
    write_srt(items, normal_srt)

    dubbed_audio_path = build_dubbed_audio(base_name, items, source_video)
    dubbed_video_path = REVERSE_OUTPUT_DIR / f"{base_name}_dubbed.mp4"
    mux_video_with_audio(source_video, dubbed_audio_path, dubbed_video_path)

    audio_duration = get_media_duration(dubbed_audio_path)
    plan = build_retime_plan(items, video_duration)
    plan_path = save_retime_plan(base_name, plan, audio_duration, video_duration)

    # keep tts_file references aligned with the generated clips
    for segment, item in zip((s for s in plan if s["kind"] == "speech"), items):
        segment["tts_file"] = item.get("tts_file", "")

    retimed_audio_path = build_retimed_audio(base_name, plan)
    retimed_video_path = REVERSE_OUTPUT_DIR / f"{base_name}_retimed_v4.mp4"
    render_retimed_video(source_video, plan, retimed_audio_path, retimed_video_path)

    retimed_srt = REVERSE_SUBTITLE_DIR / f"{base_name}_retimed_v4.srt"
    retimed_entries = [
        {"start": float(seg["output_start"]), "end": float(seg["output_end"]), "text": str(seg.get("en", ""))}
        for seg in plan
        if seg["kind"] == "speech"
    ]
    write_srt(retimed_entries, retimed_srt)

    final_srt = retimed_srt.with_name(f"{retimed_srt.stem}_final.srt")
    final_srt.write_text(retimed_srt.read_text(encoding="utf-8-sig"), encoding="utf-8-sig")
    print(f"[INFO] Final subtitle copied to: {final_srt.relative_to(PROJECT_ROOT)}")

    return retimed_video_path, final_srt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finish the reverse Bilibili translation pipeline.")
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Optional English translation JSON path. If omitted, use the newest one in data/reverse/translations.",
    )
    return parser.parse_args()


def resolve_default_translation_path() -> Path:
    candidates = sorted(REVERSE_TRANSLATION_DIR.glob("*_en.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError("No reverse translation JSON found in data/reverse/translations.")
    return candidates[0]


def main() -> int:
    args = parse_args()
    try:
        ensure_directories()
        translation_path = Path(args.input_path).resolve() if args.input_path else resolve_default_translation_path()
        tts_provider = build_tts_provider()
        print(f"[INFO] Using translation JSON: {translation_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Using TTS provider: {tts_provider.__class__.__name__}")
        retimed_video_path, final_srt = process_reverse_translation(translation_path, tts_provider)
        print("[INFO] Reverse finish completed.")
        print(f"[INFO] Retimed video: {retimed_video_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Final subtitle: {final_srt.relative_to(PROJECT_ROOT)}")
        return 0
    except Exception as exc:
        print(f"[ERROR] Reverse finish failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
