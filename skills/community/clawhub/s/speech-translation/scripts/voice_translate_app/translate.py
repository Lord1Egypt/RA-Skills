from pathlib import Path
import sys

import requests

from .types import TranslationResult


TRANSLATION_GUIDE = """请把下面文本翻译成目标语言，然后粘贴回终端，最后按 Ctrl-D（macOS/Linux）或 Ctrl-Z 回车（Windows）结束输入。"""



def _load_translation_from_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()



def _prompt_for_translation(text: str, source_lang: str, target_lang: str) -> str:
    print("\n=== Translation Required ===")
    print(TRANSLATION_GUIDE)
    print(f"Source language: {source_lang}")
    print(f"Target language: {target_lang}")
    print("\n--- Source Text Begin ---")
    print(text)
    print("--- Source Text End ---\n")
    print("请输入译文，然后结束输入：")
    translated = sys.stdin.read().strip()

    if not translated:
        raise ValueError("No translation provided.")
    return translated



def _translate_via_service(text: str, source_lang: str, target_lang: str, service_url: str) -> str:
    response = requests.post(
        service_url,
        json={
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    translated = str(data.get("translation", "")).strip()
    if not translated:
        raise ValueError("Translation service returned empty translation.")
    return translated



def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    backend: str = "llm",
    translation_file: Path | None = None,
    interactive: bool = True,
    translation_service_url: str | None = None,
) -> TranslationResult:
    normalized_text = text.strip()

    if source_lang == target_lang:
        translated = normalized_text
    elif translation_file is not None:
        translated = _load_translation_from_file(translation_file)
    elif backend == "service":
        if not translation_service_url:
            raise ValueError("translation_service_url is required when backend=service")
        translated = _translate_via_service(
            normalized_text,
            source_lang,
            target_lang,
            translation_service_url,
        )
    elif backend == "llm":
        raise ValueError(
            "translation_backend=llm requires a pre-generated --translation-file. "
            "When this skill is used inside an agent, let the agent translate the transcript with its current model, "
            "save the result to a file, then rerun or continue the pipeline with --translation-file."
        )
    elif interactive:
        translated = _prompt_for_translation(normalized_text, source_lang, target_lang)
    else:
        raise ValueError(
            "Translation is required, but neither translation_file, llm-produced file, service backend, nor interactive mode is available."
        )

    return TranslationResult(
        text=translated,
        source_language=source_lang,
        target_language=target_lang,
    )
