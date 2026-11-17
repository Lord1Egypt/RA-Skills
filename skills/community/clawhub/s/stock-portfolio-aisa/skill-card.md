## Description:

Create and manage stock and crypto portfolios with live AISA pricing and P&L tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local stock and crypto portfolios, add or update holdings, rename portfolios, and review current profit and loss using live AISA pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_API_KEY can be sent to a configurable external endpoint.

Mitigation: Run only with a trusted AISA_BASE_URL and use a narrowly scoped, rotatable API key.

Risk: Displayed live prices may be incorrect or incomplete.

Mitigation: Verify prices independently before making financial decisions.

Risk: Portfolio remove and delete operations immediately modify the local portfolio file.

Mitigation: Review commands before execution and keep backups or an isolated CLAWDBOT_STATE_DIR for important portfolio data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-portfolio-aisa)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and writes portfolio state to a local JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
