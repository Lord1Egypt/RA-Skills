"""Shared scene-parsing utilities for module content ingestion and export.

Used by both ``_scenes()`` (import path) and ``_parse_scene_index()``
(export path) in ``nanobot.dnd.db.module_content``.
"""

from __future__ import annotations

import re
from typing import Any, Callable

#: CJK unified ideograph ranges used by the bilingual-heading-merge heuristic.
CJK_RANGES: tuple[tuple[str, str], ...] = (
    ("一", "鿿"),
    ("㐀", "䶿"),
    ("豈", "﫿"),
)


def has_cjk(text: str) -> bool:
    """Return True when *text* contains at least one CJK unified ideograph."""
    return any(lo <= c <= hi for lo, hi in CJK_RANGES for c in text)


def has_ascii_alpha(text: str) -> bool:
    """Return True when *text* contains at least two consecutive ASCII letters."""
    return bool(re.search(r"[A-Za-z]{2,}", text))


def detect_scene_heading_level(lines: list[str]) -> tuple[int, int | None, int | None]:
    """Determine which Markdown heading level marks scene boundaries.

    Returns ``(scene_level, sub_level, room_level)`` where *sub_level* and
    *room_level* may be ``None`` when the hierarchy is exhausted.

    Heuristic: when H3 headings outnumber H2 by ≥5× the real structural
    level is H3 (common in PDF conversions where H2 is used only for
    top-level bookmarks).  Otherwise H2 is preferred when present.
    """
    _h_counts = {
        level: sum(
            1
            for l in lines
            if l.startswith(level * "#" + " ")
            and not l.startswith((level + 1) * "#")
        )
        for level in (2, 3, 4)
    }
    if _h_counts[2] > 0 and _h_counts[3] >= _h_counts[2] * 5:
        scene_level = 3
    elif _h_counts[2] > 0:
        scene_level = 2
    elif _h_counts[3] > 0:
        scene_level = 3
    else:
        scene_level = 4

    sub_level = scene_level + 1 if scene_level < 4 else None
    room_level = scene_level + 2 if scene_level < 3 else None
    return scene_level, sub_level, room_level


def heading_prefix(level: int) -> str:
    """``## `` / ``### `` / ``#### `` for *level*."""
    return level * "#" + " "


def preamble_title(lines: list[str], limit: int) -> str:
    """Pick a human-readable title from the first *limit* lines.

    Tries the first heading (any level), then the first non-blank,
    non-comment line; falls back to ``"Chapter Intro"``.
    """
    for pline in lines[:limit]:
        ps = pline.strip()
        if ps.startswith("#") and ps.lstrip("#").strip():
            return ps.lstrip("#").strip()
    for pline in lines[:limit]:
        ps = pline.strip()
        if ps and not ps.startswith("<!--"):
            return ps[:80]
    return "Chapter Intro"


def capture_preamble_scene(
    lines: list[str],
    *,
    scene_start_line: int,
    sub_prefix: str | None,
    tag_func: Callable[[str], list[str]],
) -> dict[str, object] | None:
    """Return a preamble scene dict covering ``lines[: scene_start_line - 1]``.

    Returns ``None`` when the first scene already starts at line 1.
    Callers should insert the result at position 0 of their scene list.
    """
    if scene_start_line <= 1:
        return None
    preamble_end = scene_start_line - 1
    preamble_lines = lines[:preamble_end]
    title = preamble_title(preamble_lines, preamble_end)
    tags = tag_func(title)
    return {
        "title": title,
        "start_line": 1,
        "end_line": preamble_end,
        "type": "section",
        "subsections": [],
        "line_count": preamble_end,
        "tags": tags,
    }


def merge_bilingual_scenes(
    scenes: list[dict[str, object]],
    *,
    title_key: str = "title",
    start_line_key: str = "start_line",
    end_line_key: str = "end_line",
    line_count_key: str = "line_count",
    subs_key: str = "subsections",
    tags_key: str = "tags",
) -> list[dict[str, object]]:
    """Merge adjacent heading-only scenes whose titles are CJK/ASCII complements.

    The PDF parser sometimes emits ``## Chinese`` / ``## English`` as two
    consecutive headings with no body content between them.  Those produce
    scenes whose *line_count_key* is ≤ 2 (heading + blank line).  This
    function merges them into the following scene so the result matches the
    single-heading expectation.
    """
    merged: list[dict[str, object]] = []
    i = 0
    while i < len(scenes):
        scene = scenes[i]
        # Compute line count: prefer the named key, fall back to end-start
        lc_raw = scene.get(line_count_key)
        if lc_raw is not None:
            lc = int(lc_raw)
        else:
            lc = int(scene.get(end_line_key, 0)) - int(scene.get(start_line_key, 0))
        if lc <= 2 and i + 1 < len(scenes):
            nxt = scenes[i + 1]
            cur_cjk = has_cjk(str(scene.get(title_key, "")))
            cur_asc = has_ascii_alpha(str(scene.get(title_key, "")))
            nxt_cjk = has_cjk(str(nxt.get(title_key, "")))
            nxt_asc = has_ascii_alpha(str(nxt.get(title_key, "")))
            complementary = (
                cur_cjk and not cur_asc and nxt_asc and not nxt_cjk
            ) or (
                cur_asc and not cur_cjk and nxt_cjk and not nxt_asc
            )
            if complementary:
                nxt[title_key] = (
                    str(scene.get(title_key, ""))
                    + " "
                    + str(nxt.get(title_key, ""))
                )
                nxt[start_line_key] = scene.get(start_line_key)
                nxt[subs_key] = list(
                    scene.get(subs_key, [])
                ) + list(nxt.get(subs_key, []))
                nxt[line_count_key] = (
                    int(nxt.get(end_line_key, 0))
                    - int(nxt.get(start_line_key, 0))
                    + 1
                )
                nxt[tags_key] = list(
                    dict.fromkeys(
                        list(scene.get(tags_key, []))
                        + list(nxt.get(tags_key, []))
                    )
                )
                i += 1
                scene = nxt
        merged.append(scene)
        i += 1
    return merged
