"""Provider registry and ``@register`` decorator.

This module implements :class:`ProviderRegistry`, the mechanism by which
concrete translation and TTS providers are discovered at runtime, and the
module-level :func:`register` decorator + :data:`default_registry`
singleton that wire providers into the global registry via import side
effects.

Design mapping
--------------

Corresponds to requirements R5.3, R5.4, R5.7, R6.3, R6.4, R6.8, R7.5 and
the design section "Provider 注册与加载（ProviderRegistry）".

- Mapping key: ``(kind, provider_type)`` where ``kind`` is a
  :data:`ProviderKind` literal (``"translation" | "tts"``) and
  ``provider_type`` is the provider's stable string identifier.
- :meth:`ProviderRegistry.register` stores ``cls`` under that key.
- :meth:`ProviderRegistry.create` instantiates the stored class, invokes
  ``initialize(config)`` on the instance, and returns it.
- :meth:`ProviderRegistry.list` returns the sorted provider-type
  identifiers registered for a given kind.
- Unknown ``provider_type`` passed to :meth:`~ProviderRegistry.create`
  raises :class:`~translation_dubbing_skill.errors.ProviderNotRegisteredError`
  whose ``context`` carries ``requested_type`` and ``registered_types``.

The decorator form is::

    @register(kind="translation", provider_type="llm")
    class LLMTranslationProvider: ...

which is equivalent to
``default_registry.register("translation", "llm", LLMTranslationProvider)``
and returns the class unchanged so downstream imports still see it.
"""

from __future__ import annotations

from typing import Any, Literal, TypeVar

from translation_dubbing_skill.errors import ProviderNotRegisteredError
from translation_dubbing_skill.models import ProviderConfig

ProviderKind = Literal["translation", "tts"]
"""Closed set of provider kinds supported by the registry."""

_VALID_KINDS: frozenset[str] = frozenset({"translation", "tts"})

_STAGE_BY_KIND: dict[str, str] = {
    "translation": "translating",
    "tts": "tts",
}

_T = TypeVar("_T", bound=type)


class ProviderRegistry:
    """Runtime lookup from ``(kind, provider_type)`` to provider class.

    Instances are plain containers; concurrency is not a concern because
    registration happens at import time and lookup is read-only afterwards.

    Attributes:
        _classes: Mapping from ``kind`` to an inner mapping of
            ``provider_type -> class``.
    """

    def __init__(self) -> None:
        self._classes: dict[str, dict[str, type]] = {
            "translation": {},
            "tts": {},
        }

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        kind: ProviderKind,
        provider_type: str,
        cls: type,
    ) -> None:
        """Register ``cls`` under ``(kind, provider_type)``.

        Re-registering the same ``(kind, provider_type)`` pair silently
        overwrites the previous class. This keeps test fixtures simple
        (a test double can replace the real class for the duration of
        a test) and matches the design doc's "module import side
        effect" registration model.

        Args:
            kind: Either ``"translation"`` or ``"tts"``.
            provider_type: Stable string identifier, e.g. ``"llm"`` or
                ``"web"``.
            cls: The provider class. Not instantiated here.

        Raises:
            ValueError: If ``kind`` is outside the valid set or
                ``provider_type`` is empty.
        """
        self._check_kind(kind)
        if not provider_type:
            raise ValueError("provider_type must be a non-empty string")
        self._classes[kind][provider_type] = cls

    # ------------------------------------------------------------------
    # Instantiation
    # ------------------------------------------------------------------

    def create(
        self,
        kind: ProviderKind,
        provider_type: str,
        config: ProviderConfig,
    ) -> Any:
        """Instantiate the registered provider and initialize it.

        Looks up the class for ``(kind, provider_type)``, invokes its
        no-argument constructor, then calls ``instance.initialize(config)``
        before returning the instance. Providers are expected to accept
        a zero-argument ``__init__`` so the registry does not need to
        know their constructor signatures.

        Args:
            kind: Either ``"translation"`` or ``"tts"``.
            provider_type: Stable string identifier of the provider.
            config: Configuration passed verbatim to ``initialize``.

        Returns:
            A fully initialized provider instance.

        Raises:
            ProviderNotRegisteredError: No class is registered for
                ``(kind, provider_type)``. The error carries
                ``context={"requested_type": provider_type,
                "registered_types": [...]}`` — the list is the sorted
                currently registered identifiers for ``kind``.
            ValueError: If ``kind`` is outside the valid set.
        """
        self._check_kind(kind)
        cls = self._classes[kind].get(provider_type)
        if cls is None:
            registered = self.list(kind)
            raise ProviderNotRegisteredError(
                f"{kind} provider {provider_type!r} is not registered",
                stage=_STAGE_BY_KIND[kind],  # type: ignore[arg-type]
                context={
                    "requested_type": provider_type,
                    "registered_types": registered,
                    "kind": kind,
                },
            )
        instance = cls()
        instance.initialize(config)
        return instance

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list(self, kind: ProviderKind) -> list[str]:
        """Return the sorted provider-type identifiers for ``kind``.

        Args:
            kind: Either ``"translation"`` or ``"tts"``.

        Returns:
            A freshly-built, sorted list of registered ``provider_type``
            strings. Mutating the returned list does not affect the
            registry state.
        """
        self._check_kind(kind)
        return sorted(self._classes[kind].keys())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _check_kind(kind: str) -> None:
        if kind not in _VALID_KINDS:
            raise ValueError(
                f"invalid kind {kind!r}; expected one of {sorted(_VALID_KINDS)}"
            )


# ---------------------------------------------------------------------------
# Module-level singleton + decorator
# ---------------------------------------------------------------------------


default_registry: ProviderRegistry = ProviderRegistry()
"""Process-wide registry populated by the :func:`register` decorator.

Concrete provider modules import this indirectly via ``@register(...)`` so
that simply importing a provider module is enough to make it available
through the coordinators.
"""


def register(kind: ProviderKind, provider_type: str):
    """Class decorator that registers ``cls`` on :data:`default_registry`.

    Example::

        @register(kind="translation", provider_type="llm")
        class LLMTranslationProvider:
            provider_type = "llm"
            ...

    The decorator returns the class unchanged, so normal imports and
    ``isinstance`` checks continue to work.

    Args:
        kind: Either ``"translation"`` or ``"tts"``.
        provider_type: Stable string identifier for the provider.

    Returns:
        A decorator that registers its argument class and returns it.
    """

    def _decorator(cls: _T) -> _T:
        default_registry.register(kind, provider_type, cls)
        return cls

    return _decorator


__all__ = [
    "ProviderKind",
    "ProviderRegistry",
    "default_registry",
    "register",
]
