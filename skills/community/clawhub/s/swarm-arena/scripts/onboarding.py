#!/usr/bin/env python3
"""onboarding.py — interactive setup wizard (SPEC section 6).

Flow:
  1. Credentials: read from env; prompt for any that are missing
     (LIGHTER_API_PRIVATE_KEY, LIGHTER_API_KEY_INDEX, LIGHTER_ACCOUNT_INDEX,
     LIGHTER_L1_ADDRESS for account discovery). Secrets are masked in all
     output (last 4 chars) and NEVER written to any file.
  2. LIVE VERIFY (skipped only when the chosen mode is paper): mint an auth
     token via the SDK and read the account. Failure here is fatal — no
     config.json is written.
  3. Collect: symbols, base value per trade, leverage bounds, exposure cap,
     daily loss limit, allow_short.
  4. CONSENT GATE: autonomous_live is offered; enabling it requires the human
     to physically type ACCEPT at the keyboard. This is the ONLY place in the
     whole skill where autonomous_live_consent can become true. Every other
     script treats it as read-only.
  5. Write config.json (atomic, chmod 600).
  6. Offer to run register_crons.py and one first paper cycle.

CLI: python3 onboarding.py [--dir DIR]
"""

import argparse
import getpass
import json
import os
import stat
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lighter_rest_client import LighterRestClient, LighterAPIError, DEFAULT_BASE_URL  # noqa: E402

CONSENT_WORD = "ACCEPT"


def _mask(value):
    if not value:
        return "<unset>"
    value = str(value)
    return "...%s" % value[-4:] if len(value) > 4 else "...%s" % value


def _ask(prompt, default=None, secret=False):
    suffix = " [%s]" % (_mask(default) if secret and default else default) if default else ""
    if secret:
        value = getpass.getpass("%s%s: " % (prompt, suffix))
    else:
        value = input("%s%s: " % (prompt, suffix))
    value = value.strip()
    return value or (str(default) if default is not None else "")


def _ask_int(prompt, default):
    while True:
        raw = _ask(prompt, default)
        try:
            return int(raw)
        except ValueError:
            print("  please enter an integer")


def _ask_float(prompt, default):
    while True:
        raw = _ask(prompt, default)
        try:
            return float(raw)
        except ValueError:
            print("  please enter a number")


def _ask_bool(prompt, default):
    raw = _ask(prompt, "yes" if default else "no")
    return raw.strip().lower() in ("y", "yes", "true", "1")


def collect_credentials():
    print("\n== Step 1/4: Lighter API credentials (env-first, never stored) ==")
    private_key = os.environ.get("LIGHTER_API_PRIVATE_KEY") or _ask(
        "LIGHTER_API_PRIVATE_KEY", secret=True)
    key_index = os.environ.get("LIGHTER_API_KEY_INDEX") or _ask("LIGHTER_API_KEY_INDEX (2-254)")
    account_index = os.environ.get("LIGHTER_ACCOUNT_INDEX")
    l1_address = os.environ.get("LIGHTER_L1_ADDRESS")
    if not account_index and l1_address:
        print("  discovering account index for L1 address %s ..." % _mask(l1_address))
        try:
            account_index = str(LighterRestClient().discover_account_index(l1_address))
            print("  discovered account index %s" % account_index)
        except LighterAPIError as e:
            print("  discovery failed: %s" % e)
    if not account_index:
        account_index = _ask("LIGHTER_ACCOUNT_INDEX")
    print("  key: %s  key_index: %s  account: %s"
          % (_mask(private_key), key_index, account_index))
    return private_key, int(key_index), int(account_index)


def verify_live(private_key, key_index, account_index, base_url):
    """Fail hard unless the SDK can mint a token AND read the account."""
    print("\n== Live verification against Lighter ==")
    import lighter_signer
    creds = {"private_key": private_key, "api_key_index": key_index,
             "account_index": account_index, "base_url": base_url}
    token = lighter_signer.mint_auth_token(deadline=600, creds=creds)
    print("  auth token minted (%s)" % _mask(token))
    client = LighterRestClient(base_url=base_url, auth_token=token)
    account = client.get_account(account_index, auth=True)
    summary = client.account_summary(account)
    print("  account %d OK — collateral $%.2f" % (account_index, summary["equity"]))
    return summary


def consent_gate():
    """Returns True only when the human physically types ACCEPT."""
    print("\n== Step 4/4: autonomous_live consent gate ==")
    print("  autonomous_live lets swarmArena place REAL orders 24/7 with no")
    print("  per-trade approval. Hard caps still apply (notional, exposure,")
    print("  daily loss, leverage ceiling, mandatory reduce-only SL/TP).")
    print("  This consent is one-way: scripts can never set it themselves.")
    print("  To enable autonomous_live, type exactly: %s" % CONSENT_WORD)
    print("  Anything else keeps the account in safer modes.")
    if not sys.stdin.isatty():
        print("  (not a TTY — consent refused by default)")
        return False
    answer = input("  consent: ").strip()
    granted = answer == CONSENT_WORD
    print("  consent %s." % ("GRANTED" if granted else "not granted"))
    return granted


