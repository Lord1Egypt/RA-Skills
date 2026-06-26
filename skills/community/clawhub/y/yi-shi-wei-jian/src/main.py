from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from analyzer import DecisionAnalyzer
from case_store import CaseStore, CaseValidationError, build_case_template
from classifier import SituationClassifier
from renderer import ResponseRenderer
from retriever import CaseRetriever


def read_stdin_text() -> str:
    return sys.stdin.buffer.read().decode("utf-8", errors="strict")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="以史为鉴：把中国历史案例映射到现实决策问题。")
    parser.add_argument("question_text", nargs="*", help="待分析的问题。")
    parser.add_argument("--question", dest="question", help="待分析的问题。")
    parser.add_argument("--top-k", type=int, default=3, help="返回案例数量，默认 3。")
    parser.add_argument("--add-case-file", help="将新增案例 JSON 写入 data/user_cases.json。")
    parser.add_argument("--add-case-json", help="直接传入单条案例 JSON 字符串，并写入 data/user_cases.json。")
    parser.add_argument("--add-case-stdin", action="store_true", help="从标准输入读取单条案例 JSON，并写入 data/user_cases.json。")
    parser.add_argument("--print-case-template", action="store_true", help="输出新增案例模板 JSON。")
    parser.add_argument("--core-cases-path", help="基础案例库路径，默认 data/historical_cases.json。")
    parser.add_argument("--user-cases-path", help="用户案例库路径，默认 data/user_cases.json。")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    cases_path = Path(args.core_cases_path).expanduser().resolve() if args.core_cases_path else repo_root / "data" / "historical_cases.json"
    user_cases_path = Path(args.user_cases_path).expanduser().resolve() if args.user_cases_path else repo_root / "data" / "user_cases.json"
    store = CaseStore(cases_path, user_cases_path)

    if args.print_case_template:
        print(json.dumps(build_case_template(), ensure_ascii=False, indent=2))
        return 0

    add_case_modes = [bool(args.add_case_file), bool(args.add_case_json), bool(args.add_case_stdin)]
    if sum(add_case_modes) > 1:
        parser.error("请从 --add-case-file、--add-case-json 或 --add-case-stdin 中选择一种新增案例输入方式。")

    if args.add_case_file or args.add_case_json or args.add_case_stdin:
        try:
            if args.add_case_file:
                candidate = store.load_case_candidate(Path(args.add_case_file).expanduser().resolve())
            elif args.add_case_json:
                candidate = store.parse_case_payload(args.add_case_json)
            else:
                candidate = store.parse_case_payload(read_stdin_text())
            added_case = store.add_case(candidate)
        except (CaseValidationError, FileNotFoundError, json.JSONDecodeError) as exc:
            print(f"新增案例失败: {exc}", file=sys.stderr)
            return 1
        print(f"新增案例成功: {added_case['id']} -> {user_cases_path}")
        return 0

    question = args.question or " ".join(args.question_text).strip()
    if not question:
        parser.error("请通过 --question 或位置参数提供问题。")

    classifier = SituationClassifier()
    retriever = CaseRetriever(cases_path, user_cases_path)
    analyzer = DecisionAnalyzer()
    renderer = ResponseRenderer()

    assessment = classifier.classify(question)
    cases = retriever.retrieve(question, assessment, top_k=max(2, min(args.top_k, 4)))
    analysis = analyzer.analyze(question, assessment, cases)
    print(renderer.render(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
