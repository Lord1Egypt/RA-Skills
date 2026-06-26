# Project notes

This skill currently maps to the workspace project at:

- `projects/sim-trading/account.json`
- `projects/sim-trading/trades.jsonl`

Current default rules in the project:

- Initial cash: $10,000
- Allowed: US stocks, ETFs
- Disallowed: options, leverage, shorting
- Max single position: 30%
- Min cash: 10%
- Max high-vol positions: 3
- Max decision windows per day: 3
- Windows: `pre_or_open`, `intraday`, `near_close`

Current strategy label:

- `custom-intuition-opportunity-hunter`

Daily output should be a Chinese post-market recap with:

- account performance
- positions
- today's three decisions
- reasoning
- review and next watch items
