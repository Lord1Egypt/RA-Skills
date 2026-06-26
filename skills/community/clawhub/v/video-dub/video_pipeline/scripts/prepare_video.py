import json
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
COVERS_DIR = PROJECT_ROOT / "data" / "covers"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
VIDEO_META_DIR = PROJECT_ROOT / "data" / "state" / "video_meta"
TEMP_DIR = PROJECT_ROOT / "data" / "state" / "temp"
INTRO_SECONDS = 10
MAX_OUTPUT_WIDTH = 1920


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)


def get_video_display_size(video_path: Path) -> tuple[int, int]:
    """Use ffmpeg to get display (DAR-adjusted) width x height of the first video stream."""
    command = [
        str(video_path),
    ]
    result = subprocess.run(
        ["ffmpeg", "-i", str(video_path)],
        capture_output=True,
        text=True,
    )
    # Parse Video: ... 1920x1080 [SAR 256:81 DAR 9:16] ...
    pattern = r"Video:[^,]*,\s*(\d+)x(\d+)\s*\[SAR\s*(\d+):(\d+)\s+DAR\s*(\d+):(\d+)\]"
    match = re.search(pattern, result.stderr)
    if not match:
        # fallback: try simpler pattern
        pattern2 = r"(\d+)x(\d+)"
        m2 = re.search(pattern2, result.stderr)
        if m2:
            return int(m2.group(1)) // 2 * 2, int(m2.group(2)) // 2 * 2
        raise RuntimeError(f"Unable to determine video display size for {video_path}")
    width = int(match.group(1))
    height = int(match.group(2))
    sar_w = int(match.group(3))
    sar_h = int(match.group(4))
    dar_w = int(match.group(5))
    dar_h = int(match.group(6))
    sar = sar_w / sar_h if sar_h != 0 else 1.0
    dar = dar_w / dar_h if dar_h != 0 else (width / height)
    display_width = int(round(width * sar))
    display_height = int(round(height * sar))
    # Clamp to even numbers
    display_width = display_width // 2 * 2
    display_height = display_height // 2 * 2
    return display_width, display_height


def find_cover_for_video(video_path: Path) -> Path | None:
    for suffix in [".jpg", ".png", ".webp"]:
        candidate = COVERS_DIR / f"{video_path.stem}{suffix}"
        if candidate.exists():
            return candidate
    return None


def prepare_cover_image(cover_path: Path, video_path: Path) -> Path:
    ensure_directories()
    target_width, _ = get_video_display_size(video_path)
    target_width = min(target_width, MAX_OUTPUT_WIDTH)
    prepared_path = TEMP_DIR / f"{video_path.stem}_cover_prepared.jpg"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(cover_path),
        "-vf",
        f"scale='min(iw,{target_width})':-2",
        "-frames:v",
        "1",
        "-q:v",
        "3",
        str(prepared_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed to prepare cover image")
    return prepared_path


def load_video_settings(video_path: Path) -> dict[str, int | bool]:
    meta_path = VIDEO_META_DIR / f"{video_path.stem}.json"
    if not meta_path.exists():
        return {
            "download_cover": False,
            "replace_intro_with_cover": False,
            "intro_seconds": INTRO_SECONDS,
        }
    payload = json.loads(meta_path.read_text(encoding="utf-8"))
    settings = payload.get("settings", {})
    return {
        "download_cover": bool(settings.get("download_cover", True)),
        "replace_intro_with_cover": bool(settings.get("replace_intro_with_cover", True)),
        "intro_seconds": int(settings.get("intro_seconds", INTRO_SECONDS) or INTRO_SECONDS),
    }


def prepare_video(video_path: Path) -> Path:
    ensure_directories()
    settings = load_video_settings(video_path)
    if not settings.get("replace_intro_with_cover", True):
        print("[INFO] Skip intro cover replacement for this channel by config.")
        return video_path

    output_path = PROCESSED_DIR / video_path.name
    if output_path.exists():
        print(f"[INFO] Skip existing processed video: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

    cover_path = find_cover_for_video(video_path)
    if cover_path is None:
        raise FileNotFoundError(f"Cover image not found for video: {video_path.name}")
    prepared_cover_path = prepare_cover_image(cover_path, video_path)

    intro_seconds = int(settings.get("intro_seconds", INTRO_SECONDS) or INTRO_SECONDS)
    print(f"[INFO] Replacing first {intro_seconds} seconds with cover: {cover_path.relative_to(PROJECT_ROOT)}")
    print(f"[INFO] Prepared cover image: {prepared_cover_path.relative_to(PROJECT_ROOT)}")

    command = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(prepared_cover_path),
        "-i",
        str(video_path),
        "-filter_complex",
        (
            # scale2ref: scale cover [0:v] to match video [1:v] dimensions
            # Keep the original intro audio and only replace the intro picture.
            f"[0:v][1:v]scale2ref=iw:ih[introv][refv];"
            f"[introv]setsar=1,trim=duration={intro_seconds},setpts=PTS-STARTPTS[scaled_introv];"
            f"[refv]setsar=1,trim=start={intro_seconds},setpts=PTS-STARTPTS[mainv];"
            f"[1:a]atrim=duration={intro_seconds},asetpts=PTS-STARTPTS[introa];"
            f"[1:a]atrim=start={intro_seconds},asetpts=PTS-STARTPTS[maina];"
            "[scaled_introv][mainv]concat=n=2:v=1:a=0[concatv];"
            f"[concatv]scale='if(gt(iw,{MAX_OUTPUT_WIDTH}),{MAX_OUTPUT_WIDTH},iw)':'if(gt(iw,{MAX_OUTPUT_WIDTH}),-2,ih)'[outv];"
            "[introa][maina]concat=n=2:v=0:a=1[outa]"
        ),
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "20",
        "-threads",
        "1",
        "-x264-params",
        "ref=1:rc-lookahead=0",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        str(output_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed to build processed video")

    print(f"[INFO] Processed video saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def main() -> int:
    ensure_directories()
    try:
        videos = sorted(RAW_DIR.glob("*.mp4"))
        if not videos:
            print("[WARN] No MP4 files found in data/raw. Nothing to process.")
            return 0
        for video_path in videos:
            prepare_video(video_path)
    except Exception as exc:
        print(f"[ERROR] Failed to prepare video: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
