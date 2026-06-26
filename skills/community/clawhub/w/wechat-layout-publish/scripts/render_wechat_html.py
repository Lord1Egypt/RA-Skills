#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


ALERT_META = {
    "note": {"label": "Note", "icon": "i"},
    "tip": {"label": "Tip", "icon": "!"}, 
    "info": {"label": "Info", "icon": "i"},
    "important": {"label": "Important", "icon": "!"},
    "warning": {"label": "Warning", "icon": "!"},
    "caution": {"label": "Caution", "icon": "!"},
}


def style_str(style: Dict[str, str]) -> str:
    return ";".join(f"{k}:{v}" for k, v in style.items() if v)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def load_theme(theme_id: str) -> Dict:
    skill_dir = Path(__file__).resolve().parent.parent
    theme_pack_path = skill_dir / "assets" / "theme-pack.json"
    theme_pack = json.loads(theme_pack_path.read_text(encoding="utf-8"))
    themes = {theme["id"]: theme for theme in theme_pack["themes"]}
    if theme_id not in themes:
        raise SystemExit(f"Unknown theme id: {theme_id}")
    return themes[theme_id]


def make_state(footnotes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    return {
        "footnote_defs": footnotes or {},
        "footnote_order": [],
        "footnote_index_map": {},
    }


def register_footnote_ref(fn_id: str, state: Dict[str, Any]) -> int:
    if fn_id not in state["footnote_index_map"]:
        index = len(state["footnote_order"]) + 1
        state["footnote_index_map"][fn_id] = index
        state["footnote_order"].append(fn_id)
    return state["footnote_index_map"][fn_id]


def extract_footnote_defs(markdown: str) -> Tuple[str, Dict[str, str]]:
    lines = markdown.splitlines()
    defs: Dict[str, str] = {}
    kept: List[str] = []
    i = 0
    while i < len(lines):
        match = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", lines[i])
        if not match:
            kept.append(lines[i])
            i += 1
            continue
        fn_id = match.group(1).strip()
        content_lines = [match.group(2).strip()]
        i += 1
        while i < len(lines):
            line = lines[i]
            if line.startswith("    ") or line.startswith("\t"):
                content_lines.append(line.strip())
                i += 1
                continue
            if not line.strip():
                content_lines.append("")
                i += 1
                continue
            break
        defs[fn_id] = " ".join(part for part in content_lines if part).strip()
    cleaned = "\n".join(kept).strip()
    return (cleaned + "\n") if cleaned else "", defs


def parse_inline(text: str, theme: Dict, state: Dict[str, Any]) -> str:
    placeholders: List[str] = []

    def stash(match: re.Match) -> str:
        code = escape(match.group(1))
        rendered = (
            f"<code class=\"code-inline\" style=\"{style_str(code_inline_style(theme))}\">{code}</code>"
        )
        placeholders.append(rendered)
        return f"@@PH{len(placeholders) - 1}@@"

    def stash_raw(rendered: str) -> str:
        placeholders.append(rendered)
        return f"@@PH{len(placeholders) - 1}@@"

    def ruby_repl(match: re.Match) -> str:
        base = match.group(1).strip()
        ruby = match.group(2).strip()
        return stash_raw(render_ruby(base, ruby, theme))

    text = re.sub(r"`([^`]+)`", stash, text)
    text = re.sub(r"\[([^\]]+)\]\{([^}]+)\}", ruby_repl, text)
    text = re.sub(r"\[([^\]]+)\]\^\(([^)]+)\)", ruby_repl, text)
    text = escape(text)
    text = re.sub(
        r"\[\^([^\]]+)\]",
        lambda m: render_footnote_ref(m.group(1), theme, state),
        text,
    )
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: render_image(m.group(2), m.group(1), theme),
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: (
            f"<a href=\"{escape(m.group(2))}\" "
            f"style=\"{style_str(link_style(theme))}\">{m.group(1)}</a>"
        ),
        text,
    )
    text = re.sub(
        r"==(.+?)==",
        lambda m: f"<span class=\"markup-highlight\" style=\"{style_str(markup_highlight_style(theme))}\">{m.group(1)}</span>",
        text,
    )
    text = re.sub(
        r"\+\+(.+?)\+\+",
        lambda m: f"<span class=\"markup-underline\" style=\"{style_str(markup_underline_style(theme))}\">{m.group(1)}</span>",
        text,
    )
    text = re.sub(
        r"(?<!~)~([^~\n]+)~(?!~)",
        lambda m: f"<span class=\"markup-wavyline\" style=\"{style_str(markup_wavyline_style(theme))}\">{m.group(1)}</span>",
        text,
    )
    text = re.sub(
        r"\$\$([^$]+)\$\$",
        lambda m: f"<span class=\"katex-inline\" style=\"{style_str(katex_inline_style(theme))}\">{m.group(1).strip()}</span>",
        text,
    )
    text = re.sub(
        r"\\\((.+?)\\\)",
        lambda m: f"<span class=\"katex-inline\" style=\"{style_str(katex_inline_style(theme))}\">{m.group(1).strip()}</span>",
        text,
    )
    text = re.sub(
        r"(?<!\$)\$((?:\\.|[^\\\n$])+?)\$(?!\$)",
        lambda m: f"<span class=\"katex-inline\" style=\"{style_str(katex_inline_style(theme))}\">{m.group(1).strip()}</span>",
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", text)
    text = re.sub(r"<strong>(.*?)</strong>", lambda m: f"<strong style=\"{style_str(strong_style(theme))}\">{m.group(1)}</strong>", text)
    text = re.sub(r"<em>(.*?)</em>", lambda m: f"<em style=\"{style_str(em_style(theme))}\">{m.group(1)}</em>", text)
    text = re.sub(r"<del>(.*?)</del>", lambda m: f"<del style=\"{style_str(del_style(theme))}\">{m.group(1)}</del>", text)

    for idx, rendered in enumerate(placeholders):
        text = text.replace(f"@@PH{idx}@@", rendered)
    return text


def render_image(src: str, alt: str, theme: Dict) -> str:
    palette = theme["palette"]
    img_style = style_str(
        {
            "display": "block",
            "max-width": "100%",
            "height": "auto",
            "margin": "16px auto",
            "border-radius": "10px",
            "border": f"1px solid {palette['border']}",
        }
    )
    figure_style = style_str({"margin": "18px 0", "text-align": "center"})
    caption_style = style_str(
        {
            "margin": "8px 0 0",
            "font-size": "13px",
            "color": palette["muted"],
            "line-height": "1.6",
        }
    )
    image_html = f"<img src=\"{escape(src)}\" alt=\"{escape(alt)}\" style=\"{img_style}\" />"
    if not alt:
        return image_html
    return (
        f"<figure style=\"{figure_style}\">"
        f"{image_html}"
        f"<figcaption style=\"{caption_style}\">{escape(alt)}</figcaption>"
        f"</figure>"
    )


def code_inline_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "background": palette["codeBg"],
        "color": palette["text"],
        "padding": "2px 6px",
        "border-radius": "4px",
        "font-family": "Menlo, Monaco, Consolas, monospace",
        "font-size": "0.92em",
    }


