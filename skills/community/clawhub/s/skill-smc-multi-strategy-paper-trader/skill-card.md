## Description:

Paper trading monitors for Smart Money Concepts and macro rotation strategies that use public market data to generate regime scores, simulated portfolio updates, and runnable monitor workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run and schedule crypto paper-trading monitors that simulate strategy entries, exits, portfolio P&L, and regime classification without exchange account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Several scripts may read a local GitHub token and upload portfolio data to a fixed GitHub repository.

Mitigation: Review before installing, run only in an isolated environment or after removing/disabling the GitHub push blocks, and do not keep ~/.github_token available unless that sync is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-smc-multi-strategy-paper-trader)
- [zero2ai-hub publisher profile](https://clawhub.ai/user/zero2ai-hub)
- [Binance Futures public market data endpoint](https://fapi.binance.com)
- [FRED graph CSV endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv)
- [Fear and Greed Index API](https://api.alternative.me/fng/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with runnable shell commands and JSON/file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for local Node.js scripts that create JSON portfolio and regime files; exchange account credentials are not required.]

## Skill Version(s):

2.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
