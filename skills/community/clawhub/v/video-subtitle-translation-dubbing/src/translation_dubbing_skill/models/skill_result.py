"""Skill result data model returned from the entry point.

Defines :class:`SkillResult`, the value returned by the skill entry point
``run(params)`` after a successful execution in either processing mode.

Corresponds to requirement R9.16 and the "Data Models > SkillResult" section
of the design document.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillResult:
    """Final outputs produced by a successful skill invocation.

    Attributes:
        output_video_path: Filesystem path to the muxed output video
            (``.mkv``). Contents depend on the processing mode.
        output_subtitle_path: Filesystem path to the translated Chinese
            subtitle file (UTF-8 SRT or VTT).
    """

    output_video_path: Path
    output_subtitle_path: Path


__all__ = ["SkillResult"]