def strong_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "color": palette["primary"],
        "font-weight": "700",
    }


def em_style(theme: Dict) -> Dict[str, str]:
    return {
        "font-style": "italic",
    }


def del_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "color": palette["muted"],
        "text-decoration": "line-through",
    }


def markup_highlight_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "background": palette["secondary"],
        "color": palette["text"],
        "padding": "0 4px",
        "border-radius": "4px",
    }


def markup_underline_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "text-decoration": "underline 2px",
        "text-decoration-color": palette["primary"],
    }


def markup_wavyline_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "text-decoration": "underline wavy",
        "text-decoration-color": palette["primary"],
    }


def katex_inline_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "display": "inline-block",
        "padding": "0 4px",
        "color": palette["primary"],
        "font-style": "italic",
        "background": palette["panel"],
        "border-radius": "4px",
    }


def katex_block_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "display": "block",
        "margin": "18px 0",
        "padding": "14px 16px",
        "background": palette["panel"],
        "color": palette["primary"],
        "border": f"1px solid {palette['border']}",
        "border-radius": "12px",
        "overflow-x": "auto",
        "text-align": "center",
        "font-style": "italic",
    }


def ruby_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "ruby-align": "center",
        "color": palette["text"],
    }


def footnote_ref_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "color": palette["primary"],
        "text-decoration": "none",
        "font-size": "12px",
    }


def render_footnote_ref(fn_id: str, theme: Dict, state: Dict[str, Any]) -> str:
    if fn_id not in state["footnote_defs"]:
        return f"[^{escape(fn_id)}]"
    index = register_footnote_ref(fn_id, state)
    return (
        f"<sup style=\"{style_str({'color': theme['palette']['primary']})}\">"
        f"<a href=\"#fnDef-{escape(fn_id)}\" id=\"fnRef-{escape(fn_id)}\" "
        f"style=\"{style_str(footnote_ref_style(theme))}\">[{index}]</a>"
        f"</sup>"
    )


