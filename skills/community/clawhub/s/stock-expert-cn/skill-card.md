## Description:

Provides stock market analysis, technical indicator interpretation, stock screening, investment guidance, risk notes, and position-management suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sionyugg-a11y](https://clawhub.ai/user/sionyugg-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate market reports, analyze individual stocks, screen candidate stocks, and receive risk-aware portfolio guidance. It is oriented toward stock research workflows using Tushare and optional Finnhub market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a real-looking embedded Tushare token.

Mitigation: Remove the embedded token before use and provide a user-owned token through a secure environment variable or secret store.

Risk: The release evidence warns that dependency examples encourage system-wide Python installation.

Mitigation: Install dependencies in an isolated virtual environment instead of using system-wide installation.

Risk: The release evidence notes persistent scheduled agent runs through cron examples.

Mitigation: Treat scheduled runs as optional automation and configure explicit names, expiry, and removal commands before enabling them.

Risk: The skill produces investment-oriented analysis and recommendations that may be incomplete or unsuitable for a specific user.

Mitigation: Use outputs as research support only, verify market data and assumptions, and apply independent financial review before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sionyugg-a11y/skills/stock-expert-cn)
- [Publisher Profile](https://clawhub.ai/user/sionyugg-a11y)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on external market-data APIs and configured credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
