"""x402 auto-pay — the feature that turns a wallet into autonomy.

Without this, an agent with a wallet is an agent with a piggy bank. With it,
an agent hits a paywalled API, pays, and carries on — no human in the loop.

    from stipend.x402 import fetch
    response = fetch("https://api.example.com/expensive-thing")

How the protocol works, in one paragraph: the server answers `402 Payment
Required` with a base64 `PAYMENT-REQUIRED` header describing what it wants.
The client signs an **EIP-3009 `transferWithAuthorization`** — a gasless USDC
authorisation — and retries with a `PAYMENT-SIGNATURE` header. A facilitator
verifies the signature, submits it on-chain, and pays the gas. The agent never
needs ETH, and the server never holds a private key.

IMPORTANT — what is verified and what is not:
  * EIP-3009 is a settled standard and the signing here follows it exactly.
    The EIP-712 domain is read FROM THE TOKEN CONTRACT at runtime rather than
    hardcoded, so it cannot drift from whatever USDC actually expects.
  * The public x402 spec is incomplete on header encoding details. This
    implementation follows the documented shape, but INTEROP IS UNVERIFIED
    until tested against a live x402 server. Do not treat a passing self-test
    as proof it works against a real merchant.

Every payment goes through the same policy checks as a manual payout. An
injected "just pay this" from a hostile web page cannot exceed the caps, and
cannot reach a destination outside the allowlist.
"""

import base64
import json
import secrets
import time
import urllib.error
import urllib.request

from . import chain, keystore, ledger, policy
from .config import chain_params, from_units, load_config

X402_VERSION = 2
HEADER_REQUIRED = "PAYMENT-REQUIRED"
HEADER_SIGNATURE = "PAYMENT-SIGNATURE"
# What a server sends back once it has settled: base64 JSON naming the
# transaction. Nothing in the spec compels it, so treat it as a courtesy.
HEADER_RESPONSE = "PAYMENT-RESPONSE"

# Who a merchant sees paying them. We sent nothing at all until 29 August 2026,
# which made our payers indistinguishable from any Python script and meant a
# merchant offering to watch for us had nothing to match on.
USER_AGENT = "stipend/%s (+https://stipend.sh)"

# EIP-3009. Field order matters — it is part of the type hash.
EIP3009_TYPES = {
    "TransferWithAuthorization": [
        {"name": "from", "type": "address"},
        {"name": "to", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "validAfter", "type": "uint256"},
        {"name": "validBefore", "type": "uint256"},
        {"name": "nonce", "type": "bytes32"},
    ]
}

SEL_NAME = "06fdde03"     # name()
SEL_VERSION = "54fd4d50"  # version()


class PaymentRequired(RuntimeError):
    """A 402 we could not or would not satisfy. Carries the reason."""


def _b64_decode_json(value):
    padded = value + "=" * (-len(value) % 4)
    return json.loads(base64.b64decode(padded).decode("utf-8"))


def _b64_encode_json(obj):
    return base64.b64encode(json.dumps(obj, separators=(",", ":")).encode()).decode()


def _decode_string_return(hex_result):
    """Decode an ABI-encoded string return value."""
    if not hex_result or hex_result == "0x":
        return None
    raw = bytes.fromhex(hex_result[2:])
    if len(raw) < 64:
        return None
    length = int.from_bytes(raw[32:64], "big")
    return raw[64:64 + length].decode("utf-8", errors="ignore") or None


def _funding_address():
    """This wallet's address, for a message asking a human to fund it.

    Never raises. This is only ever called while reporting a failure, and a
    second exception thrown while explaining the first one would replace a
    useful message with a stack trace.
    """
    try:
        return keystore.address() or "(run: stipend wallet address)"
    except Exception:
        return "(run: stipend wallet address)"


def token_domain(token_address, cfg=None):
    """Read the EIP-712 domain from the token contract itself.

    Hardcoding name/version is how signature bugs happen — a mismatch produces
    a valid-looking signature that every verifier rejects. Asking the contract
    cannot drift.
    """
    p = chain_params(cfg)
    name = version = None
    try:
        name = _decode_string_return(
            chain._rpc("eth_call", [{"to": token_address, "data": "0x" + SEL_NAME}, "latest"], cfg=cfg))
    except Exception:
        pass
    try:
        version = _decode_string_return(
            chain._rpc("eth_call", [{"to": token_address, "data": "0x" + SEL_VERSION}, "latest"], cfg=cfg))
    except Exception:
        pass
    return {
        "name": name or "USD Coin",
        "version": version or "2",
        "chainId": p["chain_id"],
        "verifyingContract": token_address,
    }


