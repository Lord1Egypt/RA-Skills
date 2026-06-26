import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
AUDIO_DIR = PROJECT_ROOT / "data" / "audio"


def ensure_directories() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def extract_audio(video_path: Path) -> Path:
    ensure_directories()

    output_path = AUDIO_DIR / f"{video_path.stem}.wav"
    if output_path.exists():
        print(f"[INFO] Skip existing audio: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_path),
    ]

    print(f"[INFO] Extracting audio from: {video_path.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed without stderr output")

    print(f"[INFO] Audio saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def main() -> int:
    try:
        ensure_directories()
        videos = sorted(PROCESSED_DIR.glob("*.mp4"))
        if not videos:
            videos = sorted(RAW_DIR.glob("*.mp4"))
        if not videos:
            print("[WARN] No MP4 files found in data/raw. Nothing to process.")
            return 0

        for video_path in videos:
            extract_audio(video_path)
    except FileNotFoundError as exc:
        print(f"[ERROR] Missing file or directory: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[ERROR] Failed to extract audio: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
