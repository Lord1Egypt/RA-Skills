import argparse
import hashlib
import errno
import json
import os
import re
import stat
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from dataclasses import dataclass, field as dataclass_field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ARXIV_REQUEST_DELAY_SECONDS = 3
_ACTIVE_LOCK_PATHS: set[str] = set()


@dataclass
class FieldConfig:
    name: str
    query: str


@dataclass
class Config:
    retention_days: int
    per_field_limit: int
    lookback_days: int
    sort_by: str
    sort_order: str
    summary_enabled: bool
    summary_provider: str
    deepseek_model: str
    deepseek_base_url: str
    request_timeout_seconds: int
    fields: list[FieldConfig]


@dataclass
class Paper:
    arxiv_id: str
    title: str
    authors: list[str]
    published: date
    updated: date
    abstract: str
    url: str
    pdf_url: str
    field: str
    matched_query: str


@dataclass
class Summary:
    status: str
    chinese_summary: str
    key_contributions: list[str]
    method_summary: str
    reading_reason: str
    warning: str | None = dataclass_field(
        default=None,
        compare=False,
        repr=False,
    )


def fallback_summary(paper: Paper) -> Summary:
    return Summary(
        status="abstract_only",
        chinese_summary=f"DeepSeek 不可用，以下为原始摘要：{paper.abstract}",
        key_contributions=["暂未生成（使用原始摘要作为备用）"],
        method_summary="DeepSeek 摘要暂不可用，未提取方法信息。",
        reading_reason="如需判断价值，请先直接阅读原始摘要。",
    )


def build_summary_prompt(paper: Paper) -> str:
    authors = "、".join(paper.authors) if paper.authors else "未知"
    return "\n".join(
        [
            "你是一名严谨的学术论文中文摘要助手。",
            "请基于下面的论文信息，用简洁、学术化的中文输出。",
            "不得编造原文没有的信息。",
            "请严格只返回 JSON 对象，且必须且只能包含以下 4 个键：",
            '- "chinese_summary"',
            '- "key_contributions"',
            '- "method_summary"',
            '- "reading_reason"',
            "要求：",
            "- chinese_summary：1-3 句中文概述。",
            "- key_contributions：1-3 条中文要点列表。",
            "- method_summary：1-2 句中文方法概述。",
            "- reading_reason：1 句中文说明为什么值得阅读。",
            "请输出严格 JSON，不要输出任何额外说明、Markdown 或代码围栏。",
            "论文信息：",
            f"- 标题：{paper.title}",
            f"- 领域：{paper.field}",
            f"- 作者：{authors}",
            f"- 摘要：{paper.abstract}",
        ]
    )


def _strip_json_code_fences(content: str) -> str:
    stripped = content.strip()
    fence_match = re.fullmatch(
        r"```(?:json)?\s*(.*?)\s*```",
        stripped,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if fence_match is not None:
        return fence_match.group(1).strip()
    return stripped


def parse_deepseek_summary(content: str) -> Summary:
    try:
        payload = json.loads(_strip_json_code_fences(content))
    except json.JSONDecodeError as exc:
        raise ValueError("DeepSeek summary must be valid JSON") from exc

    if not isinstance(payload, dict):
        raise ValueError("DeepSeek summary must be a JSON object")

    expected_keys = {
        "chinese_summary",
        "key_contributions",
        "method_summary",
        "reading_reason",
    }
    if set(payload) != expected_keys:
        raise ValueError("DeepSeek summary must contain exactly the expected keys")

    chinese_summary = payload["chinese_summary"]
    method_summary = payload["method_summary"]
    reading_reason = payload["reading_reason"]
    key_contributions = payload["key_contributions"]

    if not isinstance(chinese_summary, str) or not chinese_summary.strip():
        raise ValueError("chinese_summary must be a non-empty string")
    if not isinstance(method_summary, str) or not method_summary.strip():
        raise ValueError("method_summary must be a non-empty string")
    if not isinstance(reading_reason, str) or not reading_reason.strip():
        raise ValueError("reading_reason must be a non-empty string")
    if not isinstance(key_contributions, list) or not key_contributions:
        raise ValueError("key_contributions must be a non-empty list")

    normalized_key_contributions: list[str] = []
    for item in key_contributions:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "key_contributions must contain non-empty strings"
            )
        normalized_key_contributions.append(item.strip())

    return Summary(
        status="deepseek_generated",
        chinese_summary=chinese_summary.strip(),
        key_contributions=normalized_key_contributions,
        method_summary=method_summary.strip(),
        reading_reason=reading_reason.strip(),
    )


