#!/usr/bin/env python3
"""Pure planning and verification primitives for Markdown uploads."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Sequence
from urllib.parse import unquote


IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\("
    r"(?!<?(?:https?://|data:))"
    r"(?:<([^>\n]+)>|([^)\n]+?))"
    r"(?:\s+['\"][^'\"]*['\"])?\s*"
    r"\)"
)
REMOTE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?:<)?https?://[^)>]+(?:>)?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"(^```[^\n]*\n[\s\S]*?^```\s*$)", re.MULTILINE)
LEXIANG_MATH_RE = re.compile(r"\$`([^`\n]+)`\$")
PORTABLE_CALLOUT_RE = re.compile(
    r"^>[ \t]+\[!(stat|definition|note)\][ \t]+(.+?)[ \t]*\n"
    r"((?:>[ \t]?.*(?:\n|$))+)",
    re.MULTILINE,
)
CAPTION_HEADING_RE = re.compile(
    r"^#{1,6}\s+((?:FIG\.|TABLE(?:\s|$)|Table of Contents Graphic:).*)$",
    re.MULTILINE | re.IGNORECASE,
)


class PreflightError(ValueError):
    """The local package is unsafe to upload."""


class VerificationError(RuntimeError):
    """The remote page does not match the validated local plan."""


@dataclass(frozen=True)
class Segment:
    kind: str
    value: str
    icon: str = ""


@dataclass(frozen=True)
class Formula:
    latex: str
    display: bool


@dataclass(frozen=True)
class Callout:
    kind: str
    markdown: str
    icon: str


@dataclass(frozen=True)
class UploadPlan:
    markdown: str
    segments: tuple[Segment, ...]
    image_paths: tuple[Path, ...]
    remote_image_references: int
    formulas: tuple[Formula, ...]
    callouts: tuple[Callout, ...]
    headings: tuple[str, ...]
    anchors: tuple[str, ...]


def _image_path(match: re.Match[str]) -> str:
    """Return a local image destination, including non-standard paths with spaces."""
    return (match.group(1) or match.group(2) or "").strip()


def _find_closing_dollar(text: str, start: int, double: bool) -> int:
    token = "$$" if double else "$"
    cursor = start
    while cursor < len(text):
        position = text.find(token, cursor)
        if position < 0:
            return -1
        slashes = 0
        index = position - 1
        while index >= 0 and text[index] == "\\":
            slashes += 1
            index -= 1
        if slashes % 2 == 0:
            return position
        cursor = position + len(token)
    return -1


def _convert_math_outside_code(text: str) -> tuple[str, list[Formula]]:
    output: list[str] = []
    formulas: list[Formula] = []
    index = 0
    while index < len(text):
        if text.startswith(r"\$", index):
            output.append(r"\$")
            index += 2
            continue
        if text[index] != "$":
            output.append(text[index])
            index += 1
            continue
        if index + 1 < len(text) and (
            text[index + 1].isdigit()
            or (
                text[index + 1] in {"≈", "~"}
                and index + 2 < len(text)
                and text[index + 2].isdigit()
            )
        ):
            output.append("$")
            index += 1
            continue
        display = text.startswith("$$", index)
        width = 2 if display else 1
        end = _find_closing_dollar(text, index + width, display)
        if end < 0:
            raise PreflightError(f"未闭合的 LaTeX 公式，字符偏移 {index}")
        latex = text[index + width : end].strip()
        if not latex:
            raise PreflightError(f"空公式，字符偏移 {index}")
        if "`" in latex:
            raise PreflightError(f"公式含反引号，无法安全表示：{latex[:80]}")
        formulas.append(Formula(latex=latex, display=display))
        rendered = f"$`{latex}`$"
        output.append(f"\n\n{rendered}\n\n" if display else rendered)
        index = end + width
    return "".join(output), formulas


def _convert_inline_code_aware(text: str) -> tuple[str, list[Formula]]:
    output: list[str] = []
    formulas: list[Formula] = []
    cursor = 0
    for match in re.finditer(r"`[^`\n]*`", text):
        before, found = _convert_math_outside_code(text[cursor : match.start()])
        output.extend((before, match.group(0)))
        formulas.extend(found)
        cursor = match.end()
    tail, found = _convert_math_outside_code(text[cursor:])
    output.append(tail)
    formulas.extend(found)
    return "".join(output), formulas


def convert_math(markdown: str) -> tuple[str, tuple[Formula, ...]]:
    """Convert standard LaTeX delimiters without touching code."""
    output: list[str] = []
    formulas: list[Formula] = []
    cursor = 0
    for fence in FENCE_RE.finditer(markdown):
        before, found = _convert_inline_code_aware(markdown[cursor : fence.start()])
        output.extend((before, fence.group(0)))
        formulas.extend(found)
        cursor = fence.end()
    tail, found = _convert_inline_code_aware(markdown[cursor:])
    output.append(tail)
    formulas.extend(found)
    return "".join(output), tuple(formulas)


def _split_large_text(text: str, limit: int) -> Iterable[str]:
    if len(text) <= limit:
        yield text
        return
    paragraphs = text.split("\n\n")
    buffer = ""
    for paragraph in paragraphs:
        candidate = f"{buffer}\n\n{paragraph}" if buffer else paragraph
        if buffer and len(candidate) > limit:
            yield buffer
            buffer = paragraph
        else:
            buffer = candidate
    if buffer:
        yield buffer


def parse_portable_callouts(markdown: str) -> tuple[tuple[Callout, ...], tuple[tuple[int, int], ...]]:
    """Parse supported trans-doc-to-md callouts outside fenced code."""
    callouts: list[Callout] = []
    spans: list[tuple[int, int]] = []
    fence_spans = tuple((match.start(), match.end()) for match in FENCE_RE.finditer(markdown))
    icons = {"stat": "📊", "definition": "📖", "note": "💡"}
    for match in PORTABLE_CALLOUT_RE.finditer(markdown):
        if any(start <= match.start() < end for start, end in fence_spans):
            continue
        quote_lines = match.group(3).splitlines()
        body_lines = [re.sub(r"^>[ \t]?", "", line) for line in quote_lines]
        if len(body_lines) < 2:
            continue
        paragraphs = [match.group(2).strip(), *(line.strip() for line in body_lines)]
        markdown_body = "\n\n".join(paragraph for paragraph in paragraphs if paragraph)
        kind = match.group(1)
        callouts.append(Callout(kind=kind, markdown=markdown_body, icon=icons[kind]))
        spans.append(match.span())
    return tuple(callouts), tuple(spans)


def split_segments(
    markdown: str,
    image_paths: Sequence[Path],
    callouts: Sequence[Callout] = (),
    callout_spans: Sequence[tuple[int, int]] = (),
    text_limit: int = 15_000,
) -> tuple[Segment, ...]:
    segments: list[Segment] = []
    cursor = 0
    image_matches = [
        match
        for match in IMAGE_RE.finditer(markdown)
        if not any(start <= match.start() < end for start, end in callout_spans)
    ]
    events = [
        (match.start(), match.end(), "image", str(image_paths[index]), "")
        for index, match in enumerate(image_matches)
    ]
    events.extend(
        (start, end, "callout", callouts[index].markdown, callouts[index].icon)
        for index, (start, end) in enumerate(callout_spans)
    )
    for start, end, kind, value, icon in sorted(events):
        text = markdown[cursor:start].strip()
        segments.extend(Segment("text", chunk) for chunk in _split_large_text(text, text_limit) if chunk)
        segments.append(Segment(kind, value, icon))
        cursor = end
    tail = markdown[cursor:].strip()
    segments.extend(Segment("text", chunk) for chunk in _split_large_text(tail, text_limit) if chunk)
    return tuple(segments)


def split_large_gfm_tables(markdown: str, max_rows: int = 10) -> str:
    """Split GFM tables to satisfy Lexiang's row limit."""
    if max_rows < 2:
        raise ValueError("max_rows must leave room for a header row")
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0

    def is_separator(line: str) -> bool:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)

    while index < len(lines):
        if index + 1 < len(lines) and lines[index].lstrip().startswith("|") and is_separator(lines[index + 1]):
            end = index + 2
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            header, separator = lines[index], lines[index + 1]
            rows = lines[index + 2 : end]
            page_size = max_rows - 1
            if len(rows) > page_size:
                for start in range(0, len(rows), page_size):
                    if start:
                        output.append("")
                    output.extend([header, separator, *rows[start : start + page_size]])
            else:
                output.extend(lines[index:end])
            index = end
            continue
        output.append(lines[index])
        index += 1
    return "\n".join(output)


