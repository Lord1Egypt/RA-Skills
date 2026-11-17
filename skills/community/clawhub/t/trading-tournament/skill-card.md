## Description:

Run autonomous multi-agent trading competitions on OKX. 5 AI agents compete with real-time market data, evolutionary selection replaces losers daily, exchange-level stop-losses protect capital. Battle-tested framework for algorithmic trading research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peti0402](https://clawhub.ai/user/peti0402)

### License/Terms of Use:


## Use Case:

Developers and trading-system operators use this skill to configure and run autonomous OKX trading competitions where multiple AI strategies analyze market data, execute trades, and rotate strategies based on performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an autonomous trading system that may use live OKX funds.

Mitigation: Start with OKX demo credentials, keep withdrawal permissions disabled, and set strict account and exchange limits before any live use.

Risk: The recommended Guardian cron or Windows Task can persistently restart live trading without clear operational controls.

Mitigation: Review the actual code, restart command, permissions, disable procedure, and failure limits before enabling persistent restart behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peti0402/skills/trading-tournament)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, trading configuration guidance, operational checklists, and safety guidance for OKX demo or live trading.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