def summarize_with_deepseek(config: Config, paper: Paper, api_key: str) -> Summary:
    parsed_base_url = urllib.parse.urlsplit(config.deepseek_base_url)
    if (
        parsed_base_url.scheme != "https"
        or parsed_base_url.hostname is None
        or parsed_base_url.hostname.lower() != "api.deepseek.com"
        or parsed_base_url.username is not None
        or parsed_base_url.password is not None
        or parsed_base_url.query
        or parsed_base_url.fragment
        or parsed_base_url.port is not None
        or parsed_base_url.path not in {"", "/"}
    ):
        raise ValueError("Invalid DeepSeek base URL")

    request_payload = {
        "model": config.deepseek_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一名严谨的学术论文摘要器。"
                    "请只依据用户提供的论文信息输出结果。"
                ),
            },
            {
                "role": "user",
                "content": build_summary_prompt(paper),
            },
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        config.deepseek_base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=config.request_timeout_seconds,
    ) as response:
        response_payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(response_payload, dict):
        raise ValueError("Invalid DeepSeek response schema")

    choices = response_payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("Invalid DeepSeek response schema")

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise ValueError("Invalid DeepSeek response schema")

    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise ValueError("Invalid DeepSeek response schema")

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Invalid DeepSeek response schema")

    return parse_deepseek_summary(content)


def summarize_paper(config: Config, paper: Paper) -> Summary:
    if not config.summary_enabled or config.summary_provider != "deepseek":
        return fallback_summary(paper)

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return fallback_summary(paper)

    try:
        return summarize_with_deepseek(config, paper, api_key)
    except Exception as exc:
        summary = fallback_summary(paper)
        summary.warning = (
            "DeepSeek summary failed: "
            f"{_sanitize_log_message(f'{exc.__class__.__name__}: {exc}')}"
        )
        return summary


def sanitize_filename(value: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*]', " ", value)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized.rstrip(" .")


def _paper_note_arxiv_id_component(arxiv_id: str) -> str:
    sanitized = sanitize_filename(arxiv_id)
    if len(sanitized) <= 80:
        return sanitized
    return sanitized[:80].rstrip(" .")


def extract_arxiv_id(value: str) -> str:
    parsed = urllib.parse.urlsplit(value.strip())
    arxiv_id = parsed.path if parsed.scheme else value.strip()
    arxiv_id = arxiv_id.rstrip("/")
    for prefix in ("/abs/", "/pdf/"):
        if arxiv_id.startswith(prefix):
            arxiv_id = arxiv_id[len(prefix) :]
            break
    arxiv_id = arxiv_id.removesuffix(".pdf")
    return re.sub(r"v\d+$", "", arxiv_id)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def build_arxiv_search_query(query: str) -> str:
    tokens = re.findall(
        (
            r"submittedDate:\[[^\]]+\]|"
            r'(?:ti|au|abs|co|jr|cat|rn|id|all):"[^"]*"|'
            r'"[^"]*"|\(|\)|\bANDNOT\b|\bAND\b|\bOR\b|[^\s()]+'
        ),
        query,
        flags=re.IGNORECASE,
    )
    result: list[str] = []
    previous_was_term = False

    for token in tokens:
        upper_token = token.upper()
        if upper_token in {"AND", "ANDNOT", "OR"}:
            result.append(upper_token)
            previous_was_term = False
            continue

        if token == ")":
            result.append(token)
            previous_was_term = True
            continue

        if previous_was_term:
            result.append("AND")

        if token == "(":
            result.append(token)
            previous_was_term = False
        else:
            if re.match(
                r"^(?:ti|au|abs|co|jr|cat|rn|id|all):",
                token,
                flags=re.IGNORECASE,
            ) or re.match(
                r"^submittedDate:\[",
                token,
                flags=re.IGNORECASE,
            ):
                result.append(token)
            else:
                result.append(f"all:{token}")
            previous_was_term = True

    return " ".join(result)


def _parse_date(value: str) -> date:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date()


def _https_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    return urllib.parse.urlunsplit(
        ("https", parsed.netloc, parsed.path, parsed.query, parsed.fragment)
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_arxiv_feed(
    xml_text: str,
    field: str,
    matched_query: str,
) -> list[Paper]:
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)
    papers: list[Paper] = []

    for entry in root.findall("atom:entry", namespace):
        entry_id = entry.findtext("atom:id", default="", namespaces=namespace)
        arxiv_id = extract_arxiv_id(entry_id)
        pdf_url = ""
        for link in entry.findall("atom:link", namespace):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
                break

        authors = [
            normalize_space(name)
            for name in (
                author.findtext(
                    "atom:name",
                    default="",
                    namespaces=namespace,
                )
                for author in entry.findall("atom:author", namespace)
            )
            if name
        ]
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=normalize_space(
                    entry.findtext(
                        "atom:title",
                        default="",
                        namespaces=namespace,
                    )
                ),
                authors=authors,
                published=_parse_date(
                    entry.findtext(
                        "atom:published",
                        default="",
                        namespaces=namespace,
                    )
                ),
                updated=_parse_date(
                    entry.findtext(
                        "atom:updated",
                        default="",
                        namespaces=namespace,
                    )
                ),
                abstract=normalize_space(
                    entry.findtext(
                        "atom:summary",
                        default="",
                        namespaces=namespace,
                    )
                ),
                url=_https_url(entry_id),
                pdf_url=(
                    _https_url(pdf_url)
                    if pdf_url
                    else f"https://arxiv.org/pdf/{arxiv_id}"
                ),
                field=field,
                matched_query=matched_query,
            )
        )

    return papers


