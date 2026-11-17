import json
import re
from pathlib import Path

from catalog import catalog_entry, catalog_from_raw, merge_catalog, render_index
from gitea_api import GiteaClient
from utils import extract_keywords, now, safe_relpath, sha256_text, strip_frontmatter, unique


ALLOWED_ROOTS = {
    "overview",
    "projects",
    "papers",
    "surveys",
    "code",
    "meetings",
    "experiments",
    "tech-notes",
    "notes",
    "concepts",
    "resources",
}

TYPE_BY_ROOT = {
    "overview": "overview",
    "projects": "project",
    "papers": "paper",
    "surveys": "survey",
    "code": "code",
    "meetings": "meeting",
    "experiments": "experiment",
    "tech-notes": "tech-note",
    "notes": "note",
    "concepts": "concept",
    "resources": "resource",
}
RELATION_ROOTS = ALLOWED_ROOTS | {"qa"}
RELATION_FIELDS = (
    ("relatedConcepts", "相关概念"),
    ("relatedResources", "相关资源"),
    ("relatedCodePages", "相关代码页"),
    ("relatedPages", "相关页面"),
)
MANIFEST_FORMAT = "research-kb-markdown-drafts/v1"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")


def apply_pages(payload, pages_doc, context=None, draft_dir=None, require_drafts=False):
    context = context or {}
    normalized_pages, items = validate_and_normalize_pages(
        pages_doc,
        context,
        draft_dir=draft_dir,
        require_drafts=require_drafts,
    )

    client = GiteaClient(payload)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    created = []
    updated = []
    entries = []
    commit = ""

    for page in normalized_pages:
        path = page["path"]
        content = build_page_content(payload, page, items)
        page["contentHash"] = sha256_text(strip_frontmatter(content))
        existed = client.exists(path)
        client.upsert_text(path, content, f"OpenClaw update {path}")
        commit = client.last_commit
        entry = catalog_entry(page)
        entries.append(entry)
        (updated if existed else created).append(entry)

    catalog = merge_catalog(catalog, entries)
    client.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "OpenClaw update catalog.json")
    commit = client.last_commit
    client.upsert_text("index.md", render_index(catalog), "OpenClaw update index.md")
    commit = client.last_commit

    snapshot = dict(context.get("snapshot") or {})
    if isinstance(pages_doc, dict) and not require_drafts:
        snapshot.update(pages_doc.get("snapshot") or {})
    snapshot.update({
        "entityPageCount": len([page for page in normalized_pages if page["path"].startswith("meetings/")]),
        "relatedPageUpdateCount": len([page for page in normalized_pages if not page["path"].startswith("meetings/")]),
        "archivedFiles": archived_paths(items),
    })

    return {
        "processedSources": sorted(items),
        "createdPages": created,
        "updatedPages": updated,
        "archivedFiles": archived_paths(items),
        "skippedSources": normalize_messages(context.get("skippedSources") or []) + normalize_messages((pages_doc or {}).get("skippedSources") if isinstance(pages_doc, dict) and not require_drafts else []),
        "incompleteItems": context.get("incompleteItems") or [],
        "errors": normalize_messages(context.get("errors") or []) + normalize_messages((pages_doc or {}).get("errors") if isinstance(pages_doc, dict) and not require_drafts else []),
        "commitId": commit,
        "snapshot": snapshot,
    }


def validate_page_manifest(pages_doc, context=None, draft_dir=None, require_drafts=True):
    normalized_pages, items = validate_and_normalize_pages(
        pages_doc,
        context or {},
        draft_dir=draft_dir,
        require_drafts=require_drafts,
    )
    meeting_pages = [page for page in normalized_pages if page["path"].startswith("meetings/")]
    return {
        "success": True,
        "validationOnly": True,
        "format": MANIFEST_FORMAT if require_drafts else "legacy-pages-json",
        "pageCount": len(normalized_pages),
        "meetingPageCount": len(meeting_pages),
        "relatedPageCount": len(normalized_pages) - len(meeting_pages),
        "coveredItemKeys": sorted(items),
    }


