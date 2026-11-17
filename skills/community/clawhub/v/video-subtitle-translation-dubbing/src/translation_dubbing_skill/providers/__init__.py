"""Pluggable translation and TTS provider implementations.

This package hosts the Protocol definitions every concrete provider must
satisfy (:class:`~translation_dubbing_skill.providers.translation.protocol.TranslationProvider`,
:class:`~translation_dubbing_skill.providers.tts.protocol.TTSProvider`),
shared text-volume measurement helpers, the registry and decorator that
let providers opt in at import time, and the built-in LLM/web providers
themselves.

Importing this module has the side effect of registering the four
built-in providers with :data:`default_registry` (task 14.2):

    * ``translation``: ``llm`` → :class:`LLMTranslationProvider`
    * ``translation``: ``web`` → :class:`WebTranslationProvider`
    * ``tts``:         ``llm`` → :class:`LLMTTSProvider`
    * ``tts``:         ``web`` → :class:`WebTTSProvider`

The skill entry point (:mod:`translation_dubbing_skill.entry`) imports
:data:`default_registry` from here so any runtime that loads the skill
package gets a fully-populated registry without extra wiring.
"""

from translation_dubbing_skill.providers.registry import (
    ProviderKind,
    ProviderRegistry,
    default_registry,
    register,
)
from translation_dubbing_skill.providers.sizing import (
    PayloadUnit,
    default_size_of,
    size_of_chars,
    size_of_tokens,
)

# Import the concrete provider modules purely for their registration
# side effects. The ``@register(...)`` decorators on each class body run
# at import time and populate ``default_registry``. The imports are
# annotated with ``noqa: F401`` because the names are intentionally
# unused — they exist to pull the decorators into the import graph.
from translation_dubbing_skill.providers.translation.llm import (  # noqa: F401
    LLMTranslationProvider,
)
from translation_dubbing_skill.providers.translation.web import (  # noqa: F401
    WebTranslationProvider,
)
from translation_dubbing_skill.providers.tts.llm import (  # noqa: F401
    LLMTTSProvider,
)
from translation_dubbing_skill.providers.tts.edge import (  # noqa: F401
    EdgeTTSProvider,
)
from translation_dubbing_skill.providers.tts.minimax import (  # noqa: F401
    MiniMaxTTSProvider,
)
from translation_dubbing_skill.providers.tts.web import (  # noqa: F401
    WebTTSProvider,
)

__all__ = [
    "PayloadUnit",
    "ProviderKind",
    "ProviderRegistry",
    "default_registry",
    "default_size_of",
    "register",
    "size_of_chars",
    "size_of_tokens",
    "LLMTranslationProvider",
    "WebTranslationProvider",
    "LLMTTSProvider",
    "EdgeTTSProvider",
    "MiniMaxTTSProvider",
    "WebTTSProvider",
]
