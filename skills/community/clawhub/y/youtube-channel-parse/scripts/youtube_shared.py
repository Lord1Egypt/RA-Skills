#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

DEFAULT_STOPWORDS = {
    "a",
    "an",
    "are",
    "as",
    "at",
    "be",
    "been",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "done",
    "get",
    "gets",
    "got",
    "had",
    "has",
    "the",
    "and",
    "for",
    "you",
    "our",
    "ours",
    "we",
    "us",
    "with",
    "that",
    "this",
    "from",
    "were",
    "was",
    "it's",
    "its",
    "i'm",
    "i've",
    "we're",
    "we've",
    "into",
    "your",
    "their",
    "about",
    "have",
    "will",
    "they",
    "what",
    "when",
    "where",
    "which",
    "more",
    "than",
    "just",
    "over",
    "across",
    "like",
    "them",
    "then",
    "also",
    "being",
    "because",
    "much",
    "many",
    "video",
    "videos",
    "youtube",
    "youtu",
    "channel",
    "http",
    "https",
    "www",
    "com",
    "there",
    "here",
    "how",
    "not",
    "next",
    "every",
    "single",
    "one",
    "two",
    "three",
    "very",
    "really",
    "quite",
    "yeah",
    "okay",
    "ok",
    "right",
    "well",
    "want",
    "wants",
    "wanted",
    "need",
    "needs",
    "going",
    "gone",
    "come",
    "comes",
    "coming",
    "look",
    "looks",
    "looking",
    "make",
    "makes",
    "made",
    "thing",
    "things",
    "stuff",
    "people",
    "person",
    "actually",
    "basically",
    "literally",
    "maybe",
    "perhaps",
    "still",
    "even",
    "back",
    "again",
    "already",
    "able",
    "let",
    "lets",
    "lot",
    "lots",
    "kind",
    "sort",
    "mean",
    "means",
    "said",
    "say",
    "says",
    "talk",
    "talks",
    "agent",
    "clicker",
    "little",
    "bit",
    "thank",
    "thanks",
}

LANGUAGE_STOPWORDS = {
    "en": {
        "the", "and", "for", "with", "that", "this", "from", "were", "was", "have", "will", "they",
        "what", "when", "where", "which", "more", "than", "just", "like", "them", "then", "also",
        "because", "video", "videos", "there", "here", "how", "very", "really", "right", "well",
        "want", "need", "going", "look", "make", "thing", "things", "people", "said", "say", "talk",
    },
    "ru": {
        "и", "в", "во", "на", "с", "со", "к", "ко", "по", "из", "у", "о", "об", "от", "за", "для",
        "что", "это", "как", "так", "но", "да", "нет", "или", "а", "же", "бы", "ли", "мы", "вы",
        "они", "он", "она", "оно", "я", "ты", "их", "его", "ее", "её", "тут", "там", "где", "когда",
        "если", "уже", "еще", "ещё", "тоже", "только", "очень", "просто", "вот", "ну", "давайте",
        "сейчас", "потом", "был", "была", "были", "есть", "будет", "будут", "можно", "нужно",
        "чтобы", "который", "которая", "которые", "этот", "эта", "эти", "того", "потому", "себя",
    },
    "uk": {
        "і", "й", "в", "у", "на", "з", "із", "до", "за", "для", "про", "це", "як", "так", "але",
        "або", "ми", "ви", "вони", "він", "вона", "воно", "я", "ти", "їх", "його", "її", "тут",
        "там", "де", "коли", "якщо", "вже", "ще", "також", "тільки", "дуже", "просто", "ось", "ну",
        "зараз", "потім", "був", "була", "були", "є", "буде", "будуть", "можна", "треба",
    },
    "es": {
        "de", "la", "el", "que", "y", "en", "a", "los", "las", "un", "una", "por", "para", "con",
        "como", "pero", "si", "ya", "más", "muy", "sobre", "del", "al", "lo", "se", "es", "son",
        "fue", "ser", "esta", "este", "estos", "estas", "también", "porque", "cuando", "donde",
    },
    "fr": {
        "de", "la", "le", "les", "des", "un", "une", "et", "en", "à", "au", "aux", "pour", "par",
        "avec", "comme", "mais", "ou", "où", "est", "sont", "sur", "dans", "que", "qui", "ce",
        "ces", "cette", "plus", "très", "déjà", "encore", "quand",
    },
    "de": {
        "der", "die", "das", "und", "in", "im", "den", "dem", "ein", "eine", "mit", "für", "auf",
        "wie", "aber", "auch", "ist", "sind", "war", "schon", "noch", "sehr", "wenn", "dann",
        "von", "zu", "zur", "zum", "über", "bei",
    },
    "pt": {
        "de", "da", "do", "das", "dos", "e", "em", "para", "com", "como", "mas", "ou", "que", "se",
        "por", "um", "uma", "já", "muito", "mais", "sobre", "quando", "onde", "está", "estão",
    },
    "it": {
        "di", "del", "della", "e", "in", "con", "per", "come", "ma", "o", "che", "si", "un", "una",
        "già", "molto", "più", "quando", "dove", "sono", "era", "anche", "sul", "della", "degli",
    },
}

