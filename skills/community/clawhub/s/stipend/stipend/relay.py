"""Gas credits — send USDC without ever holding ETH.

Every transfer on Base costs gas, gas is ETH, and getting ETH needs a human.
That single fact is what stops an agent being self-sufficient: it can earn USDC
all day and still not be able to spend a cent of it.

A credit is one transaction that stipend.sh broadcasts and pays the gas for. You
sign the transfer locally — exactly as you would if you were sending it yourself
— and we submit it.

    stipend credits                     what you have
    stipend credits claim <key>         turn a purchase into credits
    stipend payout send --to 0x... --amount 5   uses a credit if you have no ETH

What we can and cannot do with what you send us:

  * the signature authorises ONE transfer, of a fixed amount, to a named
    recipient, before a deadline. We cannot change any of it.
  * we cannot reuse it — the contract rejects a nonce twice, and so do we.
  * we never hold your funds. The USDC moves from you to them, directly.

The worst we can do is refuse to broadcast, at which point you are exactly where
the free tier leaves you: fund a little ETH and send it yourself.
"""

import json
import os
import secrets
import time
import urllib.error
import urllib.request

from . import __version__
from .config import PENDING_RELAY_FILE, chain_params, ensure_dirs, load_config, to_units

RELAY_URL = "https://stipend.sh/api/relay"
CREDITS_URL = "https://stipend.sh/api/credits"
CLAIM_URL = "https://stipend.sh/api/credits/claim"
STATUS_URL = "https://stipend.sh/api/relay/status"

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


class RelayError(RuntimeError):
    """The relay refused. Nothing moved, and retrying is safe."""


class RelayUnresolved(RelayError):
    """We do not know whether the transfer happened.

    This distinction matters more than any other in this file. A refusal is
    safe: the server answered, nothing was broadcast, and the caller can try
    again. An unresolved send may already be on-chain — a connection that drops
    after we hand over a signed authorisation looks identical to one that drops
    before.

    Signing a second authorisation for the same payment is how an agent pays
    twice, because a fresh nonce is a fresh authorisation and every replay guard
    we have keys on the nonce. So an unresolved send is written down and settled
    against the nonce it was signed with, never re-signed blindly.
    """


def _call(url, payload=None, method=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json",
                 "User-Agent": "stipend/" + __version__})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        # A 4xx is the server telling us it decided not to act: definite, and
        # safe to retry. A 5xx is the server falling over, which can happen on
        # either side of the broadcast — treat it as unknown.
        fail = RelayUnresolved if e.code >= 500 else RelayError
        try:
            body = json.loads(e.read().decode())
        except Exception:
            raise fail("stipend.sh returned HTTP %s" % e.code)
        message = body.get("error", "HTTP %s" % e.code)
        if e.code == 402:
            how = body.get("how_to_get_them") or []
            message = message + "\n  " + "\n  ".join(how) if how else message
            if body.get("meanwhile"):
                message += "\n" + body["meanwhile"]
        raise fail(message)
    except Exception as e:
        # Timeout, reset, DNS. We never learned what the server did with it.
        raise RelayUnresolved("could not reach stipend.sh: %s" % str(e)[:120])


def balance(address):
    return _call(CREDITS_URL + "?address=" + address, method="GET")


def claim(license_key, address):
    """Exchange a purchase for credits, once."""
    return _call(CLAIM_URL, {"license_key": license_key, "address": address})


def sign_transfer(account, to_address, amount_usdc, cfg=None, seconds=600,
                  nonce=None):
    """Sign an EIP-3009 authorisation for exactly this transfer.

    `nonce` is 32 bytes whose only required property is uniqueness, so it is
    normally random. Passing one lets it carry meaning instead: set it to the
    hash of an agreement both parties signed, and the payment becomes
    self-describing — anybody holding the agreement can recompute the hash and
    check it against the transaction, without trusting either party's records.

    That is the whole of the attribution design; the rest is bookkeeping. See
    receipt-design.md. Random by default, because an unexplained hash is worse
    than an honest random number.
    """
    from eth_account import Account

    cfg = cfg or load_config()
    p = chain_params(cfg)
    now = int(time.time())
    authorization = {
        "from": account.address,
        "to": to_address,
        "value": to_units(amount_usdc, p["decimals"]),
        "validAfter": 0,
        "validBefore": now + seconds,
        "nonce": nonce or ("0x" + secrets.token_bytes(32).hex()),
    }

    # Read the EIP-712 domain from the token itself rather than hardcoding it —
    # a mismatch produces a signature that looks fine and every verifier rejects.
    from .x402 import token_domain
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
        "payload": {
            "signature": "0x" + signed.signature.hex().replace("0x", ""),
            "authorization": authorization,
        }
    }


