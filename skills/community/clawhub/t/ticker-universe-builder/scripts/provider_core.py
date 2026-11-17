"""Optional public-data adapters. Fetch facts and bars; never select a universe.

Raw receipts stay in the caller's output directory. Network failure is recorded, never replaced
by a made-up value or an older cache presented as fresh. Selection does not import this module.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import http.client
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

SCANNERS = {
    "us": "america",
    "cn": "china",
    "jp": "japan",
    "kr": "korea",
    "hk": "hongkong",
    "uk": "uk",
}
LANGUAGES = {"cn": "zh", "jp": "ja", "kr": "ko", "hk": "zh_TW"}
CURRENCIES = {
    "us": {"USD"},
    "cn": {"CNY"},
    "jp": {"JPY"},
    "kr": {"KRW"},
    "hk": {"HKD"},
    "uk": {"GBX", "GBP", "GBp"},
}
COLUMNS = [
    "name",
    "description",
    "exchange",
    "type",
    "typespecs",
    "sector",
    "industry",
    "market_cap_basic",
    "close",
    "volume",
    "currency",
    "is_primary",
    "active_symbol",
]
GAUGES = {
    "us": ["AMEX:SPY", "NASDAQ:QQQ", "AMEX:IWM"],
    "cn": ["SSE:510300", "SSE:510500", "SSE:588000"],
    "jp": ["TSE:1306", "TSE:1321"],
    "kr": ["KRX:069500", "KRX:229200"],
    "hk": ["HKEX:2800", "HKEX:2828", "HKEX:3033"],
    "uk": ["LSE:ISF", "LSE:VMID"],
}


class ProviderError(ValueError):
    pass


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def curl_bytes(executable: str, url: str, payload: dict | None) -> bytes:
    """Optional OS transport for proxy/HTTP incompatibilities, with the same TLS boundary."""
    argv = [executable, "--fail", "--silent", "--show-error", "--location", "--compressed",
            "--proto", "=http,https", "--proto-redir", "=http,https",
            "--max-time", "18", "--connect-timeout", "8", "--user-agent", "Mozilla/5.0"]
    for variable, option in (("SSL_CERT_FILE", "--cacert"), ("SSL_CERT_DIR", "--capath")):
        if os.environ.get(variable):
            argv.extend([option, os.environ[variable]])
    if payload is not None:
        argv.extend(["--header", "Content-Type: application/json", "--data-binary", "@-"])
    argv.extend(["--url", url])
    try:
        result = subprocess.run(argv, input=json.dumps(payload).encode()
                                if payload is not None else None,
                                capture_output=True, timeout=20, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ProviderError("curl transport timed out") from exc
    if result.returncode:
        message = result.stderr.decode(errors="replace").strip()
        status = re.search(r"URL returned error: (\d{3})", message)
        if result.returncode == 22 and status:
            raise urllib.error.HTTPError(url, int(status[1]), message, {}, None)
        raise ProviderError(f"curl exit {result.returncode}: "
                            + message)
    return result.stdout


def request_json(url: str, cache: Path, payload: dict | None = None) -> Any:
    """A receipt is reusable only for its exact URL/body; its acquisition date is retained."""
    key = hashlib.sha256(json.dumps([url, payload], sort_keys=True).encode()).hexdigest()
    if cache.exists():
        try:
            record = json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            record = {}  # A damaged cache is fetched again, never trusted as evidence.
        if (
            record.get("request_hash") == key
            and isinstance(record.get("response"), (dict, list))
            and str(record.get("retrieved_at", ""))[:10]
            == datetime.now(timezone.utc).date().isoformat()
        ):
            return record["response"]
    errors = []
    context = None
    curl = None
    error_path = cache.with_suffix(cache.suffix + ".error.json")
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode() if payload is not None else None,
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json",
                         "Accept-Encoding": "gzip"},
            )
            if curl:
                raw, encoding = curl_bytes(curl, url, payload), "identity"
            else:
                with urllib.request.urlopen(req, timeout=18, context=context) as response:
                    # Read incrementally; still reject unfinished chunks and mismatched lengths.
                    chunks = []
                    while chunk := response.read1(64 * 1024):
                        chunks.append(chunk)
                    raw = b"".join(chunks)
                    length = response.headers.get("Content-Length")
                    if length is not None and len(raw) != int(length):
                        raise ProviderError("truncated response body")
                    encoding = response.headers.get("Content-Encoding", "identity").lower()
            if encoding == "gzip":
                body = gzip.decompress(raw)
            elif encoding == "deflate":
                body = zlib.decompress(raw)
            elif encoding in ("", "identity"):
                body = raw
            else:
                raise ProviderError(f"unsupported response encoding: {encoding}")
            result = json.loads(body)
            if not isinstance(result, (dict, list)):
                raise ProviderError("expected JSON object or array")
            write_json(
                cache,
                {
                    "url": url,
                    "request": payload,
                    "request_hash": key,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "content_encoding": encoding,
                    "transport": "curl" if curl else "urllib",
                    "response": result,
                },
            )
            error_path.unlink(missing_ok=True)
            return result
        except (OSError, ValueError, http.client.HTTPException, zlib.error) as exc:
            errors.append({"attempt": attempt + 1, "error": f"{type(exc).__name__}: {exc}"})
            write_json(error_path, {"url": url, "request": payload, "request_hash": key,
                                   "retrieved_at": datetime.now(timezone.utc).isoformat(),
                                   "attempts": errors})
            reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
            if isinstance(reason, ssl.SSLCertVerificationError):
                # macOS Python distributions may omit the OS bundle. Never disable verification
                # or override a trust store deliberately configured by the operator.
                system_ca = Path("/etc/ssl/cert.pem")
                if context is None and sys.platform == "darwin" and system_ca.is_file() and not (
                    os.environ.get("SSL_CERT_FILE") or os.environ.get("SSL_CERT_DIR")
                ):
                    context = ssl.create_default_context(cafile=str(system_ca))
                    continue
                raise ProviderError(
                    f"{url}: TLS verification failed; configure SSL_CERT_FILE"
                ) from exc
            permanent = isinstance(exc, urllib.error.HTTPError) and exc.code in (400, 401, 403, 404)
            if permanent or attempt == 2:
                raise ProviderError(f"{url}: {exc}; diagnostics: {error_path}") from exc
            curl = curl or shutil.which("curl")
            time.sleep(0.5 * (attempt + 1))
    raise ProviderError(url)


def scan_equities(market: str, output: Path) -> tuple[list[dict], dict]:
    if market not in SCANNERS:
        raise ProviderError(f"no equity adapter for {market}")
    url = f"https://scanner.tradingview.com/{SCANNERS[market]}/scan"
    rows, total = [], 1
    page_size = 500
    for offset in range(0, 30000, page_size):
        payload = {
            "filter": [
                {"left": "type", "operation": "equal", "right": "stock"},
                {"left": "is_primary", "operation": "equal", "right": True},
            ],
            "columns": COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
            "range": [offset, offset + page_size],
            "options": {"lang": LANGUAGES.get(market, "en")},
        }
        # A/H dual listings are independent instruments in this skill. A provider's global
        # primary flag must not remove an active CNY A-share (e.g. SMIC's Shanghai listing).
        if market == "cn":
            payload["filter"] = payload["filter"][:1]
        response = request_json(url, output / "raw" / f"listing-{offset}.json", payload)
        total = int(response.get("totalCount", 0))
        page = response.get("data") or []
        rows.extend(
            {"ticker": r["s"], **dict(zip(COLUMNS, r["d"], strict=True)), "source": url}
            for r in page
        )
        if offset + len(page) >= total:
            break
        if not page:
            raise ProviderError(f"{market}: listing page empty before total {total}")
    unique = {r["ticker"]: r for r in rows}
    if len(unique) < total * 0.99:
        raise ProviderError(f"{market}: incomplete listings {len(unique)}/{total}")
    return list(unique.values()), {"source": url, "reported": total, "observed": len(unique)}


def admissible_equity(row: dict, market: str) -> bool:
    """Listing/type/quote checks only. Regulatory review remains visible in the snapshot."""
    name = str(row.get("description", "")).upper()
    return bool(
        row.get("active_symbol")
        and (market == "cn" or row.get("is_primary"))
        and "common" in (row.get("typespecs") or [])
        and row.get("currency") in CURRENCIES[market]
        and (row.get("volume") or 0) > 0
        and (row.get("close") or 0) > 0
        and (row.get("market_cap_basic") or 0) > 0
        and row.get("industry")
        and row.get("sector")
        and not (market == "cn" and ("ST" in name or "退" in name))
    )


def yahoo_symbols(ticker: str, market: str) -> list[str]:
    venue, symbol = ticker.split(":", 1)
    if market == "cn":
        return [symbol + {"SSE": ".SS", "SZSE": ".SZ", "BSE": ".BJ"}[venue]]
    if market == "hk":
        return [symbol.zfill(4) + ".HK"]
    if market == "jp":
        return [symbol + ".T"]
    if market == "kr":
        return [symbol + ".KS", symbol + ".KQ"]
    if market == "uk":
        return [symbol.rstrip(".").replace(".", "-") + ".L"]
    return [symbol.replace(".", "-")]


def parse_yahoo(payload: dict, ticker: str, cutoff: str, *, expected_symbol: str | None = None,
                currencies: set[str] | None = None) -> tuple[list[tuple], dict]:
    result = ((payload.get("chart") or {}).get("result") or [None])[0]
    if not result:
        raise ProviderError(f"{ticker}: chart has no series")
    meta = result.get("meta") or {}
    if expected_symbol is not None and meta.get("symbol") != expected_symbol:
        raise ProviderError(f"{ticker}: history identity mismatch: {meta.get('symbol')}")
    if currencies is not None and meta.get("currency") not in currencies:
        raise ProviderError(f"{ticker}: unexpected currency: {meta.get('currency')}")
    indicators = result.get("indicators") or {}
    quote = (indicators.get("quote") or [{}])[0]
    adjusted = ((indicators.get("adjclose") or [{}])[0]).get("adjclose")
    if not adjusted:
        raise ProviderError(f"{ticker}: adjusted closes unavailable")
    closes, volumes = quote.get("close") or [], quote.get("volume") or []
    timestamps = result.get("timestamp") or []
    if len({len(timestamps), len(adjusted), len(closes), len(volumes)}) != 1:
        raise ProviderError(f"{ticker}: misaligned history arrays")
    currency = meta.get("currency")
    scale = 0.01 if currency in ("GBp", "GBX") else 1.0
    rows = []
    for stamp, close, raw, volume in zip(
        timestamps,
        adjusted,
        closes,
        volumes,
        strict=True,
    ):
        # Quote timezone preserves the exchange's calendar day, not the caller's timezone.
        day = datetime.fromtimestamp(stamp + int(meta.get("gmtoffset", 0)), timezone.utc)
        label = day.date().isoformat()
        if label > cutoff or close is None or raw is None or volume is None:
            continue
        if close > 0 and raw > 0 and volume > 0:
            rows.append((label, ticker, float(close), float(raw) * float(volume) * scale))
    if len(rows) < 30:
        raise ProviderError(f"{ticker}: only {len(rows)} effective daily bars")
    if (date.fromisoformat(cutoff) - date.fromisoformat(rows[-1][0])).days > 10:
        raise ProviderError(f"{ticker}: stale last quotation {rows[-1][0]}")
    if len({r[2] for r in rows[-30:]}) < 2:
        raise ProviderError(f"{ticker}: flat last 30 sessions")
    return rows, {
        "currency": currency,
        "turnover_currency": "GBP" if scale == 0.01 else currency,
        "adjustment": "Yahoo adjusted close; turnover proxy uses raw close times volume",
        "provider_symbol": meta.get("symbol"),
        "first": rows[0][0],
        "last": rows[-1][0],
        "observations": len(rows),
    }


def fetch_equity_bars(row: dict, market: str, output: Path, cutoff: str) -> tuple[list, dict]:
    errors = []
    for symbol in yahoo_symbols(row["ticker"], market):
        for host in ("query1", "query2"):
            url = f"https://{host}.finance.yahoo.com/v8/finance/chart/"
            url += urllib.parse.quote(symbol) + "?range=2y&interval=1d"
            cache = output / "raw" / (f"bars-{host}-" + symbol.replace("/", "_") + ".json")
            try:
                payload = request_json(url, cache)
                bars, details = parse_yahoo(payload, row["ticker"], cutoff,
                                            expected_symbol=symbol, currencies=CURRENCIES[market])
                details.update(
                    source=url,
                    ticker=row["ticker"],
                    receipt_sha256=hashlib.sha256(cache.read_bytes()).hexdigest(),
                    fallback_notes=list(errors),
                )
                return bars, details
            except (ProviderError, KeyError, TypeError, ValueError) as exc:
                errors.append(str(exc))
    raise ProviderError("; ".join(errors))


def fetch_equities(
    market: str, output: Path, cutoff: str, limit: int, workers: int, include: set[str]
) -> dict:
    listings, inventory = scan_equities(market, output)
    write_json(
        output / "listings.json",
        {"schema_version": 1, "market": market, "as_of": str(date.today()), "rows": listings},
    )
    eligible = [r for r in listings if admissible_equity(r, market)]
    eligible.sort(key=lambda r: (-(r.get("market_cap_basic") or 0), r["ticker"]))
    selected = {r["ticker"]: r for r in eligible[:limit]}
    # Coverage research: make sure smaller industries get price history too. This is the
    # research bench, never the final member list; the deterministic builder owns that.
    industries: dict[str, int] = {}
    for row in eligible:
        industry = row["industry"]
        industries[industry] = industries.get(industry, 0) + 1
        if industries[industry] <= 3 or row["ticker"] in include:
            selected[row["ticker"]] = row
    bars, receipts, failures = [], [], []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        pending = {
            executor.submit(fetch_equity_bars, row, market, output, cutoff): token
            for token, row in selected.items()
        }
        for count, future in enumerate(as_completed(pending), 1):
            ticker = pending[future]
            try:
                part, receipt = future.result()
                bars.extend(part)
                receipts.append(receipt)
            except (ProviderError, KeyError, ValueError) as exc:
                failures.append({"ticker": ticker, "reason": str(exc)})
            if count % 50 == 0:
                print(
                    f"{market}: {count}/{len(pending)} histories; failed {len(failures)}",
                    flush=True,
                )
    return write_fetch_result(
        output,
        market,
        cutoff,
        bars,
        {
            "inventory": inventory,
            "requested": len(selected),
            "received": len(receipts),
            "receipts": sorted(receipts, key=lambda r: r["ticker"]),
            "failures": failures,
            "not_in_active_inventory": sorted(include - {r["ticker"] for r in eligible}),
            "listing_checks": (
                "Common shares; primary outside CN; active quote; "
                "positive volume; currency; CN ST names"
            ),
            "limits": [
                "Industry is a provider classification requiring research review.",
                "Active quotes do not certify the absence of every regulatory adverse flag.",
                "Turnover is a raw-close x volume proxy, not exchange-reported daily notional.",
                "The requested price bench is a subset of the listing inventory.",
            ],
        },
    )


def fetch_gauges(market: str, output: Path, cutoff: str) -> None:
    """Append explicitly observed broad/style gauges to a completed equity research batch."""
    url = f"https://scanner.tradingview.com/{SCANNERS[market]}/scan"
    payload = {
        "symbols": {"tickers": GAUGES[market]},
        "columns": COLUMNS,
        "options": {"lang": LANGUAGES.get(market, "en")},
    }
    response = request_json(url, output / "raw/gauges.json", payload)
    listing_path = output / "listings.json"
    listings = json.loads(listing_path.read_text(encoding="utf-8"))
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    held = {r["ticker"] for r in listings["rows"]}
    receipts = {r["ticker"] for r in manifest["receipts"]}
    added = []
    for raw in response.get("data") or []:
        row = {"ticker": raw["s"], **dict(zip(COLUMNS, raw["d"], strict=True)), "source": url}
        if not row.get("active_symbol"):
            continue
        if row["ticker"] not in held:
            listings["rows"].append(row)
        if row["ticker"] not in receipts:
            manifest["requested"] += 1
            try:
                part, receipt = fetch_equity_bars(row, market, output, cutoff)
                added.extend(part)
                manifest["receipts"].append(receipt)
                manifest["received"] += 1
            except ProviderError as exc:
                manifest["failures"].append({"ticker": row["ticker"], "reason": str(exc)})
    path = output / "prices.csv"
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerows(added)
    manifest["prices_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest["complete"] = not manifest["failures"]
    write_json(listing_path, listings)
    write_json(output / "manifest.json", manifest)


def write_fetch_result(output: Path, market: str, cutoff: str, bars: list, manifest: dict) -> dict:
    path = output / "prices.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "ticker", "close", "turnover"])
        writer.writerows(sorted(bars, key=lambda r: (r[1], r[0])))
    manifest.update(
        schema_version=1,
        market=market,
        as_of=str(date.today()),
        prices_until=cutoff,
        prices_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        complete=not manifest.get("failures"),
    )
    write_json(output / "manifest.json", manifest)
    return manifest


def fetch_crypto(output: Path, cutoff: str, limit: int, workers: int,
                 scope: str = "spot-linked") -> dict:
    products_url = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products"
    spot_url = "https://api.binance.com/api/v3/exchangeInfo"
    perp_url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    products = request_json(products_url, output / "raw/products.json")["data"]
    spots = request_json(spot_url, output / "raw/spot-listings.json")["symbols"]
    perps = request_json(perp_url, output / "raw/perp-listings.json")["symbols"]
    spot_by_base = {
        r["baseAsset"]: r for r in spots if r["status"] == "TRADING" and r["quoteAsset"] == "USDT"
    }
    perp_by_base = {
        r["baseAsset"]: r
        for r in perps
        if r["status"] == "TRADING"
        and r["quoteAsset"] == "USDT"
        and r["contractType"] == "PERPETUAL"
    }
    stable = {
        "USDC",
        "FDUSD",
        "TUSD",
        "DAI",
        "USDP",
        "BUSD",
        "USD1",
        "USDE",
        "USDD",
        "AEUR",
        "EURI",
        "PAXG",
        "XAUT",
    }
    # Tokenised gold remains a useful instrument but is outside this crypto operating-asset bench.
    candidates = [
        r
        for r in products
        if r.get("q") == "USDT"
        and r.get("st") == "TRADING"
        and r["b"] in spot_by_base
        and r["b"] not in stable
        and not r.get("etf")
        and r.get("tags")
        and not {"stablecoin", "stablecoins", "bStocks", "tCommodities", "Monitoring"}
        & set(r["tags"])
    ]
    candidates.sort(key=lambda r: (-float(r.get("qv") or 0), r["b"]))
    if scope == "all-perpetuals":
        # Exchange-provided subtype labels extend coverage without guessing protocol economics.
        aliases = {"DeFi": "defi", "Layer-1": "Layer1_Layer2", "Layer-2": "Layer1_Layer2",
                   "Storage": "storage-zone", "Payment": "Payments", "PoW": "mining-zone"}
        banned = {r["b"] for r in products if r.get("etf") or
                  {"stablecoin", "stablecoins", "bStocks", "tCommodities", "Monitoring"}
                  & set(r.get("tags") or [])} | stable
        by_base = {r["b"]: dict(r) for r in candidates}
        for base, contract in sorted(perp_by_base.items()):
            subtypes = contract.get("underlyingSubType") or []
            possible_spot_base = base.lstrip("0123456789")
            if base != possible_spot_base and possible_spot_base in by_base:
                # Do not introduce a second economic identity before verifying the multiplier.
                continue
            if base in banned or contract.get("underlyingType") != "COIN" or (
                {"TradFi", "Index", "Cross Pair", "USDC"} & set(subtypes)
            ):
                continue
            # Marketing-only categories (Alpha/Crypto/Chinese) do not assert an economic theme.
            tags = [aliases.get(t, t) for t in subtypes
                    if t not in {"Alpha", "Crypto", "Chinese"}]
            if not tags:
                continue
            if base not in by_base or not set(by_base[base]["tags"]) - {
                "Seed", "HODLer", "Launchpool", "Launchpad", "innovation-zone", "",
            }:
                by_base[base] = {"b": base, "an": base, "tags": tags,
                                 "_theme_source": perp_url}
        # Preserve the liquid spot-linked research order; additional contracts are deterministic.
        candidates = list(by_base.values())
    chosen = candidates[:limit]
    for anchor in ("BTC", "ETH", "SOL"):
        if not any(r["b"] == anchor for r in chosen):
            match = next((r for r in candidates if r["b"] == anchor), None)
            if match:
                chosen.append(match)
    until = int(
        datetime.combine(date.fromisoformat(cutoff), datetime.max.time(), timezone.utc).timestamp()
        * 1000
    )

    def history(product: dict) -> tuple[list, dict, dict]:
        base = product["b"]
        failures = []
        for kind, inventory, listing_url in (
            ("perp", perp_by_base, perp_url),
            ("spot", spot_by_base, spot_url),
        ):
            if base not in inventory:
                continue
            contract = inventory[base]
            symbol = contract["symbol"]
            ticker = "BINANCE:" + symbol + (".P" if kind == "perp" else "")
            endpoint = (
                "https://fapi.binance.com/fapi/v1/klines"
                if kind == "perp"
                else "https://api.binance.com/api/v3/klines"
            )
            url = (
                endpoint
                + "?"
                + urllib.parse.urlencode(
                    {"symbol": symbol, "interval": "1d", "limit": 550, "endTime": until}
                )
            )
            try:
                payload = request_json(url, output / "raw" / f"{kind}-{symbol}.json")
                bars = [
                    (
                        datetime.fromtimestamp(r[0] / 1000, timezone.utc).date().isoformat(),
                        ticker,
                        float(r[4]),
                        float(r[7]),
                    )
                    for r in payload
                    if int(r[6]) <= until and float(r[4]) > 0 and float(r[7]) > 0
                ]
                if (
                    len(bars) < 180
                    or (date.fromisoformat(bars[-1][0]) - date.fromisoformat(bars[-30][0])).days
                    != 29
                    or (date.fromisoformat(cutoff) - date.fromisoformat(bars[-1][0])).days > 2
                ):
                    raise ProviderError("insufficient continuous history or stale quote")
                if sum(r[3] for r in bars[-30:]) / 30 < 1_000_000:
                    raise ProviderError(
                        "30d mean quoted turnover below the disclosed $1m research floor"
                    )
                row = {
                    "ticker": ticker,
                    "name": product.get("an") or base,
                    "asset_id": base,
                    "tags": product["tags"],
                    "source": listing_url,
                    "theme_source": product.get("_theme_source", products_url),
                    "status": contract["status"],
                    "listing_as_of": str(date.today()),
                    "venue_choice": kind,
                    "fallback_notes": failures,
                }
                return (
                    bars,
                    row,
                    {
                        "ticker": ticker,
                        "source": url,
                        "observations": len(bars),
                        "first": bars[0][0],
                        "last": bars[-1][0],
                    },
                )
            except (ProviderError, TypeError, KeyError, ValueError) as exc:
                failures.append(f"{kind}: {exc}")
        raise ProviderError(f"{base}: " + "; ".join(failures))

    bars, rows, receipts, failed = [], [], [], []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        pending = {executor.submit(history, product): product["b"] for product in chosen}
        for count, future in enumerate(as_completed(pending), 1):
            try:
                part, row, receipt = future.result()
                bars.extend(part)
                rows.append(row)
                receipts.append(receipt)
            except ProviderError as exc:
                failed.append({"asset_id": pending[future], "reason": str(exc)})
            if count % 50 == 0:
                print(
                    f"crypto: {count}/{len(pending)} histories; excluded {len(failed)}", flush=True
                )
    write_json(
        output / "listings.json",
        {"schema_version": 1, "market": "crypto", "as_of": str(date.today()), "rows": rows},
    )
    return write_fetch_result(
        output,
        "crypto",
        cutoff,
        bars,
        {
            "requested": len(chosen),
            "received": len(rows),
            "failures": failed,
            "receipts": sorted(receipts, key=lambda r: r["ticker"]),
            "inventory": {
                "spot_usdt": len(spot_by_base),
                "perp_usdt": len(perp_by_base),
                "tagged_products": len(candidates),
                "research_scope": scope,
            },
            "limits": [
                "Binance product tags or official contract subtypes classify the research bench.",
                "Perpetual preferred only after history and $1m 30d notional floor; spot fallback.",
                "180 effective days required for this measured example; new listings excluded.",
                "Possible multiplier/spot pairs await identity research; not double-counted.",
            ],
        },
    )


def fetch(
    *,
    market: str,
    output: str | Path,
    cutoff: str,
    limit: int = 500,
    workers: int = 6,
    include: set[str] | None = None,
    crypto_scope: str = "spot-linked",
) -> dict:
    try:
        cutoff_date = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ProviderError("prices cutoff must be ISO YYYY-MM-DD") from exc
    if market not in {*SCANNERS, "crypto"}:
        raise ProviderError(f"no public-data adapter for {market}")
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    if cutoff_date >= date.today():
        raise ProviderError("prices cutoff must precede today to exclude incomplete sessions")
    if limit < 1 or not 1 <= workers <= 8:
        raise ProviderError("limit must be positive; workers must be 1..8")
    if crypto_scope not in {"spot-linked", "all-perpetuals"}:
        raise ProviderError("crypto_scope must be spot-linked or all-perpetuals")
    try:
        if market == "crypto":
            return fetch_crypto(root, cutoff, limit, workers, crypto_scope)
        fetch_equities(market, root, cutoff, limit, workers, include or set())
        fetch_gauges(market, root, cutoff)
    except (ProviderError, KeyError, TypeError, ValueError) as exc:
        failure = {"stage": "inventory_or_gauges", "reason": str(exc)}
        manifest_path = root / "manifest.json"
        if manifest_path.exists():
            # Preserve previously acquired bars and their original cutoff on an inventory failure.
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update(complete=False, requested_prices_until=cutoff)
            manifest.setdefault("failures", []).append(failure)
            write_json(manifest_path, manifest)
            return manifest
        return write_fetch_result(root, market, cutoff, [],
                                  {"requested": 0, "received": 0, "receipts": [],
                                   "failures": [failure]})
    return json.loads((root / "manifest.json").read_text(encoding="utf-8"))
