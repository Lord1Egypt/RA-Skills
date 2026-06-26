"""YouOS user configuration loader.

Reads youos_config.yaml and provides typed access to user settings.
All persona-specific values (name, emails, internal domains) are derived from this config.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]


def _default_config_path() -> Path:
    data_dir = os.environ.get("YOUOS_DATA_DIR")
    if data_dir:
        return Path(data_dir).expanduser().resolve() / "youos_config.yaml"
    return ROOT_DIR / "youos_config.yaml"


CONFIG_PATH = _default_config_path()


def _load_raw_config(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or CONFIG_PATH
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@lru_cache(maxsize=1)
def load_config(config_path: Path | None = None) -> dict[str, Any]:
    return _load_raw_config(config_path)


def get_user_name(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("user", {}).get("name", "") or "User"


def get_display_name(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("user", {}).get("display_name", "") or "YouOS"


def get_user_emails(config: dict[str, Any] | None = None) -> tuple[str, ...]:
    cfg = config or load_config()
    emails = cfg.get("user", {}).get("emails", [])
    return tuple(emails) if emails else ()


def get_user_names(config: dict[str, Any] | None = None) -> tuple[str, ...]:
    cfg = config or load_config()
    names = cfg.get("user", {}).get("names", [])
    return tuple(names) if names else ()


def get_internal_domains(config: dict[str, Any] | None = None) -> frozenset[str]:
    """Get internal domains from explicit config or derive from user emails."""
    cfg = config or load_config()
    # Explicit internal_domains from config takes priority
    explicit = cfg.get("user", {}).get("internal_domains", [])
    if explicit:
        return frozenset(d.lower() for d in explicit if d)

    # Fall back to deriving from email addresses
    emails = get_user_emails(cfg)
    domains: set[str] = set()
    personal = {
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "icloud.com",
        "me.com",
        "outlook.com",
        "live.com",
        "aol.com",
        "protonmail.com",
        "proton.me",
        "fastmail.com",
    }
    for email in emails:
        if "@" in email:
            domain = email.split("@", 1)[1].lower()
            if domain not in personal:
                domains.add(domain)
    return frozenset(domains)


def get_ingestion_accounts(config: dict[str, Any] | None = None) -> tuple[str, ...]:
    cfg = config or load_config()
    accounts = cfg.get("ingestion", {}).get("accounts", [])
    if accounts:
        return tuple(accounts)
    return get_user_emails(cfg)


def get_ingestion_google_backend(config: dict[str, Any] | None = None) -> str:
    """Which backend fetches Gmail/Docs: ``gog`` (default), ``gws``, or ``native``.

    Surfaced so YouOS can move off the OpenClaw ``gog`` CLI without code
    changes — ``gws`` is Google's own Workspace CLI and ``native`` is the
    direct Google-API client. An unrecognized value degrades to ``gog`` (the
    always-available default) rather than breaking ingestion at config-read
    time; the doctor is responsible for flagging a misconfigured backend.
    """
    cfg = config or load_config()
    raw = cfg.get("ingestion", {}).get("google_backend", "gog")
    value = str(raw).strip().lower() if raw else "gog"
    return value if value in ("gog", "gws", "native") else "gog"


def get_base_model(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("model", {}).get("base", "Qwen/Qwen2.5-1.5B-Instruct")


def get_model_fallback(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("model", {}).get("fallback", "none")


def get_server_port(config: dict[str, Any] | None = None) -> int:
    cfg = config or load_config()
    return int(cfg.get("server", {}).get("port", 8901))


def get_server_host(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("server", {}).get("host", "127.0.0.1")


def get_tailscale_hostname(config: dict[str, Any] | None = None) -> str:
    cfg = config or load_config()
    return cfg.get("tailscale", {}).get("hostname", "")


def get_user_timezone(config: dict[str, Any] | None = None) -> str:
    """Return ``user.timezone`` (IANA name) or ``UTC`` when unset/invalid.

    Used by ingestion paths that need to attach tzinfo to naive timestamps
    (WhatsApp exports record local times with no offset). Falling back to
    UTC rather than tzlocal() because the server's clock may be in a
    different zone than the device that produced the export — UTC at
    least makes the timestamps monotonic across sources, even if the
    wall-clock interpretation is wrong by a few hours.
    """
    cfg = config or load_config()
    tz = (cfg.get("user", {}) or {}).get("timezone", "") or ""
    if not isinstance(tz, str) or not tz.strip():
        return "UTC"
    return tz.strip()


def get_autoresearch_iterations(config: dict[str, Any] | None = None) -> int:
    cfg = config or load_config()
    return int(cfg.get("autoresearch", {}).get("iterations", 80))


def get_persona_mode_config(sender_type: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    return cfg.get("persona", {}).get("modes", {}).get(sender_type, {})


def get_persona_style_anchor(sender_type: str, config: dict[str, Any] | None = None) -> str | None:
    mode_config = get_persona_mode_config(sender_type, config)
    return mode_config.get("style_anchor")


def get_ollama_config(config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    return cfg.get("model", {}).get("ollama", {})


def is_ollama_enabled(config: dict[str, Any] | None = None) -> bool:
    return bool(get_ollama_config(config).get("enabled", False))


def get_review_batch_size(config: dict[str, Any] | None = None) -> int:
    """Read review.batch_size from config, default 10, clamped to 5-50."""
    cfg = config or load_config()
    raw = cfg.get("review", {}).get("batch_size", 10)
    return max(5, min(50, int(raw)))


def get_review_draft_model(config: dict[str, Any] | None = None) -> str:
    """Read review.draft_model from config.

    'claude'  — use Claude CLI
    'local'   — use local Qwen adapter (private)
    'auto'    — (default) use local if an adapter is trained, else Claude
    """
    cfg = config or load_config()
    val = cfg.get("review", {}).get("draft_model", "auto").lower().strip()
    if val not in ("claude", "local", "auto"):
        return "auto"
    return val


def get_last_ingest_at(account: str, config: dict[str, Any] | None = None) -> str | None:
    cfg = config or load_config()
    return cfg.get("ingestion", {}).get("last_ingest_at", {}).get(account)


def set_last_ingest_at(account: str, timestamp: str, config: dict[str, Any] | None = None) -> None:
    cfg = config if config is not None else _load_raw_config()
    cfg.setdefault("ingestion", {}).setdefault("last_ingest_at", {})[account] = timestamp
    save_config(cfg)


_PERSONAL_DOMAINS = frozenset(
    {
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "icloud.com",
        "me.com",
        "outlook.com",
        "live.com",
        "aol.com",
        "protonmail.com",
        "proton.me",
        "fastmail.com",
    }
)


def get_account_for_sender(sender: str, config: dict[str, Any] | None = None) -> str | None:
    """Infer which user account email to use based on sender domain.

    - If sender domain matches an internal domain → return work account email
    - If sender is from a personal domain (gmail, yahoo, etc) → return personal account email
    - If ambiguous → return None (use all accounts)
    """
    if not sender or "@" not in sender:
        return None

    cfg = config or load_config()
    emails = get_user_emails(cfg)
    if not emails:
        return None

    sender_domain = sender.rsplit("@", 1)[-1].lower()
    internal_domains = get_internal_domains(cfg)

    # Sender is from an internal domain → use work email (non-personal domain email)
    if sender_domain in internal_domains:
        for email in emails:
            domain = email.split("@", 1)[-1].lower() if "@" in email else ""
            if domain not in _PERSONAL_DOMAINS:
                return email
        return emails[0] if emails else None

    # Sender is from a personal domain → use personal email
    if sender_domain in _PERSONAL_DOMAINS:
        for email in emails:
            domain = email.split("@", 1)[-1].lower() if "@" in email else ""
            if domain in _PERSONAL_DOMAINS:
                return email
        return emails[0] if emails else None

    # External/ambiguous domain → return None (no filter)
    return None


def save_config(config: dict[str, Any], config_path: Path | None = None) -> None:
    path = config_path or CONFIG_PATH
    path.write_text(
        yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    load_config.cache_clear()
