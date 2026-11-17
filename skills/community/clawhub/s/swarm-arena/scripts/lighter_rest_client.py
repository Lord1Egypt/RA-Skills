#!/usr/bin/env python3
"""Lighter REST client (stdlib only — no third-party packages).

Public reads need no auth. Private reads accept an auth token minted by
lighter_signer.mint_auth_token() and send it as the Authorization header.

Wire precision: Lighter transmits order prices/sizes as INTEGERS scaled by the
market's decimals (price $3100 with 2 price decimals -> 310000; 0.0010 ETH with
4 size decimals -> 10). Use to_int_price / to_int_size / from_int_price /
from_int_size. Market metadata comes from orderBookDetails (cached 1 hour).

Retry policy: up to 3 attempts on HTTP 429 / 5xx and transient network errors,
exponential backoff (1s, 2s, 4s), honoring the Retry-After header when present.

CLI (manual use):
  python3 lighter_rest_client.py market ETH
  python3 lighter_rest_client.py candles ETH 1h 10
  python3 lighter_rest_client.py book ETH [limit]
  python3 lighter_rest_client.py funding [ETH]
  python3 lighter_rest_client.py account <account_index>
  python3 lighter_rest_client.py positions <account_index>
  python3 lighter_rest_client.py trades <account_index> [limit]
  python3 lighter_rest_client.py pnl <account_index> [resolution]
  python3 lighter_rest_client.py discover <l1_address>

Gateway mode (SPEC section 8C): pass the config's "gateway" block to the
constructor. When enabled, every read POSTs to {gateway.url}/gw/rest with body
{path, params, auth_token?} and a Bearer token from the env var named by
gateway.token_env; the {ok, status, data} envelope is unwrapped so callers see
identical shapes. All failures raise LighterAPIError, exactly like direct mode,
so circuit-breaker accounting never notices the transport. When
gateway.required is false and the gateway is unreachable, the client falls
back to direct venue access and sets self.gateway_fallback_used (the runner
journals that warning).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Default API base URL value (SPEC section 2).
# Override with the LIGHTER_BASE_URL environment variable.
DEFAULT_BASE_URL = "https://mainnet.zklighter.elliot.ai"

MARKET_DETAIL_TTL_SEC = 3600  # orderBookDetails cache lifetime
MAX_RETRIES = 3
BACKOFF_BASE_SEC = 1.0
REQUEST_TIMEOUT_SEC = 20

# Candles: verified resolution values on Lighter.
RESOLUTIONS = ("1m", "5m", "15m", "1h", "4h", "1d")


class LighterAPIError(Exception):
    """Non-retryable API error (4xx other than 429, or error code in body)."""


class _GatewayUnreachable(Exception):
    """Gateway transport failure (connection/timeout/exhausted 5xx retries)."""


class LighterRestClient:
    def __init__(self, base_url=None, auth_token=None, timeout=REQUEST_TIMEOUT_SEC,
                 gateway=None, agent=None):
        self.base_url = (base_url or os.environ.get("LIGHTER_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.auth_token = auth_token
        self.timeout = timeout
        self.gateway = self._normalize_gateway(gateway)
        self.agent = agent  # gateway identity (X-swarmArena-Agent), e.g. arena model id
        self.gateway_fallback_used = False
        self._market_details = None          # raw order_book_details list
        self._market_details_ts = 0.0
        self._markets_by_symbol = {}         # normalized per-symbol map

    @staticmethod
    def _normalize_gateway(gateway):
        if not isinstance(gateway, dict) or not gateway.get("enabled"):
            return None
        return {
            "url": str(gateway.get("url", "")).rstrip("/"),
            "token_env": gateway.get("token_env", "MANTIS_AGENT_TOKEN"),
            "timeout_sec": float(gateway.get("timeout_sec", 10) or 10),
            "required": bool(gateway.get("required", True)),
        }

    @property
    def gateway_active(self):
        return self.gateway is not None and not self.gateway_fallback_used

    # ------------------------------------------------------------------ HTTP

    def get(self, path, params=None, auth=None):
        """GET path with query params. Retries 429/5xx with exp backoff (<=3).

        auth: True -> require the client's token; str -> use that token;
              None/False -> send token only if the client already has one.
        When gateway mode is active the read is POSTed through
        {gateway.url}/gw/rest instead; the envelope is unwrapped so the
        returned payload is identical to direct mode.
        """
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        token = self.auth_token if auth is not False else None
        if isinstance(auth, str):
            token = auth

        if self.gateway_active:
            try:
                data = self._get_via_gateway(path, clean, token)
            except _GatewayUnreachable as e:
                if self.gateway["required"]:
                    raise LighterAPIError("gateway unreachable: %s" % e)
                self.gateway_fallback_used = True
                print("warning: gateway unreachable (%s); direct venue access fallback"
                      % e, file=sys.stderr)
                data = self._get_direct(path, clean, token)
        else:
            data = self._get_direct(path, clean, token)
        if isinstance(data, dict) and isinstance(data.get("code"), int) and data["code"] != 200:
            raise LighterAPIError("API code %s on %s: %s" % (data["code"], path, data.get("message", "")))
        return data

    def _get_direct(self, path, params, token):
        """Original direct-to-venue GET (unchanged transport)."""
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        headers = {"Accept": "application/json", "User-Agent": "swarm-arena/1.0"}
        if token:
            headers["Authorization"] = token
        last_err = None
        for attempt in range(1, MAX_RETRIES + 1):
            req = urllib.request.Request(url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read().decode("utf-8", "replace")
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code == 429 or 500 <= e.code < 600:
                    self._sleep_before_retry(e, attempt)
                    continue
                detail = e.read().decode("utf-8", "replace")[:500]
                raise LighterAPIError("HTTP %s on %s: %s" % (e.code, path, detail))
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                last_err = e
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE_SEC * (2 ** (attempt - 1)))
                    continue
                raise LighterAPIError("network error on %s after %d attempts: %s" % (path, MAX_RETRIES, e))
        raise LighterAPIError("request failed on %s: %s" % (path, last_err))

    def _get_via_gateway(self, path, params, token):
        """Read-through POST to {gateway.url}/gw/rest; unwrap {ok, status, data}."""
        url = self.gateway["url"] + "/gw/rest"
        body = {"path": path, "params": params}
        if token:
            body["auth_token"] = token
        bearer = os.environ.get(self.gateway["token_env"])
        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   "User-Agent": "swarm-arena/1.0",
                   "X-swarmArena-Agent": self.agent or "swarm-arena"}
        if bearer:
            headers["Authorization"] = "Bearer " + bearer
        payload = json.dumps(body).encode("utf-8")
        last_err = None
        raw = ""
        for attempt in range(1, MAX_RETRIES + 1):
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.gateway["timeout_sec"]) as resp:
                    raw = resp.read().decode("utf-8", "replace")
                    envelope = json.loads(raw) if raw else {}
                    break
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code == 429 or 500 <= e.code < 600:
                    if attempt < MAX_RETRIES:
                        self._sleep_before_retry(e, attempt)
                        continue
                    raise _GatewayUnreachable("HTTP %s after %d attempts" % (e.code, MAX_RETRIES))
                detail = e.read().decode("utf-8", "replace")[:500]
                # Same exception class a direct 4xx would raise.
                raise LighterAPIError("HTTP %s via gateway on %s: %s" % (e.code, path, detail))
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                last_err = e
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE_SEC * (2 ** (attempt - 1)))
                    continue
                raise _GatewayUnreachable(str(e))
        else:
            raise _GatewayUnreachable(str(last_err))
        if not isinstance(envelope, dict) or envelope.get("ok") is not True:
            raise LighterAPIError("gateway envelope error on %s: %s"
                                  % (path, (envelope or {}).get("error", raw[:300])))
        return envelope.get("data")

    @staticmethod
    def _sleep_before_retry(http_error, attempt):
        wait = BACKOFF_BASE_SEC * (2 ** (attempt - 1))
        retry_after = http_error.headers.get("Retry-After") if http_error.headers else None
        if retry_after:
            try:
                wait = max(wait, float(retry_after))
            except ValueError:
                pass
        time.sleep(wait)

    # ------------------------------------------------------- market metadata

    def get_order_book_details(self, market_id=None, force=False):
        """Raw orderBookDetails payload, cached for 1 hour."""
        stale = (time.time() - self._market_details_ts) > MARKET_DETAIL_TTL_SEC
        if force or stale or self._market_details is None:
            params = {}
            if market_id is not None:
                params["market_id"] = market_id
            data = self.get("/api/v1/orderBookDetails", params or None)
            details = data.get("order_book_details") or data.get("orderBookDetails") or []
            if market_id is None:
                self._market_details = details
                self._market_details_ts = time.time()
                self._rebuild_symbol_map()
                return self._market_details
            return details
        if market_id is None:
            return self._market_details
        return [d for d in self._market_details if _int(d.get("market_id")) == int(market_id)]

    def _rebuild_symbol_map(self):
        self._markets_by_symbol = {}
        for d in self._market_details or []:
            sym = d.get("symbol")
            if not sym:
                continue
            self._markets_by_symbol[sym.upper()] = {
                "symbol": sym,
                "market_id": _int(d.get("market_id", d.get("market_index"))),
                "market_index": _int(d.get("market_id", d.get("market_index"))),
                "market_type": d.get("market_type", "perp"),
                "status": d.get("status", "active"),
                "price_decimals": _int(d.get("price_decimals", d.get("supported_price_decimals", 0))),
                "size_decimals": _int(d.get("size_decimals", d.get("supported_size_decimals", 0))),
                "min_base_amount": _float(d.get("min_base_amount")),
                "min_quote_amount": _float(d.get("min_quote_amount")),
                "mark_price": _float(d.get("mark_price")),
                "index_price": _float(d.get("index_price")),
                "last_trade_price": _float(d.get("last_trade_price")),
                "open_interest": _float(d.get("open_interest")),
            }

    def list_markets(self, force=False):
        self.get_order_book_details(force=force)
        return dict(self._markets_by_symbol)

    def get_market(self, symbol):
        """Normalized market dict for a symbol like 'ETH' (1h cached)."""
        self.get_order_book_details()
        market = self._markets_by_symbol.get(symbol.upper())
        if market is None:
            raise LighterAPIError("unknown symbol %r on Lighter (known: %s)"
                                  % (symbol, ", ".join(sorted(self._markets_by_symbol)) or "none"))
        return market

    def market_id_for(self, symbol):
        return self.get_market(symbol)["market_id"]

    # ---------------------------------------------------------------- candles

    def get_candles(self, market_id, resolution, count_back=100,
                    start_timestamp=None, end_timestamp=None):
        """Candles normalized to ascending [{ts, open, high, low, close, volume}].

        Timestamps on the wire are milliseconds. The venue omits zero-valued
        fields, so missing OHLC values are filled defensively and bars without a
        usable close are dropped. At most 500 bars come back per call.
        """
        if resolution not in RESOLUTIONS:
            raise LighterAPIError("resolution must be one of %s" % (", ".join(RESOLUTIONS),))
        if end_timestamp is None:
            end_timestamp = int(time.time() * 1000)
        span_ms = int(count_back) * _resolution_ms(resolution) * 2
        if start_timestamp is None:
            start_timestamp = end_timestamp - span_ms
        data = self.get("/api/v1/candles", {
            "market_id": market_id,
            "resolution": resolution,
            "start_timestamp": int(start_timestamp),
            "end_timestamp": int(end_timestamp),
            "count_back": int(count_back),
        })
        raw = data.get("c") or data.get("candles") or []
        out = []
        prev_close = None
        for k in raw:
            close = _float(k.get("c", k.get("close")))
            if close is None:
                close = prev_close
            if close is None:
                continue
            open_ = _float(k.get("o", k.get("open"))) or close
            high = _float(k.get("h", k.get("high"))) or max(open_, close)
            low = _float(k.get("l", k.get("low"))) or min(open_, close)
            ts = _int(k.get("t", k.get("timestamp"))) or 0
            vol = _float(k.get("v", k.get("volume"))) or 0.0
            out.append({"ts": ts, "open": open_, "high": high, "low": low,
                        "close": close, "volume": vol})
            prev_close = close
        out.sort(key=lambda k: k["ts"])
        return out[-int(count_back):] if count_back else out

    # -------------------------------------------------------------- order book

    def get_order_book(self, market_id, limit=50):
        """Top-of-book depth as floats: {bids: [(price, size)], asks: [...]}."""
        data = self.get("/api/v1/orderBookOrders", {"market_id": market_id, "limit": int(limit)})
        def side(rows):
            out = []
            for r in rows or []:
                price = _float(r.get("price"))
                size = _float(r.get("remaining_base_amount", r.get("size", r.get("base_amount"))))
                if price and size:
                    out.append((price, size))
            return out
        return {"bids": side(data.get("bids")), "asks": side(data.get("asks")),
                "total_bids": _int(data.get("total_bids")) or len(data.get("bids") or []),
                "total_asks": _int(data.get("total_asks")) or len(data.get("asks") or [])}

    # ---------------------------------------------------------------- funding

    def get_funding_rates(self):
        data = self.get("/api/v1/funding-rates")
        return data.get("funding_rates") or data.get("fundingRates") or []

    def get_funding_rate(self, symbol=None, market_id=None):
        """Lighter's own funding rate for a market (None when unavailable)."""
        if market_id is None and symbol is not None:
            market_id = self.market_id_for(symbol)
        candidates = []
        for row in self.get_funding_rates():
            if market_id is not None and _int(row.get("market_id")) != int(market_id):
                continue
            if symbol is not None and str(row.get("symbol", "")).upper() != symbol.upper():
                continue
            candidates.append(row)
        for row in candidates:
            if str(row.get("exchange", "")).lower() == "lighter":
                return _float(row.get("rate"))
        return _float(candidates[0].get("rate")) if candidates else None

    # --------------------------------------------------------- private reads

    def discover_account_index(self, l1_address):
        """L1 address -> account index (first sub-account)."""
        data = self.get("/api/v1/accountsByL1Address", {"l1_address": l1_address})
        subs = data.get("sub_accounts") or []
        if not subs:
            raise LighterAPIError("no Lighter account found for L1 address %s" % l1_address)
        return _int(subs[0].get("index"))

    def get_account(self, account_index, auth=None):
        data = self.get("/api/v1/account", {"by": "index", "value": int(account_index)}, auth=auth)
        accounts = data.get("accounts") or []
        if not accounts:
            raise LighterAPIError("account index %s not found" % account_index)
        return accounts[0]

    def get_positions(self, account_index, auth=None):
        """Non-zero positions normalized to floats. sign: 1 long / -1 short."""
        account = self.get_account(account_index, auth=auth)
        out = []
        for p in account.get("positions") or []:
            size = _float(p.get("position")) or 0.0
            if size == 0.0:
                continue
            sign = _int(p.get("sign")) or (1 if size > 0 else -1)
            out.append({
                "symbol": p.get("symbol"),
                "market_id": _int(p.get("market_id")),
                "side": "long" if sign > 0 else "short",
                "sign": sign,
                "size": abs(size),
                "entry_price": _float(p.get("avg_entry_price")),
                "position_value": _float(p.get("position_value")),
                "unrealized_pnl": _float(p.get("unrealized_pnl")),
                "realized_pnl": _float(p.get("realized_pnl")),
                "liquidation_price": _float(p.get("liquidation_price")),
            })
        return out

    def get_account_trades(self, account_index, limit=100, market_id=None, auth=None):
        params = {"account_index": int(account_index), "limit": min(int(limit), 100),
                  "sort_by": "block_height", "sort_dir": "desc"}
        if market_id is not None:
            params["market_id"] = market_id
        data = self.get("/api/v1/trades", params, auth=auth)
        return data.get("trades") or []

    def get_pnl(self, account_index, resolution="1d", count_back=30,
                start_timestamp=None, end_timestamp=None, auth=None):
        """Account PnL series. Timestamps here are SECONDS (unlike candles)."""
        if end_timestamp is None:
            end_timestamp = int(time.time())
        if start_timestamp is None:
            start_timestamp = end_timestamp - count_back * 86400
        data = self.get("/api/v1/pnl", {
            "by": "index", "value": int(account_index), "resolution": resolution,
            "start_timestamp": int(start_timestamp), "end_timestamp": int(end_timestamp),
            "count_back": int(count_back),
        }, auth=auth)
        return data.get("pnl") or []

    def get_active_orders(self, account_index, market_id=None, auth=None):
        params = {"account_index": int(account_index)}
        if market_id is not None:
            params["market_id"] = market_id
        data = self.get("/api/v1/accountActiveOrders", params, auth=True if (auth is None and self.auth_token) else auth)
        return data.get("orders") or []

    def get_recent_trades(self, market_id, limit=20):
        data = self.get("/api/v1/recentTrades", {"market_id": market_id, "limit": min(int(limit), 100)})
        return data.get("trades") or []

    # ------------------------------------------------------------ account util

    @staticmethod
    def account_summary(account):
        """Equity/available margin view of a raw account object."""
        collateral = _float(account.get("collateral")) or 0.0
        available = _float(account.get("available_balance"))
        upnl = 0.0
        for p in account.get("positions") or []:
            if (_float(p.get("position")) or 0.0) != 0.0:
                upnl += _float(p.get("unrealized_pnl")) or 0.0
        return {"equity": collateral, "collateral": collateral,
                "available_margin": available if available is not None else collateral,
                "unrealized_pnl": upnl}


