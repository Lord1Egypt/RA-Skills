import os
import re

import yaml

from smart_home.models import PipelineConfig


def _resolve_env_vars(value: str) -> str:
    """Replace ${VAR_NAME} patterns with environment variable values."""
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        env_val = os.environ.get(var_name)
        if env_val is None:
            raise ValueError(
                f"Environment variable ${var_name} is not set. "
                f"Set it before running the skill."
            )
        return env_val
    return re.sub(r"\$\{(\w+)\}", replacer, value)


def load_config(path: str) -> PipelineConfig:
    """Load skill configuration from a YAML file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        raw = yaml.safe_load(f)

    ha = raw["home_assistant"]
    ha_url = ha["url"]
    ha_token = _resolve_env_vars(ha["token"])

    if "rules" not in raw or not raw["rules"]:
        raise ValueError("Config file must contain at least one rule under 'rules'")
    rule = raw["rules"][0]
    outputs = raw.get("outputs", {}).get("default", ["summary", "table"])

    return PipelineConfig(
        ha_url=ha_url,
        ha_token=ha_token,
        threshold_watts=rule["threshold_watts"],
        time_after=rule["time_window"]["after"],
        time_before=rule["time_window"]["before"],
        require_occupancy=rule.get("require_occupancy", "off"),
        action=rule.get("action", "turn_off"),
        default_outputs=outputs,
    )
