#!/usr/bin/env python3
"""validate_config.py — config validator. Prints {"ok", "errors", "warnings"}.

Checks (SPEC section 6):
  required fields present and correctly typed
  mode in paper | approval | live | autonomous_live
  consent pairing: mode=autonomous_live REQUIRES autonomous_live_consent=true;
                   consent=true with any other mode -> warning (harmless)
  min_leverage >= 1 and min_leverage <= max_leverage
  max_notional_per_trade <= max_total_exposure (sanity, warning if violated)
  allowed_symbols non-empty
  risk_pct_per_trade in (0, 0.25] (sanity bound, warning above 5%)
  numeric limits non-negative
Keys starting with "_" are annotations and ignored.

CLI:  python3 validate_config.py < config.json
      python3 validate_config.py config.json
Exit: 0 ok, 1 errors.
"""

import argparse
import json
import sys

MODES = ("paper", "approval", "live", "autonomous_live")

REQUIRED = {
    "mode": str,
    "base_url": str,
    "allowed_symbols": list,
    "base_value_per_trade": (int, float),
    "risk_pct_per_trade": (int, float),
    "min_leverage": int,
    "max_leverage": int,
    "max_notional_per_trade": (int, float),
    "max_total_exposure": (int, float),
    "max_concurrent_positions": int,
    "max_daily_loss": (int, float),
    "allow_short": bool,
    "require_stop_loss": bool,
    "require_take_profit": bool,
    "min_reward_risk": (int, float),
    "cooldown_after_close_sec": (int, float),
    "minimum_hold_sec": (int, float),
}