def fetch_arxiv_papers(config: Config, field: FieldConfig) -> list[Paper]:
    end = utc_now().astimezone(timezone.utc)
    start = end - timedelta(days=config.lookback_days)
    date_range = (
        f"submittedDate:[{start:%Y%m%d%H%M} TO {end:%Y%m%d%H%M}]"
    )
    search_query = (
        f"({build_arxiv_search_query(field.query)}) AND {date_range}"
    )
    parameters = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": config.per_field_limit,
            "sortBy": config.sort_by,
            "sortOrder": config.sort_order,
        }
    )
    request = urllib.request.Request(
        f"https://export.arxiv.org/api/query?{parameters}",
        headers={"User-Agent": "ObsidianArxivDaily/1.0"},
    )
    with urllib.request.urlopen(
        request,
        timeout=config.request_timeout_seconds,
    ) as response:
        xml_text = response.read().decode("utf-8")
    return parse_arxiv_feed(xml_text, field.name, field.query)


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def authors_yaml(authors: list[str]) -> str:
    return f"[{', '.join(yaml_quote(author) for author in authors)}]"


def markdown_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _scalar_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    return value


def parse_config(path: Path) -> Config:
    scalars: dict[str, str] = {}
    fields: list[FieldConfig] = []
    current_field: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or stripped == "fields:":
            continue

        if stripped.startswith("- "):
            if current_field is not None:
                fields.append(FieldConfig(**current_field))
            current_field = {}
            stripped = stripped[2:].strip()

        key, raw_value = stripped.split(":", 1)
        value = _scalar_value(raw_value)
        if current_field is None:
            scalars[key.strip()] = value
        else:
            current_field[key.strip()] = value

    if current_field is not None:
        fields.append(FieldConfig(**current_field))

    return Config(
        retention_days=int(scalars["retention_days"]),
        per_field_limit=int(scalars["per_field_limit"]),
        lookback_days=int(scalars["lookback_days"]),
        sort_by=scalars.get("sort_by", "submittedDate"),
        sort_order=scalars.get("sort_order", "descending"),
        summary_enabled=scalars["summary_enabled"].lower() == "true",
        summary_provider=scalars.get("summary_provider", "deepseek"),
        deepseek_model=scalars.get("deepseek_model", "deepseek-v4-pro"),
        deepseek_base_url=scalars.get(
            "deepseek_base_url",
            "https://api.deepseek.com",
        ),
        request_timeout_seconds=int(
            scalars.get("request_timeout_seconds", "60")
        ),
        fields=fields,
    )


def paper_note_path(root: Path, paper: Paper) -> Path:
    prefix = f"{paper.published.isoformat()} - "
    sanitized_arxiv_id = _paper_note_arxiv_id_component(paper.arxiv_id)
    suffix = f" ({sanitized_arxiv_id}).md"
    title = sanitize_filename(paper.title)
    title = title[: max(0, 180 - len(prefix) - len(suffix))].rstrip(" .")
    filename = f"{prefix}{title}{suffix}"
    return root / "papers" / str(paper.published.year) / filename


def render_paper_markdown(
    paper: Paper,
    summary: Summary,
    today: date,
) -> str:
    frontmatter = [
        "---",
        "type: arxiv-paper",
        f"arxiv_id: {yaml_quote(paper.arxiv_id)}",
        f"title: {yaml_quote(paper.title)}",
        f"authors: {authors_yaml(paper.authors)}",
        f"field: {yaml_quote(paper.field)}",
        f"matched_query: {yaml_quote(paper.matched_query)}",
        f"published: {paper.published.isoformat()}",
        f"updated: {paper.updated.isoformat()}",
        f"url: {yaml_quote(paper.url)}",
        f"pdf_url: {yaml_quote(paper.pdf_url)}",
        "status: new",
        f"summary_status: {summary.status}",
        f"created: {today.isoformat()}",
        "archived: false",
        "---",
    ]
    author_text = ", ".join(paper.authors)
    body = [
        f"# {paper.title}",
        "",
        "## 基本信息",
        f"- arXiv ID: {paper.arxiv_id}",
        f"- 作者: {author_text}",
        f"- 领域: {paper.field}",
        f"- 匹配查询: {paper.matched_query}",
        f"- 发布日期: {paper.published.isoformat()}",
        f"- 更新日期: {paper.updated.isoformat()}",
        f"- 链接: {paper.url}",
        f"- PDF: {paper.pdf_url}",
        "",
        "## 中文摘要",
        summary.chinese_summary,
        "",
        "## 关键贡献",
        markdown_bullets(summary.key_contributions),
        "",
        "## 方法简述",
        summary.method_summary,
        "",
        "## 值得阅读的原因",
        summary.reading_reason,
        "",
        "## 原始 Abstract",
        paper.abstract,
        "",
    ]
    return "\n".join(frontmatter + [""] + body)


