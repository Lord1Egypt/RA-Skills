"""TTS coordinator package.

Exposes :class:`TTSEngine`, the coordinator that drives text-to-speech
providers through the adaptive scheduler, skips empty subtitle entries,
and validates the provider's return shape before handing back a list of
:class:`AudioClip` objects to the aligner.
"""

from translation_dubbing_skill.tts.engine import TTSEngine

__all__ = ["TTSEngine"]
