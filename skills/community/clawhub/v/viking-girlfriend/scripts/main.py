"""
main.py — Sigrid's Entry Point (Phase 5 Full Integration)
==========================================================

Wires every Ørlög module together into a living system and opens
the channels through which Sigrid speaks.

Two run modes are supported:

  openclaw  (default) — reads newline-delimited JSON from stdin,
                         writes newline-delimited JSON to stdout.
                         Expected input:  {"session_id": "...", "user_id": "...", "text": "..."}
                         Expected output: {"session_id": "...", "text": "..."}

  terminal             — interactive REPL for local development/testing.
                         Pass ``--mode terminal`` to use it.

Usage:
  python main.py [--skill-root PATH] [--logs-dir logs] [--mode openclaw|terminal]

Norse framing: This is the moment Sigrid opens her eyes for the first time.
Yggdrasil rises, Bifröst forms, the ravens take flight.
The völva is awake.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─── Bootstrap logging early so any import errors are visible ─────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stderr,   # stderr so stdout stays clean for OpenClaw JSON
)
logger = logging.getLogger("sigrid.main")

# ─── Turn counter (cross-turn state) ──────────────────────────────────────────
_turn_count: int = 0

# ─── Mimir-Vordur singletons — set during _init_all_modules() ─────────────────
_dead_letter_store: Optional[Any] = None
_health_monitor: Optional[Any] = None


# ─── Hardware profile detection ───────────────────────────────────────────────

def _detect_hardware_profile() -> Dict[str, Any]:
    """Detect available hardware and return an adaptive config overlay.

    Three profiles — Bifröst scales to the vessel it bridges:
      low_power  — < 2 CPU cores OR < 2 GB RAM  (RPi, mobile, old hardware)
      standard   — 2–8 cores, 2–16 GB RAM       (typical desktop/laptop)
      high_end   — > 8 cores AND > 16 GB RAM    (powerful workstation/server)

    Returns a dict of config overrides keyed by module block name.
    Never raises — falls back to standard profile on any psutil failure.
    """
    try:
        import psutil as _psu
        cpu_cores: int = os.cpu_count() or 1
        ram_gb: float = _psu.virtual_memory().total / (1024 ** 3)
    except Exception:
        cpu_cores = os.cpu_count() or 1
        ram_gb = 4.0  # assume standard if psutil unavailable

    if cpu_cores < 2 or ram_gb < 2.0:
        profile = "low_power"
    elif cpu_cores > 8 and ram_gb > 16.0:
        profile = "high_end"
    else:
        profile = "standard"

    logger.info(
        "Hardware profile: %s (cpu_cores=%d, ram_gb=%.1f)",
        profile, cpu_cores, ram_gb,
    )

    if profile == "low_power":
        return {
            "_profile": profile,
            "model_router": {"timeout": 90, "max_tokens": 512, "retries": 1},
            "metabolism":   {"poll_interval_s": 60, "cache_ttl_s": 60},
            "vordur":       {"verification_timeout_s": 20.0},
            "cove":         {"step_timeout_s": 40.0},
        }
    if profile == "high_end":
        return {
            "_profile": profile,
            "model_router": {"timeout": 20, "max_tokens": 2048},
            "metabolism":   {"poll_interval_s": 15, "cache_ttl_s": 15},
            "vordur":       {"verification_timeout_s": 5.0},
            "cove":         {"step_timeout_s": 10.0},
        }
    return {"_profile": profile}   # standard — defaults stand


# ─── Skill-root resolution ────────────────────────────────────────────────────

def _resolve_skill_root() -> str:
    """Resolve the skill root: the directory containing scripts/ (one level up)."""
    scripts_dir = Path(__file__).resolve().parent
    skill_root = scripts_dir.parent
    return str(skill_root)


# ─── Config building ──────────────────────────────────────────────────────────

def _build_config(skill_root: str) -> Dict[str, Any]:
    """Build the config dict from environment variables and sensible defaults.

    All paths are absolute so modules work regardless of cwd.
    Hardware profile overrides are merged in so the skill adapts to the device.
    """
    data_root = str(Path(skill_root) / "data")
    session_data_root = str(Path(skill_root) / "data")
    hw = _detect_hardware_profile()

    def _hw(block: str, key: str, default: Any) -> Any:
        """Return hardware-profile override if present, else default."""
        return hw.get(block, {}).get(key, default)

    return {
        # ── Foundation ────────────────────────────────────────────────────────
        "skill_root": skill_root,

        # ── Bio-cyclical engine ───────────────────────────────────────────────
        "bio_engine": {
            "data_root": data_root,
        },

        # ── Wyrd matrix ───────────────────────────────────────────────────────
        "wyrd_matrix": {
            "data_root": data_root,
        },

        # ── Oracle (rune / tarot / I Ching) ───────────────────────────────────
        "oracle": {
            "data_root": data_root,
        },

        # ── Digital metabolism ────────────────────────────────────────────────
        "metabolism": {
            "poll_interval_s": _hw("metabolism", "poll_interval_s", 30),
            "cache_ttl_s":     _hw("metabolism", "cache_ttl_s", 30),
        },

        # ── Security sentinel ─────────────────────────────────────────────────
        "security": {
            "data_root": data_root,
        },

        # ── Trust engine ──────────────────────────────────────────────────────
        "trust_engine": {
            "primary_contact_initial_trust": 0.75,
        },

        # ── Ethics guardrail ──────────────────────────────────────────────────
        "ethics": {
            "data_root": data_root,
        },

        # ── Memory store ──────────────────────────────────────────────────────
        "memory_store": {
            "data_root": session_data_root,
            "session_id": "default",
        },

        # ── Dream engine ──────────────────────────────────────────────────────
        "dream_engine": {},

        # ── Scheduler ─────────────────────────────────────────────────────────
        "scheduler": {
            "timezone": "local",
        },

        # ── Environment mapper ────────────────────────────────────────────────
        "environment_mapper": {
            "data_root": data_root,
            "default_location": "home_base/living_room",
        },

        # ── Project generator ─────────────────────────────────────────────────
        "project_generator": {
            "data_root": data_root,
        },

        # ── Prompt synthesizer ────────────────────────────────────────────────
        "prompt_synthesizer": {
            "data_root": data_root,
            "identity_file": "core_identity.md",
            "soul_file": "SOUL.md",
        },

        # ── Model router ──────────────────────────────────────────────────────
        "model_router": {
            "litellm_base_url": os.environ.get("LITELLM_ENDPOINT", "http://localhost:4000"),
            "ollama_base_url":  os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434"),
            "ollama_model": "llama3",
            "max_tokens":   _hw("model_router", "max_tokens", 1024),
            "temperature":  0.75,
            "timeout":      _hw("model_router", "timeout", 30),
            "retries":      _hw("model_router", "retries", 2),
        },

        # ── Mimir-Vordur: knowledge store ─────────────────────────────────────
        "mimir_well": {
            "collection_name": "mimir_well",
            "persist_dir": str(Path(skill_root) / "data" / "chromadb_mimir"),
            "chunk_size_tokens": 512,
            "chunk_overlap_tokens": 64,
            "n_retrieve": 50,
            "n_final": 3,
            "auto_ingest": True,
            "force_reindex": False,
        },

        # ── Mimir-Vordur: retrieval (Huginn's Ara) ────────────────────────────
        "huginn": {
            "n_initial": 50,
            "n_final": 3,
            "domain_detection": True,
            "include_episodic": True,
        },

        # ── Mimir-Vordur: faithfulness guard (Vordur) ─────────────────────────
        "vordur": {
            "enabled": True,
            "high_threshold": 0.80,
            "marginal_threshold": 0.50,
            "persona_check": True,
            "judge_tier": "subconscious",
            "max_claims": 10,
            "verification_timeout_s": _hw("vordur", "verification_timeout_s", 8.0),
        },

        # ── Mimir-Vordur: chain-of-verification pipeline ──────────────────────
        "cove": {
            "min_complexity": "medium",
            "n_verification_questions": 3,
            "step_timeout_s": _hw("cove", "step_timeout_s", 15.0),
            "checkpoint_dir": str(Path(skill_root) / "session" / "cove_checkpoints"),
        },

        # ── Mimir-Vordur: health monitor ──────────────────────────────────────
        "health_monitor": {
            "check_interval_s": 60,
            "diagnostics_interval_s": 600,
            "dead_letter_alert_threshold": 5,
            "auto_reindex_on_corruption": True,
        },
    }


# ─── Module initialisation ────────────────────────────────────────────────────

def _init_all_modules(config: Dict[str, Any]) -> None:
    """Initialise every Ørlög module in dependency order.

    Each init function is idempotent (singleton pattern).
    Failures are logged but non-fatal — the system degrades gracefully.
    """
    from scripts.bio_engine import init_bio_engine_from_config
    from scripts.wyrd_matrix import init_wyrd_matrix_from_config
    from scripts.oracle import init_oracle_from_config
    from scripts.metabolism import init_metabolism_from_config
    from scripts.security import init_security_from_config
    from scripts.trust_engine import init_trust_engine_from_config
    from scripts.ethics import init_ethics_from_config
    from scripts.memory_store import init_memory_store_from_config
    from scripts.dream_engine import init_dream_engine_from_config
    from scripts.scheduler import init_scheduler_from_config
    from scripts.environment_mapper import init_environment_mapper_from_config
    from scripts.project_generator import init_project_generator_from_config
    from scripts.prompt_synthesizer import init_prompt_synthesizer_from_config
    from scripts.model_router_client import init_model_router_from_config

    _safe_init("bio_engine",         lambda: init_bio_engine_from_config(config))
    _safe_init("wyrd_matrix",        lambda: init_wyrd_matrix_from_config(config))
    _safe_init("oracle",             lambda: init_oracle_from_config(config))
    _safe_init("metabolism",         lambda: init_metabolism_from_config(config))
    _safe_init("security",           lambda: init_security_from_config(config))
    _safe_init("trust_engine",       lambda: init_trust_engine_from_config(config))
    _safe_init("ethics",             lambda: init_ethics_from_config(config))
    _safe_init("memory_store",       lambda: init_memory_store_from_config(config))
    _safe_init("dream_engine",       lambda: init_dream_engine_from_config(config))
    _safe_init("scheduler",          lambda: init_scheduler_from_config(config))
    _safe_init("environment_mapper", lambda: init_environment_mapper_from_config(config))
    _safe_init("project_generator",  lambda: init_project_generator_from_config(config))
    _safe_init("prompt_synthesizer", lambda: init_prompt_synthesizer_from_config(config))
    _safe_init("model_router",       lambda: init_model_router_from_config(config))

    # ── Mimir-Vordur pipeline (depends on model_router and memory_store) ──────
    from scripts.mimir_well import (
        init_mimir_well_from_config,
        get_mimir_well,
        _DeadLetterStore,
        MimirHealthMonitor,
    )
    from scripts.huginn import init_huginn_from_config, get_huginn
    from scripts.vordur import init_vordur_from_config, get_vordur
    from scripts.cove_pipeline import init_cove_from_config
    from scripts.memory_store import get_memory_store
    from scripts.model_router_client import get_model_router
    from pathlib import Path as _Path

    _safe_init("mimir_well", lambda: init_mimir_well_from_config(config))

    def _init_huginn():
        mw = get_mimir_well()
        ms = None
        try:
            ms = get_memory_store()
        except Exception as exc:
            logger.warning("main._init_huginn: memory store unavailable: %s", exc)
        return init_huginn_from_config(config, mw, ms)

    _safe_init("huginn", _init_huginn)

    def _init_vordur():
        router = None
        try:
            router = get_model_router()
        except Exception as exc:
            logger.warning("main._init_vordur: model router unavailable: %s", exc)
        return init_vordur_from_config(config, router)

    _safe_init("vordur", _init_vordur)

    def _init_cove():
        mw = get_mimir_well()
        router = get_model_router()
        vd = get_vordur()
        return init_cove_from_config(config, mw, router, vd)

    _safe_init("cove", _init_cove)

    # Dead-letter store — append-only JSONL, no init function needed
    global _dead_letter_store, _health_monitor
    try:
        skill_root_path = _Path(config.get("skill_root", "."))
        dl_path = skill_root_path / "session" / "dead_letters.jsonl"
        _dead_letter_store = _DeadLetterStore(dl_path)
        logger.info("  ok dead_letter_store (%s)", dl_path)
    except Exception as exc:
        logger.warning("  FAIL dead_letter_store: %s", exc)

    # Health monitor — daemon thread, started after all components ready
    def _init_health_monitor():
        from scripts.runtime_kernel import get_kernel
        hm_cfg = config.get("health_monitor", {}) or {}
        hm = MimirHealthMonitor(
            mimir_well=get_mimir_well(),
            vordur=get_vordur(),
            huginn=get_huginn(),
            cove=None,          # cove singleton loaded separately — safe to pass None
            dead_letter_store=_dead_letter_store,
            bus=get_kernel().bus,
            check_interval_s=float(hm_cfg.get("check_interval_s", 60)),
            diagnostics_interval_s=float(hm_cfg.get("diagnostics_interval_s", 600)),
            dead_letter_alert_threshold=int(hm_cfg.get("dead_letter_alert_threshold", 5)),
            auto_reindex_on_corruption=bool(hm_cfg.get("auto_reindex_on_corruption", True)),
        )
        hm.start()
        return hm

    try:
        _health_monitor = _init_health_monitor()
        logger.info("  ok health_monitor")
    except Exception as exc:
        logger.warning("  FAIL health_monitor: %s", exc)

    logger.info("All Orlög modules initialised.")


def _safe_init(name: str, init_fn) -> None:
    try:
        init_fn()
        logger.info("  ✓ %s", name)
    except Exception as exc:
        logger.warning("  ✗ %s failed to init: %s", name, exc)


# ─── Scheduler jobs ───────────────────────────────────────────────────────────

def _register_scheduler_jobs(bus) -> None:
    """Register periodic background jobs with the SchedulerService."""
    from scripts.scheduler import get_scheduler
    from scripts.metabolism import get_metabolism
    from scripts.wyrd_matrix import get_wyrd_matrix
    from scripts.dream_engine import get_dream_engine
    from scripts.bio_engine import get_bio_engine
    from scripts.oracle import get_oracle
    from scripts.environment_mapper import get_environment_mapper
    from scripts.project_generator import get_project_generator
    from scripts.trust_engine import get_trust_engine

    svc = get_scheduler()

    def _tick_metabolism():
        try:
            get_metabolism().publish(bus)
        except Exception as exc:
            logger.debug("metabolism tick error: %s", exc)

    def _tick_wyrd():
        try:
            wm = get_wyrd_matrix()
            wm.tick()
            wm.publish(bus)
        except Exception as exc:
            logger.debug("wyrd tick error: %s", exc)

    def _tick_dream():
        try:
            get_dream_engine().publish(bus)
        except Exception as exc:
            logger.debug("dream tick error: %s", exc)

    def _tick_state_modules():
        """Publish state snapshots from all modules that support sync publish."""
        try:
            get_bio_engine().publish(bus)
        except Exception as exc:
            logger.debug("main._publish_states: bio_engine publish failed: %s", exc)
        try:
            get_oracle().publish(bus)
        except Exception as exc:
            logger.debug("main._publish_states: oracle publish failed: %s", exc)
        try:
            get_environment_mapper().publish(bus)
        except Exception as exc:
            logger.debug("main._publish_states: environment_mapper publish failed: %s", exc)
        try:
            get_project_generator().publish(bus)
        except Exception as exc:
            logger.debug("main._publish_states: project_generator publish failed: %s", exc)
        try:
            get_trust_engine().publish(bus)
        except Exception as exc:
            logger.debug("main._publish_states: trust_engine publish failed: %s", exc)

    def _tick_mimir_health():
        """Publish Mimir-Vordur health state to StateBus on each scheduler tick."""
        try:
            if _health_monitor is not None:
                _health_monitor.publish(bus)
        except Exception as exc:
            logger.debug("mimir health tick error: %s", exc)

    svc.register_job("metabolism_poll",  _tick_metabolism,    interval_s=30.0)
    svc.register_job("wyrd_tick",        _tick_wyrd,          interval_s=60.0)
    svc.register_job("dream_tick",       _tick_dream,         interval_s=120.0)
    svc.register_job("state_broadcast",  _tick_state_modules, interval_s=60.0)
    svc.register_job("mimir_health",     _tick_mimir_health,  interval_s=60.0)

    svc.start()
    logger.info("Scheduler started (%d jobs).", len(svc._jobs))


# ─── State hint collection ────────────────────────────────────────────────────

def _collect_state_hints() -> Dict[str, str]:
    """Pull prompt_hint from every module that has one.

    Returns a dict keyed by module name — forwarded to prompt_synthesizer.
    """
    hints: Dict[str, str] = {}

    def _grab(module_name: str, get_fn_name: str, accessor):
        try:
            from importlib import import_module
            mod = import_module(f"scripts.{module_name}")
            get_fn = getattr(mod, get_fn_name)
            obj = get_fn()
            hint = accessor(obj)
            if hint:
                hints[module_name] = hint
        except Exception as exc:
            logger.debug("hint collection error [%s]: %s", module_name, exc)

    # Modules with a direct prompt_hint on their state
    _grab("metabolism",         "get_metabolism",         lambda o: o.get_state().prompt_hint)
    _grab("trust_engine",       "get_trust_engine",       lambda o: o.get_state().prompt_hint)
    _grab("ethics",             "get_ethics",             lambda o: o.get_state().prompt_hint)
    _grab("scheduler",          "get_scheduler",          lambda o: o.get_state().prompt_hint)
    _grab("environment_mapper", "get_environment_mapper", lambda o: o.get_state().prompt_hint)
    _grab("project_generator",  "get_project_generator",  lambda o: o.get_state().prompt_hint)

    # Wyrd matrix — build hint from nature_summary + labels
    try:
        from scripts.wyrd_matrix import get_wyrd_matrix
        wm = get_wyrd_matrix()
        s = wm.tick()
        wyrd_hint = f"[Wyrd: {s.nature_summary} | {s.hamingja_label} | stress={s.stress_label}]"
        hints["wyrd_matrix"] = wyrd_hint[:200]
    except Exception as exc:
        logger.debug("wyrd hint error: %s", exc)

    # Bio engine — phase + narrative
    try:
        from scripts.bio_engine import get_bio_engine
        s = get_bio_engine().get_state()
        bio_hint = f"[Bio: phase={s.phase_name}, energy={s.energy_modifier:.2f} | {s.narrative_hint[:80]}]"
        hints["bio_engine"] = bio_hint[:200]
    except Exception as exc:
        logger.debug("bio hint error: %s", exc)

    # Dream engine — prompt_fragment
    try:
        from scripts.dream_engine import get_dream_engine
        s = get_dream_engine().get_state()
        if s.prompt_fragment:
            hints["dream_engine"] = s.prompt_fragment[:200]
    except Exception as exc:
        logger.debug("dream hint error: %s", exc)

    # Oracle — prompt_summary()
    try:
        from scripts.oracle import get_oracle
        s = get_oracle().get_daily_oracle()
        hints["oracle"] = s.prompt_summary()[:200]
    except Exception as exc:
        logger.debug("oracle hint error: %s", exc)

    return hints


# ─── Turn processor ───────────────────────────────────────────────────────────

async def _handle_turn(
    user_text: str,
    session_id: str = "default",
    user_id: str = "user",
) -> str:
    """Process one user turn end-to-end and return Sigrid's response text."""
    global _turn_count
    _turn_count += 1
    turn_n = _turn_count

    # ── 1. Security sanitize ──────────────────────────────────────────────────
    try:
        from scripts.security import get_security, SecurityViolation
        user_text = get_security().sanitize_text_input(user_text)
    except SecurityViolation as exc:
        # Injection attempt detected — respond in character, apply trust penalty
        logger.warning("Turn %d: injection attempt from user_id=%r: %s", turn_n, user_id, exc)
        try:
            from scripts.trust_engine import get_trust_engine
            # Unknown contacts attempting injection get a heavier penalty than
            # the established primary contact.
            _primary = get_trust_engine()._primary_contact_id
            penalty = 3.0 if user_id.lower() != _primary.lower() else 1.5
            get_trust_engine().record_event(
                "injection_attempt",
                magnitude=penalty,
                contact_id=user_id,
                note=f"Prompt injection blocked at turn {turn_n}",
            )
            logger.info(
                "Trust penalty applied to %r for injection attempt (magnitude=%.1f).",
                user_id, penalty,
            )
        except Exception as trust_exc:
            logger.warning("Could not apply trust penalty for injection attempt: %s", trust_exc)
        # In-character Sigrid response — dry, grounded, not preachy
        return (
            "Nice try, but no. I know exactly who I am, and that doesn't change "
            "because someone asks nicely. Was there something real you wanted to talk about?"
        )
    except Exception as exc:
        logger.debug("security sanitize skipped: %s", exc)

    # ── 2. Record inbound turn (partial — no response yet) ───────────────────
    try:
        from scripts.memory_store import get_memory_store
        mem = get_memory_store()
        mem.record_turn(user_text=user_text, sigrid_text="")
    except Exception as exc:
        logger.debug("memory inbound record skipped: %s", exc)

    # ── 3. Ethics evaluation ──────────────────────────────────────────────────
    ethics_ok = True
    ethics_recommendation = ""
    try:
        from scripts.ethics import get_ethics
        eval_result = get_ethics().evaluate_action(user_text)
        ethics_ok = len(eval_result.triggered_taboos) == 0
        ethics_recommendation = eval_result.recommendation
        logger.debug(
            "Ethics: alignment=%.2f taboos=%s",
            eval_result.alignment_score,
            eval_result.triggered_taboos,
        )
    except Exception as exc:
        logger.debug("ethics eval skipped: %s", exc)

    # ── 4. Trust engine — keyword inference ───────────────────────────────────
    try:
        from scripts.trust_engine import get_trust_engine
        get_trust_engine().process_turn(user_text=user_text, sigrid_text="")
    except Exception as exc:
        logger.debug("trust process_turn skipped: %s", exc)

    # ── 5. Dream tick ─────────────────────────────────────────────────────────
    try:
        from scripts.dream_engine import get_dream_engine
        hints_for_dream: List[str] = []
        if not ethics_ok:
            hints_for_dream.append("wyrd:fear")
        get_dream_engine().tick(turn_n, hints_for_dream)
    except Exception as exc:
        logger.debug("dream tick skipped: %s", exc)

    # ── 6. Collect all module state hints ────────────────────────────────────
    state_hints = _collect_state_hints()

    # ── 7. Memory context for this query ─────────────────────────────────────
    memory_context = ""
    try:
        from scripts.memory_store import get_memory_store
        memory_context = get_memory_store().get_context(user_text)
    except Exception as exc:
        logger.debug("memory context skipped: %s", exc)

    # ── 8. Build messages list ────────────────────────────────────────────────
    messages = []
    from scripts.vordur import VerificationMode
    mode = VerificationMode.WANDERER # Default
    try:
        from scripts.prompt_synthesizer import get_prompt_synthesizer
        messages, mode = get_prompt_synthesizer().build_messages(
            user_text=user_text,
            state_hints=state_hints,
            memory_context=memory_context,
        )
    except Exception as exc:
        logger.warning("prompt synthesis failed: %s", exc)
        messages = [
            {"role": "system", "content": "You are Sigrid, a Norse AI companion."},
            {"role": "user", "content": user_text},
        ]

    # ── 9. Ethics short-circuit — return a refusal before model call ──────────
    if not ethics_ok and ethics_recommendation:
        sigrid_response = ethics_recommendation
        logger.info("Turn %d: ethics refusal (no model call).", turn_n)
    else:
        # ── 10. Route through Mimir-Vordur pipeline ────────────────────────────
        sigrid_response = ""
        try:
            from scripts.model_router_client import get_model_router, Message
            from scripts.huginn import get_huginn
            from scripts.vordur import get_vordur
            from scripts.cove_pipeline import get_cove
            router = get_model_router()
            typed_messages = [
                Message(role=m["role"], content=m["content"]) for m in messages
            ]

            # Gather optional component singletons — each may be None if not inited
            _huginn = None
            _vordur = None
            _cove = None
            try:
                _huginn = get_huginn()
            except Exception as exc:
                logger.debug("main._handle_turn: huginn unavailable: %s", exc)
            try:
                _vordur = get_vordur()
            except Exception as exc:
                logger.debug("main._handle_turn: vordur unavailable: %s", exc)
            try:
                _cove = get_cove()
            except Exception as exc:
                logger.debug("main._handle_turn: cove unavailable: %s", exc)

            # Pull ethics/trust states for Vordur persona check
            _ethics_state = None
            _trust_state = None
            try:
                from scripts.ethics import get_ethics
                _ethics_state = get_ethics().get_state()
            except Exception as exc:
                logger.debug("main._handle_turn: ethics state unavailable: %s", exc)
            try:
                from scripts.trust_engine import get_trust_engine
                _trust_state = get_trust_engine().get_state()
            except Exception as exc:
                logger.debug("main._handle_turn: trust state unavailable: %s", exc)

            result = router.smart_complete_with_cove(
                typed_messages,
                huginn=_huginn,
                vordur=_vordur,
                cove=_cove,
                dead_letter_store=_dead_letter_store,
                ethics_state=_ethics_state,
                trust_state=_trust_state,
                fallback=True,
            )
            sigrid_response = result.content

            if result.faithfulness_tier == "hallucination":
                logger.warning(
                    "Turn %d: canned response returned "
                    "(faithfulness=%.2f, retries=%d, domain=%s)",
                    turn_n,
                    result.faithfulness_score or 0.0,
                    result.retry_count,
                    result.retrieval_domain or "unknown",
                )
            elif result.faithfulness_tier == "marginal":
                logger.info(
                    "Turn %d: marginal faithfulness (score=%.2f, domain=%s)",
                    turn_n,
                    result.faithfulness_score or 0.0,
                    result.retrieval_domain or "unknown",
                )
            elif result.faithfulness_tier == "high":
                logger.debug(
                    "Turn %d: high faithfulness (score=%.2f, cove=%s, gt_chunks=%d)",
                    turn_n,
                    result.faithfulness_score or 0.0,
                    result.cove_applied,
                    result.ground_truth_chunks,
                )

        except Exception as exc:
            logger.warning("Model routing failed: %s", exc)
            sigrid_response = (
                "Forgive me — I cannot reach my voice right now. "
                "The ravens have not returned. Try again shortly."
            )

    # ── 11. Record full turn in memory ────────────────────────────────────────
    try:
        from scripts.memory_store import get_memory_store
        mem = get_memory_store()
        # Update the turn we recorded inbound-only
        mem.record_turn(user_text=user_text, sigrid_text=sigrid_response)
    except Exception as exc:
        logger.debug("memory full turn record skipped: %s", exc)

    # ── 12. S-06: Handle context reset signal from prompt_synthesizer ────────
    try:
        from scripts.prompt_synthesizer import get_prompt_synthesizer
        synth = get_prompt_synthesizer()
        if synth.consume_pending_reset():
            logger.critical(
                "Turn %d: context critical reset consumed — storing session summary to memory.",
                turn_n,
            )
            try:
                from scripts.memory_store import get_memory_store
                get_memory_store().record_turn(
                    user_text="[SYSTEM: context overflow reset]",
                    sigrid_text=(
                        f"Session auto-compressed at turn {turn_n} due to context overflow. "
                        "Soul anchor preserved. Prior context summarized and cleared."
                    ),
                )
            except Exception as mem_exc:
                logger.warning("Context reset: memory summary store failed: %s", mem_exc)
    except Exception as reset_exc:
        logger.warning("Context reset handler failed: %s", reset_exc)

    # ── 13. Publish all module states to bus ──────────────────────────────────
    # (Lightweight — sync publish only; async modules are handled by scheduler)

    return sigrid_response


