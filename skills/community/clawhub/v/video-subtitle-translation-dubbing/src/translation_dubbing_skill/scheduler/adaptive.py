"""Adaptive scheduler driving three-dimensional AIMD auto-tuning.

The scheduler is the shared execution layer used by both the translation
coordinator and the TTS coordinator to talk to providers. It simultaneously
manages three dimensions of load:

- ``batch_size``       — entries per batched request
- ``payload_size``     — total text volume per request (chars or tokens)
- ``concurrency``      — in-flight batch requests at any moment

On success it gradually up-tunes all three (additive increase after
``probe_up_every_n_success`` consecutive wins). On rate-limit feedback it
halves all three (multiplicative decrease) and waits per ``Retry-After``
or exponential backoff + jitter. On payload-too-large feedback it only
shrinks ``payload_size`` and re-slices the offending batch — this
re-slice does NOT consume the retry budget (R12.12). On other transient
failures it simply retries with backoff.

Design mapping: design §"自适应调度器 · AdaptiveScheduler", requirements
R12.1, R12.2, R12.5, R12.6, R12.7, R12.8, R12.9, R12.10, R12.11, R12.12,
R12.13, R12.14, R12.15, R12.16.
"""

from __future__ import annotations

import asyncio
import logging
import random
from dataclasses import dataclass, field
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    Protocol,
    TypeVar,
)

from translation_dubbing_skill.scheduler.config import ProviderRateLimitConfig
from translation_dubbing_skill.scheduler.signals import (
    is_payload_too_large as _default_is_payload_too_large,
    is_rate_limited as _default_is_rate_limited,
    retry_after_of as _default_retry_after_of,
)

_LOGGER = logging.getLogger(__name__)

I = TypeVar("I")   # single input item type (e.g. SubtitleEntry, str)
O = TypeVar("O")   # single output item type


class _ReporterLike(Protocol):
    """Minimal shape the scheduler needs from a progress reporter.

    Accepts either the full :class:`ProgressReporter` (once task 11.1
    lands) or a lightweight test double exposing ``report(event)``. The
    scheduler never constructs :class:`ProgressEvent` itself — progress
    is reported by the coordinators (Translator / TTSEngine), not here.
    This protocol exists so the scheduler constructor can accept
    ``None`` as well as any reporter without a hard dependency.
    """

    def report(self, event: Any) -> None: ...  # pragma: no cover


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SchedulerBatchFailure(Exception):
    """Raised by the scheduler when a batch exhausts its retry budget.

    The exception carries enough context for the coordinator to wrap it
    into a ``TranslationError`` / ``TTSError`` that lists the affected
    entry indices and provider type (R12.8, R12.9).

    Attributes:
        entry_indices: The positions (0-indexed) of the items in the
            original ``items`` list passed to :meth:`AdaptiveScheduler.run`
            that belonged to the failing batch.
        provider_type: The provider type label supplied at scheduler
            construction (e.g. ``"llm"`` or ``"web"``).
        last_error: The final exception that caused the budget to run
            out. Chained via ``__cause__`` as well for traceback clarity.
    """

    def __init__(
        self,
        reason: str,
        *,
        entry_indices: list[int],
        provider_type: str,
        last_error: BaseException,
    ) -> None:
        super().__init__(reason)
        self.entry_indices: list[int] = list(entry_indices)
        self.provider_type: str = provider_type
        self.last_error: BaseException = last_error


# ---------------------------------------------------------------------------
# Pure batching function (P43)
# ---------------------------------------------------------------------------