def validate_and_normalize_pages(pages_doc, context, draft_dir=None, require_drafts=False):
    if require_drafts:
        validate_manifest_format(pages_doc)
    pages = normalize_pages(pages_doc)
    if not pages:
        raise ValueError("OpenClaw page manifest must contain a non-empty pages[] array")

    items = {str(item.get("itemKey")): item for item in context.get("inputItems") or [] if item.get("itemKey")}
    if not items:
        raise ValueError("No Tencent Meeting inputItems available for apply")

    normalized_pages = []
    meeting_covered = set()
    seen_paths = set()
    for page in pages:
        hydrated = hydrate_page_from_draft(page, draft_dir, require_drafts)
        normalized = normalize_page(hydrated, items, strict_source_keys=require_drafts)
        if normalized["path"] in seen_paths:
            raise ValueError(f"Duplicate page path in manifest: {normalized['path']}")
        seen_paths.add(normalized["path"])
        normalized_pages.append(normalized)
        if normalized["path"].startswith("meetings/"):
            meeting_covered.update(normalized["sourceItemKeys"])

    missing = sorted({key for key, item in items.items() if item.get("readable", True)} - meeting_covered)
    if missing:
        raise ValueError("Every Tencent Meeting input item must appear in at least one meetings/ page; missing itemKeys: " + ", ".join(missing))
    return normalized_pages, items


def validate_manifest_format(pages_doc):
    if not isinstance(pages_doc, dict):
        raise ValueError("Tencent Meeting page manifest must be a JSON object")
    value = str(pages_doc.get("format") or pages_doc.get("formatVersion") or "")
    if value != MANIFEST_FORMAT:
        raise ValueError(f"Tencent Meeting page manifest format must be {MANIFEST_FORMAT}")


def hydrate_page_from_draft(page, draft_dir, require_drafts):
    page = dict(page)
    draft_file = page.get("draftFile")
    if not draft_file:
        if require_drafts:
            raise ValueError("Every manifest page must include draftFile")
        return page
    if not draft_dir:
        raise ValueError("draftDir is required when manifest pages use draftFile")
    if require_drafts and (page.get("content") or page.get("body")):
        raise ValueError(f"Manifest page {draft_file} must not embed content/body; write Markdown to the draft file")

    raw_draft_path = str(draft_file).replace("\\", "/").strip()
    if raw_draft_path.startswith("/") or re.match(r"^[A-Za-z]:", raw_draft_path):
        raise ValueError(f"draftFile must be a KB-relative path: {draft_file}")
    draft_path = validate_page_path(draft_file)
    declared_path = page.get("path")
    if declared_path and validate_page_path(declared_path) != draft_path:
        raise ValueError(f"Manifest path must match draftFile: {declared_path} != {draft_path}")

    root = Path(draft_dir).expanduser().resolve()
    target = (root / Path(*draft_path.split("/"))).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Draft file escapes draftDir: {draft_file}") from exc
    if not target.is_file():
        raise ValueError(f"Draft Markdown file does not exist: {draft_file}")
    try:
        content = target.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Draft Markdown file must be UTF-8: {draft_file}") from exc
    if not content.strip():
        raise ValueError(f"Draft Markdown file is empty: {draft_file}")

    page["path"] = draft_path
    page["draftFile"] = draft_path
    page["content"] = content
    return page


def normalize_pages(pages_doc):
    if isinstance(pages_doc, list):
        return pages_doc
    if not isinstance(pages_doc, dict):
        raise ValueError("pages JSON must be an object or array")
    pages = pages_doc.get("pages")
    if pages is None:
        pages = (pages_doc.get("createdPages") or []) + (pages_doc.get("updatedPages") or [])
    if not isinstance(pages, list):
        raise ValueError("pages must be a list")
    invalid = [index for index, page in enumerate(pages) if not isinstance(page, dict)]
    if invalid:
        raise ValueError("Every pages[] entry must be an object; invalid indexes: " + ", ".join(map(str, invalid)))
    return pages


def normalize_page(page, items, strict_source_keys=False):
    path = validate_page_path(page.get("path") or "")
    content = str(page.get("content") or page.get("body") or "").strip()
    if not content:
        raise ValueError(f"Page {path} is missing content/body")
    source_item_keys = source_keys_for_page(page, items, strict=strict_source_keys)
    if not source_item_keys:
        raise ValueError(f"Page {path} must include sourceItemKeys referencing Tencent Meeting input items")
    page = dict(page)
    page["path"] = path
    page["type"] = type_from_path(path) if strict_source_keys else (page.get("type") or type_from_path(path))
    page["title"] = title_from_content(content) or page.get("title") or title_from_path(path)
    page["kbType"] = kb_type_for_path(path) if strict_source_keys else (page.get("kbType") or kb_type_for_path(path))
    page["sourceItemKeys"] = source_item_keys
    derived_source_ids = [items[key].get("sourceId") for key in source_item_keys if key in items]
    page["sourceIds"] = unique(derived_source_ids if strict_source_keys else (as_list(page.get("sourceIds")) or derived_source_ids))
    page["projectIds"] = unique(as_list(page.get("projectIds")) or ["general"])
    page["keywords"] = unique(as_list(page.get("keywords")) or extract_keywords((page.get("title") or "") + "\n" + content))
    inferred = infer_relations(content, path)
    page["relatedConcepts"] = normalize_relation_paths(as_list(page.get("relatedConcepts")) + inferred["relatedConcepts"])
    page["relatedResources"] = normalize_relation_paths(as_list(page.get("relatedResources")) + inferred["relatedResources"])
    page["relatedCodePages"] = normalize_relation_paths(as_list(page.get("relatedCodePages")) + inferred["relatedCodePages"])
    page["relatedPages"] = normalize_relation_paths(as_list(page.get("relatedPages")) + inferred["relatedPages"])
    page["sourceStatus"] = "active" if strict_source_keys else (page.get("sourceStatus") or "active")
    return page


