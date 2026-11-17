## Description:

Save and track per-stock investment strategies with entry and exit conditions, then check tracked conditions against market data to produce next-step recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcsight](https://clawhub.ai/user/dcsight)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local Markdown record of stock strategy assumptions, entry conditions, stop-loss conditions, target prices, and check reports. It supports saving strategy details after analysis and generating review summaries when users ask to check tracked stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The save script can modify any agent-writable path when STOCK_SCHEME_PATH or --path points outside the intended strategy file.

Mitigation: Configure STOCK_SCHEME_PATH only to a dedicated Markdown file and avoid passing arbitrary --path values.

Risk: The documentation states path-validation and atomic-write protections that are not implemented in this version.

Mitigation: Treat those protections as unavailable for version 1.1.0 and review or back up the tracking file before automated saves.

Risk: The skill produces stock strategy recommendations from saved assumptions and market data.

Mitigation: Review recommendations before acting; the skill does not execute trades or connect to brokerage accounts.

## Reference(s):

- [Scheme Format Reference](references/scheme_format.md)
- [ClawHub Skill Page](https://clawhub.ai/dcsight/skills/stock-scheme-tracker)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown strategy entries, Markdown check reports, JSON parse output from scripts, and concise user-facing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses STOCK_SCHEME_PATH when configured and otherwise defaults to ~/Documents/stock/scheme.md.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