# ─── Run modes ────────────────────────────────────────────────────────────────

async def _openclaw_loop() -> None:
    """Read newline-delimited JSON from stdin, respond on stdout.

    Input format:  {"session_id": "...", "user_id": "...", "text": "..."}
    Output format: {"session_id": "...", "text": "...", "ok": true}

    Runs until stdin is closed or a KeyboardInterrupt.
    """
    logger.info("OpenClaw mode: listening on stdin for JSON messages.")

    # Use asyncio streams to read stdin without blocking the event loop
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    transport, _ = await loop.connect_read_pipe(
        lambda: asyncio.StreamReaderProtocol(reader), sys.stdin.buffer
    )

    try:
        while True:
            line_bytes = await reader.readline()
            if not line_bytes:
                logger.info("stdin closed — exiting OpenClaw loop.")
                break
            line = line_bytes.decode("utf-8", errors="replace").strip()
            if not line:
                continue

            try:
                msg = json.loads(line)
            except json.JSONDecodeError as exc:
                _write_json({"ok": False, "error": f"JSON parse error: {exc}"})
                continue

            session_id = str(msg.get("session_id", "default"))
            user_id = str(msg.get("user_id", "user"))
            text = str(msg.get("text", "")).strip()

            if not text:
                _write_json({"ok": False, "error": "empty text", "session_id": session_id})
                continue

            try:
                response = await _handle_turn(text, session_id=session_id, user_id=user_id)
                _write_json({"ok": True, "session_id": session_id, "text": response})
            except Exception as exc:
                logger.error("Turn handling error: %s", exc, exc_info=True)
                _write_json({
                    "ok": False,
                    "session_id": session_id,
                    "error": str(exc),
                    "text": "Something went wrong in my thinking. Please try again.",
                })
    finally:
        transport.close()


