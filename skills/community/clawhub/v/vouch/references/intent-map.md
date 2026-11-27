# Claim to Telegraph intent map

Starting points only. Confirm with `telegraph_find_intents`, then read the intent's `params` and `answer_fields` with `telegraph_intent`, because intents and miners change. Seen on the Telegraph devnode on 2026-11-26. Rows marked (unchecked) come from intent search results only and were not asked.

| Claim looks like | Intent | Params | Compare these answer fields |
|---|---|---|---|
| Gas on Ethereum is under N gwei | GAS_PRICE_GENERAL | chain | gas_price_gwei, as_of |
| Team A beat Team B N-M on DATE (finished game) | GAME_RESULT_GENERAL | game ("A vs B, YYYY-MM-DD") | winner, home_team, away_team, home_score, away_score, date |
| Token T has total supply N | TOKEN_TOTAL_SUPPLY_VERIFY_GENERAL | token (symbol or contract, and chain) | total_supply |
| BTC is at $N (unchecked) | CRYPTO_PRICE_USD | symbol | current price only |
| AAPL trades at $N (unchecked) | STOCK_PRICE_US_EQUITY | ticker | current price only |
| The score is N-M, game in progress (unchecked) | SPORTS_SCORE_GENERAL | fixture | score fields |
| EVENT had outcome X (unchecked) | EVENT_OUTCOME_RESOLUTION_GENERAL | event | outcome, past events only |
| Address A held N ETH at block B (unchecked) | ONCHAIN_METRIC_VERIFY_GENERAL | address, block, chain | balance, nonce |
| Token has N holders (unchecked) | TOKEN_HOLDER_COUNT_GENERAL | token | holder count |
| Reserves back the stablecoin (unchecked) | ASSET_RESERVE_ATTESTATION_GENERAL | asset | attestation fields |
| CVE-N has CVSS S (unchecked) | CVE_LOOKUP_CVSS | cve | cvss score |
| IP X is clean (unchecked) | THREAT_IP_REPUTATION_GENERAL | ip | risk score |
| Power price at a hub is N (unchecked) | GRID_POWER_PRICE_GENERAL | hub or region | price fields |

Not checkable (report cannot verify without spending): opinions, forecasts, events after today, private or local data, anything with no matching intent.

Tolerance hints: live prices and gas move, so compare against a stated bound (`lt`, `gt`) or `pct:` and read `as_of`; game results, supplies and filing facts are `exact`.
