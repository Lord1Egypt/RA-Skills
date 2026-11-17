#!/usr/bin/env python3
"""lighter_signer.py — signing + order writes via the official Lighter SDK.

The `lighter` package (pip install lighter-sdk) is imported LAZILY inside
functions so paper mode never needs it. If it is missing you get a clear
install hint, not a traceback.

Credentials come from environment variables ONLY:
  LIGHTER_API_PRIVATE_KEY   API key private key (hex, 0x prefix optional)
  LIGHTER_API_KEY_INDEX     integer, 2-254
  LIGHTER_ACCOUNT_INDEX     integer account index
  LIGHTER_BASE_URL          optional base URL override

Verified SDK surface (lighter-python @ commit 7d27964, 2026-09 — pinned in
requirements.txt; PyPI builds ship an outdated native signer that rejects the
venue's current perp market ids):
  SignerClient(url, account_index, api_private_keys={idx: key})  # chain_id auto
  client.create_auth_token_with_expiry(deadline=3600) -> (auth, err)
  client.sign_create_order(...) / sign_cancel_order / sign_cancel_all_orders
      -> (tx_type, tx_info, tx_hash, err)          # sign WITHOUT sending
  Constants: ORDER_TYPE_MARKET, ORDER_TYPE_STOP_LOSS, ORDER_TYPE_TAKE_PROFIT,
             ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL, DEFAULT_IOC_EXPIRY (=0),
             DEFAULT_28_DAY_ORDER_EXPIRY (=-1), NIL_TRIGGER_PRICE (=0)
             — module-level on old SDKs, SignerClient class attrs on new ones
             (hoisted by _require_sdk). client_order_index must be <= 2**48-1;
             CANCEL_ALL_TIF_IMMEDIATE requires cancel-all time = 0.

Gateway mode (SPEC section 8C): pass the config "gateway" dict to any write
function. Signing stays LOCAL (SDK + env keys — the exchange private key never
leaves this host). In gateway mode the SignerClient is initialized with
url=gateway.url, so the SDK's own HTTP traffic (nonce reads, auth-token creation,
sendTx submission) is sent to the swarm-arena-backend, which proxies /api/v1/*
verbatim to the upstream venue and records every sendTx to its order journal
(data/orders.jsonl). Unreachable gateway with required=true: the cycle fails
cleanly and the circuit breaker counts it; required=false: warns and points the
SDK directly at the venue.

All public functions are SYNCHRONOUS (asyncio.run wrappers) so cron CLI
scripts stay simple. Prices/sizes must already be wire INTEGERS — convert with
lighter_rest_client.to_int_price / to_int_size first.
"""

import argparse
import asyncio
import json
import os
import random
import sys
import time
import types
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lighter_rest_client import LighterAPIError  # noqa: E402  (shared error class)

INSTALL_HINT = (
    "the 'lighter' SDK is not installed. Run: pip install lighter-sdk\n"
    "(lighter-sdk bundles the native signer library; it is only needed for "
    "live / autonomous_live modes — paper mode is stdlib-only.)"
)

AUTH_TOKEN_TTL_SEC = 3600


def _require_sdk():
    try:
        import lighter  # noqa: PLC0415
    except ImportError:
        raise SystemExit("error: " + INSTALL_HINT)
    # SDK layout compat: order-type/TIF constants are module-level on older
    # builds and SignerClient class attributes on newer ones. Hoist them so the
    # rest of this module can always use lighter.CONST.
    if not hasattr(lighter, "ORDER_TYPE_MARKET") and hasattr(lighter, "SignerClient"):
        for name in ("ORDER_TYPE_MARKET", "ORDER_TYPE_STOP_LOSS", "ORDER_TYPE_TAKE_PROFIT",
                     "ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL", "DEFAULT_IOC_EXPIRY",
                     "DEFAULT_28_DAY_ORDER_EXPIRY", "NIL_TRIGGER_PRICE",
                     "CANCEL_ALL_TIF_IMMEDIATE"):
            setattr(lighter, name, getattr(lighter.SignerClient, name))
    return lighter