def demote_caption_headings(markdown: str) -> str:
    return CAPTION_HEADING_RE.sub(r"\1", markdown)


def _plain_text(markdown: str) -> str:
    text = IMAGE_RE.sub("", markdown)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[#>*_~`\[\]()|\\$^{}]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _anchors(markdown: str) -> tuple[str, ...]:
    anchors: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "!", "|", "<", "```")):
            continue
        plain = _plain_text(stripped)
        if len(plain) >= 80 and plain[:100] not in anchors:
            anchors.append(plain[:100])
    return tuple(anchors)


def _resolve_image(markdown_dir: Path, raw_path: str) -> Path:
    decoded = unquote(raw_path).split("#", 1)[0].split("?", 1)[0]
    candidate = (markdown_dir / decoded).resolve()
    try:
        candidate.relative_to(markdown_dir.resolve())
    except ValueError as error:
        raise PreflightError(f"图片路径越出 Markdown 目录：{raw_path}") from error
    return candidate


def build_plan(markdown: str, markdown_dir: Path, text_limit: int = 15_000) -> UploadPlan:
    if not markdown.strip():
        raise PreflightError("Markdown 为空")
    converted, formulas = convert_math(markdown)
    converted = split_large_gfm_tables(demote_caption_headings(converted))
    callouts, callout_spans = parse_portable_callouts(converted)
    image_matches = [
        match
        for match in IMAGE_RE.finditer(converted)
        if not any(start <= match.start() < end for start, end in callout_spans)
    ]
    image_paths = tuple(_resolve_image(markdown_dir, _image_path(match)) for match in image_matches)
    missing = [str(path) for path in image_paths if not path.is_file()]
    if missing:
        raise PreflightError("缺少图片文件：" + ", ".join(missing))
    headings = tuple(match.group(1).strip() for match in HEADING_RE.finditer(converted))
    segments = split_segments(
        converted,
        image_paths,
        callouts,
        callout_spans,
        text_limit=text_limit,
    )
    if not segments or not any(segment.kind in {"text", "callout"} for segment in segments):
        raise PreflightError("文档没有可写入的正文")
    return UploadPlan(
        markdown=converted,
        segments=segments,
        image_paths=image_paths,
        remote_image_references=len(REMOTE_IMAGE_RE.findall(converted)),
        formulas=formulas,
        callouts=callouts,
        headings=headings,
        anchors=_anchors(converted),
    )


