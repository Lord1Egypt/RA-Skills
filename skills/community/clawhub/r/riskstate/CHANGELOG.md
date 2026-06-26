# Changelog

All notable changes to the RiskState API will be documented in this file.

## [1.4.0] - 2026-04-22

### Added
- **Policy combiner refinements (PR3)** — Five additive refinements to `policy_permissions`, all surfaced in the response and the audit `policy_hash`:
  - **TREND / RANGE weight split** — `TREND` blends 0.65 structural / 0.35 tactical (continuation-led); `RANGE` 0.55 / 0.45 (tactical has more voice). PANIC, EUPHORIA, and SQUEEZE weights unchanged.
  - **DQ-gated structural veto** — structural veto is skipped when `structural_score.data_quality < 60`, emitting `STRUCTURAL_VETO_SKIPPED_LOW_DQ`. Prevents low-confidence structural reads from overriding clean tactical signals.
  - **PANIC SHORT override** — PANIC regime exempts SHORT positions from the strong-structural veto (`STRUCTURAL_VETO_SKIPPED_PANIC`), so dead-cat-bounce / fake-breakout setups are not blocked.
  - **Bucket codes in `reason_codes`** — typed tokens (e.g. `TACTICAL_STRONG_BULL_72`, `STRUCTURAL_WEAK_22`) replace raw scores for downstream classification.
  - **`shadow_max_size_fraction`** — read-only preview of a candidate combiner-driven sizing rule. Does not bind today; surfaced for offline comparison.

### Changed
- Policy hash inputs widened to cover the new bucket codes and shadow size — cached hashes from v1.3.0 will not match (one-time invalidation).

## [1.3.0] - 2026-04-21

### Added
- **Decoupled Structural + Tactical scores + policy combiner (PR2)** — Splits the single composite into two layers that each drive the appropriate decision:
  - `structural_score` — slow horizon (weeks-months): cycle, supply, demand, macro. `{overall, label, subfamilies, data_quality, source}`.
  - `tactical_score` — fast horizon (24-72h): positioning pressure, momentum, volume/CVD, derivatives extremity, L/S velocity, whale pressure. `{overall, label, components, signals}`.
  - `policy_permissions` — context-aware combiner producing `risk_permission_score`, regime-dependent weights, `direction_bias`, `direction_layer` (audit), and `reason_codes`.

### Changed
- **`exposure_policy.direction_bias` now comes from the combiner** (was composite-tilt). Breaking semantics.
- `exposure_policy.direction_layer` added — audit field showing which layer drove direction.
- Existing `composite` retained for backwards compatibility; `max_size_fraction` still driven by the legacy 4-cap engine.

## [1.2.1] - 2026-04-21

### Added
- **Positioning Pressure Score (PR1)** — continuous 0-100 tactical signal derived from the squeeze scorer (50 = neutral, >50 short-squeeze setup). Wired into BTC and ETH composite as a 9% subscore. Response gains `positioning.positioning_pressure_score` and `positioning.positioning_pressure_net`.

### Changed
- **ETH issuance recalibration** — asymmetric bands + 7d/30d blend. Mild post-Merge inflation (+0.82%/yr) now scores ~53 (was ~30); hard-downgrade threshold raised to >+2.0%/yr.

## [1.2.0] - 2026-03-19

### Added
- **Usage tracking** — Monthly and total API call counts per key, visible in admin panel
- **Bybit V5 + OKX V5 fallback chain** — Funding rate and OI now have 4-level fallback: Binance → OKX → Bybit → CoinGlass → default. 98%+ uptime for positioning data
- **DXY in API** — Frankfurter EUR/USD proxy added to API (was missing, affected regime classification)
- **Aave V3 support** — DeFi position monitoring now supports both Spark Protocol and Aave V3 with per-collateral liquidation thresholds

### Fixed
- **BTC cycle phase alignment** — API now replicates exact dashboard 9-branch priority order (was simplified 6-branch, causing POST-PEAK vs CORRECTION divergence)
- **Regime classification fix** — Missing DXY caused false BEAR regime in API (DXY defaulted to 100 → extra bearSignal)
- **ETH structural score** — Now fetches real data (was hardcoded null → default 50). Lido staking, burn rate, DEX volume, fees, stablecoin TVL all live
- **Macro regime alignment** — API now calls macro.js as single source of truth (was divergent inline computation)

## [1.1.1] - 2026-03-16

### Added
- **English standardization** — All API responses in English (was mixed Spanish/English)
- **ETH Structural Score v2.2** — Widened issuance bands, lending heat directional scoring, hard/soft downgrade reclassification
- **Weighted warnings in rules cap** — Structural warnings (slow-moving) penalize 0.5x vs tactical 1.0x

### Fixed
- **False BLOCK prevention** — Mild ETH inflation (+0.3%/yr) no longer triggers defensive policy
- **CoinGlass fallback fixes** — OI, L/S ratio, MVRV fallback chains corrected (wrong field names, unused data)

## [1.1.0] - 2026-03-13

### Added
- **Deterministic API contract** — `allowed_actions` and `blocked_actions` use uppercase enum tokens (DCA, WAIT, LEVERAGE_GT_2X) instead of free-text
- **`reason_codes`** — Machine-parseable tokens in `binding_constraint` (e.g., MACRO_RISK_OFF, COUPLING_NORMAL)
- **`ttl_seconds`** — Cache TTL in response (60s) for agent scheduling
- **`binding_constraint.source` uppercased** — RULES, DEFI, MACRO, CYCLE (consistent enum style)

### Changed
- **SKILL.md rewritten** — Binding precedence section, decision rules table, failure modes table, updated example response

## [1.0.0] - 2026-03-12

### Added
- **Initial release** — `POST /v1/risk-state` endpoint
- **5-level policy engine** — BLOCK (1-2) → CAUTIOUS (3) → GREEN (4-5)
- **Multi-asset support** — BTC and ETH with asset-specific scoring
- **4-cap system** — Rules, DeFi, Macro, Cycle caps × quality × volatility adjustment
- **30+ real-time signals** — Macro, on-chain, derivatives, DeFi health, sentiment
- **DeFi-aware** — Optional wallet parameter for Spark/Aave V3 health factor integration
- **SHA-256 policy hash** — Deterministic audit trail for non-repudiation
- **Hierarchical risk flags** — `structural_blockers` (hard stop) vs `context_risks` (reduce conviction)
- **60s Blob cache** — Skip cache when wallet parameter provided
- **Bearer auth** — Fail-closed authentication
- **SKILL.md** — Agent discovery file for skills.sh and agentskills.io ecosystems
- **Full API documentation** — docs/api-v1.md with field types, error codes, interpretation guide
