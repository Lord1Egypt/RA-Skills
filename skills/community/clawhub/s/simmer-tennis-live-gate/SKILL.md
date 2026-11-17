---
name: simmer-tennis-live-gate
description: Gate Simmer/Polymarket tennis market entries on the live match state (score, who is serving, break-point flag, retirement/walkover/suspension) from the Live Tennis API. Observe-only — it returns a trade/no-trade decision and a suggested size; it places no orders. Modeled line-for-line on simmer-sdk's regime_gate_skill.py. Use when a tennis strategy should not fire into a break point or a stopped match.
metadata:
  author: Live Tennis API (hello@livetennisapi.com)
  version: "0.1.0"
  displayName: Tennis Live-State Gate
  difficulty: intermediate
  attribution: Vendor-authored by the Live Tennis API team. Live match state comes from our feed — judge accordingly.
---
# Tennis Live-State Gate

> **Vendor-authored.** We run the [Live Tennis API](https://livetennisapi.com).
> The live match state this gate reads comes from our feed — judge accordingly.

Gate a tennis strategy's entry on the **actual match state**. This is the tennis
analog of simmer-sdk's `examples/regime_gate_skill.py`: fetch an external signal,
run a gate as a *precondition* to sizing, skip (never fall through) when the gate
says no, and only then call `size_position(...)`.

Where the regime gate reads a realized-volatility regime off a candle series, this
gate reads the real match state off the Live Tennis API — the score, who is
serving, whether a **break point** is live, and whether the match has **stopped**
(retirement, walkover, suspension). A strategy that means to trade a calm mid-match
state should not fire into a break point, and must not trade a market whose match
has already retired.

> 🎾 **Observe-only. Places no orders — ever.** This skill returns a gate decision
> and the dollar amount a strategy *would* allocate. Execution stays with the
> calling framework, exactly as in `regime_gate_skill.py`. There is no `--live`
> real-money path here because there is no trading here at all. Read
> [DISCLAIMER.md](./DISCLAIMER.md).

## What it does

1. **Resolve** the market's two players (folded last-name match; the fuller
   reversed-name / diacritic / confidence heuristics live in our MIT-licensed
   [polymarket-tennis](https://github.com/livetennisapi/polymarket-tennis) toolkit).
2. **Fetch** live state from the FREE Live Tennis API tier:
   - `GET /matches?status=live` — find the live match for the two players
   - `GET /matches/{id}/score` — score, server, points, is_tiebreak, timestamp
   - `GET /matches/{id}` — status + `event_status` (Retired / Walk Over / Interrupted)
3. **Gate.** `live_tennis_state_gate(...)` returns a binary allow/skip plus a
   `size_factor`. It fails **closed** on anything it cannot verify.
4. **Size.** When allowed, the reference flow calls `size_position(...)` scaled by
   `decision.size_factor` (1.0 normally; a haircut on a break point if you chose to
   trim rather than skip). It returns the amount; it does not place the order.

## Gate logic (honest)

The gate returns `allowed=False` (skip) for, in order:

| reason | when |
|---|---|
| `state_unavailable` | no live match matched the two players |
| `match_not_live` | status is `upcoming` or `completed` |
| `retirement` | `event_status` is `Retired` or `Walk Over` |
| `interrupted` | `event_status` is `Interrupted` (rain/darkness/medical pause) |
| `state_stale` | score snapshot older than `max_staleness_s` (default 120 s) |
| `state_undetermined` | break point is **UNDEF** — server or points are null |
| `break_point_live` | a break point is live (unless you set a downsize factor) |

And `allowed=True` for:

| reason | size_factor |
|---|---|
| `ok` | 1.0 — clean live state |
| `break_point_downsize` | your `break_point_size_factor` (e.g. 0.5) when a break point is live and you chose to trim instead of skip |

**Break-point derivation** (three-valued): receiver at AD, or receiver at 40 while
the server is at 0/15/30. Never in a tiebreak. When the server or in-game points
are null/absent the state is **UNDEF** (`break_point=None`) and the gate fails
closed — it never guesses "no break point".

## Configuration

| env var | default | meaning |
|---|---|---|
| `LIVETENNIS_API_KEY` | — (required) | Live Tennis API key. FREE tier is enough. |
| `SIMMER_API_KEY` | — | Only for `--live-data`, to list real Polymarket markets. |
| `LIVETENNIS_BASE_URL` | `https://api.livetennisapi.com/api/public/v1` | API base override. |
| `break_point_size_factor` (config.json) | `0.0` | `0.0` skips on a live break point; `0.5` trims to half instead. |
| `max_staleness_s` (config.json) | `120.0` | Fail closed if the score snapshot is older than this. |

## Run it

```bash
# Self-contained demo over inlined fixtures — no network, no keys, no orders:
python tennis_live_gate_skill.py

# Gate real Polymarket tennis markets against real Live Tennis API state
# (needs LIVETENNIS_API_KEY + SIMMER_API_KEY). Still places no orders:
export LIVETENNIS_API_KEY=...   # https://livetennisapi.com/subscribe/free
export SIMMER_API_KEY=sk_live_...
python tennis_live_gate_skill.py --live-data
```

`--live-data` means *use live data sources*. It is **not** a real-money flag — this
skill never trades.

## Free-tier limits (say it plainly)

The FREE Live Tennis API key is **30 requests/min, 100 requests/day**. That covers
live scores, fixtures and players — enough for gate checks at decision time and for
develop-and-test, but **not** continuous fast polling (100/day is roughly one check
every ~15 minutes over a day). Size `max_staleness_s` to how often you can actually
read; if you need per-point freshness, that is a paid concern, not a free-tier one.

## Using the gate from your own skill

```python
from tennis_live_gate_skill import fetch_live_tennis_state, live_tennis_state_gate

state = fetch_live_tennis_state(["Carlos Alcaraz", "Jannik Sinner"], api_key=KEY)
decision = live_tennis_state_gate(state, break_point_size_factor=0.5)
if not decision.allowed:
    return  # skip — do NOT fall through to sizing
amount = your_size_fn(...) * decision.size_factor
```

The gate is a precondition to sizing; it does not estimate edge. Pair it with your
own `p_win`.
