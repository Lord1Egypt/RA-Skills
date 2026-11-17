#!/usr/bin/env python3
"""Verification harness for the arena (multi-model) pipeline:

  1. decision_parser: prose/fenced/plain JSON, garbage -> hold, clamps
  2. prompt_builder: context lands in the user prompt, schema in the system
  3. llm_client: request shapes per provider against a local stub server
  4. model_runner: full paper cycle with fake LLM + fixture-backed client,
     including open -> journal -> state, model isolation, and global halt

Run: python3 tests/test_arena.py
Plain asserts, no framework. Sandboxes under /tmp; repo files untouched.
"""

import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import decision_parser           # noqa: E402
import prompt_builder            # noqa: E402
import llm_client                # noqa: E402
import model_runner              # noqa: E402
import journal_trade             # noqa: E402
import bot                       # noqa: E402
import arena_preflight           # noqa: E402
from autonomous_runner import OfflineClient  # noqa: E402


def _fixtures():
    """OfflineClient fixture dict: 40 rising candles for ETH on all TFs."""
    candles = []
    price = 3000.0
    for i in range(40):
        price += 5.0
        candles.append({"t": 1700000000000 + i * 3600000, "o": price - 5,
                        "h": price + 2, "l": price - 7, "c": price, "v": 10.0})
    return {"ETH": {
        "candles": {"5m": candles, "1h": candles, "4h": candles},
        "market": {"market_id": 1, "symbol": "ETH", "price_decimals": 2,
                   "size_decimals": 4, "last_trade_price": price,
                   "min_base_amount": 0.0001, "min_quote_amount": 1.0},
        "funding_rate": 0.0001,
    }}


def _arena_config(d, **over):
    cfg = {
        "mode": "paper",
        "base_url": "http://127.0.0.1:9",
        "allowed_symbols": ["ETH"],
        "risk_pct_per_trade": 0.01,
        "min_leverage": 1, "max_leverage": 10,
        "max_notional_per_trade": 5000,
        "max_total_exposure": 50000,
        "max_concurrent_positions": 3,
        "max_daily_loss": 1000,
        "allow_short": True,
        "require_stop_loss": True,
        "require_take_profit": True,
        "minimum_hold_sec": 0,
        "gateway": {"enabled": False},
        "arena": {"start_equity": 10000, "models": [
            {"id": "alpha", "provider": "anthropic", "model": "m1",
             "api_key_env": "UNUSED_KEY"},
            {"id": "beta", "provider": "openai", "model": "m2",
             "api_key_env": "UNUSED_KEY"},
        ]},
    }
    cfg.update(over)
    path = os.path.join(d, "config.json")
    json.dump(cfg, open(path, "w"))
    return path, cfg


# ------------------------------------------------------------- parser

def check_parser_plain_json():
    d = decision_parser.parse_decision(
        '{"action":"open_long","symbol":"ETH","confidence":0.8,"size_usd":500,'
        '"leverage":99,"stop_loss":2900,"take_profit":3200,"exit_plan":"e","reasoning":"r"}',
        config={"max_leverage": 10, "allowed_symbols": ["ETH"]})
    assert d["action"] == "open_long" and d["leverage"] == 10, d
    assert d["confidence"] == 0.8 and d["exit_plan"] == "e", d


def check_parser_fenced_and_prose():
    text = 'Sure! Here is my analysis.\n```json\n{"action":"close","symbol":"eth"}\n```\nHope that helps.'
    d = decision_parser.parse_decision(text, config={"allowed_symbols": ["ETH"]})
    assert d["action"] == "close" and d["symbol"] == "ETH", d


def check_parser_garbage_is_hold():
    for junk in ("", "no json here at all", '{"action":"nuke"}', '[1,2,3]',
                 '{"action":"open_long","symbol":"DOGE"}'):
        d = decision_parser.parse_decision(junk, config={"allowed_symbols": ["ETH"]})
        assert d["action"] == "hold", (junk, d)
    # aliases
    d = decision_parser.parse_decision('{"action":"buy","symbol":"ETH"}',
                                       config={"allowed_symbols": ["ETH"]})
    assert d["action"] == "open_long", d


# ------------------------------------------------------------- prompt

def check_prompt_builder():
    system, user = prompt_builder.build_prompt({
        "features": {"ETH": {"1h": {"last_price": 3200, "atr14": 25}}},
        "account": {"equity": 10000, "available_margin": 9000},
        "positions": {"ETH": {"side": "long", "quantity": 0.5, "entry_price": 3000}},
        "config": {"allowed_symbols": ["ETH"], "min_leverage": 1, "max_leverage": 10},
    })
    assert "open_long" in system and "exit_plan" in system, system
    assert "3200" in user and "10000" in user and "0.5" in user, user


