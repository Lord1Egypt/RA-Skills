## Description:

Creates and manages stock and crypto portfolios with real-time price and profit/loss tracking through AISA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, update, list, rename, delete, and review stock or crypto portfolios from the command line. It helps track holdings, current prices, total value, and profit/loss using AISA live pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio data is stored locally and may include sensitive financial holdings.

Mitigation: Protect the CLAWDBOT_STATE_DIR state directory and avoid using shared or untrusted workspaces for sensitive portfolios.

Risk: The AISA API key and ticker list can be sent to an API endpoint selected by AISA_BASE_URL.

Mitigation: Use the default AISA endpoint or set AISA_BASE_URL only to an explicitly trusted service, and keep AISA_API_KEY protected.

Risk: Delete and remove commands permanently change local portfolio state.

Mitigation: Review destructive commands before execution and keep backups of portfolio state when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-portfolio-zh-aisa)
- [AISA API endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may create or update local portfolio state files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
