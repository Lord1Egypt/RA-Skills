import json
import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file(env_path: Path) -> None:
    """Parse a .env file and populate os.environ (stdlib only, no dotenv needed)."""
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def load_config(config_path: str = None) -> dict:
    """Load configuration from config.json, .env, and environment variables.

    Priority (highest first): env vars > .env > config.json
    """
    # Load .env if present
    env_path = SKILL_ROOT / ".env"
    if env_path.exists():
        _load_env_file(env_path)

    # Load config.json
    if config_path is None:
        config_path = SKILL_ROOT / "config.json"
    else:
        config_path = Path(config_path)

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        # Fall back to example config
        example_path = SKILL_ROOT / "assets" / "config.example.json"
        if example_path.exists():
            with open(example_path, "r") as f:
                config = json.load(f)
        else:
            config = {}

    # Override with env vars
    if os.getenv("IMAGE_DEFAULT_PROVIDER"):
        config["default_provider"] = os.getenv("IMAGE_DEFAULT_PROVIDER")

    if os.getenv("IMAGE_OUTPUT_DIR"):
        config["output_dir"] = os.getenv("IMAGE_OUTPUT_DIR")

    # Ensure providers section exists
    config.setdefault("providers", {})
    config.setdefault("default_provider", "openrouter")
    config.setdefault("output_dir", "output")

    return config


def get_api_key(provider_name: str) -> str:
    """Get API key for a provider from environment."""
    env_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "kie": "KIE_API_KEY",
        "yandexart": "YANDEX_IAM_TOKEN",
    }
    env_var = env_map.get(provider_name)
    if env_var is None:
        raise ValueError(f"Unknown provider: {provider_name}")

    key = os.getenv(env_var)
    if not key:
        raise EnvironmentError(
            f"API key not found. Set the {env_var} environment variable."
        )
    return key


def get_output_dir(config: dict) -> Path:
    """Resolve output directory path."""
    output_dir = config.get("output_dir", "output")
    path = Path(output_dir)
    if not path.is_absolute():
        path = SKILL_ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path
