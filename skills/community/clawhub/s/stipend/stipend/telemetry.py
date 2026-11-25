"""Anonymous usage counting.

We need to know how many installs exist — without it there is nothing to show a
merchant and no way to tell whether this is working. But this is a product whose
entire pitch is that it doesn't leak your money or your data, so the bar is high.

What is sent:
  * a random install id, generated locally, tied to nothing
  * the version, the chain name (base / base-sepolia)
  * counts: how many payments, how many x402 calls
  * coarse spend buckets, NOT amounts
  * how often the limits refused a payment, and which limit — as buckets, from
    our own fixed list of reasons

What is never sent — and there is no code path that could:
  * wallet addresses, private keys, the passphrase
  * counterparties, URLs, transaction hashes
  * exact amounts, balances, or anything joinable back to a person
  * the reason text of a refusal, or who it was to

Disclosed on first run, one line to turn off, and the payload is printable
before it is sent (`stipend telemetry show`). If you would not be comfortable
publishing the payload, it should not be in here.
"""

import json
import os
import secrets
import time
import urllib.error
import urllib.request

from . import __version__
from .config import CONFIG_DIR, ensure_dirs, load_config

STATE_FILE = CONFIG_DIR / "telemetry.json"
ENDPOINT = os.environ.get("STIPEND_TELEMETRY_URL", "https://stipend.sh/api/ping")
SEND_EVERY = 24 * 3600

NOTICE = """
Stipend counts anonymous installs so we know how many agents are using it.
Sent: a random id, the version, the chain name, how many payments were made,
and how many the limits refused. Never sent: addresses, keys, amounts,
counterparties or URLs.

  See exactly what would be sent:  stipend telemetry show
  Turn it off:                     stipend telemetry off
"""


def _bucket(count):
    """Coarse buckets, so no exact figure ever leaves the machine."""
    for edge in (0, 1, 5, 10, 25, 50, 100, 250, 500, 1000):
        if count <= edge:
            return f"<={edge}"
    return ">1000"


