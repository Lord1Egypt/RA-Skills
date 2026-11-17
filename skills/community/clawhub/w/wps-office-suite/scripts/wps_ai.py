"""
AI 统一入口 v4.9.0
功能：统一 9 大 AI 功能入口，--action 路由到对应模块，集成 llm_bridge 统一模型层

死规则合规：
  - 规则4：禁止自动发布
  - 规则9：基础功能自研（规则引擎 + 模板匹配，无外部 API）
  - 规则10：性能优化（按需加载模块，不预加载）
  - 规则13：不生成禁止文件类型
  - 规则14：三轮自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭（llm_bridge 子进程）

安全合规：
  - auto 模式仅使用本地引擎，不读取外部凭证或 API Key
  - 外部 LLM/ASR 仅在用户显式指定 method 时调用
  - llm_bridge 通过白名单探测 + subprocess 调用 cn-llm-router
  - 未命中 cn-llm-router 时回落本地规则引擎 + 自配 API 降级链
"""
import json
import sys
import os
from pathlib import Path

__version__ = "4.8.0"

SCRIPT_DIR = Path(__file__).parent


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=f"WPS AI 统一入口 v{__version__} — 6 大 AI 功能统一路由"
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=[
            "email-reply",
            "report",
            "meeting",
            "translate",
            "formula",
            "continue",
            "rewrite",
            "expand",
        ],
        help="AI 功能动作",
    )

    # 通用参数
    parser.add_argument("--file", default="", help="输入文件路径")
    parser.add_argument("--output", default="", help="输出文件路径")
    parser.add_argument("--sheet", default="Sheet1", help="工作表名")
    parser.add_argument("--formula", default="", help="Excel 公式（formula 动作）")

    # 邮件回复参数
    parser.add_argument("--content", default="", help="邮件内容（email-reply 动作）")
    parser.add_argument(
        "--tone",
        default="friendly",
        choices=["friendly", "polite", "formal", "professional"],
        help="回复语气",
    )
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="语言")
    parser.add_argument("--context", default="", help="上下文/历史邮件")

    # 周报月报参数
    parser.add_argument(
        "--type",
        default="weekly",
        choices=["weekly", "monthly"],
        help="报告类型（report 动作）",
    )
    parser.add_argument("--points", default="", help="关键点（逗号分隔）")
    parser.add_argument("--title", default="", help="报告标题")
    parser.add_argument("--author", default="", help="作者")

    # 会议纪要参数
    parser.add_argument(
        "--method",
        default="auto",
        choices=["auto", "whisper-local", "azure-speech", "google-stt", "template"],
        help="ASR 方法（meeting 动作）",
    )
    parser.add_argument("--language", default="zh", help="语言代码")
    parser.add_argument(
        "--summary-method",
        default="auto",
        choices=["auto", "rule-engine", "external-llm", "pure-template"],
        help="摘要方法",
    )

    # 文档翻译参数
    parser.add_argument("--source", default="", help="源语言（translate 动作）")
    parser.add_argument("--target", default="zh", help="目标语言")

    # 公式解释参数
    parser.add_argument("--cell", default="", help="单元格地址（formula 动作）")

    # v4.9: 续写/改写/扩写参数
    parser.add_argument("--text", default="", help="输入文本（continue/rewrite/expand 动作）")
    parser.add_argument("--style", default="formal",
                        choices=["formal", "casual", "concise", "detailed", "polite", "professional"],
                        help="目标风格（rewrite 动作）")
    parser.add_argument("--aspect", default="details",
                        choices=["details", "examples", "background", "analysis"],
                        help="扩写方向（expand 动作）")
    # --context 已在 line 68 定义（email-reply 使用），此处不再重复

    args = parser.parse_args()

    result = {"ok": False, "error": "未知动作"}

    if args.action == "email-reply":
        result = _ai_email_reply(args)
    elif args.action == "report":
        result = _ai_report(args)
    elif args.action == "meeting":
        result = _ai_meeting(args)
    elif args.action == "translate":
        result = _ai_translate(args)
    elif args.action == "formula":
        result = _ai_formula(args)
    elif args.action == "continue":
        result = _ai_continue(args)
    elif args.action == "rewrite":
        result = _ai_rewrite(args)
    elif args.action == "expand":
        result = _ai_expand(args)

    print(json.dumps(result, ensure_ascii=False, default=str))