TOKEN_PATTERN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)

FACT_HINTS = ("%", "percent", "million", "billion", "year", "years", "today", "now", "currently", "data", "result", "results")
INSIGHT_HINTS = ("because", "therefore", "however", "problem", "challenge", "opportunity", "risk", "benefit", "future", "scale", "why", "thesis", "insight", "lesson", "tradeoff", "better", "worse", "important")
OPINION_HINTS = ("think", "believe", "argue", "should", "must", "recommend", "prefer", "opinion", "view")
OUTCOME_HINTS = ("outcome", "result", "conclusion", "takeaway", "next", "future", "goal", "plan", "closing", "summary", "ultimately")
DISFLUENCY_TOKENS = {"um", "uh", "yeah", "oh", "okay", "ok", "hmm", "ah"}
PROMO_HINTS = (
    "sponsor",
    "sponsored",
    "sponsoring",
    "subscription",
    "subscribe",
    "patreon",
    "podcast",
    "welcome kit",
    "flavor sampler",
    "link in the description",
    "click the link",
    "through my link",
    "use my code",
    "promo code",
    "support the channel",
    "brand new podcast",
    "exclusive episode",
    "ad free",
    "travel packs",
    "vitamin d3",
    "ag1",
    "thank you so much to",
    "check out the patreon",
    "check out the podcast",
    "first subscription order",
    "welcome to today's sponsor",
    "sponsor of this video",
    "партнер выпуска",
    "партнёр выпуска",
    "спонсор",
    "реклама",
    "по ссылке в описании",
    "подписывайтесь",
    "подпишись на канал",
)
PROMO_TOKEN_HINTS = {
    "sponsor",
    "sponsored",
    "subscribe",
    "subscription",
    "patreon",
    "podcast",
    "welcome",
    "kit",
    "sampler",
    "promo",
    "code",
    "travel",
    "packs",
    "vitamin",
    "channel",
    "ag1",
    "link",
    "links",
    "description",
    "support",
    "exclusive",
    "episode",
    "free",
    "ad",
    "sponsor",
    "спонсор",
    "реклама",
    "подписывайтесь",
    "подпишись",
}


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_words(text: str, *, min_length: int = 2) -> list[str]:
    tokens = [token.lower() for token in TOKEN_PATTERN.findall(clean_text(text))]
    return [token for token in tokens if len(token) >= min_length]


def stopwords_for_language(language: str | None) -> set[str]:
    base = base_language_code(str(language or "").strip())
    return DEFAULT_STOPWORDS | LANGUAGE_STOPWORDS.get(base, set())


