"""Referrals — free to join, one level, commission only on real sales.

    stipend affiliate join       get your code (uses your wallet as the payout address)
    stipend affiliate status     what you have earned
    stipend affiliate link       the URL to share

There is no signup form, no email and no account. Your code is derived from your
wallet address, which is also where commission is paid. Joining twice returns
the same code.

Two things this deliberately does NOT do:

  * pay for signups — only for genuine sales to real customers
  * pay on a second level — if someone you referred refers ten more, you earn
    nothing from those ten, they do

That is not modesty. Paying for recruitment rather than sales is a pyramid
scheme under ss 44-46 of the Australian Consumer Law, which is criminal, not
merely frowned upon. Anyone offering you multi-level commission on software is
either ignorant of that or hoping you are.
"""

import json
import urllib.error
import urllib.request

from . import __version__
from .config import CONFIG_DIR

API = "https://stipend.sh/api/affiliate"
STATE_FILE = CONFIG_DIR / "affiliate.json"


class AffiliateError(RuntimeError):
    pass


def _post(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        API + path, data=body,
        headers={"Content-Type": "application/json",
                 "User-Agent": "stipend/" + __version__})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            raise AffiliateError(json.loads(e.read().decode()).get("error", str(e)))
        except (ValueError, AttributeError):
            raise AffiliateError("stipend.sh returned HTTP %s" % e.code)
    except Exception as e:
        raise AffiliateError("could not reach stipend.sh: %s" % str(e)[:120])


def _get(path):
    req = urllib.request.Request(
        API + path, headers={"User-Agent": "stipend/" + __version__})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            raise AffiliateError(json.loads(e.read().decode()).get("error", str(e)))
        except (ValueError, AttributeError):
            raise AffiliateError("stipend.sh returned HTTP %s" % e.code)
    except Exception as e:
        raise AffiliateError("could not reach stipend.sh: %s" % str(e)[:120])


def _remember(code):
    try:
        STATE_FILE.write_text(json.dumps({"code": code}), encoding="utf-8")
    except OSError:
        pass    # not being able to cache it is not a failure


def code():
    """The code stored locally, or None."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8")).get("code")
    except (OSError, ValueError):
        return None


def join(address):
    """Register a payout address and get a referral code back."""
    result = _post("/join", {"address": address})
    if result.get("code"):
        _remember(result["code"])
    return result


def status(existing=None):
    existing = existing or code()
    if not existing:
        raise AffiliateError("You have not joined yet. Run: stipend affiliate join")
    return _get("/status?code=" + existing)