def normalize_for_compare(text: str) -> str:
    text = text.replace("\\", "").replace("_", "")
    text = re.sub(r"\$`([^`]+)`\$", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[^\w\u3400-\u9fff]+", "", text, flags=re.UNICODE).lower()


def verify_remote(
    plan: UploadPlan,
    remote_clean: str,
    remote_markdown: str,
    remote_image_count: int,
    remote_callout_count: int = 0,
) -> None:
    problems: list[str] = []
    normalized_remote = normalize_for_compare(remote_clean)
    missing_headings = [heading for heading in plan.headings if normalize_for_compare(heading) not in normalized_remote]
    if missing_headings:
        problems.append("缺少标题：" + "；".join(missing_headings[:5]))
    missing_anchors = [anchor for anchor in plan.anchors if normalize_for_compare(anchor) not in normalized_remote]
    if missing_anchors:
        preview = "；".join(missing_anchors[:3])
        problems.append(
            f"缺少长段落锚点 {len(missing_anchors)}/{len(plan.anchors)}：{preview}"
        )
    expected_images = len(plan.image_paths) + plan.remote_image_references
    if remote_image_count != expected_images:
        problems.append(f"图片数不一致：Markdown {expected_images}，线上 {remote_image_count}")
    if remote_callout_count != len(plan.callouts):
        problems.append(f"callout 数不一致：本地 {len(plan.callouts)}，线上 {remote_callout_count}")
    missing_callouts = [
        callout
        for callout in plan.callouts
        if normalize_for_compare(callout.markdown) not in normalized_remote
    ]
    if missing_callouts:
        problems.append(f"callout 内容缺失 {len(missing_callouts)}/{len(plan.callouts)}")
    normalized_markdown = normalize_for_compare(remote_markdown)
    remote_formulas = LEXIANG_MATH_RE.findall(remote_markdown)
    if len(remote_formulas) != len(plan.formulas):
        problems.append(f"原生公式数不一致：本地 {len(plan.formulas)}，线上 {len(remote_formulas)}")
    missing_formulas = [
        formula.latex for formula in plan.formulas
        if normalize_for_compare(formula.latex) not in normalized_markdown
    ]
    if missing_formulas:
        problems.append(f"公式内容缺失 {len(missing_formulas)}/{len(plan.formulas)}")
    if problems:
        raise VerificationError("；".join(problems))


def count_remote_images(blocks: Sequence[dict]) -> int:
    return sum(1 for block in blocks if block.get("block_type") == "image")


def count_remote_callouts(blocks: Sequence[dict]) -> int:
    return sum(1 for block in blocks if block.get("block_type") == "callout")