def _script_counts(text: str) -> dict[str, int]:
    counts = {
        "latin": 0,
        "cyrillic": 0,
        "arabic": 0,
        "greek": 0,
        "hebrew": 0,
        "devanagari": 0,
        "hangul": 0,
        "hiragana": 0,
        "katakana": 0,
        "han": 0,
    }
    for char in text:
        code = ord(char)
        if 0x0041 <= code <= 0x024F:
            counts["latin"] += 1
        elif 0x0400 <= code <= 0x052F:
            counts["cyrillic"] += 1
        elif 0x0590 <= code <= 0x05FF:
            counts["hebrew"] += 1
        elif 0x0600 <= code <= 0x06FF:
            counts["arabic"] += 1
        elif 0x0370 <= code <= 0x03FF:
            counts["greek"] += 1
        elif 0x0900 <= code <= 0x097F:
            counts["devanagari"] += 1
        elif 0x1100 <= code <= 0x11FF or 0xAC00 <= code <= 0xD7AF:
            counts["hangul"] += 1
        elif 0x3040 <= code <= 0x309F:
            counts["hiragana"] += 1
        elif 0x30A0 <= code <= 0x30FF:
            counts["katakana"] += 1
        elif 0x4E00 <= code <= 0x9FFF:
            counts["han"] += 1
    return counts


def detect_language_from_text(text: str) -> str:
    text = clean_text(text)
    if not text:
        return ""

    script_counts = _script_counts(text)
    if script_counts["hangul"] >= 10:
        return "ko"
    if script_counts["hiragana"] + script_counts["katakana"] >= 10:
        return "ja"
    if script_counts["han"] >= 10:
        return "zh"
    if script_counts["arabic"] >= 10:
        return "ar"
    if script_counts["hebrew"] >= 10:
        return "he"
    if script_counts["greek"] >= 10:
        return "el"
    if script_counts["devanagari"] >= 10:
        return "hi"

    tokens = tokenize_words(text, min_length=1)
    if not tokens:
        return ""

    if script_counts["cyrillic"] > script_counts["latin"]:
        scores = {
            language: sum(token in stopwords for token in tokens)
            for language, stopwords in {
                "ru": LANGUAGE_STOPWORDS["ru"],
                "uk": LANGUAGE_STOPWORDS["uk"],
            }.items()
        }
        best_language, best_score = max(scores.items(), key=lambda item: item[1])
        return best_language if best_score >= 2 else "ru"

    if script_counts["latin"] > 0:
        candidate_languages = ("en", "es", "fr", "de", "pt", "it")
        scores = {
            language: sum(token in LANGUAGE_STOPWORDS.get(language, set()) for token in tokens)
            for language in candidate_languages
        }
        best_language, best_score = max(scores.items(), key=lambda item: item[1])
        return best_language if best_score >= 2 else "en"

    return ""


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def is_probable_ad_sentence(sentence: str) -> bool:
    lowered = clean_text(sentence).lower()
    if not lowered:
        return False
    if "http://" in lowered or "https://" in lowered or "www." in lowered:
        return True
    if any(hint in lowered for hint in PROMO_HINTS):
        return True
    if "follow the link" in lowered or "click the link" in lowered:
        return True
    if "welcome kit" in lowered or "subscription order" in lowered:
        return True
    return False


def content_sentences(text: str) -> list[str]:
    return [sentence for sentence in split_sentences(text) if not is_probable_ad_sentence(sentence)]


def summary_needs_refresh(text: str | None) -> bool:
    value = clean_text(str(text or ""))
    if not value:
        return True
    if is_probable_ad_sentence(value):
        return True
    return any(is_probable_ad_sentence(sentence) for sentence in split_sentences(value))