def validate_page_path(path):
    raw = str(path or "").replace("\\", "/").strip()
    if not raw or "\x00" in raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise ValueError(f"Page path must be a non-empty KB-relative path: {path}")
    value = safe_relpath(path)
    if not value.endswith(".md"):
        raise ValueError(f"Page path must end with .md: {path}")
    root = value.split("/", 1)[0]
    if root not in ALLOWED_ROOTS:
        raise ValueError(f"tencent_meeting_ingest cannot write {path}. Allowed roots: {', '.join(sorted(ALLOWED_ROOTS))}")
    return value


def source_keys_for_page(page, items, strict=False):
    raw = page.get("sourceItemKeys") or page.get("sourceItemKey") or page.get("itemKeys") or page.get("itemKey") or []
    if isinstance(raw, (str, int)):
        raw = [raw]
    if strict and not raw:
        raise ValueError(f"Manifest page {page.get('path') or page.get('draftFile') or '<unknown>'} must declare sourceItemKeys")
    keys = []
    for key in raw or []:
        matches = match_source_candidate(key, items)
        if strict and len(matches) != 1:
            raise ValueError(f"Unknown or ambiguous Tencent Meeting sourceItemKey: {key}")
        keys.extend(matches)
    for source in page.get("sources") or []:
        if not isinstance(source, dict):
            continue
        for candidate in [source.get("itemKey"), source.get("sourceItemKey"), source.get("recordFileId"), source.get("meetingRecordId"), source.get("sha256")]:
            keys.extend(match_source_candidate(candidate, items))
    if not keys and len(items) == 1:
        keys = list(items.keys())
    return unique(keys)


def title_from_content(content):
    match = re.search(r"^#\s+(.+?)\s*$", strip_frontmatter(content or ""), re.MULTILINE)
    return match.group(1).strip() if match else ""


def infer_relations(content, page_path):
    fields = {
        "relatedConcepts": [],
        "relatedResources": [],
        "relatedCodePages": [],
        "relatedPages": [],
    }
    candidates = list(WIKILINK_RE.findall(content or "")) + list(MARKDOWN_LINK_RE.findall(content or ""))
    for candidate in candidates:
        value = str(candidate or "").split("#", 1)[0].split("?", 1)[0].strip()
        if not value or "://" in value or value.startswith(("mailto:", "#")):
            continue
        normalized = normalize_relation_paths([value])
        if not normalized:
            continue
        path = normalized[0]
        if path == page_path:
            continue
        root = path.split("/", 1)[0]
        if root == "concepts":
            fields["relatedConcepts"].append(path)
        elif root == "resources":
            fields["relatedResources"].append(path)
        elif root == "code":
            fields["relatedCodePages"].append(path)
        else:
            fields["relatedPages"].append(path)
    return {key: unique(value) for key, value in fields.items()}


def match_source_candidate(candidate, items):
    key = str(candidate or "")
    if not key:
        return []
    if key in items:
        return [key]
    matches = [item_key for item_key, item in items.items() if str(item.get("sha256") or "") == key or str(item.get("recordFileId") or "") == key or str(item.get("meetingRecordId") or "") == key]
    return matches if len(matches) == 1 else []