# ------------------------------------------------------------- llm client

class _Stub(BaseHTTPRequestHandler):
    requests = []

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        _Stub.requests.append((self.path, dict(self.headers), json.loads(body)))
        if "generateContent" in self.path:
            out = {"candidates": [{"content": {"parts": [{"text": "gemini says hi"}]}}]}
        elif "messages" in self.path:
            out = {"content": [{"type": "text", "text": "anthropic says hi"}]}
        else:
            out = {"choices": [{"message": {"content": "openai says hi"}}]}
        data = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


def check_llm_client_shapes():
    srv = HTTPServer(("127.0.0.1", 0), _Stub)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_port
    os.environ["HARNESS_KEY"] = "k-123"
    try:
        out = llm_client.chat({"provider": "anthropic", "model": "m",
                               "api_key_env": "HARNESS_KEY", "base_url": base},
                              "sys", "usr")
        assert out == "anthropic says hi", out
        path, headers, body = _Stub.requests[-1]
        assert path == "/v1/messages" and headers.get("X-Api-Key") == "k-123", (path, headers)
        assert body["system"] == "sys" and body["messages"][0]["content"] == "usr", body

        out = llm_client.chat({"provider": "openai", "model": "m",
                               "api_key_env": "HARNESS_KEY", "base_url": base},
                              "sys", "usr")
        assert out == "openai says hi", out
        path, headers, body = _Stub.requests[-1]
        assert path == "/v1/chat/completions", path
        assert headers.get("Authorization") == "Bearer k-123", headers
        assert body["messages"][0]["role"] == "system", body

        out = llm_client.chat({"provider": "gemini", "model": "g",
                               "api_key_env": "HARNESS_KEY", "base_url": base},
                              "sys", "usr")
        assert out == "gemini says hi", out
        path, _, body = _Stub.requests[-1]
        assert "generateContent?key=k-123" in path, path
        assert body["systemInstruction"]["parts"][0]["text"] == "sys", body

        try:
            llm_client.chat({"provider": "openai", "model": "m",
                             "api_key_env": "DEFINITELY_MISSING", "base_url": base},
                            "s", "u")
            raise AssertionError("missing key must raise")
        except llm_client.LLMError:
            pass
    finally:
        srv.shutdown()


# ------------------------------------------------------------- model runner

def check_model_runner_paper_cycle():
    with tempfile.TemporaryDirectory() as d:
        config_path, config = _arena_config(d)
        model_cfg = config["arena"]["models"][0]
        client = OfflineClient(_fixtures())
        llm = lambda s, u: json.dumps({
            "action": "open_long", "symbol": "ETH", "confidence": 0.9,
            "size_usd": 500, "leverage": 4, "reasoning": "uptrend",
            "exit_plan": "close on 1h close below EMA21"})
        import io
        summary = model_runner.run_model_cycle(config, config_path, model_cfg,
                                               client=client, llm_fn=llm,
                                               out=io.StringIO())
        assert summary["action"] == "open_long", summary
        assert not summary["errors"], summary

        state = json.load(open(os.path.join(d, "state.alpha.json")))
        pos = state["known_open_positions"]["ETH"]
        assert pos["side"] == "long" and pos["leverage"] == 4, pos
        assert pos["exit_plan"].startswith("close on"), pos
        assert pos["stop_loss"] < pos["entry_price"] < pos["take_profit"], pos
        assert state["account"]["available_margin"] < 10000, state["account"]

        journal = journal_trade.load_journal(os.path.join(d, "trades.alpha.json"))
        executed = [e for e in journal if e["decision"] == "executed"]
        assert len(executed) == 1, journal
        assert executed[0]["model"] == "alpha", executed[0]
        assert executed[0]["llm_reasoning"] == "uptrend", executed[0]
        assert "beta" not in json.dumps(journal), "model isolation broken"


def check_model_runner_close_cycle():
    with tempfile.TemporaryDirectory() as d:
        config_path, config = _arena_config(d)
        model_cfg = config["arena"]["models"][0]
        client = OfflineClient(_fixtures())
        import io
        model_runner.run_model_cycle(config, config_path, model_cfg, client=client,
                                     llm_fn=lambda s, u: json.dumps({
                                         "action": "open_long", "symbol": "ETH",
                                         "size_usd": 500, "leverage": 2}),
                                     out=io.StringIO())
        # second cycle: model closes
        model_runner.run_model_cycle(config, config_path, model_cfg, client=client,
                                     llm_fn=lambda s, u: json.dumps({
                                         "action": "close", "symbol": "ETH",
                                         "reasoning": "target zone"}),
                                     out=io.StringIO())
        state = json.load(open(os.path.join(d, "state.alpha.json")))
        assert not state["known_open_positions"], state["known_open_positions"]
        journal = journal_trade.load_journal(os.path.join(d, "trades.alpha.json"))
        closed = [e for e in journal if e.get("status") == "closed"]
        assert closed and closed[0]["close_reason"] == "model_close", closed