def _credentials(require_key=True):
    """Read credentials from env. Never logs full secrets."""
    private_key = os.environ.get("LIGHTER_API_PRIVATE_KEY")
    key_index_raw = os.environ.get("LIGHTER_API_KEY_INDEX")
    account_index_raw = os.environ.get("LIGHTER_ACCOUNT_INDEX")
    missing = []
    if require_key and not private_key:
        missing.append("LIGHTER_API_PRIVATE_KEY")
    if not key_index_raw:
        missing.append("LIGHTER_API_KEY_INDEX")
    if not account_index_raw:
        missing.append("LIGHTER_ACCOUNT_INDEX")
    if missing:
        raise SystemExit("error: missing environment variables: %s" % ", ".join(missing))
    return {
        "private_key": private_key,
        "api_key_index": int(key_index_raw) if key_index_raw else None,
        "account_index": int(account_index_raw) if account_index_raw else None,
        "base_url": os.environ.get("LIGHTER_BASE_URL"),
    }


def mask_secret(value):
    """Mask a secret for logs: last 4 chars only."""
    if not value:
        return "<unset>"
    value = str(value)
    return "...%s" % value[-4:] if len(value) > 4 else "...%s" % value


def new_client_order_index():
    """Unique positive order index within the venue's 2**48-1 bound
    (time-based ms prefix + random tail; ~1.8e14 today, headroom to ~2035)."""
    return int(time.time() * 1000) * 100 + random.randint(0, 99)


def _gateway_active(gateway):
    return isinstance(gateway, dict) and bool(gateway.get("enabled")) and gateway.get("url")


