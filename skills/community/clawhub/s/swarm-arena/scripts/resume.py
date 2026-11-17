#!/usr/bin/env python3
"""resume.py — clear halt / circuit-breaker and resume trading (SPEC section 5).

Clears halt + circuit_breaker, resets consecutive_errors, optionally switches
mode via --mode (default keeps current). CONSENT GUARD: resuming into
autonomous_live is refused unless config.autonomous_live_consent is already
true — this script can never create consent, only check it.

  --mode MODE   switch mode while resuming (paper default suggestion)
  --run-now     immediately run one autonomous_runner cycle after resuming
Every resume is journaled as a resume_event entry.

CLI: python3 resume.py config.json --mode paper --run-now
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402
from validate_config import MODES  # noqa: E402


def resume(config, config_path, state, state_path, trades_path,
           new_mode=None, run_now=False):
    mode_before = config.get("mode", "paper")
    if new_mode and new_mode != mode_before:
        if new_mode not in MODES:
            return {"ok": False, "error": "mode must be one of %s" % (", ".join(MODES),)}
        if new_mode == "autonomous_live" and not config.get("autonomous_live_consent", False):
            return {"ok": False,
                    "error": "cannot resume into autonomous_live: consent not present. "
                             "Consent can only be created by typing ACCEPT in onboarding.py."}
        config["mode"] = new_mode
        tmp = config_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(config, f, indent=2)
            f.write("\n")
        os.replace(tmp, config_path)

    state["halt"] = False
    state["circuit_breaker"] = False
    state["consecutive_errors"] = 0
    state["resumed_at"] = journal_trade.utcnow()

    journal_trade.journal_entry(trades_path, {
        "ts": state["resumed_at"], "symbol": "*",
        "mode": config.get("mode", mode_before),
        "decision": "resume_event", "signal": "resume",
        "signal_reason": "resumed (mode %s -> %s)" % (mode_before, config.get("mode", mode_before)),
        "status": "journaled",
    })

    tmp = state_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    os.replace(tmp, state_path)

    result = {"ok": True, "halt": False, "circuit_breaker": False,
              "mode": config.get("mode", mode_before)}
    if run_now:
        import autonomous_runner
        import io
        buf = io.StringIO()
        code = autonomous_runner.run_cycle(config_path, out=buf)
        result["run_now"] = {"exit_code": code, "output": buf.getvalue()[:2000]}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resume trading after halt / circuit breaker")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
    parser.add_argument("--mode", default=None, choices=MODES)
    parser.add_argument("--run-now", action="store_true")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    import filelock
    with filelock.held(state_path):  # load->mutate->save is one critical section
        state = {}
        if os.path.exists(state_path):
            with open(state_path) as f:
                state = json.load(f)
        result = resume(config, args.config, state, state_path, trades_path,
                        new_mode=args.mode, run_now=args.run_now)
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
