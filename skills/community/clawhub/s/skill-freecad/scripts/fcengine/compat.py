"""Supported FreeCAD versions (pure Python).

FreeCAD 1.1 is the minimum. In 1.0.x, Draft (used for arrays, copy and
scale) imports FreeCADGui unconditionally (draftutils/params.py ->
init_draft_statusbar), which fails headless wherever the GUI library
cannot load, e.g. conda builds on macOS and Windows. 1.1 guards that import.
"""

from __future__ import annotations

import re
from typing import Sequence, Tuple

from . import errors

MIN_FREECAD: Tuple[int, int] = (1, 1)


def parse_version(parts: Sequence[str]) -> Tuple[int, int, int]:
    """FreeCAD.Version() -> (major, minor, patch); non-numeric parts count as 0."""
    nums = []
    for p in list(parts)[:3]:
        m = re.match(r"\d+", str(p).strip())
        nums.append(int(m.group()) if m else 0)
    while len(nums) < 3:
        nums.append(0)
    return nums[0], nums[1], nums[2]


def check_version(parts: Sequence[str]) -> None:
    v = parse_version(parts)
    if v[:2] < MIN_FREECAD:
        need = ".".join(map(str, MIN_FREECAD))
        raise errors.SkillError(
            errors.FREECAD_VERSION,
            f"FreeCAD {'.'.join(map(str, v))} is not supported; this skill needs FreeCAD {need} or newer",
            hint=f"Ask the user to install FreeCAD {need}+ (https://www.freecad.org/downloads.php), or to point "
            "FCSKILL_FREECAD at a newer installation if several are installed.",
        )
