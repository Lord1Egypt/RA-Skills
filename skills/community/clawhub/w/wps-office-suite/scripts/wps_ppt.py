"""
WPS PPT CLI v2.0 - 三引擎自动调用
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
    parser = argparse.ArgumentParser(description="WPS PPT")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create")
    p.add_argument("--title", required=True)
    p.add_argument("--filepath", default="")
    p.add_argument("--slides", default="")

    p = sub.add_parser("add-slide")
    p.add_argument("--file", required=True)
    p.add_argument("--layout", default="title_content")
    p.add_argument("--title", default="")

    p = sub.add_parser("insert")
    p.add_argument("--file", required=True)
    p.add_argument("--slide", type=int, required=True)
    p.add_argument("--content", required=True)

    p = sub.add_parser("theme")
    p.add_argument("--file", required=True)
    p.add_argument("--name", default="business")

    p = sub.add_parser("export")
    p.add_argument("--file", required=True)
    p.add_argument("--format", default="pdf")

    p = sub.add_parser("info")
    p.add_argument("--file", required=True)

    p = sub.add_parser("engine-info")

    args = parser.parse_args()

    if args.command == "create":
        r = call_worker("create_ppt", {
            "title": args.title,
            "filepath": args.filepath,
        })
    elif args.command == "add-slide":
        r = call_worker("add_ppt_slide", {
            "filepath": args.file, "layout": args.layout, "title": args.title
        })
    elif args.command == "insert":
        r = call_worker("insert_ppt", {
            "filepath": args.file, "slide": args.slide, "content": args.content
        })
    elif args.command == "theme":
        r = call_worker("theme_ppt", {"filepath": args.file, "name": args.name})
    elif args.command == "export":
        r = call_worker("export_ppt", {"filepath": args.file, "format": args.format})
    elif args.command == "info":
        r = call_worker("info_ppt", {"filepath": args.file})
    elif args.command == "engine-info":
        r = call_worker("engine_info", {})
    else:
        r = {"ok": False, "error": "未知命令"}

    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
