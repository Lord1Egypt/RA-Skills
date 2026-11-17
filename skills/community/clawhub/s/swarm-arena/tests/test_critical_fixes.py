#!/usr/bin/env python3
"""Verification harness for the critical fixes:

  1. halt.py persists halt=true even when the signer/credentials are unusable
  2. lighter_signer rolls back a partially placed bracket (cancel legs + close)
  3. filelock makes journal appends safe across concurrent cron processes
  4. circuit-breaker accounting: per-symbol errors counted once, trailing-stop
     failures feed the counter, clean cycle resets

Run: python3 tests/test_critical_fixes.py
Plain asserts, no framework. Sandboxes under /tmp; repo files untouched.
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import filelock            # noqa: E402
import journal_trade       # noqa: E402
import halt as halt_mod    # noqa: E402
import autonomous_runner as runner  # noqa: E402
import lighter_signer as signer     # noqa: E402


def _sandbox_config(**over):
    cfg = {
        "mode": "paper",
        "autonomous_live_consent": False,
        "base_url": "http://127.0.0.1:9",
        "allowed_symbols": ["ETH", "BTC", "SOL"],
        "base_value_per_trade": 100,
        "risk_pct_per_trade": 0.01,
        "min_leverage": 2,
        "max_leverage": 10,
        "max_notional_per_trade": 500,
        "max_total_exposure": 2000,
        "max_concurrent_positions": 3,
        "max_daily_loss": 100,
        "allow_short": True,
        "require_stop_loss": True,
        "require_take_profit": True,
        "min_reward_risk": 1.5,
        "cooldown_after_close_sec": 0,
        "minimum_hold_sec": 0,
        "gateway": {"enabled": False},
    }
    cfg.update(over)
    return cfg


def _run_patched_cycle(config_path, trade_loop_fn, monitor_result, trailing_result):
    orig = (runner.run_trade_loop, runner.run_position_monitor, runner.run_trailing_stops)
    runner.run_trade_loop = trade_loop_fn
    runner.run_position_monitor = lambda *a, **k: monitor_result
    runner.run_trailing_stops = lambda *a, **k: trailing_result
    try:
        with open(os.devnull, "w") as devnull:
            return runner.run_cycle(config_path, out=devnull)
    finally:
        (runner.run_trade_loop, runner.run_position_monitor,
         runner.run_trailing_stops) = orig


def check_breaker_symbol_errors_counted_once():
    """3 failing symbols -> counter 3, not 4 (no double count)."""
    def _boom(*a, **k):
        raise RuntimeError("scan boom")

    with tempfile.TemporaryDirectory() as d:
        cp = os.path.join(d, "config.json")
        json.dump(_sandbox_config(), open(cp, "w"))
        code = _run_patched_cycle(cp, _boom,
                                  {"closed": [], "errors": []},
                                  {"actions": [], "errors": []})
        state = json.load(open(os.path.join(d, "state.json")))
        assert code == 1, code
        assert state["consecutive_errors"] == 3, state["consecutive_errors"]


def check_breaker_trailing_errors_feed_counter():
    """Clean monitor + clean symbols + 1 trailing failure -> counter 1 (was: reset to 0)."""
    def _wait(*a, **k):
        return {"symbol": "ETH", "decision": "wait", "reason": "flat"}

    with tempfile.TemporaryDirectory() as d:
        cp = os.path.join(d, "config.json")
        json.dump(_sandbox_config(), open(cp, "w"))
        code = _run_patched_cycle(cp, _wait,
                                  {"closed": [], "errors": []},
                                  {"actions": [], "errors": ["ETH: no price"]})
        state = json.load(open(os.path.join(d, "state.json")))
        assert code == 1, code
        assert state["consecutive_errors"] == 1, state["consecutive_errors"]
        # a following clean cycle resets
        code = _run_patched_cycle(cp, _wait,
                                  {"closed": [], "errors": []},
                                  {"actions": [], "errors": []})
        state = json.load(open(os.path.join(d, "state.json")))
        assert code == 0, code
        assert state["consecutive_errors"] == 0, state["consecutive_errors"]


def check_halt_persists_without_signer_env():
    """live mode + cancel_all + missing LIGHTER_* env -> halt still lands."""
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "state.json")
        tp = os.path.join(d, "trades.json")
        json.dump({"halt": False, "circuit_breaker": False}, open(sp, "w"))
        cfg = {"mode": "live", "execution": {"cancel_on_halt": True},
               "gateway": {"enabled": False}}
        for k in ("LIGHTER_API_PRIVATE_KEY", "LIGHTER_API_KEY_INDEX", "LIGHTER_ACCOUNT_INDEX"):
            os.environ.pop(k, None)
        state = json.load(open(sp))
        res = halt_mod.halt(cfg, state, sp, tp, reason="harness", cancel_orders=True)
        saved = json.load(open(sp))
        assert saved["halt"] is True and saved["circuit_breaker"] is True, saved
        cancel = res["actions"]["cancel_all"]
        assert isinstance(cancel, dict) and "error" in cancel, cancel
        entries = journal_trade.load_journal(tp)
        assert entries and entries[-1]["decision"] == "halt_event", entries


def check_bracket_rollback_on_partial_failure():
    """entry ok, SL rejected, TP ok -> TP cancelled + reduce-only close issued."""
    calls = {"cancel": [], "close": []}
    ok_resp = types.SimpleNamespace(code=200, tx_hash="0xabc", message=None)

    def triple_ok(idx):
        return (types.SimpleNamespace(order_index=idx, tx_hash="0xabc"), ok_resp, None)

    async def fake_entry(client, lighter, mi, side, size, price, gateway=None):
        return triple_ok(111)

    async def fake_sl(client, lighter, mi, side, size, trig, gateway=None):
        return (None, None, "trigger too close")

    async def fake_tp(client, lighter, mi, side, size, trig, gateway=None):
        return triple_ok(333)

    async def fake_create_order(client, lighter, mi, side, size, price, **kw):
        calls["close"].append(kw)
        return triple_ok(444)

    class FakeClient:
        def sign_cancel_order(self, mi, oi):
            calls["cancel"].append((mi, oi))
            return (1, "{}", None, None)

        async def send_tx(self, tx_type=None, tx_info=None):
            return ok_resp

        async def close(self):
            pass

    orig = (signer._build_client, signer._create_entry, signer._create_sl,
            signer._create_tp, signer._create_order)
    signer._build_client = lambda creds, gateway=None: FakeClient()
    signer._create_entry, signer._create_sl, signer._create_tp = fake_entry, fake_sl, fake_tp
    signer._create_order = fake_create_order
    try:
        result = asyncio.run(signer._place_bracket({"private_key": "x"}, 1, "long",
                                                   100, 5000, 4000, 6000))
    finally:
        (signer._build_client, signer._create_entry, signer._create_sl,
         signer._create_tp, signer._create_order) = orig

    assert result["ok"] is False, result
    assert "rollback" in result, result
    assert calls["cancel"] == [(1, 333)], calls["cancel"]
    assert len(calls["close"]) == 1 and calls["close"][0].get("reduce_only") is True, calls["close"]
    assert result["rollback"]["close"]["ok"] is True, result["rollback"]


def check_journal_lock_cross_process():
    """2 concurrent cron-like processes x 40 appends -> all 80 entries survive."""
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "trades.json")
        worker = (
            "import sys; sys.path.insert(0, %r);"
            "import journal_trade;"
            "[journal_trade.journal_entry(%r, {'symbol': 'ETH', 'decision': 'wait'})"
            " for _ in range(40)]"
        ) % (SCRIPTS, jp)
        procs = [subprocess.Popen([sys.executable, "-c", worker]) for _ in range(2)]
        for p in procs:
            assert p.wait() == 0
        entries = journal_trade.load_journal(jp)
        assert len(entries) == 80, len(entries)


def check_lock_reentrant_same_process():
    """Nested held() in one process returns instead of deadlocking on flock."""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "state.json")
        with filelock.held(p):
            with filelock.held(p):
                pass


if __name__ == "__main__":
    checks = [v for k, v in sorted(globals().items())
              if k.startswith("check_") and callable(v)]
    for fn in checks:
        fn()
        print("ok -", fn.__name__)
    print("all %d checks passed" % len(checks))
