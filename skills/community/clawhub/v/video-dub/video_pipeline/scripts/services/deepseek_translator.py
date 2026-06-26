import json
import os
import re

from openai import OpenAI

from services.translation_base import Translator


class DeepSeekTranslator(Translator):
    TRANSLATE_CHUNK_SIZE = 18
    POLISH_CHUNK_SIZE = 18
    RESTORE_CHUNK_SIZE = 6

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
    ) -> None:
        resolved_api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not resolved_api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set.")

        self.client = OpenAI(api_key=resolved_api_key, base_url=base_url)
        self.model = model

    def translate_sentences(self, sentences: list[str]) -> list[str]:
        if not sentences:
            return []

        translated: list[str] = []
        for start in range(0, len(sentences), self.TRANSLATE_CHUNK_SIZE):
            chunk = sentences[start : start + self.TRANSLATE_CHUNK_SIZE]
            try:
                draft_translations = self._translate_chunk(chunk)
                polished_translations = self._polish_chunk(chunk, draft_translations)
                translated.extend(polished_translations)
            except ValueError as exc:
                print(
                    "[WARN] Chunk translation or polishing incomplete, retrying sentence by sentence: "
                    f"{exc}"
                )
                for sentence in chunk:
                    draft = self._translate_chunk([sentence])
                    try:
                        translated.extend(self._polish_chunk([sentence], draft))
                    except ValueError as polish_exc:
                        print(
                            "[WARN] Single-sentence polish failed, falling back to draft translation: "
                            f"{polish_exc}"
                        )
                        translated.extend(draft)
        return translated

    def restore_english_sentences(self, sentences: list[str]) -> list[list[str]]:
        if not sentences:
            return []

        restored: list[list[str]] = []
        for start in range(0, len(sentences), self.RESTORE_CHUNK_SIZE):
            chunk = sentences[start : start + self.RESTORE_CHUNK_SIZE]
            try:
                restored.extend(self._restore_chunk(chunk))
            except ValueError as exc:
                print(
                    "[WARN] English restoration failed, falling back to original sentences: "
                    f"{exc}"
                )
                restored.extend([[sentence] for sentence in chunk])
        return restored

    def _translate_chunk(self, sentences: list[str]) -> list[str]:
        payload = json.dumps(
            [{"index": index, "en": sentence} for index, sentence in enumerate(sentences)],
            ensure_ascii=False,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional subtitle translator. "
                        "Translate each English sentence into faithful Simplified Chinese. "
                        "Return only valid JSON in the form "
                        '[{"index":0,"zh":"..."},{"index":1,"zh":"..."}].'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Translate the following subtitle sentences into Simplified Chinese. "
                        "Keep the same order and preserve meaning for dubbing/video editing. "
                        "Prefer concise, literal phrasing at this stage.\n"
                        f"{payload}"
                    ),
                },
            ],
            stream=False,
        )

        content = self._strip_code_fences(response.choices[0].message.content or "")
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"DeepSeek returned invalid JSON: {content}") from exc

        if not isinstance(parsed, list):
            raise ValueError("DeepSeek translation response must be a JSON list.")

        translations_by_index: dict[int, str] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            index = item.get("index")
            zh = item.get("zh")
            if isinstance(index, int) and isinstance(zh, str):
                translations_by_index[index] = zh.strip()

        missing = [str(index) for index in range(len(sentences)) if index not in translations_by_index]
        if missing:
            raise ValueError(f"Missing translations for sentence indexes: {', '.join(missing)}")

        return [translations_by_index[index] for index in range(len(sentences))]

    def _polish_chunk(self, sentences: list[str], draft_translations: list[str]) -> list[str]:
        if not sentences:
            return []

        payload = json.dumps(
            [
                {"index": index, "en": en_sentence, "draft_zh": draft_zh}
                for index, (en_sentence, draft_zh) in enumerate(zip(sentences, draft_translations, strict=True))
            ],
            ensure_ascii=False,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior Chinese subtitle editor. "
                        "Rewrite each draft translation into natural Simplified Chinese subtitle style. "
                        "Keep the meaning faithful, preserve the original order, keep each item as one subtitle line, "
                        "avoid overly literal wording, and prefer fluent broadcast-style Chinese. "
                        "Do not add explanations or extra text. "
                        "Return only valid JSON in the form "
                        '[{"index":0,"zh":"..."},{"index":1,"zh":"..."}].'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Polish the following subtitle translations using the English sentence for context. "
                        "Keep the output concise, natural, and ready for dubbing/subtitles.\n"
                        f"{payload}"
                    ),
                },
            ],
            stream=False,
        )

        content = self._strip_code_fences(response.choices[0].message.content or "")
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"DeepSeek polish returned invalid JSON: {content}") from exc

        if not isinstance(parsed, list):
            raise ValueError("DeepSeek polish response must be a JSON list.")

        translations_by_index: dict[int, str] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            index = item.get("index")
            zh = item.get("zh")
            if isinstance(index, int) and isinstance(zh, str):
                translations_by_index[index] = zh.strip()

        missing = [str(index) for index in range(len(sentences)) if index not in translations_by_index]
        if missing:
            raise ValueError(f"Missing polished translations for sentence indexes: {', '.join(missing)}")

        return [translations_by_index[index] for index in range(len(sentences))]

    def _restore_chunk(self, sentences: list[str]) -> list[list[str]]:
        payload = json.dumps(
            [{"index": index, "en": sentence} for index, sentence in enumerate(sentences)],
            ensure_ascii=False,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You restore Whisper-style English subtitle text into natural sentence boundaries. "
                        "Do not summarize, do not drop facts, do not rewrite names, and do not translate. "
                        "Only add punctuation, break run-on text into natural English sentences, and remove obvious exact repetitions. "
                        "Return only valid JSON in the form "
                        '[{"index":0,"sentences":["...","..."]},{"index":1,"sentences":["..."]}].'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Restore punctuation and sentence boundaries for the following English ASR text. "
                        "Preserve meaning and terminology, but split long run-on text into clean English sentences.\n"
                        f"{payload}"
                    ),
                },
            ],
            stream=False,
        )

        content = self._strip_code_fences(response.choices[0].message.content or "")
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"DeepSeek restore returned invalid JSON: {content}") from exc

        if not isinstance(parsed, list):
            raise ValueError("DeepSeek restore response must be a JSON list.")

        restored_by_index: dict[int, list[str]] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            index = item.get("index")
            restored_sentences = item.get("sentences")
            if not isinstance(index, int) or not isinstance(restored_sentences, list):
                continue

            cleaned_sentences = [str(sentence).strip() for sentence in restored_sentences if str(sentence).strip()]
            if cleaned_sentences:
                restored_by_index[index] = cleaned_sentences

        missing = [str(index) for index in range(len(sentences)) if index not in restored_by_index]
        if missing:
            raise ValueError(f"Missing restored sentence indexes: {', '.join(missing)}")

        return [restored_by_index[index] for index in range(len(sentences))]

    @staticmethod
    def _strip_code_fences(content: str) -> str:
        stripped = content.strip()
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
        return stripped.strip()
