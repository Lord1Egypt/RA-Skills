# simmer-tennis-live-gate

A **live-tennis match-state gate** for [Simmer](https://simmer.markets) /
Polymarket tennis markets, packaged as a [ClawHub](https://clawhub.ai) skill.

> **Vendor-authored.** We run the [Live Tennis API](https://livetennisapi.com).
> The live match state this gate reads comes from our feed — this is a
> vendor-authored integration, so judge it accordingly.

## What it is

This is the tennis analog of simmer-sdk's `examples/regime_gate_skill.py`, mirrored
line-for-line. The regime example gates a strategy on a realized-volatility
*regime* read off a candle series. This skill gates a strategy on the **actual
tennis match state** read off the Live Tennis API — the score, who is serving,
whether a **break point** is live, and whether the match has **stopped**
(retirement, walkover, in-play suspension).

The gate is a **precondition to sizing**: fetch the signal, run the gate, skip
(never fall through) when it says no, and only then size the position. A strategy
that means to trade a calm mid-match state should not fire into a break point, and
must not trade a market whose match has already retired.

### Observe-only

This skill **places no orders — real-money or paper.** It returns a trade/no-trade
decision and the dollar amount a strategy *would* allocate; execution stays with
the calling framework, exactly as in `regime_gate_skill.py`. There is no `--live`
real-money flag here because there is no trading here at all. See
[DISCLAIMER.md](./DISCLAIMER.md).

## Gate logic

Skip (`allowed=False`), in order: `state_unavailable` (no live match matched the
players), `match_not_live` (upcoming/completed), `retirement` (Retired/Walk Over),
`interrupted` (paused), `state_stale` (snapshot older than `max_staleness_s`),
`state_undetermined` (break point UNDEF — server/points null), `break_point_live`.

Allow (`allowed=True`): `ok` at `size_factor=1.0`, or `break_point_downsize` at a
configurable factor when a break point is live and you chose to trim rather than
skip. The gate **fails closed** on everything it cannot verify.

**Break-point derivation** is three-valued: receiver at AD, or receiver at 40 vs
server at 0/15/30; never in a tiebreak; **UNDEF** (`None`) when the server or
in-game points are null. It matches the derivation in our MIT-licensed
[polymarket-tennis](https://github.com/livetennisapi/polymarket-tennis) toolkit,
tightened to expose UNDEF rather than collapse it to "no break point".

## Install & run

```bash
git clone https://github.com/livetennisapi/simmer-tennis-live-gate
cd simmer-tennis-live-gate

# Self-contained demo over inlined fixtures — no network, no keys, no orders:
python tennis_live_gate_skill.py

# Probe the live state + gate decision for a real pair of players (read-only):
export LIVETENNIS_API_KEY=...   # FREE key: https://livetennisapi.com/subscribe/free
python scripts/status.py "Carlos Alcaraz" "Jannik Sinner"

# Gate real Polymarket tennis markets (needs SIMMER_API_KEY too). Still no orders:
export SIMMER_API_KEY=sk_live_...
python tennis_live_gate_skill.py --live-data
```

The only runtime dependency is `simmer-sdk` (used for `size_position` and, under
`--live-data`, to list markets). The gate and the Live Tennis API reads use the
Python standard library only (`urllib`).

## Free-tier limits (plainly)

The FREE Live Tennis API key is **30 requests/min, 100 requests/day** — live
scores, fixtures and players. That is enough for gate checks at decision time and
for develop-and-test, but **not** continuous fast polling (100/day is roughly one
check every ~15 minutes). Set `max_staleness_s` to match how often you can actually
read. Per-point freshness is a paid concern, not a free-tier one. Get a free key at
<https://livetennisapi.com/subscribe/free>.

## Tests

```bash
python -m unittest discover -s tests -v   # 33 tests, no network, no keys
```

All tests are fixture-driven: the Live Tennis API reads and the `size_position`
call are injected, so nothing hits the network.

## Publishing to ClawHub

ClawHub lists a published skill in the Simmer registry automatically. Publishing is
an external account action.

**Ben does (once):** create/sign in to an account at <https://clawhub.ai> under the
Live Tennis org identity. No Simmer `sk_live` key is needed to *publish* — ClawHub
reads this folder's `SKILL.md` frontmatter and `clawhub.json`.

**Then a session runs (from this repo root):**

```bash
npx clawhub@latest publish . --slug simmer-tennis-live-gate --version 0.1.0
```

The Simmer sync job picks it up within ~1 hour (hourly at :45 UTC) and lists it at
<https://simmer.markets/skills>. No approval step.

> **Validator note.** simmer-sdk's `validate_skill.py` is written for *auto-run
> trader* skills, so it flags a missing `automaton.entrypoint`. That is expected
> and correct here: this is an **observe-only** skill with no auto-trading loop
> (the published read-only `polymarket-wallet-xray` skill omits `automaton` for
> the same reason). `npx clawhub@latest publish` does not require that check —
> it reads `SKILL.md` frontmatter and `clawhub.json`, both present and valid.

### The `sk_live` caveat (stated plainly)

End-to-end validation of the `--live-data` path — actually listing real Polymarket
markets via `SimmerClient` — needs a **live Simmer `sk_live` API key, which we do
not have.** Everything else is fully exercised without it:

- the gate logic, break-point derivation, staleness, and fail-closed paths (33
  mocked tests);
- the FREE-tier Live Tennis API reads and the `scripts/status.py` probe (a FREE
  Live Tennis key is enough — no Simmer key involved);
- publishing to ClawHub (reads `SKILL.md` + `clawhub.json`; no `sk_live` needed).

So the skill is publish-ready and its gate is fully tested; only the optional
`--live-data` market-listing round-trip is unverified end-to-end for want of an
`sk_live` key.

## License

MIT — see [LICENSE](./LICENSE).
