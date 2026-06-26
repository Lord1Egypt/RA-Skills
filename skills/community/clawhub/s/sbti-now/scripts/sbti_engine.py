#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_LANGUAGE = "zh-Hans"
FALLBACK_THRESHOLD = 60
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "question-bank.json"
QUESTION_BANK = json.loads(DATA_PATH.read_text(encoding="utf-8"))
SUPPORTED_LANGUAGES = tuple(QUESTION_BANK["languages"])
TYPE_INDEX = {item["code"]: item for item in QUESTION_BANK["types"]}


def get_localized(value, language: str = DEFAULT_LANGUAGE) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return (
        value.get(language)
        or value.get(DEFAULT_LANGUAGE)
        or value.get("en")
        or next(iter(value.values()), "")
    )


def normalize_language(language: str | None) -> str:
    if language in SUPPORTED_LANGUAGES:
        return language
    return DEFAULT_LANGUAGE


def _assert_answer_value(value: int, field_name: str) -> None:
    if value not in (1, 2, 3):
        raise ValueError(f"{field_name} must contain only 1, 2, or 3.")


def parse_answer_list(input_value, expected_length: int, field_name: str = "answers") -> list[int]:
    if isinstance(input_value, (list, tuple)):
        values = [int(item) for item in input_value]
    elif isinstance(input_value, str) and input_value.strip():
        if "," in input_value:
            values = [int(item.strip()) for item in input_value.split(",") if item.strip()]
        else:
            values = [int(char) for char in input_value.replace(" ", "")]
    else:
        raise ValueError(f"{field_name} must be a non-empty string or array.")

    if len(values) != expected_length:
        raise ValueError(f"{field_name} must contain {expected_length} answers.")

    for value in values:
        _assert_answer_value(value, field_name)

    return values


def flatten_pattern(pattern: str) -> str:
    return pattern.replace("-", "")


def split_every(text: str, size: int) -> list[str]:
    return [text[index : index + size] for index in range(0, len(text), size)]


def score_to_level(score: int) -> str:
    if score <= 3:
        return "L"
    if score == 4:
        return "M"
    return "H"


def level_to_number(level: str) -> int:
    return {"L": 1, "M": 2, "H": 3}[level]


def answers_from_pattern(pattern: str) -> list[int]:
    flattened = flatten_pattern(pattern)
    if len(flattened) != len(QUESTION_BANK["dimensionOrder"]):
        raise ValueError("Pattern must describe 15 dimensions.")

    answers: list[int] = []
    for level in flattened:
        if level == "L":
            answers.extend((1, 1))
        elif level == "M":
            answers.extend((1, 3))
        elif level == "H":
            answers.extend((3, 3))
        else:
            raise ValueError(f"Unsupported pattern level: {level}")
    return answers


def calculate_dimensions(answers: list[int]) -> dict[str, str]:
    questions = QUESTION_BANK["questions"]
    if len(answers) != len(questions):
        raise ValueError(f"Expected {len(questions)} standard answers before scoring.")

    totals: dict[str, int] = {}
    for question, answer in zip(questions, answers):
        totals[question["dimension"]] = totals.get(question["dimension"], 0) + int(answer)

    return {
        dimension: score_to_level(totals[dimension])
        for dimension in QUESTION_BANK["dimensionOrder"]
    }


def vector_from_dimensions(dimensions: dict[str, str]) -> str:
    raw = "".join(dimensions[dimension] for dimension in QUESTION_BANK["dimensionOrder"])
    return "-".join(split_every(raw, 3))


def build_localized_type(personality_type: dict, language: str, similarity: int) -> dict:
    return {
        "code": personality_type["code"],
        "name": get_localized(personality_type["name"], language),
        "description": get_localized(personality_type["description"], language),
        "traits": list(personality_type["traits"]),
        "shareableText": get_localized(personality_type["shareableText"], language),
        "similarity": similarity,
        "pattern": personality_type["pattern"],
    }


