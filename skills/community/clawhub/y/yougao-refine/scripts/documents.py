"""Convert Markdown to the public Yougao document schema; never execute raw HTML."""
from pathlib import Path
import sys
from urllib.parse import urlsplit

from yougao import APIError


def plain_document(text):
    return {"type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": line}]} if line else {"type": "paragraph"}
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]}


def markdown_document(text):
    if len(text.encode("utf-8")) > 512 * 1024:
        raise APIError("Markdown 超过稿件容量，请分成独立文章。")
    sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
    try:
        import mistune
    finally:
        sys.path.pop(0)
    if mistune.__version__ != "3.4.0":
        raise APIError("请使用本包自带的 Markdown 解析器，避免不同版本造成内容损失。")
    ast = mistune.create_markdown(renderer="ast", plugins=["table", "strikethrough"])(text)

    def safe_url(value, image=False):
        p = urlsplit(value)
        if p.username or p.password or any(c in value for c in "\r\n\t"):
            raise APIError("文章包含不支持的链接，请核对原文。")
        if (p.scheme in ("http", "https") and p.hostname) or (not image and p.scheme == "mailto"):
            return value
        raise APIError("文章含本地图片或不支持的链接，请先在优稿编辑器上传图片，或提供已有稿件 ID；不会丢弃图片。")

    def inlines(tokens, marks=None):
        out = []
        for t in tokens:
            kind, attrs = t["type"], t.get("attrs", {})
            if kind in ("text", "codespan", "softbreak"):
                value = t.get("raw", "\n" if kind == "softbreak" else "")
                if value:
                    node = {"type": "text", "text": value}
                    active = (marks or []) + ([{"type": "code"}] if kind == "codespan" else [])
                    if active:
                        node["marks"] = active
                    out.append(node)
            elif kind == "linebreak":
                out.append({"type": "hardBreak"})
            elif kind in ("strong", "emphasis", "strikethrough", "link"):
                mark = {"type": {"strong": "bold", "emphasis": "italic", "strikethrough": "strike", "link": "link"}[kind]}
                if kind == "link":
                    mark["attrs"] = {"href": safe_url(attrs["url"])}
                out.extend(inlines(t.get("children", []), (marks or []) + [mark]))
            elif kind == "image":
                alt = "".join(x.get("raw", "") for x in t.get("children", []))
                out.append({"type": "image", "attrs": {"src": safe_url(attrs["url"], True), "alt": alt, "title": attrs.get("title", "")}})
            else:
                raise APIError("Markdown 含暂不支持的内联结构（" + kind + "），请用已有稿件，不能自动丢弃内容。")
        return out

    def blocks(tokens):
        result = []
        for t in tokens:
            kind, attrs, children = t["type"], t.get("attrs", {}), t.get("children", [])
            if kind == "blank_line":
                continue
            if kind in ("paragraph", "block_text", "heading"):
                node = {"type": "heading" if kind == "heading" else "paragraph", "content": []}
                if kind == "heading":
                    node["attrs"] = {"level": attrs["level"]}
                for child in inlines(children):
                    if child["type"] == "image":
                        if node["content"]:
                            result.append(node)
                        result.append(child)
                        node = {"type": "paragraph", "content": []}
                    else:
                        node["content"].append(child)
                if node["content"]:
                    result.append(node)
            elif kind == "list":
                node = {"type": "orderedList" if attrs.get("ordered") else "bulletList", "content": blocks(children)}
                if attrs.get("ordered"):
                    node["attrs"] = {"start": attrs.get("start", 1)}
                result.append(node)
            elif kind in ("list_item", "block_quote"):
                result.append({"type": "listItem" if kind == "list_item" else "blockquote", "content": blocks(children)})
            elif kind == "block_code":
                node = {"type": "codeBlock", "content": [{"type": "text", "text": t.get("raw", "")} ]}
                if attrs.get("info"):
                    node["attrs"] = {"language": attrs["info"].split()[0]}
                result.append(node)
            elif kind == "thematic_break":
                result.append({"type": "horizontalRule"})
            elif kind == "table":
                rows = []
                for section in children:
                    entries = [section] if section["type"] == "table_head" else section.get("children", [])
                    for row in entries:
                        cells = []
                        for cell in row.get("children", []):
                            cell_type = "tableHeader" if cell.get("attrs", {}).get("head") else "tableCell"
                            content = inlines(cell.get("children", []))
                            if any(x["type"] == "image" for x in content):
                                raise APIError("表格内图片请通过已有图文稿件排版，不会自动丢弃图片。")
                            cells.append({"type": cell_type, "content": [{"type": "paragraph", "content": content}]})
                        rows.append({"type": "tableRow", "content": cells})
                result.append({"type": "table", "content": rows})
            else:
                raise APIError("Markdown 含暂不支持的结构（" + kind + "），请使用已有稿件；原文保持不动。")
        return result

    return {"type": "doc", "content": blocks(ast)}
