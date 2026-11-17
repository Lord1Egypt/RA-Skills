"""Translation provider implementations and protocol.

Importing this package pulls in the concrete :class:`LLMTranslationProvider`
and :class:`WebTranslationProvider` modules, whose ``@register`` decorators
populate the default provider registry as an import side effect.
"""

from translation_dubbing_skill.providers.translation.llm import (
    LLMTranslationProvider,
)
from translation_dubbing_skill.providers.translation.protocol import (
    TranslationProvider,
    default_size_of_for,
)
from translation_dubbing_skill.providers.translation.web import (
    WebTranslationProvider,
)

__all__ = [
    "TranslationProvider",
    "default_size_of_for",
    "LLMTranslationProvider",
    "WebTranslationProvider",
]
