#!/usr/bin/env python3
from __future__ import annotations

from _bootstrap import bootstrap_src

bootstrap_src()

from resource_hunter.common import ensure_utf8_stdio  # noqa: E402
from resource_hunter.core import parse_intent  # noqa: E402


def main() -> int:
    ensure_utf8_stdio()
    cases = {
        "https://www.bilibili.com/video/BV1xx": "video",
        "magnet:?xt=urn:btih:abc": "torrent",
        "进击的巨人 Attack on Titan": "anime",
        "Breaking Bad S01E01": "tv",
        "Adobe Photoshop 2024": "software",
        "周杰伦 无损": "music",
        "三体 epub": "book",
        "Oppenheimer 2023": "movie",
    }
    failures: list[str] = []
    for query, expected in cases.items():
        kind = parse_intent(query).kind
        if kind != expected:
            failures.append(f"{query!r}: expected={expected!r} got={kind!r}")
    if failures:
        print("FAIL")
        for line in failures:
            print(f"- {line}")
        return 1
    print("OK")
    print(f"cases={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