def _available_paper_note_path(root: Path, paper: Paper) -> Path:
    intended = paper_note_path(root, paper)
    candidate = intended
    suffix_number = 2
    while candidate.exists():
        candidate = intended.with_name(
            f"{intended.stem} - {suffix_number}{intended.suffix}"
        )
        suffix_number += 1
    return candidate


def write_paper_note(
    root: Path,
    paper: Paper,
    summary: Summary,
    today: date,
    dry_run: bool,
) -> Path:
    path = _available_paper_note_path(root, paper)
    output_root = root / "papers"
    _assert_safe_output_path(output_root, path)
    if dry_run:
        return path

    content = render_paper_markdown(paper, summary, today)
    path.parent.mkdir(parents=True, exist_ok=True)
    _assert_safe_output_path(output_root, path)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            _assert_safe_output_path(output_root, temp_path)
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        while True:
            try:
                _assert_safe_output_path(output_root, path)
                os.link(temp_path, path)
                return path
            except FileExistsError:
                path = _available_paper_note_path(root, paper)
                _assert_safe_output_path(output_root, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()

def load_existing_arxiv_ids(root: Path) -> set[str]:
    arxiv_ids: set[str] = set()
    for notes_root in (root / "papers", root / "archive" / "papers"):
        if not notes_root.exists():
            continue
        for path in _iter_safe_markdown_files(notes_root):
            lines = path.read_text(encoding="utf-8").splitlines()
            if not lines or lines[0].strip() != "---":
                continue
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                match = re.match(r"^arxiv_id:\s*(.*?)\s*$", line)
                if match:
                    arxiv_ids.add(_scalar_value(match.group(1)))
                    break
    return arxiv_ids


def _is_junction(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    if callable(is_junction):
        try:
            if bool(is_junction()):
                return True
        except (OSError, NotImplementedError):
            pass

    try:
        stat_result = os.lstat(path)
    except (FileNotFoundError, NotADirectoryError, PermissionError, OSError):
        return False

    return bool(
        getattr(stat_result, "st_file_attributes", 0)
        & stat.FILE_ATTRIBUTE_REPARSE_POINT
    )


def _assert_safe_output_path(expected_root: Path, target: Path) -> None:
    if not target.is_relative_to(expected_root):
        raise ValueError(f"Unsafe output path outside {expected_root}")

    expected_resolved = expected_root.resolve(strict=False)
    target_resolved = target.resolve(strict=False)
    if not target_resolved.is_relative_to(expected_resolved):
        raise ValueError(f"Unsafe resolved output path outside {expected_root}")

    current = expected_root
    if current.exists() and (current.is_symlink() or _is_junction(current)):
        raise ValueError(f"Unsafe output root component: {current}")

    try:
        relative_parts = target.parent.relative_to(expected_root).parts
    except ValueError as exc:
        raise ValueError(f"Unsafe output path outside {expected_root}") from exc

    for part in relative_parts:
        current = current / part
        if current.exists() and (current.is_symlink() or _is_junction(current)):
            raise ValueError(f"Unsafe output path component: {current}")


def _iter_safe_markdown_files(root: Path):
    resolved_root = root.resolve()
    if not root.exists():
        return

    for current_dir, dirnames, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current_dir)
        safe_dirnames: list[str] = []
        for dirname in sorted(dirnames):
            child_dir = current_path / dirname
            if child_dir.is_symlink() or _is_junction(child_dir):
                continue
            try:
                resolved_child = child_dir.resolve()
            except OSError:
                continue
            if not resolved_child.is_relative_to(resolved_root):
                continue
            safe_dirnames.append(dirname)
        dirnames[:] = safe_dirnames

        for filename in sorted(filenames):
            if not filename.lower().endswith(".md"):
                continue
            child_file = current_path / filename
            if child_file.is_symlink() or _is_junction(child_file):
                continue
            try:
                resolved_child = child_file.resolve()
            except OSError:
                continue
            if not resolved_child.is_relative_to(resolved_root):
                continue
            yield child_file


def read_frontmatter_value(text: str, key: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    closing_index: int | None = None
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
        match = pattern.match(line)
        if match is not None:
            return _scalar_value(match.group(1))

    return None


def vault_wikilink(path: Path) -> str:
    normalized_path = path.as_posix().lstrip("/\\")
    return f"[[{normalized_path}]]"


def _frontmatter_bounds(text: str) -> tuple[list[str], int] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines, index
    return None


def _rewrite_frontmatter_field(text: str, key: str, value: str) -> str:
    bounds = _frontmatter_bounds(text)
    if bounds is None:
        return text

    lines, closing_index = bounds
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*")
    replacement_index: int | None = None
    for index in range(1, closing_index):
        if pattern.match(lines[index]):
            replacement_index = index
            break

    if replacement_index is None:
        lines.insert(closing_index, f"{key}: {value}")
    else:
        lines[replacement_index] = f"{key}: {value}"

    rewritten = "\n".join(lines)
    if text.endswith("\n"):
        rewritten += "\n"
    return rewritten


def _collision_free_path(intended: Path) -> Path:
    candidate = intended
    suffix_number = 2
    while candidate.exists():
        candidate = intended.with_name(
            f"{intended.stem} - {suffix_number}{intended.suffix}"
        )
        suffix_number += 1
    return candidate


def _project_wikilink_path(root: Path, path: Path) -> Path:
    try:
        relative_path = path.relative_to(root)
    except ValueError:
        relative_path = path
    return Path(root.name) / relative_path


def archive_old_papers(
    root: Path,
    retention_days: int,
    today: date,
    dry_run: bool,
) -> list[Path]:
    notes_root = root / "papers"
    if not notes_root.exists():
        return []

    archived_paths: list[Path] = []
    output_root = root / "archive" / "papers"
    for source_path in _iter_safe_markdown_files(notes_root):
        try:
            resolved_source = source_path.resolve()
        except OSError:
            continue
        if not resolved_source.is_relative_to(notes_root.resolve()):
            continue

        text = source_path.read_text(encoding="utf-8")
        archived_value = read_frontmatter_value(text, "archived")
        if archived_value is not None and archived_value.lower() == "true":
            continue

        published_value = read_frontmatter_value(text, "published")
        if published_value is None:
            continue
        try:
            published_date = date.fromisoformat(published_value)
        except ValueError:
            continue

        age = today - published_date
        if age.days <= retention_days:
            continue

        intended_destination = root / "archive" / "papers" / source_path.relative_to(notes_root)
        destination = _collision_free_path(intended_destination)
        _assert_safe_output_path(output_root, destination)
        archived_paths.append(destination)
        if dry_run:
            continue

        updated_text = _rewrite_frontmatter_field(text, "archived", "true")
        destination.parent.mkdir(parents=True, exist_ok=True)
        _assert_safe_output_path(output_root, destination)
        temp_path: Path | None = None
        moved = False
        try:
            while True:
                destination = _collision_free_path(intended_destination)
                _assert_safe_output_path(output_root, destination)
                try:
                    os.rename(source_path, destination)
                    moved = True
                    break
                except FileExistsError:
                    continue

            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    newline="\n",
                    dir=destination.parent,
                    suffix=".tmp",
                    delete=False,
                ) as temp_file:
                    temp_path = Path(temp_file.name)
                    _assert_safe_output_path(output_root, temp_path)
                    temp_file.write(updated_text)
                    temp_file.flush()
                    os.fsync(temp_file.fileno())

                _assert_safe_output_path(output_root, destination)
                os.replace(temp_path, destination)
                temp_path = None
            except Exception:
                if moved and destination.exists():
                    os.rename(destination, source_path)
                raise
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()

    return archived_paths

def _daily_item_line(root: Path, paper: Paper, path: Path, summary: Summary) -> str:
    link_path = _project_wikilink_path(root, path)
    summary_text = normalize_space(summary.chinese_summary)
    return f"- {vault_wikilink(link_path)} — {paper.title} — {summary_text}"


def _read_markdown_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    try:
        heading_index = lines.index(heading)
    except ValueError:
        return None

    section_lines: list[str] = []
    for line in lines[heading_index + 1 :]:
        if line.startswith("## "):
            break
        section_lines.append(line)

    section = "\n".join(section_lines).strip()
    return section or None


def _load_same_day_items(
    root: Path,
    today: date,
) -> list[tuple[Paper, Path, Summary]]:
    items: list[tuple[Paper, Path, Summary]] = []
    for notes_root in (root / "papers", root / "archive" / "papers"):
        if not notes_root.exists():
            continue
        for note_path in _iter_safe_markdown_files(notes_root):
            text = note_path.read_text(encoding="utf-8")
            if read_frontmatter_value(text, "created") != today.isoformat():
                continue

            arxiv_id = read_frontmatter_value(text, "arxiv_id")
            title = read_frontmatter_value(text, "title")
            field = read_frontmatter_value(text, "field")
            chinese_summary = _read_markdown_section(
                text,
                "## 中文摘要",
            )
            if not arxiv_id or not title or not field or not chinese_summary:
                continue

            paper = Paper(
                arxiv_id=arxiv_id,
                title=title,
                authors=[],
                published=today,
                updated=today,
                abstract="",
                url=read_frontmatter_value(text, "url") or "",
                pdf_url=read_frontmatter_value(text, "pdf_url") or "",
                field=field,
                matched_query=(
                    read_frontmatter_value(text, "matched_query") or ""
                ),
            )
            summary = Summary(
                status=(
                    read_frontmatter_value(text, "summary_status")
                    or "abstract_only"
                ),
                chinese_summary=chinese_summary,
                key_contributions=[],
                method_summary="",
                reading_reason="",
            )
            items.append((paper, note_path, summary))
    return items


def _merge_daily_items(
    stored_items: list[tuple[Paper, Path, Summary]],
    new_items: list[tuple[Paper, Path, Summary]],
) -> list[tuple[Paper, Path, Summary]]:
    merged: list[tuple[Paper, Path, Summary]] = []
    known_arxiv_ids: set[str] = set()
    for item in [*stored_items, *new_items]:
        arxiv_id = item[0].arxiv_id
        if arxiv_id not in known_arxiv_ids:
            merged.append(item)
            known_arxiv_ids.add(arxiv_id)
    return merged


def _load_same_day_archived_paths(root: Path, today: date) -> list[Path]:
    daily_path = root / "daily" / f"{today.isoformat()}.md"
    if not daily_path.exists():
        return []

    section = _read_markdown_section(
        daily_path.read_text(encoding="utf-8"),
        "## 今日归档",
    )
    if section is None:
        return []

    archive_root = root / "archive" / "papers"
    expected_prefix = f"{root.name}/archive/papers/"
    archived_paths: list[Path] = []
    for line in section.splitlines():
        match = re.fullmatch(r"- \[\[([^|\]#]+)\]\]", line.strip())
        if match is None:
            continue
        link_path = match.group(1)
        if not link_path.startswith(expected_prefix):
            continue
        archived_path = root.joinpath(*link_path.split("/")[1:])
        try:
            _assert_safe_output_path(archive_root, archived_path)
        except ValueError:
            continue
        archived_paths.append(archived_path)
    return archived_paths


def _merge_paths(stored_paths: list[Path], new_paths: list[Path]) -> list[Path]:
    merged: list[Path] = []
    known_paths: set[str] = set()
    for path in stored_paths + new_paths:
        path_key = os.path.normcase(str(path.resolve(strict=False)))
        if path_key not in known_paths:
            merged.append(path)
            known_paths.add(path_key)
    return merged


def write_daily_summary(
    root: Path,
    today: date,
    new_items: list[tuple[Paper, Path, Summary]],
    archived_paths: list[Path],
    dry_run: bool,
) -> Path:
    path = root / "daily" / f"{today.isoformat()}.md"
    output_root = root / "daily"
    _assert_safe_output_path(output_root, path)
    if dry_run:
        return path
    if not new_items and not archived_paths and path.exists():
        return path
    new_items = _merge_daily_items(
        _load_same_day_items(root, today),
        new_items,
    )
    archived_paths = _merge_paths(
        _load_same_day_archived_paths(root, today),
        archived_paths,
    )

    field_groups: dict[str, list[tuple[Paper, Path, Summary]]] = {}
    for paper, note_path, summary in new_items:
        field_groups.setdefault(paper.field, []).append((paper, note_path, summary))

    lines: list[str] = [
        f"# 每日 arXiv 论文速报 - {today.isoformat()}",
        "",
        "## 今日概览",
        f"- 新增论文总数：{len(new_items)}",
        f"- 今日归档：{len(archived_paths)}",
    ]

    if field_groups:
        lines.append("- 分领域统计：")
        for field, papers_in_field in field_groups.items():
            lines.append(f"  - {field}：{len(papers_in_field)}")
    else:
        lines.append("- 分领域统计：无")

    lines.extend(
        [
            "",
            "## 优先阅读",
        ]
    )
    if new_items:
        for paper, note_path, summary in new_items[:5]:
            lines.append(_daily_item_line(root, paper, note_path, summary))
    else:
        lines.append("- 今日没有新增论文。")

    lines.extend(
        [
            "",
            "## 分领域论文",
        ]
    )
    if field_groups:
        for field, papers_in_field in field_groups.items():
            lines.append(f"### {field}（{len(papers_in_field)}）")
            for paper, note_path, summary in papers_in_field:
                lines.append(_daily_item_line(root, paper, note_path, summary))
            lines.append("")
        if lines[-1] == "":
            lines.pop()
    else:
        lines.append("- 暂无分领域论文。")

    lines.extend(
        [
            "",
            "## 今日归档",
        ]
    )
    if archived_paths:
        for archived_path in archived_paths:
            link_path = _project_wikilink_path(root, archived_path)
            lines.append(f"- {vault_wikilink(link_path)}")
    else:
        lines.append("- 今日无归档。")

    lines.extend(
        [
            "",
            "## 运行信息",
            f"- 运行时间：{utc_now().astimezone().isoformat(timespec='seconds')}",
            f"- 日志：{vault_wikilink(Path(root.name) / 'logs' / f'{today.isoformat()}.log')}",
        ]
    )

    content = "\n".join(lines).rstrip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    _assert_safe_output_path(output_root, path)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            _assert_safe_output_path(output_root, temp_path)
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        _assert_safe_output_path(output_root, path)
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()

    return path


def _sanitize_log_message(message: str) -> str:
    sanitized = re.sub(r"[\r\n]+", " ", message)
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if api_key:
        sanitized = sanitized.replace(api_key, "[REDACTED]")
    sanitized = re.sub(r"(?i)\bBearer\s+\S+", "Bearer [REDACTED]", sanitized)
    return sanitized


def log_line(root: Path, today: date, message: str) -> None:
    logs_root = Path(root) / "logs"
    log_path = logs_root / f"{today.isoformat()}.log"
    _assert_safe_output_path(logs_root, log_path)
    logs_root.mkdir(parents=True, exist_ok=True)
    _assert_safe_output_path(logs_root, log_path)

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    line = f"[{timestamp}] {_sanitize_log_message(message)}\n"
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)