def normalize_relation_paths(values):
    result = []
    for raw in as_list(values):
        value = raw
        if isinstance(raw, dict):
            value = raw.get("path") or raw.get("target") or raw.get("href") or ""
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value.startswith("[[") and "]]" in value:
            value = value[2:value.find("]]")]
        if "|" in value:
            value = value.split("|", 1)[0].strip()
        if not value:
            continue
        normalized_raw = value.replace("\\", "/")
        if "\x00" in normalized_raw or normalized_raw.startswith("/") or re.match(r"^[A-Za-z]:", normalized_raw):
            continue
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        try:
            path = safe_relpath(value)
        except ValueError:
            continue
        root = path.split("/", 1)[0]
        if root not in RELATION_ROOTS or path.startswith("source_files/") or "/" not in path:
            continue
        result.append(path)
    return unique(result)


def as_list(value):
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


def build_page_content(payload, page, items):
    body = strip_frontmatter(page.get("content") or page.get("body") or "")
    title = page.get("title") or title_from_path(page.get("path"))
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}".strip()
    body = append_relation_section(body, page)
    data = {
        "id": page.get("id") or page.get("path", "").replace("/", "-").replace(".md", ""),
        "title": title,
        "type": page.get("type") or type_from_path(page.get("path")),
        "kbType": page.get("kbType") or kb_type_for_path(page.get("path")),
        "projectIds": page.get("projectIds") or ["general"],
        "tags": as_list(page.get("tags")),
        "keywords": page.get("keywords") or extract_keywords(title + "\n" + body),
        "createdAt": page.get("createdAt") or now(),
        "updatedAt": now(),
        "generatedBy": "openclaw:tencent_meeting_ingest",
        "contentHash": sha256_text(body),
        "sourceStatus": page.get("sourceStatus") or "active",
        "relatedConcepts": page.get("relatedConcepts") or [],
        "relatedResources": page.get("relatedResources") or [],
        "relatedCodePages": page.get("relatedCodePages") or [],
        "relatedPages": page.get("relatedPages") or [],
        "sources": source_traces(payload, page, items),
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def append_relation_section(body, page):
    if any(heading in body for heading in ("## 关联页面", "## 知识关联", "## 相关页面")):
        return body
    lines = []
    seen = set()
    for field, label in RELATION_FIELDS:
        for raw in page.get(field) or []:
            path, title = relation_target(raw)
            if not path or path in seen:
                continue
            seen.add(path)
            lines.append(f"- {label}: [[{path}|{title}]]")
    if not lines:
        return body
    return body.rstrip() + "\n\n## 关联页面\n\n" + "\n".join(lines)


def relation_target(raw):
    title = ""
    value = raw
    if isinstance(raw, dict):
        title = str(raw.get("title") or raw.get("label") or "")
        value = raw.get("path") or raw.get("target") or ""
    if not isinstance(value, str):
        return "", ""
    value = value.strip()
    if value.startswith("[[") and "]]" in value:
        value = value[2:value.find("]]")]
    if "|" in value:
        value, alias = value.split("|", 1)
        title = title or alias.strip()
    if value.endswith(".md"):
        value = value[:-3]
    try:
        path = safe_relpath(value)
    except ValueError:
        return "", ""
    if not path or path.startswith("source_files/"):
        return "", ""
    return path, title or title_from_path(path)


def source_traces(payload, page, items):
    source = payload.get("source") or {}
    traces = []
    for key in page.get("sourceItemKeys") or []:
        item = items.get(key)
        if not item:
            continue
        traces.append({
            "sourceId": source.get("id") or payload.get("sourceId") or item.get("sourceId"),
            "sourceType": "tencent_meeting",
            "platform": "tencent_meeting",
            "title": item.get("title") or key,
            "originalPath": item.get("meetingId") or item.get("meetingCode") or "",
            "archivedPath": item.get("archivedPath") or "",
            "sha256": item.get("sha256") or "",
            "meetingId": item.get("meetingId") or "",
            "meetingCode": item.get("meetingCode") or "",
            "recordFileId": item.get("recordFileId") or "",
            "meetingRecordId": item.get("meetingRecordId") or "",
            "status": "active",
            "ingestedAt": now(),
        })
    return traces


def archived_paths(items):
    return unique([item.get("archivedPath") for item in items.values()])


def normalize_messages(items):
    result = []
    for item in items or []:
        if isinstance(item, str):
            result.append({"message": item})
        elif isinstance(item, dict):
            result.append(item)
    return result


def type_from_path(path):
    return TYPE_BY_ROOT.get(str(path or "").split("/", 1)[0], "wiki")


def kb_type_for_path(path):
    root = str(path or "").split("/", 1)[0]
    if root == "concepts":
        return "concept"
    if root == "resources":
        return "resource"
    if root == "projects":
        return "project"
    return "wiki"


def title_from_path(path):
    return str(path or "page.md").rsplit("/", 1)[-1].replace(".md", "")
