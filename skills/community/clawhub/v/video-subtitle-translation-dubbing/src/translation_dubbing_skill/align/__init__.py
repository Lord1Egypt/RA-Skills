"""Audio alignment: place TTS clips onto a silent base track matching the video.

Exports the :class:`AudioAligner` (main entry point) and the
``build_atempo_chain`` / ``apply_atempo`` helpers used for audio time-scaling.
Only used in ``subtitle_and_dubbing`` processing mode.
"""

from translation_dubbing_skill.align.aligner import AtempoFn, AudioAligner
from translation_dubbing_skill.align.atempo import apply_atempo, build_atempo_chain

__all__ = [
    "AudioAligner",
    "AtempoFn",
    "build_atempo_chain",
    "apply_atempo",
]
