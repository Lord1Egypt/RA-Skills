#!/usr/bin/env python3
"""Convert Whisper word-timestamp JSON into Remotion caption JSON."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_MERGE_TERMS = [
    "Codex",
    "ChatGPT",
    "Remotion",
    "Whisper",
    "提示词",
    "逐词",
    "高亮",
    "字幕",
    "手机",
    "照片",
    "视频",
    "封面",
]

BREAK_PUNCTUATION = "。，,！？!?；;：:、"
DISPLAY_PUNCTUATION = BREAK_PUNCTUATION


def ms(value: float | int) -> int:
    return int(round(float(value) * 1000))


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_replacements(items: list[str]) -> list[tuple[str, str]]:
    replacements: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--replace must use OLD=NEW format: {item}")
        old, new = item.split("=", 1)
        replacements.append((old, new))
    return replacements


def apply_replacements(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def match_key(text: str) -> str:
    return re.sub(rf"[\s{re.escape(BREAK_PUNCTUATION)}]+", "", text)


def trailing_punctuation(text: str) -> str:
    match = re.search(rf"[{re.escape(BREAK_PUNCTUATION)}]+$", text.strip())
    return match.group(0) if match else ""


def strip_display_punctuation(text: str) -> str:
    cleaned = clean_text(text)
    return re.sub(
        rf"^[{re.escape(DISPLAY_PUNCTUATION)}]+|[{re.escape(DISPLAY_PUNCTUATION)}]+$",
        "",
        cleaned,
    ).strip()


def with_trailing_punctuation(text: str, source_text: str) -> str:
    suffix = trailing_punctuation(source_text)
    if suffix and not text.endswith(suffix):
        return f"{text}{suffix}"
    return text


def term_matches(tokens: list[dict[str, Any]], index: int, term: str) -> int:
    combined = ""
    target = match_key(term)
    for cursor in range(index, len(tokens)):
        combined += tokens[cursor]["text"]
        candidate = match_key(combined)
        if candidate == target:
            return cursor - index + 1
        if not target.startswith(candidate):
            return 0
    return 0


def merge_terms(
    tokens: list[dict[str, Any]],
    terms: list[str],
    keyword_terms: set[str],
) -> list[dict[str, Any]]:
    sorted_terms = sorted(set(terms), key=len, reverse=True)
    merged: list[dict[str, Any]] = []
    index = 0

    while index < len(tokens):
        matched_term = ""
        matched_count = 0
        for term in sorted_terms:
            count = term_matches(tokens, index, term)
            if count:
                matched_term = term
                matched_count = count
                break

        if matched_count:
            chunk = tokens[index : index + matched_count]
            chunk_text = "".join(str(item["text"]) for item in chunk)
            merged.append(
                {
                    "text": with_trailing_punctuation(matched_term, chunk_text),
                    "startMs": chunk[0]["startMs"],
                    "endMs": chunk[-1]["endMs"],
                    "keyword": matched_term in keyword_terms,
                }
            )
            index += matched_count
            continue

        token = dict(tokens[index])
        token["keyword"] = token["text"] in keyword_terms
        merged.append(token)
        index += 1

    return merged


def replace_phrases(
    tokens: list[dict[str, Any]],
    replacements: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    sorted_replacements = sorted(replacements, key=lambda item: len(item[0]), reverse=True)
    replaced: list[dict[str, Any]] = []
    index = 0

    while index < len(tokens):
        matched_new = ""
        matched_count = 0
        for old, new in sorted_replacements:
            count = term_matches(tokens, index, old)
            if count:
                matched_new = new
                matched_count = count
                break

        if matched_count:
            chunk = tokens[index : index + matched_count]
            chunk_text = "".join(str(item["text"]) for item in chunk)
            token: dict[str, Any] = {
                "text": with_trailing_punctuation(matched_new, chunk_text),
                "startMs": chunk[0]["startMs"],
                "endMs": chunk[-1]["endMs"],
            }
            confidences = [
                float(item["confidence"])
                for item in chunk
                if "confidence" in item
            ]
            if confidences:
                token["confidence"] = min(confidences)
            replaced.append(token)
            index += matched_count
            continue

        replaced.append(dict(tokens[index]))
        index += 1

    return replaced


def tokens_to_text(tokens: list[dict[str, Any]]) -> str:
    return clean_text("".join(str(token["text"]) for token in tokens))


def display_tokens(tokens: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for token in tokens:
        text = strip_display_punctuation(str(token["text"]))
        if not text:
            continue
        display_token = dict(token)
        display_token["text"] = text
        result.append(display_token)
    return result


def visible_length(tokens: list[dict[str, Any]]) -> int:
    return len(match_key(tokens_to_text(tokens)))


def has_break_punctuation(token: dict[str, Any]) -> bool:
    return bool(trailing_punctuation(str(token["text"])))


def find_split_index(tokens: list[dict[str, Any]], gap_ms: int) -> int:
    for index in range(len(tokens) - 2, -1, -1):
        current = tokens[index]
        next_token = tokens[index + 1]
        gap = int(next_token["startMs"]) - int(current["endMs"])
        if has_break_punctuation(current) or gap >= gap_ms:
            return index
    return -1


def split_caption_tokens(
    tokens: list[dict[str, Any]],
    max_chars: int,
    max_duration_ms: int,
    gap_ms: int,
    min_punctuation_caption_ms: int,
) -> list[list[dict[str, Any]]]:
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []

    def needs_split(items: list[dict[str, Any]]) -> bool:
        if len(items) < 2:
            return False
        duration = int(items[-1]["endMs"]) - int(items[0]["startMs"])
        return visible_length(items) > max_chars or duration > max_duration_ms

    for token in tokens:
        current.append(token)
        duration = int(current[-1]["endMs"]) - int(current[0]["startMs"])
        if has_break_punctuation(token) and duration >= min_punctuation_caption_ms:
            chunks.append(current)
            current = []
            continue
        while needs_split(current):
            split_at = find_split_index(current, gap_ms)
            if split_at < 0:
                split_at = len(current) - 2
            if split_at < 0:
                break
            chunks.append(current[: split_at + 1])
            current = current[split_at + 1 :]

    if current:
        chunks.append(current)

    return chunks


def segment_tokens(
    segment: dict[str, Any],
    replacements: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    tokens: list[dict[str, Any]] = []
    for word in segment.get("words", []):
        raw_text = clean_text(str(word.get("word", "")))
        text = apply_replacements(raw_text, replacements)
        if not text:
            continue
        token = {
            "text": text,
            "startMs": ms(word.get("start", segment.get("start", 0))),
            "endMs": ms(word.get("end", segment.get("end", 0))),
        }
        if "probability" in word:
            token["confidence"] = word["probability"]
        tokens.append(token)
    return tokens


def convert(
    whisper_json: Path,
    output_json: Path,
    replacements: list[tuple[str, str]],
    phrase_replacements: list[tuple[str, str]],
    merge_term_values: list[str],
    keyword_values: list[str],
    max_caption_chars: int,
    max_caption_duration_ms: int,
    split_gap_ms: int,
    min_punctuation_caption_ms: int,
    keep_display_punctuation: bool,
) -> None:
    data = json.loads(whisper_json.read_text(encoding="utf-8"))
    keyword_terms = set(keyword_values)
    merge_term_values = list(dict.fromkeys([*merge_term_values, *keyword_values]))

    captions: list[dict[str, Any]] = []
    for segment in data.get("segments", []):
        text = clean_text(str(segment.get("text", "")))
        text = apply_replacements(text, phrase_replacements)
        text = apply_replacements(text, replacements)
        tokens = segment_tokens(segment, replacements)
        if not tokens:
            continue
        tokens = replace_phrases(tokens, phrase_replacements)
        tokens = merge_terms(tokens, merge_term_values, keyword_terms)
        for chunk in split_caption_tokens(
            tokens,
            max_caption_chars,
            max_caption_duration_ms,
            split_gap_ms,
            min_punctuation_caption_ms,
        ):
            output_tokens = (
                [dict(token) for token in chunk]
                if keep_display_punctuation
                else display_tokens(chunk)
            )
            if not output_tokens:
                continue
            captions.append(
                {
                    "text": tokens_to_text(output_tokens),
                    "startMs": chunk[0]["startMs"],
                    "endMs": chunk[-1]["endMs"],
                    "tokens": output_tokens,
                }
            )

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(captions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Whisper JSON with word timestamps to Remotion captions.json"
    )
    parser.add_argument("whisper_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument(
        "--replace",
        action="append",
        default=[],
        help="Per-token text correction in OLD=NEW form. Can be repeated.",
    )
    parser.add_argument(
        "--replace-phrase",
        action="append",
        default=[],
        help="Adjacent-token phrase correction in OLD=NEW form. Can be repeated.",
    )
    parser.add_argument(
        "--merge-term",
        action="append",
        default=[],
        help="Adjacent token text to merge into one displayed token. Can be repeated.",
    )
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Terms to color as secondary keyword highlights. Can be repeated.",
    )
    parser.add_argument(
        "--no-default-merge-terms",
        action="store_true",
        help="Disable the built-in merge terms for common video/subtitle words.",
    )
    parser.add_argument(
        "--max-caption-chars",
        type=int,
        default=28,
        help="Split long Whisper segments when a caption exceeds this visible character count.",
    )
    parser.add_argument(
        "--max-caption-duration-ms",
        type=int,
        default=4200,
        help="Split long Whisper segments when a caption exceeds this duration.",
    )
    parser.add_argument(
        "--split-gap-ms",
        type=int,
        default=260,
        help="Prefer splitting at word gaps at least this long.",
    )
    parser.add_argument(
        "--min-punctuation-caption-ms",
        type=int,
        default=900,
        help="Split at punctuation once the current caption is at least this long.",
    )
    parser.add_argument(
        "--keep-display-punctuation",
        action="store_true",
        help=(
            "Keep punctuation in final displayed captions. By default display "
            "punctuation is stripped after splitting."
        ),
    )
    args = parser.parse_args()

    merge_terms_arg = [] if args.no_default_merge_terms else DEFAULT_MERGE_TERMS[:]
    merge_terms_arg.extend(args.merge_term)

    convert(
        args.whisper_json,
        args.output_json,
        parse_replacements(args.replace),
        parse_replacements(args.replace_phrase),
        merge_terms_arg,
        args.keyword,
        args.max_caption_chars,
        args.max_caption_duration_ms,
        args.split_gap_ms,
        args.min_punctuation_caption_ms,
        args.keep_display_punctuation,
    )


if __name__ == "__main__":
    main()