def make_batches(
    items: list[I],
    current_batch_size: int,
    current_payload_size: int,
    size_of: Callable[[I], int],
) -> list[list[I]]:
    """Split ``items`` into batches honouring both count and volume limits.

    Every produced batch ``B`` satisfies simultaneously:

    - ``len(B) <= current_batch_size`` (entry count cap);
    - ``sum(size_of(x) for x in B) <= current_payload_size`` (text volume
      cap), EXCEPT for the single-oversized-item escape hatch below.

    When a single item's size exceeds ``current_payload_size``, that item
    is emitted as its own singleton batch. The caller's ``size_of`` is
    trusted blindly, so this is the only way to make progress without
    knowing the upstream's real limit; if the provider subsequently
    rejects the singleton with :class:`PayloadTooLargeError`, the
    scheduler will further shrink ``current_payload_size`` and re-enter
    :func:`make_batches` until either the item fits or the floor is hit.

    Order is preserved: concatenating the output batches in iteration
    order reproduces ``items`` exactly (P43).

    Args:
        items: The full input list. May be empty, in which case the
            function returns ``[]``.
        current_batch_size: Current entry-count cap. Must be ``>= 1``.
        current_payload_size: Current volume cap. Must be ``>= 1``.
        size_of: Callable measuring one item's volume under the
            provider's ``payload_unit``. Must return a non-negative int.

    Returns:
        A list of non-empty batches covering ``items`` in order.

    Raises:
        ValueError: If ``current_batch_size < 1`` or
            ``current_payload_size < 1``.
    """
    if current_batch_size < 1:
        raise ValueError(
            f"current_batch_size must be >= 1, got {current_batch_size}"
        )
    if current_payload_size < 1:
        raise ValueError(
            f"current_payload_size must be >= 1, got {current_payload_size}"
        )

    batches: list[list[I]] = []
    current: list[I] = []
    current_payload = 0
    for item in items:
        item_size = size_of(item)
        if item_size < 0:
            raise ValueError(f"size_of returned negative value {item_size}")
        # Oversized singleton: flush the working batch, emit alone.
        if item_size > current_payload_size:
            if current:
                batches.append(current)
                current = []
                current_payload = 0
            batches.append([item])
            continue
        # Would exceed either cap → flush before appending.
        if (
            len(current) + 1 > current_batch_size
            or current_payload + item_size > current_payload_size
        ):
            if current:
                batches.append(current)
                current = []
                current_payload = 0
        current.append(item)
        current_payload += item_size
    if current:
        batches.append(current)
    return batches



# ---------------------------------------------------------------------------
# Internal scheduling state
# ---------------------------------------------------------------------------


@dataclass
class _PendingBatch(Generic[I]):
    """A batch enqueued for (possibly re-tried) execution.

    Carries both the payload (``items``) and the bookkeeping fields the
    scheduler needs to enforce the retry budget and place results back
    into the original order.
    """

    items: list[I]
    original_indices: list[int]
    # Number of attempts already spent on this batch. Incremented on
    # every rate-limit / transient failure. NOT incremented when the
    # batch is re-sliced due to PayloadTooLargeError (R12.12).
    attempts: int = 0
    # Wait (seconds) to observe before the next attempt; set by the
    # rate-limit / transient paths from Retry-After or exponential
    # backoff. Reset to 0 after being consumed.
    pending_delay_s: float = 0.0


@dataclass
class _SchedulerState:
    """Mutable runtime state shared across the scheduler's coroutines.

    All fields are protected by ``lock`` when mutated from more than one
    concurrent task. The AIMD adjustments are point updates on ints /
    floats so the lock can be held briefly.
    """

    batch_size: int
    payload_size: int
    concurrency: int
    consecutive_success: int = 0
    # Semaphore bounding in-flight work to ``concurrency``. Replaced on
    # every adjustment so new work sees the updated cap; tasks that
    # already hold a permit continue to completion under the old
    # semaphore (correct upper-bound semantics for any moment).
    semaphore: asyncio.Semaphore = field(init=False)
    lock: asyncio.Lock = field(init=False)

    def __post_init__(self) -> None:
        self.semaphore = asyncio.Semaphore(self.concurrency)
        self.lock = asyncio.Lock()


# ---------------------------------------------------------------------------
# AdaptiveScheduler
# ---------------------------------------------------------------------------


