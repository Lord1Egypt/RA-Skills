#!/usr/bin/env python3
"""halt.py — emergency stop (SPEC sections 5+7).

Sets halt=true AND circuit_breaker=true in state.json: every trading path
(autonomous_runner, trade_loop) refuses to run while either flag is set.

Options:
  --reason TEXT      recorded in the journal entry (default: manual halt)
  --cancel-orders    live modes: cancel ALL open orders via the signer
                     (default behavior follows execution.cancel_on_halt)
  --no-cancel        never cancel orders
  --flatten          also market-close every known position (dangerous;
                     requires execution.flatten_on_emergency_stop=true or
                     the extra --confirm-flatten flag)
Every halt is journaled to trades.json as a halt_event entry.

CLI: python3 halt.py config.json --reason "news event" --cancel-orders
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402
import filelock  # noqa: E402
from lighter_rest_client import LighterRestClient, to_int_size, to_int_price  # noqa: E402


def halt(config, state, state_path, trades_path, reason="manual halt",
         cancel_orders=None, flatten=False, confirm_flatten=False):
    state["halt"] = True
    state["circuit_breaker"] = True
    state["halted_at"] = journal_trade.utcnow()
    state["halt_reason"] = reason

    # Persist the flags FIRST: an emergency stop must land even when env
    # credentials, the SDK, or the venue are unreachable. Anything below can
    # fail (SystemExit included) without undoing the halt.
    tmp = state_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    os.replace(tmp, state_path)

    actions = {"cancel_all": None, "flatten": []}
    mode = config.get("mode", "paper")
    execution = config.get("execution") or {}
    if cancel_orders is None:
        cancel_orders = bool(execution.get("cancel_on_halt", True))

    if mode in ("live", "autonomous_live") and (cancel_orders or flatten):
        try:
            import lighter_signer
        except BaseException as e:  # missing env/SDK raises SystemExit
            lighter_signer = None
            actions["cancel_all"] = {"error": str(e)}
        gateway_cfg = config.get("gateway")
        if cancel_orders and lighter_signer is not None:
            try:
                actions["cancel_all"] = lighter_signer.cancel_all(gateway=gateway_cfg)
            except BaseException as e:  # halt already persisted; record and continue
                actions["cancel_all"] = {"error": str(e)}
        if flatten:
            if not (execution.get("flatten_on_emergency_stop") or confirm_flatten):
                actions["flatten"] = [{"skipped": "flatten_on_emergency_stop=false; "
                                       "pass --confirm-flatten to override"}]
            elif lighter_signer is None:
                actions["flatten"] = [{"error": "signer unavailable: %s" % actions["cancel_all"]}]
            else:
                client = LighterRestClient(base_url=config.get("base_url"),
                                           gateway=gateway_cfg)
                for symbol, pos in (state.get("known_open_positions") or {}).items():
                    try:
                        market = client.get_market(symbol)
                        last = market.get("mark_price") or market.get("last_trade_price") or pos["entry_price"]
                        res = lighter_signer.close_position(
                            market["market_id"], pos["side"],
                            to_int_size(pos["quantity"], market["size_decimals"]),
                            to_int_price(last, market["price_decimals"]),
                            gateway=gateway_cfg)
                        actions["flatten"].append({"symbol": symbol, "result": res})
                    except BaseException as e:  # halt must not crash mid-flatten
                        actions["flatten"].append({"symbol": symbol, "error": str(e)})

    journal_trade.journal_entry(trades_path, {
        "ts": state["halted_at"], "symbol": "*", "mode": mode,
        "decision": "halt_event", "signal": "halt", "signal_reason": reason,
        "status": "journaled",
        "exec_result": {"cancel_all": actions["cancel_all"], "flatten": actions["flatten"]},
    })

    return {"halt": True, "circuit_breaker": True, "reason": reason, "actions": actions}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Emergency stop: halt + circuit breaker")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
    parser.add_argument("--reason", default="manual halt")
    parser.add_argument("--cancel-orders", action="store_true", default=None)
    parser.add_argument("--no-cancel", action="store_true")
    parser.add_argument("--flatten", action="store_true")
    parser.add_argument("--confirm-flatten", action="store_true")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    cancel = False if args.no_cancel else (True if args.cancel_orders else None)
    # Lock across load->mutate->save so a concurrent cycle can't erase the halt.
    with filelock.held(state_path):
        state = {}
        if os.path.exists(state_path):
            with open(state_path) as f:
                state = json.load(f)
        result = halt(config, state, state_path, trades_path, reason=args.reason,
                      cancel_orders=cancel, flatten=args.flatten,
                      confirm_flatten=args.confirm_flatten)
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
