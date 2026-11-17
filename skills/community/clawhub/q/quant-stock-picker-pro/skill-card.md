## Description:

AI-powered stock screening tool for Chinese A-shares. Daily picks using multi-factor analysis (fundamentals + technical + sentiment). Use when user asks about stock screening, quantitative trading, or investment opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric961](https://clawhub.ai/user/eric961)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate Chinese A-share stock screening reports with ranked candidates, factor scores, risk notes, and setup guidance. The reports are for informational review and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be configured for unattended weekday execution and may act on changing market data without user review.

Mitigation: Do not enable the cron schedule unless unattended runs are intended; review each generated report before using it for any decision.

Risk: The scripts install broad dependencies and make live network requests to financial and sentiment data sources.

Mitigation: Run in an isolated environment with pinned dependencies and network access limited to approved data sources.

Risk: The main script changes proxy-related environment variables and includes a hard-coded local path.

Mitigation: Remove local path assumptions and proxy overrides before deployment in a shared or production environment.

Risk: The skill produces stock recommendations that may be inaccurate, stale, or unsuitable for a user's risk profile.

Mitigation: Treat outputs as experimental screening information, not investment advice, and require qualified human review.

## Reference(s):

- [Factor Library](references/factors.md)
- [ClawHub Skill Page](https://clawhub.ai/eric961/skills/quant-stock-picker-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with ranked stock picks, risk disclosures, setup commands, configuration examples, and optional CSV output from the provided script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live market and sentiment data sources and include informational financial screening content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
