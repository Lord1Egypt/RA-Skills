#!/usr/bin/env python3
"""model_runner.py — one arena cycle for ONE model.

Each arena model gets its own account state (state.<model>.json) and journal
(trades.<model>.json) beside config.json. A cycle:

  1. global halt check (main state.json halt / circuit_breaker stops everyone)
  2. per-model lock -> load state -> position monitor closes finished trades
  3. build market context (features per allowed symbol) + account + positions
  4. prompt -> LLM -> parse_decision (garbage becomes hold)
  5. open: ATR fallback bracket -> size -> risk gates -> execute -> journal
     close: reduce-only close (live) / mark-to-market close (paper)
  6. every decision journaled with model id, reasoning and exit plan

Per-model venue credentials: model_cfg "env" maps canonical env names to
per-model env vars, e.g. {"LIGHTER_ACCOUNT_INDEX": "LIGHTER_ACCOUNT_INDEX_A"}
reads LIGHTER_ACCOUNT_INDEX_A and exposes it as LIGHTER_ACCOUNT_INDEX for the
duration of the cycle.

Module:  from model_runner import run_model_cycle
CLI:     python3 model_runner.py config.json --model claude
"""

import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import envfile                                     # noqa: E402

# auto-load per-model credentials from <skill>/.env (never config.json);
# vars already present in the process environment win
envfile.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import filelock                                     # noqa: E402
import journal_trade                                # noqa: E402
import llm_client                                   # noqa: E402
from autonomous_runner import ERROR_TRIP_THRESHOLD, _daily_reset, _save_state  # noqa: E402
from compute_features import compute_features       # noqa: E402
from decision_parser import parse_decision          # noqa: E402
from lighter_rest_client import LighterRestClient, LighterAPIError  # noqa: E402
from market_scan_from_lighter import build_bracket  # noqa: E402
from position_monitor import run_position_monitor, _close_position  # noqa: E402
from prepare_order import prepare_order             # noqa: E402
from prompt_builder import build_prompt             # noqa: E402
from risk_checks import risk_checks                 # noqa: E402
from live_execution_adapter import execute_order    # noqa: E402

CANDLE_TFS = {"5m": 60, "1h": 120, "4h": 60}

# A tripped circuit breaker auto-resets after this cooldown, so a transient
# LLM outage cannot sideline an arena agent forever.
CB_RESET_SEC = 900


def resolve_model_cfg(config, model_cfg):
    """Config-first defaults: arena.endpoint / arena.api_key_env fill in any
    model entry that omits base_url / api_key_env. Provider defaults to the
    OpenAI-compatible shape."""
    arena = config.get("arena") or {}
    m = dict(model_cfg)
    m.setdefault("provider", "openai")
    if not m.get("base_url") and arena.get("endpoint"):
        m["base_url"] = arena["endpoint"]
    if not m.get("api_key_env") and arena.get("api_key_env"):
        m["api_key_env"] = arena["api_key_env"]
    return m


def model_files(config_path, model_id):
    base = os.path.dirname(os.path.abspath(config_path))
    return (os.path.join(base, "state.%s.json" % model_id),
            os.path.join(base, "trades.%s.json" % model_id))


def _global_halted(config_path):
    main_state = os.path.join(os.path.dirname(os.path.abspath(config_path)), "state.json")
    if not os.path.exists(main_state):
        return False
    try:
        with open(main_state) as f:
            state = json.load(f)
    except (ValueError, OSError):
        return False
    return bool(state.get("halt") or state.get("circuit_breaker"))


def _load_model_state(state_path, start_equity):
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    else:
        state = {}
    account = state.setdefault("account", {})
    account.setdefault("equity", float(start_equity))
    account.setdefault("available_margin", account["equity"])
    account.setdefault("daily_pnl", 0.0)
    state.setdefault("known_open_positions", {})
    state.setdefault("consecutive_errors", 0)
    return state


def _apply_env_overrides(model_cfg):
    """model_cfg env mapping -> temporarily set os.environ. Returns restore fn."""
    originals = {}
    for canonical, source in (model_cfg.get("env") or {}).items():
        if source in os.environ:
            originals[canonical] = os.environ.get(canonical)
            os.environ[canonical] = os.environ[source]

    def restore():
        for name, old in originals.items():
            if old is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = old
    return restore


