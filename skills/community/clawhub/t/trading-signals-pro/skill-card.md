## Description: <br>
Crypto trading signals using CoinGecko price data, DeFiLlama TVL trends, and CCXT exchange order flow for momentum, RSI, VWAP, DeFi yield, and portfolio scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to generate crypto market research signals for assets and DeFi pools using public market data. It supports momentum, RSI, VWAP, DeFi yield, and portfolio dashboard workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generated trading signals as guaranteed financial advice. <br>
Mitigation: Treat outputs as market research only and require independent review before making trading or portfolio decisions. <br>
Risk: Credential exposure if users provide exchange trading keys or wallet credentials. <br>
Mitigation: Use only a limited CoinGecko API key and do not provide exchange trading keys, wallet credentials, or private keys. <br>
Risk: Behavior may change if code is supplied outside the reviewed package. <br>
Mitigation: Verify the source of any trade_signals.py or other code supplied outside this package before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drivenautoplex1/trading-signals-pro) <br>
- [Project Homepage](https://github.com/drivenautoplex1/openclaw-skills) <br>
- [SaucerSwap Pools API](https://api.saucerswap.finance/pools) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, guidance] <br>
**Output Format:** [JSON with a human-readable Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes asset signals, signal strength, market context, top picks, avoidance notes, and DeFi yield details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
