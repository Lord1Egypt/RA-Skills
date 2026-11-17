"""
WPS Word CLI v4.8 - 四引擎自动调用（含会议纪要 + COM 健康检查 + 文档翻译 + MD转换 + 邮件回复 + 周报月报）
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

    p = sub.add_parser("long-document", help="长文档排版（目录/页眉页脚/编号/图表索引/格式统一）")
    p.add_argument("--file", required=True, help="Word 文件路径")
    p.add_argument("--action", default="analyze",
                   choices=["analyze", "toc", "header", "numbering", "fig-index", "xref", "format", "all", "preview"],
                   help="排版动作")
    p.add_argument("--max-level", type=int, default=3, help="目录/编号层级")
    p.add_argument("--field", action="store_true", help="目录使用域代码")
    p.add_argument("--insert", action="store_true", help="插入到文档")
    p.add_argument("--odd-even", action="store_true", help="奇偶页不同页眉")
    p.add_argument("--odd-header", default="", help="奇数页页眉")
    p.add_argument("--even-header", default="", help="偶数页页眉")
    p.add_argument("--chapter-in-header", action="store_true", help="章节标题同步到页眉")
    p.add_argument("--page-number", action="store_true", help="添加页码")
    p.add_argument("--page-format", default="arabic", help="页码格式")
    p.add_argument("--page-start", type=int, default=1, help="起始页码")
    p.add_argument("--style", default="arabic", help="编号样式: chinese/arabic/roman")
    p.add_argument("--preset", default="thesis", help="格式预设: thesis/bid/report")
    p.add_argument("--numbering-style", default="arabic", help="标题编号样式")
    p.add_argument("--output", default="", help="输出路径（不指定则覆盖原文件）")

    # v4.7: MD→Word 转换
    p = sub.add_parser("md-convert", help="Markdown → Word/PPT")
    p.add_argument("--file", default="", help="Markdown 文件路径（单文件模式）")
    p.add_argument("--output", default="", help="输出文件路径（单文件模式）")
    p.add_argument("--format", default="docx", choices=["docx", "pptx"], help="输出格式")
    p.add_argument("--dir", default="", help="输入目录（批量模式）")
    p.add_argument("--output-dir", default="", help="输出目录（批量模式）")

    # v4.5: 会议纪要子命令
    p = sub.add_parser("meeting-minutes", help="会议纪要生成（音频→纪要→Word）")
    p.add_argument("--file", required=True, help="音频文件路径（wav/mp3/m4a）")
    p.add_argument("--output", default="", help="输出 Word 文件路径")
    p.add_argument("--title", default="会议纪要", help="文档标题")
    p.add_argument("--language", default="zh", help="语言代码")
    p.add_argument("--asr-method", default="auto", choices=["auto", "whisper-local", "azure-speech", "google-stt", "template"])
    p.add_argument("--summary-method", default="auto", choices=["auto", "rule-engine", "external-llm", "pure-template"])
    p.add_argument("--segment-minutes", type=int, default=5, help="音频分段时长（分钟）")

    # v4.5: COM 健康检查子命令
    p = sub.add_parser("com-health", help="COM 健康检查（WPS/MS Office 状态检测）")
    p.add_argument("--check", default="full", choices=["full", "wps", "ms", "residuals", "release"], help="检查类型")
    p.add_argument("--force", action="store_true", help="强制清理（包括 COM 缓存）")
    p.add_argument("--auto-release", action="store_true", help="检查后自动释放")

    # v4.6: 文档翻译子命令
    p = sub.add_parser("translate", help="文档翻译（Word/Excel/PPT 专业翻译）")
    p.add_argument("--file", default="", help="输入文件路径（单文件模式）")
    p.add_argument("--output", default="", help="输出文件路径（单文件模式）")
    p.add_argument("--source", default="", help="源语言（不指定则自动检测）")
    p.add_argument("--target", default="zh", help="目标语言")
    p.add_argument("--method", default="auto", choices=["auto", "cn-llm-router", "local-rule", "pure-template"], help="翻译引擎")
    p.add_argument("--input-dir", default="", help="输入目录（批量模式）")
    p.add_argument("--output-dir", default="", help="输出目录（批量模式）")

    # v4.8: 邮件智能回复
    p = sub.add_parser("email-reply", help="邮件智能回复（模板匹配 + 可选 LLM）")
    p.add_argument("--content", required=True, help="邮件内容")
    p.add_argument("--tone", default="friendly",
                   choices=["friendly", "polite", "formal", "professional"],
                   help="回复语气")
    p.add_argument("--lang", default="zh", choices=["zh", "en"])
    p.add_argument("--context", default="", help="上下文/历史邮件")
    p.add_argument("--template", default="", help="自定义模板路径")
    p.add_argument("--output", default="", help="输出回复到 Word 文档路径")

    # v4.8: 周报/月报自动生成
    p = sub.add_parser("report", help="周报/月报自动生成（关键点→Word 报告）")
    p.add_argument("--type", required=True, choices=["weekly", "monthly"],
                   help="报告类型")
    p.add_argument("--points", required=True, help="关键点（逗号分隔）")
    p.add_argument("--title", default="", help="报告标题")
    p.add_argument("--author", default="", help="作者")
    p.add_argument("--output", required=True, help="输出 .docx 路径")
    p.add_argument("--tone", default="formal", choices=["formal", "casual"],
                   help="报告语气")
    p.add_argument("--template", default="", help="自定义报告模板路径")

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
    elif args.command == "long-doc":
        r = call_worker("long_document", {
            "file": args.file,
            "task": args.task,
            "max_level": args.max_level,
            "field": args.field,
            "insert": args.insert,
            "odd_even": args.odd_even,
            "odd_header": args.odd_header,
            "even_header": args.even_header,
            "chapter_in_header": args.chapter_in_header,
            "page_number": args.page_number,
            "page_format": args.page_format,
            "page_start": args.page_start,
            "style": args.style,
            "preset": args.preset,
            "numbering_style": args.numbering_style,
            "output": args.output,
        })
    elif args.command == "meeting-minutes":
        r = call_worker("meeting_minutes", {
            "file": args.file,
            "output": args.output,
            "title": args.title,
            "language": args.language,
            "asr_method": args.asr_method,
            "summary_method": args.summary_method,
            "segment_minutes": args.segment_minutes,
        })
    elif args.command == "com-health":
        r = call_worker("com_health", {
            "check_type": args.check,
            "force": args.force,
            "auto_release": args.auto_release,
        })
    elif args.command == "translate":
        # v4.6: 文档翻译
        from document_translator import DocumentTranslator
        t = DocumentTranslator(engine_method=args.method)
        if args.input_dir and args.output_dir:
            r = t.batch_translate(args.input_dir, args.output_dir, args.source, args.target)
        elif args.file and args.output:
            r = t.translate_document(args.file, args.output, args.source, args.target)
        else:
            r = {"ok": False, "error": "请指定 --file/--output 或 --input-dir/--output-dir"}
        r = {"ok": r.get("success", False), **r}
    elif args.command == "long-document":
        # v4.7: 长文档排版统一入口（--action 路由）
        r = call_worker("long_document", {
            "file": args.file,
            "task": args.action,
            "max_level": args.max_level,
            "field": args.field,
            "insert": args.insert,
            "odd_even": args.odd_even,
            "odd_header": args.odd_header,
            "even_header": args.even_header,
            "chapter_in_header": args.chapter_in_header,
            "page_number": args.page_number,
            "page_format": args.page_format,
            "page_start": args.page_start,
            "style": args.style,
            "preset": args.preset,
            "numbering_style": args.numbering_style,
            "output": args.output,
        })
    elif args.command == "email-reply":
        # v4.8: 邮件智能回复
        from email_reply import EmailReplier
        replier = EmailReplier()
        result = replier.reply(
            content=args.content,
            tone=args.tone,
            lang=args.lang,
            context=args.context,
            template_path=args.template or "",
        )
        # 如果指定了 output，生成 Word 文档
        if args.output and result.get("ok"):
            reply_text = result.get("reply", "")
            if reply_text:
                try:
                    from docx import Document
                    from docx.shared import Pt
                    doc = Document()
                    doc.add_paragraph(reply_text)
                    doc.save(args.output)
                    result["output"] = args.output
                except ImportError:
                    result["docx_error"] = "python-docx 未安装，仅返回文本"
        r = {"ok": result.get("ok", False), **result}
    elif args.command == "report":
        # v4.8: 周报/月报自动生成
        from report_generator import ReportGenerator
        gen = ReportGenerator()
        points_list = [pt.strip() for pt in args.points.split(",") if pt.strip()]
        if not points_list:
            r = {"ok": False, "error": "请指定 --points（逗号分隔的关键点）"}
        else:
            r = gen.generate(
                report_type=args.type,
                points=points_list,
                title=args.title or f"{'周' if args.type == 'weekly' else '月'}报",
                author=args.author,
                date="",
                template_path=args.template or "",
                output=args.output,
                tone=args.tone,
            )
    elif args.command == "md-convert":
        # v4.7: MD→Word/PPT
        from md_converter import MDConverter
        converter = MDConverter()
        if args.dir:
            # 批量模式
            import os
            from pathlib import Path
            input_path = Path(args.dir)
            output_path = Path(args.output_dir) if args.output_dir else input_path.parent / "md_output"
            output_path.mkdir(parents=True, exist_ok=True)
            md_files = list(input_path.glob("*.md")) + list(input_path.glob("*.markdown"))
            results = []
            for md_file in md_files:
                out_file = output_path / f"{md_file.stem}.{'pptx' if args.format == 'pptx' else 'docx'}"
                if args.format == "pptx":
                    result = converter.md_to_pptx(str(md_file), str(out_file))
                else:
                    result = converter.md_to_docx(str(md_file), str(out_file))
                results.append({"file": md_file.name, "success": result.get("success", False)})
            r = {"ok": True, "count": len(results), "results": results}
        else:
            # 单文件模式
            if args.format == "pptx":
                result = converter.md_to_pptx(args.file, args.output)
            else:
                result = converter.md_to_docx(args.file, args.output)
            r = {"ok": result.get("success", False), **result}
    else:
        r = {"ok": False, "error": "未知命令"}

    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
