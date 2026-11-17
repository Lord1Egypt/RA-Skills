# Disclaimer

This skill is a **decision-support gate**, not a production trading system, and
not financial advice. Read this in full before wiring it into anything that
moves money.

## Vendor disclosure

This skill is **vendor-authored** by the Live Tennis API team
(https://livetennisapi.com). The live match state it reads — score, server,
break-point flag, match status — comes from our own feed. Judge its claims
accordingly.

## Observe-only

This skill **places no orders**, real-money or paper. It returns a trade /
no-trade decision and the dollar amount a strategy *would* allocate. Whether,
when, and how to act on that decision is entirely the calling framework's
responsibility. Nothing here signs, submits, or cancels an order.

## No financial advice, no validated edge

The gate conditions (skip on a live break point, skip on a stopped match, fail
closed on stale/undetermined state) are a conservative, defensible starting
point — not a tested edge. They do not estimate probability of winning or
market value; you must supply your own `p_win`. Suitability for any account size
or risk tolerance is yours to assess.

## Data can be missing, late, or wrong

Live sports data is best-effort. The score endpoint is a point-in-time snapshot
that can lag the match, and player-name pairing can mis-resolve. The gate fails
**closed** on anything it cannot verify (missing match, stale snapshot,
undetermined break point), so its failure mode is "skip", not "trade blind" —
but do not treat an `allowed=True` as a guarantee the state is correct. Set
`max_staleness_s` honestly for how often you can actually read (the FREE tier is
100 requests/day).

## Use at your own risk

By using this skill you agree the authors are not liable for any losses, direct
or indirect, arising from its use or from the data it surfaces.

## Where to learn more

- This skill's `SKILL.md` documents the gate logic and every skip reason.
- Live Tennis API docs: https://docs.livetennisapi.com
- The reference pattern: simmer-sdk `examples/regime_gate_skill.py`.