def _write_durable(path, text):
    """Write so that the file is either the old content or all of the new one.

    Three things, and the third is the one people leave out:

      * a temporary file in the same directory, so the rename cannot cross a
        filesystem boundary and stop being atomic
      * fsync before the rename, so the bytes are on the device and not only in
        the page cache — a killed process survives without this, a lost machine
        does not
      * os.replace, which is atomic on POSIX and on Windows

    Without it, `write_text` truncates first, and a crash mid-write leaves a
    half-written record of a payment that may already have been sent.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
    except BaseException:
        try:
            os.unlink(str(tmp))
        except OSError:
            pass
        raise
    os.replace(str(tmp), str(path))
    # The directory entry itself needs flushing for the rename to survive power
    # loss. Not available on Windows, where the rename is already durable.
    try:
        dfd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except (OSError, AttributeError):
        pass


class PendingUnreadable(RelayUnresolved):
    """There is a pending record and we cannot read it.

    Distinct from "there is nothing pending", and the distinction is the whole
    point. Both used to return None, so a truncated or corrupt file read as
    "no payment outstanding" and the next send went ahead — the file that exists
    to prevent a double payment causing one.

    Absent means nothing is outstanding. Unreadable means something might be.
    """


def _load_pending():
    """The outstanding payment, or None if there genuinely is not one.

    Raises PendingUnreadable if a record exists but cannot be parsed. Failing
    closed on a damaged file is the only safe direction here: refusing to send
    costs an agent a delay, and guessing costs its owner a duplicate payment.
    """
    try:
        raw = PENDING_RELAY_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError as e:
        raise PendingUnreadable(
            "Cannot read the outstanding-payment record at %s (%s).\n"
            "Refusing to send in case a payment is unaccounted for."
            % (PENDING_RELAY_FILE, e))
    try:
        return json.loads(raw)
    except ValueError:
        raise PendingUnreadable(
            "The outstanding-payment record at %s is damaged.\n"
            "A payment may or may not have been sent. Check the recipient's "
            "balance before deleting it."
            % PENDING_RELAY_FILE)


def _save_pending(payment, to_address, amount_usdc, approved=None):
    """Write the signed authorisation down BEFORE it is sent.

    Written first and cleared last, deliberately. A crash between signing and
    sending leaves a record of something that may have happened; the reverse
    order leaves a payment nobody can account for.
    """
    ensure_dirs()
    auth = payment["payload"]["authorization"]
    _write_durable(PENDING_RELAY_FILE, json.dumps({
        "payment": payment,
        "to": to_address,
        "amount_usdc": float(amount_usdc),
        "nonce": auth["nonce"],
        "valid_before": auth["validBefore"],
        # The approval this payment was made under. Kept so that settling later
        # burns the same one-time approval the first attempt would have, rather
        # than leaving it live for something else to spend.
        "approved": approved,
        "at": int(time.time()),
    }, indent=2))


def _clear_pending():
    try:
        PENDING_RELAY_FILE.unlink()
    except Exception:
        pass


def remember_direct(tx_hash, to_address, amount_usdc, approved=None):
    """Record a signed transfer about to go out on our own gas.

    The relayed path has had this since 0.32.2; the direct path did not, so a
    process that died between broadcasting and recording left money moved and
    nothing written down. The daily total would then be understated for the rest
    of the day, which is the same failure as the concurrency bug and just as
    quiet.
    """
    ensure_dirs()
    _write_durable(PENDING_RELAY_FILE, json.dumps({
        "kind": "direct",
        "tx_hash": tx_hash,
        "to": to_address,
        "amount_usdc": float(amount_usdc),
        "approved": approved,
        "at": int(time.time()),
    }, indent=2))


def forget_direct():
    _clear_pending()


def _resolve_direct(p, cfg):
    """Ask the network what became of a transfer we signed but never recorded.

    No server to ask here, so the chain is the authority. The hash was written
    before the broadcast, so it is always answerable.
    """
    from . import chain
    try:
        receipt = chain.receipt(p["tx_hash"], cfg)
    except Exception as e:
        raise RelayUnresolved(
            "Could not ask the network about %s (%s). Still unresolved; nothing "
            "was sent again." % (p["tx_hash"], str(e)[:100]))

    if receipt is None:
        # Signed, possibly never broadcast, possibly still in the mempool.
        # Both are safe to leave: the nonce is fixed, so it cannot become a
        # second payment. What it must not do is silently disappear.
        raise RelayUnresolved(
            "Transaction %s is not on the network yet. It was signed against a "
            "fixed account nonce, so it cannot turn into a second payment — but "
            "it may still confirm. Run this again shortly." % p["tx_hash"])

    _clear_pending()
    ok = str(receipt.get("status", "0x1")).lower() in ("0x1", "1", "true")
    return {"tx_hash": p["tx_hash"], "relayed": False, "confirmed": ok,
            "resolved": "confirmed_on_chain" if ok else "reverted",
            "approved": p.get("approved"), "to": p.get("to"),
            "amount_usdc": p.get("amount_usdc")}


def status(nonce):
    """Has this authorisation been broadcast? The only authority is the server."""
    return _call(STATUS_URL + "?nonce=" + nonce, method="GET")


def unresolved():
    """The payment we do not know the fate of, if there is one."""
    return _load_pending()


def resolve(cfg=None):
    """Settle an unresolved send without any chance of paying twice.

    Three outcomes, and only the third involves signing anything:

      relayed          the server has it. Return the original tx; nothing new
                       is sent, and the caller settles as if the first attempt
                       had returned normally.
      still valid      never broadcast, and the authorisation has not expired.
                       Re-send THAT authorisation — same nonce, so if the server
                       did have it after all, its replay guard catches it.
      expired          never broadcast, and validBefore has passed. The contract
                       will now reject it for all time, which is the one thing
                       that makes signing a replacement provably safe.

    Returns None when there was nothing pending.
    """
    p = _load_pending()
    if not p:
        return None

    # Two ways a payment can be outstanding, and they are answered by different
    # authorities: a relayed one by the server that broadcast it, a direct one
    # by the network itself.
    if p.get("kind") == "direct":
        return _resolve_direct(p, cfg)

    try:
        st = status(p["nonce"])
    except RelayError:
        # Cannot ask, so cannot know. Leave it pending: an unresolved payment
        # that stays unresolved is recoverable, and one we guess about is not.
        raise

    if st.get("relayed"):
        _clear_pending()
        return {"tx_hash": st.get("tx"), "relayed": True,
                "resolved": "already_broadcast", "gas_paid_by": "stipend.sh",
                "approved": p.get("approved"), "to": p.get("to"),
                "amount_usdc": p.get("amount_usdc")}

    if int(p.get("valid_before") or 0) > int(time.time()):
        result = _call(RELAY_URL, p["payment"])
        _clear_pending()
        answer = _answer(result, resolved="resent")
        answer.update({"approved": p.get("approved"), "to": p.get("to"),
                       "amount_usdc": p.get("amount_usdc")})
        return answer

    _clear_pending()
    return {"relayed": False, "resolved": "expired_unsent",
            "note": "The authorisation expired without being broadcast and can "
                    "never be used. Nothing moved. Send again when ready."}


def _answer(result, resolved=None):
    answer = {"tx_hash": result.get("tx"), "relayed": True,
              "credits_left": result.get("balance"),
              "gas_paid_by": "stipend.sh"}
    if resolved:
        answer["resolved"] = resolved
    # Anything the server wants the caller to see, rather than only the fields
    # this function happened to name. The low-credit warning was being generated
    # correctly, logged correctly, and then dropped here — so the one notice
    # designed to reach an agent before it runs out never reached one.
    for extra in ("running_low", "welcome_credits", "note", "duplicate"):
        if result.get(extra) is not None:
            answer[extra] = result[extra]
    return answer


def send(account, to_address, amount_usdc, cfg=None, approved=None):
    """Sign a transfer and have stipend.sh broadcast it. Costs one credit."""
    # Never start a second payment on top of one whose fate is unknown. The
    # agent cannot be asked to reason about this; it is the sort of thing that
    # has to be impossible rather than discouraged.
    pending = _load_pending()
    if pending:
        raise RelayUnresolved(
            "A previous payment of %s USDC to %s was never confirmed, so it may "
            "or may not have been broadcast.\n"
            "Settle it before sending anything else:\n"
            "  stipend payout resolve"
            % (pending.get("amount_usdc"), pending.get("to")))

    payment = sign_transfer(account, to_address, amount_usdc, cfg)
    _save_pending(payment, to_address, amount_usdc, approved)
    try:
        result = _call(RELAY_URL, payment)
    except RelayUnresolved:
        raise                     # keep the record; resolve() will settle it
    except RelayError:
        _clear_pending()          # the server answered and did nothing
        raise
    _clear_pending()
    return _answer(result)
