import argparse
import difflib
import json
import re
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from services.deepseek_translator import DeepSeekTranslator
from services.translation_base import Translator
from services.tts_base import TTSProvider
from services.tts_factory import build_tts_provider as build_configured_tts_provider


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUBS_DIR = PROJECT_ROOT / "data" / "subs"
STRUCTURED_DIR = PROJECT_ROOT / "data" / "structured"
TTS_DIR = PROJECT_ROOT / "data" / "tts"
VIDEO_META_DIR = PROJECT_ROOT / "data" / "state" / "video_meta"
DEBUG_DIR = PROJECT_ROOT / "data" / "state" / "debug"
PROPER_NOUNS_PATH = PROJECT_ROOT / "data" / "proper_nouns.json"
MIN_SEGMENT_DURATION = 1.6
TARGET_SEGMENT_DURATION = 4.5
MAX_SEGMENT_DURATION = 12.0
MAX_SEGMENT_DURATION_NO_PUNCT = 20.0
MIN_SENTENCE_DURATION = 0.2
EN_SHORT_SEGMENT_DURATION = 1.1
EN_SHORT_SEGMENT_CHARS = 24
EN_REBALANCE_MIN_DURATION = 1.2
EN_REBALANCE_MIN_CHARS = 45
EN_MAX_COMBINED_CHARS = 150
EN_TRANSLATION_MIN_CHARS = 100
EN_TRANSLATION_MAX_CHARS = 160
EN_NATURAL_GAP_SECONDS = 0.5
EN_UNIT_MAX_CHARS = 90
EN_UNIT_MAX_DURATION = 8.0
EN_RESTORE_MIN_CHARS = 220
EN_RESTORE_MIN_DURATION = 18.0
EN_RESTORE_MAX_PUNCTUATION = 1
STRONG_PUNCTUATION = (".", "!", "?", ":", ";")
WEAK_PUNCTUATION = (",",)
ZH_STRONG_PUNCTUATION = ("。", "！", "？", "；")
ZH_WEAK_PUNCTUATION = ("，", "：", "、")
ZH_ALL_PUNCTUATION = ZH_STRONG_PUNCTUATION + ZH_WEAK_PUNCTUATION
MAX_ZH_SEGMENT_CHARS = 70
FINALIZE_MAX_SEGMENT_DURATION = 30.0
FINALIZE_MAX_SEGMENT_CHARS = 120
CLAUSE_STARTERS = (
    "however",
    "instead",
    "therefore",
    "thus",
    "so",
    "but",
    "because",
    "if",
    "when",
    "while",
    "whereas",
    "although",
    "though",
    "since",
    "after",
    "before",
    "meanwhile",
    "moreover",
    "furthermore",
    "nevertheless",
    "otherwise",
    "for example",
    "for instance",
)
BAD_ENDINGS = (
    "a",
    "an",
    "the",
    "to",
    "of",
    "in",
    "on",
    "at",
    "for",
    "with",
    "from",
    "by",
    "and",
    "or",
    "but",
    "so",
    "if",
    "when",
    "while",
    "because",
    "that",
    "which",
    "who",
    "whom",
    "whose",
    "this",
    "these",
    "those",
    "it",
    "they",
    "we",
    "you",
    "i",
    "he",
    "she",
    "there",
    "here",
    "as",
    "than",
    "into",
    "onto",
    "about",
    "over",
    "under",
    "through",
    "before",
    "after",
    "during",
    "within",
    "without",
    "between",
    "among",
    "per",
    "up",
    "down",
    "out",
    "off",
    "can",
    "could",
    "should",
    "would",
    "will",
    "shall",
    "may",
    "might",
    "must",
    "do",
    "does",
    "did",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "not",
)
BAD_STARTINGS = (
    "and",
    "or",
    "but",
    "so",
    "because",
    "if",
    "when",
    "while",
    "though",
    "although",
    "since",
    "to",
    "of",
    "in",
    "on",
    "at",
    "for",
    "with",
    "from",
    "by",
    "into",
    "onto",
    "about",
    "over",
    "under",
    "through",
    "before",
    "after",
    "during",
    "within",
    "without",
    "between",
    "among",
    "as",
    "than",
    "can",
    "could",
    "should",
    "would",
    "will",
    "shall",
    "may",
    "might",
    "must",
    "do",
    "does",
    "did",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "it",
    "they",
    "we",
    "you",
    "he",
    "she",
    "there",
    "here",
    "this",
    "these",
    "those",
)
BAD_ENDING_PATTERN = re.compile(r"\b(" + "|".join(re.escape(item) for item in BAD_ENDINGS) + r")$", re.IGNORECASE)
BAD_STARTING_PATTERN = re.compile(r"^(" + "|".join(re.escape(item) for item in BAD_STARTINGS) + r")\b", re.IGNORECASE)
CLAUSE_STARTER_PATTERN = re.compile(r"^(" + "|".join(re.escape(item) for item in CLAUSE_STARTERS) + r")\b", re.IGNORECASE)


def ensure_directories() -> None:
    STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)


