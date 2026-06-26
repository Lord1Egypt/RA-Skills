"""
scheduler.py — Sigrid's Time & Background Task Scheduler
=========================================================

Adapted from timeline_service.py. Drops the game simulation clock
(turn-minutes, seasons, travel tables) and replaces it with real
wall-clock time awareness plus APScheduler for background periodic tasks.

Two responsibilities:

  1. Time-of-day awareness — maps the real current hour to a named
     segment (dawn / morning / midday / afternoon / evening / night).
     Sigrid's mood, tone, and energy shift across the day; prompt_synthesizer
     reads this to tune her voice.

  2. Background job scheduler — APScheduler BackgroundScheduler manages
     periodic callbacks (heartbeat ticks, memory consolidation, dream
     ticks, oracle refresh, etc.). Jobs are registered by name and can
     be started, paused, and removed at runtime.

Norse framing: Dagr (the god of Day) drives his horse Skinfaxi across
the sky. The light he casts changes everything beneath it — Sigrid is
alive to the time of day in ways that matter.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

# ─── Time segments ────────────────────────────────────────────────────────────
# Maps real wall-clock hour (0-23) to a named time-of-day segment.
# Each segment carries a mood hint for prompt_synthesizer.

_TIME_SEGMENTS: tuple = (
    (5,  "deep night"),     # 00:00–04:59
    (8,  "dawn"),           # 05:00–07:59
    (12, "morning"),        # 08:00–11:59
    (14, "midday"),         # 12:00–13:59
    (18, "afternoon"),      # 14:00–17:59
    (21, "evening"),        # 18:00–20:59
    (24, "night"),          # 21:00–23:59
)

_SEGMENT_HINTS: Dict[str, str] = {
    "deep night": "quiet and introspective; the veil is thin",
    "dawn":       "liminal and gentle; the world waking",
    "morning":    "alert and purposeful; fresh energy",
    "midday":     "clear and direct; full presence",
    "afternoon":  "warm and steady; flowing forward",
    "evening":    "reflective and warm; candle-light mind",
    "night":      "soft and inward; the day settling",
}


def _current_time_of_day() -> str:
    """Map the current local hour to a named time-of-day segment."""
    hour = datetime.now().hour
    for threshold, label in _TIME_SEGMENTS:
        if hour < threshold:
            return label
    return "night"


# ─── Seasonal bands (E-14) ────────────────────────────────────────────────────
# Six astronomical seasons (northern hemisphere). Each tuple:
#   (month_start, day_start, month_end, day_end,
#    season_name, energy_modifier, light_quality)
# Energy modifier: 0.85 = 15% drain (deep winter), 1.10 = 10% boost (summer).

_SEASONAL_BANDS_NORTH: Tuple = (
    (12, 21, 1, 31, "winter_deep",  0.85, "long dark nights, cold clarity"),
    ( 2,  1, 3, 19, "winter_end",   0.90, "lengthening days, pale light returning"),
    ( 3, 20, 6, 20, "spring",       1.00, "equinox light, rising energy"),
    ( 6, 21, 8, 31, "summer",       1.10, "long solstice days, high vitality"),
    ( 9,  1, 9, 22, "harvest",      0.95, "golden light, abundance and gathering"),
    ( 9, 23, 12, 20, "autumn_deep", 0.90, "fading light, turning inward"),
)

# Solstice and equinox reference dates (fixed year-agnostic day-of-year)
_SUMMER_SOLSTICE_MONTH, _SUMMER_SOLSTICE_DAY = 6, 21
_WINTER_SOLSTICE_MONTH, _WINTER_SOLSTICE_DAY = 12, 21


def _days_between(m1: int, d1: int, m2: int, d2: int) -> int:
    """Approximate day-of-year distance between two (month, day) pairs."""
    year = 2000  # leap year for safe Feb 29 handling
    try:
        dt1 = date(year, m1, d1)
        dt2 = date(year, m2, d2)
        return abs((dt2 - dt1).days)
    except ValueError:
        return 90  # safe fallback


def _get_seasonal_state(hemisphere: str = "north", today: Optional[date] = None) -> "SeasonalState":
    """Compute SeasonalState for the given hemisphere and date."""
    if today is None:
        today = datetime.now(timezone.utc).date()

    # For southern hemisphere, flip 6 months
    if hemisphere == "south":
        month = ((today.month - 1 + 6) % 12) + 1
        check_day = today.day
    else:
        month = today.month
        check_day = today.day

    # Match current date against the seasonal bands
    season_name = "autumn_deep"
    energy_modifier = 0.90
    light_quality = "fading light, turning inward"

    for (ms, ds, me, de, name, em, lq) in _SEASONAL_BANDS_NORTH:
        if ms <= me:
            # Normal range (no year wrap)
            if (month == ms and check_day >= ds) or (ms < month < me) or (month == me and check_day <= de):
                season_name, energy_modifier, light_quality = name, em, lq
                break
        else:
            # Wraps across year boundary (e.g. Dec 21 – Jan 31)
            if (month == ms and check_day >= ds) or (month > ms) or (month < me) or (month == me and check_day <= de):
                season_name, energy_modifier, light_quality = name, em, lq
                break

    # Compute solstice proximity (nearer of summer/winter solstice, same year)
    year = today.year
    try:
        summer_sol = date(year, _SUMMER_SOLSTICE_MONTH, _SUMMER_SOLSTICE_DAY)
        winter_sol = date(year, _WINTER_SOLSTICE_MONTH, _WINTER_SOLSTICE_DAY)
        summer_away = abs((today - summer_sol).days)
        winter_away = abs((today - winter_sol).days)
        solstice_days_away = min(summer_away, winter_away)
    except Exception:
        solstice_days_away = 90

    return SeasonalState(
        season_name=season_name,
        energy_modifier=energy_modifier,
        light_quality=light_quality,
        solstice_days_away=solstice_days_away,
    )


@dataclass(slots=True)
class SeasonalState:
    """E-14: Astronomical season awareness — Dagr and Nótt measure the light."""

    season_name: str            # winter_deep / winter_end / spring / summer / harvest / autumn_deep
    energy_modifier: float      # 0.85–1.10 — multiplier for bio_engine energy_reserve
    light_quality: str          # prose description for prompt injection
    solstice_days_away: int     # distance in days to nearest solstice

    def to_dict(self) -> Dict[str, Any]:
        return {
            "season_name": self.season_name,
            "energy_modifier": round(self.energy_modifier, 3),
            "light_quality": self.light_quality,
            "solstice_days_away": self.solstice_days_away,
        }


# ─── Heartbeat utility (E-13) ────────────────────────────────────────────────

def get_heartbeat_age_s(session_dir: str) -> Optional[float]:
    """Return seconds since the last heartbeat write, or None if unreadable.

    Used by main.py startup and MimirHealthMonitor to detect a dead scheduler.
    """
    try:
        path = Path(session_dir) / "heartbeat.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        ts = datetime.fromisoformat(data["ts"])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - ts).total_seconds()
    except Exception as exc:
        logger.debug("get_heartbeat_age_s failed: %s", exc)
        return None


# ─── SchedulerState ───────────────────────────────────────────────────────────


@dataclass(slots=True)
class SchedulerState:
    """Typed snapshot of scheduler health and current time awareness."""

    time_of_day: str
    time_hint: str              # mood/tone hint for this segment
    active_job_count: int
    job_names: List[str]
    running: bool
    prompt_hint: str
    timestamp: str
    heartbeat_age_s: Optional[float] = None   # E-13: seconds since last heartbeat write
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": {
                "segment": self.time_of_day,
                "hint": self.time_hint,
            },
            "jobs": {
                "active": self.active_job_count,
                "names": self.job_names,
                "running": self.running,
            },
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "heartbeat_age_s": self.heartbeat_age_s,
            "degraded": self.degraded,
        }


# ─── SchedulerService ─────────────────────────────────────────────────────────


class SchedulerService:
    """Real-time scheduler — time-of-day awareness + APScheduler background jobs.

    Call ``start()`` to begin background processing. Register periodic
    callbacks with ``register_job()``. The scheduler degrades gracefully
    if APScheduler is not available — time-of-day awareness still works.
    """

    def __init__(
        self,
        timezone_str: str = "local",
        session_dir: Optional[str] = None,
        hemisphere: str = "north",
    ) -> None:
        self._timezone_str = timezone_str
        self._session_dir = session_dir
        self._hemisphere = hemisphere
        self._heartbeat_path: Optional[Path] = (
            Path(session_dir) / "heartbeat.json" if session_dir else None
        )
        self._jobs: Dict[str, Dict[str, Any]] = {}   # name → {func, interval_s, job_id}
        self._scheduler = None
        self._running: bool = False
        self._degraded: bool = False
        # E-15: track whether dream.tick has been published for the current deep_night
        self._deep_night_published: bool = False

        self._init_apscheduler()

    # ── Public API ────────────────────────────────────────────────────────────

    def register_job(
        self,
        name: str,
        func: Callable[[], None],
        interval_s: float,
        replace_existing: bool = True,
    ) -> bool:
        """Register a named periodic job.

        Returns True if the job was registered (and scheduled if running).
        ``func`` must be a zero-argument callable.
        """
        if name in self._jobs and not replace_existing:
            logger.debug("SchedulerService: job '%s' already registered.", name)
            return False

        self._jobs[name] = {
            "func": func,
            "trigger": "interval",
            "interval_s": interval_s,
            "job_id": f"sigrid_{name}",
        }

        if self._running and self._scheduler is not None:
            self._add_apscheduler_job(name)

        logger.info("SchedulerService: job '%s' registered (interval=%.1fs).", name, interval_s)
        return True

    def register_cron_job(
        self,
        name: str,
        func: Callable[[], None],
        hour: int,
        minute: int,
        replace_existing: bool = True,
    ) -> bool:
        """E-19: Register a named daily cron job to run at HH:MM local time.

        Returns True if the job was registered.
        ``func`` must be a zero-argument callable.
        """
        if name in self._jobs and not replace_existing:
            logger.debug("SchedulerService: cron job '%s' already registered.", name)
            return False

        self._jobs[name] = {
            "func": func,
            "trigger": "cron",
            "hour": hour,
            "minute": minute,
            "job_id": f"sigrid_{name}",
        }

        if self._running and self._scheduler is not None:
            self._add_apscheduler_job(name)

        logger.info(
            "SchedulerService: cron job '%s' registered (daily at %02d:%02d).",
            name, hour, minute,
        )
        return True

    def register_consolidation_job(
        self,
        consolidator: Any,
        bus: Any,
    ) -> bool:
        """E-19: Register the nightly memory consolidation job at 03:30 local time.

        ``consolidator`` must be a MemoryConsolidator instance.
        ``bus`` must be a StateBus instance.
        """
        def _consolidation_job() -> None:
            try:
                consolidator.run(bus=bus)
            except Exception as exc:
                logger.warning("SchedulerService: consolidation job failed: %s", exc)

        return self.register_cron_job("memory_consolidation", _consolidation_job, hour=3, minute=30)

    def remove_job(self, name: str) -> bool:
        """Remove a named job. Returns True if it existed."""
        if name not in self._jobs:
            return False
        if self._scheduler is not None:
            try:
                self._scheduler.remove_job(f"sigrid_{name}")
            except Exception as exc:
                logger.debug("SchedulerService.remove_job: APScheduler remove failed (job may not exist): %s", exc)
        del self._jobs[name]
        logger.info("SchedulerService: job '%s' removed.", name)
        return True

    def start(self) -> None:
        """Start the background scheduler and all registered jobs.

        E-13: Auto-registers the heartbeat job if session_dir was provided.
        """
        if self._running:
            return
        # E-13: register heartbeat before starting
        if self._heartbeat_path is not None:
            self.register_job("heartbeat", self._heartbeat_tick, interval_s=60.0)

        if self._scheduler is None:
            logger.warning("SchedulerService: APScheduler unavailable — background jobs disabled.")
            self._degraded = True
            return
        try:
            for name in self._jobs:
                self._add_apscheduler_job(name)
            self._scheduler.start()
            self._running = True
            logger.info("SchedulerService started (%d jobs).", len(self._jobs))
        except Exception as exc:
            logger.warning("SchedulerService.start() failed: %s", exc)
            self._degraded = True

    def stop(self) -> None:
        """Stop the background scheduler gracefully."""
        if not self._running or self._scheduler is None:
            return
        try:
            self._scheduler.shutdown(wait=False)
            self._running = False
            logger.info("SchedulerService stopped.")
        except Exception as exc:
            logger.warning("SchedulerService.stop() failed: %s", exc)

    def time_of_day(self) -> str:
        """Return the current named time-of-day segment."""
        return _current_time_of_day()

    def time_hint(self) -> str:
        """Return the mood/tone hint for the current time segment."""
        return _SEGMENT_HINTS.get(self.time_of_day(), "present and aware")

    # ── State bus integration ─────────────────────────────────────────────────

    def get_state(self) -> SchedulerState:
        """Build a typed SchedulerState snapshot."""
        tod = self.time_of_day()
        hint = _SEGMENT_HINTS.get(tod, "")
        names = list(self._jobs.keys())
        prompt_hint = f"[Time: {tod} — {hint}]"
        # E-13: include heartbeat age in state
        hb_age = get_heartbeat_age_s(self._session_dir) if self._session_dir else None
        return SchedulerState(
            time_of_day=tod,
            time_hint=hint,
            active_job_count=len(names),
            job_names=names,
            running=self._running,
            prompt_hint=prompt_hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            heartbeat_age_s=hb_age,
            degraded=self._degraded,
        )

    def get_seasonal_state(self, today: Optional[date] = None) -> SeasonalState:
        """E-14: Return the current SeasonalState for this scheduler's hemisphere."""
        return _get_seasonal_state(hemisphere=self._hemisphere, today=today)

    def publish(self, bus: StateBus) -> None:
        """Emit a ``scheduler_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="scheduler",
                event_type="scheduler_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("SchedulerService.publish failed: %s", exc)

    # ── E-13: Heartbeat ───────────────────────────────────────────────────────

    def _heartbeat_tick(self) -> None:
        """Write a timestamped heartbeat record to session/heartbeat.json."""
        if self._heartbeat_path is None:
            return
        try:
            self._heartbeat_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "pid": os.getpid(),
            }
            self._heartbeat_path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            logger.debug("SchedulerService: heartbeat written to %s", self._heartbeat_path)
        except Exception as exc:
            logger.warning("SchedulerService: heartbeat write failed: %s", exc)

    # ── E-15: Dream tick ──────────────────────────────────────────────────────

    def emit_dream_tick_if_needed(self, bus: StateBus) -> bool:
        """Publish 'dream.tick' once per deep_night entry to the state bus.

        Returns True if the event was published this call.
        """
        tod = self.time_of_day()
        if tod == "deep night":
            if not self._deep_night_published:
                try:
                    event = StateEvent(
                        source_module="scheduler",
                        event_type="dream.tick",
                        payload={"time_of_day": tod, "ts": datetime.now(timezone.utc).isoformat()},
                    )
                    import asyncio as _asyncio
                    loop = _asyncio.get_event_loop()
                    if loop.is_running():
                        loop.call_soon_threadsafe(
                            loop.create_task,
                            bus.publish_state(event, nowait=True),
                        )
                    else:
                        loop.run_until_complete(bus.publish_state(event, nowait=True))
                    self._deep_night_published = True
                    logger.info("SchedulerService: dream.tick published for deep_night")
                    return True
                except Exception as exc:
                    logger.warning("SchedulerService: dream.tick publish failed: %s", exc)
        else:
            # Reset flag so next deep_night can fire again
            self._deep_night_published = False
        return False

    # ── Internals ─────────────────────────────────────────────────────────────

    def _init_apscheduler(self) -> None:
        try:
            import os as _os
            from apscheduler.schedulers.background import BackgroundScheduler
            # Size thread pool to the hardware — never more than one thread per
            # logical core, never more than 4 for background jobs (keeps RPi stable).
            _pool_size = min(max(1, (_os.cpu_count() or 1)), 4)
            self._scheduler = BackgroundScheduler(
                job_defaults={"coalesce": True, "max_instances": 1},
                executors={"default": {"type": "threadpool", "max_workers": _pool_size}},
            )
            logger.info("SchedulerService: APScheduler ready (thread_pool=%d).", _pool_size)
        except ImportError:
            logger.warning("SchedulerService: APScheduler not installed — background jobs disabled.")
            self._scheduler = None
            self._degraded = True

    def _add_apscheduler_job(self, name: str) -> None:
        if self._scheduler is None:
            return
        job_cfg = self._jobs[name]
        trigger = job_cfg.get("trigger", "interval")
        try:
            if trigger == "cron":
                self._scheduler.add_job(
                    func=job_cfg["func"],
                    trigger="cron",
                    hour=job_cfg["hour"],
                    minute=job_cfg["minute"],
                    id=job_cfg["job_id"],
                    replace_existing=True,
                )
            else:
                self._scheduler.add_job(
                    func=job_cfg["func"],
                    trigger="interval",
                    seconds=job_cfg["interval_s"],
                    id=job_cfg["job_id"],
                    replace_existing=True,
                )
        except Exception as exc:
            logger.warning("SchedulerService: failed to add job '%s': %s", name, exc)

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "SchedulerService":
        """Construct from a config dict.

        Reads keys under ``scheduler``:
          timezone      (str, default "local")
          session_dir   (str, default None) — E-13 heartbeat path
          hemisphere    (str, default "north") — E-14 seasonal awareness
        """
        cfg: Dict[str, Any] = config.get("scheduler", {})
        hemisphere = str(
            cfg.get("hemisphere")
            or config.get("hemisphere", "north")  # also accepts top-level key
        )
        return cls(
            timezone_str=str(cfg.get("timezone", "local")),
            session_dir=cfg.get("session_dir") or None,
            hemisphere=hemisphere,
        )


# ─── Singleton ────────────────────────────────────────────────────────────────

_SCHEDULER: Optional[SchedulerService] = None


def init_scheduler_from_config(config: Dict[str, Any]) -> SchedulerService:
    """Initialise the global SchedulerService from a config dict. Idempotent."""
    global _SCHEDULER
    if _SCHEDULER is None:
        _SCHEDULER = SchedulerService.from_config(config)
        logger.info("SchedulerService initialised (degraded=%s).", _SCHEDULER._degraded)
    return _SCHEDULER


def get_scheduler() -> SchedulerService:
    """Return the global SchedulerService.

    Raises RuntimeError if not yet initialised.
    """
    if _SCHEDULER is None:
        raise RuntimeError(
            "SchedulerService not initialised — call init_scheduler_from_config() first."
        )
    return _SCHEDULER
