import datetime as dt
import hashlib
import json
import re
from pathlib import Path


PAGE_RULES = [
    ("papers", ["paper", "arxiv", "article", "journal", "conference", "survey", "review", "comparison", "literature"]),
    ("projects", ["project", "requirement", "proposal", "roadmap", "plan"]),
    ("code", ["repo", "repository", "code", "module", "api", "sdk", "package"]),
    ("tech-notes", ["deploy", "architecture", "interface", "config", "technical", "tooling", "manual"]),
    ("experiments", ["experiment", "benchmark", "evaluation", "result", "failure"]),
    ("meetings", ["meeting", "minutes", "transcript", "discussion"]),
    ("concepts", ["concept", "definition", "method", "theory"]),
    ("resources", ["resource", "note", "snippet", "chat", "idea", "link", "attachment"]),
]


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(text):
    text = str(text or "untitled").strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:80] or "untitled"


def sha256_text(text):
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def safe_relpath(path):
    value = str(path or "").replace("\\", "/").strip()
    while value.startswith("/"):
        value = value[1:]
    parts = [part for part in value.split("/") if part not in ("", ".")]
    if any(part == ".." for part in parts):
        raise ValueError(f"Invalid relative path: {path}")
    return "/".join(parts)


def classify_summary(title, source_type=""):
    haystack = f"{title} {source_type}".lower()
    for folder, keywords in PAGE_RULES:
        if any(keyword in haystack for keyword in keywords):
            return folder
    return "resources"


def extract_keywords(text):
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+-]{2,}", text or "")
    seen = []
    lowered = set()
    for token in tokens:
        key = token.lower()
        if key not in lowered:
            seen.append(token)
            lowered.add(key)
        if len(seen) >= 12:
            break
    return seen


def query_tokens(question):
    raw_tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+-]{2,}", question or "")
    tokens = set()
    for token in raw_tokens:
        lowered = token.lower()
        tokens.add(lowered)
        if re.fullmatch(r"[\u4e00-\u9fff]+", token) and len(token) > 3:
            for size in (2, 3, 4):
                for index in range(0, len(token) - size + 1):
                    tokens.add(token[index:index + size])
    return {token for token in tokens if token.strip()}


def strip_markdown_frontmatter(text):
    return re.sub(r"^---[\s\S]*?---\s*", "", text or "").strip()


def strip_frontmatter(text):
    return strip_markdown_frontmatter(text)


def unique(items):
    result = []
    seen = set()
    for item in items or []:
        if item in (None, ""):
            continue
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def read_json_file(path):
    if not path:
        return {}
    target = Path(path)
    if not target.exists():
        return {}
    raw = target.read_bytes()
    if not raw.strip():
        return {}
    return json.loads(raw.decode("utf-8-sig", errors="replace"))


def write_json_file(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data or {}, ensure_ascii=False, indent=2), encoding="utf-8")