def validate_config(config):
    errors, warnings = [], []
    if not isinstance(config, dict):
        return {"ok": False, "errors": ["config must be a JSON object"], "warnings": []}

    for field, types in REQUIRED.items():
        if field not in config:
            errors.append("missing required field: %s" % field)
            continue
        value = config[field]
        tuple_types = types if isinstance(types, tuple) else (types,)
        if isinstance(value, bool) and bool not in tuple_types:
            errors.append("field %s must not be a boolean" % field)
        elif not isinstance(value, tuple_types):
            errors.append("field %s has wrong type (want %s)" % (field, types))

    if errors:
        return {"ok": False, "errors": errors, "warnings": warnings}

    mode = config["mode"]
    if mode not in MODES:
        errors.append("mode must be one of %s" % (", ".join(MODES),))

    consent = config.get("autonomous_live_consent", False)
    if not isinstance(consent, bool):
        errors.append("autonomous_live_consent must be a boolean")
    elif mode == "autonomous_live" and not consent:
        errors.append("mode=autonomous_live requires autonomous_live_consent=true "
                      "(set only by typing ACCEPT in onboarding.py)")
    elif consent and mode != "autonomous_live":
        warnings.append("autonomous_live_consent=true is set but mode=%s; consent is "
                        "inert until mode switches" % mode)

    if not config["allowed_symbols"] or not all(isinstance(s, str) and s for s in config["allowed_symbols"]):
        errors.append("allowed_symbols must be a non-empty list of symbols")

    if config["min_leverage"] < 1:
        errors.append("min_leverage must be >= 1")
    if config["min_leverage"] > config["max_leverage"]:
        errors.append("min_leverage (%s) > max_leverage (%s)"
                      % (config["min_leverage"], config["max_leverage"]))

    if config["max_notional_per_trade"] > config["max_total_exposure"] and config["max_total_exposure"] > 0:
        warnings.append("max_notional_per_trade (%s) exceeds max_total_exposure (%s); "
                        "exposure cap will bind first"
                        % (config["max_notional_per_trade"], config["max_total_exposure"]))

    if not (0 < float(config["risk_pct_per_trade"]) <= 0.25):
        errors.append("risk_pct_per_trade must be in (0, 0.25]")
    elif float(config["risk_pct_per_trade"]) > 0.05:
        warnings.append("risk_pct_per_trade above 5%% is aggressive")

    for field in ("max_notional_per_trade", "max_total_exposure", "max_daily_loss",
                  "min_reward_risk", "base_value_per_trade"):
        if float(config[field]) < 0:
            errors.append("%s must be >= 0" % field)
    if config["max_concurrent_positions"] < 0:
        errors.append("max_concurrent_positions must be >= 0")
    if config["require_stop_loss"] is False and mode in ("live", "autonomous_live"):
        errors.append("require_stop_loss cannot be disabled in live modes (hard rule)")
    if config["require_take_profit"] is False and mode in ("live", "autonomous_live"):
        errors.append("require_take_profit cannot be disabled in live modes (hard rule)")

    for section in ("cron", "sentiment", "execution"):
        if section in config and not isinstance(config[section], dict):
            errors.append("section %s must be an object" % section)

    gw = config.get("gateway")
    if gw is not None:
        if not isinstance(gw, dict):
            errors.append("section gateway must be an object")
        else:
            if "enabled" in gw and not isinstance(gw["enabled"], bool):
                errors.append("gateway.enabled must be a boolean")
            if gw.get("enabled"):
                url = gw.get("url")
                if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
                    errors.append("gateway.url must be an http(s) URL when gateway is enabled")
                token_env = gw.get("token_env", "MANTIS_AGENT_TOKEN")
                if not isinstance(token_env, str) or not token_env:
                    errors.append("gateway.token_env must be a non-empty env var name")
                else:
                    import os
                    if not os.environ.get(token_env):
                        warnings.append("gateway enabled but env %s is not set "
                                        "(must match the backend's agent token)" % token_env)
                timeout = gw.get("timeout_sec", 10)
                if not isinstance(timeout, (int, float)) or not (1 <= float(timeout) <= 60):
                    errors.append("gateway.timeout_sec must be a number in [1, 60]")
                if "required" in gw and not isinstance(gw["required"], bool):
                    errors.append("gateway.required must be a boolean")

    if mode in ("live", "autonomous_live"):
        import os
        for var in ("LIGHTER_API_PRIVATE_KEY", "LIGHTER_API_KEY_INDEX", "LIGHTER_ACCOUNT_INDEX"):
            if not os.environ.get(var):
                warnings.append("live mode: env %s is not set (checked at runtime)" % var)

    _validate_arena(config, mode, errors, warnings)

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def _validate_arena(config, mode, errors, warnings):
    """arena block: 1 agent = 1 model = 1 account. Each model needs a unique id,
    an LLM model name, and — in live modes — resolvable venue credentials
    (its own "env" map wins over the canonical env name)."""
    arena = config.get("arena")
    if arena is None:
        return
    if not isinstance(arena, dict):
        errors.append("section arena must be an object")
        return
    if "start_equity" in arena and not isinstance(arena["start_equity"], (int, float)):
        errors.append("arena.start_equity must be a number")
    if "cycle_interval_minutes" in arena:
        iv = arena["cycle_interval_minutes"]
        if not isinstance(iv, (int, float)) or iv < 1:
            errors.append("arena.cycle_interval_minutes must be a number >= 1")
    models = arena.get("models")
    if models is None:
        return
    if not isinstance(models, list) or not all(isinstance(m, dict) for m in models):
        errors.append("arena.models must be a list of objects")
        return
    import os
    seen = set()
    for m in models:
        mid = m.get("id")
        if not isinstance(mid, str) or not mid:
            errors.append("arena.models entry missing a non-empty \"id\"")
            continue
        if mid in seen:
            errors.append("arena.models id %r is duplicated" % mid)
        seen.add(mid)
        if not isinstance(m.get("model"), str) or not m.get("model"):
            errors.append("arena model %r is missing \"model\"" % mid)
        env = m.get("env")
        if env is not None and (not isinstance(env, dict) or
                                not all(isinstance(k, str) and k and isinstance(v, str) and v
                                        for k, v in env.items())):
            errors.append("arena model %r: \"env\" must map env names to env names" % mid)
            env = None
        if mode in ("live", "autonomous_live"):
            env = env or {}
            missing = [env.get(var, var)
                       for var in ("LIGHTER_API_PRIVATE_KEY", "LIGHTER_API_KEY_INDEX",
                                   "LIGHTER_ACCOUNT_INDEX")
                       if not os.environ.get(env.get(var, var))]
            if missing:
                warnings.append("arena model %r: live mode but credential env not set: %s "
                                "(run arena_preflight.py)" % (mid, ", ".join(missing)))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a swarmArena config")
    parser.add_argument("config", nargs="?", help="config.json path (default: stdin)")
    args = parser.parse_args(argv)
    try:
        if args.config and args.config != "-":
            with open(args.config) as f:
                config = json.load(f)
        else:
            config = json.load(sys.stdin)
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "errors": ["cannot parse config: %s" % e], "warnings": []}))
        return 1
    result = validate_config(config)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