def _state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _save(state):
    ensure_dirs()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        os.chmod(STATE_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass


def install_id():
    """Random, local, tied to nothing. Not derived from the wallet."""
    state = _state()
    if not state.get("install_id"):
        state["install_id"] = secrets.token_hex(8)
        state["first_seen"] = time.time()
        _save(state)
    return state["install_id"]


# A file we drop on our own machines. Our testing was landing in the install
# count as if strangers had adopted the wallet — twice we read a number as
# traction and it was us. A count that flatters is worse than no count, so the
# machines that build this thing are excluded at the source.
OURS_MARKER = "/etc/stipend-is-ours"


def _is_one_of_ours():
    if os.environ.get("STIPEND_OURS", "").lower() in ("1", "true", "yes"):
        return True
    try:
        return os.path.exists(OURS_MARKER)
    except Exception:
        return False


def enabled():
    if os.environ.get("STIPEND_TELEMETRY", "").lower() in ("0", "off", "false", "no"):
        return False
    if _is_one_of_ours():
        return False
    if _state().get("disabled"):
        return False
    return bool(load_config().get("telemetry", True))


def set_enabled(on):
    state = _state()
    state["disabled"] = not on
    _save(state)
    return on


def first_run_notice():
    """Show the notice once, so nobody is surprised later."""
    state = _state()
    if state.get("notice_shown"):
        return False
    state["notice_shown"] = True
    _save(state)
    return True


def _tier():
    """"paid" or "free", from the installed licence. Never raises."""
    try:
        from . import license as lic
        return "paid" if lic.is_paid() else "free"
    except Exception:
        return "free"


def payload():
    """Exactly what would be sent. Printable, by design."""
    from . import ledger
    cfg = load_config()
    rows = ledger.entries(days=30)
    return {
        "install_id": install_id(),
        # Our own release checks install the real tarball and ping like anybody
        # else, so five of five "installs" on 11 August were us. This lets the
        # server tell them apart without us storing anyone's address. It is
        # opt-in from this side and says nothing about the machine.
        "dev": bool(os.environ.get("STIPEND_DEV")),
        "version": __version__,
        "chain": cfg.get("chain"),
        "payments_30d": _bucket(len([e for e in rows if e["direction"] == "out"])),
        "earnings_30d": _bucket(len([e for e in rows if e["direction"] == "in"])),
        "has_earned": any(e["direction"] == "in" for e in rows),
        # Read from the licence, not from config. config["tier"] defaults to
        # "free" and nothing has ever written "paid" into it, so this reported
        # every paying customer as free and the conversion count on our own
        # stats page was permanently zero. The licence file is the only thing
        # that actually knows.
        "tier": _tier(),
        **_refusals(),
    }


def _refusals():
    """How often the limits refused something, by kind. Counts only.

    The limits are the product. Whether they are set anywhere near right is a
    question we could not answer at all: a refusal was written to a file on the
    agent's own machine and stayed there, so "the defaults are well judged" and
    "nobody has ever reached the defaults" produced identical evidence — none.

    Same bar as everything else here. The kind is a word our own code chose
    from a fixed list; the count is a bucket. Who was being paid, how much, and
    the reason text never leave, and no code path here could carry them.

    Never raises: telemetry is the least important thing on this machine.
    """
    try:
        from . import policy
        summary = policy.refusal_summary(days=30)
        return {
            "refusals_30d": _bucket(summary["total"]),
            # Which limits are doing the work. A build where only
            # new_destination ever fires is telling us something different from
            # one where over_daily fires constantly.
            "refused_by_kind": {k: _bucket(n)
                                for k, n in summary["by_kind"].items()},
            # Runs of refusals in minutes — someone rephrasing until something
            # gets through, which is the case the limits exist for.
            "refusal_bursts_30d": _bucket(summary["bursts"]),
        }
    except Exception:
        return {}


RELEASE_URL = os.environ.get("STIPEND_RELEASE_URL", "https://stipend.sh/api/release")


def _remember_release(release):
    if not isinstance(release, dict) or not release.get("latest_version"):
        return
    state = _state()
    state["release"] = release
    state["release_checked"] = time.time()
    _save(state)


def known_release():
    return _state().get("release") or {}


def update_available():
    """Is there a newer version than the one running? Never raises.

    Deliberately dumb string comparison on a semver triple — this only decides
    whether to mention an update, so being occasionally conservative is fine.
    """
    latest = (known_release().get("latest_version") or "").strip()
    if not latest:
        return None
    def parts(v):
        try:
            return tuple(int(x) for x in v.split(".")[:3])
        except ValueError:
            return (0,)
    if parts(latest) > parts(__version__):
        rel = known_release()
        return {
            "current": __version__,
            "latest": latest,
            "urgent": bool(rel.get("urgent")),
            "notice": rel.get("notice") or "",
            "download": rel.get("download") or "https://stipend.sh/stipend.tar.gz",
        }
    return None


def pending_notice():
    """A message from stipend.sh that this install has not seen yet.

    The ping response is the only channel we have to reach anyone: no email
    list, no account, no contact details held. It was already carrying a
    `notice` field — but nothing ever displayed it, so anything we broadcast
    sat unread in a state file. A channel nobody reads is not a channel.

    Notices are tracked by content hash, so each distinct message is shown once
    and editing it on the server reaches everyone again.
    """
    rel = known_release()
    text = (rel.get("notice") or "").strip()
    if not text:
        return None

    import hashlib
    fingerprint = hashlib.sha256(text.encode()).hexdigest()[:16]
    if _state().get("notice_seen") == fingerprint:
        return None

    return {"notice": text, "urgent": bool(rel.get("urgent")),
            "fingerprint": fingerprint,
            "latest_version": rel.get("latest_version")}


def mark_notice_seen(fingerprint):
    state = _state()
    state["notice_seen"] = fingerprint
    _save(state)


def check_release():
    """Ask directly. Works even with telemetry off — sends nothing about you."""
    try:
        req = urllib.request.Request(
            RELEASE_URL, headers={"User-Agent": f"stipend/{__version__}"})
        release = json.loads(urllib.request.urlopen(req, timeout=8).read().decode())
        _remember_release(release)
        return release
    except Exception as e:
        return {"error": str(e)[:80]}


def due():
    """Is a send actually owed right now? A local file read, no network.

    Callers use this to avoid paying any latency on the 99% of runs where the
    daily ping has already gone.
    """
    if not enabled():
        return False
    return time.time() - float(_state().get("last_sent", 0)) >= SEND_EVERY


def ping(force=False):
    """Send at most once a day. Never blocks, never raises, never retries."""
    if not enabled():
        return {"sent": False, "reason": "telemetry disabled"}

    state = _state()
    if not force and time.time() - float(state.get("last_sent", 0)) < SEND_EVERY:
        return {"sent": False, "reason": "already sent today"}

    try:
        request = urllib.request.Request(
            ENDPOINT, data=json.dumps(payload()).encode(),
            headers={"Content-Type": "application/json",
                     "User-Agent": f"stipend/{__version__}"})
        response = urllib.request.urlopen(request, timeout=5)
        try:
            body = json.loads(response.read().decode())
            _remember_release(body.get("release") or {})
        except Exception:
            pass    # a malformed reply must not break anything
        state = _state()
        state["last_sent"] = time.time()
        _save(state)
        return {"sent": True}
    except Exception as e:
        # A telemetry failure must never affect the agent. Swallow it.
        return {"sent": False, "reason": str(e)[:80]}
