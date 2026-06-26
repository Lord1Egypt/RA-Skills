import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import whisper

import add_subtitles
import download
import dub_video
import enrich_subtitles
import extract_audio
import prepare_video
import retime_video
import transcribe


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TTS_DIR = PROJECT_ROOT / "data" / "tts"
DUBBED_AUDIO_DIR = PROJECT_ROOT / "data" / "dubbed_audio"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
RETIME_PLAN_DIR = PROJECT_ROOT / "data" / "state" / "retime_plans"
SUBTITLE_DIR = PROJECT_ROOT / "data" / "subtitles"
STRUCTURED_DIR = PROJECT_ROOT / "data" / "structured"
WHISPER_MODEL_NAME = "small"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Quick delivery pipeline: output retimed Chinese video and SRT without burning subtitles."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--refresh-tts",
        action="store_true",
        help="Regenerate TTS, dubbed audio, retimed audio, delivery videos, and SRT files for this video.",
    )
    return parser.parse_args()


def cleanup_delivery_outputs(base_name: str) -> None:
    for path in TTS_DIR.glob(f"{base_name}_*.mp3"):
        path.unlink(missing_ok=True)

    cleanup_paths = [
        DUBBED_AUDIO_DIR / f"{base_name}_zh_male.wav",
        DUBBED_AUDIO_DIR / f"{base_name}_zh_retimed_v4.wav",
        OUTPUT_DIR / f"{base_name}_zh_male.mp4",
        OUTPUT_DIR / f"{base_name}_zh_retimed_v4.mp4",
        RETIME_PLAN_DIR / f"{base_name}.json",
        STRUCTURED_DIR / f"{base_name}.json",
        SUBTITLE_DIR / f"{base_name}_zh.srt",
        SUBTITLE_DIR / f"{base_name}_zh_retimed_v4.srt",
    ]
    for path in cleanup_paths:
        path.unlink(missing_ok=True)


def rewrite_retimed_srt(base_name: str) -> Path:
    plan_path = RETIME_PLAN_DIR / f"{base_name}.json"
    retimed_srt_path = SUBTITLE_DIR / f"{base_name}_zh_retimed_v4.srt"
    plan_payload = json.loads(plan_path.read_text(encoding="utf-8"))
    retimed_entries = add_subtitles.build_retimed_entries(plan_payload)
    add_subtitles.write_srt(retimed_entries, retimed_srt_path)
    return retimed_srt_path


def copy_final_srt(retimed_srt_path: Path) -> Path:
    final_srt_path = retimed_srt_path.with_name(f"{retimed_srt_path.stem}_final.srt")
    shutil.copy2(retimed_srt_path, final_srt_path)
    return final_srt_path


def main() -> int:
    args = parse_args()

    try:
        t0 = time.perf_counter()
        print(f"[INFO] Loading Whisper model: {WHISPER_MODEL_NAME}")
        model = whisper.load_model(WHISPER_MODEL_NAME)
        translator = enrich_subtitles.build_translator()
        tts_provider = enrich_subtitles.build_tts_provider()
        t1 = time.perf_counter()

        print("[INFO] Step 1/8: Download video")
        video_path = download.download_video(args.url)
        if video_path is None:
            print("[ERROR] No local video is available for this URL.", file=sys.stderr)
            return 1
        t2 = time.perf_counter()

        print("[INFO] Step 2/8: Prepare source video")
        processed_video_path = prepare_video.prepare_video(video_path)
        t3 = time.perf_counter()

        print("[INFO] Step 3/8: Extract audio")
        audio_path = extract_audio.extract_audio(processed_video_path)
        t4 = time.perf_counter()

        print("[INFO] Step 4/8: Transcribe")
        subtitle_path = transcribe.transcribe_audio(model, audio_path)
        t5 = time.perf_counter()

        if args.refresh_tts:
            print("[INFO] Refresh requested, clearing cached delivery outputs")
            cleanup_delivery_outputs(subtitle_path.stem)

        print("[INFO] Step 5/8: Enrich subtitles")
        structured_path = enrich_subtitles.enrich_subtitle_file(subtitle_path, translator, tts_provider)
        t6 = time.perf_counter()

        print("[INFO] Step 6/8: Generate Chinese dub")
        dubbed_video_path = dub_video.generate_dubbed_video(structured_path)
        t7 = time.perf_counter()

        print("[INFO] Step 7/8: Retime video")
        _, retimed_video_path = retime_video.process_file(structured_path)
        t8 = time.perf_counter()

        print("[INFO] Step 8/8: Export SRT only")
        add_subtitles.process_file(structured_path, only_srt=True)
        retimed_srt_path = rewrite_retimed_srt(structured_path.stem)
        final_srt_path = copy_final_srt(retimed_srt_path)
        t9 = time.perf_counter()

        normal_srt_path = SUBTITLE_DIR / f"{structured_path.stem}_zh.srt"

        print("[INFO] Quick delivery completed.")
        print(f"[INFO] Dubbed video: {dubbed_video_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Retimed video: {retimed_video_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Subtitle: {normal_srt_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Retimed subtitle: {retimed_srt_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] Final subtitle: {final_srt_path.relative_to(PROJECT_ROOT)}")
        print("[INFO] Stage timing (seconds):")
        print(f"[INFO]   init:       {t1 - t0:.1f}")
        print(f"[INFO]   download:   {t2 - t1:.1f}")
        print(f"[INFO]   prepare:    {t3 - t2:.1f}")
        print(f"[INFO]   extract:    {t4 - t3:.1f}")
        print(f"[INFO]   transcribe: {t5 - t4:.1f}")
        print(f"[INFO]   enrich:     {t6 - t5:.1f}")
        print(f"[INFO]   tts+dub:    {t7 - t6:.1f}")
        print(f"[INFO]   retime:     {t8 - t7:.1f}")
        print(f"[INFO]   subtitles:  {t9 - t8:.1f}")
        print(f"[INFO]   total:      {t9 - t0:.1f}")
        return 0
    except Exception as exc:
        print(f"[ERROR] Quick delivery failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
