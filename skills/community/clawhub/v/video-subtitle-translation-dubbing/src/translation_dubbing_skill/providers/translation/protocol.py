"""Translation provider protocol.

Defines :class:`TranslationProvider`, the structural interface every
translation provider (LLM-based, third-party web API, etc.) must satisfy.
The translation coordinator (``Translator``) and the adaptive scheduler
interact with providers exclusively through this Protocol, keeping
coordinator code decoupled from concrete implementations (R7.5).

Contracts (informally, per batch call):

    - ``len(output) == len(entries)``
    - ``output[i].index / start_ms / end_ms`` equal the input's.
    - Whitespace-only ``entries[i].text`` ⇒ ``output[i].text == ""``.
    - Non-empty ``entries[i].text`` ⇒ ``output[i].text`` is non-empty
      simplified Chinese.
    - On rate-limit, payload overflow, or transient failure, the provider
      SHALL raise an exception the scheduler can recognise: respectively
      ``RateLimitError`` / ``PayloadTooLargeError`` / ``TransientError``
      (defined in ``translation_dubbing_skill.scheduler.signals`` — see
      task 5.3). Until that module lands, providers may raise these
      concrete classes via string-based forward reference; this protocol
      module does NOT import them to avoid a circular dependency during
      incremental build-out.

Corresponds to requirements R5.1, R5.2, R6.2, R7.1, R7.2, R7.5, R12.1,
R12.2, R12.12.
"""

from __future__ import annotations

from typing import ClassVar, Literal, Protocol, runtime_checkable

from translation_dubbing_skill.models import ProviderConfig, SubtitleEntry
from translation_dubbing_skill.providers.sizing import (
    PayloadUnit,
    default_size_of,
)


@runtime_checkable
class TranslationProvider(Protocol):
    """Structural protocol for translation providers.

    Concrete providers (e.g. ``LLMTranslationProvider``,
    ``WebTranslationProvider``) are registered via
    ``@register(kind="translation", provider_type=...)`` and instantiated
    by the coordinator through the provider registry (task 5.2).

    Class attributes:
        provider_type: Stable string identifier for this provider kind
            (e.g. ``"llm"`` or ``"web"``). Used as the registry key.
        supports_batch: Whether :meth:`translate_batch` issues a genuine
            batched request. When ``False`` the scheduler forces
            ``batch_size=1`` (R12.14).
        payload_unit: Unit in which single-request text volume is
            measured — either ``"chars"`` or ``"tokens"``. The scheduler
            uses this together with :meth:`size_of` to enforce the
            ``payload_size`` constraint.
    """

    provider_type: ClassVar[str]
    supports_batch: ClassVar[bool] = True
    payload_unit: ClassVar[Literal["chars", "tokens"]]

    def initialize(self, config: ProviderConfig) -> None:
        """Initialize the provider from the Manifest-supplied config.

        Called once per invocation before any translation call. Providers
        typically read ``config.endpoint``, ``config.credential`` and any
        ``config.extra`` keys they understand (e.g. ``model_name``,
        ``language_pair``).

        Args:
            config: The validated provider configuration.
        """
        ...

    def size_of(self, text: str) -> int:
        """Measure the text volume of ``text`` under :attr:`payload_unit`.

        Used by the adaptive scheduler to split inputs into batches that
        respect the per-request ``payload_size`` limit. Providers MAY
        override this with a more accurate estimate (e.g. a real
        tokenizer); the default delegates to a generic helper.

        Args:
            text: The text to measure.

        Returns:
            A non-negative integer volume estimate.
        """
        ...

    async def translate_batch(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
    ) -> list[SubtitleEntry]:
        """Translate a batch of subtitle entries in a single request.

        Args:
            entries: The subtitle entries to translate. Order MUST be
                preserved in the output.
            target_language: BCP-47 language tag of the desired output.
                Defaults to ``"zh-CN"``.

        Returns:
            Translated entries aligned 1:1 with ``entries`` by index,
            ``start_ms`` and ``end_ms``.

        Raises:
            RateLimitError: The upstream signalled rate limiting (HTTP
                429 or equivalent). The scheduler will back off and
                retry.
            PayloadTooLargeError: The upstream rejected the request
                because the aggregated text volume exceeded its limit
                (HTTP 413 / context-window-exceeded / provider-specific
                payload-too-large business code). The scheduler will
                shrink ``payload_size`` and re-slice.
            TransientError: Any other transient failure (timeout, 5xx,
                partial-response parse error). The scheduler will retry
                with backoff.
        """
        ...

    async def translate(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
    ) -> list[SubtitleEntry]:
        """Compatibility alias for single-/small-batch translation.

        Default semantics delegate to :meth:`translate_batch`; providers
        MAY override with a dedicated single-entry endpoint when that is
        more natural. See :meth:`translate_batch` for the full contract.

        Args:
            entries: Subtitle entries to translate.
            target_language: BCP-47 target language tag.

        Returns:
            Translated entries, aligned 1:1 with the input.
        """
        ...


def default_size_of_for(
    payload_unit: PayloadUnit,
) -> "callable[[str], int]":
    """Return a ``size_of`` function implementing the default for ``unit``.

    Concrete providers can reuse this to wire up :meth:`size_of` without
    writing boilerplate::

        class MyProvider:
            payload_unit = "tokens"

            def size_of(self, text: str) -> int:
                return default_size_of(text, self.payload_unit)

    This helper is a thin factory around
    :func:`translation_dubbing_skill.providers.sizing.default_size_of`
    for cases where a callable-per-unit form is more convenient.

    Args:
        payload_unit: ``"chars"`` or ``"tokens"``.

    Returns:
        A callable mapping ``text -> int`` under the requested unit.
    """

    def _sizer(text: str) -> int:
        return default_size_of(text, payload_unit)

    return _sizer


__all__ = ["TranslationProvider", "default_size_of_for"]
