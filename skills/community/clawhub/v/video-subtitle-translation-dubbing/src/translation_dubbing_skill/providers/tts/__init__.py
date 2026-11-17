"""Text-to-speech provider implementations and protocol.

Importing this package pulls in the concrete :class:`LLMTTSProvider`
and :class:`WebTTSProvider` modules, whose ``@register`` decorators
populate the default provider registry as an import side effect.
"""

from translation_dubbing_skill.providers.tts.llm import LLMTTSProvider
from translation_dubbing_skill.providers.tts.edge import EdgeTTSProvider
from translation_dubbing_skill.providers.tts.minimax import MiniMaxTTSProvider
from translation_dubbing_skill.providers.tts.protocol import (
    TTSProvider,
    default_size_of_for,
)
from translation_dubbing_skill.providers.tts.web import WebTTSProvider

__all__ = [
    "TTSProvider",
    "default_size_of_for",
    "LLMTTSProvider",
    "EdgeTTSProvider",
    "MiniMaxTTSProvider",
    "WebTTSProvider",
]
