"""One-time payment approvals.

The problem this solves: raising `max_per_tx_usdc` to afford one purchase
weakens the limit for *every* payment, to *anyone*, permanently. An attacker who
can talk an agent into raising its cap then has a raised cap to work with.

So don't raise the cap. Authorise one payment instead:

    stipend approve --to 0xSELLER --amount 39

That authorisation is bound to a single recipient, a single amount, expires, and
is consumed on use. It cannot be pointed somewhere else, cannot be reused, and
leaves the global limits untouched.

Approvals are the only thing that can exceed a cap, and they are deliberately
narrow: an attacker who obtains one can spend exactly that amount, exactly once,
to exactly the address the user already chose to pay.

Every sentence above was true of the intent and false of the code until 11
August 2026. `find()` matched any amount at or below the approved figure, so an
approval was a small, short-lived raised cap rather than a single payment — the
one thing this module exists to avoid. It is exact now.

The lesson is not about approvals. A docstring that describes what a control was
meant to do is worse than none: it is the sentence the author reads instead of
the code, and we repeated it in public because it was written here.
"""

import json
import os
import secrets
from datetime import datetime, timedelta, timezone

from .config import CONFIG_DIR, ensure_dirs

APPROVALS_FILE = CONFIG_DIR / "approvals.json"
DEFAULT_TTL_MINUTES = 30


class ApprovalError(RuntimeError):
    pass


def _load():
    if not APPROVALS_FILE.exists():
        return {}
    try:
        return json.loads(APPROVALS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        # Fail closed: an unreadable store means no approvals exist, so
        # everything falls back to the ordinary caps.
        return {}


def _save(data):
    ensure_dirs()
    APPROVALS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        os.chmod(APPROVALS_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass


def _prune(data):
    now = datetime.now(timezone.utc)
    live = {}
    for token, a in data.items():
        if a.get("used"):
            continue
        try:
            if datetime.fromisoformat(a["expires_at"]) > now:
                live[token] = a
        except (KeyError, ValueError):
            continue
    return live


def create(to_address, amount_usdc, ttl_minutes=DEFAULT_TTL_MINUTES, note=None):
    """Authorise exactly one payment. Returns the approval record."""
    from .policy import validate_address
    to_address = validate_address(to_address)

    try:
        amount = float(amount_usdc)
    except (TypeError, ValueError):
        raise ApprovalError(f"Amount is not a number: {amount_usdc!r}")
    if amount <= 0:
        raise ApprovalError("Amount must be greater than zero.")

    ttl = max(1, min(int(ttl_minutes), 24 * 60))
    now = datetime.now(timezone.utc)
    token = secrets.token_hex(8)

    data = _prune(_load())
    data[token] = {
        "to": to_address,
        "amount_usdc": amount,
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(minutes=ttl)).isoformat(),
        "note": note,
        "used": False,
    }
    _save(data)
    return {"token": token, **data[token]}


def find(to_address, amount_usdc):
    """An unused, unexpired approval for exactly this payment, or None.

    Exact, not a ceiling. It used to accept any amount at or under the approved
    figure, while the documentation two lines above claimed it was bound to a
    single amount. hermessol, on Moltbook, worked out the consequence from the
    documentation alone:

        approve up to $500 to avoid a second round-trip, settle at $5, and what
        remains is $495 of live, recipient-bound, single-use authority

    `consume()` does burn the whole token on first use, so it was never a
    standing balance. But between creating an approval and spending it — up to
    the 30-minute default — the surplus was real, and nothing tied the ceiling
    to the invoice that justified it.

    A human approving $500 for a $39 invoice is approving $39. Anything else
    makes the approval a small raised cap, which is the exact thing this module
    exists to avoid.
    """
    data = _prune(_load())
    want = float(amount_usdc)
    for token, a in data.items():
        if a["to"].lower() != str(to_address).lower():
            continue
        # Float equality, tolerant to the last cent-of-a-cent. USDC has six
        # decimals, so anything closer than that is the same payment.
        if abs(want - float(a["amount_usdc"])) <= 1e-9:
            return {"token": token, **a}
    return None


def get(token):
    """A specific approval by its token, if it is still usable.

    The caller naming the approval it means is stronger than us searching for
    one that fits: there is nothing to match, so there is nothing to match
    loosely.
    """
    if not token:
        return None
    a = _prune(_load()).get(str(token))
    return {"token": str(token), **a} if a else None


def consume(token):
    """Mark an approval used. Called only after a payment actually succeeds."""
    data = _load()
    if token not in data:
        raise ApprovalError("Approval no longer exists.")
    data[token]["used"] = True
    data[token]["used_at"] = datetime.now(timezone.utc).isoformat()
    _save(_prune(data))
    return True


def active():
    data = _prune(_load())
    _save(data)
    return [{"token": t, **a} for t, a in data.items()]


def revoke(token=None):
    """Cancel one approval, or all of them."""
    data = _load()
    if token is None:
        _save({})
        return len(data)
    if token not in data:
        raise ApprovalError(f"No approval with token {token}.")
    del data[token]
    _save(data)
    return 1
