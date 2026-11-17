"""Translation coordinator.

:class:`Translator` is the upper-layer coordinator that drives any
registered :class:`~translation_dubbing_skill.providers.translation.protocol.TranslationProvider`
through the shared :class:`~translation_dubbing_skill.scheduler.AdaptiveScheduler`.

Responsibilities (design §"翻译协调器 Translator"):

1. Instantiate the provider via :class:`ProviderRegistry`; re-raise
   :class:`ProviderNotRegisteredError` verbatim and wrap any other
   ``initialize``-time failure as :class:`ProviderUnavailableError`
   with ``phase="initialize"`` (R5.8).
2. Fast-path empty / whitespace-only entries: their translation is
   ``""`` and they are never sent to the provider (R5.6).
3. Build a ``size_of`` closure from the provider's declared
   ``payload_unit`` (or the provider's own ``size_of`` when present)
   and pass it to the scheduler for double-dimension batching (R12.13).
4. Drive the scheduler with ``fetch = provider.translate_batch`` and
   the signal classifiers from
   :mod:`translation_dubbing_skill.scheduler.signals` (R12.6, R12.12).
5. Report per-batch progress through the optional
   :class:`ProgressReporter`; ``completed`` is strictly monotonic
   non-decreasing and terminates at ``len(entries)`` (R11.2, R12.16).
6. Validate the scheduler's output against the structural contract
   (length / index / start_ms / end_ms equality) and the semantic
   contract (empty → empty; non-empty → non-empty simplified Chinese),
   raising :class:`ProviderContractViolationError` on violation (R7.6).
7. Wrap :class:`SchedulerBatchFailure` as :class:`TranslationError`
   carrying the batch's entry indices, the provider type, and the
   upstream reason (R5.9, R12.9).
8. Merge non-empty translations back with empty placeholders into a
   result list of the same length and order as the input (R5.2).

Sentence-context hint (R5.5) is honoured implicitly: entries are passed
to the scheduler (and therefore to ``translate_batch``) in their
original order; adjacent entries that semantically belong to the same
sentence naturally end up in the same batch because
:func:`~translation_dubbing_skill.scheduler.make_batches` preserves
order. Providers are free to inspect the contiguous list to recover
cross-entry context.

Corresponds to requirements R5.1, R5.2, R5.3, R5.5, R5.6, R5.7, R5.8,
R5.9, R7.1, R7.2, R7.5, R7.6, R11.2, R12.1, R12.8, R12.9, R12.12,
R12.13, R12.16.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Protocol

from translation_dubbing_skill.errors import (
    ProviderContractViolationError,
    ProviderNotRegisteredError,
    ProviderUnavailableError,
    TranslationError,
)
from translation_dubbing_skill.models import (
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
    """Minimal shape the translator needs from a progress reporter.

    Accepts any object exposing ``report(event)``. ``None`` is also
    allowed via the translator's constructor and means progress events
    are discarded.
    """

    def report(self, event: ProgressEvent) -> None: ...  # pragma: no cover


# ---------------------------------------------------------------------------
# Semantic contract helpers
# ---------------------------------------------------------------------------


# CJK Unified Ideographs + the common Extension A / Extension B ranges
# used in simplified Chinese text. We treat "contains at least one CJK
# ideograph" as a pragmatic proxy for "is simplified Chinese" — the
# skill targets ``zh-CN`` so the output is expected to be dominated by
# Han characters. A stricter variant would consult a script database,
# but that would add a runtime dependency for negligible extra value.
_CJK_RANGES: tuple[tuple[int, int], ...] = (
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0x3400, 0x4DBF),    # CJK Extension A
    (0x20000, 0x2A6DF),  # CJK Extension B
    (0x2A700, 0x2B73F),  # CJK Extension C
    (0x2B740, 0x2B81F),  # CJK Extension D
)


def _is_blank(text: str) -> bool:
    """Return ``True`` when ``text`` is empty or whitespace-only."""
    return not text.strip()


def _contains_cjk(text: str) -> bool:
    """Return ``True`` when ``text`` contains at least one CJK ideograph."""
    for ch in text:
        code = ord(ch)
        for low, high in _CJK_RANGES:
            if low <= code <= high:
                return True
    return False


# ---------------------------------------------------------------------------
# Translator
# ---------------------------------------------------------------------------


class Translator:
    """Coordinate translation provider calls through the adaptive scheduler.

    Instances are light-weight and safe to reuse across multiple
    :meth:`translate` calls (no per-call state lives on the instance).

    Args:
        registry: The provider registry used to resolve the requested
            ``provider_type`` to a concrete :class:`TranslationProvider`
            implementation. Typically the module-level
            :data:`~translation_dubbing_skill.providers.default_registry`.
        reporter: Optional progress reporter. When ``None`` no progress
            events are emitted. The translator never constructs
            :class:`ProgressEvent` objects when ``reporter is None`` so
            passing ``None`` is a zero-cost opt-out.
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

    async def translate(
        self,
        entries: list[SubtitleEntry],
        provider_type: str,
        config: ProviderConfig,
        rate_limit_config: ProviderRateLimitConfig,
        target_language: str = "zh-CN",
        source_language: str = "en",
    ) -> list[SubtitleEntry]:
        """Translate ``entries`` into ``target_language`` via the provider.

        Args:
            entries: Full list of subtitle entries to translate. May be
                empty (in which case the method returns ``[]``
                immediately without touching the provider).
            provider_type: Stable identifier of the provider to load
                from :attr:`registry` (e.g. ``"llm"``, ``"web"``).
            config: Provider configuration injected by the manifest.
            rate_limit_config: Adaptive scheduler knobs. The translator
                picks a default ``size_of`` based on
                ``rate_limit_config.payload_unit``; the provider may
                override with its own ``size_of`` method for more
                accurate estimates.
            target_language: BCP-47 language tag of the desired output.
                Defaults to ``"zh-CN"``; providers are free to accept
                any valid tag.
            source_language: BCP-47 language tag of the source language.
                Defaults to ``"en"``.

        Returns:
            A list of :class:`SubtitleEntry` of the same length and
            order as ``entries``; each entry carries the translated
            text (or ``""`` for whitespace-only inputs) while
            ``index`` / ``start_ms`` / ``end_ms`` are preserved.

        Raises:
            ProviderNotRegisteredError: Propagated unchanged from the
                registry when ``provider_type`` is unknown (R5.7).
            ProviderUnavailableError: The registered provider's
                ``initialize`` raised an exception (R5.8).
            TranslationError: The scheduler exhausted its retry budget
                on at least one batch (R5.9). The error carries the
                ``entry_indices`` (0-indexed positions within
                ``entries``), ``provider_type``, and
                ``provider_reason``.
            ProviderContractViolationError: The provider's response
                violated the structural contract (length / index /
                start_ms / end_ms) or the semantic contract
                (empty→empty; non-empty→non-empty text matching language checks)
                (R7.6).
        """
        total = len(entries)
        if total == 0:
            return []

        # --- 1. Split entries into empty / non-empty tracks. ----------
        #
        # ``non_empty_entries`` feeds the scheduler; ``non_empty_positions``
        # maps each non-empty entry back to its position in ``entries``
        # so the merged output preserves the original order.
        non_empty_entries: list[SubtitleEntry] = []
        non_empty_positions: list[int] = []
        for position, entry in enumerate(entries):
            if _is_blank(entry.text):
                continue
            non_empty_entries.append(entry)
            non_empty_positions.append(position)

        # --- 2. Instantiate the provider. ----------------------------
        provider = self._create_provider(provider_type, config)

        # --- 3. If nothing to translate, short-circuit with empties. -
        if not non_empty_entries:
            self._report_progress(total=total, completed=total)
            return [
                SubtitleEntry(
                    index=e.index,
                    start_ms=e.start_ms,
                    end_ms=e.end_ms,
                    text="",
                )
                for e in entries
            ]

        # --- 4. Build the size_of closure. ---------------------------
        text_sizer = self._build_text_sizer(
            provider,
            rate_limit_config.payload_unit,
        )

        def size_of_entry(entry: SubtitleEntry) -> int:
            return text_sizer(entry.text)

        # --- 5. Build the scheduler + progress-tracking fetch. -------
        completed = 0

        async def fetch(
            batch: list[SubtitleEntry],
        ) -> list[SubtitleEntry]:
            # Some providers accept source_language too.
            # To be compatible, we can check if provider method supports source_language,
            # or pass it if it accepts positional/keyword args.
            try:
                outputs = await provider.translate_batch(
                    batch,
                    target_language=target_language,
                    source_language=source_language,
                )
            except TypeError:
                # Fallback for providers that don't accept source_language yet
                outputs = await provider.translate_batch(batch, target_language)

            # R12.16: report cumulative progress after every successful
            # batch.
            nonlocal completed
            completed += len(batch)
            self._report_progress(total=total, completed=completed)
            return outputs

        scheduler: AdaptiveScheduler[SubtitleEntry, SubtitleEntry] = (
            AdaptiveScheduler(
                rate_limit_config,
                reporter=self._reporter,
                size_of=size_of_entry,
                kind="translation",
                provider_type=provider_type,
            )
        )

        # --- 6. Run the scheduler. -----------------------------------
        try:
            translated_non_empty = await scheduler.run(
                non_empty_entries,
                fetch,
                is_rate_limited=is_rate_limited,
                is_payload_too_large=is_payload_too_large,
                retry_after_of=retry_after_of,
            )
        except SchedulerBatchFailure as exc:
            # Map scheduler's batch positions to the caller's view:
            # ``exc.entry_indices`` are indices into
            # ``non_empty_entries``; translate them back to positions
            # in the original ``entries`` list so the TranslationError
            # context is meaningful end-to-end.
            original_indices = [
                non_empty_positions[i] for i in exc.entry_indices
            ]
            raise TranslationError(
                f"translation batch failed after retries: {exc}",
                context={
                    "entry_indices": original_indices,
                    "provider_type": provider_type,
                    "provider_reason": str(exc.last_error),
                },
            ) from exc

        # --- 7. Validate structural + semantic contracts. ------------
        self._validate_contract(
            inputs=non_empty_entries,
            outputs=translated_non_empty,
            provider_type=provider_type,
            target_language=target_language,
        )

        # --- 8. Merge non-empty outputs with empty placeholders. ----
        merged: list[SubtitleEntry] = []
        translated_iter = iter(translated_non_empty)
        non_empty_index_set = set(non_empty_positions)
        for position, original in enumerate(entries):
            if position in non_empty_index_set:
                merged.append(next(translated_iter))
            else:
                merged.append(
                    SubtitleEntry(
                        index=original.index,
                        start_ms=original.start_ms,
                        end_ms=original.end_ms,
                        text="",
                    )
                )

        # Final progress event pins completed at total even if the
        # provider short-circuited (defensive; the scheduler normally
        # delivers len(non_empty_entries) progress hits).
        if completed < total:
            self._report_progress(total=total, completed=total)

        return merged

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_provider(
        self,
        provider_type: str,
        config: ProviderConfig,
    ) -> Any:
        """Instantiate the provider, wrapping init failures.

        The registry's ``create`` call both constructs the class and
        invokes ``initialize(config)``, so any ``initialize``-time
        exception surfaces here. :class:`ProviderNotRegisteredError` is
        allowed to propagate unchanged (it already carries the right
        stage and context); everything else is wrapped as
        :class:`ProviderUnavailableError` with ``phase="initialize"``.
        """
        try:
            return self._registry.create("translation", provider_type, config)
        except ProviderNotRegisteredError:
            # R5.7: surface unchanged so callers can match on the
            # specific subtype without losing registry context.
            raise
        except Exception as exc:
            raise ProviderUnavailableError(
                f"translation provider {provider_type!r} failed to initialize: {exc}",
                context={
                    "provider_type": provider_type,
                    "phase": "initialize",
                    "reason": str(exc),
                },
                stage="translating",
            ) from exc

    @staticmethod
    def _build_text_sizer(
        provider: Any,
        payload_unit: str,
    ) -> Callable[[str], int]:
        """Return a ``str -> int`` sizer honouring provider overrides.

        Preference order:

        1. ``provider.size_of(text)`` when the attribute is callable —
           providers with access to a real tokenizer advertise a more
           accurate estimate there (design §"自适应调度器 · 文本量度量").
        2. The default per-unit sizer from
           :func:`~translation_dubbing_skill.scheduler.size_of_for_unit`
           otherwise.
        """
        size_of_attr = getattr(provider, "size_of", None)
        if callable(size_of_attr):
            return size_of_attr  # type: ignore[return-value]
        # ``payload_unit`` comes from the caller-provided rate-limit
        # config, which the config dataclass has already validated to
        # be one of ``"chars" | "tokens"``. Pass through verbatim.
        return size_of_for_unit(payload_unit)  # type: ignore[arg-type]

    def _validate_contract(
        self,
        *,
        inputs: list[SubtitleEntry],
        outputs: list[SubtitleEntry],
        provider_type: str,
        target_language: str = "zh-CN",
    ) -> None:
        """Check structural + semantic contracts; raise on violation.

        Structural (R7.1):
            - ``len(outputs) == len(inputs)``
            - per-index ``index / start_ms / end_ms`` match

        Semantic (R7.2):
            - For every ``i``: whitespace-only input produces
              ``output.text == ""``
            - For every ``i``: non-empty input produces non-empty text.
              If target_language is Simplified / Traditional Chinese (starts with 'zh'),
              we additionally verify it contains at least one CJK ideograph (R7.2).

        Raises :class:`ProviderContractViolationError` with ``stage="translating"``
        and ``context`` carrying the violated clause and the offending
        ``entry_index`` (the input's original ``index`` field when
        available).
        """
        if len(outputs) != len(inputs):
            raise ProviderContractViolationError(
                (
                    f"provider returned {len(outputs)} entries for a batch "
                    f"of {len(inputs)}"
                ),
                context={
                    "violated_clause": "length_mismatch",
                    "provider_type": provider_type,
                    "expected_length": len(inputs),
                    "actual_length": len(outputs),
                },
                stage="translating",
            )

        for position, (src, dst) in enumerate(zip(inputs, outputs)):
            if dst.index != src.index:
                raise ProviderContractViolationError(
                    "provider altered subtitle index",
                    context={
                        "violated_clause": "index_mismatch",
                        "provider_type": provider_type,
                        "entry_index": src.index,
                        "position": position,
                        "expected_index": src.index,
                        "actual_index": dst.index,
                    },
                    stage="translating",
                )
            if dst.start_ms != src.start_ms:
                raise ProviderContractViolationError(
                    "provider altered subtitle start_ms",
                    context={
                        "violated_clause": "start_ms_mismatch",
                        "provider_type": provider_type,
                        "entry_index": src.index,
                        "position": position,
                        "expected_start_ms": src.start_ms,
                        "actual_start_ms": dst.start_ms,
                    },
                    stage="translating",
                )
            if dst.end_ms != src.end_ms:
                raise ProviderContractViolationError(
                    "provider altered subtitle end_ms",
                    context={
                        "violated_clause": "end_ms_mismatch",
                        "provider_type": provider_type,
                        "entry_index": src.index,
                        "position": position,
                        "expected_end_ms": src.end_ms,
                        "actual_end_ms": dst.end_ms,
                    },
                    stage="translating",
                )

            # Semantic checks. We know ``src.text`` is non-blank here
            # because empty entries were filtered out before the
            # provider was called.
            text = dst.text
            if _is_blank(text):
                raise ProviderContractViolationError(
                    "provider produced empty translation for non-empty input",
                    context={
                        "violated_clause": "empty_translation_for_nonempty_input",
                        "provider_type": provider_type,
                        "entry_index": src.index,
                        "position": position,
                    },
                    stage="translating",
                )
            # Only enforce CJK validation if translating to Chinese
            if target_language.lower().startswith("zh"):
                if not _contains_cjk(text):
                    raise ProviderContractViolationError(
                        "provider produced translation without simplified Chinese characters",
                        context={
                            "violated_clause": "non_simplified_chinese_output",
                            "provider_type": provider_type,
                            "entry_index": src.index,
                            "position": position,
                        },
                        stage="translating",
                    )

    # ------------------------------------------------------------------
    # Progress
    # ------------------------------------------------------------------

    def _report_progress(self, *, total: int, completed: int) -> None:
        """Emit a translation progress event, if a reporter is attached."""
        if self._reporter is None:
            return
        self._reporter.report(
            ProgressEvent(
                stage="translating",
                message="翻译中",
                completed=completed,
                total=total,
            )
        )


__all__ = ["Translator"]