def _log_run_message(root: Path, today: date, message: str) -> None:
    log_line(root, today, _sanitize_log_message(message))


def _sort_papers_for_selection(papers: list[Paper]) -> list[Paper]:
    sorted_papers = sorted(papers, key=lambda paper: paper.arxiv_id)
    sorted_papers.sort(key=lambda paper: paper.updated, reverse=True)
    return sorted_papers


def _lock_file_path(root: Path) -> Path:
    lock_dir = Path(tempfile.gettempdir()) / "obsidian-arxiv-daily-locks"
    normalized_root = os.path.normcase(str(root.resolve(strict=False)))
    lock_name = hashlib.sha256(normalized_root.encode("utf-8")).hexdigest()
    return lock_dir / f"{lock_name}.lock"


@contextmanager
def _single_instance_lock(root: Path):
    lock_path = _lock_file_path(root)
    lock_dir = Path(tempfile.gettempdir()) / "obsidian-arxiv-daily-locks"
    if lock_path.parent != lock_dir:
        raise ValueError("Unsafe lock path")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_key = os.path.normcase(str(lock_path.resolve(strict=False)))
    if lock_key in _ACTIVE_LOCK_PATHS:
        raise BlockingIOError("Another arXiv daily run is already active")

    handle = None
    locked = False
    _ACTIVE_LOCK_PATHS.add(lock_key)
    try:
        handle = lock_path.open("a+b")
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"\0")
            handle.flush()
            os.fsync(handle.fileno())
        handle.seek(0)

        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                raise BlockingIOError(
                    "Another arXiv daily run is already active"
                ) from exc
            raise

        locked = True
        yield
    finally:
        try:
            if locked and handle is not None:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            if handle is not None:
                handle.close()
            _ACTIVE_LOCK_PATHS.discard(lock_key)


