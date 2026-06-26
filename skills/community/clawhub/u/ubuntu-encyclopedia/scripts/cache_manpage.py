#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import ipaddress
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

ALLOWED_NETLOCS = {'manpages.ubuntu.com'}
ALLOWED_SCHEMES = {'https'}
OUTPUT_NETLOC = 'manpages.ubuntu.com'
USER_AGENT = 'Ubuntu-Encyclopedia/1.1'
TITLE_FALLBACK = 'Ubuntu Manpage'
PATH_HELP = 'manpages.ubuntu.com URL to cache'
ROOT_HELP = 'Ubuntu Encyclopedia data root (default: <cwd>/.Ubuntu-Encyclopedia)'
DESCRIPTION = 'Fetch and cache an Ubuntu manpage into .Ubuntu-Encyclopedia.'
PATH_PREFIX = '/manpages'
BLOCK_QUERY = True


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_script = False
        self.in_style = False
        self.title = ''
        self._in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        elif tag == 'title':
            self._in_title = True
        elif tag in {'li', 'br', 'h1', 'h4', 'h3', 'div', 'h2', 'article', 'tr', 'p', 'section', 'pre', 'h6', 'h5'}:
            self.parts.append('\n')

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'title':
            self._in_title = False
        elif tag in {'li', 'br', 'h1', 'h4', 'h3', 'div', 'h2', 'article', 'tr', 'p', 'section', 'pre', 'h6', 'h5'}:
            self.parts.append('\n')

    def handle_data(self, data: str):
        if self.in_script or self.in_style:
            return
        text = html.unescape(data)
        if self._in_title:
            self.title += text
        self.parts.append(text)

    def text(self) -> str:
        text = ''.join(self.parts)
        text = re.sub(r'\r', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        lines = [line.rstrip() for line in text.splitlines()]
        return '\n'.join(line for line in lines if line.strip()).strip()


def default_root() -> Path:
    return Path.cwd() / '.Ubuntu-Encyclopedia'


def normalized_relative_path(parsed: urllib.parse.ParseResult) -> PurePosixPath:
    raw_path = urllib.parse.unquote(parsed.path or '/')
    if '\x00' in raw_path:
        raise ValueError('NUL bytes are not supported in URL paths')
    if PATH_PREFIX and not (raw_path == PATH_PREFIX or raw_path.startswith(PATH_PREFIX + '/')):
        raise ValueError(f'Only {PATH_PREFIX} URLs are supported')
    pure = PurePosixPath(raw_path)
    parts = [part for part in pure.parts if part not in ('/', '')]
    if any(part in {'.', '..'} for part in parts):
        raise ValueError('Dot path segments are not supported')
    rel = PurePosixPath(*parts) if parts else PurePosixPath('index')
    if raw_path.endswith('/'):
        rel = rel / 'index'
    return rel.with_suffix('.md')


def validate_url(url: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f'Only {sorted(ALLOWED_SCHEMES)} URLs are supported')
    if parsed.username or parsed.password:
        raise ValueError('Userinfo in URLs is not supported')
    if parsed.hostname is None:
        raise ValueError('URL must include a hostname')
    try:
        ipaddress.ip_address(parsed.hostname)
    except ValueError:
        pass
    else:
        raise ValueError('Direct IP URLs are not supported')
    if parsed.hostname not in ALLOWED_NETLOCS:
        raise ValueError(f'Only {sorted(ALLOWED_NETLOCS)} URLs are supported')
    if parsed.port is not None:
        raise ValueError('Explicit ports are not supported')
    if BLOCK_QUERY and (parsed.params or parsed.query or parsed.fragment):
        raise ValueError('Query strings, params, and fragments are not supported')
    normalized_relative_path(parsed)
    return parsed


def ensure_within(base: Path, candidate: Path) -> Path:
    resolved_base = base.resolve(strict=False)
    resolved_candidate = candidate.resolve(strict=False)
    try:
        resolved_candidate.relative_to(resolved_base)
    except ValueError as exc:
        raise ValueError('Refusing to write outside the cache root') from exc
    return resolved_candidate


def build_output_path(root: Path, parsed: urllib.parse.ParseResult) -> Path:
    rel = normalized_relative_path(parsed)
    base = root / 'manpages' / OUTPUT_NETLOC
    out = base.joinpath(*rel.parts)
    return ensure_within(base, out)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        return resp.read().decode(charset, errors='replace')


def main() -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--url', required=True, help=PATH_HELP)
    parser.add_argument('--root', default=str(default_root()), help=ROOT_HELP)
    args = parser.parse_args()

    parsed = validate_url(args.url)
    root = Path(args.root).expanduser().resolve()
    html_body = fetch_html(args.url)
    extractor = TextExtractor()
    extractor.feed(html_body)
    title = extractor.title.strip() or Path(parsed.path).name or TITLE_FALLBACK
    body = extractor.text()
    out = build_output_path(root, parsed)
    out.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f'# {title}\n\n'
        f'- Source: {args.url}\n'
        f'- Cached at: {datetime.now(timezone.utc).isoformat()}\n\n'
        '## Cached text\n\n'
        f'{body}\n'
    )
    out.write_text(content, encoding='utf-8')
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
