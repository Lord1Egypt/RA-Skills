"""Validation helpers owned by trans-doc-to-md.

This module validates translation completeness only. It deliberately contains no
Lexiang upload or authentication logic.
"""
from __future__ import annotations

from difflib import SequenceMatcher
import re
import unicodedata


class ValidationError(ValueError):
    """The bilingual output appears to have dropped source text."""


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE_ONLY_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\s*\)"
)
TOKEN_RE = re.compile(r"[a-z]+(?:['’][a-z]+)*|\d+(?:\.\d+)?", re.IGNORECASE)
CONTENTS_RE = re.compile(r"^(?:contents|table of contents)(?:\s*/\s*(?:目录|目次))?$", re.IGNORECASE)
TOC_ITEM_RE = re.compile(
    r"^\s*-\s+(?:\*\*[^*]+\*\*\s*:\s+\S.+|\*\*[^*]+\*\*)\s+·\s+p\.\d+\s*$",
    re.IGNORECASE,
)
TOC_LIST_TITLE_RE = re.compile(
    r"^\s*-\s+\*\*[^*]+\*\*\s*:\s*(.+?)(?:\s+·\s+p\.\d+)?\s*$",
    re.IGNORECASE,
)
TOC_UNLABELED_TITLE_RE = re.compile(
    r"^\s*-\s+\*\*(.+?)\*\*\s+·\s+p\.\d+\s*$",
    re.IGNORECASE,
)
TOC_CATEGORY_RE = re.compile(r"^\s*-\s+\*\*([^*]+)\*\*\s*:", re.IGNORECASE)
NUMBERED_CHAPTER_RE = re.compile(r"^(?:section|chapter|part)\s+\w+\b", re.IGNORECASE)
END_MATTER_RE = re.compile(
    r"^(?:endnotes?|references?|appendi(?:x|ces)|disclaimer|acknowledg)",
    re.IGNORECASE,
)
LIST_ITEM_RE = re.compile(r"^\s*(?:[-+*]|\d+\.)\s+(.+?)\s*$")


def _select_section(markdown: str, section: str | None) -> str:
    if not section:
        return markdown
    lines = markdown.splitlines()
    wanted = section.casefold()
    start = None
    level = None
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match and wanted in match.group(2).casefold():
            start = index + 1
            level = len(match.group(1))
            break
    if start is None or level is None:
        raise ValidationError(f"源文档中找不到章节：{section}")
    end = len(lines)
    for index in range(start, len(lines)):
        match = HEADING_RE.match(lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])


def _paragraphs(markdown: str) -> list[str]:
    markdown = re.sub(
        r"(?ms)^\[IMAGE\]\s*$.*?^\[/IMAGE\]\s*$",
        "",
        markdown,
    )
    markdown = re.sub(
        r"<image_ocr>.*?</image_ocr>",
        "",
        markdown,
        flags=re.IGNORECASE | re.DOTALL,
    )
    paragraphs = []
    for block in re.split(r"\n\s*\n", markdown):
        block = block.strip()
        if not block or HEADING_RE.match(block) or IMAGE_ONLY_RE.match(block):
            continue
        if block.startswith("<!--") and block.endswith("-->"):
            continue
        paragraphs.append(block)
    return paragraphs


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\$\^\{?\d+\}?\$", " ", text)
    text = re.sub(r"\[\d+(?:[-,]\d+)*\]", " ", text)
    return " ".join(TOKEN_RE.findall(text.casefold()))


