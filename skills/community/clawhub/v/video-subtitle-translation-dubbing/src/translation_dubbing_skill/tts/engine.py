"""TTS coordinator.

:class:`TTSEngine` is the upper-layer coordinator that drives any
registered :class:`~translation_dubbing_skill.providers.tts.protocol.TTSProvider`
through the shared :class:`~translation_dubbing_skill.scheduler.AdaptiveScheduler`.

Responsibilities (design §"语音合成协调器 TTSEngine"):

1. Instantiate the provider via :class:`ProviderRegistry`; re-raise
   :class:`ProviderNotRegisteredError` verbatim (with ``stage="tts"``)
   and wrap any other ``initialize``-time failure as
   :class:`ProviderUnavailableError` with ``phase="initialize"`` (R6.9).
2. Skip empty / whitespace-only entries entirely — they never reach the
   provider and never produce an :class:`AudioClip` (R6.1).
3. Resolve the effective ``voice_id``: prefer the caller-provided value,
   else fall back to ``config.extra["default_voice"]`` (R6.5).
4. Build a ``size_of`` closure from the provider's declared
   ``payload_unit`` (or the provider's own ``size_of`` when present)
   and pass it to the scheduler for double-dimension batching (R12.13).
5. Drive the scheduler with a ``fetch`` callback that dispatches to
   ``provider.synth_batch(texts, voice_id)`` when the provider
   advertises ``supports_batch=True``; otherwise the scheduler forces
   ``batch_size=1`` and ``fetch`` calls ``provider.synth(text, voice_id)``
   once per singleton batch (R12.14).
6. Report per-batch progress through the optional
   :class:`ProgressReporter`; ``completed`` is strictly monotonic
   non-decreasing and terminates at the number of non-empty entries
   (R11.3, R12.16).
7. Validate the scheduler's output shape (each element is a
   ``(bytes, int)`` pair and ``duration_ms >= 0``); on violation raise
   :class:`ProviderContractViolationError` with ``stage="tts"`` (R7.6).
8. Wrap :class:`SchedulerBatchFailure` as :class:`TTSError` carrying
   the batch's entry indices, the provider type, and the upstream
   reason (R6.10, R12.9).
9. Merge outputs back into order — the returned list is in the order
   of the original (non-empty) subtitle entries.

Corresponds to requirements R6.1, R6.2, R6.3, R6.5, R6.6, R6.8, R6.9,
R6.10, R7.3, R7.4, R7.6, R11.3, R12.2, R12.8, R12.9, R12.12, R12.13,
R12.14, R12.16.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Protocol

from translation_dubbing_skill.errors import (
    ProviderContractViolationError,
    ProviderNotRegisteredError,
    ProviderUnavailableError,
    TTSError,
)
from translation_dubbing_skill.models import (
    AudioClip,
    ProgressEvent,
    ProviderConfig,
    SubtitleEntry,
)
from translation_dubbing_skill.providers.registry import ProviderRegistry
from translation_dubbing_skill.scheduler import (
    AdaptiveScheduler,
    ProviderRateLimitConfig,
    SchedulerBatchFailure,
    is_payload_too_large,
    is_rate_limited,
    retry_after_of,
    size_of_for_unit,
)


class _ReporterLike(Protocol):
    """Minimal shape the engine needs from a progress reporter.

    Accepts any object exposing ``report(event)``. ``None`` is also
    allowed via the engine's constructor and means progress events are
    discarded.
    """

    def report(self, event: ProgressEvent) -> None: ...  # pragma: no cover


def _is_blank(text: str) -> bool:
    """Return ``True`` when ``text`` is empty or whitespace-only."""
    return not text.strip()


class TTSEngine:
    """Coordinate TTS provider calls through the adaptive scheduler.

    Instances are light-weight and safe to reuse across multiple
    :meth:`synthesize` calls (no per-call state lives on the instance).

    Args:
        registry: The provider registry used to resolve the requested
            ``provider_type`` to a concrete :class:`TTSProvider`
            implementation. Typically the module-level
            :data:`~translation_dubbing_skill.providers.default_registry`.
        reporter: Optional progress reporter. When ``None`` no progress
            events are emitted.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
        reporter: _ReporterLike | None = None,
    ) -> None:
        self._registry = registry
        self._reporter = reporter

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    async def synthesize(
        self,
        entries: list[SubtitleEntry],
        voice_id: str | None,
        provider_type: str,
        config: ProviderConfig,
        rate_limit_config: ProviderRateLimitConfig,
    ) -> list[AudioClip]:
        """Synthesize audio clips for every non-empty subtitle in ``entries``.

        Args:
            entries: Full list of subtitle entries. Empty and
                whitespace-only entries are skipped entirely (no clip
                is produced for them). May be empty, in which case the
                method returns ``[]`` without touching the provider.
            voice_id: Provider-specific voice identifier. When ``None``
                or empty, the engine falls back to
                ``config.extra["default_voice"]``. The resolved
                ``voice_id`` must itself be non-empty — an all-empty
                configuration raises :class:`ValueError` before any
                provider call (R6.5).
            provider_type: Stable identifier of the TTS provider to
                load from :attr:`registry` (e.g. ``"llm"``, ``"web"``).
            config: Provider configuration injected by the manifest.
            rate_limit_config: Adaptive scheduler knobs.

        Returns:
            A list of :class:`AudioClip` objects, one per non-empty
            input entry, in the original order of ``entries``. Each
            clip carries the provider's audio bytes and the measured
            ``duration_ms``.

        Raises:
            ProviderNotRegisteredError: Propagated from the registry
                when ``provider_type`` is unknown, carrying
                ``stage="tts"`` (R6.8).
            ProviderUnavailableError: The registered provider's
                ``initialize`` raised an exception (R6.9).
            TTSError: The scheduler exhausted its retry budget on at
                least one batch (R6.10). Context carries the
                ``entry_indices`` (0-indexed positions among the
                non-empty entries passed to the provider),
                ``provider_type``, and ``provider_reason``.
            ProviderContractViolationError: The provider's response
                violated the structural contract (wrong tuple shape,
                ``duration_ms < 0``) (R7.6).
            ValueError: Neither ``voice_id`` nor
                ``config.extra["default_voice"]`` resolved to a
                non-empty string.
        """
        if not entries:
            return []

        # --- 1. Resolve effective voice_id. --------------------------
        effective_voice = self._resolve_voice_id(voice_id, config)

        # --- 2. Filter non-empty entries, remembering their origin. --
        non_empty_entries: list[SubtitleEntry] = []
        non_empty_positions: list[int] = []
        for position, entry in enumerate(entries):
            if _is_blank(entry.text):
                continue
            non_empty_entries.append(entry)
            non_empty_positions.append(position)

        # --- 3. Instantiate the provider. ----------------------------
        provider = self._create_provider(provider_type, config)

        total = len(non_empty_entries)

        # --- 4. Short-circuit if everything was empty. ---------------
        if total == 0:
            return []

        # --- 5. Build the size_of closure for the scheduler. ---------
        text_sizer = self._build_text_sizer(
            provider,
            rate_limit_config.payload_unit,
        )

        def size_of_entry(entry: SubtitleEntry) -> int:
            return text_sizer(entry.text)

        # --- 6. Build the fetch closure around synth / synth_batch. -
        supports_batch = bool(getattr(provider, "supports_batch", False))
        completed = 0

        # Import the text normalizer
        from translation_dubbing_skill.tts.text_normalizer import normalize_text

        async def fetch_batch(
            batch: list[SubtitleEntry],
        ) -> list[tuple[bytes, int]]:
            texts = [normalize_text(e.text, effective_voice) for e in batch]
            outputs = await provider.synth_batch(texts, effective_voice)
            nonlocal completed
            completed += len(batch)
            self._report_progress(total=total, completed=completed)
            return outputs

        async def fetch_single(
            batch: list[SubtitleEntry],
        ) -> list[tuple[bytes, int]]:
            # Scheduler forces batch_size=1 for non-batch providers so
            # ``batch`` is always a singleton here; the defensive guard
            # keeps the fetch correct if a future change allows >1.
            results: list[tuple[bytes, int]] = []
            for entry in batch:
                normalized_text = normalize_text(entry.text, effective_voice)
                results.append(await provider.synth(normalized_text, effective_voice))
            nonlocal completed
            completed += len(batch)
            self._report_progress(total=total, completed=completed)
            return results

        fetch = fetch_batch if supports_batch else fetch_single

        # --- 7. Run through the adaptive scheduler. ------------------
        scheduler: AdaptiveScheduler[SubtitleEntry, tuple[bytes, int]] = (
            AdaptiveScheduler(
                rate_limit_config,
                reporter=self._reporter,
                size_of=size_of_entry,
                kind="tts",
                provider_type=provider_type,
            )
        )

        try:
            raw_results = await scheduler.run(
                non_empty_entries,
                fetch,
                is_rate_limited=is_rate_limited,
                is_payload_too_large=is_payload_too_large,
                retry_after_of=retry_after_of,
            )
        except SchedulerBatchFailure as exc:
            raise TTSError(
                f"tts batch failed after retries: {exc}",
                context={
                    "entry_indices": list(exc.entry_indices),
                    "provider_type": provider_type,
                    "provider_reason": str(exc.last_error),
                },
            ) from exc

        # --- 8. Validate the return shape + build AudioClip list. ---
        clips: list[AudioClip] = []
        for position, (entry, pair) in enumerate(
            zip(non_empty_entries, raw_results)
        ):
            audio, duration_ms = self._validate_pair(
                pair,
                entry=entry,
                position=position,
                provider_type=provider_type,
            )
            clips.append(
                AudioClip(
                    entry_index=entry.index,
                    start_ms=entry.start_ms,
                    end_ms=entry.end_ms,
                    audio=audio,
                    duration_ms=duration_ms,
                )
            )

        # Pin the final progress event at ``total`` in case the
        # scheduler short-circuited (defensive).
        if completed < total:
            self._report_progress(total=total, completed=total)

        return clips

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_voice_id(
        voice_id: str | None,
        config: ProviderConfig,
    ) -> str:
        """Return the voice id to use for this invocation.

        Preference order: explicit ``voice_id`` argument, then
        ``config.extra["default_voice"]``. Empty strings are treated as
        "not provided" so the fallback can take over.

        Raises:
            ValueError: If neither source produced a non-empty string.
        """
        if voice_id:
            return voice_id
        default_voice = None
        if config.extra:
            default_voice = config.extra.get("default_voice")
        if isinstance(default_voice, str) and default_voice:
            return default_voice
        raise ValueError(
            "TTSEngine: voice_id is required — provide it via the "
            "function argument or via config.extra['default_voice']"
        )

    def _create_provider(
        self,
        provider_type: str,
        config: ProviderConfig,
    ) -> Any:
        """Instantiate the provider, wrapping init failures.

        The registry's ``create`` call both constructs the class and
        invokes ``initialize(config)``, so any ``initialize``-time
        exception surfaces here. :class:`ProviderNotRegisteredError`
        is allowed to propagate unchanged (its ``stage`` is already
        ``"tts"`` thanks to the registry's per-kind stage map);
        everything else is wrapped as :class:`ProviderUnavailableError`
        with ``phase="initialize"`` and ``stage="tts"``.
        """
        try:
            return self._registry.create("tts", provider_type, config)
        except ProviderNotRegisteredError:
            # R6.8: surface unchanged so callers can match on the
            # specific subtype without losing registry context.
            raise
        except Exception as exc:
            raise ProviderUnavailableError(
                f"tts provider {provider_type!r} failed to initialize: {exc}",
                context={
                    "provider_type": provider_type,
                    "phase": "initialize",
                    "reason": str(exc),
                },
                stage="tts",
            ) from exc

    @staticmethod
    def _build_text_sizer(
        provider: Any,
        payload_unit: str,
    ) -> Callable[[str], int]:
        """Return a ``str -> int`` sizer honouring provider overrides.

        Preference order matches :class:`Translator`:

        1. ``provider.size_of(text)`` when callable (providers with a
           real tokenizer / accurate estimator advertise it there).
        2. The default per-unit sizer from
           :func:`~translation_dubbing_skill.scheduler.size_of_for_unit`.
        """
        size_of_attr = getattr(provider, "size_of", None)
        if callable(size_of_attr):
            return size_of_attr  # type: ignore[return-value]
        return size_of_for_unit(payload_unit)  # type: ignore[arg-type]

    def _validate_pair(
        self,
        pair: Any,
        *,
        entry: SubtitleEntry,
        position: int,
        provider_type: str,
    ) -> tuple[bytes, int]:
        """Unpack and validate one provider return value.

        The contract is ``(audio_bytes, duration_ms)`` where
        ``duration_ms`` is a non-negative integer. Any violation raises
        :class:`ProviderContractViolationError` with ``stage="tts"``.

        Args:
            pair: The item returned by the provider.
            entry: The source subtitle entry (used only for context).
            position: Position of ``entry`` within the non-empty list.
            provider_type: The provider kind (for error context).

        Returns:
            The validated ``(bytes, int)`` pair.
        """
        if not (isinstance(pair, tuple) and len(pair) == 2):
            raise ProviderContractViolationError(
                "tts provider returned non-(bytes, int) shape",
                context={
                    "violated_clause": "return_shape",
                    "provider_type": provider_type,
                    "entry_index": entry.index,
                    "position": position,
                },
                stage="tts",
            )
        audio, duration_ms = pair
        if not isinstance(audio, (bytes, bytearray)):
            raise ProviderContractViolationError(
                "tts provider returned non-bytes audio",
                context={
                    "violated_clause": "audio_type",
                    "provider_type": provider_type,
                    "entry_index": entry.index,
                    "position": position,
                    "actual_audio_type": type(audio).__name__,
                },
                stage="tts",
            )
        if not isinstance(duration_ms, int) or isinstance(duration_ms, bool):
            raise ProviderContractViolationError(
                "tts provider returned non-int duration_ms",
                context={
                    "violated_clause": "duration_ms_type",
                    "provider_type": provider_type,
                    "entry_index": entry.index,
                    "position": position,
                    "actual_duration_type": type(duration_ms).__name__,
                },
                stage="tts",
            )
        if duration_ms < 0:
            raise ProviderContractViolationError(
                "tts provider returned negative duration_ms",
                context={
                    "violated_clause": "duration_ms_negative",
                    "provider_type": provider_type,
                    "entry_index": entry.index,
                    "position": position,
                    "actual_duration_ms": duration_ms,
                },
                stage="tts",
            )
        return bytes(audio), duration_ms

    # ------------------------------------------------------------------
    # Progress
    # ------------------------------------------------------------------

    def _report_progress(self, *, total: int, completed: int) -> None:
        """Emit a TTS progress event, if a reporter is attached."""
        if self._reporter is None:
            return
        self._reporter.report(
            ProgressEvent(
                stage="tts",
                message="语音合成中",
                completed=completed,
                total=total,
            )
        )


__all__ = ["TTSEngine"]