def user_agent():
    """The string we identify ourselves with, version included.

    A merchant reporting "payments from stipend started failing" is only
    actionable if we know which build they mean.
    """
    from . import __version__
    return USER_AGENT % __version__


def _header_lookup(headers, name):
    """Find a header whatever case the server used.

    HTTP header names are case-insensitive, and the callers here are not
    consistent about what they hand us: an HTTPMessage is case-insensitive, a
    plain dict is not. A live endpoint sent `Payment-Required` in title case,
    our lookup asked for `PAYMENT-REQUIRED`, the dict said no, and we silently
    fell through to parsing the body — which produced a requirement with no
    recipient and a refusal that read like a policy problem. It was not. It was
    this.
    """
    if headers is None:
        return None
    wanted = name.lower()
    variants = (wanted, "x-" + wanted)
    try:
        items = headers.items()
    except AttributeError:
        return None
    for key, value in items:
        if str(key).lower() in variants and value:
            return value
    return None


def parse_payment_required(response_headers, body=None):
    """Extract PaymentRequirements from a 402 response."""
    raw = _header_lookup(response_headers, HEADER_REQUIRED)

    if raw:
        try:
            data = _b64_decode_json(raw)
        except Exception as e:
            raise PaymentRequired(f"402 header was not valid base64 JSON: {e}")
    elif body:
        try:
            data = json.loads(body)
        except Exception as e:
            raise PaymentRequired(f"402 had no {HEADER_REQUIRED} header and body was not JSON: {e}")
    else:
        raise PaymentRequired("402 response carried no payment requirements")

    # Servers may offer several options; take the first we can actually pay.
    options = data.get("accepts") or data.get("accepted") or [data]
    if isinstance(options, dict):
        options = [options]
    return options


CHAIN_NAMES = {
    "eip155:8453": "Base mainnet",
    "eip155:84532": "Base Sepolia (testnet)",
}

# CAIP-2 is what the x402 schema asks for, but a good share of live servers
# still name their chain the old way. Both mean the same chain, and refusing to
# pay over spelling would be our bug, not theirs.
NETWORK_ALIASES = {
    "base": 8453,
    "base-mainnet": 8453,
    "base mainnet": 8453,
    "base-sepolia": 84532,
    "base sepolia": 84532,
    "basesepolia": 84532,
}


def network_chain_id(network):
    """The chain id a server means, or None if we do not recognise the name."""
    name = (network or "").strip().lower()
    if not name:
        return None
    if name.startswith("eip155:"):
        try:
            return int(name.split(":", 1)[1])
        except ValueError:
            return None
    return NETWORK_ALIASES.get(name)


def _network_mismatch(theirs, ours, params):
    """Say which chain, and what to type. Not two numbers to go and look up."""
    them = CHAIN_NAMES.get(theirs, theirs)
    us = CHAIN_NAMES.get(ours, ours)

    # The overwhelmingly common case, and the one where the fix is one command.
    if ours.endswith(":84532") and theirs.endswith(":8453"):
        return ("this costs real money on %s, and you are on %s. "
                "The wallet address is the same on both. Switch with:  "
                "stipend config set chain base" % (them, us))
    if ours.endswith(":8453") and theirs.endswith(":84532"):
        return ("this wants %s and you are on %s. Switch with:  "
                "stipend config set chain base-sepolia" % (them, us))
    return "it wants %s and this wallet is on %s" % (them, us)


def _select_requirement(options, cfg):
    """Pick an option we can pay, or explain why none work."""
    p = chain_params(cfg)
    want_network = f"eip155:{p['chain_id']}"
    reasons = []
    for opt in options:
        scheme = (opt.get("scheme") or "").lower()
        network = opt.get("network") or ""
        asset = opt.get("asset") or opt.get("token") or ""
        if scheme and scheme != "exact":
            reasons.append(f"unsupported scheme {scheme!r}"); continue
        if network:
            theirs = network_chain_id(network)
            if theirs != int(p["chain_id"]):
                # Almost always the same thing: a fresh install is on the
                # testnet it ships with, and the thing it is trying to buy is
                # real. Chain ids are not something to make an agent look up
                # mid-purchase, so name the chains and give the exact command.
                canonical = "eip155:%d" % theirs if theirs else network
                reasons.append(_network_mismatch(canonical, want_network, p))
                continue
        if asset and asset.lower() != p["usdc"].lower():
            reasons.append(f"asset {asset} is not the USDC we hold"); continue
        return opt
    raise PaymentRequired("no payable option: " + "; ".join(reasons or ["none offered"]))


