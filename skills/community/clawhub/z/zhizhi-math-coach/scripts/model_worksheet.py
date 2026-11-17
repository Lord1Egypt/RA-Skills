"""Validate model-authored static worksheets without restricting question types."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path


TAGS = set("html head meta title style body main section article header footer div span p br hr h1 h2 h3 h4 ol ul li table thead tbody tfoot tr th td strong em b i u small sup sub figure figcaption img svg g path line polyline polygon rect circle ellipse text tspan defs marker clippath use symbol desc".split())
FORBIDDEN_MARKERS = {"answer_detail", "答案与批改标准", "批改重点", "复评标准"}


def worksheet_language(spec: dict) -> str:
    """Resolve generated labels without translating model-authored content."""
    language = spec.get("language")
    if language is None and isinstance(spec.get("student_html"), str):
        match = re.search(r'''<html\b[^>]*\blang\s*=\s*["']([^"']+)["']''', spec["student_html"], re.I)
        if match:
            language = match.group(1)
    if language is None:
        return "zh"
    if not isinstance(language, str) or not language.strip():
        raise ValueError("language must be a non-empty language tag")
    base = language.strip().lower().split("-")[0]
    if base not in {"en", "zh"}:
        raise ValueError("generated answer-key labels support English and Chinese; use direct document authoring for other languages")
    return base


class StaticWorksheet(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.question_ids: list[str] = []
        self.style_depth = 0
        self.style_text: list[str] = []
        self.has_html = False
        self.has_body = False
        self.has_head = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in TAGS:
            raise ValueError(f"student_html must be static; unsupported element: {tag}")
        self.has_html |= tag == "html"
        self.has_body |= tag == "body"
        self.has_head |= tag == "head"
        if tag == "style":
            self.style_depth += 1
        for name, value in attrs:
            value = value or ""
            if name.startswith("on") or name in {"srcdoc", "data-answer", "data-solution", "http-equiv", "srcset", "background"}:
                raise ValueError(f"unsupported student_html attribute: {name}")
            if name in {"src", "href", "xlink:href"} and not value.startswith("#"):
                # Embedded raster images are supported; active SVG/external URLs are not.
                if not re.fullmatch(r"data:image/(?:png|jpeg|webp);base64,[A-Za-z0-9+/=\s]+", value):
                    raise ValueError("worksheet assets must be inline SVG, fragment references or embedded raster images")
            if re.search(r"url\s*\(", value, re.I) and not re.fullmatch(r"url\(#[A-Za-z0-9_-]+\)", value):
                raise ValueError("SVG paint references must stay inside the document")
            if name == "style":
                check_css(value)
            if name == "data-question-id":
                self.question_ids.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.style_depth = max(0, self.style_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.style_depth:
            self.style_text.append(data)


def check_css(css: str) -> None:
    normalized = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    # Escapes can hide remote URLs, so restrict this static-print surface.
    if "\\" in normalized or re.search(r"url\s*\(|@import|expression\s*\(|-moz-binding|behavior\s*:", normalized, flags=re.I):
        raise ValueError("worksheet CSS must not fetch external assets or execute code")


def validate_model_spec(spec: dict) -> None:
    worksheet_language(spec)
    if not isinstance(spec.get("title"), str) or not spec["title"].strip():
        raise ValueError("model worksheet needs a title")
    if spec.get("review_status") not in {"model_reviewed", "approved"}:
        raise ValueError("model worksheet requires independent math/diagram review before generation")
    questions = spec.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("model worksheet needs a questions answer manifest")
    ids = []
    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("questions must contain objects")
        for key in ("id", "answer", "explanation"):
            if not isinstance(question.get(key), str) or not question[key].strip():
                raise ValueError(f"each question needs a non-empty {key}")
        ids.append(question["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("question IDs must be unique")
    student_html = spec.get("student_html")
    if not isinstance(student_html, str) or not student_html.strip():
        raise ValueError("model worksheet needs complete student_html")
    if any(marker in student_html for marker in FORBIDDEN_MARKERS):
        raise ValueError("student_html contains an answer/diagnosis marker")
    parser = StaticWorksheet()
    parser.feed(student_html)
    parser.close()
    check_css("".join(parser.style_text))
    if not parser.has_html or not parser.has_body or not parser.has_head or not re.search(r"</head\s*>", student_html, re.I):
        raise ValueError("student_html must be a complete HTML document")
    if sorted(parser.question_ids) != sorted(ids):
        raise ValueError("each answer-manifest ID must occur exactly once as data-question-id in student_html")


def apply_print_profile(student_html: str) -> str:
    css = (Path(__file__).resolve().parents[1] / "assets/worksheet/a4-print.css").read_text(encoding="utf-8")
    return re.sub(r"</head\s*>", lambda _: f'<style id="zhizhi-print-profile">\n{css}\n</style>\n</head>', student_html, count=1, flags=re.I)


def render_model_spec(spec: dict) -> tuple[str, list[str], int]:
    validate_model_spec(spec)
    explanation_label = "Explanation: " if worksheet_language(spec) == "en" else "解析："
    answers = [f"{q['id']}. {q['answer']}\n\n   {explanation_label}{q['explanation']}" for q in spec["questions"]]
    return apply_print_profile(spec["student_html"]), answers, len(answers)
