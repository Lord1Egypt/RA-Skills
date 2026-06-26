"""Doctor checks for YouOS system health."""

from __future__ import annotations

import importlib
import importlib.util
import os
import shutil
import socket
import sys
from pathlib import Path

from app.core.settings import get_instance_root, get_models_dir
from app.db.bootstrap import resolve_sqlite_path

ROOT_DIR = Path(__file__).resolve().parents[2]


def _google_backend_status() -> tuple[str, bool, str]:
    """Health of the configured Google ingestion backend's dependency.

    Returns ``(backend, ok, detail)``. Only the ``gog`` backend requires the
    OpenClaw ``gog`` CLI; ``gws`` requires Google's own ``gws`` CLI; ``native``
    requires the ``youos[google]`` libraries. This keeps the doctor (and setup
    wizard) from failing a ``gws``/``native`` user just because ``gog`` — an
    OpenClaw tool they don't use — isn't installed.
    """
    from app.core.config import get_ingestion_google_backend

    backend = get_ingestion_google_backend()
    if backend == "gws":
        if shutil.which("gws") is None:
            return backend, False, "gws CLI not found in PATH (ingestion.google_backend: gws)"
        return backend, True, "gws CLI installed"
    if backend == "native":
        missing = [m for m in ("googleapiclient", "google_auth_oauthlib") if importlib.util.find_spec(m) is None]
        if missing:
            return backend, False, "native backend needs the google extra (pip install youos[google])"
        return backend, True, "Google API libraries importable"
    # gog (default)
    if shutil.which("gog") is None:
        return backend, False, "gog CLI not found in PATH"
    return backend, True, "gog CLI installed"


def run_doctor_checks() -> tuple[bool, list[str]]:
    """Run system health checks.

    Returns (all_required_passed, list_of_failure_messages_for_required_only).
    """
    failures: list[str] = []

    # Required: Python >= 3.11
    if sys.version_info < (3, 11):
        failures.append(f"Python >= 3.11 required (have {sys.version_info.major}.{sys.version_info.minor})")

    # Required: the configured Google ingestion backend's dependency
    # (backend-aware — gog only when ingestion.google_backend is gog).
    _backend, backend_ok, backend_detail = _google_backend_status()
    if not backend_ok:
        failures.append(backend_detail)

    # Required: mlx_lm importable in *this* venv. A globally-installed `mlx_lm`
    # binary on PATH (Homebrew etc.) doesn't help — generation imports the
    # Python package. Distinguish the two so the error matches reality.
    try:
        importlib.import_module("mlx_lm")
    except ImportError:
        import shutil
        bin_present = shutil.which("mlx_lm") is not None
        hint = ' (a global `mlx_lm` binary on PATH was found, but YouOS needs the Python package in this venv)' if bin_present else ''
        failures.append(f'mlx_lm Python package not importable in this venv — install the local model engine: pip install -e ".[mlx]"{hint}')

    # Required: youos_config.yaml exists (in the active instance, not the repo)
    config_path = get_instance_root() / "youos_config.yaml"
    if not config_path.exists():
        failures.append(f"youos_config.yaml not found at {config_path}")

    # Required: user.emails set
    try:
        from app.core.config import get_user_emails

        emails = get_user_emails()
        if not emails:
            failures.append("user.emails not set in config")
    except Exception:
        failures.append("user.emails not set in config")

    all_passed = len(failures) == 0
    return (all_passed, failures)


def run_doctor_checks_full() -> tuple[bool, list[str], list[str]]:
    """Run all checks including warnings.

    Returns (all_required_passed, required_failures, warnings).
    """
    passed, failures = run_doctor_checks()
    warnings: list[str] = []

    # Warning: youos.db exists (in the active instance, not the repo)
    from app.core.settings import get_settings

    db_path = resolve_sqlite_path(get_settings().database_url)
    if not db_path.exists():
        warnings.append(f"{db_path} not found")

    # Warning: >= 3GB disk free
    try:
        stat = os.statvfs(ROOT_DIR)
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        if free_gb < 3.0:
            warnings.append(f"Low disk space ({free_gb:.1f}GB free, recommend >= 3GB)")
    except Exception:
        warnings.append("Could not check disk space")

    # Warning: models/ has content (active instance, not the repo)
    models_dir = get_models_dir()
    if not models_dir.exists() or not any(models_dir.iterdir()):
        warnings.append(f"{models_dir} is empty")

    # Warning: drafts are silently NOT using a LoRA adapter. The most common
    # silent failure — a user believes drafts are personalized while they run on
    # the base model (no adapter trained) or can't run locally at all (mlx_lm
    # missing → cloud fallback). Reuses the same reality-based signal the stats
    # dashboard shows. Healthy (LoRA actually in use) → no warning.
    try:
        from app.core.settings import get_settings
        from app.core.stats import get_drafting_model_status

        drafting = get_drafting_model_status(get_settings().database_url)
        if not drafting.get("healthy", True):
            warnings.append(f"Drafting: {drafting.get('label')} — {drafting.get('detail')}")
    except Exception:
        pass

    # Warning: personas.routing_enabled in config but no per-persona
    # adapters are trained yet — every draft will silently fall through
    # to the global, defeating the point of flipping the routing flag.
    # Catches the order-of-operations misconfig where the user enables
    # routing before Phase 2's nightly has accumulated any adapters.
    try:
        from app.core.config import load_config
        from app.core.stats import get_persona_adapter_status

        cfg = load_config() or {}
        if isinstance(cfg, dict):
            personas_cfg = cfg.get("personas") or {}
            if isinstance(personas_cfg, dict) and personas_cfg.get("routing_enabled"):
                statuses = get_persona_adapter_status()
                if not any(s.get("trained") for s in statuses.values()):
                    warnings.append(
                        "personas.routing_enabled: true but no per-persona adapters "
                        "are trained yet — every draft will fall through to the "
                        "global adapter. Wait for the nightly's finetune-personas "
                        "step to accumulate adapters, or set routing_enabled: false."
                    )
    except Exception:
        pass

    # Warning: reranker_enabled in config but sentence-transformers not loadable.
    # Without this the silent fallback would let the user think reranking is
    # firing when nothing is being reranked — exactly the misconfiguration the
    # `reranker_applied` response field exists to surface.
    try:
        import yaml

        from app.core.settings import get_settings

        cfg_path = Path(get_settings().configs_dir) / "retrieval" / "defaults.yaml"
        if cfg_path.exists():
            retrieval_cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            if isinstance(retrieval_cfg, dict) and retrieval_cfg.get("reranker_enabled"):
                from app.core.reranker import is_reranker_available

                if not is_reranker_available():
                    warnings.append(
                        "reranker_enabled: true in retrieval/defaults.yaml but "
                        "sentence-transformers isn't loadable — install with "
                        "`pip install youos[reranker]` or set reranker_enabled: false"
                    )
    except Exception:
        # Doctor must never crash on a single check; the absence of the warning
        # is its own signal that something went wrong upstream.
        pass

    # Warning: port 8901 free
    try:
        from app.core.config import get_server_port

        port = get_server_port()
    except Exception:
        port = 8901
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", port))
        s.close()
    except OSError:
        warnings.append(f"Port {port} is in use")

    return (passed, failures, warnings)