def ensure_proper_nouns_file() -> None:
    if PROPER_NOUNS_PATH.exists():
        return
    default_payload = {
        "terms": [
            {
                "canonical": "Kryvyi Rih",
                "aliases": ["Krivorya Rock", "Krivoi Rog", "Krivoy Rog"],
                "min_similarity": 0.72,
            },
            {
                "canonical": "Zaporizhzhia",
                "aliases": ["Zaparoshya", "Zaporozhye", "Zaporozhye"],
                "min_similarity": 0.74,
            },
            {
                "canonical": "Kupiansk",
                "aliases": ["Kupyansk", "Kubiansk"],
                "min_similarity": 0.8,
            },
        ]
    }
    PROPER_NOUNS_PATH.write_text(json.dumps(default_payload, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_term_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


@lru_cache(maxsize=1)
def load_proper_noun_terms() -> list[dict[str, Any]]:
    ensure_proper_nouns_file()
    payload = json.loads(PROPER_NOUNS_PATH.read_text(encoding="utf-8"))
    raw_terms = payload.get("terms", []) if isinstance(payload, dict) else []
    normalized_terms: list[dict[str, Any]] = []

    for entry in raw_terms:
        if isinstance(entry, str):
            canonical = normalize_text(entry)
            aliases = [canonical]
            min_similarity = 0.84
        elif isinstance(entry, dict):
            canonical = normalize_text(str(entry.get("canonical", "")))
            aliases = [normalize_text(str(alias)) for alias in entry.get("aliases", []) if str(alias).strip()]
            aliases.append(canonical)
            min_similarity = float(entry.get("min_similarity", 0.84) or 0.84)
        else:
            continue

        if not canonical:
            continue

        normalized_terms.append(
            {
                "canonical": canonical,
                "canonical_tokens": len(canonical.split()),
                "variant_token_counts": sorted(
                    {len(variant.split()) for variant in {normalize_term_key(alias) for alias in aliases if normalize_term_key(alias)}}
                ),
                "normalized_variants": sorted(
                    {normalize_term_key(alias) for alias in aliases if normalize_term_key(alias)},
                    key=len,
                    reverse=True,
                ),
                "min_similarity": min_similarity,
            }
        )

    return normalized_terms


def restore_phrase_case(original: str, canonical: str) -> str:
    if original.isupper():
        return canonical.upper()
    if original.istitle():
        return canonical
    if original.islower():
        return canonical.lower()
    return canonical


def find_best_proper_noun_match(phrase: str) -> dict[str, Any] | None:
    normalized_phrase = normalize_term_key(phrase)
    if not normalized_phrase:
        return None

    best_match: dict[str, Any] | None = None
    best_score = 0.0
    token_count = len(normalized_phrase.split())

    for term in load_proper_noun_terms():
        if token_count not in term["variant_token_counts"]:
            continue
        for variant in term["normalized_variants"]:
            score = difflib.SequenceMatcher(None, normalized_phrase, variant).ratio()
            if score >= term["min_similarity"] and score > best_score:
                best_score = score
                best_match = {
                    "canonical": restore_phrase_case(phrase, term["canonical"]),
                    "score": score,
                }

    return best_match


def correct_proper_nouns(text: str) -> str:
    words = list(re.finditer(r"[A-Za-z][A-Za-z0-9'-]*", text))
    if not words:
        return text

    replacements: list[tuple[int, int, str]] = []
    index = 0
    max_term_tokens = max((term["canonical_tokens"] for term in load_proper_noun_terms()), default=1)

    while index < len(words):
        best_replacement: tuple[int, int, str] | None = None
        best_score = 0.0
        max_window = min(max_term_tokens + 1, len(words) - index)

        for window in range(max_window, 0, -1):
            start_match = words[index]
            end_match = words[index + window - 1]
            candidate = text[start_match.start() : end_match.end()]
            match = find_best_proper_noun_match(candidate)
            if match and match["score"] > best_score and normalize_term_key(candidate) != normalize_term_key(match["canonical"]):
                best_score = match["score"]
                best_replacement = (start_match.start(), end_match.end(), match["canonical"])

        if best_replacement is None:
            index += 1
            continue

        replacements.append(best_replacement)
        replaced_end = best_replacement[1]
        while index < len(words) and words[index].end() <= replaced_end:
            index += 1

    if not replacements:
        return text

    result_parts: list[str] = []
    cursor = 0
    for start, end, replacement in replacements:
        result_parts.append(text[cursor:start])
        result_parts.append(replacement)
        cursor = end
    result_parts.append(text[cursor:])
    return "".join(result_parts)


def punctuation_count(text: str) -> int:
    return sum(1 for char in text if char in ".!?;,:")


def should_restore_english_item(item: dict[str, Any]) -> bool:
    text = normalize_text(str(item["en"]))
    duration = float(item["end"]) - float(item["start"])
    return (
        len(text) >= EN_RESTORE_MIN_CHARS
        or duration >= EN_RESTORE_MIN_DURATION
    ) and punctuation_count(text) <= EN_RESTORE_MAX_PUNCTUATION


def split_item_by_english_parts(item: dict[str, Any], parts: list[str]) -> list[dict[str, Any]]:
    cleaned_parts = [normalize_text(part) for part in parts if normalize_text(part)]
    if len(cleaned_parts) <= 1:
        return [item]

    start = float(item["start"])
    end = float(item["end"])
    duration = max(0.0, end - start)
    total_chars = sum(len(part) for part in cleaned_parts)
    if total_chars <= 0 or duration <= 0:
        return [item]

    result: list[dict[str, Any]] = []
    cursor = start
    remaining_duration = duration
    remaining_chars = total_chars

    for index, part in enumerate(cleaned_parts):
        if index == len(cleaned_parts) - 1:
            part_start = cursor
            part_end = end
        else:
            ratio = len(part) / max(1, remaining_chars)
            allocation = max(MIN_SENTENCE_DURATION, remaining_duration * ratio)
            part_start = cursor
            part_end = min(end, part_start + allocation)

        result.append(
            {
                "start": round(part_start, 3),
                "end": round(part_end, 3),
                "en": part,
            }
        )
        cursor = part_end
        remaining_duration = max(0.0, end - cursor)
        remaining_chars = max(0, remaining_chars - len(part))

    return result


def should_preserve_split_boundary(item: dict[str, Any]) -> bool:
    return bool(item.get("no_merge"))


def mark_split_boundary(item: dict[str, Any]) -> dict[str, Any]:
    marked = item.copy()
    marked["no_merge"] = True
    return marked


def split_intro_opening_item(sentence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not sentence_items:
        return sentence_items

    first_item = sentence_items[0]
    raw_text = normalize_text(str(first_item.get("en", "")))
    if not raw_text:
        return sentence_items

    normalized_intro = normalize_intro_english(raw_text)
    matched_pattern = next((pattern for pattern in INTRO_OVERRIDE_END_PATTERNS if pattern in normalized_intro), None)
    if matched_pattern is None:
        return sentence_items

    prefix_end_index = normalized_intro.index(matched_pattern) + len(matched_pattern)
    prefix_word_count = len(normalized_intro[:prefix_end_index].split())
    raw_words = raw_text.split()
    if prefix_word_count <= 0 or prefix_word_count >= len(raw_words):
        return sentence_items

    prefix_text = normalize_text(" ".join(raw_words[:prefix_word_count]))
    suffix_text = normalize_text(" ".join(raw_words[prefix_word_count:]))
    if not prefix_text or not suffix_text:
        return sentence_items

    split_parts = split_item_by_english_parts(first_item, [prefix_text, suffix_text])
    if len(split_parts) != 2:
        return sentence_items

    split_parts = [mark_split_boundary(part) for part in split_parts]
    return [*split_parts, *sentence_items[1:]]


def restore_english_sentence_items(sentence_items: list[dict[str, Any]], translator: Translator) -> list[dict[str, Any]]:
    restore_indexes = [index for index, item in enumerate(sentence_items) if should_restore_english_item(item)]
    if not restore_indexes:
        return sentence_items

    restore_inputs = [normalize_text(str(sentence_items[index]["en"])) for index in restore_indexes]
    restored_groups = translator.restore_english_sentences(restore_inputs)
    if len(restored_groups) != len(restore_indexes):
        print("[WARN] English restoration count mismatch, skipping restored output.")
        return sentence_items

    restored_map = {index: restored_groups[position] for position, index in enumerate(restore_indexes)}
    restored_items: list[dict[str, Any]] = []
    for index, item in enumerate(sentence_items):
        restored_sentences = restored_map.get(index)
        if not restored_sentences:
            restored_items.append(item)
            continue

        split_items = split_item_by_english_parts(item, restored_sentences)
        for split_item in split_items:
            restored_items.extend(
                split_segment_by_punctuation(
                    float(split_item["start"]),
                    float(split_item["end"]),
                    str(split_item["en"]),
                )
            )

    return restored_items


def split_segments_into_sentences(segments: list[dict[str, Any]], translator: Translator) -> list[dict[str, Any]]:
    sentence_items: list[dict[str, Any]] = []

    for segment in segments:
        start = float(segment["start"])
        end = float(segment["end"])
        text = clean_asr_text(str(segment["text"]))
        if not text:
            continue

        sentence_items.extend(split_segment_by_punctuation(start, end, text))

    sentence_items = restore_english_sentence_items(sentence_items, translator)
    sentence_items = split_intro_opening_item(sentence_items)
    sentence_items = build_translation_sentence_items(sentence_items)
    sentence_items = restore_english_sentence_items(sentence_items, translator)
    sentence_items = build_translation_sentence_items(sentence_items)
    return rebalance_sentence_items(sentence_items)


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def tokenize_text(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+|[^\w\s]", text)


def clean_asr_text(text: str) -> str:
    normalized = normalize_text(text)
    if not normalized:
        return normalized

    cleaned = collapse_exact_repetitions(normalized)
    cleaned = collapse_repeated_windows(cleaned)
    cleaned = correct_proper_nouns(cleaned)
    return normalize_text(cleaned)


def collapse_exact_repetitions(text: str) -> str:
    words = text.split()
    if len(words) < 8:
        return text

    current = words
    changed = True
    while changed and len(current) >= 8:
        changed = False
        for repeat_count in range(4, 1, -1):
            if len(current) % repeat_count != 0:
                continue
            chunk_size = len(current) // repeat_count
            if chunk_size < 4:
                continue
            first_chunk = current[:chunk_size]
            if all(current[i * chunk_size : (i + 1) * chunk_size] == first_chunk for i in range(repeat_count)):
                current = first_chunk
                changed = True
                break

    return " ".join(current)


def collapse_repeated_windows(text: str) -> str:
    words = text.split()
    if len(words) < 12:
        return text

    for window_size in range(min(18, len(words) // 2), 5, -1):
        index = 0
        collapsed: list[str] = []
        changed = False
        while index < len(words):
            window = words[index : index + window_size]
            next_window = words[index + window_size : index + (2 * window_size)]
            if len(window) == window_size and window == next_window:
                collapsed.extend(window)
                index += 2 * window_size
                changed = True
                while words[index : index + window_size] == window:
                    index += window_size
            else:
                collapsed.append(words[index])
                index += 1

        words = collapsed
        if changed:
            break

    return " ".join(words)


def split_segment_by_punctuation(start: float, end: float, text: str) -> list[dict[str, Any]]:
    duration = max(0.0, end - start)
    normalized = normalize_text(text)
    if not normalized:
        return []

    if duration <= EN_UNIT_MAX_DURATION and len(normalized) <= EN_UNIT_MAX_CHARS:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    candidates = collect_punctuation_candidates(normalized)
    if not candidates:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    best_index = select_best_punctuation_index(normalized, candidates)
    if best_index < 0:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    left_text, right_text = cut_text_at_index(normalized, best_index)
    if not left_text or not right_text:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    total_chars = len(left_text) + len(right_text)
    if total_chars <= 0:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    left_duration = max(MIN_SENTENCE_DURATION, duration * (len(left_text) / total_chars))
    left_end = min(end, start + left_duration)
    if left_end - start < MIN_SENTENCE_DURATION or end - left_end < MIN_SENTENCE_DURATION:
        return [
            {
                "start": round(start, 3),
                "end": round(end, 3),
                "en": normalized,
            }
        ]

    return split_segment_by_punctuation(start, left_end, left_text) + split_segment_by_punctuation(left_end, end, right_text)


def collect_punctuation_candidates(text: str) -> list[tuple[int, str]]:
    candidates: list[tuple[int, str]] = []
    for match in re.finditer(r"[.!?;,:]", text):
        candidates.append((match.start(), match.group()))

    return candidates


def cut_text_at_index(text: str, index: int) -> tuple[str, str]:
    left_text = text[: index + 1].strip()
    right_text = text[index + 1 :].strip()
    return left_text, right_text


def split_text_score(text: str, index: int, marker: str) -> float:
    left_text, right_text = cut_text_at_index(text, index)
    if not left_text or not right_text:
        return float("-inf")

    score = 0.0
    distance_from_middle = abs(len(left_text) - len(text) / 2)
    score -= distance_from_middle * 0.12

    if marker in STRONG_PUNCTUATION:
        score += 120.0
    elif marker in WEAK_PUNCTUATION:
        score += 85.0

    left_lower = left_text.lower()
    right_lower = right_text.lower()

    if ends_with_any_strong_punctuation(left_text):
        score += 35.0
    elif ends_with_any_weak_punctuation(left_text):
        score += 18.0

    if CLAUSE_STARTER_PATTERN.match(right_lower):
        score += 30.0

    if left_lower.endswith(("and", "or", "but", "so", "because", "if", "when", "while", "as", "than", "to", "of", "in", "on", "for", "with", "from", "by")):
        score -= 55.0

    if BAD_ENDING_PATTERN.search(left_lower):
        score -= 45.0

    if BAD_STARTING_PATTERN.match(right_lower):
        score -= 35.0

    left_word_count = len(tokenize_text(left_text))
    right_word_count = len(tokenize_text(right_text))
    if left_word_count < 4 or right_word_count < 4:
        score -= 20.0
    if len(left_text) < 8 or len(right_text) < 8:
        score -= 35.0

    return score


def select_best_punctuation_index(text: str, candidates: list[tuple[int, str]]) -> int:
    best_index = -1
    best_score = float("-inf")

    for index, marker in candidates:
        score = split_text_score(text, index, marker)
        if score > best_score:
            best_score = score
            best_index = index

    return best_index if best_score > 0 else -1


def merge_en_items(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {
        "start": round(float(left["start"]), 3),
        "end": round(float(right["end"]), 3),
        "en": normalize_text(f"{left['en']} {right['en']}"),
    }


def unit_ends_with_strong_punctuation(text: str) -> bool:
    return normalize_text(text).rstrip().endswith(STRONG_PUNCTUATION)


def unit_ends_with_any_punctuation(text: str) -> bool:
    return normalize_text(text).rstrip().endswith(STRONG_PUNCTUATION + WEAK_PUNCTUATION)


def current_en_length(units: list[dict[str, Any]]) -> int:
    return len(normalize_text(" ".join(str(unit["en"]) for unit in units)))


def find_translation_cut_index(units: list[dict[str, Any]]) -> int | None:
    cumulative_lengths: list[int] = []
    running_text = ""
    for unit in units:
        running_text = normalize_text(f"{running_text} {unit['en']}") if running_text else normalize_text(str(unit["en"]))
        cumulative_lengths.append(len(running_text))

    for prefer_strong in (True, False):
        for index in range(len(units) - 1, 0, -1):
            boundary_text = str(units[index - 1]["en"])
            length_before = cumulative_lengths[index - 1]
            if length_before < EN_TRANSLATION_MIN_CHARS or length_before > EN_TRANSLATION_MAX_CHARS:
                continue
            if prefer_strong and unit_ends_with_strong_punctuation(boundary_text):
                return index
            if (not prefer_strong) and unit_ends_with_any_punctuation(boundary_text):
                return index

    for prefer_strong in (True, False):
        for index in range(len(units) - 1, 0, -1):
            boundary_text = str(units[index - 1]["en"])
            if prefer_strong and unit_ends_with_strong_punctuation(boundary_text):
                return index
            if (not prefer_strong) and unit_ends_with_any_punctuation(boundary_text):
                return index

    return None


def build_translation_sentence_items(sentence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not sentence_items:
        return sentence_items

    blocks: list[dict[str, Any]] = []
    current_units: list[dict[str, Any]] = []

    def flush_units(units: list[dict[str, Any]]) -> None:
        if not units:
            return
        merged = units[0].copy()
        for unit in units[1:]:
            merged = merge_en_items(merged, unit)
        blocks.append(merged)

    for unit in sentence_items:
        if current_units and (should_preserve_split_boundary(current_units[-1]) or should_preserve_split_boundary(unit)):
            flush_units(current_units)
            current_units = []

        if current_units:
            gap = float(unit["start"]) - float(current_units[-1]["end"])
            if gap > EN_NATURAL_GAP_SECONDS and current_en_length(current_units) >= EN_REBALANCE_MIN_CHARS:
                flush_units(current_units)
                current_units = []

        current_units.append(unit.copy())

        while current_units and current_en_length(current_units) > EN_TRANSLATION_MAX_CHARS:
            cut_index = find_translation_cut_index(current_units)
            if cut_index is None:
                break
            left_units = current_units[:cut_index]
            current_units = current_units[cut_index:]
            flush_units(left_units)

        if current_units:
            text_length = current_en_length(current_units)
            if text_length >= EN_TRANSLATION_MIN_CHARS and unit_ends_with_strong_punctuation(current_units[-1]["en"]):
                flush_units(current_units)
                current_units = []

    if current_units:
        flush_units(current_units)

    return blocks


def ends_with_any_strong_punctuation(text: str) -> bool:
    stripped = text.rstrip()
    return stripped.endswith(STRONG_PUNCTUATION)


def ends_with_any_weak_punctuation(text: str) -> bool:
    stripped = text.rstrip()
    return stripped.endswith(WEAK_PUNCTUATION)


def should_merge_items(previous: dict[str, Any], current: dict[str, Any]) -> bool:
    if should_preserve_split_boundary(previous) or should_preserve_split_boundary(current):
        return False

    previous_text = normalize_text(str(previous.get("en", "")))
    current_text = normalize_text(str(current.get("en", "")))
    if not previous_text or not current_text:
        return False

    previous_duration = float(previous["end"]) - float(previous["start"])
    current_duration = float(current["end"]) - float(current["start"])
    combined_duration = float(current["end"]) - float(previous["start"])
    combined_text_length = len(previous_text) + len(current_text)
    if combined_duration > MAX_SEGMENT_DURATION_NO_PUNCT or combined_text_length > EN_MAX_COMBINED_CHARS:
        return False

    if ends_with_any_strong_punctuation(previous_text):
        return False

    if previous_duration < EN_SHORT_SEGMENT_DURATION or current_duration < EN_SHORT_SEGMENT_DURATION:
        return True
    if len(previous_text) < EN_SHORT_SEGMENT_CHARS or len(current_text) < EN_SHORT_SEGMENT_CHARS:
        return True

    previous_lower = previous_text.lower()
    current_lower = current_text.lower()
    if BAD_ENDING_PATTERN.search(previous_lower):
        return True
    if BAD_STARTING_PATTERN.match(current_lower):
        return True

    return False


def rebalance_sentence_items(sentence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not sentence_items:
        return sentence_items
    return rebalance_too_short_segments(sentence_items)


def rebalance_too_short_segments(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(entries) < 2:
        return entries

    balanced: list[dict[str, Any]] = []
    index = 0
    while index < len(entries):
        current = entries[index].copy()
        if should_preserve_split_boundary(current):
            balanced.append(current)
            index += 1
            continue

        current_duration = float(current["end"]) - float(current["start"])
        current_length = len(normalize_text(str(current.get("en", ""))))
        if current_duration >= EN_REBALANCE_MIN_DURATION and current_length >= EN_REBALANCE_MIN_CHARS:
            balanced.append(current)
            index += 1
            continue

        previous = balanced[-1] if balanced else None
        following = entries[index + 1] if index + 1 < len(entries) else None

        if previous is not None and can_merge_sentence_items(previous, current):
            balanced[-1] = merge_sentence_items(previous, current)
            index += 1
            continue

        if following is not None and can_merge_sentence_items(current, following):
            balanced.append(merge_sentence_items(current, following))
            index += 2
            continue

        balanced.append(current)
        index += 1

    return balanced


def can_merge_sentence_items(left: dict[str, Any], right: dict[str, Any]) -> bool:
    merged = merge_sentence_items(left, right)
    merged_duration = float(merged["end"]) - float(merged["start"])
    merged_length = len(normalize_text(str(merged.get("en", ""))))
    return merged_duration <= MAX_SEGMENT_DURATION and merged_length <= EN_MAX_COMBINED_CHARS


def merge_sentence_items(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return merge_en_items(left, right)


def build_structured_items(
    segments: list[dict[str, Any]],
    translator: Translator,
    tts_provider: TTSProvider,
    base_name: str,
) -> list[dict[str, Any]]:
    sentence_items = split_segments_into_sentences(segments, translator)
    english_sentences = [item["en"] for item in sentence_items]
    save_english_blocks_debug(sentence_items, base_name)

    print(f"[INFO] Sentence count: {len(english_sentences)}")
    translated_sentences = translator.translate_sentences(english_sentences)
    sentence_items, translated_sentences = apply_intro_override(
        sentence_items,
        translated_sentences,
        base_name,
    )

    output_items: list[dict[str, Any]] = []
    for index, item in enumerate(sentence_items):
        zh_text = translated_sentences[index]
        output_items.append(
            {
                "start": item["start"],
                "end": item["end"],
                "en": item["en"],
                "zh": zh_text,
            }
        )

    merged_items = merge_translated_items(output_items)
    final_items: list[dict[str, Any]] = []
    for index, item in enumerate(merged_items):
        tts_path = TTS_DIR / f"{base_name}_{index:04d}.mp3"
        zh_text = normalize_text(str(item["zh"]))
        final_items.append(
            {
                "start": round(float(item["start"]), 3),
                "end": round(float(item["end"]), 3),
                "zh": zh_text,
                "tts_text": build_tts_text(zh_text),
                "tts_file": tts_path.relative_to(PROJECT_ROOT).as_posix(),
                "tts_duration": 0.0,
            }
        )

    return final_items


def save_english_blocks_debug(sentence_items: list[dict[str, Any]], base_name: str) -> Path:
    debug_path = DEBUG_DIR / f"{base_name}_en_blocks.json"
    payload = [
        {
            "start": round(float(item["start"]), 3),
            "end": round(float(item["end"]), 3),
            "en": normalize_text(str(item["en"])),
        }
        for item in sentence_items
    ]
    debug_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] English block debug saved to: {debug_path.relative_to(PROJECT_ROOT)}")
    return debug_path


def build_tts_text(text: str) -> str:
    return normalize_text(str(text))


def strip_trailing_quotes(text: str) -> str:
    return str(text).strip().rstrip("\"'”’)]}】").rstrip()


def ends_with_zh_strong_punctuation(text: str) -> bool:
    return strip_trailing_quotes(text).endswith(ZH_STRONG_PUNCTUATION)


def ends_with_zh_weak_punctuation(text: str) -> bool:
    return strip_trailing_quotes(text).endswith(ZH_WEAK_PUNCTUATION)


def merge_item_pair(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {
        "start": round(float(left["start"]), 3),
        "end": round(float(right["end"]), 3),
        "en": normalize_text(f"{left['en']} {right['en']}"),
        "zh": normalize_text(f"{left['zh']}{right['zh']}"),
    }


def split_zh_text(text: str, punctuation: tuple[str, ...] = ZH_ALL_PUNCTUATION) -> list[str]:
    if not text:
        return []
    punctuation_class = re.escape("".join(punctuation))
    pattern = rf"[^{punctuation_class}]+[{punctuation_class}]?"
    parts = [part.strip() for part in re.findall(pattern, text) if part.strip()]
    return parts or [text]


def split_item_by_parts(item: dict[str, Any], zh_parts: list[str]) -> list[dict[str, Any]]:
    if len(zh_parts) <= 1:
        return [item]

    start = float(item["start"])
    end = float(item["end"])
    duration = max(end - start, 0.0)
    total_chars = sum(len(part) for part in zh_parts)
    if total_chars <= 0 or duration <= MIN_SENTENCE_DURATION * 2:
        return [item]

    result: list[dict[str, Any]] = []
    cursor = start
    remaining_duration = duration
    remaining_chars = total_chars
    for index, zh_part in enumerate(zh_parts):
        if index == len(zh_parts) - 1:
            part_start = cursor
            part_end = end
        else:
            ratio = len(zh_part) / max(1, remaining_chars)
            allocation = max(MIN_SENTENCE_DURATION, remaining_duration * ratio)
            part_start = cursor
            part_end = min(end, part_start + allocation)

        result.append(
            {
                "start": round(part_start, 3),
                "end": round(part_end, 3),
                "en": normalize_text(str(item["en"])),
                "zh": zh_part,
            }
        )
        cursor = part_end
        remaining_duration = max(0.0, end - cursor)
        remaining_chars = max(0, remaining_chars - len(zh_part))

    return result


def is_item_too_long(item: dict[str, Any]) -> bool:
    duration = float(item["end"]) - float(item["start"])
    text_length = len(normalize_text(str(item["zh"])))
    return duration > MAX_SEGMENT_DURATION_NO_PUNCT or text_length > MAX_ZH_SEGMENT_CHARS


def split_item_at_break_index(item: dict[str, Any], break_index: int) -> list[dict[str, Any]]:
    text = normalize_text(str(item["zh"]))
    if break_index <= 0 or break_index >= len(text):
        return [item]

    left_text = text[:break_index].strip()
    right_text = text[break_index:].strip()
    if not left_text or not right_text:
        return [item]

    return split_item_by_parts(item, [left_text, right_text])


def find_last_punctuation_break(text: str) -> int | None:
    normalized = normalize_text(text)
    punctuation = set("".join(ZH_ALL_PUNCTUATION))
    for index in range(len(normalized) - 1, -1, -1):
        if normalized[index] in punctuation and index + 1 < len(normalized):
            return index + 1
    return None


def split_item_once(item: dict[str, Any], punctuation: tuple[str, ...]) -> list[dict[str, Any]]:
    zh_parts = split_zh_text(normalize_text(str(item["zh"])), punctuation)
    if len(zh_parts) <= 1:
        return [item]
    return split_item_by_parts(item, zh_parts)


def split_oversized_merged_item(item: dict[str, Any]) -> list[dict[str, Any]]:
    pending = [item]
    result: list[dict[str, Any]] = []

    while pending:
        current = pending.pop(0)
        if not is_item_too_long(current):
            result.append(current)
            continue

        break_index = find_last_punctuation_break(str(current["zh"]))
        if break_index is None:
            result.append(current)
            continue

        split_parts = split_item_at_break_index(current, break_index)
        if len(split_parts) <= 1:
            result.append(current)
            continue

        pending = split_parts + pending

    return result


def should_merge_translated_items(previous: dict[str, Any], current: dict[str, Any]) -> bool:
    if should_preserve_split_boundary(previous) or should_preserve_split_boundary(current):
        return False

    previous_duration = float(previous["end"]) - float(previous["start"])
    current_duration = float(current["end"]) - float(current["start"])
    combined_duration = float(current["end"]) - float(previous["start"])
    combined_zh = normalize_text(f"{previous['zh']}{current['zh']}")
    combined_length = len(combined_zh)

    if combined_duration > MAX_SEGMENT_DURATION_NO_PUNCT or combined_length > 100:
        return False

    if previous_duration < MIN_SEGMENT_DURATION or current_duration < MIN_SEGMENT_DURATION:
        return True

    if not ends_with_zh_strong_punctuation(previous["zh"]):
        return True

    if ends_with_zh_weak_punctuation(previous["zh"]) and previous_duration < TARGET_SEGMENT_DURATION:
        return True

    if combined_length < 18 and combined_duration < TARGET_SEGMENT_DURATION:
        return True

    return False


def rebalance_short_translated_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(items) < 2:
        return items

    balanced: list[dict[str, Any]] = []
    index = 0
    while index < len(items):
        current = items[index].copy()
        current_duration = float(current["end"]) - float(current["start"])
        current_length = len(normalize_text(str(current["zh"])))

        if current_duration >= MIN_SEGMENT_DURATION and current_length >= 8:
            balanced.append(current)
            index += 1
            continue

        previous = balanced[-1] if balanced else None
        following = items[index + 1] if index + 1 < len(items) else None

        if previous is not None and should_merge_translated_items(previous, current):
            balanced[-1] = merge_item_pair(previous, current)
            index += 1
            continue

        if following is not None and should_merge_translated_items(current, following):
            balanced.append(merge_item_pair(current, following))
            index += 2
            continue

        balanced.append(current)
        index += 1

    return balanced


def can_extend_in_finalize(current: dict[str, Any], following: dict[str, Any]) -> bool:
    candidate = merge_item_pair(current, following)
    candidate_duration = float(candidate["end"]) - float(candidate["start"])
    candidate_length = len(normalize_text(str(candidate["zh"])))
    current_duration = float(current["end"]) - float(current["start"])
    current_length = len(normalize_text(str(current["zh"])))

    if candidate_duration <= FINALIZE_MAX_SEGMENT_DURATION and candidate_length <= FINALIZE_MAX_SEGMENT_CHARS:
        return True

    return current_duration < TARGET_SEGMENT_DURATION or current_length < 24


def finalize_translated_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(items) < 2:
        return items

    finalized: list[dict[str, Any]] = []
    index = 0
    while index < len(items):
        current = items[index].copy()
        while (
            index + 1 < len(items)
            and not ends_with_zh_strong_punctuation(current["zh"])
            and can_extend_in_finalize(current, items[index + 1])
        ):
            current = merge_item_pair(current, items[index + 1])
            index += 1

        finalized.append(current)
        index += 1

    result: list[dict[str, Any]] = []
    for item in finalized:
        if is_item_too_long(item):
            result.extend(split_oversized_merged_item(item))
        else:
            result.append(item)

    if len(result) < 2:
        return result

    stitched: list[dict[str, Any]] = []
    index = 0
    while index < len(result):
        current = result[index].copy()
        if (
            index + 1 < len(result)
            and not ends_with_zh_strong_punctuation(current["zh"])
            and can_extend_in_finalize(current, result[index + 1])
        ):
            current = merge_item_pair(current, result[index + 1])
            index += 1
        stitched.append(current)
        index += 1

    return stitched


def merge_translated_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not items:
        return items

    merged: list[dict[str, Any]] = []
    for item in items:
        current = {
            "start": round(float(item["start"]), 3),
            "end": round(float(item["end"]), 3),
            "en": normalize_text(str(item["en"])),
            "zh": normalize_text(str(item["zh"])),
        }
        if not merged:
            merged.append(current)
            continue

        previous = merged[-1]
        if should_preserve_split_boundary(previous) or should_preserve_split_boundary(current):
            merged.append(current)
            continue

        if should_merge_translated_items(previous, current):
            merged[-1] = merge_item_pair(previous, current)
        else:
            merged.append(current)

    rebalanced: list[dict[str, Any]] = []
    for item in merged:
        if is_item_too_long(item):
            rebalanced.extend(split_oversized_merged_item(item))
        else:
            rebalanced.append(item)

    return finalize_translated_items(rebalance_short_translated_items(rebalanced))


def enrich_subtitle_file(
    subtitle_path: Path,
    translator: Translator,
    tts_provider: TTSProvider,
) -> Path:
    ensure_directories()
    subtitle_path = subtitle_path.resolve()
    output_path = STRUCTURED_DIR / f"{subtitle_path.stem}.json"
    if output_path.exists():
        print(f"[INFO] Skip existing structured JSON: {output_path.relative_to(PROJECT_ROOT)}")
        return output_path

    print(f"[INFO] Enriching subtitle file: {subtitle_path.relative_to(PROJECT_ROOT)}")
    payload = json.loads(subtitle_path.read_text(encoding="utf-8"))
    segments = payload.get("segments", [])
    if not isinstance(segments, list):
        raise ValueError(f"Invalid subtitle JSON structure: {subtitle_path}")

    structured_items = build_structured_items(segments, translator, tts_provider, subtitle_path.stem)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(structured_items, fp, ensure_ascii=False, indent=2)

    print(f"[INFO] Structured JSON saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def build_translator() -> Translator:
    return DeepSeekTranslator()


def build_tts_provider() -> TTSProvider:
    return build_configured_tts_provider()


INTRO_OVERRIDE_END_PATTERNS = (
    "today we have a lots of very interesting updates so lets start",
    "today we have lots of very interesting updates so lets start",
    "today we have a lot of very interesting updates so lets start",
    "today we have a lot of interesting updates so lets start",
    "today we have lots of interesting updates so lets start",
    "we have a lots of very interesting updates so lets start",
    "we have lots of very interesting updates so lets start",
)
INTRO_OVERRIDE_MAX_SENTENCES = 8
INTRO_OVERRIDE_MAX_END_SECONDS = 45.0


def normalize_intro_english(text: str) -> str:
    normalized = normalize_text(text).lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return normalize_text(normalized)


def find_intro_override_end_index(sentence_items: list[dict[str, Any]]) -> int | None:
    cumulative_parts: list[str] = []
    for index, item in enumerate(sentence_items[:INTRO_OVERRIDE_MAX_SENTENCES]):
        if float(item["end"]) > INTRO_OVERRIDE_MAX_END_SECONDS:
            break

        cumulative_parts.append(str(item.get("en", "")))
        normalized_cumulative = normalize_intro_english(" ".join(cumulative_parts))
        if any(pattern in normalized_cumulative for pattern in INTRO_OVERRIDE_END_PATTERNS):
            return index

    return None


def apply_intro_override(
    sentence_items: list[dict[str, Any]],
    translated_sentences: list[str],
    base_name: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not translated_sentences or not sentence_items:
        return sentence_items, translated_sentences
    if not should_apply_intro_override(base_name):
        return sentence_items, translated_sentences

    report_date = get_production_date()
    intro = (
        "\u5927\u5bb6\u597d\uff0c\u6211\u662f\u8001\u91d1\uff0c"
        f"\u7ed9\u5927\u5bb6\u5e26\u6765{report_date.year}\u5e74"
        f"{report_date.month}\u6708{report_date.day}\u65e5"
        "\u7684\u4fc4\u4e4c\u6218\u573a\u6d88\u606f\u3002"
    )

    matched_index = find_intro_override_end_index(sentence_items)
    if matched_index is None:
        translated_sentences[0] = intro
        return sentence_items, translated_sentences

    merged_intro_item = sentence_items[0].copy()
    merged_intro_item["end"] = sentence_items[matched_index]["end"]
    merged_intro_item["en"] = normalize_text(
        " ".join(str(item.get("en", "")) for item in sentence_items[: matched_index + 1])
    )

    remaining_sentence_items = [merged_intro_item, *sentence_items[matched_index + 1 :]]
    remaining_translations = [intro, *translated_sentences[matched_index + 1 :]]
    return remaining_sentence_items, remaining_translations


def should_apply_intro_override(base_name: str) -> bool:
    meta_path = VIDEO_META_DIR / f"{base_name}.json"
    if not meta_path.exists():
        return True

    payload = json.loads(meta_path.read_text(encoding="utf-8"))
    settings = payload.get("settings", {})
    return bool(settings.get("use_intro_override", True))


def get_production_date() -> datetime:
    return datetime.now(timezone.utc).astimezone()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate English subtitles to Chinese and build sentence-level structured JSON."
    )
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Optional single subtitle JSON path. If omitted, scan data/subs/*.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        translator = build_translator()
        tts_provider = build_tts_provider()
    except Exception as exc:
        print(f"[ERROR] Failed to initialize services: {exc}", file=sys.stderr)
        return 1

    try:
        ensure_directories()
        if args.input_path:
            subtitle_files = [Path(args.input_path).resolve()]
        else:
            subtitle_files = [path.resolve() for path in sorted(SUBS_DIR.glob("*.json"))]

        if not subtitle_files:
            print("[WARN] No subtitle JSON files found. Nothing to process.")
            return 0

        for subtitle_path in subtitle_files:
            try:
                enrich_subtitle_file(subtitle_path, translator, tts_provider)
            except Exception as exc:
                print(f"[ERROR] Failed to enrich subtitle: {subtitle_path}", file=sys.stderr)
                print(f"[ERROR] Reason: {exc}", file=sys.stderr)
    except Exception as exc:
        print(f"[ERROR] Failed to run subtitle enrichment: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
