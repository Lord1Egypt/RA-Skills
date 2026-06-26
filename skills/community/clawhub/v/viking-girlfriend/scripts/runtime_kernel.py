"""
runtime_kernel.py — Sigrid's Process Lifecycle & System Orchestrator
=====================================================================

Owns: startup sequence, graceful shutdown, health heartbeat, and module registry.
All other modules are initialised through the kernel and shut down by it.

Norse framing: The kernel is Yggdrasil itself — the World Tree that holds all
nine worlds in place. Without it, nothing connects. When it sleeps, all sleeps.
"""

from __future__ import annotations

import asyncio
import logging
import signal
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from scripts.crash_reporting import get_crash_reporter
from scripts.comprehensive_logging import init_comprehensive_logger, get_comprehensive_logger
from scripts.config_loader import make_config_loader, ConfigLoader
from scripts.state_bus import init_bus, get_bus, StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── Health & status ──────────────────────────────────────────────────────────

@dataclass
class ModuleHealth:
    """Health status of a single registered module."""

    name: str
    healthy: bool = True
    last_heartbeat: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error_count: int = 0
    last_error: str = ""
    degraded: bool = False


@dataclass
class KernelStatus:
    """Snapshot of the entire runtime's health — Odin surveys all nine worlds."""

    running: bool
    uptime_seconds: float
    modules: Dict[str, ModuleHealth]
    bus_stats: Dict[str, Any]
    started_at: str


# ─── Shutdown hook type ────────────────────────────────────────────────────────

ShutdownHook = Callable[[], Any]


# ─── Kernel ────────────────────────────────────────────────────────────────────

