"""
WPS Word CLI v2.0 - 三引擎自动调用
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
    stdout, stderr = proc.communicate(input=req.encode("utf-8"), timeout=60)
    if proc.returncode != 0:
        err_msg = stderr.decode("utf-8") if stderr else "未知错误"
        return {"ok": False, "error": f"WPS Worker 异常: {err_msg[:200]}"}
    try:
        return json.loads(stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"ok": False, "error": f"Worker 输出解析失败"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="WPS Word")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="创建文档")
    p.add_argument("--title", required=True)
    p.add_argument("--filepath", default="")

    p = sub.add_parser("edit", help="编辑")
    p.add_argument("--file", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--position", choices=["start", "end", "replace"], default="end")

    p = sub.add_parser("format", help="格式")
    p.add_argument("--file", required=True)
    p.add_argument("--align", default="")
    p.add_argument("--font", default="")
    p.add_argument("--size", type=int, default=0)
    p.add_argument("--bold", action="store_true")
    p.add_argument("--color", default="")
    p.add_argument("--space-after", type=float, default=0)
    p.add_argument("--first-indent", type=float, default=0)

    p = sub.add_parser("export", help="导出")
    p.add_argument("--file", required=True)
    p.add_argument("--format", default="pdf")

    p = sub.add_parser("info", help="信息")
    p.add_argument("--file", required=True)

    p = sub.add_parser("engine-info", help="引擎信息")

    args = parser.parse_args()

    if args.command == "create":
        r = call_worker("create_word", {"title": args.title, "filepath": args.filepath})
    elif args.command == "edit":
        r = call_worker("edit_word", {"filepath": args.file, "text": args.text, "position": args.position})
    elif args.command == "format":
        r = call_worker("format_word", {"filepath": args.file, "align": args.align, "font": args.font, "size": args.size, "bold": args.bold, "color": args.color, "space_after": args.space_after, "first_line_indent": args.first_indent})
    elif args.command == "export":
        r = call_worker("export_word", {"filepath": args.file, "format": args.format})
    elif args.command == "info":
        r = call_worker("info_word", {"filepath": args.file})
    elif args.command == "engine-info":
        r = call_worker("engine_info", {})
    else:
        r = {"ok": False, "error": "未知命令"}

    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
