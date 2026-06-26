#!/usr/bin/env python3
"""
Wiki Ingest 去重缓存（SHA256）

用法：
  python3 dedup.py check <file_or_url>    # 检查是否已 ingest，0=新内容，1=重复
  python3 dedup.py record <file_or_url> <wiki_page_path>  # 记录一条
  python3 dedup.py list                   # 列出所有已记录
  python3 dedup.py stats                  # 统计

环境变量：
  WIKI_ROOT    wiki markdown 根目录（默认 ~/.openclaw/workspace/wiki）

缓存文件：$WIKI_ROOT/.ingest-cache.json
格式：
  {
    "<sha256>": {
      "source": "file:/path/to/pdf OR https://...",
      "title": "来源标题（可选）",
      "wiki_page": "pages/aws/xxx.md",
      "ingested_at": "2026-04-25T06:07:00Z",
      "size_bytes": 12345
    },
    ...
  }
"""

import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

def _wiki_dir() -> Path:
    env = os.environ.get("WIKI_ROOT")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".openclaw/workspace/wiki"


WIKI_DIR = _wiki_dir()
CACHE_FILE = WIKI_DIR / ".ingest-cache.json"


def load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True))


def compute_hash(source: str) -> tuple[str, int]:
    """Return (sha256_hex, size_bytes) for a local path or URL. Raises on fetch errors."""
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "wikisage-dedup/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    else:
        path = Path(source).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"source not found: {source}")
        data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def cmd_check(args: list[str]) -> int:
    if not args:
        print("usage: dedup.py check <file_or_url>", file=sys.stderr)
        return 2
    source = args[0]
    try:
        digest, size = compute_hash(source)
    except Exception as e:
        print(f"ERROR computing hash for {source}: {e}", file=sys.stderr)
        return 2

    cache = load_cache()
    if digest in cache:
        entry = cache[digest]
        print(f"DUPLICATE")
        print(f"  sha256:     {digest}")
        print(f"  source:     {entry.get('source')}")
        print(f"  title:      {entry.get('title', '-')}")
        print(f"  wiki_page:  {entry.get('wiki_page')}")
        print(f"  ingested:   {entry.get('ingested_at')}")
        return 1
    print(f"NEW")
    print(f"  sha256: {digest}")
    print(f"  size:   {size} bytes")
    return 0


def cmd_record(args: list[str]) -> int:
    if len(args) < 2:
        print("usage: dedup.py record <file_or_url> <wiki_page_path> [title]", file=sys.stderr)
        return 2
    source = args[0]
    wiki_page = args[1]
    title = args[2] if len(args) > 2 else ""

    try:
        digest, size = compute_hash(source)
    except Exception as e:
        print(f"ERROR computing hash for {source}: {e}", file=sys.stderr)
        return 2

    cache = load_cache()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    cache[digest] = {
        "source": source,
        "title": title,
        "wiki_page": wiki_page,
        "ingested_at": now,
        "size_bytes": size,
    }
    save_cache(cache)
    print(f"RECORDED {digest[:16]}...  {wiki_page}")
    return 0


def cmd_list(_args: list[str]) -> int:
    cache = load_cache()
    if not cache:
        print("(cache empty)")
        return 0
    for digest, entry in sorted(cache.items(), key=lambda kv: kv[1].get("ingested_at", "")):
        print(f"{digest[:16]}...  {entry.get('ingested_at', '?'):<20}  {entry.get('wiki_page'):<40}  {entry.get('source')}")
    return 0


def cmd_stats(_args: list[str]) -> int:
    cache = load_cache()
    total = len(cache)
    size = sum(e.get("size_bytes", 0) for e in cache.values())
    print(f"entries:     {total}")
    print(f"total size:  {size:,} bytes")
    print(f"cache file:  {CACHE_FILE}")
    return 0


COMMANDS = {
    "check": cmd_check,
    "record": cmd_record,
    "list": cmd_list,
    "stats": cmd_stats,
}


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print(__doc__)
        return 2
    return COMMANDS[argv[1]](argv[2:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