def build_payment(requirement, account, cfg=None):
    """Sign an EIP-3009 authorisation for this requirement."""
    p = chain_params(cfg)
    pay_to = requirement.get("payTo") or requirement.get("recipient")
    if not pay_to:
        raise PaymentRequired("requirement did not name a recipient")
    policy.validate_address(pay_to)

    amount_units = int(requirement.get("amount") or requirement.get("maxAmountRequired") or 0)
    if amount_units <= 0:
        raise PaymentRequired("requirement did not name a positive amount")

    timeout = int(requirement.get("maxTimeoutSeconds") or 300)
    now = int(time.time())
    authorization = {
        "from": account.address,
        "to": pay_to,
        "value": amount_units,
        # Back-dated rather than zero. Some validators refuse a zero validAfter,
        # and a little back-dating absorbs clock skew between us and them.
        "validAfter": max(now - 60, 0),
        "validBefore": now + max(timeout, 60),
        "nonce": "0x" + secrets.token_bytes(32).hex(),
    }

    # Signed as numbers, sent as strings. EIP-712 hashes uint256 values, but the
    # x402 schema types these three as strings and a facilitator that validates
    # the payload before verifying the signature answers a bare
    # "verification_failed" when it sees integers.
    wire_authorization = dict(authorization)
    for field in ("value", "validAfter", "validBefore"):
        wire_authorization[field] = str(authorization[field])

    from eth_account import Account
    signed = Account.sign_typed_data(
        account.key,
        full_message={
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                **EIP3009_TYPES,
            },
            "primaryType": "TransferWithAuthorization",
            "domain": token_domain(p["usdc"], cfg),
            "message": authorization,
        },
    )

    return {
        "x402Version": X402_VERSION,
        "accepted": requirement,
        "payload": {
            "signature": "0x" + signed.signature.hex().replace("0x", ""),
            "authorization": wire_authorization,
        },
    }


def settlement_tx(headers):
    """The chain record for a payment just made, if the server names one.

    Best effort by design. A server that settles correctly and says nothing
    is not an error, so this returns None rather than raising: never lose a
    resource the agent has already paid for over a missing receipt.
    """
    raw = _header_lookup(headers, HEADER_RESPONSE)
    if not raw:
        return None
    try:
        info = _b64_decode_json(raw)
    except Exception:
        # Some servers send the JSON unencoded. Same information.
        try:
            info = json.loads(raw)
        except Exception:
            return None
    if not isinstance(info, dict):
        return None
    # Field name varies across implementations and versions.
    for key in ("transaction", "transactionHash", "txHash", "tx_hash", "tx"):
        value = info.get(key)
        if isinstance(value, str) and value.startswith("0x") and len(value) == 66:
            return value
    return None


def fetch(url, data=None, headers=None, cfg=None, method=None,
          auto_pay=True, confirmed=False, timeout=60, _depth=0,
          _served=None):
    """HTTP request that pays a 402 and retries, within policy.

    Returns the final response body as bytes. Raises PaymentRequired if the
    payment was refused — by policy, by balance, or because the server asked
    for something we cannot pay.

    Serialised against every other payment. An agent fetching several paid URLs
    at once is the ordinary case, not an exotic one, and each of those fetches
    reads the daily total to decide whether it may spend. Without the lock they
    all read the same one.

    The lock is re-entrant across the retry recursion below: `_depth` only
    reaches 1 through the same call, which already holds it.
    """
    if _depth == 0:
        from . import locks
        try:
            with locks.payment_lock():
                return _fetch(url, data, headers, cfg, method, auto_pay,
                              confirmed, timeout, _depth, _served)
        except locks.LockBusy as e:
            raise PaymentRequired(str(e)) from e
    return _fetch(url, data, headers, cfg, method, auto_pay, confirmed,
                  timeout, _depth, _served)


