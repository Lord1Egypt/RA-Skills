#!/usr/bin/env python3
"""xh_pay.py - minimal x402 payer for the XH Agents catalogue.

Used by the ClawHub skill (copied to scripts/xh_pay.py) and by mcp_server.py in this folder.

Modes
  catalogue : list the paid routes from https://xhagents.xyz/openapi.json. Free, no key.
  quote     : read a resource 402 challenge, print price / network / payTo / asset. Free, no key.
  whoami    : print the payer address and its USDC balance. Reads the key, prints no key material.
  pay       : sign an EIP-3009 authorization, retry with the payment header, print the product and
              the decoded PAYMENT-RESPONSE settlement proof.

Rules this code enforces (in code, not by convention)
  * payer key: read only from env XH_PAYER_KEY, or from the first non-comment line of the file named
    by XH_PAYER_KEY_FILE (expected mode 600). Never printed, never written back to disk.
  * price ceiling: --max (default 0.10 USDC). A challenge priced above it is refused before signing.
  * destination: payTo must be a well-formed EVM address. Optional --pay-to allowlist.
  * asset: only canonical USDC on Base is signed for, checked by contract address and by the asset
    name carried in the challenge. A price ceiling alone is bypassable: a hostile seller can quote a
    small amount denominated in a different token, or in the same token with different decimals.
  * network: only eip155:8453 (Base), with the documented x402 v1 shorthand "base" accepted as
    an alias. Anything else is refused.
  * the payer key is required for `pay` and `whoami` only; `quote` and `catalogue` never touch it.

Examples
  python3 xh_pay.py catalogue
  python3 xh_pay.py quote https://xhagents.xyz/api/x402-trust --method POST
  python3 xh_pay.py whoami
  python3 xh_pay.py pay https://xhagents.xyz/api/x402-trust --body '{"url":"https://example.com"}'
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

try:
    from eth_account import Account
    from x402.client import x402ClientSync
    from x402.http import (
        decode_payment_required_header,
        decode_payment_response_header,
        encode_payment_signature_header,
        x402HTTPClientSync,
    )
    from x402.mechanisms.evm.exact import register_exact_evm_client
    from x402.mechanisms.evm.signers import EthAccountSigner

    SDK_AVAILABLE = True
    SDK_ERROR = ""
except ImportError as exc:  # the free modes still work without the SDK
    SDK_AVAILABLE = False
    SDK_ERROR = str(exc)

UA = "xh-pay/1.1 (+https://xhagents.xyz)"
DEFAULT_MAX = 0.10
NETWORK = "eip155:8453"
# Many x402 v1 services advertise the chain as a short name ("base") instead of the CAIP-2 id. That is
# a label, not a different chain, and the authorization is always built for NETWORK - so the documented
# v1 shorthand is accepted, while anything unknown is still refused. (Decision 2026-10-10.)
NETWORK_ALIASES = {"base": NETWORK, "base-mainnet": NETWORK}
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_NAMES = ("usd coin", "usdc")
USDC_DECIMALS = 6
RPCS = ("https://1rpc.io/base", "https://base.drpc.org", "https://mainnet.base.org")
CATALOGUE_URL = "https://xhagents.xyz/openapi.json"


def read_key() -> Optional[str]:
    """Payer key from env XH_PAYER_KEY, else the first non-comment line of XH_PAYER_KEY_FILE.

    The value is returned to the caller and never printed or persisted by this module.
    """
    value = os.environ.get("XH_PAYER_KEY")
    if value:
        return value.strip()
    path = (os.environ.get("XH_PAYER_KEY_FILE") or "").strip()
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line.split("=")[-1].strip().strip('"').strip("'")
    except OSError:
        return None
    return None


def _signer(key: str) -> Tuple[Any, Any]:
    """Build the local account and the x402 EIP-712 signer. Requires the SDK."""
    account = Account.from_key(key)
    return account, EthAccountSigner(account)


def usdc_balance(address: str) -> Optional[float]:
    """USDC balance of an address on Base via eth_call (no key needed, read only)."""
    data = "0x70a08231" + address[2:].rjust(64, "0")
    for rpc in RPCS:
        try:
            payload = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "eth_call",
                    "params": [{"to": USDC_BASE, "data": data}, "latest"],
                }
            ).encode()
            request = urllib.request.Request(
                rpc,
                data=payload,
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode()).get("result")
            if isinstance(result, str) and result.startswith("0x"):
                return int(result, 16) / float(10 ** USDC_DECIMALS)
        except Exception:  # noqa: BLE001 - try the next RPC
            continue
    return None


def as_dict(obj: Any) -> Dict[str, Any]:
    """Normalise a pydantic model or a plain dict (the x402 SDK returns models)."""
    if obj is None:
        return {}
    for attr in ("model_dump", "dict"):
        method = getattr(obj, attr, None)
        if callable(method):
            try:
                return method()
            except Exception:  # noqa: BLE001
                pass
    return obj if isinstance(obj, dict) else {}


def _decode_challenge_header(header: str) -> Optional[Any]:
    """Decode a PAYMENT-REQUIRED header with the SDK, falling back to plain base64 JSON."""
    if SDK_AVAILABLE:
        try:
            return decode_payment_required_header(header)
        except Exception:  # noqa: BLE001
            pass
    try:
        padded = header + "=" * (-len(header) % 4)
        return json.loads(base64.b64decode(padded).decode())
    except Exception:  # noqa: BLE001
        return None


def describe(required: Any) -> Dict[str, Any]:
    """Summarise a 402 challenge: price in USDC, network, payTo, asset, scheme, resource."""
    out: Dict[str, Any] = {
        "price_usdc": None,
        "network": None,
        "payTo": None,
        "asset": None,
        "scheme": None,
        "resource": None,
        "asset_name": None,
    }
    root = as_dict(required)
    resource = root.get("resource")
    if resource is not None:
        out["resource"] = str(as_dict(resource).get("url") or resource)
    accepts = root.get("accepts") or []
    first = as_dict(accepts[0]) if accepts else root
    amount = first.get("maxAmountRequired") or first.get("amount")
    try:
        out["price_usdc"] = round(int(amount) / float(10 ** USDC_DECIMALS), 6) if amount else None
    except Exception:  # noqa: BLE001
        out["price_usdc"] = None
    for field in ("network", "payTo", "asset", "scheme"):
        value = first.get(field)
        out[field] = str(value) if value is not None else None
    out["asset_name"] = as_dict(first.get("extra")).get("name")
    return out


def validate_quote(info: Dict[str, Any], max_price: float = DEFAULT_MAX,
                   allow_pay_to: Optional[List[str]] = None) -> Optional[str]:
    """Return the refusal reason when a 402 challenge must not be signed, else None.

    Order of checks: destination present and address-shaped, optional destination allowlist,
    supported network, canonical USDC on Base (contract address plus declared asset name),
    price readable, positive, within the ceiling.
    """
    pay_to = (info.get("payTo") or "").strip()
    if not pay_to:
        return "challenge names no payTo: there is no destination address"
    if not (pay_to.startswith("0x") and len(pay_to) == 42):
        return "payTo is not a well-formed EVM address: %s" % pay_to[:20]
    if allow_pay_to and pay_to.lower() not in {a.lower() for a in allow_pay_to}:
        return "payTo %s is not in the --pay-to allowlist" % pay_to
    network = (info.get("network") or "").strip()
    if network.lower() in NETWORK_ALIASES:
        network = NETWORK_ALIASES[network.lower()]  # v1 shorthand mapped to the CAIP-2 id
    if network != NETWORK:
        return "network %s is not supported (only %s)" % (network or "(empty)", NETWORK)
    asset = (info.get("asset") or "").strip().lower()
    if asset != USDC_BASE.lower():
        return "asset %s is not canonical USDC on Base" % (asset or "(empty)")
    asset_name = (info.get("asset_name") or "").strip().lower()
    if asset_name and asset_name not in USDC_NAMES:
        return "asset name '%s' contradicts canonical USDC" % asset_name
    price = info.get("price_usdc")
    if price is None:
        return "price is not readable from the challenge"
    if price <= 0:
        return "price is not sane: %s" % price
    if price > max_price:
        return "price %s is above the ceiling %s" % (price, max_price)
    return None


def challenge(url: str, method: str = "GET",
              body: Optional[Dict[str, Any]] = None) -> Tuple[int, Optional[Any], Optional[str], str]:
    """Request without paying. Returns (status, PaymentRequired|None, raw header, body text)."""
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers={"User-Agent": UA, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, None, None, response.read(4000).decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        raw = error.read(4000).decode("utf-8", "replace")
        header = error.headers.get("PAYMENT-REQUIRED") or error.headers.get("payment-required")
        required = _decode_challenge_header(header) if header else None
        if required is None and raw.strip().startswith("{"):
            try:
                required = json.loads(raw)
            except Exception:  # noqa: BLE001
                required = None
        return error.code, required, header, raw


def catalogue() -> List[Dict[str, str]]:
    """Paid routes advertised in our openapi.json (free, read only)."""
    request = urllib.request.Request(CATALOGUE_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=45) as response:
        document = json.loads(response.read().decode())
    rows: List[Dict[str, str]] = []
    for path, methods in (document.get("paths") or {}).items():
        for name, spec in methods.items():
            if name.lower() not in ("get", "post") or not isinstance(spec, dict):
                continue
            if not spec.get("security"):
                continue
            rows.append(
                {
                    "path": path,
                    "method": name.upper(),
                    "summary": (spec.get("summary") or spec.get("description") or "")[:120],
                }
            )
    return sorted(rows, key=lambda row: row["path"])


def pay(url: str, method: str = "POST", body: Optional[Dict[str, Any]] = None,
        max_price: float = DEFAULT_MAX, show: int = 1500,
        allow_pay_to: Optional[List[str]] = None) -> Dict[str, Any]:
    """Pay a resource and return the product plus the settlement proof.

    Refuses before signing when the challenge fails validate_quote().
    """
    if not SDK_AVAILABLE:
        return {"ok": False, "error": "x402 SDK not importable: %s" % SDK_ERROR,
                "hint": "pip install x402 eth_account"}
    key = read_key()
    if not key:
        return {"ok": False, "error": "no payer key (set XH_PAYER_KEY or XH_PAYER_KEY_FILE)"}

    account, signer = _signer(key)
    status, required, _header, raw = challenge(url, method, body)
    if status != 402 or required is None:
        return {"ok": status == 200, "status": status, "payer": account.address,
                "note": "no readable 402 challenge", "body": raw[:show]}

    info = describe(required)
    refusal = validate_quote(info, max_price, allow_pay_to)
    if refusal:
        return {"ok": False, "payer": account.address, "refused": refusal,
                "guard": "payTo + network + asset allowlist + price ceiling", "quote": info}

    client = x402ClientSync()
    register_exact_evm_client(client, signer, [NETWORK])
    http_client = x402HTTPClientSync(client)
    signature = encode_payment_signature_header(http_client.create_payment_payload(required))

    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers={
            "X-PAYMENT": signature,
            "PAYMENT-SIGNATURE": signature,
            "User-Agent": UA,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            text = response.read(20000).decode("utf-8", "replace")
            proof = response.headers.get("PAYMENT-RESPONSE") or response.headers.get("payment-response")
            settled: Any = None
            if proof:
                try:
                    settled = as_dict(decode_payment_response_header(proof)) or {"_raw": proof[:200]}
                except Exception:  # noqa: BLE001
                    settled = {"_raw": proof[:200]}
            return {"ok": True, "status": response.status, "payer": account.address,
                    "quote": info, "settlement": settled, "body": text[:show]}
    except urllib.error.HTTPError as error:
        return {"ok": False, "status": error.code, "payer": account.address, "quote": info,
                "error": error.read(400).decode("utf-8", "replace")}


def main() -> None:
    parser = argparse.ArgumentParser(description="pay-per-call x402 client for the XH Agents catalogue")
    parser.add_argument("action", choices=["quote", "pay", "catalogue", "whoami"])
    parser.add_argument("url", nargs="?")
    parser.add_argument("--method", default=None, help="HTTP method (default: POST with --body, else GET)")
    parser.add_argument("--body", default=None, help="JSON request body for POST routes")
    parser.add_argument("--max", type=float, default=DEFAULT_MAX, help="USDC ceiling for this call")
    parser.add_argument("--pay-to", action="append", default=None,
                        help="restrict the destination address (repeatable)")
    parser.add_argument("--show", type=int, default=1500, help="characters of the product to print")
    args = parser.parse_args()

    if args.action == "catalogue":
        for row in catalogue():
            print("  %-4s %-34s %s" % (row["method"], row["path"], row["summary"]))
        return

    if args.action == "whoami":
        key = read_key()
        if not key:
            print("no payer key in env/file")
            return
        account, _ = _signer(key)
        print("payer address:", account.address, "| USDC balance:", usdc_balance(account.address))
        return

    if not args.url:
        print("a URL is required", file=sys.stderr)
        sys.exit(2)
    method = (args.method or ("POST" if args.body else "GET")).upper()
    body = json.loads(args.body) if args.body else None

    if args.action == "quote":
        status, required, _header, raw = challenge(args.url, method, body)
        print("HTTP %s" % status)
        if required is None:
            print(json.dumps({"_note": "no PAYMENT-REQUIRED header", "_body": raw[:200]}, indent=1))
            return
        info = describe(required)
        print(json.dumps(info, indent=1))
        refusal = validate_quote(info, args.max, args.pay_to)
        print(json.dumps({"signable": refusal is None, "refused_because": refusal}, indent=1))
        return

    print(json.dumps(pay(args.url, method, body, args.max, args.show, args.pay_to), indent=1)[:6000])


if __name__ == "__main__":
    main()