# ------------------------------------------------------------- conversions

def _float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        try:
            return int(float(v))
        except (TypeError, ValueError):
            return None


def _resolution_ms(resolution):
    unit = resolution[-1]
    n = int(resolution[:-1])
    mult = {"m": 60_000, "h": 3_600_000, "d": 86_400_000}[unit]
    return n * mult


def round_to_decimals(value, decimals):
    return round(float(value) + 0.0, int(decimals))


def to_int_price(price, price_decimals):
    """Float price -> Lighter wire integer (e.g. 3100.0, 2 -> 310000)."""
    return int(round(float(price) * (10 ** int(price_decimals))))


def to_int_size(size, size_decimals):
    """Float base size -> Lighter wire integer (e.g. 0.001, 4 -> 10)."""
    return int(round(float(size) * (10 ** int(size_decimals))))


def from_int_price(value, price_decimals):
    return float(value) / (10 ** int(price_decimals))


def from_int_size(value, size_decimals):
    return float(value) / (10 ** int(size_decimals))


def floor_to_step(value, decimals):
    """Round down to the market's decimal step (never rounds a size up)."""
    factor = 10 ** int(decimals)
    return int(float(value) * factor) / factor


# --------------------------------------------------------------------- CLI

def _print(obj):
    print(json.dumps(obj, indent=2, sort_keys=False))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lighter REST client (manual CLI)")
    parser.add_argument("--base-url", default=None, help="override API base URL")
    parser.add_argument("--auth-token", default=os.environ.get("LIGHTER_AUTH_TOKEN"),
                        help="auth token for private reads (or LIGHTER_AUTH_TOKEN env)")
    parser.add_argument("--gateway-url", default=None,
                        help="route reads through this gateway's /gw/rest endpoint")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("market", help="market metadata for a symbol"); p.add_argument("symbol")
    p = sub.add_parser("candles", help="candles for a symbol")
    p.add_argument("symbol"); p.add_argument("resolution", choices=RESOLUTIONS)
    p.add_argument("count", type=int, nargs="?", default=10)
    p = sub.add_parser("book", help="order book depth"); p.add_argument("symbol")
    p.add_argument("limit", type=int, nargs="?", default=20)
    p = sub.add_parser("funding", help="funding rates"); p.add_argument("symbol", nargs="?")
    p = sub.add_parser("account", help="account object"); p.add_argument("account_index", type=int)
    p = sub.add_parser("positions", help="open positions"); p.add_argument("account_index", type=int)
    p = sub.add_parser("trades", help="account trades")
    p.add_argument("account_index", type=int); p.add_argument("limit", type=int, nargs="?", default=25)
    p = sub.add_parser("pnl", help="account pnl series")
    p.add_argument("account_index", type=int); p.add_argument("resolution", nargs="?", default="1d")
    p = sub.add_parser("discover", help="account index for an L1 address"); p.add_argument("l1_address")
    args = parser.parse_args(argv)

    gateway = None
    if args.gateway_url:
        gateway = {"enabled": True, "url": args.gateway_url,
                   "token_env": "MANTIS_AGENT_TOKEN", "timeout_sec": 10, "required": True}
    client = LighterRestClient(base_url=args.base_url, auth_token=args.auth_token,
                               gateway=gateway)
    try:
        if args.command == "market":
            _print(client.get_market(args.symbol))
        elif args.command == "candles":
            _print(client.get_candles(client.market_id_for(args.symbol), args.resolution, args.count))
        elif args.command == "book":
            _print(client.get_order_book(client.market_id_for(args.symbol), args.limit))
        elif args.command == "funding":
            if args.symbol:
                _print({"symbol": args.symbol.upper(), "funding_rate": client.get_funding_rate(symbol=args.symbol)})
            else:
                _print(client.get_funding_rates())
        elif args.command == "account":
            _print(client.get_account(args.account_index))
        elif args.command == "positions":
            _print(client.get_positions(args.account_index))
        elif args.command == "trades":
            _print(client.get_account_trades(args.account_index, args.limit))
        elif args.command == "pnl":
            _print(client.get_pnl(args.account_index, args.resolution))
        elif args.command == "discover":
            _print({"account_index": client.discover_account_index(args.l1_address)})
    except LighterAPIError as e:
        print("error: %s" % e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