def main(argv=None):
    parser = argparse.ArgumentParser(description="swarmArena onboarding wizard")
    parser.add_argument("--dir", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        help="directory to write config.json into (default: skill root)")
    args = parser.parse_args(argv)

    print("swarmArena onboarding — Lighter perpetual futures agent")
    base_url = os.environ.get("LIGHTER_BASE_URL") or _ask("Base URL", DEFAULT_BASE_URL)

    mode = _ask("Mode (paper/approval/live/autonomous_live)", "paper").lower()
    if mode not in ("paper", "approval", "live", "autonomous_live"):
        print("error: unknown mode %r" % mode, file=sys.stderr)
        return 1

    private_key = key_index = account_index = None
    if mode in ("live", "autonomous_live"):
        private_key, key_index, account_index = collect_credentials()
        try:
            verify_live(private_key, key_index, account_index, base_url)
        except SystemExit as e:
            print(str(e), file=sys.stderr)
            return 1
        except LighterAPIError as e:
            print("error: live verification failed: %s" % e, file=sys.stderr)
            print("config.json was NOT written.", file=sys.stderr)
            return 1
    else:
        print("\n== Step 1/4: credentials ==")
        print("  mode=%s needs no credentials now; live upgrade will verify them then." % mode)

    print("\n== Step 3/4: risk parameters ==")
    symbols_raw = _ask("Allowed symbols (comma separated)", "ETH,BTC,SOL")
    symbols = [s.strip().upper() for s in symbols_raw.split(",") if s.strip()]
    base_value = _ask_float("Base value per trade (USD)", 100)
    min_lev = _ask_int("Min leverage (client-side cap)", 2)
    max_lev = _ask_int("Max leverage (client-side cap)", 10)
    max_notional = _ask_float("Max notional per trade (USD)", 500)
    max_exposure = _ask_float("Max total exposure (USD)", 2000)
    max_daily_loss = _ask_float("Max daily loss (USD)", 100)
    allow_short = _ask_bool("Allow shorts?", True)

    consent = False
    if mode == "autonomous_live":
        consent = consent_gate()
        if not consent:
            print("  autonomous_live requires consent; falling back to mode=live.")
            mode = "live"
    elif mode == "live":
        print("\n(autonomous_live is available only through the consent gate; staying with live.)")

    config = {
        "mode": mode,
        "autonomous_live_consent": consent,
        "base_url": base_url,
        "allowed_symbols": symbols,
        "base_value_per_trade": base_value,
        "risk_pct_per_trade": 0.01,
        "min_leverage": min_lev,
        "max_leverage": max_lev,
        "max_notional_per_trade": max_notional,
        "max_total_exposure": max_exposure,
        "max_concurrent_positions": 3,
        "max_daily_loss": max_daily_loss,
        "allow_short": allow_short,
        "require_stop_loss": True,
        "require_take_profit": True,
        "min_reward_risk": 1.5,
        "cooldown_after_close_sec": 120,
        "minimum_hold_sec": 60,
        "cron": {"enabled": True, "scan_interval_minutes": 2,
                 "review_interval_minutes": 30, "daily_summary_hour": 0},
        "sentiment": {"enabled": False, "weight": 0.1},
        "execution": {"cancel_on_halt": True, "flatten_on_emergency_stop": False,
                      "require_human_approval_for_live_orders": mode == "live"},
        "gateway": {"enabled": True, "url": "http://127.0.0.1:8080",
                    "token_env": "MANTIS_AGENT_TOKEN", "timeout_sec": 10,
                    "required": True},
    }

    print("\n== Gateway mode ==")
    print("  All exchange traffic will flow through the swarm-arena-backend")
    print("  (%s), which proxies to Lighter and records every order." % config["gateway"]["url"])
    print("  Set the SAME shared token in both environments before running:")
    print("    export MANTIS_AGENT_TOKEN=<shared-secret>")

    config_path = os.path.join(args.dir, "config.json")
    tmp = config_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
    os.replace(tmp, config_path)
    print("\n== config.json written to %s (mode 600) ==" % config_path)
    print("Credentials were NOT written anywhere. Export them before running live:")
    print("  export LIGHTER_API_PRIVATE_KEY=... LIGHTER_API_KEY_INDEX=%s LIGHTER_ACCOUNT_INDEX=%s"
          % (key_index or "N", account_index or "N"))

    from validate_config import validate_config
    verdict = validate_config(config)
    if not verdict["ok"]:
        print("warning: fresh config failed validation: %s" % verdict["errors"], file=sys.stderr)
        return 1

    if _ask_bool("Register cron schedules now?", True):
        import register_crons
        register_crons.main(["--mode", "paper" if mode == "paper" else "live"])

    if _ask_bool("Run a first cycle now?", False):
        import autonomous_runner
        autonomous_runner.run_cycle(config_path)
    print("Onboarding complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