def _ai_email_reply(args) -> dict:
    """邮件智能回复"""
    try:
        from email_reply import EmailReplier
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from email_reply import EmailReplier

    replier = EmailReplier()
    return replier.reply(
        content=args.content,
        tone=args.tone,
        lang=args.lang,
        context=args.context,
        template_path=args.template or "",
    )


def _ai_report(args) -> dict:
    """周报/月报生成"""
    try:
        from report_generator import ReportGenerator
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from report_generator import ReportGenerator

    gen = ReportGenerator()
    output = args.output or f"./{args.type}_report.docx"
    points_list = [p.strip() for p in args.points.split(",") if p.strip()]

    if not points_list:
        return {"ok": False, "error": "请指定 --points（逗号分隔的关键点）"}

    return gen.generate(
        report_type=args.type,
        points=points_list,
        title=args.title or f"{'周' if args.type == 'weekly' else '月'}报",
        author=args.author,
        date="",
        template_path=args.template or "",
        output=output,
        tone="formal",
    )


def _ai_meeting(args) -> dict:
    """会议纪要"""
    try:
        from meeting_minutes import MeetingGenerator
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from meeting_minutes import MeetingGenerator

    gen = MeetingGenerator()
    return gen.generate(
        audio_path=args.file,
        output=args.output or "./meeting_minutes.docx",
        asr_method=args.method,
        summary_method=args.summary_method,
        language=args.language,
    )


def _ai_translate(args) -> dict:
    """文档翻译"""
    try:
        from document_translator import DocumentTranslator
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from document_translator import DocumentTranslator

    translator = DocumentTranslator()
    return translator.translate(
        filepath=args.file,
        output=args.output or "",
        source_lang=args.source,
        target_lang=args.target,
        method="auto",
    )


def _ai_formula(args) -> dict:
    """公式解释"""
    try:
        from formula_explainer import FormulaExplainer
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from formula_explainer import FormulaExplainer

    explainer = FormulaExplainer()

    if args.formula:
        return {
            "ok": True,
            "formula": args.formula,
            "explanation": explainer.explain(args.formula),
        }
    elif args.file and args.cell:
        return explainer.explain_cell(args.file, args.sheet, args.cell)
    elif args.file:
        results = explainer.explain_file(args.file, args.sheet)
        return {"ok": True, "count": len(results), "formulas": results}
    else:
        return {"ok": False, "error": "请指定 --formula 或 --file（可配合 --cell）"}


def _ai_continue(args) -> dict:
    """续写文本（v4.9 新增，通过 llm_bridge 走 cn-llm-router）"""
    try:
        from llm_bridge import continue_writing, INSTALL_HINT
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from llm_bridge import continue_writing, INSTALL_HINT

    if not args.text:
        return {"ok": False, "error": "请指定 --text（要续写的文本）"}

    result = continue_writing(
        text=args.text,
        context=args.context,
        timeout=30,
    )

    # 如果未命中 cn-llm-router，添加安装提示
    if result.get("source") == "fallback" and not result.get("ok"):
        result["install_hint"] = INSTALL_HINT
        result["message"] = "未检测到 cn-llm-router，已降级到本地规则引擎。安装后可零配置使用更多模型。"

    return result


def _ai_rewrite(args) -> dict:
    """改写文本（v4.9 新增，通过 llm_bridge 走 cn-llm-router）"""
    try:
        from llm_bridge import rewrite_text, INSTALL_HINT
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from llm_bridge import rewrite_text, INSTALL_HINT

    if not args.text:
        return {"ok": False, "error": "请指定 --text（要改写的文本）"}

    result = rewrite_text(
        text=args.text,
        style=args.style,
        timeout=30,
    )

    if result.get("source") == "fallback" and not result.get("ok"):
        result["install_hint"] = INSTALL_HINT
        result["message"] = "未检测到 cn-llm-router，已降级到本地规则引擎。安装后可零配置使用更多模型。"

    return result


def _ai_expand(args) -> dict:
    """扩写文本（v4.9 新增，通过 llm_bridge 走 cn-llm-router）"""
    try:
        from llm_bridge import expand_text, INSTALL_HINT
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from llm_bridge import expand_text, INSTALL_HINT

    if not args.text:
        return {"ok": False, "error": "请指定 --text（要扩写的文本）"}

    result = expand_text(
        text=args.text,
        aspect=args.aspect,
        timeout=30,
    )

    if result.get("source") == "fallback" and not result.get("ok"):
        result["install_hint"] = INSTALL_HINT
        result["message"] = "未检测到 cn-llm-router，已降级到本地规则引擎。安装后可零配置使用更多模型。"

    return result


if __name__ == "__main__":
    main()