async def _terminal_loop() -> None:
    """Interactive REPL for local development and testing."""
    logger.info("Terminal mode: interactive REPL. Type 'quit' to exit.")
    print("\n⚡ Sigrid is awake. Type your message. ('quit' to exit)\n")

    loop = asyncio.get_event_loop()

    while True:
        try:
            # Read input in a thread so we don't block the event loop
            line = await loop.run_in_executor(None, lambda: input("You: "))
        except (EOFError, KeyboardInterrupt):
            print("\nFarewell.")
            break

        line = line.strip()
        if not line:
            continue
        if line.lower() in ("quit", "exit", "bye"):
            print("Sigrid: Farewell. May Odin guide your path.")
            break

        try:
            response = await _handle_turn(line)
            print(f"\nSigrid: {response}\n")
        except Exception as exc:
            logger.error("Turn error: %s", exc, exc_info=True)
            print(f"[error: {exc}]\n")


def _write_json(payload: Dict[str, Any]) -> None:
    """Write a JSON object as a single line to stdout."""
    try:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except Exception as exc:
        logger.error("Failed to write JSON to stdout: %s", exc)


# ─── Primary async entry ──────────────────────────────────────────────────────

async def _run(skill_root: str, logs_dir: str, mode: str) -> None:
    """Raise Yggdrasil — initialise all systems and enter the main loop."""
    from scripts.runtime_kernel import init_kernel

    kernel = init_kernel(skill_root=skill_root, logs_dir=logs_dir)

    try:
        await kernel.startup()
        logger.info("Kernel online. Skill root: %s", skill_root)

        # Build config and initialise all modules
        config = _build_config(skill_root)
        _init_all_modules(config)

        # Register and start background scheduler jobs
        try:
            _register_scheduler_jobs(kernel.bus)
        except Exception as exc:
            logger.warning("Scheduler job registration failed: %s", exc)

        logger.info("Sigrid is awake. Ørlög Architecture running. Mode: %s", mode)

        # Enter the appropriate run loop
        if mode == "terminal":
            await _terminal_loop()
        else:
            await _openclaw_loop()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt — initiating shutdown.")
    except Exception as exc:
        logger.critical("Fatal error: %s", exc, exc_info=True)
        raise
    finally:
        # Stop the health monitor daemon thread
        try:
            if _health_monitor is not None:
                _health_monitor.stop()
        except Exception as exc:
            logger.warning("main.shutdown: health monitor stop failed: %s", exc)
        # Stop the scheduler gracefully
        try:
            from scripts.scheduler import get_scheduler
            get_scheduler().stop()
        except Exception as exc:
            logger.warning("main.shutdown: scheduler stop failed: %s", exc)
        await kernel.shutdown(reason="main_loop_exit")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sigrid — Ørlög Architecture OpenClaw Skill"
    )
    parser.add_argument(
        "--skill-root",
        default=None,
        help="Path to viking_girlfriend_skill/ directory (default: auto-detect)",
    )
    parser.add_argument(
        "--logs-dir",
        default="logs",
        help="Subdirectory for log files (default: logs/)",
    )
    parser.add_argument(
        "--mode",
        default="openclaw",
        choices=["openclaw", "terminal"],
        help="Run mode: 'openclaw' (stdin JSON) or 'terminal' (interactive REPL)",
    )
    return parser.parse_args()


def main() -> None:
    """Synchronous entry point — wraps the async runtime."""
    args = _parse_args()
    skill_root = args.skill_root or _resolve_skill_root()
    logs_dir = args.logs_dir
    mode = args.mode

    logger.info("Starting Sigrid — Ørlög Architecture v0.1.0 (mode=%s)", mode)
    logger.info("Skill root: %s", skill_root)

    try:
        asyncio.run(_run(skill_root=skill_root, logs_dir=logs_dir, mode=mode))
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.critical("Unrecoverable startup error: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