def build_dimension_explanations(dimensions: dict[str, str], language: str) -> list[dict]:
    return [
        {
            "code": dimension,
            "model": get_localized(QUESTION_BANK["dimensionMeta"][dimension]["modelName"], language),
            "title": get_localized(QUESTION_BANK["dimensionMeta"][dimension]["title"], language),
            "level": dimensions[dimension],
            "explanation": get_localized(
                QUESTION_BANK["dimensionMeta"][dimension]["levels"][dimensions[dimension]],
                language,
            ),
        }
        for dimension in QUESTION_BANK["dimensionOrder"]
    ]


def get_standard_matches(dimensions: dict[str, str]) -> list[dict]:
    flattened_vector = flatten_pattern(vector_from_dimensions(dimensions))
    matches = []
    for personality_type in QUESTION_BANK["types"]:
        if personality_type["code"] in {"DRUNK", "HHHH"}:
            continue

        target = flatten_pattern(personality_type["pattern"])
        distance = sum(
            abs(level_to_number(flattened_vector[index]) - level_to_number(target[index]))
            for index in range(len(flattened_vector))
        )
        similarity = max(
            0,
            round((1 - distance / (len(QUESTION_BANK["dimensionOrder"]) * 2)) * 100),
        )
        matches.append(
            {
                "type": personality_type,
                "distance": distance,
                "similarity": similarity,
            }
        )

    matches.sort(key=lambda item: (-item["similarity"], item["distance"]))
    return matches


def calculate_result(language: str, answers, special_answers=(1, 1)) -> dict:
    normalized_language = normalize_language(language)
    parsed_answers = parse_answer_list(answers, len(QUESTION_BANK["questions"]), "answers")
    parsed_special = parse_answer_list(
        special_answers,
        len(QUESTION_BANK["specialQuestions"]),
        "specialAnswers",
    )
    dimensions = calculate_dimensions(parsed_answers)
    vector = vector_from_dimensions(dimensions)
    matches = get_standard_matches(dimensions)
    best_match = matches[0]
    drinks, liquor = parsed_special

    matched_type = best_match["type"]
    score = best_match["similarity"]
    reason = "prototype"

    if drinks >= 2 and liquor == 3:
        matched_type = TYPE_INDEX["DRUNK"]
        score = 100
        reason = "special:drunk"
    elif best_match["similarity"] < FALLBACK_THRESHOLD:
        matched_type = TYPE_INDEX["HHHH"]
        reason = "fallback:hhhh"

    return {
        "language": normalized_language,
        "personality": matched_type["code"],
        "personalityName": get_localized(matched_type["name"], normalized_language),
        "score": score,
        "vector": vector,
        "dimensions": dimensions,
        "matchedType": build_localized_type(matched_type, normalized_language, score),
        "topMatches": [
            build_localized_type(item["type"], normalized_language, item["similarity"])
            for item in matches[:3]
        ],
        "answers": parsed_answers,
        "specialAnswers": parsed_special,
        "reason": reason,
        "dimensionExplanations": build_dimension_explanations(dimensions, normalized_language),
    }


def format_result(result: dict) -> str:
    lines = [
        f"{result['personality']} · {result['personalityName']}",
        f"score: {result['score']}%",
        f"vector: {result['vector']}",
        f"share: {result['matchedType']['shareableText']}",
        "top matches:",
    ]

    for match in result["topMatches"]:
        lines.append(f"- {match['code']} · {match['name']} ({match['similarity']}%)")

    lines.append("dimensions:")
    for explanation in result["dimensionExplanations"]:
        lines.append(
            f"- {explanation['code']} {explanation['level']} · "
            f"{explanation['title']}: {explanation['explanation']}"
        )

    return "\n".join(lines)


def get_questions() -> list[dict]:
    return QUESTION_BANK["questions"]


def get_special_questions() -> list[dict]:
    return QUESTION_BANK["specialQuestions"]


def get_types() -> list[dict]:
    return QUESTION_BANK["types"]
