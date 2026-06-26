from __future__ import annotations

import re

from bs4 import BeautifulSoup

from .markdown_tools import normalize_code_blocks


def _normalize_lists(soup: BeautifulSoup) -> None:
    for list_node in soup.find_all(["ul", "ol"]):
        for child in list(list_node.contents):
            name = getattr(child, "name", None)
            if name == "li":
                continue
            text = str(child).strip() if not name else ""
            if text and text not in ("\n", "\r\n"):
                li = soup.new_tag("li")
                li.string = text
                child.replace_with(li)
            else:
                child.extract()

    for li in soup.find_all("li"):
        if not li.get_text(" ", strip=True):
            li.decompose()


def _enhance_reference_links(soup: BeautifulSoup) -> None:
    ref_keywords = ("参考资源", "相关链接", "references", "reference")
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        text = heading.get_text(" ", strip=True).lower()
        if not any(keyword in text for keyword in ref_keywords):
            continue

        level = int(heading.name[1])
        node = heading.next_sibling
        while node is not None:
            if getattr(node, "name", None) and re.match(r"^h[1-6]$", node.name):
                next_level = int(node.name[1])
                if next_level <= level:
                    break

            anchors = node.find_all("a") if getattr(node, "find_all", None) else []
            for anchor in anchors:
                href = (anchor.get("href") or "").strip()
                if not href:
                    continue
                parent_text = anchor.parent.get_text(" ", strip=True) if anchor.parent else ""
                if href in parent_text:
                    continue
                url_anchor = soup.new_tag("a", href=href)
                url_anchor["style"] = "color:#576b95;text-decoration:underline;word-break:break-all;"
                url_anchor["target"] = "_blank"
                url_anchor.string = href
                holder = soup.new_tag("span")
                holder["style"] = "display:block;margin-top:2px;font-size:13px;line-height:1.6;color:#7a7a7a;"
                holder.append(url_anchor)
                anchor.insert_after(holder)
            node = node.next_sibling


def _style_lead_paragraph(soup: BeautifulSoup, template: str) -> None:
    styles = {
        "standard": "margin:1em 0;padding:0.85em 0.96em;background:#fff7e6;border:1px solid #ffe1a6;border-radius:8px;line-height:1.9;font-size:16px;color:#2b2f38;",
        "business": "margin:1em 0;padding:0.86em 1em;background:#f5f8fb;border:1px solid #d8e3ef;border-radius:10px;line-height:1.92;font-size:16px;color:#213547;",
        "story": "margin:1em 0;padding:0.9em 1em;background:#fff8eb;border:1px solid #f5d9a8;border-radius:10px;line-height:1.92;font-size:16px;color:#3a2b18;",
    }
    for paragraph in soup.find_all("p"):
        if paragraph.find_parent(["li", "blockquote", "td", "th"]):
            continue
        if not paragraph.get_text(" ", strip=True):
            continue
        paragraph["style"] = styles.get(template, styles["standard"])
        break


