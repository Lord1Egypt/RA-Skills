#!/usr/bin/env python3
"""Synchronize the current navigation-visible DeBox documentation."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


SCRIPT_VERSION = "1.1.0"
SCHEMA_VERSION = 1
BASE_URL = "https://docs.debox.pro"
START_URLS = {"zh": f"{BASE_URL}/UserGuide", "en": f"{BASE_URL}/en/UserGuide"}
USER_AGENT = f"sync-debox-docs/{SCRIPT_VERSION}"
MARKER = ".sync-debox-docs.json"
MANAGED_ROOTS = ("markdown", "images", "reports")
MANAGED_FILES = (MARKER, "manifest.json", "index.md", "update-report.md")
TIMEOUT = 25
MAX_HTML_BYTES = 12 * 1024 * 1024
MAX_IMAGE_BYTES = 25 * 1024 * 1024


def timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def stamp_name() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d-%H%M%S")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    path = unquote(parts.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def request_url(url: str) -> str:
    parts = urlsplit(url)
    path = quote(unquote(parts.path or "/"), safe="/:@-._~!$&'()*+,;=")
    query = quote(unquote(parts.query), safe="=&?/:@-._~!$'()*+,;")
    return urlunsplit((parts.scheme, parts.netloc, path, query, ""))


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value).replace("\x00", "")).strip()


def fetch(url: str, max_bytes: int, accept: str = "*/*") -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            request = Request(request_url(url), headers={"User-Agent": USER_AGENT, "Accept": accept})
            with urlopen(request, timeout=TIMEOUT) as response:
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError(f"response exceeds size limit: {url}")
                return data, response.headers.get_content_type()
        except HTTPError as exc:
            if exc.code < 500:
                raise
            last_error = exc
        except (URLError, TimeoutError, OSError) as exc:
            last_error = exc
        if attempt < 2:
            time.sleep(attempt + 1)
    assert last_error is not None
    raise last_error


def fetch_html(url: str) -> str:
    data, content_type = fetch(url, MAX_HTML_BYTES, "text/html,application/xhtml+xml")
    if content_type not in {"text/html", "application/xhtml+xml"}:
        raise ValueError(f"expected HTML but received {content_type}: {url}")
    return data.decode("utf-8", errors="replace")


class NavigationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.current_href: str | None = None
        self.current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and "menu__link" in (values.get("class") or "").split() and values.get("href"):
            self.current_href = values["href"]
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_href is not None:
            self.links.append((self.current_href, clean_text(" ".join(self.current_text))))
            self.current_href = None
            self.current_text = []


class ArticleDataParser(HTMLParser):
    BLOCKED = {"script", "style", "noscript", "svg", "canvas", "nav", "footer", "header", "button"}

    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.article_depth = 0
        self.blocked_depth = 0
        self.title_depth = 0
        self.title_done = False
        self.title_parts: list[str] = []
        self.links: list[str] = []
        self.images: list[tuple[str, str]] = []
        self.events: list[tuple[str, object]] = []

    def active(self) -> bool:
        return self.article_depth > 0 and self.blocked_depth == 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "article":
            self.article_depth += 1
        if tag in self.BLOCKED:
            self.blocked_depth += 1
            return
        if not self.active():
            return
        if re.fullmatch(r"h[1-6]", tag) and not self.title_done:
            self.title_depth = 1
        if tag == "a" and values.get("href"):
            link = urljoin(self.base_url, values["href"])
            self.links.append(link)
            self.events.append(("start", (tag, link)))
        elif tag == "img" and values.get("src"):
            source = urljoin(self.base_url, values["src"])
            alt = clean_text(values.get("alt") or "image")
            self.images.append((source, alt))
            self.events.append(("image", (source, alt)))
        else:
            self.events.append(("start", (tag, None)))

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCKED:
            self.blocked_depth = max(0, self.blocked_depth - 1)
            return
        if self.active():
            self.events.append(("end", tag))
        if re.fullmatch(r"h[1-6]", tag) and self.title_depth:
            self.title_depth = 0
            self.title_done = True
        if tag == "article":
            self.article_depth = max(0, self.article_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.active():
            data = data.replace("\x00", "")
            self.events.append(("text", data))
            if self.title_depth:
                self.title_parts.append(data)

    @property
    def title(self) -> str:
        return clean_text(" ".join(self.title_parts))


class MarkdownRenderer:
    def __init__(self, page_url: str, page_files: dict[str, str], image_files: dict[str, str]) -> None:
        self.page_url = page_url
        self.page_files = page_files
        self.image_files = image_files
        self.output: list[str] = []
        self.list_stack: list[str] = []
        self.link_stack: list[str | None] = []
        self.pre_depth = 0
        self.table_rows: list[list[str]] = []
        self.table_row: list[str] | None = None
        self.table_cell: list[str] | None = None

    def write(self, value: str) -> None:
        if self.table_cell is not None:
            self.table_cell.append(value)
        else:
            self.output.append(value)

    def newline(self, count: int = 1) -> None:
        self.write("\n" * count)

    def local_page_link(self, url: str) -> str:
        normalized = normalize_url(url)
        target = self.page_files.get(normalized)
        if not target:
            return url
        current = PurePosixPath(self.page_files[self.page_url]).parent
        return os.path.relpath(target, current.as_posix()).replace("\\", "/")

    def local_image_link(self, target: str) -> str:
        current = PurePosixPath(self.page_files[self.page_url]).parent
        return os.path.relpath(target, current.as_posix()).replace("\\", "/")

    def render(self, events: Iterable[tuple[str, object]]) -> str:
        for kind, payload in events:
            if kind == "text":
                data = str(payload)
                if self.pre_depth:
                    self.write(data)
                else:
                    text = re.sub(r"\s+", " ", data)
                    if text.strip():
                        self.write(text)
                continue
            if kind == "image":
                source, alt = payload  # type: ignore[misc]
                target = self.image_files.get(source)
                self.write(f"![{alt}]({self.local_image_link(target)})" if target else f"![{alt}]({source})")
                continue
            if kind == "start":
                tag, value = payload  # type: ignore[misc]
                self.start(tag, value)
            elif kind == "end":
                self.end(str(payload))
        text = html.unescape("".join(self.output))
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" +([,.;:!?，。；：！？])", r"\1", text)
        return text.strip() + "\n"

    def start(self, tag: str, value: str | None) -> None:
        if re.fullmatch(r"h[1-6]", tag):
            self.newline(2)
            self.write("#" * int(tag[1]) + " ")
        elif tag in {"p", "div", "section", "aside", "blockquote", "details", "summary"}:
            self.newline(2)
            if tag == "blockquote":
                self.write("> ")
        elif tag == "br":
            self.newline()
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
            self.newline()
        elif tag == "li":
            self.newline()
            marker = "1. " if self.list_stack and self.list_stack[-1] == "ol" else "- "
            self.write("  " * max(0, len(self.list_stack) - 1) + marker)
        elif tag in {"strong", "b"}:
            self.write("**")
        elif tag in {"em", "i"}:
            self.write("*")
        elif tag == "a":
            self.link_stack.append(value)
            self.write("[")
        elif tag == "pre":
            self.pre_depth += 1
            self.newline(2)
            self.write("```\n")
        elif tag == "code" and not self.pre_depth:
            self.write("`")
        elif tag == "table":
            self.table_rows = []
        elif tag == "tr":
            self.table_row = []
        elif tag in {"td", "th"} and self.table_row is not None:
            self.table_cell = []

    def end(self, tag: str) -> None:
        if re.fullmatch(r"h[1-6]", tag) or tag in {"p", "section", "aside", "blockquote", "details", "summary"}:
            self.newline(2)
        elif tag == "div":
            self.newline()
        elif tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self.newline()
        elif tag in {"strong", "b"}:
            self.write("**")
        elif tag in {"em", "i"}:
            self.write("*")
        elif tag == "a":
            url = self.link_stack.pop() if self.link_stack else None
            self.write(f"]({self.local_page_link(url)})" if url else "]")
        elif tag == "pre":
            self.pre_depth = max(0, self.pre_depth - 1)
            self.write("\n```\n\n")
        elif tag == "code" and not self.pre_depth:
            self.write("`")
        elif tag in {"td", "th"} and self.table_cell is not None and self.table_row is not None:
            self.table_row.append(clean_text("".join(self.table_cell)))
            self.table_cell = None
        elif tag == "tr" and self.table_row is not None:
            self.table_rows.append(self.table_row)
            self.table_row = None
        elif tag == "table":
            self.flush_table()

    def flush_table(self) -> None:
        if not self.table_rows:
            return
        width = max(len(row) for row in self.table_rows)
        rows = [row + [""] * (width - len(row)) for row in self.table_rows]
        self.newline(2)
        self.write("| " + " | ".join(rows[0]) + " |\n")
        self.write("| " + " | ".join(["---"] * width) + " |\n")
        for row in rows[1:]:
            self.write("| " + " | ".join(row) + " |\n")
        self.newline()


def safe_page_file(url: str, used: set[str]) -> str:
    path = unquote(urlsplit(url).path).strip("/") or "index"
    parts = [re.sub(r"[^A-Za-z0-9._-]+", "-", part).strip("-") or "page" for part in path.split("/")]
    candidate = "/".join(parts) + ".md"
    if candidate.lower() in used:
        candidate = "/".join(parts) + "-" + sha256(url.encode())[:8] + ".md"
    used.add(candidate.lower())
    return f"markdown/{candidate}"


def image_file(url: str, content_type: str) -> str:
    suffix = Path(unquote(urlsplit(url).path)).suffix.lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,8}", suffix):
        suffix = {
            "image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
            "image/webp": ".webp", "image/svg+xml": ".svg",
        }.get(content_type, ".bin")
    return f"images/{sha256(url.encode())[:24]}{suffix}"


def frontmatter(title: str, source_url: str, fetched_at: str) -> str:
    return (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"source_url: {json.dumps(source_url, ensure_ascii=False)}\n"
        f"fetched_at: {json.dumps(fetched_at)}\n"
        "---\n\n"
    )


def discover_navigation(language: str) -> list[dict[str, str]]:
    start_url = START_URLS[language]
    parser = NavigationParser()
    parser.feed(fetch_html(start_url))
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for href, label in parser.links:
        url = normalize_url(urljoin(start_url, href))
        parts = urlsplit(url)
        if parts.scheme != "https" or parts.netloc != "docs.debox.pro":
            continue
        if language == "en" and not parts.path.startswith("/en/"):
            continue
        if language == "zh" and parts.path.startswith("/en/"):
            continue
        if url not in seen:
            seen.add(url)
            pages.append({"url": url, "label": label or parts.path.rsplit("/", 1)[-1]})
    if len(pages) < 10 or normalize_url(start_url) not in seen:
        raise ValueError("DeBox navigation could not be recognized safely")
    return pages


def validate_output(output: Path, language: str, create: bool) -> None:
    if output.exists() and not output.is_dir():
        raise ValueError("output path exists but is not a folder")
    if not output.exists():
        if not create:
            output.parent.mkdir(parents=True, exist_ok=True)
            probe = output.parent / f".sync-debox-write-test-{os.getpid()}"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return
        output.mkdir(parents=True)
    entries = list(output.iterdir())
    marker_path = output / MARKER
    if entries and not marker_path.exists():
        raise ValueError("output folder is not empty and is not managed by sync-debox-docs")
    if marker_path.exists():
        marker = json.loads(marker_path.read_text(encoding="utf-8-sig"))
        if marker.get("language") != language:
            raise ValueError(
                f"output folder contains {marker.get('language')} documentation; choose a different folder for {language}"
            )
    probe = output / f".sync-debox-write-test-{os.getpid()}"
    probe.write_text("ok", encoding="utf-8")
    probe.unlink()
    free = shutil.disk_usage(output).free
    if free < 100 * 1024 * 1024:
        raise ValueError("less than 100 MiB free disk space is available")


def load_manifest(output: Path) -> dict:
    path = output / "manifest.json"
    if not path.exists():
        return {"pages": {}, "images": {}}
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("manifest schema version is not supported by this script")
    return value


def check_link(url: str) -> str | None:
    if urlsplit(url).scheme not in {"http", "https"}:
        return None
    try:
        url = urlunsplit((*urlsplit(url)[:4], ""))
        request = Request(request_url(url), method="HEAD", headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=TIMEOUT) as response:
            if response.status >= 400:
                return f"{url}: HTTP {response.status}"
        return None
    except HTTPError as exc:
        if exc.code in {403, 405}:
            try:
                request = Request(request_url(url), headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"})
                with urlopen(request, timeout=TIMEOUT):
                    return None
            except Exception as retry_exc:  # noqa: BLE001
                return f"{url}: {retry_exc}"
        return f"{url}: HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return f"{url}: {exc}"


def self_check(language: str, output: Path) -> None:
    if sys.version_info < (3, 10):
        raise ValueError("Python 3.10 or newer is required")
    validate_output(output, language, create=False)
    pages = discover_navigation(language)
    sample = fetch_html(pages[0]["url"])
    parser = ArticleDataParser(pages[0]["url"])
    parser.feed(sample)
    if not parser.events or not parser.title:
        raise ValueError("DeBox document article content could not be recognized")
    print(json.dumps({
        "success": True,
        "script_version": SCRIPT_VERSION,
        "language": language,
        "navigation_pages": len(pages),
        "output": str(output.resolve()),
    }, ensure_ascii=False, indent=2))


def report_text(language: str, complete: bool, added: list[str], changed: list[str], removed: list[str],
                broken_links: list[str], broken_images: list[str], errors: list[str]) -> str:
    sections = [
        "# DeBox Documentation Sync Report", "",
        f"- Time: {timestamp()}",
        f"- Language: {language}",
        f"- Complete: {'yes' if complete else 'no'}",
        f"- Script version: {SCRIPT_VERSION}",
    ]
    for heading, values in (
        ("Added pages", added), ("Changed pages", changed), ("Removed pages", removed),
        ("Broken links", broken_links), ("Broken images", broken_images), ("Errors", errors),
    ):
        sections.extend(["", f"## {heading}", ""])
        sections.extend([f"- {value}" for value in values] or ["- None"])
    return "\n".join(sections) + "\n"


def sync(language: str, output: Path) -> None:
    validate_output(output, language, create=True)
    old = load_manifest(output)
    pages = discover_navigation(language)
    fetched_at = timestamp()
    used_files: set[str] = set()
    page_files = {page["url"]: safe_page_file(page["url"], used_files) for page in pages}
    errors: list[str] = []
    broken_images: list[str] = []
    parsed_pages: dict[str, ArticleDataParser] = {}
    image_sources: dict[str, tuple[bytes, str]] = {}
    image_usage: dict[str, set[str]] = {}
    image_alts: dict[str, set[str]] = {}
    all_links: set[str] = set()

    with tempfile.TemporaryDirectory(prefix="sync-debox-docs-") as temp_name:
        stage = Path(temp_name)
        for page in pages:
            try:
                raw = fetch_html(page["url"])
                parser = ArticleDataParser(page["url"])
                parser.feed(raw)
                plain = clean_text(" ".join(str(payload) for kind, payload in parser.events if kind == "text"))
                if not parser.title or len(plain) < 80:
                    raise ValueError("article content is empty or invalid")
                parsed_pages[page["url"]] = parser
                all_links.update(parser.links)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{page['url']}: {exc}")

        for parser in parsed_pages.values():
            for source, alt in parser.images:
                image_usage.setdefault(source, set()).add(parser.base_url)
                if alt:
                    image_alts.setdefault(source, set()).add(alt)
                if source in image_sources:
                    continue
                try:
                    data, content_type = fetch(source, MAX_IMAGE_BYTES, "image/*")
                    if not content_type.startswith("image/"):
                        raise ValueError(f"expected image but received {content_type}")
                    image_sources[source] = (data, content_type)
                except Exception as exc:  # noqa: BLE001
                    broken_images.append(f"{source}: {exc}")

        image_files = {source: entry["file"] for source, entry in old.get("images", {}).items()}
        image_files.update({
            source: image_file(source, content_type)
            for source, (_data, content_type) in image_sources.items()
        })
        new_pages: dict[str, dict] = {}
        new_images: dict[str, dict] = {}
        for url, parser in parsed_pages.items():
            markdown = MarkdownRenderer(url, page_files, image_files).render(parser.events)
            body = frontmatter(parser.title, url, fetched_at) + markdown
            data = body.encode("utf-8")
            target = stage / page_files[url]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            new_pages[url] = {
                "title": parser.title,
                "file": page_files[url],
                "sha256": sha256((parser.title + "\n" + markdown).encode("utf-8")),
            }
        for source, (data, content_type) in image_sources.items():
            target = stage / image_files[source]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            new_images[source] = {
                "file": image_files[source],
                "content_type": content_type,
                "sha256": sha256(data),
                "used_by": sorted(image_usage.get(source, set())),
                "alt_texts": sorted(image_alts.get(source, set())),
            }

        complete = not errors and not broken_images and len(new_pages) == len(pages)
        old_pages = old.get("pages", {})
        old_images = old.get("images", {})
        added = sorted(set(new_pages) - set(old_pages))
        changed = sorted(
            url for url in set(new_pages) & set(old_pages)
            if new_pages[url]["sha256"] != old_pages[url].get("sha256")
        )
        removed = sorted(set(old_pages) - set(new_pages)) if complete else []
        unchanged_files = {
            entry["file"] for url, entry in new_pages.items()
            if url in old_pages and entry["sha256"] == old_pages[url].get("sha256")
        } | {
            entry["file"] for url, entry in new_images.items()
            if url in old_images and entry["sha256"] == old_images[url].get("sha256")
        }

        check_urls = sorted({
            urlunsplit((*urlsplit(url)[:4], ""))
            for url in all_links
            if urlsplit(url).scheme in {"http", "https"}
        })
        with ThreadPoolExecutor(max_workers=12) as pool:
            broken_links = sorted(filter(None, pool.map(check_link, check_urls)))
        report = report_text(language, complete, added, changed, removed, broken_links, broken_images, errors)

        for group in ("markdown", "images"):
            source_root = stage / group
            if source_root.exists():
                for source in source_root.rglob("*"):
                    if source.is_file():
                        relative = source.relative_to(stage)
                        if relative.as_posix() in unchanged_files:
                            continue
                        destination = output / relative
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        sibling_temp = destination.with_name(f".{destination.name}.sync-debox-temp")
                        shutil.copy2(source, sibling_temp)
                        os.replace(sibling_temp, destination)

        if complete:
            current_files = {entry["file"] for entry in new_pages.values()} | {entry["file"] for entry in new_images.values()}
            old_files = {entry["file"] for entry in old_pages.values()} | {entry["file"] for entry in old_images.values()}
            for relative in old_files - current_files:
                target = (output / relative).resolve()
                if output.resolve() in target.parents and target.exists():
                    target.unlink()
        else:
            for url, entry in old_pages.items():
                new_pages.setdefault(url, entry)
            for url, entry in old_images.items():
                new_images.setdefault(url, entry)

        index = ["# DeBox Documentation Index", "", f"- Language: {language}", f"- Updated: {fetched_at}", "", "## Pages", ""]
        for url, entry in sorted(new_pages.items(), key=lambda item: item[1]["title"].lower()):
            index.append(f"- [{entry['title']}]({entry['file']}) - {url}")
        (output / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")

        reports = output / "reports"
        reports.mkdir(exist_ok=True)
        (output / "update-report.md").write_text(report, encoding="utf-8")
        (reports / f"{stamp_name()}.md").write_text(report, encoding="utf-8")
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "script_version": SCRIPT_VERSION,
            "language": language,
            "source": START_URLS[language],
            "last_sync": fetched_at,
            "complete": complete,
            "pages": new_pages,
            "images": new_images,
            "broken_links": broken_links,
            "broken_images": broken_images,
            "errors": errors,
        }
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / MARKER).write_text(json.dumps({
            "owner": "sync-debox-docs",
            "language": language,
            "created_with": SCRIPT_VERSION,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(report)
        if not complete:
            raise RuntimeError("sync was incomplete; existing files were preserved and no stale files were deleted")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize current public DeBox documentation.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("self-check", "sync"):
        child = subparsers.add_parser(command)
        child.add_argument("--language", choices=("zh", "en"), required=True)
        child.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        output = Path(args.output).expanduser().resolve()
        if args.command == "self-check":
            self_check(args.language, output)
        else:
            sync(args.language, output)
        return 0
    except (HTTPError, URLError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
