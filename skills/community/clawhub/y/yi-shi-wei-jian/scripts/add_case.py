from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from case_store import CaseStore, CaseValidationError, build_case_template  # noqa: E402


def read_stdin_text() -> str:
    return sys.stdin.buffer.read().decode("utf-8", errors="strict")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将新增历史案例写入 data/user_cases.json。")
    parser.add_argument("--case-file", help="新增案例 JSON 文件路径。")
    parser.add_argument("--case-json", help="直接传入单条案例 JSON 字符串。")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取单条案例 JSON。")
    parser.add_argument("--print-template", action="store_true", help="输出案例模板 JSON。")
    parser.add_argument("--core-cases-path", help="基础案例库路径，默认 data/historical_cases.json。")
    parser.add_argument("--user-cases-path", help="用户案例库路径，默认 data/user_cases.json。")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.print_template:
        print(json.dumps(build_case_template(), ensure_ascii=False, indent=2))
        return 0

    input_modes = [bool(args.case_file), bool(args.case_json), bool(args.stdin)]
    if sum(input_modes) != 1:
        parser.error("请从 --case-file、--case-json 或 --stdin 中选择一种输入方式。")

    core_cases_path = Path(args.core_cases_path).expanduser().resolve() if args.core_cases_path else REPO_ROOT / "data" / "historical_cases.json"
    user_cases_path = Path(args.user_cases_path).expanduser().resolve() if args.user_cases_path else REPO_ROOT / "data" / "user_cases.json"
    store = CaseStore(core_cases_path, user_cases_path)

    try:
        if args.case_file:
            case_file = Path(args.case_file).expanduser().resolve()
            if not case_file.exists():
                print(f"案例文件不存在: {case_file}", file=sys.stderr)
                return 1
            candidate = store.load_case_candidate(case_file)
        elif args.case_json:
            candidate = store.parse_case_payload(args.case_json)
        else:
            candidate = store.parse_case_payload(read_stdin_text())
        added_case = store.add_case(candidate)
    except (CaseValidationError, json.JSONDecodeError) as exc:
        print(f"新增案例失败: {exc}", file=sys.stderr)
        return 1

    print(f"新增案例成功: {added_case['id']} -> {user_cases_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