def check_model_runner_global_halt():
    with tempfile.TemporaryDirectory() as d:
        config_path, config = _arena_config(d)
        json.dump({"halt": True}, open(os.path.join(d, "state.json"), "w"))
        import io
        summary = model_runner.run_model_cycle(config, config_path,
                                               config["arena"]["models"][0],
                                               client=OfflineClient(_fixtures()),
                                               llm_fn=lambda s, u: "{}", out=io.StringIO())
        assert summary["action"] == "skipped_global_halt", summary
        assert not os.path.exists(os.path.join(d, "trades.alpha.json"))


def check_model_runner_llm_failure_journals_error():
    with tempfile.TemporaryDirectory() as d:
        config_path, config = _arena_config(d)
        os.environ.pop("UNUSED_KEY", None)
        import io
        summary = model_runner.run_model_cycle(config, config_path,
                                               config["arena"]["models"][0],
                                               client=OfflineClient(_fixtures()),
                                               out=io.StringIO())  # real llm path, no key
        assert any("llm:" in e for e in summary["errors"]), summary
        journal = journal_trade.load_journal(os.path.join(d, "trades.alpha.json"))
        assert journal[-1]["decision"] == "error", journal
        state = json.load(open(os.path.join(d, "state.alpha.json")))
        assert state["consecutive_errors"] == 1, state


# ------------------------------------------------------------- bot

def check_bot_parse_models():
    models = bot.parse_models("alpha=gpt-5, beta:MY_KEY=deepseek-chat", "SHARED_KEY")
    assert models[0] == {"id": "alpha", "provider": "openai", "model": "gpt-5",
                         "api_key_env": "SHARED_KEY"}, models
    assert models[1]["api_key_env"] == "MY_KEY" and models[1]["model"] == "deepseek-chat", models
    for bad in ("", "noid", "=model"):
        try:
            bot.parse_models(bad, "K")
            raise AssertionError("bad spec %r must raise" % bad)
        except ValueError:
            pass


def check_resolve_model_cfg_from_config():
    """arena.endpoint / arena.api_key_env fill sparse model entries."""
    config = {"arena": {"endpoint": "https://llm.example", "api_key_env": "SHARED"}}
    m = model_runner.resolve_model_cfg(config, {"id": "a", "model": "gpt-5"})
    assert m["base_url"] == "https://llm.example" and m["api_key_env"] == "SHARED", m
    assert m["provider"] == "openai", m
    # explicit per-model values win over the arena defaults
    m = model_runner.resolve_model_cfg(config, {
        "id": "b", "model": "x", "provider": "anthropic",
        "base_url": "https://other.example", "api_key_env": "OWN"})
    assert m["base_url"] == "https://other.example" and m["api_key_env"] == "OWN", m
    assert m["provider"] == "anthropic", m


def check_arena_preflight_readiness():
    """1-1-1: per-model env-map credentials resolve; missing env -> NOT READY."""
    with tempfile.TemporaryDirectory() as td:
        cfg_path = os.path.join(td, "config.json")
        with open(cfg_path, "w") as f:
            json.dump({"mode": "paper", "arena": {
                "endpoint": "https://llm.example", "api_key_env": "PFX_LLM",
                "models": [
                    {"id": "one", "model": "m1",
                     "env": {"LIGHTER_API_PRIVATE_KEY": "PFX_PK_ONE",
                             "LIGHTER_API_KEY_INDEX": "PFX_KI_ONE",
                             "LIGHTER_ACCOUNT_INDEX": "PFX_AI_ONE"}},
                    {"id": "two", "model": "m2"}]}}, f)
        for var, val in (("PFX_LLM", "k"), ("PFX_PK_ONE", "pk"),
                         ("PFX_KI_ONE", "1"), ("PFX_AI_ONE", "7")):
            os.environ[var] = val
        try:
            report = arena_preflight.run_preflight(cfg_path)
        finally:
            for var in ("PFX_LLM", "PFX_PK_ONE", "PFX_KI_ONE", "PFX_AI_ONE"):
                os.environ.pop(var, None)
    rows = {r["model"]: r for r in report["models"]}
    assert rows["one"]["ready"], rows["one"]
    assert rows["one"]["account"]["LIGHTER_API_PRIVATE_KEY"]["via"] == "PFX_PK_ONE"
    assert not rows["two"]["ready"], rows["two"]
    assert any("LIGHTER_API_PRIVATE_KEY" in p for p in rows["two"]["problems"])
    assert not report["all_ready"]