def _contents_lines(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or not CONTENTS_RE.match(match.group(2).strip()):
            continue
        level = len(match.group(1))
        contents = []
        for candidate in lines[index + 1 :]:
            next_heading = HEADING_RE.match(candidate)
            if next_heading and len(next_heading.group(1)) <= level:
                break
            if candidate.lstrip().startswith('<!-- "type": "page-number"'):
                break
            contents.append(candidate)
        return contents
    raise ValidationError("文档中找不到 Contents / 目录")


def has_toc(markdown: str) -> bool:
    """Return whether the document declares a Contents/TOC heading."""
    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match and CONTENTS_RE.match(match.group(2).strip()):
            return True
    return False


def local_image_paths(markdown: str) -> list[str]:
    """Extract local Markdown image paths while ignoring remote/data URLs."""
    paths = []
    for match in MARKDOWN_IMAGE_RE.finditer(markdown):
        path = (match.group(1) or match.group(2)).strip()
        if path.startswith(("//", "#")) or re.match(
            r"^[a-z][a-z0-9+.-]*:", path, re.IGNORECASE
        ):
            continue
        paths.append(path)
    return paths


def validate_local_images_preserved(source: str, target: str) -> None:
    """Require source local images to remain, in order, with unchanged paths."""
    source_paths = local_image_paths(source)
    target_paths = local_image_paths(target)
    target_index = 0
    for source_index, path in enumerate(source_paths):
        try:
            target_index = target_paths.index(path, target_index) + 1
        except ValueError as error:
            remaining = target_paths[target_index:]
            location = f"第 {source_index + 1} 张图片"
            if path in target_paths:
                detail = "顺序已改变"
            elif remaining:
                detail = "缺失或路径已改变"
            else:
                detail = "缺失"
            raise ValidationError(
                f"本地图片引用{detail}（{location}）：{path}"
            ) from error


def _source_toc_titles(markdown: str) -> list[str]:
    titles = []
    for line in _contents_lines(markdown):
        stripped = line.strip()
        if not stripped:
            continue
        list_match = TOC_LIST_TITLE_RE.match(stripped)
        if list_match:
            titles.append(list_match.group(1).strip())
            continue
        unlabeled_match = TOC_UNLABELED_TITLE_RE.match(stripped)
        if unlabeled_match:
            titles.append(unlabeled_match.group(1).strip())
            continue
        if stripped.startswith(("#", "<!--")):
            continue
        titles.append(re.sub(r"^\d+\s+", "", stripped).strip())
    return titles


def validate_toc_titles_preserved(source: str, target: str) -> None:
    """Require every source TOC title to remain complete in the target TOC."""
    target_contents = normalize_for_toc_compare("\n".join(_contents_lines(target)))
    missing = [
        title
        for title in _source_toc_titles(source)
        if normalize_for_toc_compare(title) not in target_contents
    ]
    if missing:
        raise ValidationError("目录标题被截断或改写：" + "；".join(missing[:5]))


def validate_toc_categories_attested(raw_source: str, target: str) -> None:
    """Reject TOC category labels that do not exist as source structural labels."""
    source_labels = {
        normalize_for_toc_compare(re.sub(r"^#{1,6}\s+", "", line.strip()))
        for line in raw_source.splitlines()
        if line.strip() and len(line.strip()) <= 100
    }
    fabricated = []
    for line in _contents_lines(target):
        match = TOC_CATEGORY_RE.match(line)
        if not match:
            continue
        english_category = match.group(1).split(" / ", 1)[0].strip()
        if normalize_for_toc_compare(english_category) not in source_labels:
            fabricated.append(english_category)
    if fabricated:
        raise ValidationError("目录类别未获源文结构佐证：" + "；".join(fabricated[:5]))


def normalize_for_toc_compare(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[^\w\u3400-\u9fff]+", "", text, flags=re.UNICODE)


def validate_bilingual_source(
    source: str,
    bilingual: str,
    *,
    section: str | None = None,
) -> None:
    """Require every meaningful source paragraph in the bilingual output."""
    source_scope = _select_section(source, section)
    target_paragraphs = [_normalize(block) for block in _paragraphs(bilingual)]
    target_document = "\n".join(target_paragraphs)
    missing = []
    checked = 0
    for block in _paragraphs(source_scope):
        normalized = _normalize(block)
        tokens = normalized.split()
        if len(tokens) < 5:
            continue
        checked += 1
        if normalized in target_document:
            continue
        best_ratio = max(
            (SequenceMatcher(None, normalized, candidate).ratio() for candidate in target_paragraphs),
            default=0.0,
        )
        if best_ratio < 0.92:
            missing.append(" ".join(tokens[:14]))
    if checked == 0:
        raise ValidationError("源文档中没有可校验的正文段落")
    if missing:
        preview = "；".join(missing[:5])
        suffix = f"（另有 {len(missing) - 5} 段）" if len(missing) > 5 else ""
        raise ValidationError(f"双语文档疑似缺少 {len(missing)} 个源文段落：{preview}{suffix}")


def validate_document(
    source: str,
    bilingual: str,
    *,
    profile: str = "generic",
    section: str | None = None,
    raw_source: str | None = None,
) -> None:
    """Validate a bilingual package according to its input profile."""
    if profile not in {"generic", "pdf-rich"}:
        raise ValidationError(f"不支持的校验 profile：{profile}")

    validate_bilingual_source(source, bilingual, section=section)
    validate_local_images_preserved(source, bilingual)
    validate_no_image_metadata_or_escaped_dollars(bilingual)
    validate_no_unsafe_tildes(bilingual)
    validate_attributed_quotes_are_blockquoted(bilingual)
    validate_bilingual_list_items_paired(bilingual)

    source_has_toc = has_toc(source)
    if profile == "pdf-rich":
        validate_toc_titles_preserved(source, bilingual)
        validate_markdown_structure(source)
        validate_markdown_structure(bilingual)
    elif source_has_toc:
        validate_toc_titles_preserved(source, bilingual)

    if raw_source and (profile == "pdf-rich" or has_toc(raw_source)):
        validate_toc_titles_preserved(raw_source, source)
        validate_toc_titles_preserved(raw_source, bilingual)
        validate_toc_categories_attested(raw_source, source)
        validate_toc_categories_attested(raw_source, bilingual)


def validate_markdown_structure(markdown: str) -> None:
    """Apply the pdf-rich TOC and heading hierarchy checks."""
    lines = markdown.splitlines()
    previous_heading: tuple[int, str] | None = None
    previous_nonempty_was_heading = False

    inside_numbered_chapter = False
    for line in lines:
        if not line.strip():
            continue
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            if level == 1:
                if NUMBERED_CHAPTER_RE.match(title):
                    inside_numbered_chapter = True
                elif inside_numbered_chapter and END_MATTER_RE.match(title):
                    inside_numbered_chapter = False
                elif inside_numbered_chapter:
                    raise ValidationError(
                        "正文大章节内部出现 H1，章节内长论述标题应降为 H2："
                        + title
                    )
            if (
                previous_nonempty_was_heading
                and previous_heading is not None
                and previous_heading[0] == level
                and not (level == 1 and NUMBERED_CHAPTER_RE.match(title))
            ):
                raise ValidationError(
                    "发现相邻同级标题，疑似父子层级未下钻："
                    f"{previous_heading[1]} -> {title}"
                )
            previous_heading = (level, title)
            previous_nonempty_was_heading = True
        else:
            previous_nonempty_was_heading = False

    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or not CONTENTS_RE.match(match.group(2).strip()):
            continue
        level = len(match.group(1))
        items = []
        for candidate in lines[index + 1 :]:
            next_heading = HEADING_RE.match(candidate)
            if next_heading and len(next_heading.group(1)) <= level:
                break
            if candidate.lstrip().startswith("- "):
                items.append(candidate)
        malformed = [item for item in items if not TOC_ITEM_RE.match(item)]
        if malformed:
            raise ValidationError(
                "目录项必须为带真实类别或无类别的「加粗标题 · 页码」格式："
                + malformed[0].strip()
            )
        break


def validate_no_unsafe_tildes(markdown: str) -> None:
    """Reject approximation tildes and paired bare tildes outside code or URLs."""
    in_fence = False
    problems = []
    for number, line in enumerate(markdown.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        candidate = re.sub(r"`[^`]*`", "", line)
        candidate = re.sub(r"https?://\S+", "", candidate)
        approximation = re.search(r"(?<![\\~])~(?=\s*(?:\\?\$)?\d)", candidate)
        paired = re.search(r"(?<![\\~])~{1,2}[^~\n]+(?<!\\)~{1,2}", candidate)
        if approximation or paired:
            problems.append(f"L{number}: {line.strip()}")
    if problems:
        raise ValidationError(
            "发现可能触发删除线或表示近似值的裸 ~；近似值请改用 ≈："
            + "；".join(problems[:5])
        )


def validate_no_image_metadata_or_escaped_dollars(markdown: str) -> None:
    """Reject extraction-only image metadata and unnecessary escaped dollars."""
    in_fence = False
    problems = []
    metadata_re = re.compile(
        r"\[/?IMAGE\]|</?image_ocr>|(?:图片链接|图片标题|图片描述|图片OCR结果|图像 OCR)\s*[：:]",
        re.IGNORECASE,
    )
    for number, line in enumerate(markdown.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        candidate = re.sub(r"`[^`]*`", "", line)
        if metadata_re.search(candidate) or r"\$" in candidate:
            problems.append(f"L{number}: {line.strip()}")
    if problems:
        raise ValidationError(
            "发现图片提取元数据或非必要的转义美元符号；图片块只保留图片引用，"
            "普通金额使用 $："
            + "；".join(problems[:5])
        )


def validate_attributed_quotes_are_blockquoted(markdown: str) -> None:
    """Require explicit quote-plus-attribution groups to use standard blockquotes."""
    lines = markdown.splitlines()
    problems = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith(("“", '"')) or stripped.startswith(">"):
            continue
        following = [item.strip() for item in lines[index + 1 : index + 9] if item.strip()]
        if any("|" in item and not item.startswith(">") for item in following):
            problems.append(f"L{index + 1}: {stripped[:80]}")
    if problems:
        raise ValidationError(
            "发现未使用标准 > 引用块的「引语 + 署名」结构："
            + "；".join(problems[:5])
        )


def validate_bilingual_list_items_paired(markdown: str) -> None:
    """Require translated list items to pair English and Chinese on one line."""
    in_fence = False
    problems = []
    for number, line in enumerate(markdown.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = LIST_ITEM_RE.match(line)
        if not match:
            continue
        content = match.group(1)
        visible = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", content)
        visible = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", visible)
        visible = re.sub(r"https?://\S+", "", visible)
        visible = re.sub(r"[*_~`]", "", visible).strip()
        has_latin = bool(re.search(r"[A-Za-z]", visible))
        has_cjk = bool(re.search(r"[\u3400-\u9fff]", visible))
        if not (has_latin or has_cjk):
            continue
        if " / " not in content or not (has_latin and has_cjk):
            problems.append(f"L{number}: {line.strip()}")
    if problems:
        raise ValidationError(
            "双语列表必须逐项写在同一行，格式为「English / 中文」，"
            "禁止先列全部英文再列全部中文："
            + "；".join(problems[:5])
        )
