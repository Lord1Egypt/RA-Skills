## Description: <br>
Momentum-based trading skill for Simmer prediction markets that detects probability momentum and divergence to generate YES/NO Polymarket trade signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrjoeteam](https://clawhub.ai/user/mrjoeteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation users use this skill to monitor selected Simmer watchlist markets, evaluate a configurable probability-divergence signal, and dry-run or execute Polymarket YES/NO trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with live trading enabled can place real Polymarket trades. <br>
Mitigation: Keep the skill in dry-run until the strategy and SDK behavior are reviewed, restrict MARKET_IDS, and use a small TRADE_AMOUNT. <br>
Risk: The skill requires a Simmer API key. <br>
Mitigation: Provide SIMMER_API_KEY through the environment only, avoid hardcoding credentials, and rotate the key if it is exposed. <br>
Risk: Momentum and divergence signals can be wrong or perform poorly in volatile markets. <br>
Mitigation: Review the default signal, threshold, market context checks, and trade amount before relying on the strategy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrjoeteam/simmer-momentum-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown setup guidance with Python command examples and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires simmer-sdk, SIMMER_API_KEY, and selected market IDs; defaults to dry-run unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