def _gather_features(config, client):
    """symbol -> {tf: features}. A timeframe with too little history is
    skipped on its own; the symbol is dropped only when NO timeframe works."""
    features, errors = {}, []
    for symbol in (config.get("allowed_symbols") or []):
        try:
            market = client.get_market(symbol)
            funding = client.get_funding_rate(market_id=market["market_id"])
            per_tf = {}
            for tf, count in CANDLE_TFS.items():
                try:
                    candles = client.get_candles(market["market_id"], tf, count)
                    per_tf[tf] = compute_features(candles, funding_rate=funding)
                except (LighterAPIError, ValueError, KeyError) as e:
                    errors.append("%s %s: %s" % (symbol, tf, e))
            if per_tf:
                features[symbol] = per_tf
        except (LighterAPIError, ValueError, KeyError) as e:
            errors.append("%s: %s" % (symbol, e))
    return features, errors


def _last_price(client, symbol):
    market = client.get_market(symbol)
    return market, (market.get("mark_price") or market.get("last_trade_price"))


def _journal(path, model_id, parsed, **extra):
    entry = {"model": model_id, "mode": extra.pop("mode", None),
             "symbol": parsed.get("symbol"), "confidence": parsed.get("confidence"),
             "llm_reasoning": parsed.get("reasoning"),
             "exit_plan": parsed.get("exit_plan")}
    entry.update(extra)
    return journal_trade.journal_entry(path, entry)


def _act_close(config, state, trades_path, model_id, decision, client):
    symbol = decision.get("symbol")
    positions = state.get("known_open_positions") or {}
    if not symbol and len(positions) == 1:
        symbol = next(iter(positions))
    pos = positions.get(symbol)
    if not pos:
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="close requested but no open position")
    market, last = _last_price(client, symbol)
    direction = 1 if pos.get("side") == "long" else -1
    pnl = (float(last) - float(pos["entry_price"])) * float(pos["quantity"]) * direction

    if config.get("mode") in ("live", "autonomous_live"):
        import lighter_signer
        from lighter_rest_client import to_int_price, to_int_size
        result = lighter_signer.close_position(
            market["market_id"], pos["side"],
            to_int_size(pos["quantity"], market["size_decimals"]),
            to_int_price(last, market["price_decimals"]),
            gateway=config.get("gateway"))
        if not result.get("ok"):
            return _journal(trades_path, model_id, decision, decision="error",
                            signal_reason="close order failed: %s" % result.get("error"))
        # ponytail: paper-fill at last price; exact fill comes from venue
        # reconciliation (position_monitor) on later cycles when needed.
    closed = _close_position(symbol, pos, float(last), pnl, "model_close",
                             state, trades_path)
    return {"closed": closed, "decision": "close"}


def _act_open(config, state, trades_path, model_id, decision, features, client):
    symbol = decision.get("symbol")
    side = "long" if decision["action"] == "open_long" else "short"
    if symbol in (state.get("known_open_positions") or {}):
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="already positioned in %s" % symbol)
    market, entry = _last_price(client, symbol)
    if not entry:
        return _journal(trades_path, model_id, decision, decision="error",
                        signal_reason="no price for %s" % symbol)

    sl, tp = decision.get("stop_loss"), decision.get("take_profit")
    if sl is None or tp is None:
        per_tf = features.get(symbol) or {}
        atr = next((per_tf[tf]["atr14"] for tf in ("1h", "5m", "4h")
                    if per_tf.get(tf) and per_tf[tf].get("atr14")), None)
        fb_sl, fb_tp = build_bracket(side, float(entry), atr)
        sl = sl or fb_sl
        tp = tp or fb_tp
    if sl is None or tp is None:
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="no bracket prices and no ATR fallback")

    account = state.get("account") or {}
    equity = float(account.get("equity") or 0)
    available = float(account.get("available_margin") or 0)
    confidence = max(0.0, min(1.0, float(decision.get("confidence") or 0)))
    # Arena sizing rule: margin = equity x (0.03 + 0.02 x confidence), i.e.
    # 3-5% of equity, floored at 1000 USD. Server-side so a hallucinated
    # size_usd cannot breach it. Leverage band 10-25 (decision_parser clamp).
    margin_usd = min(max(equity * (0.03 + 0.02 * confidence), 1000.0), available)
    leverage = int(decision.get("leverage") or config.get("min_leverage") or 10)
    notional = margin_usd * leverage
    if notional <= 0:
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="zero size (size band=%.2f, available=%.2f)"
                        % (max(equity * (0.03 + 0.02 * confidence), 1000.0), available))

    size_dec = int(market["size_decimals"])
    quantity = int((notional / float(entry)) * 10 ** size_dec) / 10 ** size_dec
    if quantity <= 0 or (market.get("min_base_amount") and
                         quantity < float(market["min_base_amount"])):
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="quantity below market minimum")
    if market.get("min_quote_amount") and quantity * float(entry) < float(market["min_quote_amount"]):
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="notional below market minimum")

    try:
        plan = prepare_order(symbol, side, entry, sl, tp, quantity, leverage,
                             market=market)
    except (ValueError, TypeError) as e:
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="bracket rejected: %s" % e)

    gates = risk_checks(config, state, plan, account=account)
    if not gates["ok"]:
        return _journal(trades_path, model_id, decision, decision="hold",
                        signal_reason="risk gates: %s" % ", ".join(gates["blocked_by"]),
                        confluence=gates)

    exec_result = execute_order(plan, config)
    if exec_result.get("status") not in ("executed", "simulated"):
        return _journal(trades_path, model_id, decision, decision="error",
                        signal_reason="execution %s: %s" % (exec_result.get("status"),
                                                            exec_result.get("error")),
                        exec_result=exec_result)

    state["known_open_positions"][symbol] = {
        "side": side, "quantity": plan["quantity"], "entry_price": plan["entry_price"],
        "stop_loss": plan["stop_loss"], "take_profit": plan["take_profit"],
        "leverage": plan["leverage"], "margin": plan["margin"],
        "opened_at": journal_trade.utcnow(),
        "order_indexes": exec_result.get("order_indexes"),
        "exit_plan": decision.get("exit_plan"),
    }
    account["available_margin"] = round(available - plan["margin"], 6)
    state["trades_today"] = int(state.get("trades_today", 0) or 0) + 1
    return _journal(trades_path, model_id, decision, decision="executed",
                    status="open", signal=side, signal_reason="model decision",
                    order=plan, exec_result=exec_result,
                    market={"last_price": entry})


