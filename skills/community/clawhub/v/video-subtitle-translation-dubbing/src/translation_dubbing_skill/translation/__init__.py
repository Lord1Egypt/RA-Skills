"""Translation coordinator package.

Exposes :class:`Translator`, the coordinator that drives translation
providers through the adaptive scheduler, handles the empty/whitespace
fast path, and validates the provider's structural + semantic contract
before returning results to the caller.
"""

from translation_dubbing_skill.translation.translator import Translator

__all__ = ["Translator"]
