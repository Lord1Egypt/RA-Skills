## Description:

Automated Trading System with Multi-Strategy Voting

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikachu022700](https://clawhub.ai/user/pikachu022700)

### License/Terms of Use:


## Use Case:

External developers and traders can use this skill as a paper-trading oriented quant trading system for strategy voting, simulated position management, status reporting, and dashboard-style inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary identifies under-disclosed unauthenticated dashboard servers exposed beyond localhost.

Mitigation: Bind dashboard services to 127.0.0.1, add authentication before network exposure, and avoid importing dashboard.py unless starting a server is intended.

Risk: The security guidance says to treat the package as a paper-trading/demo tool rather than a safe live trading system.

Mitigation: Use it for paper trading or review only, validate all trading logic and external dependencies independently, and do not rely on mock or simplified indicators for financial decisions.

Risk: The artifact depends on the Hyperliquid API for market data.

Mitigation: Confirm the Hyperliquid API dependency is acceptable in the deployment environment and handle API failures before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikachu022700/skills/quant-trading-system)
- [Project homepage](https://clawhub.com/quant-trading-system)
- [Hyperliquid info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paper-trading status, strategy signals, JSON-like summaries, and dashboard endpoints when the included scripts are run.]

## Skill Version(s):

6.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
