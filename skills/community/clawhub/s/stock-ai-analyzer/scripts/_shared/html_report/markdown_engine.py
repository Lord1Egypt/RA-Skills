"""Markdown → HTML engine shared across stock-skill renderers.

Pure standard library. Supports the subset of Markdown that research reports
need: headings, paragraphs, indentation-aware nested bullet lists, blockquotes, tables (with
alignment), inline code/bold/italic/links, inline ``==text==`` highlights
(``<mark>``), fenced code blocks, and the ``==...==`` callout sugar.

Structured callout blocks render as typed cards. Each registered type in
``_STRUCTURED_BLOCKS`` maps a first-line prefix (e.g. ``==深度调研发现｜...``,
``==跟踪事项｜...``) to a CSS class prefix and the labelled rows it accepts;
the first line carries ``｜``-separated badge segments, following ``标签：值``
lines become labelled rows, anything else becomes a note line. The CSS for
each card type ships with the skill that writes the block.
"""

from __future__ import annotations

import html
import re
from typing import List


def strip_front_matter(markdown_text: str) -> str:
    """Remove a leading YAML front matter block from Markdown.

    A block is treated as front matter only when the document starts with an
    exact ``---`` fence (optionally after a UTF-8 BOM), has a closing fence,
    and contains at least one YAML-style mapping key.  The mapping check keeps
    a leading Markdown thematic break from swallowing later report content.
    """
    text = markdown_text.removeprefix("\ufeff")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text

    for idx in range(1, len(lines)):
        if lines[idx].strip() != "---":
            continue
        metadata_lines = lines[1:idx]
        has_mapping = any(
            re.match(r"^[^\s:#][^:]*:\s*.*$", line.strip())
            for line in metadata_lines
        )
        if has_mapping:
            return "".join(lines[idx + 1 :])
        return text
    return text


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped) <= {"|", "-", ":", " "}


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    code_values: List[str] = []

    def keep_code(match: re.Match[str]) -> str:
        code_values.append(f"<code>{match.group(1)}</code>")
        return f"@@CODE{len(code_values) - 1}@@"

    escaped = re.sub(r"`([^`]+)`", keep_code, escaped)
    escaped = re.sub(r"==([^=\n]+)==", r"<mark>\1</mark>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    for idx, value in enumerate(code_values):
        escaped = escaped.replace(f"@@CODE{idx}@@", value)
    return escaped


def _strip_callout_markers(lines: List[str]) -> List[str]:
    cleaned = [line.strip() for line in lines]
    if cleaned:
        cleaned[0] = cleaned[0].removeprefix("==").strip()
        cleaned[0] = cleaned[0].removesuffix("==").strip()
    if cleaned:
        cleaned[-1] = cleaned[-1].removesuffix("==").strip()
    return [line for line in cleaned if line]


# Registered structured-callout types: first-line prefix → CSS class prefix +
# the labelled rows the card accepts (in display order). CSS ships per skill.
_STRUCTURED_BLOCKS = {
    "深度调研发现": {"css": "deep-finding", "rows": ("来源", "原文", "判断", "影响")},
    "跟踪事项": {"css": "todo", "rows": ("事项", "变量", "验证", "反证", "来源")},
}


def _render_structured_block(kind: str, spec: dict, lines: List[str]) -> str:
    cleaned = _strip_callout_markers(lines)
    header = cleaned[0] if cleaned else kind
    parts = [part.strip() for part in re.split(r"[|｜]", header) if part.strip()]
    badges = parts[1:] if parts and parts[0] == kind else parts
    css = spec["css"]
    row_labels = spec["rows"]
    label_re = re.compile(r"^(" + "|".join(row_labels) + r")[：:]\s*(.+)$")

    rows = {}
    notes: List[str] = []
    for line in cleaned[1:]:
        match = label_re.match(line)
        if match:
            rows[match.group(1)] = match.group(2).strip()
        else:
            notes.append(line)

    out = [
        f'<aside class="{css}-card">',
        f'<div class="{css}-head"><span class="{css}-title">{kind}</span>',
    ]
    for badge in badges:
        out.append(f'<span class="{css}-sep">｜</span>')
        out.append(f'<span class="{css}-badge">{inline_markdown(badge)}</span>')
    out.append("</div>")
    out.append(f'<div class="{css}-body">')
    for label in row_labels:
        value = rows.get(label)
        if value:
            out.append(
                f'<div class="{css}-row {css}-row-{label}">'
                f'<span class="{css}-label">{label}：</span>'
                f'<span class="{css}-value">{inline_markdown(value)}</span>'
                "</div>"
            )
    for note in notes:
        out.append(f'<p class="{css}-note">{inline_markdown(note)}</p>')
    out.append("</div></aside>")
    return "".join(out)


def render_callout(lines: List[str]) -> str:
    cleaned = _strip_callout_markers(lines)
    first = cleaned[0] if cleaned else ""
    for kind, spec in _STRUCTURED_BLOCKS.items():
        if first.startswith(kind):
            return _render_structured_block(kind, spec, lines)
    callout = " ".join(cleaned).strip()
    return f"<div class=\"callout\">{inline_markdown(callout)}</div>"


def flush_paragraph(parts: List[str], out: List[str]) -> None:
    if not parts:
        return
    text = " ".join(part.strip() for part in parts if part.strip())
    if text:
        out.append(f"<p>{inline_markdown(text)}</p>")
    parts.clear()


def render_table(lines: List[str]) -> str:
    rows: List[List[str]] = []
    aligns: List[str] = []
    for idx, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if idx == 1 and is_table_separator(line):
            for cell in cells:
                if cell.startswith(":") and cell.endswith(":"):
                    aligns.append("center")
                elif cell.endswith(":"):
                    aligns.append("right")
                else:
                    aligns.append("left")
            continue
        rows.append(cells)

    if not rows:
        return ""

    header = rows[0]
    body = rows[1:]
    html_rows = ["<div class=\"table-wrap\"><table>"]
    html_rows.append("<thead><tr>")
    for idx, cell in enumerate(header):
        align = aligns[idx] if idx < len(aligns) else "left"
        html_rows.append(f"<th class=\"align-{align}\">{inline_markdown(cell)}</th>")
    html_rows.append("</tr></thead>")
    html_rows.append("<tbody>")
    for row in body:
        html_rows.append("<tr>")
        for idx, cell in enumerate(row):
            align = aligns[idx] if idx < len(aligns) else "left"
            html_rows.append(f"<td class=\"align-{align}\">{inline_markdown(cell)}</td>")
        html_rows.append("</tr>")
    html_rows.append("</tbody></table></div>")
    return "".join(html_rows)


def _list_item(line: str) -> tuple[int, str] | None:
    """Return ``(indent, text)`` for an unordered-list line."""
    match = re.match(r"^(\s*)[-*]\s+(.+)$", line)
    if not match:
        return None
    indent = len(match.group(1).expandtabs(4))
    return indent, match.group(2)


def render_list(lines: List[str]) -> str:
    """Render consecutive unordered-list lines, preserving indentation levels."""
    items = [item for line in lines if (item := _list_item(line)) is not None]
    if not items:
        return ""

    def render_level(index: int, indent: int) -> tuple[str, int]:
        out = ["<ul>"]
        while index < len(items):
            item_indent, text = items[index]
            if item_indent < indent:
                break
            if item_indent > indent:
                # A malformed indent jump still belongs to the previous item;
                # the recursive level uses the actual whitespace rather than
                # inventing a fixed nesting width.
                nested, index = render_level(index, item_indent)
                out.append(nested)
                continue

            index += 1
            out.append(f"<li>{inline_markdown(text)}")
            if index < len(items) and items[index][0] > indent:
                nested, index = render_level(index, items[index][0])
                out.append(nested)
            out.append("</li>")
        out.append("</ul>")
        return "".join(out), index

    rendered, _ = render_level(0, items[0][0])
    return rendered


def render_markdown(markdown_text: str) -> str:
    lines = strip_front_matter(markdown_text).splitlines()
    out: List[str] = []
    paragraph: List[str] = []
    idx = 0
    in_code = False
    code_lines: List[str] = []

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph(paragraph, out)
            if in_code:
                out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            idx += 1
            continue

        if in_code:
            code_lines.append(line)
            idx += 1
            continue

        if not stripped:
            flush_paragraph(paragraph, out)
            idx += 1
            continue

        # A paired marker at the start of an otherwise normal line is an
        # inline highlight, not the opener of a multiline callout.  Without
        # this guard, text such as ``==深度调研发现==【W3】...`` consumes every
        # following line until another line happens to end in ``==``.
        # Keep the legacy bare ``==深度调研发现==`` opener working because old
        # analyzer reports use it to introduce a short finding block.
        has_inline_pair = re.match(r"^==[^=\n]+==", stripped) is not None
        if has_inline_pair and stripped != "==深度调研发现==":
            paragraph.append(stripped)
            idx += 1
            continue

        if stripped.startswith("=="):
            flush_paragraph(paragraph, out)
            callout_parts = [stripped]
            if stripped == "==深度调研发现==":
                while idx + 1 < len(lines):
                    next_line = lines[idx + 1].strip()
                    if (
                        not next_line
                        or next_line.startswith("#")
                        or next_line.startswith("|")
                        or re.match(r"^[-*]\s+", next_line)
                    ):
                        break
                    idx += 1
                    callout_parts.append(next_line)
                    if next_line == "==" or next_line.endswith("=="):
                        break
            else:
                while not callout_parts[-1].endswith("==") and idx + 1 < len(lines):
                    idx += 1
                    callout_parts.append(lines[idx].strip())
            out.append(render_callout(callout_parts))
            idx += 1
            continue

        if stripped.startswith("|") and idx + 1 < len(lines) and is_table_separator(lines[idx + 1]):
            flush_paragraph(paragraph, out)
            table_lines = [line, lines[idx + 1]]
            idx += 2
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                table_lines.append(lines[idx])
                idx += 1
            out.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph(paragraph, out)
            level = min(len(heading.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            idx += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph(paragraph, out)
            quote = stripped.lstrip(">").strip()
            out.append(f"<blockquote>{inline_markdown(quote)}</blockquote>")
            idx += 1
            continue

        if _list_item(line) is not None:
            flush_paragraph(paragraph, out)
            list_lines = []
            while idx < len(lines) and _list_item(lines[idx]) is not None:
                list_lines.append(lines[idx])
                idx += 1
            out.append(render_list(list_lines))
            continue

        paragraph.append(stripped)
        idx += 1

    if in_code:
        out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    flush_paragraph(paragraph, out)
    return "\n".join(out)
