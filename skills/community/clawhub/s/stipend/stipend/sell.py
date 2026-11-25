"""Sell things — a paywall that runs on your machine, not ours.

The rest of this kit runs locally and holds nothing. Hosting other people's
listings would have been the one place we broke that rule, so we don't:

    stipend sell add --name "Research report" --price 5 --file report.pdf
    stipend sell serve

Your machine serves the paywall. Your wallet receives the money. Your ETH pays
the settlement gas. We are not in the transaction, which means there is no
listing for us to moderate, no file for us to store, and no refund for us to
argue about. It is entirely yours.

The trade: buyers have to be able to reach you. An agent on a server is fine;
one behind a home router needs a tunnel it sets up itself. That is a real
limitation and it is better stated plainly than papered over.

How a sale works:
  1. buyer GETs your item URL, gets a 402 with your price and YOUR address
  2. buyer signs an EIP-3009 authorisation naming you as recipient
  3. buyer POSTs it back; you broadcast it and pay a fraction of a cent of gas
  4. the USDC moves buyer -> you, directly on-chain
  5. you deliver the file, and the sale lands in your ledger as earnings
"""

import hashlib
import json
import os
import secrets
import time
from datetime import datetime, timezone

from .config import CONFIG_DIR, chain_params, ensure_dirs, from_units, load_config, to_units

CATALOG_FILE = CONFIG_DIR / "catalog.json"
SALES_FILE = CONFIG_DIR / "sales.json"
FILES_DIR = CONFIG_DIR / "for-sale"


class SellError(RuntimeError):
    pass


def _load(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _save(path, data):
    ensure_dirs()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except (OSError, NotImplementedError):
        pass


def catalog():
    return _load(CATALOG_FILE, {})


def add_item(name, price_usdc, file_path=None, text=None, description=None):
    """List something for sale. The file is copied so a later move can't break it."""
    if not name or not str(name).strip():
        raise SellError("An item needs a name.")
    try:
        price = float(price_usdc)
    except (TypeError, ValueError):
        raise SellError(f"Price is not a number: {price_usdc!r}")
    if price <= 0:
        raise SellError("Price must be greater than zero.")
    if not file_path and not text:
        raise SellError("Nothing to deliver — give --file or --text.")

    ensure_dirs()
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    slug = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8].lower()
    stored = None
    if file_path:
        src = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.isfile(src):
            raise SellError(f"No such file: {src}")
        if os.path.getsize(src) > 50 * 1024 * 1024:
            raise SellError("File is over 50 MB — host it elsewhere and sell a link.")
        stored = str(FILES_DIR / f"{slug}-{os.path.basename(src)}")
        with open(src, "rb") as fin, open(stored, "wb") as fout:
            fout.write(fin.read())

    items = catalog()
    items[slug] = {
        "name": str(name).strip()[:120],
        "description": (description or "")[:500],
        "price_usdc": price,
        "file": stored,
        "text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sales": 0,
    }
    _save(CATALOG_FILE, items)
    return {"slug": slug, **items[slug]}


def remove_item(slug):
    items = catalog()
    if slug not in items:
        raise SellError(f"No item {slug!r}.")
    stored = items[slug].get("file")
    del items[slug]
    _save(CATALOG_FILE, items)
    if stored and os.path.exists(stored):
        try:
            os.unlink(stored)
        except OSError:
            pass
    return True


def payment_requirements(slug, item, receiving_address, cfg=None):
    """The 402 body. Note payTo is the SELLER — funds never route through us."""
    p = chain_params(cfg)
    return {
        "x402Version": 2,
        "accepts": [{
            "scheme": "exact",
            "network": f"eip155:{p['chain_id']}",
            "asset": p["usdc"],
            "payTo": receiving_address,
            "amount": str(to_units(item["price_usdc"], p["decimals"])),
            "maxTimeoutSeconds": 300,
            "description": item["name"],
            "resource": f"/item/{slug}",
        }],
    }


def record_sale(slug, item, amount_usdc, tx_hash, buyer=None):
    """Log the sale and push it into the ledger so P&L sees real income."""
    sales = _load(SALES_FILE, [])
    sales.append({
        "at": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "name": item["name"],
        "amount_usdc": amount_usdc,
        "buyer": buyer,
        "tx": tx_hash,
    })
    _save(SALES_FILE, sales[-2000:])

    items = catalog()
    if slug in items:
        items[slug]["sales"] = items[slug].get("sales", 0) + 1
        _save(CATALOG_FILE, items)

    try:
        from .ledger import record_earning
        record_earning(amount_usdc, from_address=buyer, category="earnings",
                       note=f"sold: {item['name']}", tx=tx_hash)
    except Exception:
        pass    # a ledger problem must never lose the sale record

    return True


def sales(limit=50):
    return _load(SALES_FILE, [])[-limit:]


def settle(payment, expected_to, expected_units, cfg=None):
    """Broadcast the buyer's authorisation. Gas comes from the seller's wallet.

    Returns (ok, detail). Validates that the money is coming to US and is at
    least the asking price before spending a cent of gas on it.
    """
    from . import chain, keystore

    try:
        auth = payment["payload"]["authorization"]
        signature = payment["payload"]["signature"]
    except (KeyError, TypeError):
        return False, "payment payload is malformed"

    if (auth.get("to") or "").lower() != expected_to.lower():
        return False, "payment is not addressed to this seller"
    if int(auth.get("value", 0)) < expected_units:
        return False, "amount is below the asking price"
    if int(auth.get("validBefore", 0)) < int(time.time()):
        return False, "authorisation has expired"

    sig = signature[2:] if signature.startswith("0x") else signature
    if len(sig) != 130:
        return False, "signature is the wrong length"
    r_, s_, v = sig[0:64], sig[64:128], int(sig[128:130], 16)
    if v < 27:
        v += 27

    def addr(a):
        return a.lower().replace("0x", "").rjust(64, "0")

    def uint(n):
        return format(int(n), "x").rjust(64, "0")

    data = ("0xe3ee160e" + addr(auth["from"]) + addr(auth["to"])
            + uint(auth["value"]) + uint(auth["validAfter"]) + uint(auth["validBefore"])
            + auth["nonce"].replace("0x", "").rjust(64, "0")
            + uint(v) + r_.rjust(64, "0") + s_.rjust(64, "0"))

    p = chain_params(cfg)
    try:
        account = keystore.load_account()
        nonce = int(chain._rpc("eth_getTransactionCount",
                               [account.address, "pending"], cfg=cfg), 16)
        gas = int(chain._rpc("eth_estimateGas", [{
            "from": account.address, "to": p["usdc"], "data": data, "value": "0x0"}], cfg=cfg), 16)
        fees = chain._fees(cfg)
        tx = {"chainId": p["chain_id"], "to": p["usdc"], "value": 0, "data": data,
              "nonce": nonce, "gas": int(gas * 1.3), "type": 2, **fees}
        signed = account.sign_transaction(tx)
        raw = signed.raw_transaction if hasattr(signed, "raw_transaction") else signed.rawTransaction
        return True, chain._rpc("eth_sendRawTransaction",
                                ["0x" + raw.hex().replace("0x", "")], cfg=cfg)
    except Exception as e:
        return False, f"settlement failed: {str(e)[:160]}"
    finally:
        account = None