def _resolve_sdk_url(creds, gateway):
    """Pick the SignerClient base URL.

    Gateway mode: the backend's URL — its /api/v1/* transparent proxy forwards
    SDK traffic upstream and journals sendTx calls. Probes the backend /api/health
    once for the required=false fallback. Direct mode: the venue base URL.
    """
    if not _gateway_active(gateway):
        url = creds.get("base_url")
        if not url:
            raise SystemExit("error: base URL required (config base_url or LIGHTER_BASE_URL)")
        return url
    gw_url = str(gateway["url"]).rstrip("/")
    if not gateway.get("required", True):
        try:
            req = urllib.request.Request(gw_url + "/api/health", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                resp.read(64)
        except Exception:
            print("warning: gateway unreachable; SDK traffic goes directly to the venue",
                  file=sys.stderr)
            url = creds.get("base_url")
            if not url:
                raise SystemExit("error: base URL required for direct fallback "
                                 "(config base_url or LIGHTER_BASE_URL)")
            return url
    return gw_url


def _gateway_chain_id(gateway):
    """Ask the backend which L2 signing chain id the upstream venue uses.

    The SDK derives the signing domain from its own URL; in gateway mode that
    URL is the backend (loopback), so derivation would silently pick the wrong
    chain. The backend reports the real signing chain on the agent-gated
    /gw/chain_id; /api/health is the unauthenticated fallback.
    Returns None when unknown (SDK then falls back to its own derivation).
    """
    base = str(gateway["url"]).rstrip("/")
    token = os.environ.get(gateway.get("token_env", "MANTIS_AGENT_TOKEN"), "")
    attempts = [("/gw/chain_id", {"Authorization": "Bearer " + token} if token else {}),
                ("/api/health", {})]
    for path, extra in attempts:
        try:
            req = urllib.request.Request(base + path, method="GET",
                                         headers={"Accept": "application/json", **extra})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace") or "{}")
        except Exception:
            continue
        inner = data.get("data") if isinstance(data.get("data"), dict) else data
        chain_id = inner.get("chain_id")
        if isinstance(chain_id, (int, float)) and chain_id:
            return int(chain_id)
    return None


def _build_client(creds=None, gateway=None):
    lighter = _require_sdk()
    creds = creds or _credentials()
    url = _resolve_sdk_url(creds, gateway)
    kwargs = {}
    if _gateway_active(gateway):
        chain_id = _gateway_chain_id(gateway)
        if chain_id:
            kwargs["chain_id"] = chain_id
    try:
        return lighter.SignerClient(
            url=url,
            account_index=creds["account_index"],
            api_private_keys={creds["api_key_index"]: creds["private_key"]},
            **kwargs,
        )
    except TypeError:
        # older SDK without the chain_id kwarg
        kwargs.pop("chain_id", None)
        return lighter.SignerClient(
            url=url,
            account_index=creds["account_index"],
            api_private_keys={creds["api_key_index"]: creds["private_key"]},
        )


def mint_auth_token(deadline=AUTH_TOKEN_TTL_SEC, creds=None, gateway=None):
    """Mint a REST/WS auth token. Returns the token string."""
    client = _build_client(creds, gateway)
    auth, err = client.create_auth_token_with_expiry(deadline=deadline)
    if err:
        raise SystemExit("error: auth token minting failed: %s" % err)
    return auth


# --------------------------------------------------------------- tx delivery

async def _deliver(client, signed, order_index):
    """Turn a (tx_type, tx_info, tx_hash, err) sign_* result into a sent tx.

    The client's base URL already encodes the routing decision (backend gateway
    proxy in gateway mode, direct venue otherwise). Returns the (tx, resp, err)
    triple shape used by _check_response.
    """
    tx_type, tx_info, tx_hash, err = signed
    if err:
        return None, None, err
    tx = types.SimpleNamespace(order_index=order_index, tx_hash=tx_hash)
    resp = await client.send_tx(tx_type=tx_type, tx_info=tx_info)
    return tx, resp, None


def _check_response(tag, triple):
    """Normalize an SDK-style (tx, resp, err) triple into a result dict."""
    tx, resp, err = triple
    if err:
        return {"ok": False, "stage": tag, "error": str(err)}
    code = getattr(resp, "code", None)
    if code is not None and code != 200:
        return {"ok": False, "stage": tag, "error": "venue code %s" % code,
                "message": getattr(resp, "message", None)}
    order_index = getattr(tx, "order_index", None) or getattr(tx, "client_order_index", None)
    tx_hash = getattr(resp, "tx_hash", None) or getattr(tx, "tx_hash", None)
    return {"ok": True, "stage": tag, "order_index": order_index, "tx_hash": tx_hash}


# --------------------------------------------------------------- order paths

def _client_order_index_from_tx_info(tx_info):
    try:
        return json.loads(tx_info).get("ClientOrderIndex")
    except (TypeError, ValueError):
        return None


async def _sign_order(client, lighter, market_index, side, size_int, price_int,
                      order_type, reduce_only, trigger_price_int=None,
                      time_in_force=None, order_expiry=None):
    """Sign an order without sending. Returns (signed, client_order_index)."""
    is_ask = side.lower() in ("short", "sell", "ask")
    if time_in_force is None:
        time_in_force = lighter.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL
    if order_expiry is None:
        order_expiry = lighter.DEFAULT_28_DAY_ORDER_EXPIRY
    coi = new_client_order_index()
    signed = client.sign_create_order(
        int(market_index), coi, int(size_int), int(price_int), int(is_ask),
        order_type, time_in_force, bool(reduce_only),
        int(trigger_price_int) if trigger_price_int else lighter.NIL_TRIGGER_PRICE,
        order_expiry,
    )
    if signed[3] is None and signed[1]:
        coi = _client_order_index_from_tx_info(signed[1]) or coi
    return signed, coi


async def _create_order(client, lighter, market_index, side, size_int, price_int,
                        order_type, reduce_only, trigger_price_int=None,
                        time_in_force=None, order_expiry=None, gateway=None):
    signed, coi = await _sign_order(client, lighter, market_index, side, size_int,
                                    price_int, order_type, reduce_only,
                                    trigger_price_int, time_in_force, order_expiry)
    return await _deliver(client, signed, coi)


async def _create_entry(client, lighter, market_index, side, size_int, price_int,
                        gateway=None):
    """Entry: MARKET + IOC with the venue's IOC expiry."""
    return await _create_order(
        client, lighter, market_index, side, size_int, price_int,
        order_type=lighter.ORDER_TYPE_MARKET,
        reduce_only=False,
        time_in_force=lighter.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
        order_expiry=lighter.DEFAULT_IOC_EXPIRY,
        gateway=gateway,
    )


async def _create_sl(client, lighter, market_index, side, size_int, trigger_int,
                     gateway=None):
    """Protective stop: STOP_LOSS + trigger_price + reduce_only. Exits invert the side."""
    close_side = "short" if side.lower() == "long" else "long"
    return await _create_order(
        client, lighter, market_index, close_side, size_int, trigger_int,
        order_type=lighter.ORDER_TYPE_STOP_LOSS,
        reduce_only=True, trigger_price_int=trigger_int,
        order_expiry=lighter.DEFAULT_28_DAY_ORDER_EXPIRY,
        gateway=gateway,
    )


async def _create_tp(client, lighter, market_index, side, size_int, trigger_int,
                     gateway=None):
    """Take profit: TAKE_PROFIT + trigger_price + reduce_only."""
    close_side = "short" if side.lower() == "long" else "long"
    return await _create_order(
        client, lighter, market_index, close_side, size_int, trigger_int,
        order_type=lighter.ORDER_TYPE_TAKE_PROFIT,
        reduce_only=True, trigger_price_int=trigger_int,
        order_expiry=lighter.DEFAULT_28_DAY_ORDER_EXPIRY,
        gateway=gateway,
    )


async def _rollback_entry(client, lighter, market_index, side, size_int,
                          price_int, order_indexes, gateway=None):
    """Best-effort undo of a partially placed bracket. Cancels any SL/TP leg
    that did place, then market-closes whatever the entry filled — the close
    is reduce-only, so a non-filled IOC entry closes nothing. Never raises:
    the original bracket error must not be masked by the cleanup."""
    out = {"cancelled": {}, "close": None, "errors": []}
    for leg in ("sl", "tp"):
        idx = order_indexes.get(leg)
        if idx is None:
            continue
        try:
            signed = client.sign_cancel_order(int(market_index), int(idx))
            res = _check_response("cancel", await _deliver(client, signed, int(idx)))
            out["cancelled"][leg] = res.get("ok", False)
            if not res.get("ok"):
                out["errors"].append("cancel %s: %s" % (leg, res.get("error")))
        except Exception as e:  # noqa: BLE001 - rollback continues past leg errors
            out["errors"].append("cancel %s: %s" % (leg, e))
    try:
        close_side = "short" if side.lower() == "long" else "long"
        triple = await _create_order(
            client, lighter, market_index, close_side, size_int, price_int,
            order_type=lighter.ORDER_TYPE_MARKET, reduce_only=True,
            time_in_force=lighter.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
            order_expiry=lighter.DEFAULT_IOC_EXPIRY, gateway=gateway)
        close = _check_response("close_position", triple)
        out["close"] = close
        if not close.get("ok"):
            out["errors"].append("close: %s" % close.get("error"))
    except Exception as e:  # noqa: BLE001 - reported, not raised
        out["errors"].append("close: %s" % e)
    return out


async def _place_bracket(creds, market_index, side, size_int, entry_price_int,
                         sl_trigger_int, tp_trigger_int, gateway=None):
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    try:
        entry = _check_response("entry", await _create_entry(
            client, lighter, market_index, side, size_int, entry_price_int, gateway))
        result = {"ok": entry["ok"], "entry": entry, "stop_loss": None,
                  "take_profit": None, "order_indexes": {"entry": entry.get("order_index")}}
        if not entry["ok"]:
            return result
        sl = _check_response("stop_loss", await _create_sl(
            client, lighter, market_index, side, size_int, sl_trigger_int, gateway))
        result["stop_loss"] = sl
        result["order_indexes"]["sl"] = sl.get("order_index")
        tp = _check_response("take_profit", await _create_tp(
            client, lighter, market_index, side, size_int, tp_trigger_int, gateway))
        result["take_profit"] = tp
        result["order_indexes"]["tp"] = tp.get("order_index")
        result["ok"] = entry["ok"] and sl["ok"] and tp["ok"]
        if not result["ok"]:
            result["error"] = "bracket partially failed: %s" % json.dumps(
                {k: v.get("error") for k, v in
                 (("entry", entry), ("stop_loss", sl), ("take_profit", tp)) if not v["ok"]})
            # Never leave a naked position: cancel placed legs, close the entry.
            result["rollback"] = await _rollback_entry(
                client, lighter, market_index, side, size_int, entry_price_int,
                result["order_indexes"], gateway)
        return result
    finally:
        await client.close()


async def _cancel_order(creds, market_index, order_index, gateway=None):
    lighter = _require_sdk()  # noqa: F841 (ensures a clear install error first)
    client = _build_client(creds, gateway)
    try:
        signed = client.sign_cancel_order(int(market_index), int(order_index))
        return _check_response("cancel", await _deliver(client, signed,
                                                        int(order_index)))
    finally:
        await client.close()


async def _cancel_all(creds, gateway=None):
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    try:
        # TIF IMMEDIATE requires a nil cancel-all time (native signer validation).
        signed = client.sign_cancel_all_orders(lighter.CANCEL_ALL_TIF_IMMEDIATE, 0)
        return _check_response("cancel_all", await _deliver(client, signed, None))
    finally:
        await client.close()


async def _close_position(creds, market_index, side, size_int, price_int, gateway=None):
    """Market-close an open position (reduce-only IOC in the exit direction)."""
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    try:
        close_side = "short" if side.lower() == "long" else "long"
        triple = await _create_order(
            client, lighter, market_index, close_side, size_int, price_int,
            order_type=lighter.ORDER_TYPE_MARKET, reduce_only=True,
            time_in_force=lighter.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
            order_expiry=lighter.DEFAULT_IOC_EXPIRY, gateway=gateway)
        return _check_response("close_position", triple)
    finally:
        await client.close()


# ------------------------------------------------------- sync public wrappers

def create_entry_order(market_index, side, size_int, price_int, creds=None, gateway=None):
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    async def run():
        try:
            return _check_response("entry", await _create_entry(
                client, lighter, market_index, side, size_int, price_int, gateway))
        finally:
            await client.close()
    return asyncio.run(run())


def create_stop_loss(market_index, side, size_int, trigger_int, creds=None, gateway=None):
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    async def run():
        try:
            return _check_response("stop_loss", await _create_sl(
                client, lighter, market_index, side, size_int, trigger_int, gateway))
        finally:
            await client.close()
    return asyncio.run(run())


def create_take_profit(market_index, side, size_int, trigger_int, creds=None, gateway=None):
    lighter = _require_sdk()
    client = _build_client(creds, gateway)
    async def run():
        try:
            return _check_response("take_profit", await _create_tp(
                client, lighter, market_index, side, size_int, trigger_int, gateway))
        finally:
            await client.close()
    return asyncio.run(run())


def place_bracket(market_index, side, size_int, entry_price_int,
                  sl_trigger_int, tp_trigger_int, creds=None, gateway=None):
    """Entry MARKET(IOC) + reduce-only STOP_LOSS + reduce-only TAKE_PROFIT."""
    return asyncio.run(_place_bracket(creds or _credentials(), market_index, side,
                                      size_int, entry_price_int, sl_trigger_int,
                                      tp_trigger_int, gateway))


def cancel_order(market_index, order_index, creds=None, gateway=None):
    return asyncio.run(_cancel_order(creds or _credentials(), market_index, order_index,
                                     gateway))


def cancel_all(creds=None, gateway=None):
    return asyncio.run(_cancel_all(creds or _credentials(), gateway))


def close_position(market_index, side, size_int, price_int, creds=None, gateway=None):
    return asyncio.run(_close_position(creds or _credentials(), market_index, side,
                                       size_int, price_int, gateway))


# ------------------------------------------------------------------------ CLI

def main(argv=None):
    parser = argparse.ArgumentParser(description="Lighter order signing/execution (SDK wrapper)")
    parser.add_argument("--gateway-config", default=None,
                        help="config.json whose gateway block routes SDK traffic through the backend")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("auth", help="mint an auth token and print it")
    p = sub.add_parser("bracket", help="place entry+SL+TP bracket")
    for name in ("market_index", "side", "size_int", "entry_price_int", "sl_trigger_int", "tp_trigger_int"):
        p.add_argument(name)
    p = sub.add_parser("cancel", help="cancel one order")
    p.add_argument("market_index"); p.add_argument("order_index")
    sub.add_parser("cancel-all", help="cancel every open order")
    p = sub.add_parser("close", help="market-close a position (reduce-only)")
    p.add_argument("market_index"); p.add_argument("side"); p.add_argument("size_int"); p.add_argument("price_int")
    args = parser.parse_args(argv)

    gateway = None
    if args.gateway_config:
        with open(args.gateway_config) as f:
            gateway = (json.load(f).get("gateway") or None)

    if args.command == "auth":
        print(mint_auth_token(gateway=gateway))
        return 0
    if args.command == "bracket":
        out = place_bracket(args.market_index, args.side, args.size_int,
                            args.entry_price_int, args.sl_trigger_int, args.tp_trigger_int,
                            gateway=gateway)
    elif args.command == "cancel":
        out = cancel_order(args.market_index, args.order_index, gateway=gateway)
    elif args.command == "cancel-all":
        out = cancel_all(gateway=gateway)
    else:
        out = close_position(args.market_index, args.side, args.size_int, args.price_int,
                             gateway=gateway)
    print(json.dumps(out, indent=2, default=str))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
