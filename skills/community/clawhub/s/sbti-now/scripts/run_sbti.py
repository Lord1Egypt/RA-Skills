#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys

from sbti_engine import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    answers_from_pattern,
    calculate_result,
    format_result,
    get_localized,
    get_questions,
    get_special_questions,
    get_types,
    parse_answer_list,
)


def choose_language() -> str:
    prompt = "\n".join(
        [
            "Choose language / 选择语言 / 選擇語言",
            "1. 简体中文 (zh-Hans)",
            "2. 繁體中文 (zh-Hant)",
            "3. English (en)",
            "> ",
        ]
    )
    while True:
        answer = input(prompt).strip()
        if answer == "1":
            return "zh-Hans"
        if answer == "2":
            return "zh-Hant"
        if answer == "3":
            return "en"
        print("Please enter 1, 2, or 3.")


def ask_question(question: dict, language: str, index: int, total: int) -> int:
    print(f"[{index}/{total}] {get_localized(question['text'], language)}")
    for option in question["options"]:
        print(f"  {option['value']}. {get_localized(option['text'], language)}")

    while True:
        answer = input("> ").strip()
        if answer in {"1", "2", "3"}:
            print("")
            return int(answer)
        print("Please enter 1, 2, or 3.")


def resolve_preset(code: str) -> tuple[list[int], list[int]]:
    normalized_code = code.strip().upper()
    personality_type = next(
        (item for item in get_types() if item["code"].upper() == normalized_code),
        None,
    )
    if personality_type is None:
        raise ValueError(f"Unknown preset type: {code}")

    if personality_type["code"] == "DRUNK":
        return answers_from_pattern("MMM-MMM-HMH-MMM-MMM"), [2, 3]
    if personality_type["code"] == "HHHH":
        return parse_answer_list("111122323321213332321221123333", 30), [1, 1]
    return answers_from_pattern(personality_type["pattern"]), [1, 1]


def run_interactive(language: str | None) -> dict:
    selected_language = language or choose_language()
    answers = []
    special_answers = []

    questions = get_questions()
    for index, question in enumerate(questions, start=1):
        answers.append(ask_question(question, selected_language, index, len(questions)))

    special_questions = get_special_questions()
    total = len(questions) + len(special_questions)
    for offset, question in enumerate(special_questions, start=1):
        special_answers.append(
            ask_question(question, selected_language, len(questions) + offset, total)
        )

    return calculate_result(selected_language, answers, special_answers)


def list_types(language: str) -> None:
    for personality_type in get_types():
        print(f"{personality_type['code']}\t{get_localized(personality_type['name'], language)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the self-contained SBTI Now test skill.")
    parser.add_argument("--lang", choices=SUPPORTED_LANGUAGES)
    parser.add_argument("--answers")
    parser.add_argument("--special")
    parser.add_argument("--preset")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list-types", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    language = args.lang or DEFAULT_LANGUAGE

    try:
        if args.list_types:
            list_types(language)
            return 0

        if args.demo or args.preset or args.answers:
            preset_answers = preset_special = None
            if args.demo:
                preset_answers, preset_special = resolve_preset("CTRL")
            elif args.preset:
                preset_answers, preset_special = resolve_preset(args.preset)

            answers = (
                parse_answer_list(args.answers, len(get_questions()), "answers")
                if args.answers
                else preset_answers
            )
            special_answers = (
                parse_answer_list(args.special, len(get_special_questions()), "specialAnswers")
                if args.special
                else preset_special or [1, 1]
            )
            result = calculate_result(language, answers, special_answers)
        else:
            result = run_interactive(args.lang)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_result(result))
        return 0
    except (EOFError, KeyboardInterrupt):
        print("sbti-now skill: aborted by user.", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"sbti-now skill: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
