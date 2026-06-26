#!/usr/bin/env python3
"""Generate printable worksheet PDF/HTML and answer key from a compact JSON spec."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import pathname2url


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "worksheet"
DEFAULT_TEMPLATE = TEMPLATE_DIR / "a4-single.html"
TYPE_REGISTRY = TEMPLATE_DIR / "question-types.json"

LAYOUT_CLASSES = {
    "cards-3": "read-grid",
    "grid-4": "mental-grid",
    "grid-3": "compact-grid",
    "compact-3": "compact-grid",
    "problem-grid-2": "problem-grid",
    "check-grid-2": "check-grid",
    "geometry-grid-1": "geometry-grid",
}

CARD_CLASSES = {
    "reading_task": "read-card",
    "borrowing_chain": "problem",
    "check_equation": "check-card",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else line for line in text.splitlines())


def blank(kind: str = "normal") -> str:
    cls = "blank-wide" if kind == "wide" else "blank"
    return f'<span class="{cls}"></span>'


def render_with_blank_tokens(text: str) -> str:
    escaped = e(text)
    escaped = escaped.replace("[blank-wide]", blank("wide"))
    escaped = escaped.replace("[blank]", blank())
    return escaped


def render_choices(choices: list[object] | None) -> str:
    if not choices:
        return ""
    return " ".join(f'<span class="choice">{e(choice)}</span>' for choice in choices)


def render_reading_task(item: dict, number: int) -> tuple[str, str]:
    keyword_label = item.get("keyword_label", "关键词")
    task_label = item.get("task_label", "任务")
    answer_note = item.get("answer_note", "读题训练不按答案判分，能圈出关键词并说出任务即可。")
    body = (
        f'<div class="read-card">\n'
        f'  {number}. {e(item["text"])}<br>\n'
        f'  {e(keyword_label)}：{blank()}<br>\n'
        f'  {e(task_label)}：<span class="dash"></span>\n'
        f'</div>'
    )
    return body, f"{number}. {answer_note}"


def render_equation(item: dict, number: int) -> tuple[str, str]:
    body = f'<div class="item">{number}. {e(item["expr"])} = {blank()}</div>'
    answer_detail = item.get("answer_detail") or f'`{item["expr"]} = {item["answer"]}`'
    return body, f"{number}. {answer_detail}"


def render_borrowing_chain(item: dict, number: int) -> tuple[str, str]:
    step_lines = []
    for step in item["steps"]:
        step_lines.append(f'  <div class="chain">{render_with_blank_tokens(step)}</div>')
    body = (
        f'<div class="problem">\n'
        f'  {number}. {e(item["expr"])} = {blank()}\n'
        + "\n".join(step_lines)
        + "\n</div>"
    )
    return body, f"{number}. {item['answer_detail']}"


def render_check_equation(item: dict, number: int) -> tuple[str, str]:
    body = (
        f'<div class="check-card">\n'
        f'  {number}. {e(item["expr"])} = {blank()}<br>\n'
        f'  检查：{blank()} {e(item["check"])}\n'
        f'</div>'
    )
    answer_detail = item.get("answer_detail") or f'`{item["expr"]} = {item["answer"]}`，检查：`{item["answer"]} {item["check"]}`'
    return body, f"{number}. {answer_detail}"


def render_fill_condition(item: dict, number: int) -> tuple[str, str]:
    choices = render_choices(item.get("choices"))
    choices_line = f'\n  <div class="chain">圈可填的数：{choices}</div>' if choices else ""
    body = (
        f'<div class="problem">\n'
        f'  <div class="prompt">{number}. {render_with_blank_tokens(item["prompt"])}</div>'
        f'{choices_line}\n'
        f'</div>'
    )
    return body, f"{number}. {item['answer_detail']}"


def render_scratch_equation(item: dict, number: int) -> tuple[str, str]:
    check = item.get("check")
    check_line = f'\n  <div class="chain">检查：{blank()} {e(check)}</div>' if check else ""
    body = (
        f'<div class="problem">\n'
        f'  {number}. {e(item["expr"])} = {blank()}\n'
        f'  <span class="work-line"></span>\n'
        f'  <span class="work-line"></span>'
        f'{check_line}\n'
        f'</div>'
    )
    answer_detail = item.get("answer_detail") or f'`{item["expr"]} = {item["answer"]}`'
    return body, f"{number}. {answer_detail}"


def render_word_problem(item: dict, number: int) -> tuple[str, str]:
    work_lines = int(item.get("work_lines", 2))
    lines = "\n".join('  <span class="work-line"></span>' for _ in range(work_lines))
    suffix = item.get("answer_suffix", "")
    body = (
        f'<div class="problem tall">\n'
        f'  <div class="prompt">{number}. {render_with_blank_tokens(item["prompt"])}</div>\n'
        f'{lines}\n'
        f'  <div class="answer-line">{e(item["answer_prompt"])}{blank()}{e(suffix)}</div>\n'
        f'</div>'
    )
    return body, f"{number}. {item['answer_detail']}"


def svg_attrs(attrs: dict[str, object]) -> str:
    return " ".join(f'{name}="{e(value)}"' for name, value in attrs.items())


def render_geometry_svg(spec: dict) -> str:
    width = int(spec.get("canvas_width", 220))
    height = int(spec.get("canvas_height", 140))
    kind = spec.get("type")
    elements: list[str] = []

    if kind == "rectangle":
        x = int(spec.get("x", 40))
        y = int(spec.get("y", 30))
        rect_w = int(spec.get("draw_width", 130))
        rect_h = int(spec.get("draw_height", 70))
        elements.append(
            f'<rect {svg_attrs({"x": x, "y": y, "width": rect_w, "height": rect_h, "fill": "none", "stroke": "#111", "stroke-width": 2})}/>'
        )
        if spec.get("width_label"):
            elements.append(
                f'<text {svg_attrs({"x": x + rect_w / 2, "y": y + rect_h + 18})}>{e(spec["width_label"])}</text>'
            )
        if spec.get("height_label"):
            elements.append(
                f'<text {svg_attrs({"x": x - 18, "y": y + rect_h / 2})}>{e(spec["height_label"])}</text>'
            )
    elif kind == "composite_rect":
        for rect in spec.get("rects", []):
            elements.append(
                f'<rect {svg_attrs({"x": rect.get("x", 0), "y": rect.get("y", 0), "width": rect.get("width", 40), "height": rect.get("height", 30), "fill": "none", "stroke": "#111", "stroke-width": 2})}/>'
            )
        for label in spec.get("labels", []):
            elements.append(
                f'<text {svg_attrs({"x": label.get("x", 0), "y": label.get("y", 0)})}>{e(label.get("text", ""))}</text>'
            )
    else:
        raise ValueError(f"Unsupported geometry_spec type: {kind}")

    return (
        f'<svg class="geometry-diagram" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{e(spec.get("aria_label", "geometry diagram"))}">\n'
        + "\n".join(f"    {line}" for line in elements)
        + "\n  </svg>"
    )


def render_geometry_problem(item: dict, number: int) -> tuple[str, str]:
    work_lines = int(item.get("work_lines", 2))
    lines = "\n".join('  <span class="work-line"></span>' for _ in range(work_lines))
    suffix = item.get("answer_suffix", "")
    diagram = render_geometry_svg(item["geometry_spec"])
    body = (
        f'<div class="problem tall">\n'
        f'  <div class="prompt">{number}. {render_with_blank_tokens(item["prompt"])}</div>\n'
        f'  {diagram}\n'
        f'{lines}\n'
        f'  <div class="answer-line">{e(item["answer_prompt"])}{blank()}{e(suffix)}</div>\n'
        f'</div>'
    )
    return body, f"{number}. {item['answer_detail']}"


RENDERERS = {
    "reading_task": render_reading_task,
    "equation": render_equation,
    "borrowing_chain": render_borrowing_chain,
    "check_equation": render_check_equation,
    "fill_condition": render_fill_condition,
    "scratch_equation": render_scratch_equation,
    "word_problem": render_word_problem,
    "multi_step_word_problem": render_word_problem,
    "condition_filtering_problem": render_word_problem,
    "compare_after_intermediate_problem": render_word_problem,
    "geometry_problem": render_geometry_problem,
}


def validate_spec(spec: dict, registry: dict) -> None:
    registered = registry.get("types", {})
    for section in spec.get("sections", []):
        layout = section.get("layout")
        if layout not in LAYOUT_CLASSES:
            raise ValueError(f"Unknown layout: {layout}")
        for item in section.get("items", []):
            item_type = item.get("type")
            if item_type not in registered:
                raise ValueError(
                    f"Unknown item type: {item_type}. Add it to {TYPE_REGISTRY} and implement a renderer."
                )
            if item_type not in RENDERERS:
                raise ValueError(f"Item type {item_type} is registered but has no renderer.")
            missing = [field for field in registered[item_type].get("required", []) if field not in item]
            if missing:
                raise ValueError(f"{item_type} item missing required fields: {', '.join(missing)}")


def render_meta(fields: list[str]) -> str:
    parts = []
    for field in fields:
        parts.append(f'      <div>{e(field)}：<span class="line"></span></div>')
    return '    <section class="meta">\n' + "\n".join(parts) + "\n    </section>"


def render_sections(spec: dict) -> tuple[str, list[str], int]:
    sections_html = []
    answer_lines = []
    number = int(spec.get("start_number", 1))

    for section in spec.get("sections", []):
        layout = section["layout"]
        class_name = LAYOUT_CLASSES[layout]
        sections_html.append(f'    <h2>{e(section["title"])}</h2>')
        sections_html.append(f'    <section class="{class_name}">')
        for item in section.get("items", []):
            renderer = RENDERERS[item["type"]]
            item_html, answer_line = renderer(item, number)
            sections_html.append(indent(item_html, 6))
            answer_lines.append(answer_line)
            number += 1
        sections_html.append("    </section>")

    return "\n".join(sections_html), answer_lines, number - int(spec.get("start_number", 1))


def render_html(spec: dict, template_path: Path) -> tuple[str, list[str], int]:
    template = template_path.read_text(encoding="utf-8")
    sections, answers, count = render_sections(spec)
    reminder = ""
    if spec.get("reminder"):
        reminder = f'    <section class="tip">{e(spec["reminder"])}</section>'
    footer = ""
    if spec.get("footer"):
        footer = f'    <div class="footer">{e(spec["footer"])}</div>'
    html_text = (
        template.replace("{{title}}", e(spec["title"]))
        .replace("{{meta}}", render_meta(spec.get("fields", ["姓名", "日期", "用时", "正确题数"])))
        .replace("{{reminder}}", reminder)
        .replace("{{sections}}", sections)
        .replace("{{footer}}", footer)
    )
    return html_text, answers, count


def render_answer_key(spec: dict, answers: list[str], count: int) -> str:
    lines = [
        f"# {spec['title']}答案与批改标准",
        "",
        f"- 日期：{spec.get('date', '')}",
        f"- 对应练习卷：`{spec.get('worksheet_file', 'worksheet.html')}`",
    ]
    if spec.get("target"):
        lines.append(f"- 目标：{spec['target']}")
    if spec.get("strategy"):
        lines.append(f"- 出卷策略：{spec['strategy']}")
    if spec.get("diagnostic_target"):
        lines.append(f"- 诊断目标：{spec['diagnostic_target']}")
    if spec.get("review_status"):
        lines.append(f"- 复核状态：{spec['review_status']}")
    lines.extend(["", "## 答案", ""])
    lines.extend(answers)

    grading = spec.get("grading", {})
    if grading.get("error_labels"):
        lines.extend(["", "## 批改重点", "", "每个错误请标一种原因：", ""])
        for label in grading["error_labels"]:
            lines.append(f"- `{label['name']}`：{label['description']}")

    if grading.get("reassessment"):
        lines.extend(["", "## 复评标准", ""])
        for item in grading["reassessment"]:
            lines.append(f"- {item}")

    if grading.get("next"):
        lines.extend(["", "## 下次建议", ""])
        for item in grading["next"]:
            lines.append(f"- {item}")

    lines.append("")
    return "\n".join(lines)


def default_chrome() -> str | None:
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")


def export_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = default_chrome()
    if not chrome:
        raise RuntimeError("Chrome/Chromium not found; cannot export worksheet PDF.")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    url = "file://" + pathname2url(str(html_path.resolve()))
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        url,
    ]
    result = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 or not pdf_path.exists():
        detail = result.stderr.strip() or result.stdout.strip() or "Chrome did not create a PDF."
        raise RuntimeError(f"PDF export failed: {detail}")


def count_pdf_pages(pdf_path: Path) -> int:
    data = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page\b", data))


def verify_pdf_page_count(pdf_path: Path, expected_pages: int) -> int:
    pages = count_pdf_pages(pdf_path)
    if pages != expected_pages:
        raise RuntimeError(f"Print verification failed: expected {expected_pages} page(s), got {pages}.")
    return pages


def verify_print_page_count(html_path: Path, expected_pages: int) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "worksheet.pdf"
        export_pdf(html_path, pdf_path)
        return verify_pdf_page_count(pdf_path, expected_pages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate worksheet PDF/HTML and answer key from JSON spec.")
    parser.add_argument("spec", type=Path, help="Path to worksheet-spec.json")
    parser.add_argument("--pdf", action="store_true", help="Require student-facing PDF output. PDF is attempted by default.")
    parser.add_argument("--no-pdf", action="store_true", help="Skip student-facing PDF output.")
    parser.add_argument("--pdf-file", help="PDF filename relative to the worksheet directory. Defaults to worksheet.pdf.")
    parser.add_argument("--verify-print", action="store_true", help="Verify browser print page count with Chrome.")
    args = parser.parse_args()

    spec_path = args.spec.resolve()
    spec = load_json(spec_path)
    registry = load_json(TYPE_REGISTRY)
    validate_spec(spec, registry)

    out_dir = spec_path.parent
    worksheet_file = spec.get("worksheet_file", "worksheet.html")
    answer_key_file = spec.get("answer_key_file", "answer-key.md")
    pdf_file = args.pdf_file or spec.get("pdf_file", "worksheet.pdf")
    spec["worksheet_file"] = worksheet_file
    template_path = ROOT / spec.get("template", str(DEFAULT_TEMPLATE.relative_to(ROOT)))

    html_text, answers, count = render_html(spec, template_path)
    answer_key = render_answer_key(spec, answers, count)

    worksheet_path = out_dir / worksheet_file
    answer_key_path = out_dir / answer_key_file
    worksheet_path.write_text(html_text, encoding="utf-8")
    answer_key_path.write_text(answer_key, encoding="utf-8")

    print(f"generated: {worksheet_path}")
    print(f"generated: {answer_key_path}")
    print(f"items: {count}")

    page_config = spec.get("page", {})
    verify_requested = args.verify_print or page_config.get("verify_print")
    pdf_requested = not args.no_pdf or args.pdf or args.pdf_file or spec.get("pdf_file") or page_config.get("pdf")
    pdf_required = args.pdf or args.pdf_file or spec.get("pdf_file") or page_config.get("pdf_required") or verify_requested
    pdf_path = out_dir / pdf_file

    if pdf_requested:
        try:
            export_pdf(worksheet_path, pdf_path)
            print(f"generated: {pdf_path}")
        except RuntimeError as exc:
            if pdf_required:
                raise
            print(f"warning: PDF export skipped: {exc}", file=sys.stderr)

    if verify_requested:
        expected = int(spec.get("page", {}).get("expected_pages", 1))
        if pdf_path.exists():
            pages = verify_pdf_page_count(pdf_path, expected)
        else:
            pages = verify_print_page_count(worksheet_path, expected)
        print(f"print_pages: {pages}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
