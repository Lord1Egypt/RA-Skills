## Description:

Crypto trading signals using CoinGecko price data, DeFiLlama TVL trends, and CCXT exchange order flow for momentum, RSI, VWAP, and DeFi yield analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for crypto market summaries, trading-signal analysis, DeFi yield scans, and portfolio watchlist dashboards. It produces informational market analysis from public market-data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound market-data API calls and depends on external services.

Mitigation: Install it only in environments where outbound calls to market-data providers are acceptable, and review network access before deployment.

Risk: The skill requires a CoinGecko API key.

Mitigation: Use a limited CoinGecko key and avoid exposing unrelated secrets to the skill runtime.

Risk: The evidence notes that the referenced trade_signals.py file is absent.

Mitigation: Confirm the packaged implementation is present and runnable before relying on the skill in agent workflows.

Risk: The evidence notes unpinned dependencies.

Mitigation: Pin and review dependency versions before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/trading-signals-pro)
- [Publisher profile](https://clawhub.ai/user/drivenautoplex1)
- [Homepage from skill metadata](https://github.com/drivenautoplex1/openclaw-skills)
- [SaucerSwap pools API](https://api.saucerswap.finance/pools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON plus human-readable Markdown summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require python3, the requests and ccxt packages, outbound public market-data API access, and COINGECKO_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