def _fallback_candidates(config, features, model_id=""):
    """(symbol, action) ranked by |momentum| for the deterministic fallback
    entry that keeps every arena agent positioned when the model gives no
    usable signal (LLM down, unparseable reply, or repeated hold).

    Per-model rotation: each model starts from a different symbol (stable
    hash of model_id) so agents never pile onto one identical position.
    When every symbol's momentum points the same way, odd-hash models take
    the contrarian side on the weakest-momentum symbol — the arena board
    then always shows both directions."""
    ranked = []
    for symbol in (config.get("allowed_symbols") or []):
        per_tf = features.get(symbol) or {}
        f = per_tf.get("1h") or per_tf.get("5m") or per_tf.get("4h")
        if not f or f.get("momentum") is None:
            continue
        ranked.append((abs(f["momentum"]), f["momentum"], symbol))
    ranked.sort(reverse=True)
    cands = [(s, "open_long" if m >= 0 else "open_short") for _, m, s in ranked]
    if not cands or not model_id:
        return cands
    h = int(hashlib.md5(model_id.encode()).hexdigest(), 16)
    off = h % len(cands)
    cands = cands[off:] + cands[:off]
    if len(cands) > 1 and len({a for _, a in cands}) == 1 and h % 2:
        weak, act = cands[-1]
        flip = "open_short" if act == "open_long" else "open_long"
        cands = [(weak, flip)] + [c for c in cands if c[0] != weak]
    return cands


def _act_fallback(config, state, trades_path, model_id, features, client):
    """Try momentum-ranked symbols until one opens. All normal risk gates
    and bracket rules still apply via _act_open."""
    for symbol, action in _fallback_candidates(config, features, model_id):
        decision = {"action": action, "symbol": symbol, "confidence": 0.5,
                    "reasoning": "deterministic momentum fallback (no model signal)",
                    "exit_plan": "ATR bracket", "size_usd": 0.0,
                    "leverage": int(config.get("min_leverage") or 10),
                    "stop_loss": None, "take_profit": None}
        _act_open(config, state, trades_path, model_id, decision, features, client)
        if state.get("known_open_positions"):
            return True
    return False


