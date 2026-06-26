import json
import sys
from pathlib import Path
from typing import Any

import whisper


PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = PROJECT_ROOT / "data" / "audio"
SUBS_DIR = PROJECT_ROOT / "data" / "subs"
WHISPER_MODEL_NAME = "small"


def ensure_directories() -> None:
    SUBS_DIR.mkdir(parents=True, exist_ok=True)


def build_output(result: dict[str, Any]) -> dict[str, Any]:
    segments = []
    for segment in result.get("segments", []):
        segments.append(
            {
                "start": round(float(segment["start"]), 3),
                "end": round(float(segment["end"]), 3),
                "text": segment["text"].strip(),
            }
        )

    return {
        "text": result.get("text", "").strip(),
        "segments": segments,
    }


def transcribe_audio(model: whisper.Whisper, audio_path: Path) -> Path:
    output_path = SUBS_DIR / f"{audio_path.stem}.json"
    if output_path.exists():
        print(f"[INFO] Skip existing subtitle: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

    print(f"[INFO] Transcribing audio: {audio_path.relative_to(PROJECT_ROOT)}")
    result = model.transcribe(
        str(audio_path),
        language="en",
        verbose=False,
    )
    payload = build_output(result)

    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    print(f"[INFO] Subtitle JSON saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def main() -> int:
    try:
        ensure_directories()
        audio_files = sorted(AUDIO_DIR.glob("*.wav"))
        if not audio_files:
            print("[WARN] No WAV files found in data/audio. Nothing to process.")
            return 0

        print(f"[INFO] Loading Whisper model: {WHISPER_MODEL_NAME}")
        model = whisper.load_model(WHISPER_MODEL_NAME)

        for audio_path in audio_files:
            transcribe_audio(model, audio_path)
    except Exception as exc:
        print(f"[ERROR] Failed to transcribe audio: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
