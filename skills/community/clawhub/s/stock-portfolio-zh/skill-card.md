## Description:

Creates and manages stock and crypto portfolios with AISA-based price and profit/loss tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, update, rename, delete, and review local stock and crypto portfolios from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AISA API key may be sent to a configurable API endpoint if AISA_BASE_URL is changed.

Mitigation: Use a narrowly scoped AISA API key and set AISA_BASE_URL only to endpoints you fully trust.

Risk: Displayed prices and profit/loss values may be inaccurate because they come through AISA/model responses.

Mitigation: Check an authoritative market-data source before relying on displayed prices or profit/loss for financial decisions.

Risk: Remove and delete commands permanently change local portfolio data.

Mitigation: Back up the local portfolio state file before destructive portfolio operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bibaofeng/skills/stock-portfolio-zh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; writes local portfolio state under CLAWDBOT_STATE_DIR or ./.clawdbot.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
