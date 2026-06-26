#!/usr/bin/env python3
"""_model.py — resolve which OpenRouter model to use for review-agent LLM calls.

v2 (openclaw) precedence (highest → lowest):
  1. REVIEW_AGENT_MODEL env var (explicit override, any format)
  2. ~/.openclaw/openclaw.json → agents.defaults.models[*].alias == "default"
     (the user's pinned default if they set one)
  3. ~/.openclaw/openclaw.json → models.providers.openrouter.models[0]
     (first-listed openrouter model; this is what `openclaw models list` shows
     when no alias is the default)
  4. Hard fallback: "anthropic/claude-sonnet-4.6"

Returns a string ready to pass to the OpenRouter /chat/completions API.

(v1 hermes version read ~/.hermes/config.yaml and mapped hermes-style ids
like 'claude-sonnet-4-6' → 'anthropic/claude-sonnet-4.6'. In openclaw the
model config entries are already in OpenRouter format, so no mapping needed.)
"""
import json
import os
from pathlib import Path


FALLBACK_MODEL = "anthropic/claude-sonnet-4.6"


def _openclaw_default_model():
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception:
        return None

    # (2) agents.defaults.models[*] with alias == "default"
    defaults = ((cfg.get("agents") or {}).get("defaults") or {}).get("models") or {}
    if isinstance(defaults, dict):
        # Format is {"<provider>/<model>": {"alias": "default"}, ...}
        for model_id, meta in defaults.items():
            if isinstance(meta, dict) and meta.get("alias") == "default":
                return model_id.removeprefix("openrouter/") if model_id.startswith("openrouter/") else model_id

    # (3) first openrouter model in providers list
    providers = ((cfg.get("models") or {}).get("providers") or {})
    openrouter = providers.get("openrouter") or {}
    models_list = openrouter.get("models") or []
    for m in models_list:
        mid = m.get("id") if isinstance(m, dict) else None
        if mid:
            return mid

    return None


def get_main_agent_model():
    env_model = os.environ.get("REVIEW_AGENT_MODEL", "").strip()
    if env_model:
        return env_model

    picked = _openclaw_default_model()
    if picked:
        return picked

    return FALLBACK_MODEL


if __name__ == "__main__":
    # Self-test
    import sys
    override_cases = [
        ("explicit env", {"REVIEW_AGENT_MODEL": "openai/gpt-5"}, "openai/gpt-5"),
        ("no env, uses config/fallback", {"REVIEW_AGENT_MODEL": ""}, None),  # depends on machine
    ]
    for name, env_patch, expected in override_cases:
        saved = {k: os.environ.get(k) for k in env_patch}
        os.environ.update({k: v for k, v in env_patch.items()})
        got = get_main_agent_model()
        if expected is not None:
            ok = "✓" if got == expected else "✗"
            print(f"  {ok} {name}: got={got} expected={expected}")
        else:
            print(f"  · {name}: resolved to → {got}")
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
