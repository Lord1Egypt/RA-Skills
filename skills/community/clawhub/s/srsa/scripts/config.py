from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AppConfig:
    desired_retention: float
    database_path: Path
    enable_fuzzing: bool
    maximum_interval: int


def load_config(config_path: Path | None = None) -> AppConfig:
    script_dir = Path(__file__).resolve().parent
    resolved_path = config_path or (script_dir / "config.yaml")

    if not resolved_path.exists():
        raise FileNotFoundError(f"Config file not found: {resolved_path}")

    with resolved_path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    desired_retention = float(raw.get("desired_retention", 0.9))
    if not (0.0 < desired_retention < 1.0):
        raise ValueError("desired_retention must be between 0 and 1")

    configured_db_path = str(raw.get("database_path", "cache/fsrs.sqlite"))
    db_path = Path(configured_db_path)
    if not db_path.is_absolute():
        db_path = (resolved_path.parent / db_path).resolve()

    enable_fuzzing = bool(raw.get("enable_fuzzing", False))
    maximum_interval = int(raw.get("maximum_interval", 36500))

    db_path.parent.mkdir(parents=True, exist_ok=True)

    return AppConfig(
        desired_retention=desired_retention,
        database_path=db_path,
        enable_fuzzing=enable_fuzzing,
        maximum_interval=maximum_interval,
    )