class _StubVenueAndLLM(BaseHTTPRequestHandler):
    """One port, both sides: GET /api/v1/* = venue, POST /v1/* = OpenAI-shape LLM."""

    def _send(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        candles = []
        price = 3000.0
        for i in range(60):
            price += 5.0
            candles.append({"t": 1700000000000 + i * 3600000, "o": price - 5,
                            "h": price + 2, "l": price - 7, "c": price, "v": 10.0})
        if self.path.startswith("/api/v1/orderBookDetails"):
            self._send({"order_book_details": [{
                "symbol": "ETH", "market_id": 1, "price_decimals": 2,
                "size_decimals": 4, "min_base_amount": 0.0001,
                "min_quote_amount": 1.0, "last_trade_price": price,
                "mark_price": price}]})
        elif self.path.startswith("/api/v1/candles"):
            self._send({"c": candles})
        elif self.path.startswith("/api/v1/funding-rates"):
            self._send({"funding_rates": [{"market_id": 1, "symbol": "ETH",
                                           "exchange": "lighter", "rate": 0.0001}]})
        else:
            self._send({})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(length)
        self._send({"choices": [{"message": {"content": json.dumps({
            "action": "open_long", "symbol": "ETH", "confidence": 0.85,
            "size_usd": 400, "leverage": 3,
            "reasoning": "stub model: steady uptrend on all timeframes",
            "exit_plan": "close when 1h closes below EMA21"})}}]})

    def log_message(self, *a):
        pass


def check_bot_end_to_end_once():
    """bot --once, config-first: endpoint+models in config.json -> journaled trade."""
    srv = HTTPServer(("127.0.0.1", 0), _StubVenueAndLLM)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_port
    os.environ["STUB_KEY"] = "k-1"
    try:
        with tempfile.TemporaryDirectory() as d:
            config_path = os.path.join(d, "config.json")
            json.dump({"mode": "paper", "base_url": base, "allowed_symbols": ["ETH"],
                       "min_leverage": 1, "max_leverage": 10,
                       "max_notional_per_trade": 5000, "max_total_exposure": 50000,
                       "max_daily_loss": 1000, "allow_short": True,
                       "require_stop_loss": True, "require_take_profit": True,
                       "minimum_hold_sec": 0, "gateway": {"enabled": False},
                       "arena": {"endpoint": base, "api_key_env": "STUB_KEY",
                                 "start_equity": 10000,
                                 "models": [{"id": "alpha", "model": "gpt-stub"}]}},
                      open(config_path, "w"))
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = bot.main(["--config", config_path, "--once"])
            assert code == 0, buf.getvalue()

            state = json.load(open(os.path.join(d, "state.alpha.json")))
            pos = state["known_open_positions"]["ETH"]
            assert pos["side"] == "long" and pos["leverage"] == 3, pos
            journal = journal_trade.load_journal(os.path.join(d, "trades.alpha.json"))
            executed = [e for e in journal if e["decision"] == "executed"]
            assert len(executed) == 1, journal
            assert executed[0]["llm_reasoning"].startswith("stub model"), executed[0]
            assert executed[0]["exit_plan"], executed[0]
    finally:
        srv.shutdown()


def check_bot_cli_merge_still_works():
    """--models/--endpoint rewrite the arena block (override path)."""
    with tempfile.TemporaryDirectory() as d:
        config_path = os.path.join(d, "config.json")
        json.dump({"mode": "paper"}, open(config_path, "w"))
        config = bot.apply_models(
            config_path, bot.parse_models("alpha=gpt-5", "K"),
            endpoint="https://llm.example/")
        m = config["arena"]["models"][0]
        assert m["base_url"] == "https://llm.example" and m["model"] == "gpt-5", m
        assert config["arena"]["start_equity"] == 10000, config["arena"]
        assert json.load(open(config_path))["arena"]["models"], "not persisted"


if __name__ == "__main__":
    checks = [v for k, v in sorted(globals().items())
              if k.startswith("check_") and callable(v)]
    for fn in checks:
        fn()
        print("ok -", fn.__name__)
    print("all %d checks passed" % len(checks))
