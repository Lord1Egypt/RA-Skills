"""Chinese text normalization helper for TTS synthesis.

Normalizes raw Chinese subtitle translations into spoken-form Chinese.
Transforms digits to Chinese character numbers, percentages to spoken words,
and removes brackets, asterisks, and other markdown leftovers.
"""

from __future__ import annotations

import re

# Simple Chinese digit mapping
_DIGIT_MAP = {
    "0": "零",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九"
}


def _digits_to_chinese(num_str: str) -> str:
    """Convert a digit string to a natural-sounding spoken Chinese number."""
    if not num_str.isdigit():
        return num_str

    val = int(num_str)
    if val == 0:
        return "零"

    # For years or code numbers (like 2026), read them digit-by-digit if they are long
    # or look like a code. But if they represent values, natural reading is better.
    # Here we implement natural value reading for numbers up to 99999 for normal speech.
    if val >= 100000:
        return "".join(_DIGIT_MAP[d] for d in num_str)

    units = ["", "十", "百", "千", "万"]
    result = ""
    digits = [int(d) for d in num_str]
    n = len(digits)

    for i, digit in enumerate(digits):
        pos = n - 1 - i
        if digit != 0:
            # Special case for "一十" -> "十" at the beginning of 10-19
            if pos == 1 and digit == 1 and i == 0:
                result += "十"
            else:
                result += _DIGIT_MAP[str(digit)] + units[pos]
        else:
            # Avoid duplicate zeros and trailing zeros
            if result and not result.endswith("零") and pos > 0 and any(digits[i+1:]):
                result += "零"

    return result


def normalize_text(text: str, voice_id: str | None = None) -> str:
    """Normalize raw translated text to natural spoken form.

    Cleans markdown, brackets, and extra spaces for all languages.
    Performs Chinese number/percentage expansion if voice_id indicates Chinese.
    """
    if not text:
        return ""

    normalized = text

    # 1. Clean markdown elements
    # For link [text](url), we keep only 'text' instead of keeping both text and url.
    # Spoken text doesn't need to read 'http://...' urls.
    normalized = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", normalized)
    normalized = re.sub(r"\*\*|__", "", normalized)
    normalized = re.sub(r"\*|_", "", normalized)

    # 2. Strip HTML / XML / WebVTT formatting tags (e.g. <font color="...">, <v Speaker>, <b>, </i>)
    normalized = re.sub(r"<[^>]+>", " ", normalized)

    # 3. Strip ASS / SSA style tags (e.g. {\an8}, {\b1}, {\c&H00ffff&})
    normalized = re.sub(r"\{[^\}]+\}", " ", normalized)

    # 4. Remove standalone brackets/parentheses
    normalized = re.sub(r"[\(\)\[\]]", " ", normalized)

    # Detect if target language/voice is Chinese
    is_chinese = False
    if voice_id:
        v_lower = voice_id.lower()
        is_chinese = v_lower.startswith("zh") or "chinese" in v_lower

    if is_chinese:
        # Currency symbols spoken expansion for Chinese
        normalized = re.sub(r"\$(\d+)", r"\1美元", normalized)
        normalized = re.sub(r"[¥￥](\d+)", r"\1元", normalized)
        normalized = re.sub(r"€(\d+)", r"\1欧元", normalized)

        # 5. Normalize Percentages (e.g. 25% -> 百分之二十五)
        def repl_percent(match: re.Match) -> str:
            num = match.group(1)
            return f"百分之{_digits_to_chinese(num)}"
        normalized = re.sub(r"(\d+)%", repl_percent, normalized)

        # 6. Normalize integers (e.g. 100 -> 一百, 9折 -> 九折)
        def repl_digits(match: re.Match) -> str:
            num = match.group(0)
            return _digits_to_chinese(num)
        normalized = re.sub(r"\d+", repl_digits, normalized)
    else:
        # Currency symbols spoken expansion for English/international
        normalized = re.sub(r"\$(\d+)", r"\1 dollars", normalized)
        normalized = re.sub(r"€(\d+)", r"\1 euros", normalized)

    # 7. Collapse extra spaces
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def normalize_chinese_text(text: str) -> str:
    """Normalize raw translated text to natural spoken Chinese (deprecated: use normalize_text instead)."""
    return normalize_text(text, "zh")


__all__ = ["normalize_text", "normalize_chinese_text"]
