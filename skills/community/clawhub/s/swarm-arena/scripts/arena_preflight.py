#!/usr/bin/env python3
"""arena_preflight.py — 1 agent = 1 model = 1 account readiness check.

For every config.arena.models entry verify, WITHOUT placing or signing anything:
  llm:     endpoint configured + API key env present
  account: venue credential envs resolve — a model's own "env" map wins over
           the canonical name, e.g. {"LIGHTER_ACCOUNT_INDEX": "LIGHTER_ACCOUNT_INDEX_KIMI"}
  files:   state.<id>.json / trades.<id>.json parse when present
           (absent is fine — created on first run)
  flags:   halt / circuit_breaker status in the model's state file

Exit 0 when every model is ready, 1 otherwise.
CLI:  python3 arena_preflight.py config.json [--json]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model_runner import model_files, resolve_model_cfg  # noqa: E402

# signing set required for live writes; L1 address is informational
VENUE_VARS = ("LIGHTER_API_PRIVATE_KEY", "LIGHTER_API_KEY_INDEX", "LIGHTER_ACCOUNT_INDEX")
INFO_VARS = ("LIGHTER_L1_ADDRESS",)


def check_model(config, config_path, model_cfg):
    m = resolve_model_cfg(config, model_cfg)
    model_id = m.get("id") or m.get("model") or "model"
    env = m.get("env") or {}
    problems = []

    if not m.get("base_url"):
        problems.append("llm: no base_url (set arena.endpoint or a model-level base_url)")
    key_var = m.get("api_key_env")
    if not key_var:
        problems.append("llm: no api_key_env (set arena.api_key_env or a model-level one)")
    elif not os.environ.get(key_var):
        problems.append("llm: env %s is not set" % key_var)

    account = {}
    for var in VENUE_VARS + INFO_VARS:
        src = env.get(var, var)
        is_set = bool(os.environ.get(src))
        account[var] = {"via": src, "set": is_set}
        if not is_set and var in VENUE_VARS:
            problems.append("account: env %s is not set%s" %
                            (src, "" if src == var else " (mapped from %s)" % var))

    state_path, trades_path = model_files(config_path, model_id)
    files = {}
    for label, path in (("state", state_path), ("trades", trades_path)):
        if not os.path.exists(path):
            files[label] = "absent (created on first run)"
            continue
        try:
            with open(path) as f:
                json.load(f)
            files[label] = "ok"
        except (OSError, json.JSONDecodeError) as e:
            files[label] = "CORRUPT: %s" % e
            problems.append("files: %s is corrupt (%s)" % (os.path.basename(path), e))

    flags = {}
    if os.path.exists(state_path):
        try:
            with open(state_path) as f:
                st = json.load(f)
            flags = {"halt": bool(st.get("halt")),
                     "circuit_breaker": bool(st.get("circuit_breaker"))}
            if flags["halt"] or flags["circuit_breaker"]:
                problems.append("flags: halt/circuit_breaker set (resume.py clears them)")
        except (OSError, json.JSONDecodeError):
            pass  # already reported as corrupt above

    return {"model": model_id, "ready": not problems, "problems": problems,
            "account": account, "files": files, "flags": flags}


def run_preflight(config_path):
    with open(config_path) as f:
        config = json.load(f)
    models = (config.get("arena") or {}).get("models") or []
    rows = [check_model(config, config_path, mc) for mc in models]
    return {"mode": config.get("mode"), "models": rows,
            "all_ready": bool(rows) and all(r["ready"] for r in rows)}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Arena 1-1-1 readiness check")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--json", action="store_true", help="machine output")
    args = parser.parse_args(argv)
    try:
        report = run_preflight(args.config)
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"all_ready": False, "error": "cannot read config: %s" % e}))
        return 1
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("mode: %s" % report["mode"])
        for row in report["models"]:
            print("%-12s %s" % (row["model"], "READY" if row["ready"] else "NOT READY"))
            for prob in row["problems"]:
                print("  - %s" % prob)
        print("all_ready: %s" % report["all_ready"])
    return 0 if report["all_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
