# Changelog

All notable changes to this skill are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project adheres to
semantic versioning.

## [0.1.0] - 2026-08-18

Initial release.

- `live_tennis_state_gate(...)` — a precondition gate over live tennis match
  state, modeled line-for-line on simmer-sdk's `examples/regime_gate_skill.py`.
  Returns a binary allow/skip plus a `size_factor`, and fails **closed** on
  unverifiable state.
- Skip reasons: `state_unavailable`, `match_not_live`, `retirement`,
  `interrupted`, `state_stale`, `state_undetermined`, `break_point_live`.
  Allow reasons: `ok`, `break_point_downsize`.
- `derive_break_point(...)` — three-valued (True / False / UNDEF) break-point
  derivation: receiver at AD, or receiver at 40 vs server at 0/15/30; never in a
  tiebreak; UNDEF when server or points are null.
- `fetch_live_tennis_state(...)` — assembles state from FREE-tier Live Tennis API
  endpoints (`/matches?status=live`, `/matches/{id}/score`, `/matches/{id}`)
  using stdlib `urllib` only. Test hooks for network-free fixtures.
- `run_one_market_with_live_gate(...)` — the reference flow, mirroring
  `run_one_market_with_regime_gate(...)`. Observe-only: returns a sized amount,
  never places an order.
- CLI: self-contained fixture demo by default; `--live-data` gates real
  Polymarket tennis markets against real Live Tennis API state.
- 33 mocked unit tests (no network); MIT licensed.