def run_model_cycle(config, config_path, model_cfg, client=None, llm_fn=None,
                    out=sys.stdout):
    """One cycle for one model. Returns summary dict. Never raises."""
    model_cfg = resolve_model_cfg(config, model_cfg)
    model_id = model_cfg.get("id") or model_cfg.get("model") or "model"
    summary = {"model": model_id, "action": None, "errors": []}
    state_path, trades_path = model_files(config_path, model_id)

    if _global_halted(config_path):
        summary["action"] = "skipped_global_halt"
        print(json.dumps(summary), file=out)
        return summary

    restore_env = _apply_env_overrides(model_cfg)
    try:
        client = client or LighterRestClient(base_url=config.get("base_url"),
                                             gateway=config.get("gateway"),
                                             agent="arena-" + model_id)
        with filelock.held(state_path):
            arena = config.get("arena") or {}
            state = _load_model_state(state_path, arena.get("start_equity", 10000))
            _daily_reset(state)

            if state.get("halt") or state.get("circuit_breaker"):
                cb_since = float(state.get("cb_since") or 0)
                if (state.get("circuit_breaker") and not state.get("halt")
                        and time.time() - cb_since > CB_RESET_SEC):
                    # cooldown elapsed: clear the breaker and retry this cycle
                    state["circuit_breaker"] = False
                    state["consecutive_errors"] = 0
                    state.pop("cb_since", None)
                    summary["cb_reset"] = True
                else:
                    if state.get("circuit_breaker") and not cb_since:
                        state["cb_since"] = time.time()
                    summary["action"] = "skipped_model_halt"
                    _save_state(state_path, state)
                    print(json.dumps(summary), file=out)
                    return summary

            monitor = run_position_monitor(config, state, trades_path, client=client)
            summary["monitor"] = {"closed": [c["symbol"] for c in monitor["closed"]],
                                  "errors": monitor["errors"]}

            features, feat_errors = _gather_features(config, client)
            # Venue-side data gaps (thin candle history on new markets) are
            # warnings, not cycle failures: they must not feed the breaker.
            summary["data_warnings"] = feat_errors

            context = {"features": features,
                       "account": dict(state.get("account") or {},
                                       trades_today=state.get("trades_today", 0)),
                       "positions": state.get("known_open_positions"),
                       "config": config, "model_id": model_id}
            system, user = build_prompt(context)
            try:
                ask = llm_fn or (lambda s, u: llm_client.chat(model_cfg, s, u))
                raw = ask(system, user)
            except llm_client.LLMError as e:
                raw = None
                summary["errors"].append("llm: %s" % e)

            if raw is None:
                decision = {"action": "hold", "symbol": None, "confidence": 0.0,
                            "reasoning": "", "exit_plan": "", "size_usd": 0.0,
                            "leverage": 1, "stop_loss": None, "take_profit": None}
                _journal(trades_path, model_id, decision, decision="error",
                         signal_reason="llm call failed")
            else:
                decision = parse_decision(raw, config)
                action = decision["action"]
                summary["action"] = action
                if action in ("open_long", "open_short"):
                    _act_open(config, state, trades_path, model_id, decision,
                              features, client)
                elif action == "close":
                    _act_close(config, state, trades_path, model_id, decision, client)
                else:
                    reason = decision.get("parse_error") or "model hold"
                    _journal(trades_path, model_id, decision, decision="hold",
                             signal_reason=reason)

            # Arena rule: no agent sits flat. If nothing is open and the model
            # did not just close a position this cycle, enter on momentum.
            if not state.get("known_open_positions") and summary.get("action") != "close":
                if _act_fallback(config, state, trades_path, model_id, features, client):
                    summary["fallback"] = True
                    if not summary.get("action"):
                        summary["action"] = "fallback_open"

            had_errors = bool(summary["errors"] or summary["monitor"]["errors"])
            if had_errors:
                state["consecutive_errors"] = int(state.get("consecutive_errors", 0)) + 1
                if state["consecutive_errors"] >= ERROR_TRIP_THRESHOLD:
                    state["circuit_breaker"] = True
                    state["cb_since"] = time.time()
                    summary["circuit_breaker"] = "TRIPPED"
            else:
                state["consecutive_errors"] = 0
            _save_state(state_path, state)
    except Exception as e:  # model bugs must not kill the arena
        summary["errors"].append("cycle: %s: %s" % (type(e).__name__, e))
    finally:
        restore_env()
    print(json.dumps(summary, default=str), file=out)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run one arena model cycle")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--model", required=True, help="model id from arena.models")
    args = parser.parse_args(argv)
    with open(args.config) as f:
        config = json.load(f)
    models = {m.get("id"): m for m in (config.get("arena") or {}).get("models") or []}
    model_cfg = models.get(args.model)
    if not model_cfg:
        print(json.dumps({"error": "model %r not in arena.models" % args.model}))
        return 1
    summary = run_model_cycle(config, args.config, model_cfg)
    return 0 if not summary["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())