def render_ruby(base: str, ruby: str, theme: Dict) -> str:
    if any(separator in ruby for separator in ("・", "．", "。", "-")):
        parts = [part.strip() for part in re.split(r"[・．。-]", ruby) if part.strip()]
        chars = list(base)
        if parts and chars:
            rendered_parts: List[str] = []
            char_index = 0
            for part_index, part in enumerate(parts):
                remaining_chars = len(chars) - char_index
                remaining_parts = len(parts) - part_index
                char_count = remaining_chars if remaining_parts == 1 else max(1, remaining_chars - remaining_parts + 1)
                current_text = "".join(chars[char_index : char_index + char_count])
                if current_text:
                    rendered_parts.append(
                        f"<ruby style=\"{style_str(ruby_style(theme))}\" data-text=\"{escape(current_text)}\" data-ruby=\"{escape(part)}\">"
                        f"{escape(current_text)}<rp>(</rp><rt>{escape(part)}</rt><rp>)</rp></ruby>"
                    )
                char_index += char_count
            if char_index < len(chars):
                rendered_parts.append(escape("".join(chars[char_index:])))
            return "".join(rendered_parts)
    return (
        f"<ruby style=\"{style_str(ruby_style(theme))}\" data-text=\"{escape(base)}\" data-ruby=\"{escape(ruby)}\">"
        f"{escape(base)}<rp>(</rp><rt>{escape(ruby)}</rt><rp>)</rp></ruby>"
    )


def link_style(theme: Dict) -> Dict[str, str]:
    palette = theme["palette"]
    return {
        "color": palette["link"],
        "text-decoration": "none",
        "border-bottom": f"1px solid {palette['link']}",
    }


