"""
WPS PPT CLI v4.1 - 四引擎自动调用 + 智能生成
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

    p = sub.add_parser("docx-to-ppt", help="Word → PPT 一键生成")
    p.add_argument("--input", required=True, help="输入 .docx 文件路径")
    p.add_argument("--output", default="", help="输出 .pptx 文件路径")
    p.add_argument("--title", default="", help="PPT 标题")
    p.add_argument("--theme", choices=["business", "tech", "minimal"], default="business")

    p = sub.add_parser("generate", help="智能生成 PPT（多源输入 + 增强）")
    p.add_argument("--input", required=True, help="输入文件路径（Word/Markdown/思维导图/纯文本）")
    p.add_argument("--output", default="", help="输出 PPT 路径")
    p.add_argument("--type", choices=["auto", "word", "markdown", "mindmap", "text"], default="auto")
    p.add_argument("--title", default="", help="PPT 标题")
    p.add_argument("--theme", choices=["business", "tech", "minimal"], default="business")
    p.add_argument("--brand-color", default="", help="企业品牌色（HEX 格式，如 #1A73E8）")
    p.add_argument("--scheme-type", choices=["complementary", "analogous", "triadic"], default="complementary")
    p.add_argument("--no-notes", action="store_true", help="不生成演讲者备注")
    p.add_argument("--no-animations", action="store_true", help="不生成动画建议")
    p.add_argument("--no-rehearsal", action="store_true", help="不生成排练报告")

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
    elif args.command == "docx-to-ppt":
        r = call_worker("docx_to_ppt", {
            "input": args.input, "output": args.output,
            "title": args.title, "theme": args.theme
        })
    elif args.command == "generate":
        r = call_worker("ppt_generate", {
            "input": args.input,
            "output": args.output,
            "type": args.type,
            "title": args.title,
            "theme": args.theme,
            "brand_color": args.brand_color,
            "scheme_type": args.scheme_type,
            "no_notes": args.no_notes,
            "no_animations": args.no_animations,
            "no_rehearsal": args.no_rehearsal,
        })
    else:
        r = {"ok": False, "error": "未知命令"}

    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
