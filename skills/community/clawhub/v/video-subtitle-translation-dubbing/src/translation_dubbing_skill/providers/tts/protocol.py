"""Text-to-speech provider protocol.

Defines :class:`TTSProvider`, the structural interface every TTS provider
(LLM-based, third-party web API, etc.) must satisfy. The TTS coordinator
(``TTSEngine``) and the adaptive scheduler interact with providers
exclusively through this Protocol, keeping coordinator code decoupled
from concrete implementations (R7.5).

Contracts:

    - :meth:`synth` returns ``(audio_bytes, duration_ms)`` where
      ``duration_ms`` is a non-negative integer; input text is non-empty.
    - :meth:`synth_batch` (optional, only implemented when
      :attr:`supports_batch` is ``True``) returns one
      ``(audio_bytes, duration_ms)`` per input text, in order.
    - On rate-limit, payload overflow, or transient failure, the provider
      SHALL raise an exception the scheduler can recognise: respectively
      ``RateLimitError`` / ``PayloadTooLargeError`` / ``TransientError``
      (defined in ``translation_dubbing_skill.scheduler.signals`` — see
      task 5.3). This protocol module does NOT import those classes to
      avoid a circular dependency during incremental build-out; providers
      raise the concrete exceptions once the scheduler module lands.

Corresponds to requirements R5.1, R5.2, R6.2, R7.1, R7.2, R7.3, R7.5,
R12.1, R12.2, R12.12.
"""

from __future__ import annotations

from typing import ClassVar, Literal, Protocol, runtime_checkable

from translation_dubbing_skill.models import ProviderConfig
from translation_dubbing_skill.providers.sizing import (
    PayloadUnit,
    default_size_of,
)


@runtime_checkable
class TTSProvider(Protocol):
    """Structural protocol for text-to-speech providers.

    Concrete providers (e.g. ``LLMTTSProvider``, ``WebTTSProvider``) are
    registered via ``@register(kind="tts", provider_type=...)`` and
    instantiated by the coordinator through the provider registry
    (task 5.2).

    Class attributes:
        provider_type: Stable string identifier for this provider kind
            (e.g. ``"llm"`` or ``"web"``). Used as the registry key.
        supports_batch: Whether :meth:`synth_batch` issues a genuine
            batched request. Most third-party TTS services are
            single-shot, so the default is ``False``; providers whose
            upstream supports batching override this to ``True`` and
            implement :meth:`synth_batch`. When ``False`` the scheduler
            forces ``batch_size=1`` (R12.14).
        payload_unit: Unit in which single-request text volume is
            measured — either ``"chars"`` or ``"tokens"``. The scheduler
            uses this together with :meth:`size_of` to enforce the
            ``payload_size`` constraint.
    """

    provider_type: ClassVar[str]
    supports_batch: ClassVar[bool] = False
    payload_unit: ClassVar[Literal["chars", "tokens"]]

    def initialize(self, config: ProviderConfig) -> None:
        """Initialize the provider from the Manifest-supplied config.

        Called once per invocation before any synth call. Providers
        typically read ``config.endpoint``, ``config.credential`` and
        any ``config.extra`` keys they understand (e.g. ``model_name``,
        ``default_voice``).

        Args:
            config: The validated provider configuration.
        """
        ...

    def size_of(self, text: str) -> int:
        """Measure the text volume of ``text`` under :attr:`payload_unit`.

        Used by the adaptive scheduler to enforce the per-request
        ``payload_size`` limit. Providers MAY override this with a
        more accurate estimate; the default delegates to a generic
        helper in :mod:`translation_dubbing_skill.providers.sizing`.

        Args:
            text: The text to measure.

        Returns:
            A non-negative integer volume estimate.
        """
        ...

    async def synth(self, text: str, voice_id: str) -> tuple[bytes, int]:
        """Synthesize speech for a single non-empty text.

        Args:
            text: Text to synthesize. Callers guarantee this is non-empty.
            voice_id: Provider-specific voice identifier.

        Returns:
            A ``(audio_bytes, duration_ms)`` tuple. ``duration_ms`` is a
            non-negative integer.

        Raises:
            RateLimitError: The upstream signalled rate limiting.
            PayloadTooLargeError: The upstream rejected the request due
                to text volume.
            TransientError: Any other transient failure.
        """
        ...

    async def synth_batch(
        self,
        texts: list[str],
        voice_id: str,
    ) -> list[tuple[bytes, int]]:
        """Synthesize a batch of texts in a single upstream request.

        Only required when :attr:`supports_batch` is ``True``. Providers
        that genuinely batch MUST return one ``(audio_bytes, duration_ms)``
        tuple per input text, in order.

        Args:
            texts: Non-empty texts to synthesize. Order MUST be preserved
                in the output.
            voice_id: Provider-specific voice identifier.

        Returns:
            A list of ``(audio_bytes, duration_ms)`` pairs aligned 1:1
            with ``texts``.

        Raises:
            RateLimitError: The upstream signalled rate limiting.
            PayloadTooLargeError: The aggregated text volume exceeded
                the upstream's per-request limit.
            TransientError: Any other transient failure.
        """
        ...


def default_size_of_for(
    payload_unit: PayloadUnit,
) -> "callable[[str], int]":
    """Return a ``size_of`` function implementing the default for ``unit``.

    Concrete TTS providers can reuse this to wire up :meth:`size_of`
    without writing boilerplate::

        class MyTTSProvider:
            payload_unit = "chars"

            def size_of(self, text: str) -> int:
                return default_size_of(text, self.payload_unit)

    Args:
        payload_unit: ``"chars"`` or ``"tokens"``.

    Returns:
        A callable mapping ``text -> int`` under the requested unit.
    """

    def _sizer(text: str) -> int:
        return default_size_of(text, payload_unit)

    return _sizer


__all__ = ["TTSProvider", "default_size_of_for"]