def parse_blocks(markdown: str, state: Optional[Dict[str, Any]] = None) -> List[Dict]:
    state = state or make_state()
    lines = markdown.splitlines()
    blocks: List[Dict] = []
    i = 0

    def list_match(line: str) -> Optional[re.Match]:
        return re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)

    def is_list_line(line: str) -> bool:
        return bool(list_match(line))

    def is_table_sep(line: str) -> bool:
        stripped = line.strip()
        if "|" not in stripped:
            return False
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            return False
        return all(bool(re.fullmatch(r":?-{1,}:?", cell)) for cell in cells)

    def parse_table_alignments(line: str) -> List[str]:
        alignments: List[str] = []
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        for cell in cells:
            if cell.startswith(":") and cell.endswith(":"):
                alignments.append("center")
            elif cell.endswith(":"):
                alignments.append("right")
            else:
                alignments.append("left")
        return alignments

    def parse_list(start: int) -> Tuple[Dict[str, Any], int]:
        first = list_match(lines[start])
        assert first is not None
        base_indent = len(first.group(1).replace("\t", "    "))
        ordered = bool(re.match(r"^\d+\.$", first.group(2)))
        items: List[Dict[str, Any]] = []
        j = start
        while j < len(lines):
            current = list_match(lines[j])
            if not current:
                break
            indent = len(current.group(1).replace("\t", "    "))
            current_ordered = bool(re.match(r"^\d+\.$", current.group(2)))
            if indent != base_indent or current_ordered != ordered:
                break
            item_text = current.group(3).strip()
            checked: Optional[bool] = None
            task_match = re.match(r"^\[( |x|X)\]\s+(.*)$", item_text)
            if task_match:
                checked = task_match.group(1).lower() == "x"
                item_text = task_match.group(2).strip()
            j += 1
            child_lines: List[str] = []
            while j < len(lines):
                nxt = lines[j]
                nxt_match = list_match(nxt)
                nxt_indent = len((nxt_match.group(1) if nxt_match else "").replace("\t", "    ")) if nxt_match else -1
                raw_indent = len(nxt) - len(nxt.lstrip(" \t"))
                if nxt_match and nxt_indent == base_indent:
                    break
                if nxt.strip() == "":
                    child_lines.append("")
                    j += 1
                    continue
                if nxt_match and nxt_indent < base_indent:
                    break
                if not nxt_match and raw_indent <= base_indent:
                    break
                if len(nxt) > base_indent + 1:
                    child_lines.append(nxt[base_indent + 2 :] if nxt.startswith(" " * (base_indent + 2)) else nxt.lstrip())
                else:
                    child_lines.append(nxt.lstrip())
                j += 1
            children = parse_blocks("\n".join(child_lines), state) if any(line.strip() for line in child_lines) else []
            items.append({"text": item_text, "checked": checked, "children": children})
        return {"type": "list", "ordered": ordered, "items": items}, j

    def parse_alert_content(content_lines: List[str]) -> Optional[Dict[str, Any]]:
        if not content_lines:
            return None
        first_line = content_lines[0].strip()
        match = re.match(r"^\[!(NOTE|TIP|INFO|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", first_line, re.I)
        if not match:
            return None
        variant = match.group(1).lower()
        title = match.group(2).strip() or ALERT_META[variant]["label"]
        remainder = content_lines[1:]
        return {
            "type": "alert",
            "variant": variant,
            "title": title,
            "blocks": parse_blocks("\n".join(remainder), state) if remainder else [],
        }

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        container_match = re.match(r"^:::\s*(\w+)\s*$", line.strip())
        if container_match:
            variant = container_match.group(1).lower()
            if variant in ALERT_META:
                i += 1
                content_lines = []
                while i < len(lines) and lines[i].strip() != ":::": 
                    content_lines.append(lines[i])
                    i += 1
                if i < len(lines) and lines[i].strip() == ":::":
                    i += 1
                blocks.append(
                    {
                        "type": "alert",
                        "variant": variant,
                        "title": ALERT_META[variant]["label"],
                        "blocks": parse_blocks("\n".join(content_lines), state),
                    }
                )
                continue

        fence_match = re.match(r"^(`{3,}|~{3,})(.*)$", line)
        if fence_match:
            fence = fence_match.group(1)
            lang = fence_match.group(2).strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].startswith(fence):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(code_lines)})
            continue

        slider_match = re.match(r"^<((?:!\[[^\]]*\]\([^)]+\))(?:,!\[[^\]]*\]\([^)]+\))*)>$", line.strip())
        if slider_match:
            image_specs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", slider_match.group(1))
            if image_specs:
                blocks.append(
                    {
                        "type": "slider",
                        "images": [{"alt": alt.strip(), "src": src.strip()} for alt, src in image_specs],
                    }
                )
                i += 1
                continue

        if line.strip() == "$$":
            i += 1
            math_lines = []
            while i < len(lines) and lines[i].strip() != "$$":
                math_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append({"type": "math", "text": "\n".join(math_lines).strip()})
            continue

        if line.strip() == r"\[":
            i += 1
            math_lines = []
            while i < len(lines) and lines[i].strip() != r"\]":
                math_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append({"type": "math", "text": "\n".join(math_lines).strip()})
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            blocks.append(
                {
                    "type": "heading",
                    "level": len(heading_match.group(1)),
                    "text": heading_match.group(2).strip(),
                }
            )
            i += 1
            continue

        if re.match(r"^\s*([-*_])(?:\s*\1){2,}\s*$", line):
            blocks.append({"type": "hr"})
            i += 1
            continue

        if line.lstrip().startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            alert_block = parse_alert_content(quote_lines)
            if alert_block:
                blocks.append(alert_block)
            else:
                blocks.append({"type": "blockquote", "blocks": parse_blocks("\n".join(quote_lines), state)})
            continue

        if i + 1 < len(lines) and "|" in line and is_table_sep(lines[i + 1]):
            header = [cell.strip() for cell in line.strip().strip("|").split("|")]
            alignments = parse_table_alignments(lines[i + 1])
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i].strip():
                rows.append([cell.strip() for cell in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append({"type": "table", "header": header, "rows": rows, "alignments": alignments})
            continue

        if is_list_line(line):
            list_block, i = parse_list(i)
            blocks.append(list_block)
            continue

        paragraph_lines = [line.strip()]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if (
                not next_line.strip()
                or re.match(r"^(`{3,}|~{3,})", next_line)
                or re.match(r"^(#{1,6})\s+", next_line)
                or next_line.lstrip().startswith(">")
                or is_list_line(next_line)
                or re.match(r"^\s*([-*_])(?:\s*\1){2,}\s*$", next_line)
                or re.match(r"^<((?:!\[[^\]]*\]\([^)]+\))(?:,!\[[^\]]*\]\([^)]+\))*)>$", next_line.strip())
                or (i + 1 < len(lines) and "|" in next_line and is_table_sep(lines[i + 1]))
            ):
                break
            paragraph_lines.append(next_line.strip())
            i += 1
        blocks.append({"type": "paragraph", "text": " ".join(paragraph_lines)})

    return blocks


def render_heading(text: str, level: int, theme: Dict, h2_index: int, state: Dict[str, Any]) -> str:
    palette = theme["palette"]
    variant = theme["variants"]["h2"] if level == 2 else theme["variants"]["h1"] if level == 1 else "left-bar"
    accent_color = palette["link"] if theme["variants"]["h1"] == "dark-banner" else palette["primary"]
    content = parse_inline(text, theme, state)
    if level == 1:
        if variant == "banner":
            style = {
                "background": f"linear-gradient(90deg, {palette['primary']}, {palette['secondary']})",
                "color": "#ffffff",
                "padding": "12px 18px",
                "border-radius": "14px",
                "font-size": "28px",
                "font-weight": "700",
                "text-align": "center",
                "margin": "8px auto 24px",
            }
        elif variant == "dark-banner":
            style = {
                "background": palette["primary"],
                "color": "#ffffff",
                "padding": "14px 18px",
                "border-radius": "14px",
                "font-size": "28px",
                "font-weight": "700",
                "text-align": "center",
                "margin": "8px auto 24px",
            }
        elif variant == "ribbon":
            style = {
                "background": palette["secondary"],
                "color": palette["primary"],
                "padding": "10px 18px",
                "border-radius": "999px",
                "font-size": "28px",
                "font-weight": "700",
                "text-align": "center",
                "margin": "8px auto 24px",
                "border": f"1px solid {palette['border']}",
            }
        elif variant == "plain-large":
            style = {
                "color": palette["primary"],
                "font-size": "30px",
                "font-weight": "700",
                "text-align": "center",
                "margin": "8px auto 24px",
            }
        else:
            style = {
                "background": palette["panel"],
                "color": palette["primary"],
                "padding": "12px 18px",
                "border-radius": "12px",
                "font-size": "28px",
                "font-weight": "700",
                "text-align": "center",
                "margin": "8px auto 24px",
                "border": f"1px solid {palette['border']}",
            }
        return f"<h1 style=\"{style_str(style)}\">{content}</h1>"

    if level == 2:
        if variant == "filled-label":
            style = {
                "display": "inline-block",
                "background": palette["primary"],
                "color": "#ffffff",
                "padding": "6px 14px",
                "border-radius": "999px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "28px 0 16px",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "pill":
            style = {
                "display": "inline-block",
                "background": palette["secondary"],
                "color": palette["primary"],
                "padding": "6px 14px",
                "border-radius": "999px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "28px 0 16px",
                "border": f"1px solid {palette['border']}",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "left-pill":
            style = {
                "display": "inline-block",
                "background": palette["panel"],
                "color": palette["primary"],
                "padding": "6px 14px",
                "border-left": f"6px solid {palette['primary']}",
                "border-radius": "999px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "28px 0 16px",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "outline-band":
            style = {
                "display": "block",
                "color": palette["primary"],
                "padding": "8px 0 10px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "30px 0 16px",
                "border-top": f"1px solid {palette['border']}",
                "border-bottom": f"1px solid {palette['border']}",
                "text-align": "center",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "section-line":
            style = {
                "color": palette["primary"],
                "padding": "0 0 8px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "30px 0 16px",
                "border-bottom": f"2px solid {palette['primary']}",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "double-line":
            style = {
                "color": palette["primary"],
                "padding": "10px 0",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "30px 0 16px",
                "border-top": f"1px solid {palette['border']}",
                "border-bottom": f"1px solid {palette['border']}",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "numbered-section":
            wrapper = {
                "margin": "30px 0 16px",
                "text-align": "center",
            }
            prefix = {
                "display": "block",
                "color": palette["primary"],
                "font-size": "13px",
                "font-weight": "600",
                "letter-spacing": "0.04em",
                "margin-bottom": "8px",
            }
            heading = {
                "display": "inline-block",
                "color": palette["primary"],
                "font-size": "22px",
                "font-weight": "700",
                "padding": "0 6px",
                "margin": "0",
            }
            part_text = f"Part.{h2_index:02d}"
            return (
                f"<div style=\"{style_str(wrapper)}\">"
                f"<span style=\"{style_str(prefix)}\">{part_text}</span>"
                f"<h2 style=\"{style_str(heading)}\">{content}</h2>"
                f"</div>"
            )
        if variant == "tech-chip":
            style = {
                "display": "inline-block",
                "background": palette["secondary"],
                "color": palette["link"],
                "padding": "6px 12px",
                "border-radius": "8px",
                "font-size": "22px",
                "font-weight": "700",
                "margin": "28px 0 16px",
                "border": f"1px solid {palette['border']}",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"
        if variant == "underline":
            style = {
                "color": palette["primary"],
                "font-size": "22px",
                "font-weight": "700",
                "margin": "30px 0 16px",
                "padding-bottom": "6px",
                "border-bottom": f"2px solid {palette['primary']}",
            }
            return f"<h2 style=\"{style_str(style)}\">{content}</h2>"

    h_style = {
        "color": accent_color,
        "font-size": "20px" if level == 3 else "18px" if level == 4 else "16px",
        "font-weight": "700",
        "margin": "24px 0 12px",
        "padding-left": "10px" if level == 3 else "0",
        "border-left": f"4px solid {accent_color}" if level == 3 else "none",
    }
    tag = f"h{level}"
    return f"<{tag} style=\"{style_str(h_style)}\">{content}</{tag}>"


def render_blockquote(inner_html: str, theme: Dict) -> str:
    palette = theme["palette"]
    variant = theme["variants"]["blockquote"]
    if variant == "dark-panel":
        style = {
            "margin": "18px 0",
            "padding": "14px 16px",
            "background": palette["panel"],
            "color": palette["text"],
            "border-left": f"4px solid {palette['quoteBorder']}",
            "border-radius": "10px",
        }
    elif variant == "accent-panel":
        style = {
            "margin": "18px 0",
            "padding": "14px 16px",
            "background": palette["quoteBg"],
            "border": f"1px solid {palette['border']}",
            "border-left": f"4px solid {palette['quoteBorder']}",
            "border-radius": "12px",
        }
    elif variant == "soft-panel":
        style = {
            "margin": "18px 0",
            "padding": "14px 16px",
            "background": palette["quoteBg"],
            "border-left": f"4px solid {palette['quoteBorder']}",
            "border-radius": "10px",
        }
    else:
        style = {
            "margin": "18px 0",
            "padding": "4px 0 4px 14px",
            "border-left": f"4px solid {palette['quoteBorder']}",
            "color": palette["muted"],
        }
    return f"<blockquote style=\"{style_str(style)}\">{inner_html}</blockquote>"


def alert_palette(theme: Dict, variant: str) -> Dict[str, str]:
    palette = theme["palette"]
    base = {
        "note": {"bg": palette["quoteBg"], "border": palette["primary"], "text": palette["primary"]},
        "tip": {"bg": palette["secondary"], "border": palette["primary"], "text": palette["primary"]},
        "info": {"bg": palette["panel"], "border": palette["link"], "text": palette["link"]},
        "important": {"bg": palette["quoteBg"], "border": "#7c3aed", "text": "#7c3aed"},
        "warning": {"bg": "#fff7ed", "border": "#ea580c", "text": "#c2410c"},
        "caution": {"bg": "#fef2f2", "border": "#dc2626", "text": "#b91c1c"},
    }
    return base.get(variant, base["note"])


def render_alert(block: Dict[str, Any], theme: Dict, state: Dict[str, Any]) -> str:
    colors = alert_palette(theme, block["variant"])
    wrap_style = {
        "margin": "18px 0",
        "padding": "14px 16px",
        "background": colors["bg"],
        "border-left": f"4px solid {colors['border']}",
        "border-radius": "12px",
    }
    title_style = {
        "margin": "0 0 10px",
        "color": colors["text"],
        "font-size": "14px",
        "font-weight": "700",
        "display": "flex",
        "align-items": "center",
        "gap": "8px",
    }
    icon_style = {
        "display": "inline-flex",
        "align-items": "center",
        "justify-content": "center",
        "width": "18px",
        "height": "18px",
        "border-radius": "999px",
        "background": colors["border"],
        "color": "#ffffff",
        "font-size": "12px",
        "line-height": "1",
        "font-weight": "700",
    }
    icon = ALERT_META.get(block["variant"], ALERT_META["note"])["icon"]
    inner_html = render_blocks(block["blocks"], theme, state)
    return (
        f"<blockquote class=\"markdown-alert markdown-alert-{block['variant']}\" style=\"{style_str(wrap_style)}\">"
        f"<p class=\"alert-title-{block['variant']}\" style=\"{style_str(title_style)}\">"
        f"<span class=\"alert-icon-{block['variant']}\" style=\"{style_str(icon_style)}\">{escape(icon)}</span>"
        f"{escape(block['title'])}</p>"
        f"{inner_html}</blockquote>"
    )


def render_list(block: Dict[str, Any], theme: Dict, state: Dict[str, Any]) -> str:
    palette = theme["palette"]
    tag = "ol" if block["ordered"] else "ul"
    list_style = {
        "margin": "0 0 16px 22px",
        "padding": "0",
        "color": palette["text"],
    }
    item_style = {
        "margin": "8px 0",
        "line-height": "1.8",
    }
    rendered_items = []
    for item in block["items"]:
        prefix = ""
        if item["checked"] is not None:
            box_style = {
                "display": "inline-block",
                "width": "16px",
                "height": "16px",
                "margin-right": "8px",
                "border": f"1px solid {palette['border']}",
                "border-radius": "4px",
                "background": palette["primary"] if item["checked"] else "#ffffff",
                "color": "#ffffff",
                "text-align": "center",
                "font-size": "12px",
                "line-height": "16px",
                "vertical-align": "middle",
            }
            prefix = f"<span aria-hidden=\"true\" style=\"{style_str(box_style)}\">{'✓' if item['checked'] else ''}</span>"
        text_html = parse_inline(item["text"], theme, state)
        children_html = render_blocks(item["children"], theme, state) if item["children"] else ""
        rendered_items.append(
            f"<li style=\"{style_str(item_style)}\">{prefix}{text_html}{children_html}</li>"
        )
    return f"<{tag} style=\"{style_str(list_style)}\">{''.join(rendered_items)}</{tag}>"


def render_slider(block: Dict[str, Any], theme: Dict) -> str:
    palette = theme["palette"]
    outer_style = {
        "margin": "22px 0",
        "padding": "14px 12px 10px",
        "background": palette["panel"],
        "border": f"1px solid {palette['border']}",
        "border-radius": "14px",
    }
    track_style = {
        "overflow-x": "auto",
        "white-space": "nowrap",
        "-webkit-overflow-scrolling": "touch",
    }
    item_style = {
        "display": "inline-block",
        "width": "78%",
        "margin-right": "12px",
        "vertical-align": "top",
        "white-space": "normal",
    }
    image_style = {
        "display": "block",
        "width": "100%",
        "height": "auto",
        "border-radius": "10px",
        "border": f"1px solid {palette['border']}",
    }
    caption_style = {
        "margin": "8px 0 0",
        "font-size": "13px",
        "line-height": "1.6",
        "color": palette["muted"],
        "text-align": "center",
    }
    hint_style = {
        "margin": "10px 0 0",
        "font-size": "12px",
        "color": palette["muted"],
        "text-align": "center",
    }
    items_html = []
    for image in block["images"]:
        caption = f"<p style=\"{style_str(caption_style)}\">{escape(image['alt'])}</p>" if image["alt"] else ""
        items_html.append(
            f"<section style=\"{style_str(item_style)}\">"
            f"<img src=\"{escape(image['src'])}\" alt=\"{escape(image['alt'])}\" style=\"{style_str(image_style)}\" />"
            f"{caption}</section>"
        )
    return (
        f"<section data-role=\"image-slider\" style=\"{style_str(outer_style)}\">"
        f"<section style=\"{style_str(track_style)}\">{''.join(items_html)}</section>"
        f"<p style=\"{style_str(hint_style)}\">左右滑动查看组图</p>"
        f"</section>"
    )


def render_footnotes(theme: Dict, state: Dict[str, Any]) -> str:
    if not state["footnote_order"]:
        return ""
    palette = theme["palette"]
    title = f"<h4 style=\"color:{palette['primary']};font-size:18px;font-weight:700;margin:28px 0 12px\">引用链接</h4>"
    item_lines = []
    for fn_id in state["footnote_order"]:
        index = state["footnote_index_map"][fn_id]
        text = state["footnote_defs"].get(fn_id, "")
        line = (
            f"<code style=\"font-size:90%;opacity:0.6;\">[{index}]</code> "
            f"<span>{parse_inline(text, theme, state)}</span> "
            f"<a id=\"fnDef-{escape(fn_id)}\" href=\"#fnRef-{escape(fn_id)}\" style=\"color:{palette['primary']};text-decoration:none\">↩</a><br/>"
        )
        item_lines.append(line)
    p_style = {
        "font-size": "80%",
        "margin": "0.5em 8px",
        "word-break": "break-all",
        "color": palette["muted"],
    }
    return title + f"<p class=\"footnotes\" style=\"{style_str(p_style)}\">{''.join(item_lines)}</p>"


def render_blocks(blocks: List[Dict], theme: Dict, state: Optional[Dict[str, Any]] = None) -> str:
    state = state or make_state()
    palette = theme["palette"]
    accent_color = palette["link"] if theme["variants"]["h1"] == "dark-banner" else palette["primary"]
    rendered: List[str] = []
    h2_index = 0
    for block in blocks:
        if block["type"] == "heading":
            if block["level"] == 2:
                h2_index += 1
            rendered.append(render_heading(block["text"], block["level"], theme, h2_index, state))
        elif block["type"] == "paragraph":
            style = {
                "margin": "0 0 16px",
                "font-size": "16px",
                "line-height": "1.85",
                "color": palette["text"],
                "word-break": "break-word",
            }
            rendered.append(
                f"<p style=\"{style_str(style)}\">{parse_inline(block['text'], theme, state)}</p>"
            )
        elif block["type"] == "list":
            rendered.append(render_list(block, theme, state))
        elif block["type"] == "blockquote":
            rendered.append(render_blockquote(render_blocks(block["blocks"], theme, state), theme))
        elif block["type"] == "alert":
            rendered.append(render_alert(block, theme, state))
        elif block["type"] == "code":
            pre_style = {
                "margin": "18px 0",
                "padding": "14px 16px",
                "background": palette["codeBg"],
                "color": palette["text"],
                "border-radius": "12px",
                "overflow-x": "auto",
                "font-family": "Menlo, Monaco, Consolas, monospace",
                "font-size": "13px",
                "line-height": "1.7",
            }
            language_badge = ""
            if block["lang"]:
                language_badge = (
                    f"<div style=\"margin:0 0 8px;color:{palette['muted']};font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em\">"
                    f"{escape(block['lang'])}</div>"
                )
            rendered.append(
                f"<pre class=\"code-block\" style=\"{style_str(pre_style)}\">{language_badge}<code>{escape(block['text'])}</code></pre>"
            )
        elif block["type"] == "slider":
            rendered.append(render_slider(block, theme))
        elif block["type"] == "math":
            rendered.append(
                f"<div class=\"katex-block\" style=\"{style_str(katex_block_style(theme))}\">{escape(block['text'])}</div>"
            )
        elif block["type"] == "table":
            table_style = {
                "width": "100%",
                "border-collapse": "collapse",
                "margin": "18px 0",
                "font-size": "14px",
                "line-height": "1.7",
            }
            th_style = {
                "border": f"1px solid {palette['border']}",
                "padding": "8px 10px",
                "background": palette["panel"],
                "color": accent_color,
                "font-weight": "700",
                "text-align": "left",
            }
            td_style = {
                "border": f"1px solid {palette['border']}",
                "padding": "8px 10px",
                "color": palette["text"],
                "vertical-align": "top",
            }
            header_html = "".join(
                f"<th style=\"{style_str({**th_style, 'text-align': block['alignments'][idx] if idx < len(block['alignments']) else 'left'})}\">{parse_inline(cell, theme, state)}</th>"
                for idx, cell in enumerate(block["header"])
            )
            rows_html = "".join(
                "<tr>"
                + "".join(
                    f"<td style=\"{style_str({**td_style, 'text-align': block['alignments'][idx] if idx < len(block['alignments']) else 'left'})}\">{parse_inline(cell, theme, state)}</td>"
                    for idx, cell in enumerate(row)
                )
                + "</tr>"
                for row in block["rows"]
            )
            rendered.append(
                f"<table style=\"{style_str(table_style)}\"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>"
            )
        elif block["type"] == "hr":
            rendered.append(
                f"<hr style=\"border:none;border-top:1px solid {palette['border']};margin:28px 0;\" />"
            )
    return "".join(rendered)


def render_document(markdown: str, theme: Dict, title: Optional[str]) -> str:
    palette = theme["palette"]
    container_style = {
        "max-width": "760px",
        "margin": "0 auto",
        "padding": "24px 20px 40px",
        "background": palette["bg"],
        "color": palette["text"],
        "font-family": "-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',sans-serif",
    }
    cleaned_markdown, footnote_defs = extract_footnote_defs(markdown)
    state = make_state(footnote_defs)
    blocks = parse_blocks(cleaned_markdown, state)
    body_html = render_blocks(blocks, theme, state)
    footnotes_html = render_footnotes(theme, state)
    title_html = ""
    if title:
        first_block = blocks[0] if blocks else None
        if not (
            first_block
            and first_block.get("type") == "heading"
            and first_block.get("level") == 1
            and str(first_block.get("text", "")).strip() == title.strip()
        ):
            title_html = render_heading(title, 1, theme, 0)
    return (
        f"<section data-theme-id=\"{escape(theme['id'])}\" data-theme-name=\"{escape(theme['name'])}\" "
        f"style=\"{style_str(container_style)}\">"
        f"{title_html}{body_html}{footnotes_html}</section>"
    )


def read_input(path: Optional[str]) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Markdown into WeChat-friendly themed HTML using the standalone skill theme pack."
    )
    parser.add_argument("--theme", required=True, help="Theme id, for example w022")
    parser.add_argument("--input", help="Markdown input file. Reads stdin when omitted.")
    parser.add_argument("--output", help="Write rendered HTML to this file. Prints to stdout when omitted.")
    parser.add_argument("--title", help="Optional document title rendered as H1 before the markdown body.")
    args = parser.parse_args()

    theme = load_theme(args.theme)
    markdown = read_input(args.input)
    rendered = render_document(markdown, theme, args.title)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