def optimize_for_wechat_html(content_html: str, template: str = "standard") -> str:
    template = (template or "standard").strip().lower()
    soup = BeautifulSoup(content_html, "html.parser")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    _normalize_lists(soup)
    normalize_code_blocks(soup)
    _enhance_reference_links(soup)

    first_h1 = soup.find("h1")
    if first_h1:
        first_h1.decompose()

    heading_styles = {
        "standard": "margin:1.4em 0 0.7em;padding:0.38em 0.65em;font-size:1.18em;line-height:1.45;color:#1f2937;font-weight:700;background:#f5f8ff;border-left:4px solid #3b6dd8;border-radius:2px;",
        "business": "margin:1.45em 0 0.72em;padding:0.42em 0.72em;font-size:1.18em;line-height:1.45;color:#15324b;font-weight:800;background:#edf6ff;border-left:4px solid #0f6cbd;border-radius:4px;",
        "story": "margin:1.45em 0 0.72em;padding:0.44em 0.72em;font-size:1.18em;line-height:1.45;color:#6d3d14;font-weight:800;background:#fff3df;border-left:4px solid #f59e0b;border-radius:4px;",
    }
    paragraph_styles = {
        "standard": "margin:0.95em 0;line-height:1.92;font-size:16px;color:#2b2f38;text-align:justify;letter-spacing:0.01em;",
        "business": "margin:0.95em 0;line-height:1.92;font-size:16px;color:#25364a;text-align:justify;letter-spacing:0.01em;",
        "story": "margin:0.95em 0;line-height:1.94;font-size:16px;color:#3d342d;text-align:justify;letter-spacing:0.01em;",
    }
    list_styles = {
        "standard": "margin:0.95em 0;padding:0.75em 0.95em 0.75em 1.55em;line-height:1.8;color:#2f3441;background:#f8fafc;border-radius:6px;border:1px solid #edf2f7;list-style-position:outside;",
        "business": "margin:0.98em 0;padding:0.82em 1em 0.82em 1.62em;line-height:1.82;color:#24384d;background:#f5f9fd;border-radius:8px;border:1px solid #dce8f2;list-style-position:outside;",
        "story": "margin:0.98em 0;padding:0.82em 1em 0.82em 1.62em;line-height:1.84;color:#4a3c2e;background:#fffaf1;border-radius:8px;border:1px solid #f4dfb8;list-style-position:outside;",
    }
    blockquote_styles = {
        "standard": "margin:1.1em 0;padding:0.8em 1em;border-left:3px solid #7aa2ff;background:#f4f7ff;color:#43506a;line-height:1.8;border-radius:4px;",
        "business": "margin:1.1em 0;padding:0.84em 1em;border-left:3px solid #0f6cbd;background:#eff7fe;color:#284861;line-height:1.82;border-radius:4px;",
        "story": "margin:1.1em 0;padding:0.84em 1em;border-left:3px solid #f59e0b;background:#fff8ea;color:#6a5028;line-height:1.82;border-radius:4px;",
    }

    for heading in soup.find_all("h2"):
        heading["style"] = heading_styles.get(template, heading_styles["standard"])
    for heading in soup.find_all(["h3", "h4"]):
        heading["style"] = "margin:1.2em 0 0.55em;font-size:1.05em;line-height:1.5;color:#1f2937;font-weight:700;"
    for paragraph in soup.find_all("p"):
        paragraph["style"] = paragraph_styles.get(template, paragraph_styles["standard"])
    for ul in soup.find_all("ul"):
        ul["style"] = list_styles.get(template, list_styles["standard"]) + "list-style-type:disc;"
    for ol in soup.find_all("ol"):
        ol["style"] = list_styles.get(template, list_styles["standard"]) + "list-style-type:decimal;"
    for li in soup.find_all("li"):
        li["style"] = "margin:0.28em 0;font-size:16px;line-height:1.82;"
    for anchor in soup.find_all("a"):
        anchor["style"] = "color:#1f57c3;text-decoration:underline;word-break:break-all;"
        if anchor.get("href"):
            anchor["target"] = "_blank"
    for strong in soup.find_all("strong"):
        strong["style"] = "font-weight:700;color:#1f2937;"
    for quote in soup.find_all("blockquote"):
        quote["style"] = blockquote_styles.get(template, blockquote_styles["standard"])
    for pre in soup.find_all("pre"):
        pre["style"] = "margin:1em 0;padding:0.9em 1em;background:#101828;color:#f8fafc;border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.7;"
    for code in soup.find_all("code"):
        if code.find_parent("pre"):
            continue
        code["style"] = "padding:0.1em 0.3em;background:#f3f4f6;border-radius:4px;font-size:0.92em;"

    _style_lead_paragraph(soup, template)

    body_html = "".join(str(node) for node in soup.contents)
    return (
        "<section style=\"margin:0 auto;max-width:690px;padding:0;"
        "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
        "color:#1f2937;font-size:16px;line-height:1.9;\">"
        f"{body_html}"
        "</section>"
    )