class AdaptiveScheduler(Generic[I, O]):
    """Three-dimensional AIMD scheduler for provider batch calls.

    Instances are single-use per :meth:`run` invocation. Internal state
    (``batch_size`` / ``payload_size`` / ``concurrency``) is initialised
    from :class:`ProviderRateLimitConfig` at the start of every
    :meth:`run` call so repeated invocations on the same scheduler
    object behave deterministically.

    Args:
        config: The rate-limit configuration. Validated on construction
            of the config object itself; the scheduler trusts the
            invariants.
        reporter: Optional progress reporter. The scheduler does NOT
            publish :class:`ProgressEvent` objects directly (that is the
            coordinator's responsibility) but the field is accepted per
            the design signature so future per-batch progress hooks can
            be wired in without breaking callers.
        size_of: Callable measuring a single input item's volume under
            the provider's ``payload_unit``. Injected by the coordinator
            so the scheduler stays generic over ``I``.
        kind: ``"translation"`` or ``"tts"`` — used only for structured
            logging. Defaults to ``"translation"``.
        provider_type: Stable identifier of the provider being driven
            (e.g. ``"llm"``, ``"web"``). Used in logs and in
            :class:`SchedulerBatchFailure`.
        clock: Source of monotonic time for backoff calculation. Defaults
            to :func:`asyncio.get_event_loop().time`. Injected only in
            tests that need deterministic timing.
        sleeper: Awaitable ``sleep(duration)``. Defaults to
            :func:`asyncio.sleep`. Tests injecting a virtual clock also
            inject a cooperating sleeper.
        rng: Source of randomness for jitter. Defaults to a module-level
            :class:`random.Random`. Seedable for deterministic tests.
    """

    def __init__(
        self,
        config: ProviderRateLimitConfig,
        reporter: _ReporterLike | None = None,
        size_of: Callable[[I], int] | None = None,
        *,
        kind: str = "translation",
        provider_type: str = "unknown",
        clock: Callable[[], float] | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._config = config
        self._reporter = reporter
        self._size_of: Callable[[I], int] = size_of if size_of is not None else (lambda _x: 0)
        self._kind = kind
        self._provider_type = provider_type
        self._clock = clock
        self._sleeper: Callable[[float], Awaitable[None]] = (
            sleeper if sleeper is not None else asyncio.sleep
        )
        self._rng: random.Random = rng if rng is not None else random.Random()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    async def run(
        self,
        items: list[I],
        fetch: Callable[[list[I]], Awaitable[list[O]]],
        *,
        is_rate_limited: Callable[[BaseException], bool] = _default_is_rate_limited,
        is_payload_too_large: Callable[[BaseException], bool] = _default_is_payload_too_large,
        retry_after_of: Callable[[BaseException], float | None] = _default_retry_after_of,
    ) -> list[O]:
        """Execute ``fetch`` over ``items`` with adaptive tuning.

        Args:
            items: The input list. May be empty — the scheduler returns
                ``[]`` immediately without touching the provider.
            fetch: Async callable taking one batch (a ``list[I]``) and
                returning a ``list[O]`` of the same length, in the same
                order. Signal errors (``RateLimitError`` etc.) raised
                from here drive the scheduler's feedback loop.
            is_rate_limited: Exception classifier used to detect rate-limit
                signals. Defaults to the module-level helper recognising
                :class:`RateLimitError` and HTTP 429.
            is_payload_too_large: Exception classifier used to detect
                payload-overflow signals. Defaults to the module helper
                recognising :class:`PayloadTooLargeError` and HTTP 413.
            retry_after_of: Extracts an explicit ``Retry-After`` wait
                (seconds) from a signal exception; returns ``None`` when
                the upstream did not advertise one.

        Returns:
            The list of outputs aligned 1:1 with ``items`` (same length,
            same order).

        Raises:
            SchedulerBatchFailure: If any batch exhausts its retry
                budget.
        """
        if not items:
            return []

        # Initialise mutable state fresh per run.
        initial_batch_size = self._config.batch_size_initial
        if not self._config.supports_batch:
            # R12.14: clamp batch_size to 1 for non-batching providers.
            initial_batch_size = 1
        state = _SchedulerState(
            batch_size=initial_batch_size,
            payload_size=self._config.payload_size_initial,
            concurrency=self._config.concurrency_initial,
        )

        # Build initial batches with original-index bookkeeping so we
        # can splice outputs back into order-preserving form.
        initial_batches = make_batches(
            items,
            state.batch_size,
            state.payload_size,
            self._size_of,
        )
        pending: list[_PendingBatch[I]] = []
        cursor = 0
        for batch in initial_batches:
            indices = list(range(cursor, cursor + len(batch)))
            cursor += len(batch)
            pending.append(
                _PendingBatch(items=list(batch), original_indices=indices)
            )

        # Results buffer indexed by original position.
        results: list[O | None] = [None] * len(items)

        # Work-queue drain: we process one "wave" at a time — all
        # currently-pending batches run concurrently (bounded by the
        # semaphore), their outcomes feed back into ``pending`` for the
        # next wave. This matches the design's asyncio.Queue-driven
        # model while keeping the control flow legible.
        while pending:
            wave = pending
            pending = []
            await self._run_wave(
                wave,
                fetch,
                state,
                pending,
                results,
                is_rate_limited=is_rate_limited,
                is_payload_too_large=is_payload_too_large,
                retry_after_of=retry_after_of,
            )

        # Tell type-checkers that every slot is now filled.
        out: list[O] = []
        for i, slot in enumerate(results):
            if slot is None:  # pragma: no cover - defensive
                raise RuntimeError(
                    f"AdaptiveScheduler: result[{i}] missing after run()"
                )
            out.append(slot)
        return out


    # ------------------------------------------------------------------
    # Wave execution
    # ------------------------------------------------------------------

    async def _run_wave(
        self,
        wave: list[_PendingBatch[I]],
        fetch: Callable[[list[I]], Awaitable[list[O]]],
        state: _SchedulerState,
        pending_out: list[_PendingBatch[I]],
        results: list[O | None],
        *,
        is_rate_limited: Callable[[BaseException], bool],
        is_payload_too_large: Callable[[BaseException], bool],
        retry_after_of: Callable[[BaseException], float | None],
    ) -> None:
        """Run every batch in ``wave`` concurrently under the semaphore.

        Successes write into ``results`` directly. Failures feed new
        :class:`_PendingBatch` entries into ``pending_out`` for the next
        wave (or raise :class:`SchedulerBatchFailure` when the retry
        budget is exhausted). Both code paths share the semaphore so
        the in-flight cap holds uniformly (R12.11).
        """
        # Snapshot the semaphore we will use for THIS wave. AIMD
        # adjustments may rebuild the semaphore mid-wave; tasks already
        # holding a permit from the snapshot finish under the old cap,
        # and subsequent waves pick up the new semaphore. This keeps
        # "at-any-moment in_flight <= current_concurrency" true even
        # across adjustments (P35).
        semaphore = state.semaphore

        async def _one(batch: _PendingBatch[I]) -> None:
            # Honour any scheduled backoff BEFORE acquiring a permit so
            # we don't hold in-flight slots while sleeping.
            if batch.pending_delay_s > 0:
                delay = batch.pending_delay_s
                batch.pending_delay_s = 0.0
                await self._sleeper(delay)

            async with semaphore:
                await self._execute_batch(
                    batch,
                    fetch,
                    state,
                    pending_out,
                    results,
                    is_rate_limited=is_rate_limited,
                    is_payload_too_large=is_payload_too_large,
                    retry_after_of=retry_after_of,
                )

        await asyncio.gather(*(_one(b) for b in wave))

    async def _execute_batch(
        self,
        batch: _PendingBatch[I],
        fetch: Callable[[list[I]], Awaitable[list[O]]],
        state: _SchedulerState,
        pending_out: list[_PendingBatch[I]],
        results: list[O | None],
        *,
        is_rate_limited: Callable[[BaseException], bool],
        is_payload_too_large: Callable[[BaseException], bool],
        retry_after_of: Callable[[BaseException], float | None],
    ) -> None:
        """Run one batch once, then handle its outcome.

        On success, writes outputs and records a success toward the
        AIMD up-tune counter. On failure, classifies the signal and
        either enqueues a retry / re-sliced batch or raises
        :class:`SchedulerBatchFailure` when the budget is exhausted.
        """
        attempt = batch.attempts + 1
        payload_size_actual = sum(self._size_of(item) for item in batch.items)
        log_base: dict[str, Any] = {
            "kind": self._kind,
            "provider_type": self._provider_type,
            "batch_size": len(batch.items),
            "payload_size_actual": payload_size_actual,
            "payload_unit": self._config.payload_unit,
            "concurrency": state.concurrency,
            "attempt": attempt,
        }

        try:
            outputs = await fetch(list(batch.items))
        except BaseException as exc:  # noqa: BLE001 - classify then re-raise/enqueue
            # Classify the error and drive the appropriate feedback path.
            rate_limited = is_rate_limited(exc)
            payload_too_large = is_payload_too_large(exc) if not rate_limited else False
            retry_after_ms: int | None = None
            # Log before deciding so failures are always observable.
            raw_retry_after = retry_after_of(exc)
            if raw_retry_after is not None:
                retry_after_ms = int(raw_retry_after * 1000)

            status = (
                "rate_limited"
                if rate_limited
                else "payload_too_large"
                if payload_too_large
                else "transient_error"
            )
            self._log_request(
                {
                    **log_base,
                    "rate_limited": rate_limited,
                    "payload_too_large": payload_too_large,
                    "retry_after_ms": retry_after_ms,
                    "status": status,
                }
            )

            if rate_limited:
                new_batch = max(state.batch_size // 2, self._config.batch_size_min)
                new_concurrency = max(state.concurrency // 2, self._config.concurrency_min)
                print(f"⚠️ [Rate Limit] Upstream throttled. Scaling down scheduler: batch_size={new_batch}, concurrency={new_concurrency}. Retrying in {raw_retry_after if raw_retry_after is not None else 'exponential backoff'}s...")
                await self._handle_rate_limited(
                    batch,
                    exc,
                    state,
                    pending_out,
                    retry_after=raw_retry_after,
                )
                return
            if payload_too_large:
                new_payload = max(state.payload_size // 2, self._config.payload_size_min)
                print(f"⚠️ [Payload Too Large] Overflow detected. Slicing down: new payload_size={new_payload}. Re-slicing batch of size {len(batch.items)}...")
                await self._handle_payload_too_large(
                    batch,
                    exc,
                    state,
                    pending_out,
                )
                return
            # Treat anything else as a transient error: backoff + retry.
            print(f"⚠️ [Transient Error] {type(exc).__name__}: {exc}. Retrying batch with backoff...")
            await self._handle_transient(
                batch,
                exc,
                state,
                pending_out,
            )
            return

        # -------- success path --------
        if len(outputs) != len(batch.items):
            # The provider violated the structural contract; surface as
            # a budget-exhausting failure. The coordinator wraps this
            # as ProviderContractViolationError (R7.6).
            err = SchedulerBatchFailure(
                f"provider returned {len(outputs)} outputs for batch of "
                f"{len(batch.items)} items",
                entry_indices=list(batch.original_indices),
                provider_type=self._provider_type,
                last_error=RuntimeError(
                    f"len(outputs)={len(outputs)} != len(batch)={len(batch.items)}"
                ),
            )
            self._log_request(
                {
                    **log_base,
                    "rate_limited": False,
                    "payload_too_large": False,
                    "retry_after_ms": None,
                    "status": "contract_violation",
                }
            )
            raise err

        # Splice outputs back into the results buffer in original order.
        for result, original_index in zip(outputs, batch.original_indices):
            results[original_index] = result

        self._log_request(
            {
                **log_base,
                "rate_limited": False,
                "payload_too_large": False,
                "retry_after_ms": None,
                "status": "ok",
            }
        )

        await self._record_success(state)


    # ------------------------------------------------------------------
    # Outcome handlers
    # ------------------------------------------------------------------

    async def _handle_rate_limited(
        self,
        batch: _PendingBatch[I],
        exc: BaseException,
        state: _SchedulerState,
        pending_out: list[_PendingBatch[I]],
        *,
        retry_after: float | None,
    ) -> None:
        """Multiplicative down-tune + retry (R12.6, R12.7).

        Halves all three dimensions (floored at each ``*_min``), schedules
        the retry after ``retry_after`` seconds (or exponential backoff +
        jitter when the upstream did not advertise one), and either
        enqueues the next attempt or raises :class:`SchedulerBatchFailure`
        if the retry budget is exhausted.
        """
        batch.attempts += 1
        if batch.attempts > self._config.max_retries:
            raise SchedulerBatchFailure(
                f"batch exhausted max_retries={self._config.max_retries} "
                f"on rate-limit path",
                entry_indices=list(batch.original_indices),
                provider_type=self._provider_type,
                last_error=exc,
            ) from exc

        await self._down_tune_all(state)

        delay_s = retry_after if retry_after is not None else self._backoff_seconds(
            batch.attempts
        )
        batch.pending_delay_s = delay_s
        pending_out.append(batch)

    async def _handle_payload_too_large(
        self,
        batch: _PendingBatch[I],
        exc: BaseException,
        state: _SchedulerState,
        pending_out: list[_PendingBatch[I]],
    ) -> None:
        """Shrink ``payload_size`` and re-slice (R12.12).

        Re-slicing does NOT consume the retry budget — this is a sizing
        correction, not an error recovery. The offending batch is split
        under the new ``payload_size`` via :func:`make_batches`, and each
        resulting sub-batch inherits the same ``attempts`` counter as
        the original so a later rate-limit on any sub-batch still
        respects the overall budget.
        """
        async with state.lock:
            new_payload = max(
                state.payload_size // 2, self._config.payload_size_min
            )
            state.payload_size = new_payload
            state.consecutive_success = 0

        sub_batches = make_batches(
            batch.items,
            state.batch_size,
            state.payload_size,
            self._size_of,
        )
        if not sub_batches:  # pragma: no cover - defensive
            sub_batches = [list(batch.items)]

        # Map every sub-batch back to its share of original indices, in
        # order. Because make_batches preserves input order, zipping
        # sub_batch lengths with the original index slice works.
        cursor = 0
        for sub in sub_batches:
            sub_indices = batch.original_indices[cursor : cursor + len(sub)]
            cursor += len(sub)
            pending_out.append(
                _PendingBatch(
                    items=list(sub),
                    original_indices=list(sub_indices),
                    attempts=batch.attempts,  # preserve budget
                    pending_delay_s=0.0,
                )
            )

    async def _handle_transient(
        self,
        batch: _PendingBatch[I],
        exc: BaseException,
        state: _SchedulerState,
        pending_out: list[_PendingBatch[I]],
    ) -> None:
        """Exponential backoff retry without down-tuning (design §TransientError).

        Bumps the retry counter; if the budget is exhausted, raises
        :class:`SchedulerBatchFailure`. Otherwise schedules the next
        attempt with exponential backoff + jitter.
        """
        batch.attempts += 1
        if batch.attempts > self._config.max_retries:
            raise SchedulerBatchFailure(
                f"batch exhausted max_retries={self._config.max_retries} "
                f"on transient path",
                entry_indices=list(batch.original_indices),
                provider_type=self._provider_type,
                last_error=exc,
            ) from exc

        async with state.lock:
            state.consecutive_success = 0

        batch.pending_delay_s = self._backoff_seconds(batch.attempts)
        pending_out.append(batch)

    async def _record_success(self, state: _SchedulerState) -> None:
        """Count a success and trigger an AIMD up-tune when appropriate.

        After ``probe_up_every_n_success`` consecutive wins, the
        scheduler additively increases all three dimensions by one step
        (per-unit for batch / concurrency, doubled for payload since
        the down-tune halves). Every dimension stays at or below its
        configured max (R12.5).
        """
        threshold = self._config.probe_up_every_n_success
        async with state.lock:
            state.consecutive_success += 1
            if state.consecutive_success < threshold:
                return
            state.consecutive_success = 0
            # Up-tune only what the config allows us to move.
            if self._config.supports_batch:
                state.batch_size = min(
                    state.batch_size + 1, self._config.batch_size_max
                )
            # Payload up-tune mirrors the halving down-tune by doubling;
            # clamped at max and guarded against staying stuck when
            # already at the max.
            state.payload_size = min(
                max(state.payload_size * 2, state.payload_size + 1),
                self._config.payload_size_max,
            )
            new_concurrency = min(
                state.concurrency + 1, self._config.concurrency_max
            )
            if new_concurrency != state.concurrency:
                state.concurrency = new_concurrency
                state.semaphore = asyncio.Semaphore(state.concurrency)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _down_tune_all(self, state: _SchedulerState) -> None:
        """Halve every dimension (floored at the per-dimension minimum)."""
        async with state.lock:
            state.consecutive_success = 0
            if self._config.supports_batch:
                state.batch_size = max(
                    state.batch_size // 2, self._config.batch_size_min
                )
            # R12.14: non-batching providers always run with batch_size=1;
            # no-op here keeps it that way.
            state.payload_size = max(
                state.payload_size // 2, self._config.payload_size_min
            )
            new_concurrency = max(
                state.concurrency // 2, self._config.concurrency_min
            )
            if new_concurrency != state.concurrency:
                state.concurrency = new_concurrency
                state.semaphore = asyncio.Semaphore(state.concurrency)

    def _backoff_seconds(self, attempt: int) -> float:
        """Return the exponential backoff + jitter for ``attempt`` (1-indexed).

        Formula::

            delay = base * 2**(attempt-1) + U(0, jitter)

        with ``base``/``jitter`` read from :class:`ProviderRateLimitConfig`
        in milliseconds. Jitter of ``0`` yields a deterministic wait
        (useful in tests).
        """
        exponent = max(attempt - 1, 0)
        base_ms = self._config.backoff_base_ms * (2**exponent)
        jitter_ms = 0
        if self._config.backoff_jitter_ms > 0:
            jitter_ms = self._rng.randint(0, self._config.backoff_jitter_ms)
        return (base_ms + jitter_ms) / 1000.0

    def _log_request(self, fields: dict[str, Any]) -> None:
        """Emit a single structured, credential-free log line.

        The scheduler never sees credentials (they live on
        :class:`ProviderConfig`, which providers consume internally) so
        the only redaction discipline needed here is "don't include
        ``fetch`` arguments". We log the computed metadata dict
        directly; downstream log handlers can filter / route by the
        ``kind`` / ``provider_type`` fields.

        Required fields (per design §自适应调度器 · 脱敏日志):
        ``kind``, ``provider_type``, ``batch_size``,
        ``payload_size_actual``, ``payload_unit``, ``concurrency``,
        ``attempt``, ``rate_limited``, ``payload_too_large``,
        ``retry_after_ms``, ``status``.
        """
        _LOGGER.info("scheduler_request %s", fields)


__all__ = [
    "AdaptiveScheduler",
    "SchedulerBatchFailure",
    "make_batches",
]