def run(
    root: Path,
    dry_run: bool = False,
    max_total: int | None = None,
) -> int:
    today = date.today()
    config_path = root / "config.yaml"

    try:
        with _single_instance_lock(root):
            try:
                config = parse_config(config_path)
            except Exception as exc:
                if not dry_run and root.exists():
                    try:
                        _log_run_message(
                            root,
                            today,
                            f"Run failed: {exc.__class__.__name__}: {exc}",
                        )
                    except Exception:
                        pass
                return 1

            try:
                existing_ids = load_existing_arxiv_ids(root)
            except Exception as exc:
                if not dry_run:
                    try:
                        _log_run_message(
                            root,
                            today,
                            f"Run failed: {exc.__class__.__name__}: {exc}",
                        )
                    except Exception:
                        pass
                return 1

            if not dry_run:
                try:
                    _log_run_message(
                        root,
                        today,
                        (
                            "Run started: "
                            f"fields={len(config.fields)} "
                            f"existing_ids={len(existing_ids)} "
                            f"max_total={max_total}"
                        ),
                    )
                except Exception:
                    pass

            selected_papers: list[Paper] = []
            seen_ids = set(existing_ids)
            successful_field_fetches = 0

            for field_index, field in enumerate(config.fields):
                if max_total is not None and len(selected_papers) >= max_total:
                    break

                if field_index > 0:
                    time.sleep(ARXIV_REQUEST_DELAY_SECONDS)

                try:
                    fetched_papers = fetch_arxiv_papers(config, field)
                except Exception as exc:
                    if not dry_run:
                        try:
                            _log_run_message(
                                root,
                                today,
                                (
                                    f"Field {field.name} fetch failed: "
                                    f"{exc.__class__.__name__}: {exc}"
                                ),
                            )
                        except Exception:
                            pass
                    continue

                successful_field_fetches += 1
                for paper in _sort_papers_for_selection(fetched_papers):
                    if paper.arxiv_id in seen_ids:
                        continue
                    if max_total is not None and len(selected_papers) >= max_total:
                        break
                    selected_papers.append(paper)
                    seen_ids.add(paper.arxiv_id)

            if config.fields and successful_field_fetches == 0:
                if not dry_run:
                    try:
                        _log_run_message(
                            root,
                            today,
                            (
                                "Run failed: all configured arXiv "
                                "field fetches failed"
                            ),
                        )
                    except Exception:
                        pass
                return 1

            if dry_run:
                try:
                    archived_paths = archive_old_papers(
                        root,
                        config.retention_days,
                        today,
                        dry_run=True,
                    )
                    write_daily_summary(
                        root,
                        today,
                        new_items=[],
                        archived_paths=archived_paths,
                        dry_run=True,
                    )
                    print("Dry run preview")
                    print(f"Selected new papers ({len(selected_papers)}):")
                    for paper in selected_papers:
                        note_path = _available_paper_note_path(root, paper)
                        relative_note_path = note_path.relative_to(root).as_posix()
                        print(
                            f"- {paper.arxiv_id} | {paper.title} "
                            f"-> {relative_note_path}"
                        )
                    print(f"Archive candidates ({len(archived_paths)}):")
                    for archived_path in archived_paths:
                        relative_archive_path = archived_path.relative_to(root)
                        print(f"- {relative_archive_path.as_posix()}")
                except Exception:
                    return 1
                return 0

            new_items: list[tuple[Paper, Path, Summary]] = []
            for paper in selected_papers:
                try:
                    summary = summarize_paper(config, paper)
                    if summary.warning:
                        try:
                            _log_run_message(
                                root,
                                today,
                                f"Paper {paper.arxiv_id} {summary.warning}",
                            )
                        except Exception:
                            pass
                    note_path = write_paper_note(
                        root,
                        paper,
                        summary,
                        today,
                        dry_run=False,
                    )
                except Exception as exc:
                    try:
                        _log_run_message(
                            root,
                            today,
                            (
                                f"Paper {paper.arxiv_id} processing failed: "
                                f"{exc.__class__.__name__}: {exc}"
                            ),
                        )
                    except Exception:
                        pass
                    continue
                new_items.append((paper, note_path, summary))

            try:
                archived_paths = archive_old_papers(
                    root,
                    config.retention_days,
                    today,
                    dry_run=False,
                )
            except Exception as exc:
                try:
                    _log_run_message(
                        root,
                        today,
                        f"Run failed: {exc.__class__.__name__}: {exc}",
                    )
                except Exception:
                    pass
                return 1

            try:
                write_daily_summary(
                    root,
                    today,
                    new_items=new_items,
                    archived_paths=archived_paths,
                    dry_run=False,
                )
            except Exception as exc:
                try:
                    _log_run_message(
                        root,
                        today,
                        (
                            "Daily summary failed: "
                            f"{exc.__class__.__name__}: {exc}"
                        ),
                    )
                except Exception:
                    pass
                return 1

            try:
                _log_run_message(
                    root,
                    today,
                    (
                        "Run completed: "
                        f"selected={len(selected_papers)} "
                        f"written={len(new_items)} "
                        f"archived={len(archived_paths)}"
                    ),
                )
            except Exception:
                pass
            return 0
    except BlockingIOError:
        if not dry_run:
            try:
                _log_run_message(
                    root,
                    today,
                    "Another arXiv daily run is already active",
                )
            except Exception:
                pass
        return 1
    except Exception as exc:
        if not dry_run and root.exists():
            try:
                _log_run_message(
                    root,
                    today,
                    f"Run failed: {exc.__class__.__name__}: {exc}",
                )
            except Exception:
                pass
        return 1


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError(
            "--max-total must be greater than zero"
        )
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="arxiv_daily")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--max-total",
        type=_positive_int,
        default=None,
    )
    args = parser.parse_args(argv)
    return run(
        Path(args.root),
        dry_run=args.dry_run,
        max_total=args.max_total,
    )


if __name__ == "__main__":
    raise SystemExit(main())