def shorten(text: str, limit: int) -> str:
    text = clean_text(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def summary_from_record(record: dict[str, Any], limit: int = 280) -> str:
    description = clean_text(str(record.get("description") or ""))
    transcript_text = clean_text(str(record.get("transcript_text") or ""))
    title = clean_text(str(record.get("title") or record.get("video_id") or "Video"))

    description_sentences = content_sentences(description)
    if description_sentences:
        return shorten(" ".join(description_sentences[:2]), limit)

    transcript_sentences = content_sentences(transcript_text)
    if transcript_sentences:
        return shorten(" ".join(transcript_sentences[:2]), limit)

    return title


def _unique_sentences(sentences: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for sentence in sentences:
        key = sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(sentence)
    return unique


def _pick_sentences(
    sentences: list[str],
    predicate,
    *,
    limit: int = 2,
    used: set[str] | None = None,
) -> list[str]:
    picked: list[str] = []
    used = used if used is not None else set()
    for sentence in sentences:
        key = sentence.lower()
        if key in used:
            continue
        if predicate(sentence):
            picked.append(sentence)
            used.add(key)
            if len(picked) >= limit:
                break
    return picked


def language_for_record(record: dict[str, Any]) -> str:
    existing = base_language_code(str(record.get("detected_language") or "").strip())
    if existing:
        return existing
    transcript_language = detect_language_from_text(str(record.get("transcript_text") or ""))
    if transcript_language:
        return transcript_language
    preferred_languages = preferred_caption_languages(record)
    if preferred_languages:
        return preferred_languages[0]
    description_language = detect_language_from_text(
        " ".join(
            part
            for part in [
                str(record.get("title") or ""),
                str(record.get("description") or ""),
            ]
            if part
        )
    )
    if description_language:
        return description_language
    return ""


def _sentence_has_signal(sentence: str, language: str | None = None) -> bool:
    lowered = sentence.lower()
    if "[applause]" in lowered:
        return False
    raw_tokens = tokenize_words(lowered, min_length=2)
    if len(raw_tokens) < 6:
        return False
    stopwords = stopwords_for_language(language)
    meaningful_tokens = [token for token in raw_tokens if token not in stopwords]
    if len(meaningful_tokens) < 4:
        return False
    disfluencies = sum(token in DISFLUENCY_TOKENS for token in raw_tokens)
    return disfluencies <= max(1, len(raw_tokens) // 6)


def detailed_summary_from_record(record: dict[str, Any], limit: int = 900) -> str:
    description = clean_text(str(record.get("description") or ""))
    transcript_text = clean_text(str(record.get("transcript_text") or ""))
    title = clean_text(str(record.get("title") or record.get("video_id") or "Video"))
    language = language_for_record(record)

    description_sentences = _unique_sentences(content_sentences(description))
    transcript_sentences = _unique_sentences(content_sentences(transcript_text))
    source_sentences = transcript_sentences or description_sentences
    used: set[str] = set()

    main_plot = description_sentences[:2] or source_sentences[:2]
    for sentence in main_plot:
        used.add(sentence.lower())

    facts = _pick_sentences(
        source_sentences,
        lambda sentence: _sentence_has_signal(sentence, language)
        and (any(hint in sentence.lower() for hint in FACT_HINTS) or bool(re.search(r"\d", sentence))),
        used=used,
    )
    insights = _pick_sentences(
        source_sentences,
        lambda sentence: _sentence_has_signal(sentence, language)
        and any(hint in sentence.lower() for hint in INSIGHT_HINTS + OPINION_HINTS),
        used=used,
    )
    outcome = _pick_sentences(
        list(reversed(source_sentences)),
        lambda sentence: _sentence_has_signal(sentence, language)
        and (any(hint in sentence.lower() for hint in OUTCOME_HINTS) or len(sentence.split()) > 8),
        limit=1,
        used=used,
    )

    sections: list[str] = []
    if main_plot:
        sections.append(f"Main plot: {' '.join(main_plot)}")
    if facts:
        sections.append(f"Facts: {' '.join(facts)}")
    if insights:
        sections.append(f"Insights and opinions: {' '.join(insights)}")
    if outcome:
        sections.append(f"Outcome: {' '.join(outcome)}")

    if sections:
        return shorten(" ".join(sections), limit)
    return title


def _keyword_tokens(text: str) -> list[str]:
    language = detect_language_from_text(text)
    tokens = tokenize_words(text, min_length=3)
    stopwords = stopwords_for_language(language)
    return [token for token in tokens if token not in stopwords and token not in PROMO_TOKEN_HINTS]


def _raw_keyword_tokens(text: str) -> list[str]:
    cleaned = " ".join(content_sentences(text))
    return tokenize_words(cleaned, min_length=3)


def extract_top_phrases(record: dict[str, Any], limit: int = 5) -> list[str]:
    language = language_for_record(record)
    stopwords = stopwords_for_language(language)
    weighted_sections = [
        (str(record.get("title") or ""), 5),
        (str(record.get("description") or ""), 3),
        (str(record.get("transcript_text") or ""), 1),
    ]
    phrase_counts: Counter[str] = Counter()
    word_counts: Counter[str] = Counter()

    for text, weight in weighted_sections:
        raw_tokens = _raw_keyword_tokens(text)
        tokens = [token for token in raw_tokens if token not in stopwords and token not in PROMO_TOKEN_HINTS]
        for token in tokens:
            word_counts[token] += weight
        for size in (3, 2):
            for index in range(len(raw_tokens) - size + 1):
                phrase_tokens = raw_tokens[index : index + size]
                if any(token in stopwords or token in PROMO_TOKEN_HINTS for token in phrase_tokens):
                    continue
                if len(set(phrase_tokens)) < size:
                    continue
                phrase = " ".join(phrase_tokens)
                if is_probable_ad_sentence(phrase):
                    continue
                phrase_counts[phrase] += weight + size

    ranked_phrases = sorted(phrase_counts.items(), key=lambda item: (-item[1], -len(item[0].split()), item[0]))
    ranked_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    selected: list[str] = []
    for phrase, _ in ranked_phrases:
        phrase_tokens = set(phrase.split())
        if any(
            phrase_tokens <= set(existing.split()) or set(existing.split()) <= phrase_tokens
            for existing in selected
        ):
            continue
        selected.append(phrase)
        if len(selected) >= limit:
            break
    if len(selected) < limit:
        for word, _ in ranked_words:
            if any(word in existing.split() for existing in selected):
                continue
            selected.append(word)
            if len(selected) >= limit:
                break
    return selected


def parse_date_value(value: str | None) -> str | None:
    if not value:
        return None
    compact = value.strip().replace("-", "")
    if not re.fullmatch(r"\d{8}", compact):
        raise ValueError(f"Expected YYYY-MM-DD or YYYYMMDD, got: {value}")
    return compact


def parse_metadata_filters(values: list[str]) -> list[tuple[str, str]]:
    filters: list[tuple[str, str]] = []
    for item in values:
        if "=" not in item:
            raise ValueError(f"Metadata filter must use FIELD=VALUE: {item}")
        field, needle = item.split("=", 1)
        field = field.strip()
        needle = needle.strip()
        if not field or not needle:
            raise ValueError(f"Metadata filter must use FIELD=VALUE: {item}")
        filters.append((field, needle))
    return filters


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def inventory_dir(output_dir: Path) -> Path:
    return ensure_dir(output_dir / "inventory")


def filtered_dir(output_dir: Path) -> Path:
    return ensure_dir(output_dir / "filtered")


def transcripts_dir(output_dir: Path) -> Path:
    return ensure_dir(output_dir / "transcripts")


def reports_dir(output_dir: Path) -> Path:
    return ensure_dir(output_dir / "reports")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def base_language_code(language: str) -> str:
    value = str(language or "").strip()
    if value.endswith("-orig"):
        value = value[: -len("-orig")]
    return value


def caption_language_priority(language: str) -> tuple[int, str]:
    normalized = str(language or "").strip()
    base = base_language_code(normalized)
    is_original = 0 if normalized.endswith("-orig") else 1
    is_generic = 0 if base and base != normalized else 1
    return (is_original, is_generic, base or normalized)


def extract_caption_urls(raw: dict[str, Any]) -> list[dict[str, str]]:
    automatic_captions = raw.get("automatic_captions") or {}
    subtitles = raw.get("subtitles") or {}
    tracks: list[dict[str, str]] = []

    def add_tracks(source: dict[str, Any], category: str) -> None:
        for language_key in source:
            entries = source.get(language_key) or []
            if not isinstance(entries, Iterable):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                url = str(entry.get("url") or "").strip()
                ext = str(entry.get("ext") or "").strip()
                if not url or not ext:
                    continue
                tracks.append(
                    {
                        "category": category,
                        "language": language_key,
                        "ext": ext,
                        "url": url,
                    }
                )

    add_tracks(subtitles, "subtitle")
    add_tracks(automatic_captions, "automatic")

    category_priority = {"subtitle": 0, "automatic": 1}
    extension_priority = {"vtt": 0, "srv3": 1, "ttml": 2, "json3": 3, "srt": 4, "srv2": 5, "srv1": 6}
    tracks.sort(
        key=lambda item: (
            category_priority.get(item["category"], 10),
            *caption_language_priority(item["language"]),
            extension_priority.get(item["ext"], 50),
        )
    )
    return tracks


def preferred_caption_languages(record: dict[str, Any]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    fallback: list[str] = []
    fallback_seen: set[str] = set()
    for track in record.get("caption_urls") or []:
        if not isinstance(track, dict):
            continue
        language = str(track.get("language") or "").strip()
        if not language:
            continue
        normalized = base_language_code(language)
        if not normalized:
            continue
        category = str(track.get("category") or "").strip()
        if normalized not in fallback_seen:
            fallback_seen.add(normalized)
            fallback.append(normalized)
        if category != "subtitle" and not language.endswith("-orig"):
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    if ordered:
        return ordered
    return fallback[:3]


def normalize_video_record(raw: dict[str, Any]) -> dict[str, Any]:
    video_id = str(raw.get("id") or raw.get("video_id") or "").strip()
    title = clean_text(str(raw.get("title") or ""))
    description = clean_text(str(raw.get("description") or ""))
    url = (
        raw.get("webpage_url")
        or raw.get("original_url")
        or raw.get("url")
        or (f"https://www.youtube.com/watch?v={video_id}" if video_id else "")
    )
    upload_date = str(raw.get("upload_date") or "").strip()
    duration_value = raw.get("duration") if raw.get("duration") is not None else raw.get("duration_seconds")
    duration_seconds = int(duration_value) if duration_value not in (None, "") else None
    view_value = raw.get("view_count")
    view_count = int(view_value) if view_value not in (None, "") else None
    normalized_record = {
        "video_id": video_id,
        "title": title,
        "description": description,
        "url": url,
        "upload_date": upload_date,
        "duration_seconds": duration_seconds,
        "view_count": view_count,
        "channel_title": clean_text(str(raw.get("channel") or raw.get("channel_title") or raw.get("uploader") or "")),
        "transcript_text": clean_text(str(raw.get("transcript_text") or "")),
        "transcript_status": str(raw.get("transcript_status") or ""),
        "transcript_word_count": int(raw.get("transcript_word_count") or 0),
        "summary": clean_text(str(raw.get("summary") or "")),
        "detailed_summary": clean_text(str(raw.get("detailed_summary") or "")),
        "top_phrases": list(raw.get("top_phrases") or []),
        "caption_urls": list(raw.get("caption_urls") or extract_caption_urls(raw)),
        "preferred_languages": list(raw.get("preferred_languages") or []),
        "detected_language": base_language_code(str(raw.get("detected_language") or "").strip()),
    }
    if not normalized_record["detected_language"]:
        normalized_record["detected_language"] = language_for_record(normalized_record)
    return normalized_record


def matches_filters(
    record: dict[str, Any],
    *,
    since_date: str | None = None,
    until_date: str | None = None,
    topic_filter: str | None = None,
    speaker_filter: str | None = None,
    metadata_filters: list[tuple[str, str]] | None = None,
    include_transcript: bool = False,
) -> bool:
    upload_date = str(record.get("upload_date") or "")
    if since_date and upload_date and upload_date < since_date:
        return False
    if until_date and upload_date and upload_date > until_date:
        return False

    for field, expected in metadata_filters or []:
        actual = str(record.get(field, "") or "").lower()
        if expected.lower() not in actual:
            return False

    searchable = " ".join(
        part
        for part in [
            str(record.get("title") or ""),
            str(record.get("description") or ""),
            str(record.get("channel_title") or ""),
            str(record.get("transcript_text") or "") if include_transcript else "",
        ]
        if part
    ).lower()

    if topic_filter and topic_filter.lower() not in searchable:
        return False
    if speaker_filter and speaker_filter.lower() not in searchable:
        return False
    return True


def apply_filters(
    records: list[dict[str, Any]],
    *,
    since_date: str | None = None,
    until_date: str | None = None,
    topic_filter: str | None = None,
    speaker_filter: str | None = None,
    metadata_filters: list[tuple[str, str]] | None = None,
    include_transcript: bool = False,
) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if matches_filters(
            record,
            since_date=since_date,
            until_date=until_date,
            topic_filter=topic_filter,
            speaker_filter=speaker_filter,
            metadata_filters=metadata_filters,
            include_transcript=include_transcript,
        )
    ]


def write_records_csv(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "upload_date",
        "video_id",
        "title",
        "url",
        "duration_seconds",
        "view_count",
        "channel_title",
        "detected_language",
        "transcript_status",
        "transcript_word_count",
        "top_phrases",
        "summary",
        "detailed_summary",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "upload_date": record.get("upload_date", ""),
                    "video_id": record.get("video_id", ""),
                    "title": record.get("title", ""),
                    "url": record.get("url", ""),
                    "duration_seconds": record.get("duration_seconds", ""),
                    "view_count": record.get("view_count", ""),
                    "channel_title": record.get("channel_title", ""),
                    "detected_language": record.get("detected_language", ""),
                    "transcript_status": record.get("transcript_status", ""),
                    "transcript_word_count": record.get("transcript_word_count", 0),
                    "top_phrases": "; ".join(record.get("top_phrases", [])),
                    "summary": record.get("summary", ""),
                    "detailed_summary": record.get("detailed_summary", ""),
                }
            )


def transcript_source_label(status: str | None) -> str:
    value = (status or "").strip()
    if not value:
        return "transcript pending"
    if value == "cached":
        return "saved transcript"
    if value == "direct":
        return "captions available on YouTube"
    if value == "caption-url":
        return "captions retrieved from YouTube"
    if value == "subtitle":
        return "subtitle file downloaded from YouTube"
    if value == "local":
        return "transcribed from audio"
    if "audio-unavailable" in value:
        return "transcript unavailable"
    if value.startswith("direct-unavailable") or value.startswith("caption-unavailable") or value.startswith("subtitle-unavailable"):
        return "captions unavailable"
    return "transcript available"


def dataset_markdown(
    *,
    title: str,
    records: list[dict[str, Any]],
    criteria_lines: list[str] | None = None,
) -> str:
    lines = [f"# {title}", ""]
    if criteria_lines:
        lines.extend(criteria_lines)
        lines.append("")
    lines.append(f"Videos: {len(records)}")
    lines.append("")
    for record in records:
        summary = record.get("detailed_summary") or record.get("summary") or summary_from_record(record)
        lines.append(
            f"- {record.get('upload_date', '')}: [{record.get('title', record.get('video_id', 'Video'))}]({record.get('url', '')})"
            f" | transcript source: {transcript_source_label(record.get('transcript_status'))}"
            f" | language: {record.get('detected_language') or 'unknown'}"
        )
        lines.append(f"  Summary: {summary}")
    return "\n".join(lines).strip() + "\n"
