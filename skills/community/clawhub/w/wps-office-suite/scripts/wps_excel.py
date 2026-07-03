"""
WPS Excel CLI v2.0 - 三引擎自动调用
"""
import subprocess
import json
import sys
from pathlib import Path

WORKER = Path(__file__).parent / "wps_worker.py"


def call_worker(cmd: str, args: dict) -> dict:
    req = json.dumps({"cmd": cmd, "args": args}, ensure_ascii=False)
    proc = subprocess.Popen(
        [sys.executable, str(WORKER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path(__file__).parent.parent),
    )
    stdout, stderr = proc.communicate(input=req.encode("utf-8"), timeout=120)
    if proc.returncode != 0:
        err_msg = stderr.decode("utf-8") if stderr else "未知错误"
        return {"ok": False, "error": f"WPS Worker 异常: {err_msg[:200]}"}
    try:
        return json.loads(stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"ok": False, "error": "Worker 输出解析失败"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="WPS Excel")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create")
    p.add_argument("--name", required=True)
    p.add_argument("--sheets", default="")
    p.add_argument("--filepath", default="")
    p.add_argument("--data", default="", help='JSON: {"Sheet1":[["A",1],["B",2]]}')

    p = sub.add_parser("input")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--data", required=True, help='JSON array [["col1","col2"]]')

    p = sub.add_parser("formula")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--cell", required=True)
    p.add_argument("--formula", required=True)

    p = sub.add_parser("sort")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--sorts", required=True, help='JSON: [{"column":"金额","ascending":false}]')

    p = sub.add_parser("filter")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--conditions", required=True, help='JSON: [{"column":"金额","op":">","value":"1000"}]')
    p.add_argument("--logic", choices=["AND", "OR"], default="AND")

    p = sub.add_parser("chart")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--type", choices=["bar", "line", "pie", "column"], default="bar")
    p.add_argument("--data", default="A1:B10", help="数据范围")
    p.add_argument("--title", default="")

    p = sub.add_parser("add-sheet")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", required=True)
    p.add_argument("--headers", default="")
    p.add_argument("--data", default="")

    p = sub.add_parser("stats")
    p.add_argument("--file", required=True)
    p.add_argument("--sheet", default="Sheet1")
    p.add_argument("--column", required=True)
    p.add_argument("--type", choices=["SUM", "AVG", "COUNT", "MAX", "MIN", "COUNTA"], default="SUM")

    p = sub.add_parser("info")
    p.add_argument("--file", required=True)

    p = sub.add_parser("engine-info", help="引擎信息")

    args = parser.parse_args()

    if args.command == "create":
        sheets = [s.strip() for s in args.sheets.split(",") if s.strip()] if args.sheets else None
        data = json.loads(args.data) if args.data else None
        r = call_worker("create_excel", {
            "name": args.name,
            "sheets": sheets or ["Sheet1"],
            "filepath": args.filepath,
            "data": data or {}
        })
    elif args.command == "input":
        data = json.loads(args.data)
        r = call_worker("input_excel", {
            "filepath": args.file, "sheet": args.sheet, "data": data
        })
    elif args.command == "formula":
        r = call_worker("formula_excel", {
            "filepath": args.file, "sheet": args.sheet,
            "cell": args.cell, "formula": args.formula
        })
    elif args.command == "sort":
        sorts = json.loads(args.sorts)
        r = call_worker("sort_excel", {
            "filepath": args.file, "sheet": args.sheet, "sorts": sorts
        })
    elif args.command == "filter":
        conds = json.loads(args.conditions)
        r = call_worker("filter_excel", {
            "filepath": args.file, "sheet": args.sheet,
            "conditions": conds, "logic": args.logic
        })
    elif args.command == "chart":
        r = call_worker("chart_excel", {
            "filepath": args.file, "sheet": args.sheet,
            "type": args.type, "data": args.data, "title": args.title
        })
    elif args.command == "add-sheet":
        headers = json.loads(args.headers) if args.headers else None
        data = json.loads(args.data) if args.data else None
        r = call_worker("add_sheet_excel", {
            "filepath": args.file, "sheet": args.sheet,
            "headers": headers, "data": data
        })
    elif args.command == "stats":
        r = call_worker("stats_excel", {
            "filepath": args.file, "sheet": args.sheet,
            "column": args.column, "type": args.type
        })
    elif args.command == "info":
        r = call_worker("info_excel", {"filepath": args.file})
    elif args.command == "engine-info":
        r = call_worker("engine_info", {})
    else:
        r = {"ok": False, "error": "未知命令"}

    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
