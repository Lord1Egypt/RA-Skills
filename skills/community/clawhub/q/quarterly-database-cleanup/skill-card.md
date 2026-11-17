## Description:

Run a comprehensive quarterly CRM audit covering list health, bounce monitoring, data quality, scoring calibration, engagement metrics, property cleanup, and quarter-over-quarter health reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

CRM operations and marketing operations teams use this skill to run a quarterly HubSpot database health audit, compare current metrics with the previous quarter, and produce prioritized cleanup actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a HubSpot API token that can give the agent read access to CRM data.

Mitigation: Confirm the token scope and data access are appropriate before installation, and prefer a least-privilege token for audit use.

Risk: The skill writes an audit report under reports/ and may conflict with an existing report for the same quarter.

Mitigation: Check for an existing quarterly report before running the workflow and rename or archive prior output when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/quarterly-database-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown report with checklist findings, trend comparison tables, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local quarterly cleanup report under reports/ when the agent follows the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
