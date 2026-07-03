"""
output.py — SpecQ v2.0 多格式输出模块
Markdown → Word / PPT / Email / Chat 格式转换
"""
import warnings
from datetime import date


def format_output(markdown_text: str, output_format: str, metadata: dict | None = None) -> str:
    """
    多格式输出路由。

    Args:
        markdown_text: 八模块情报包 Markdown 原文
        output_format: markdown / docx / ppt / email / chat
        metadata: {"product": "..", "application": "..", "timestamp": ".."}

    Returns:
        格式化后的文本字符串
    """
    if not metadata:
        metadata = {}
    ts = metadata.get("timestamp", str(date.today()))

    if output_format == "markdown":
        return markdown_text

    elif output_format == "email":
        product = metadata.get("product", "电子化学品")
        app = metadata.get("application", "未知应用")
        subject = f"攻单情报包: {product} - {app}"
        body = _truncate(markdown_text, 2000)
        return (
            f"Subject: {subject}\n"
            f"Date: {ts}\n"
            f"To: 销售团队\n"
            f"\n"
            f"{body}\n"
            f"\n---\n"
            f"本情报由 SpecQ v2.0 自动生成"
        )

    elif output_format == "chat":
        return _truncate(markdown_text, 300)

    elif output_format == "docx":
        warnings.warn("docx 输出尚未实现完整 Word 文档生成，当前仅返回模板提示", FutureWarning, stacklevel=2)
        return (
            f"[Word 文档模板已就绪]\n"
            f"标题: {metadata.get('product', '')} 攻单情报包\n"
            f"日期: {ts}\n"
            f"格式: Microsoft Word (.docx)\n"
            f"说明: 请用 python-docx 库调用 Document() 生成正式文档，以下为 Markdown 原文供参考:\n"
            f"\n{_truncate(markdown_text, 1500)}"
        )

    elif output_format == "ppt":
        warnings.warn("ppt 输出尚未实现完整 PPT 生成，当前仅返回大纲提示", FutureWarning, stacklevel=2)
        # 提取 Markdown 标题行作为 PPT 大纲
        slides = _extract_headings(markdown_text)
        outline = "\n".join(f"  • Slide {i+1}: {h}" for i, h in enumerate(slides[:20]))
        return (
            f"[PPT 大纲已就绪]\n"
            f"标题: {metadata.get('product', '')} 攻单情报包\n"
            f"日期: {ts}\n"
            f"幻灯片数: {min(len(slides), 20)} 页\n"
            f"\n大纲:\n{outline}\n"
            f"\n说明: 请用 python-pptx 库调用 Presentation() 生成正式幻灯片。"
        )

    else:
        # 不支持的格式 → 降级为 markdown
        return markdown_text


def _truncate(text: str, max_chars: int) -> str:
    """截断文本到指定字符数，末尾加省略标记。"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n...（已截断，原文共 {len(text)} 字符）"


def _extract_headings(text: str) -> list[str]:
    """从 Markdown 中提取二级标题行。"""
    headings = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            headings.append(stripped[3:].strip())
    return headings