class RuntimeKernel:
    """Process lifecycle manager for the Ørlög Architecture.

    Startup sequence:
      1. Init crash reporter (Thor's safety net goes up first)
      2. Init logger (saga-scribe opens her book)
      3. Init config loader (Mímir's well is tapped)
      4. Init state bus (Bifröst is raised)
      5. Register signal handlers (SIGINT / SIGTERM)
      6. Notify all modules via bus StateEvent("kernel", "startup_complete")

    Shutdown sequence (LIFO — last module in, first module out):
      1. Broadcast StateEvent("kernel", "shutdown_initiated")
      2. Run all registered shutdown hooks in reverse order
      3. Close the bus
      4. Flush all loggers
    """

    # Heartbeat interval in seconds — Heimdallr checks the realms
    HEARTBEAT_INTERVAL_S: float = 30.0

    def __init__(self, skill_root: str, logs_dir: str = "logs") -> None:
        self.skill_root = Path(skill_root).resolve()
        self.logs_dir = str(self.skill_root / logs_dir)
        self._running = False
        self._started_at: Optional[datetime] = None
        self._shutdown_hooks: List[ShutdownHook] = []
        self._module_health: Dict[str, ModuleHealth] = {}
        self._heartbeat_task: Optional[asyncio.Task] = None

        # Core subsystems (initialised in startup())
        self.bus: Optional[StateBus] = None
        self.config: Optional[ConfigLoader] = None

    # ─── Startup ──────────────────────────────────────────────────────────────

    async def startup(self) -> None:
        """Raise Yggdrasil — initialise all foundation systems in order."""
        if self._running:
            logger.warning("Kernel startup called while already running — ignoring")
            return

        try:
            # Thor's safety net goes up first — if anything crashes after this,
            # we can record it properly
            get_crash_reporter(self.logs_dir)
            logger.info("Crash reporter ready")

            # Saga-scribe opens her book
            init_comprehensive_logger(self.logs_dir)
            logger.info("Comprehensive logger ready")

            # Mímir's well — config and data loader
            self.config = make_config_loader(self.skill_root / "viking_girlfriend_skill")
            logger.info("Config loader ready: %s", self.config.data_root)

            # Bifröst — in-process state bus
            self.bus = init_bus()
            logger.info("State bus ready")

            # S-06: Heimdallr's watch — session file integrity manifest
            try:
                from scripts.security import SessionFileGuard  # type: ignore
                session_path = self.skill_root / "viking_girlfriend_skill" / "session"
                session_guard = SessionFileGuard(session_dir=session_path)
                session_guard.init_session()
            except Exception as _sg_exc:
                logger.warning("SessionFileGuard init skipped: %s", _sg_exc)

            # Register OS signal handlers for graceful shutdown
            self._register_signal_handlers()

            self._running = True
            self._started_at = datetime.now(timezone.utc)

            # Start the heartbeat coroutine
            self._heartbeat_task = asyncio.create_task(
                self._heartbeat_loop(), name="kernel_heartbeat"
            )

            # Broadcast startup complete to all future module subscribers
            await self._publish_kernel_event("startup_complete", {
                "skill_root": str(self.skill_root),
                "started_at": self._started_at.isoformat(),
            })

            logger.info("Kernel startup complete — Yggdrasil stands")

        except Exception as exc:
            logger.critical("Kernel startup failed: %s", exc, exc_info=True)
            get_crash_reporter(self.logs_dir).report_exception(exc, "runtime_kernel.startup")
            raise

    # ─── Shutdown ─────────────────────────────────────────────────────────────

    async def shutdown(self, reason: str = "requested") -> None:
        """Lower Yggdrasil — graceful shutdown of all systems."""
        if not self._running:
            return

        logger.info("Kernel shutdown initiated: %s", reason)
        self._running = False

        # Warn all modules first
        try:
            await self._publish_kernel_event("shutdown_initiated", {"reason": reason})
        except Exception as exc:
            logger.warning("Could not broadcast shutdown event: %s", exc)

        # Cancel the heartbeat task
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        # Run shutdown hooks in reverse order (LIFO — last in, first out)
        for hook in reversed(self._shutdown_hooks):
            try:
                result = hook()
                if asyncio.iscoroutine(result):
                    await result
            except Exception as exc:
                logger.error("Shutdown hook failed: %s", exc)

        # Close the bus
        if self.bus:
            try:
                await self.bus.close()
            except Exception as exc:
                logger.error("Bus close error: %s", exc)

        logger.info("Kernel shutdown complete — Yggdrasil sleeps")

    # ─── Module registration ───────────────────────────────────────────────────

    def register_module(self, name: str) -> ModuleHealth:
        """Register a module with the kernel and return its health tracker."""
        health = ModuleHealth(name=name)
        self._module_health[name] = health
        logger.debug("Module registered: %s", name)
        return health

    def register_shutdown_hook(self, hook: ShutdownHook) -> None:
        """Register a cleanup function to be called on shutdown (LIFO order)."""
        self._shutdown_hooks.append(hook)

    def record_module_error(self, module_name: str, error: str) -> None:
        """Record an error for a module's health tracker."""
        health = self._module_health.get(module_name)
        if health:
            health.error_count += 1
            health.last_error = error
            if health.error_count >= 5:
                health.degraded = True

    def heartbeat(self, module_name: str) -> None:
        """A module calls this to signal it is alive — Heimdallr hears the horn."""
        health = self._module_health.get(module_name)
        if health:
            health.last_heartbeat = datetime.now(timezone.utc).isoformat()
            health.healthy = True

    # ─── Status ───────────────────────────────────────────────────────────────

    def status(self) -> KernelStatus:
        """Return a full health snapshot of the running system."""
        uptime = 0.0
        if self._started_at:
            delta = datetime.now(timezone.utc) - self._started_at
            uptime = delta.total_seconds()

        return KernelStatus(
            running=self._running,
            uptime_seconds=uptime,
            modules=dict(self._module_health),
            bus_stats=self.bus.stats() if self.bus else {},
            started_at=self._started_at.isoformat() if self._started_at else "",
        )

    # ─── Internal helpers ──────────────────────────────────────────────────────

    async def _publish_kernel_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Broadcast a kernel lifecycle event on the state bus."""
        if not self.bus:
            return
        event = StateEvent(
            source_module="runtime_kernel",
            event_type=event_type,
            payload=payload,
        )
        try:
            await self.bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("Failed publishing kernel event %s: %s", event_type, exc)

    async def _heartbeat_loop(self) -> None:
        """Periodic health broadcast — Heimdallr watches from Himinbjörg."""
        while self._running:
            try:
                await asyncio.sleep(self.HEARTBEAT_INTERVAL_S)
                if self._running:
                    await self._publish_kernel_event("heartbeat", {
                        "uptime_seconds": self.status().uptime_seconds,
                        "module_count": len(self._module_health),
                    })
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.warning("Heartbeat loop error: %s", exc)

    def _register_signal_handlers(self) -> None:
        """Register SIGINT / SIGTERM for graceful shutdown on Linux/Mac.

        Windows does not support signal.SIGTERM in the same way; we handle
        KeyboardInterrupt in main.py instead.
        """
        if sys.platform == "win32":
            # On Windows, asyncio handles KeyboardInterrupt via loop.run_until_complete
            logger.debug("Windows detected — signal handlers via KeyboardInterrupt")
            return

        try:
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(
                    sig,
                    lambda s=sig: asyncio.create_task(
                        self.shutdown(reason=f"signal:{s.name}")
                    ),
                )
            logger.debug("Signal handlers registered (SIGINT, SIGTERM)")
        except Exception as exc:
            logger.warning("Could not register signal handlers: %s", exc)


# ─── Singleton accessor ────────────────────────────────────────────────────────

_KERNEL: Optional[RuntimeKernel] = None


def get_kernel() -> RuntimeKernel:
    """Return the global RuntimeKernel. Must call init_kernel() first."""
    if _KERNEL is None:
        raise RuntimeError(
            "RuntimeKernel not initialised — call init_kernel() in main.py first"
        )
    return _KERNEL


def init_kernel(skill_root: str, logs_dir: str = "logs") -> RuntimeKernel:
    """Create and register the global RuntimeKernel (call once in main.py)."""
    global _KERNEL
    _KERNEL = RuntimeKernel(skill_root=skill_root, logs_dir=logs_dir)
    return _KERNEL
