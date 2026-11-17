"""Processing mode enumeration.

Defines the two supported processing modes for the translation-dubbing skill:

- ``SUBTITLE_ONLY``: only translate subtitles and embed them into the output video.
- ``SUBTITLE_AND_DUBBING``: translate subtitles and additionally generate a
  dubbed Chinese audio track.

The module-level ``DEFAULT_PROCESSING_MODE`` constant declares the default
mode applied when the manifest does not explicitly provide one.

Corresponds to requirement R1.3.
"""

from __future__ import annotations

from enum import Enum


class ProcessingMode(str, Enum):
    """Supported processing modes for the skill.

    Subclassing ``str`` keeps the enum values interoperable with manifest
    strings and JSON serialization without extra conversion.
    """

    SUBTITLE_ONLY = "subtitle_only"
    SUBTITLE_AND_DUBBING = "subtitle_and_dubbing"


DEFAULT_PROCESSING_MODE: ProcessingMode = ProcessingMode.SUBTITLE_AND_DUBBING
"""Default processing mode when the manifest omits ``processing_mode``."""


__all__ = ["ProcessingMode", "DEFAULT_PROCESSING_MODE"]
