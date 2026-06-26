import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI

import add_subtitles
import download
import extract_audio
import whisper


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REVERSE_DIR = PROJECT_ROOT / "data" / "reverse"
TRANSCRIPT_DIR = REVERSE_DIR / "transcripts"
TRANSLATION_DIR = REVERSE_DIR / "translations"
SUBTITLE_DIR = PROJECT_ROOT / "data" / "subtitles"
WHISPER_MODEL_NAME = "small"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
CHUNK_SIZE = 12


def ensure_directories() -> None:
    REVERSE_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    TRANSLATION_DIR.mkdir(parents=True, exist_ok=True)
    SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)


def build_transcript(result: dict[str, Any]) -> dict[str, Any]:
    segments: list[dict[str, Any]] = []
    for segment in result.get("segments", []):
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        segments.append(
            {
                "start": round(float(segment["start"]), 3),
                "end": round(float(segment["end"]), 3),
                "text": text,
            }
        )
    return {"text": str(result.get("text", "")).strip(), "segments": segments}


def save_json(path: Path, payload: Any) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] Saved JSON: {path.relative_to(PROJECT_ROOT)}")
    return path


def chunked(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


class ChineseToEnglishTranslator:
    def __init__(self) -> None:
        api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    def translate_sentences(self, sentences: list[str]) -> list[str]:
        if not sentences:
            return []

        translated: list[str] = []
        for chunk in chunked(sentences, CHUNK_SIZE):
            try:
                translated.extend(self._translate_chunk(chunk))
            except Exception as exc:
                print(f"[WARN] Chunk translation failed, retrying sentence by sentence: {exc}")
                for sentence in chunk:
                    translated.extend(self._translate_chunk([sentence]))
        return translated

    def _translate_chunk(self, sentences: list[str]) -> list[str]:
        payload = json.dumps(
            [{"index": index, "zh": sentence} for index, sentence in enumerate(sentences)],
            ensure_ascii=False,
        )

        response = self.client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional subtitle translator. "
                        "Translate each Simplified Chinese sentence into faithful natural English. "
                        "Keep proper nouns, numbers, and meaning accurate. "
                        "Write concise subtitle-style English. "
                        "Return only valid JSON in the form "
                        '[{"index":0,"en":"..."},{"index":1,"en":"..."}].'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Translate the following Chinese subtitle sentences into English. "
                        "Preserve order and meaning. Do not add explanations.\n"
                        f"{payload}"
                    ),
                },
            ],
            stream=False,
        )

        content = _strip_code_fences(response.choices[0].message.content or "")
        parsed = json.loads(content)
        if not isinstance(parsed, list):
            raise ValueError("Translation response must be a JSON list.")

        translations_by_index: dict[int, str] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            index = item.get("index")
            en = item.get("en")
            if isinstance(index, int) and isinstance(en, str):
                translations_by_index[index] = en.strip()

        missing = [str(index) for index in range(len(sentences)) if index not in translations_by_index]
        if missing:
            raise ValueError(f"Missing translations for sentence indexes: {', '.join(missing)}")

        return [translations_by_index[index] for index in range(len(sentences))]


def _strip_code_fences(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped[3:]
        if stripped.startswith("json"):
            stripped = stripped[4:]
        stripped = stripped.lstrip("\n")
    if stripped.endswith("```"):
        stripped = stripped[:-3]
    return stripped.strip()


def write_srt(entries: list[dict[str, Any]], output_path: Path) -> Path:
    lines: list[str] = []
    for index, entry in enumerate(entries, start=1):
        start = float(entry["start"])
        end = float(entry["end"])
        text = str(entry["text"]).strip()
        lines.extend(
            [
                str(index),
                f"{add_subtitles.format_srt_timestamp(start)} --> {add_subtitles.format_srt_timestamp(end)}",
                text,
                "",
            ]
        )
    output_path.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[INFO] Subtitle file saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def transcribe_chinese(audio_path: Path, model: whisper.Whisper, language: str = "zh") -> dict[str, Any]:
    print(f"[INFO] Transcribing audio as {language}: {audio_path.relative_to(PROJECT_ROOT)}")
    result = model.transcribe(str(audio_path), language=language, verbose=False)
    return build_transcript(result)


def translate_transcript(transcript: dict[str, Any], translator: ChineseToEnglishTranslator) -> list[dict[str, Any]]:
    segments = transcript.get("segments", [])
    if not isinstance(segments, list):
        raise ValueError("Transcript segments must be a list.")

    chinese_sentences = [str(item.get("text", "")).strip() for item in segments if str(item.get("text", "")).strip()]
    english_sentences = translator.translate_sentences(chinese_sentences)
    if len(english_sentences) != len(chinese_sentences):
        raise ValueError("Translation count mismatch.")

    output: list[dict[str, Any]] = []
    index = 0
    for item in segments:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        output.append(
            {
                "start": item["start"],
                "end": item["end"],
                "zh": text,
                "en": english_sentences[index],
            }
        )
        index += 1
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Translate a Chinese Bilibili video into English subtitles.")
    parser.add_argument("url", help="Bilibili video URL")
    parser.add_argument(
        "--language",
        default="zh",
        help="Whisper language hint for transcription (default: zh).",
    )
    parser.add_argument(
        "--whisper-model",
        default=WHISPER_MODEL_NAME,
        help=f"Whisper model name (default: {WHISPER_MODEL_NAME}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ensure_directories()

        print("[INFO] Checking video metadata and downloading source video")
        video_path = download.download_video(args.url)
        if video_path is None:
            print("[ERROR] Failed to download source video.", file=sys.stderr)
            return 1

        print("[INFO] Extracting audio")
        audio_path = extract_audio.extract_audio(video_path)

        print(f"[INFO] Loading Whisper model: {args.whisper_model}")
        model = whisper.load_model(args.whisper_model)
        transcript = transcribe_chinese(audio_path, model, language=args.language)

        transcript_path = TRANSCRIPT_DIR / f"{video_path.stem}_zh.json"
        save_json(transcript_path, transcript)

        print("[INFO] Translating transcript to English")
        translator = ChineseToEnglishTranslator()
        translated_items = translate_transcript(transcript, translator)

        translation_path = TRANSLATION_DIR / f"{video_path.stem}_en.json"
        save_json(translation_path, translated_items)

        srt_entries = [
            {"start": item["start"], "end": item["end"], "text": item["en"]}
            for item in translated_items
        ]
        srt_path = SUBTITLE_DIR / f"{video_path.stem}_en.srt"
        write_srt(srt_entries, srt_path)

        print("[INFO] Reverse translation completed.")
        print(f"[INFO] Transcript JSON: {transcript_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] English JSON: {translation_path.relative_to(PROJECT_ROOT)}")
        print(f"[INFO] English SRT: {srt_path.relative_to(PROJECT_ROOT)}")
        return 0
    except Exception as exc:
        print(f"[ERROR] Reverse translation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
