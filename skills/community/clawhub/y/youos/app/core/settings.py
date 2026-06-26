import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.version import get_version

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "YouOS"
    version: str = Field(default_factory=get_version)
    environment: str = "dev"
    instance_name: str = "YouOS"
    data_dir: Path | None = Field(default=None)  # YOUOS_DATA_DIR — instance root
    database_url: str = Field(default="sqlite:///var/youos.db")
    configs_dir: Path = Field(default=ROOT_DIR / "configs")

    model_config = SettingsConfigDict(
        env_prefix="YOUOS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @model_validator(mode="after")
    def _apply_data_dir(self) -> "Settings":
        """Derive database_url and configs_dir from data_dir when not set explicitly."""
        if self.data_dir is not None:
            data_dir = Path(self.data_dir).expanduser().resolve()
            if "YOUOS_DATABASE_URL" not in os.environ:
                self.database_url = f"sqlite:///{data_dir}/var/youos.db"
            if "YOUOS_CONFIGS_DIR" not in os.environ:
                self.configs_dir = data_dir / "configs"
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_instance_root() -> Path:
    """Return the root of the active instance — ``data_dir`` if set, else repo root.

    Use this when an absolute path under an instance is needed and the more
    specific helpers (``get_var_dir``, ``get_models_dir``, ``get_adapter_path``)
    don't apply — e.g. the per-instance ``youos_config.yaml``.
    """
    settings = get_settings()
    if settings.data_dir is not None:
        return Path(settings.data_dir).expanduser().resolve()
    return ROOT_DIR


def get_var_dir() -> Path:
    """Return the var/ directory for the active instance (or project root var/)."""
    return get_instance_root() / "var"


def get_models_dir() -> Path:
    """Return the models/ directory for the active instance.

    Houses ``adapters/latest/`` (the LoRA adapter) and any future per-instance
    model artifacts. Centralised here so doctor / teardown / status report on
    the same directory the fine-tune writer (``scripts.finetune_lora``) uses.
    """
    return get_instance_root() / "models"


def get_adapter_path() -> Path:
    """Return the LoRA adapter directory for the active instance.

    Honors YOUOS_DATA_DIR so per-instance fine-tunes land in (and are read
    from) the instance's own ``models/adapters/latest``. Without this every
    instance shared the repo-root adapter dir — fine-tunes overwrote each
    other and a generation reader looking at the instance dir would not find
    the adapter that the writer had put in the repo dir.

    The "latest" name dates from when this was the only adapter per instance.
    Per-persona adapters live alongside it under
    ``<models_dir>/adapters/personas/{sender_type}/`` (see
    ``get_persona_adapter_path``) — "latest" is preserved as the default
    fallback adapter when a per-persona one isn't trained yet.
    """
    return get_models_dir() / "adapters" / "latest"


def get_persona_adapter_path(sender_type: str) -> Path:
    """Return the per-persona LoRA adapter directory for a sender_type cohort.

    Sibling to ``get_adapter_path()`` (the "latest" / global adapter).
    Persona adapters live at ``<models_dir>/adapters/personas/{sender_type}/``
    so the existing global adapter dir layout is untouched — fine-tunes that
    don't opt into the persona-routing flow still write to "latest" as they
    always did.

    Sender types come from ``app.core.sender.SenderType`` (``internal`` /
    ``external_client`` / ``personal`` / ``automated`` / ``unknown``). The
    directory is *not* created here — only resolved. Phase 2 of the
    per-persona work (per-cohort fine-tune step) creates it on first write.
    """
    safe = (sender_type or "unknown").strip().lower()
    return get_models_dir() / "adapters" / "personas" / safe