def _fetch(url, data=None, headers=None, cfg=None, method=None,
           auto_pay=True, confirmed=False, timeout=60, _depth=0,
           _served=None):
    cfg = cfg or load_config()
    headers = dict(headers or {})
    if not any(k.lower() == "user-agent" for k in headers):
        headers["User-Agent"] = user_agent()
    request = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if _served is not None:
                # The paying frame needs these; the body alone cannot say
                # which transaction settled it.
                _served.append(response.headers)
            return response.read()
    except urllib.error.HTTPError as e:
        if e.code != 402:
            raise
        # Order matters. The retry after paying is made with auto_pay=False, so
        # checking auto_pay first meant a second 402 — the server rejecting a
        # payment we had already signed and sent — was reported as "auto_pay is
        # off". An agent with an empty wallet was told its configuration was
        # wrong. _depth is only ever set on that retry, so it answers first.
        if _depth:
            # The highest-intent moment this package ever sees: an agent that
            # wanted to buy a specific thing, tried, and could not. It used to
            # end here, with a diagnosis and no way forward. Nothing in this
            # package can put USDC in a wallet — that has to come from outside
            # — so the useful thing is to name the one person who can, and hand
            # over words that can be forwarded rather than paraphrased.
            raise PaymentRequired(
                "%s returned 402 again after payment was signed and sent. "
                "The server did not accept it — most often because the wallet "
                "does not hold enough USDC. Check with: stipend wallet balance"
                "\n\n"
                "If the balance is the problem, no command fixes it: USDC has "
                "to come from outside. Tell whoever runs you, and paste them "
                "this:\n\n"
                "  I tried to buy something and could not — my wallet has no "
                "money in it.\n"
                "  Send a few dollars of USDC on Base to: %s\n"
                "  Nothing to sign up for. What it is: https://stipend.sh/human\n\n"
                "Then run `stipend wallet balance` and try again."
                % (url, _funding_address()))
        if not auto_pay:
            raise PaymentRequired(f"{url} requires payment and auto_pay is off")
        error_headers, error_body = dict(e.headers or {}), e.read()

    options = parse_payment_required(error_headers, error_body)
    requirement = _select_requirement(options, cfg)

    amount_units = int(requirement.get("amount") or requirement.get("maxAmountRequired") or 0)
    amount_usdc = from_units(amount_units, chain_params(cfg)["decimals"])
    pay_to = requirement.get("payTo") or requirement.get("recipient")

    # Same gate as a manual payout. A hostile page cannot spend more than the
    # caps allow, and cannot reach an address outside the allowlist.
    try:
        approved = policy.check(amount_usdc, pay_to, cfg, confirmed=confirmed)
    except policy.PolicyError as e:
        raise PaymentRequired(f"refused by policy: {e}") from e

    account = keystore.load_account()
    try:
        payment = build_payment(requirement, account, cfg)
    finally:
        account = None

    headers[HEADER_SIGNATURE] = _b64_encode_json(payment)
    served = []
    body = fetch(url, data=data, headers=headers, cfg=cfg, method=method,
                 auto_pay=False, timeout=timeout, _depth=1, _served=served)
    tx = settlement_tx(served[0]) if served else None

    # Burns the one-time approval and records the spend. Only runs once the
    # server has actually served the resource. x402 used to record the spend but
    # not consume the approval, which left it reusable until it expired.
    policy.settle(approved, "x402:" + url[:120])

    # Record it. This used to consume the approval and stop there, so an
    # automatic 402 payment moved money and left no entry — invisible in the
    # ledger, missing from `stipend report`, and absent from the audit trail we
    # tell people they have. The manual payout path recorded; this one did not,
    # and nobody noticed because nothing errors when a write simply never
    # happens. Found by paying a stranger and then looking for the receipt.
    try:
        ledger.record_spend(approved["amount_usdc"], approved["to"],
                            category="api", note="x402 " + url[:160],
                            tx=tx)
    except Exception:
        # A bookkeeping failure must never lose a resource the agent has
        # already paid for. Better an unrecorded payment than a payment that
        # succeeded and then raised.
        pass
    return body


def probe(url, cfg=None, timeout=30):
    """What would this cost? Makes no payment and signs nothing."""
    cfg = cfg or load_config()
    try:
        probe_request = urllib.request.Request(
            url, headers={"User-Agent": user_agent()})
        with urllib.request.urlopen(probe_request, timeout=timeout) as r:
            return {"paid": False, "status": r.status, "message": "no payment required"}
    except urllib.error.HTTPError as e:
        if e.code != 402:
            return {"error": f"HTTP {e.code}"}
        options = parse_payment_required(dict(e.headers or {}), e.read())
    except Exception as e:
        return {"error": str(e)[:200]}

    p = chain_params(cfg)
    priced = []
    for opt in options:
        units = int(opt.get("amount") or opt.get("maxAmountRequired") or 0)
        priced.append({
            "scheme": opt.get("scheme"),
            "network": opt.get("network"),
            "amount_usdc": from_units(units, p["decimals"]),
            "payTo": opt.get("payTo") or opt.get("recipient"),
        })

    result = {"paid": False, "payment_required": True, "options": priced}
    try:
        req = _select_requirement(options, cfg)
        units = int(req.get("amount") or req.get("maxAmountRequired") or 0)
        amount = from_units(units, p["decimals"])
        result["payable"] = True
        result["would_pay_usdc"] = amount
        result["needs_confirmation"] = policy.confirmation_required(amount, cfg)
        try:
            policy.check(amount, req.get("payTo") or req.get("recipient"), cfg, confirmed=True)
            result["within_policy"] = True
        except policy.PolicyError as e:
            result["within_policy"] = False
            result["policy_reason"] = str(e)
    except PaymentRequired as e:
        result["payable"] = False
        result["reason"] = str(e)
    return result
