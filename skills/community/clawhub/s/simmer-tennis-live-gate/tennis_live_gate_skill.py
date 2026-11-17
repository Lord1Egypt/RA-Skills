"""
Live-tennis match-state gate for Simmer / Polymarket tennis markets.

Vendor-authored: we run the Live Tennis API (https://livetennisapi.com), so
the live match state used by this gate comes from our feed. Judge accordingly.

This is the tennis analog of `examples/regime_gate_skill.py` in simmer-sdk. It
mirrors that reference line-for-line: fetch an external signal, run a gate as a
*precondition* to sizing, skip (never fall through) when the gate says no, and
only then call `size_position(...)`.

Where the regime gate reads a realized-volatility regime off a candle series,
this gate reads the *actual match state* off the Live Tennis API — the score,
who is serving, whether a break point is live, and whether the match has stopped
(retirement / walkover / suspension). A strategy that means to trade a calm,
mid-match state should not fire into a break point or into a retirement.

Observe-only by design:
    This skill NEVER places an order — real-money or paper. It returns the gate
    decision and the dollar amount a strategy *would* allocate. Execution stays
    with the calling framework, exactly as in `regime_gate_skill.py`. There is
    no `--live` real-money path here because there is no trading here at all.

Pattern:
    1. Resolve the market's two players (title parse, or an explicit override).
    2. Fetch live state from the FREE Live Tennis API tier: score, server,
       break-point flag, match status, with an `as_of` timestamp.
    3. Run `live_tennis_state_gate(...)`. If `decision.allowed` is False, log the
       reason and return — do NOT fall through to sizing.
    4. If allowed, proceed to `size_position(...)`, scaled by
       `decision.size_factor` (1.0 normally; a downsize haircut when a break
       point is live and you chose to trim rather than skip).

The gate is a *precondition* to sizing. It decides trade / no-trade (and an
optional break-point haircut); it does not compute edge. Pair it with your own
`p_win` estimate.

Break-point derivation (honest, three-valued):
    A break point is: receiver at AD, OR receiver at 40 while the server is at
    0/15/30. Never in a tiebreak. When the server or the in-game points are
    null/absent the state is UNDETERMINABLE — the gate returns break_point=None
    (UNDEF) and fails closed, rather than guessing "no break point". This
    matches the derivation in our MIT-licensed `polymarket-tennis` toolkit,
    tightened to expose UNDEF instead of collapsing it to False.

Tuning (read before deploying):
    - `max_staleness_s` (default 120): the score endpoint is a point-in-time
      snapshot with its own `as_of`. If it is older than this, the gate fails
      closed (`state_stale`) — do not gate a fast market on a slow read. Tune to
      your decision cadence. NOTE the FREE tier is 100 requests/day (~one check
      per ~15 min); it is sized for develop-and-test and periodic checks, NOT
      continuous fast polling. If you need per-point freshness, that is a paid
      concern, not a free-tier one — size `max_staleness_s` honestly for how
      often you can actually read.
    - `break_point_size_factor` (default 0.0 = skip): set to e.g. 0.5 to trim to
      half size on a live break point instead of skipping outright. This is the
      "sizes" half of "gates/sizes on a precondition".

Free-tier endpoints only (all FREE on a keyed Live Tennis API tier):
    GET /matches?status=live   — find the live match for the two players
    GET /matches/{id}/score    — score, server, points, is_tiebreak, timestamp
    GET /matches/{id}          — status + event_status (Retired/Walk Over/...)

Usage:
    export LIVETENNIS_API_KEY="..."      # FREE key: livetennisapi.com/subscribe/free
    export SIMMER_API_KEY="sk_live_..."  # only needed for --live-data market fetch
    python tennis_live_gate_skill.py                # self-contained demo, no network
    python tennis_live_gate_skill.py --live-data    # gate real Polymarket tennis markets
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

sys.stdout.reconfigure(line_buffering=True)

DEFAULT_BASE_URL = "https://api.livetennisapi.com/api/public/v1"

# Match lifecycle / stop reasons the gate distinguishes.
STATUS_LIVE = "live"
STATUS_UPCOMING = "upcoming"
STATUS_COMPLETED = "completed"
STATUS_RETIRED = "retired"
STATUS_WALKOVER = "walkover"
STATUS_INTERRUPTED = "interrupted"
STATUS_NOT_FOUND = "not_found"

# event_status values from the API that mean the match is not a clean live one.
_EVENT_STATUS_MAP = {
    "Retired": STATUS_RETIRED,
    "Walk Over": STATUS_WALKOVER,
    "Interrupted": STATUS_INTERRUPTED,
}

# The default staleness horizon, in seconds, for the score snapshot.
DEFAULT_MAX_STALENESS_S = 120.0


# --------------------------------------------------------------------------- #
# Break-point derivation (three-valued: True / False / None==UNDEF)
# --------------------------------------------------------------------------- #
def derive_break_point(score: Optional[Mapping[str, Any]]) -> Optional[bool]:
    """Return True/False if determinable, else None (UNDEF).

    True  -> the current point is a break point.
    False -> determinable, and it is not a break point (includes tiebreaks).
    None  -> UNDETERMINABLE: no score, or server/points are null/absent.

    A break point is receiver-at-AD, or receiver-at-40 while server is at
    0/15/30. Never in a tiebreak. We expose UNDEF rather than guessing "no"
    when the inputs are missing, so the gate can fail closed on it.
    """
    if not score:
        return None
    if score.get("is_tiebreak"):
        return False  # determinable: a tiebreak is never a break point
    server = score.get("server")
    if server not in (1, 2):
        return None  # UNDEF: cannot tell who is receiving
    points = score.get("points") or []
    if len(points) != 2 or points[0] is None or points[1] is None:
        return None  # UNDEF: in-game points not reported
    receiver_points = str(points[1] if server == 1 else points[0])
    server_points = str(points[0] if server == 1 else points[1])
    if receiver_points == "AD":
        return True
    return receiver_points == "40" and server_points in ("0", "15", "30")


# --------------------------------------------------------------------------- #
# State model + gate
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class MatchState:
    """Live state for one match, assembled from FREE Live Tennis API reads.

    Attributes:
        match_id: The Live Tennis API match id, or None if no match was found.
        status: One of the STATUS_* constants above.
        score: The raw score snapshot dict (sets/games/points/server/...), or
            None when unavailable.
        as_of: The score snapshot's ISO-8601 timestamp, or None.
        age_s: Seconds between `as_of` and `now`, or None if not computable.
    """

    match_id: Optional[int]
    status: str
    score: Optional[Mapping[str, Any]]
    as_of: Optional[str]
    age_s: Optional[float]


@dataclass(frozen=True)
class LiveGateDecision:
    """Result of a live-tennis-state gate check.

    Attributes:
        allowed: True if the strategy may proceed to sizing, False if it must
            skip this opportunity.
        size_factor: Multiplier to apply to the sized position. 1.0 when fully
            allowed; a value in (0, 1) on a break-point downsize; 0.0 on a skip.
        reason: Short tag explaining the decision. One of:
            - "ok"                 -> clean live state, allowed at full size
            - "break_point_downsize" -> break point live, trimmed (not skipped)
            - "break_point_live"   -> break point live, skipped
            - "state_undetermined" -> break point UNDEF (server/points null)
            - "state_unavailable"  -> no live match found for these players
            - "state_stale"        -> score snapshot older than max_staleness_s
            - "match_not_live"     -> status is upcoming/completed
            - "retirement"         -> event_status Retired / Walk Over
            - "interrupted"        -> event_status Interrupted (paused)
        status: The observed MatchState.status.
        server: Which player is serving (1|2), or None.
        break_point: Three-valued break-point flag (True/False/None==UNDEF).
        is_tiebreak: Whether the current game is a tiebreak.
        stale: True if the snapshot exceeded max_staleness_s.
        as_of: The score snapshot timestamp used, or None.
        match_id: The Live Tennis API match id, or None.
    """

    allowed: bool
    size_factor: float
    reason: str
    status: str
    server: Optional[int]
    break_point: Optional[bool]
    is_tiebreak: bool
    stale: bool
    as_of: Optional[str]
    match_id: Optional[int]


def _skip(reason: str, state: Optional[MatchState]) -> LiveGateDecision:
    score = state.score if state else None
    return LiveGateDecision(
        allowed=False,
        size_factor=0.0,
        reason=reason,
        status=state.status if state else STATUS_NOT_FOUND,
        server=(score or {}).get("server") if score else None,
        break_point=derive_break_point(score) if score else None,
        is_tiebreak=bool((score or {}).get("is_tiebreak")) if score else False,
        stale=reason == "state_stale",
        as_of=state.as_of if state else None,
        match_id=state.match_id if state else None,
    )


def live_tennis_state_gate(
    state: Optional[MatchState],
    *,
    skip_on_break_point: bool = True,
    break_point_size_factor: float = 0.0,
    max_staleness_s: float = DEFAULT_MAX_STALENESS_S,
) -> LiveGateDecision:
    """Decide whether the live match state permits an entry, mirroring the
    realized-vol regime gate's allow/skip contract.

    This is a *precondition* to position sizing — call it before
    `simmer_sdk.sizing.size_position`. It returns a binary allow/skip, plus a
    `size_factor` so a break point can be handled as a downsize instead of a
    hard skip. It does not estimate edge.

    Fail-closed order (each returns allowed=False):
        state missing/no match   -> "state_unavailable"
        status not live          -> "match_not_live"
        Retired / Walk Over      -> "retirement"
        Interrupted (paused)     -> "interrupted"
        snapshot too old         -> "state_stale"
        break point UNDEF        -> "state_undetermined"
        break point live         -> "break_point_live" (or downsize)

    Args:
        state: The assembled MatchState, or None if no match was resolved.
        skip_on_break_point: If True (default), a live break point gates the
            entry. Set False to ignore break points entirely.
        break_point_size_factor: What to do on a live break point when
            `skip_on_break_point` is True. 0.0 (default) skips; a value in
            (0, 1] trims the position to that fraction instead of skipping.
        max_staleness_s: Fail closed if the score snapshot is older than this.

    Returns:
        A LiveGateDecision. Inspect `.allowed` for the binary result and
        `.size_factor` for the sizing multiplier.
    """
    if state is None or state.match_id is None:
        return _skip("state_unavailable", state)

    if state.status in (STATUS_RETIRED, STATUS_WALKOVER):
        return _skip("retirement", state)
    if state.status == STATUS_INTERRUPTED:
        return _skip("interrupted", state)
    if state.status != STATUS_LIVE:
        return _skip("match_not_live", state)

    if state.age_s is not None and state.age_s > max_staleness_s:
        return _skip("state_stale", state)

    score = state.score or {}
    bp = derive_break_point(score)

    if skip_on_break_point:
        if bp is None:
            # UNDEF: we cannot rule a break point in or out -> fail closed.
            return _skip("state_undetermined", state)
        if bp is True:
            if break_point_size_factor and break_point_size_factor > 0.0:
                return LiveGateDecision(
                    allowed=True,
                    size_factor=float(break_point_size_factor),
                    reason="break_point_downsize",
                    status=state.status,
                    server=score.get("server"),
                    break_point=True,
                    is_tiebreak=bool(score.get("is_tiebreak")),
                    stale=False,
                    as_of=state.as_of,
                    match_id=state.match_id,
                )
            return _skip("break_point_live", state)

    return LiveGateDecision(
        allowed=True,
        size_factor=1.0,
        reason="ok",
        status=state.status,
        server=score.get("server"),
        break_point=bp,
        is_tiebreak=bool(score.get("is_tiebreak")),
        stale=False,
        as_of=state.as_of,
        match_id=state.match_id,
    )


# --------------------------------------------------------------------------- #
# Player-name resolution (folded last-name match; the polymarket-tennis toolkit
# has the fuller heuristics — reversed names, diacritics, confidence scores)
# --------------------------------------------------------------------------- #
def fold_name(name: str) -> str:
    """Lowercase, strip diacritics, collapse punctuation to single spaces."""
    decomposed = unicodedata.normalize("NFKD", name or "")
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    out = []
    for ch in stripped.lower():
        out.append(ch if ch.isalnum() else " ")
    return " ".join("".join(out).split())


def _last_token(name: str) -> str:
    folded = fold_name(name)
    return folded.split()[-1] if folded else ""


def _player_matches(api_player: Mapping[str, Any], wanted: str) -> bool:
    """True if `wanted` (a player name) plausibly names `api_player`.

    Conservative: matches on folded last-name token equality, which is enough
    to disambiguate within a single live-match list. For production-grade
    pairing across reversed names and diacritics, use `match_market` from the
    polymarket-tennis toolkit.
    """
    api_name = str(api_player.get("name", ""))
    return _last_token(api_name) == _last_token(wanted) and _last_token(wanted) != ""


def _match_has_players(match: Mapping[str, Any], players: Sequence[str]) -> bool:
    people = match.get("players") or {}
    p1 = people.get("p1") or {}
    p2 = people.get("p2") or {}
    a, b = players[0], players[1]
    return (
        (_player_matches(p1, a) and _player_matches(p2, b))
        or (_player_matches(p1, b) and _player_matches(p2, a))
    )


# --------------------------------------------------------------------------- #
# FREE-tier Live Tennis API fetch (stdlib urllib only)
# --------------------------------------------------------------------------- #
class LiveTennisError(RuntimeError):
    """Raised on a non-recoverable Live Tennis API read error."""


def _http_get_json(
    base_url: str,
    path: str,
    api_key: str,
    params: Optional[Mapping[str, Any]] = None,
    *,
    timeout: float = 10.0,
) -> Any:
    url = base_url.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:  # pragma: no cover - network path
        raise LiveTennisError(f"HTTP {e.code} on {path}") from e
    except (urllib.error.URLError, TimeoutError) as e:  # pragma: no cover
        raise LiveTennisError(f"network error on {path}: {e}") from e


def _parse_iso8601(ts: Optional[str]) -> Optional[float]:
    if not ts:
        return None
    try:
        from datetime import datetime, timezone

        cleaned = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def _status_from_match(match: Mapping[str, Any]) -> str:
    event_status = match.get("event_status")
    if event_status in _EVENT_STATUS_MAP:
        return _EVENT_STATUS_MAP[event_status]
    return str(match.get("status") or STATUS_NOT_FOUND)


def fetch_live_tennis_state(
    players: Sequence[str],
    *,
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    now: Optional[float] = None,
    live_matches: Optional[Sequence[Mapping[str, Any]]] = None,
    score_fetch: Optional[Any] = None,
    match_fetch: Optional[Any] = None,
) -> Optional[MatchState]:
    """Resolve the live match for `players` and assemble its MatchState.

    Uses only FREE-tier endpoints. The `live_matches`, `score_fetch` and
    `match_fetch` hooks exist so tests can inject fixtures without a network.

    Args:
        players: Two player names to resolve (order-insensitive).
        api_key: A Live Tennis API key (the FREE tier is enough).
        base_url: API base; defaults to the public v1 base.
        now: Wall-clock seconds override (for testing staleness).
        live_matches: Pre-fetched `/matches?status=live` data, or None to fetch.
        score_fetch: Optional callable(match_id) -> score dict (test hook).
        match_fetch: Optional callable(match_id) -> match dict (test hook).

    Returns:
        A MatchState, or None if no live match matched the two players.
    """
    if len(players) != 2:
        raise ValueError(f"players must be exactly two names, got {players!r}")

    now = time.time() if now is None else now

    if live_matches is None:
        payload = _http_get_json(base_url, "/matches", api_key, {"status": "live"})
        live_matches = (payload or {}).get("data") or []

    hit = next((m for m in live_matches if _match_has_players(m, players)), None)
    if hit is None:
        return None

    match_id = hit.get("id")

    # Full detail (for status + event_status); FREE endpoint.
    if match_fetch is not None:
        match = match_fetch(match_id)
    else:
        match = _http_get_json(base_url, f"/matches/{match_id}", api_key)
    match = match or hit
    status = _status_from_match(match)

    # Lowest-latency score snapshot; FREE endpoint.
    if score_fetch is not None:
        score = score_fetch(match_id)
    else:
        score = _http_get_json(base_url, f"/matches/{match_id}/score", api_key)

    as_of = (score or {}).get("timestamp")
    as_of_epoch = _parse_iso8601(as_of)
    age_s = (now - as_of_epoch) if as_of_epoch is not None else None

    return MatchState(
        match_id=match_id,
        status=status,
        score=score,
        as_of=as_of,
        age_s=age_s,
    )


# --------------------------------------------------------------------------- #
# The reference flow, mirroring run_one_market_with_regime_gate(...)
# --------------------------------------------------------------------------- #
def run_one_market_with_live_gate(
    players: Sequence[str],
    p_win: float,
    market_price: float,
    bankroll: float,
    *,
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    break_point_size_factor: float = 0.0,
    max_staleness_s: float = DEFAULT_MAX_STALENESS_S,
    size_position_fn: Optional[Any] = None,
    **fetch_kwargs: Any,
) -> float:
    """Decide and (optionally) size a trade for one market, gated by live state.

    Returns the dollar amount the strategy would allocate. 0.0 means skip. This
    function NEVER places an order — execution stays with the caller.
    """
    state = fetch_live_tennis_state(
        players, api_key=api_key, base_url=base_url, **fetch_kwargs
    )

    decision = live_tennis_state_gate(
        state,
        break_point_size_factor=break_point_size_factor,
        max_staleness_s=max_staleness_s,
    )

    if not decision.allowed:
        print(
            f"[tennis-gate] skip players={list(players)} "
            f"reason={decision.reason} "
            f"status={decision.status} "
            f"break_point={decision.break_point} "
            f"stale={decision.stale}"
        )
        return 0.0

    print(
        f"[tennis-gate] allow players={list(players)} "
        f"status={decision.status} "
        f"break_point={decision.break_point} "
        f"size_factor={decision.size_factor:.2f} "
        f"as_of={decision.as_of}"
    )

    # Gate passed -> proceed to sizing as usual, scaled by the gate's factor.
    if size_position_fn is None:
        from simmer_sdk import size_position as size_position_fn  # lazy import

    base = size_position_fn(
        p_win=p_win,
        market_price=market_price,
        bankroll=bankroll,
    )
    return float(base) * decision.size_factor


# --------------------------------------------------------------------------- #
# CLI: self-contained demo by default; --live-data hits the real sources.
# --------------------------------------------------------------------------- #
_DEMO_MATCHES = [
    {
        "label": "clean live state (allow)",
        "match": {
            "id": 1,
            "status": "live",
            "event_status": None,
            "players": {"p1": {"name": "Carlos Alcaraz"}, "p2": {"name": "Jannik Sinner"}},
        },
        "score": {
            "server": 1,
            "points": ["30", "15"],
            "is_tiebreak": False,
            "timestamp": None,
        },
        "players": ["Carlos Alcaraz", "Jannik Sinner"],
    },
    {
        "label": "break point live (skip)",
        "match": {
            "id": 2,
            "status": "live",
            "event_status": None,
            "players": {"p1": {"name": "Iga Swiatek"}, "p2": {"name": "Aryna Sabalenka"}},
        },
        "score": {
            "server": 1,
            "points": ["30", "40"],  # receiver (p2) at 40, server at 30 -> break point
            "is_tiebreak": False,
            "timestamp": None,
        },
        "players": ["Iga Swiatek", "Aryna Sabalenka"],
    },
    {
        "label": "retirement (skip)",
        "match": {
            "id": 3,
            "status": "completed",
            "event_status": "Retired",
            "players": {"p1": {"name": "Novak Djokovic"}, "p2": {"name": "Daniil Medvedev"}},
        },
        "score": {"server": None, "points": [None, None], "is_tiebreak": False, "timestamp": None},
        "players": ["Novak Djokovic", "Daniil Medvedev"],
    },
]


def _demo(now: float = 0.0) -> None:
    """Run the gate over inlined fixtures — no network, no keys required."""
    print("Live-tennis gate demo (fixtures; no network, places no orders)\n")

    def _size(p_win: float, market_price: float, bankroll: float) -> float:
        # A transparent stand-in for simmer_sdk.size_position for the demo.
        edge = max(0.0, p_win - market_price)
        return round(bankroll * edge, 2)

    for case in _DEMO_MATCHES:
        state = fetch_live_tennis_state(
            case["players"],
            api_key="demo",
            now=now,
            live_matches=[case["match"]],
            score_fetch=lambda _id, s=case["score"]: s,
            match_fetch=lambda _id, m=case["match"]: m,
        )
        amount = run_one_market_with_live_gate(
            case["players"],
            p_win=0.62,
            market_price=0.55,
            bankroll=1000.0,
            api_key="demo",
            now=now,
            live_matches=[case["match"]],
            score_fetch=lambda _id, s=case["score"]: s,
            match_fetch=lambda _id, m=case["match"]: m,
            size_position_fn=_size,
        )
        print(f"    -> {case['label']}: sized ${amount:.2f}\n")


def _run_live_data() -> None:
    """Gate real Polymarket tennis markets against real Live Tennis API state.

    Fetches markets via SimmerClient (mirrors regime_gate_skill.py's __main__)
    and live state from the Live Tennis API. Still places no orders.
    """
    lt_key = os.environ.get("LIVETENNIS_API_KEY")
    if not lt_key:
        raise SystemExit(
            "LIVETENNIS_API_KEY not set. Get a FREE key at "
            "https://livetennisapi.com/subscribe/free"
        )
    sim_key = os.environ.get("SIMMER_API_KEY")
    if not sim_key:
        raise SystemExit("SIMMER_API_KEY not set; --live-data needs it to list markets.")

    from simmer_sdk import SimmerClient

    client = SimmerClient(api_key=sim_key)
    markets = client.get_markets(import_source="polymarket", limit=25)
    if not markets:
        raise SystemExit("No markets available.")

    # Resolve each market's players with the polymarket-tennis toolkit if present.
    try:
        from polymarket_tennis import extract_market_players  # type: ignore
    except ImportError:
        extract_market_players = None  # noqa: N816

    for m in markets:
        players = None
        if extract_market_players is not None:
            mp = extract_market_players(m)
            if mp is not None:
                players = [mp.player_a, mp.player_b]
        if players is None:
            # Fallback: the caller must supply players it trusts. Skip otherwise.
            continue

        run_one_market_with_live_gate(
            players,
            p_win=0.55,
            market_price=getattr(m, "current_probability", 0.5),
            bankroll=1000.0,
            api_key=lt_key,
        )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Live-tennis match-state gate for Simmer/Polymarket tennis markets. "
            "Observe-only: it emits a gate decision and a suggested size; it "
            "places no orders (real-money or paper)."
        )
    )
    parser.add_argument(
        "--live-data",
        action="store_true",
        help=(
            "Gate real Polymarket tennis markets against real Live Tennis API "
            "state (needs LIVETENNIS_API_KEY and SIMMER_API_KEY). NOTE: this "
            "uses LIVE DATA sources; it does not place any trade."
        ),
    )
    args = parser.parse_args(argv)

    if args.live_data:
        _run_live_data()
    else:
        _demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
