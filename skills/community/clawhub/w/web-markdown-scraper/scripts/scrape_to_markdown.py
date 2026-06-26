#!/usr/bin/env python3
# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: only URLs supplied by the user at runtime via --url / --url-file
# Local files read: --url-file path (if provided by user)
# Local files written: --output-dir/*.md, --output-dir/index.json (if --output-dir provided)
#                      Scrapling automatch SQLite DB (managed by Scrapling, local only)
# Credentials handled: --proxy value (never logged or transmitted beyond the proxy itself)
# Shell injection risk: none (pure Python, no subprocess or shell interpolation)
import argparse
import importlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import html2text


def to_str(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def slugify(text, max_len=80):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text[:max_len].strip("-") or "page"


def extract_html(obj):
    if obj is None:
        return ""
    for attr in ("html", "raw_html", "content", "markup", "body", "inner_html"):
        value = getattr(obj, attr, None)
        if callable(value):
            try:
                value = value()
            except Exception:
                value = None
        text = to_str(value)
        if text and "<" in text and ">" in text:
            return text
    text = to_str(obj)
    return text if "<" in text and ">" in text else ""


def extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if not m:
        return ""
    title = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", title).strip()


def load_fetcher(js=False):
    if js:
        candidates = [
            ("scrapling.fetchers", "DynamicFetcher"),
            ("scrapling.fetchers", "PlayWrightFetcher"),
            ("scrapling.default", "PlayWrightFetcher"),
            ("scrapling.defaults", "PlayWrightFetcher"),
        ]
    else:
        candidates = [
            ("scrapling.fetchers", "Fetcher"),
            ("scrapling.default", "Fetcher"),
            ("scrapling.defaults", "Fetcher"),
        ]

    errors = []
    for module_name, class_name in candidates:
        try:
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            for method_name in ("get", "fetch"):
                if callable(getattr(cls, method_name, None)):
                    return cls, method_name
        except Exception as e:
            errors.append(f"{module_name}.{class_name}: {e}")

    raise RuntimeError("No compatible Scrapling fetcher found: " + " | ".join(errors[:5]))


def fetch_page(url, js=False, wait_selector=None, timeout=30, automatch_domain=None):
    cls, method_name = load_fetcher(js=js)
    method = getattr(cls, method_name)

    kwargs = {}
    if js:
        kwargs["headless"] = True
        if wait_selector:
            kwargs["wait_selector"] = wait_selector
    else:
        kwargs["timeout"] = timeout

    if automatch_domain and not js:
        try:
            instance = cls(automatch_domain=automatch_domain)
            method = getattr(instance, method_name)
        except Exception:
            pass

    try:
        page = method(url, **kwargs)
        return page, f"{cls.__module__}.{cls.__name__}.{method_name}"
    except TypeError:
        page = method(url)
        return page, f"{cls.__module__}.{cls.__name__}.{method_name}"


def pick_main_html(page, preferred_selector=None):
    selectors = []
    if preferred_selector:
        selectors.append(preferred_selector)
    selectors.extend([
        "article",
        "main",
        "[role='main']",
        ".post-content",
        ".entry-content",
        ".article-content",
        "body",
    ])

    if hasattr(page, "css_first"):
        for selector in selectors:
            try:
                node = page.css_first(selector)
                html = extract_html(node)
                if html and len(html) >= 120:
                    return html, selector
            except Exception:
                pass

    return extract_html(page), None


def html_to_markdown(html, preserve_links=False, body_width=0):
    h = html2text.HTML2Text()
    h.ignore_links = not preserve_links
    h.ignore_images = True
    h.body_width = body_width
    h.ignore_emphasis = False
    try:
        h.ignore_tables = False
    except Exception:
        pass
    md = h.handle(html)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


def load_urls(url_args, url_file):
    urls = list(url_args or [])
    if url_file:
        with open(url_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
    clean = []
    seen = set()
    for u in urls:
        if u not in seen:
            clean.append(u)
            seen.add(u)
    return clean


def validate_url(url):
    p = urlparse(url)
    return p.scheme in ("http", "https") and bool(p.netloc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--url-file", default="")
    parser.add_argument("--selector", default="")
    parser.add_argument("--js", action="store_true")
    parser.add_argument("--wait-selector", default="")
    parser.add_argument("--preserve-links", action="store_true")
    parser.add_argument("--body-width", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--automatch-domain", default="")
    args = parser.parse_args()

    urls = load_urls(args.url, args.url_file)
    if not urls:
        print(json.dumps({"ok": False, "error": "No URLs provided"}, ensure_ascii=False))
        sys.exit(1)

    for u in urls:
        if not validate_url(u):
            print(json.dumps({"ok": False, "error": f"Invalid URL: {u}"}, ensure_ascii=False))
            sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for url in urls:
        item = {
            "url": url,
            "ok": False,
            "title": "",
            "status": None,
            "selector_used": None,
            "backend": None,
            "markdown": "",
            "preview": "",
            "output_markdown_file": None,
            "error": None,
        }
        try:
            page, backend = fetch_page(
                url=url,
                js=args.js,
                wait_selector=args.wait_selector or None,
                timeout=args.timeout,
                automatch_domain=args.automatch_domain or None,
            )
            html, selector_used = pick_main_html(page, preferred_selector=args.selector or None)
            if not html:
                raise RuntimeError("No HTML content extracted from page")

            title = extract_title(html) or urlparse(url).netloc
            markdown = html_to_markdown(
                html,
                preserve_links=args.preserve_links,
                body_width=args.body_width,
            )

            filename = slugify(f"{urlparse(url).netloc}-{title}") + ".md"
            md_path = out_dir / filename
            md_path.write_text(markdown, encoding="utf-8")

            status = getattr(page, "status", None) or getattr(page, "status_code", None)

            item.update({
                "ok": True,
                "title": title,
                "status": status,
                "selector_used": selector_used,
                "backend": backend,
                "markdown": markdown,
                "preview": markdown[:1200],
                "output_markdown_file": str(md_path),
            })
        except Exception as e:
            item["error"] = str(e)

        results.append(item)

    ok = any(x["ok"] for x in results)
    index_path = out_dir / "index.json"
    payload = {
        "ok": ok,
        "count": len(results),
        "success_count": sum(1 for x in results if x["ok"]),
        "failure_count": sum(1 for x in results if not x["ok"]),
        "output_index_file": str(index_path),
        "results": results,
    }
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()