## Description:

Generates and reviews Python trading strategy code for the JoinQuant platform, with guidance for JoinQuant APIs, backtesting, simulation, troubleshooting, and strategy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to draft, inspect, and refine JoinQuant-compatible Python strategy code. It is intended for code assistance and platform guidance, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated and bundled examples can contain live-capable trading logic, including orders, cash movement, margin behavior, file access, messaging, network access, credentials, or unpinned third-party code.

Mitigation: Review every strategy line before running it in a real account, test in backtesting or simulation first, and remove unsafe data-loading, credential, network, and execution paths unless explicitly required.

Risk: Strategy examples and optimization guidance may be mistaken for investment advice or copied into production without market, liquidity, compliance, or risk checks.

Mitigation: Treat the skill as code assistance only, require human investment review, and validate assumptions, position sizing, stop-loss behavior, data timing, and regulatory constraints before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-joinquant-trader)
- [Skill instructions](artifact/SKILL.md)
- [Selected strategies index](artifact/assets/小果精选策略.txt)
- [2025 selected strategies](artifact/assets/2025年度精选策略.txt)
- [ETF core asset rotation strategy notes](artifact/references/ETF策略之核心资产止损轮动/策略原理.txt)
- [Fixed-income rebalancing strategy notes](artifact/references/17固收再平衡/策略原理.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JoinQuant API usage notes, backtest guidance, diagnostics, and trading-code review comments.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
