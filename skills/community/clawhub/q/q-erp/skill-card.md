## Description:

Q Erp provides read-only management queries for Qianyi ERP, covering business Q&A, boss briefings, daily operations, product sales, growth opportunities, sales rankings, and multi-day sales trends through q-claw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljqdh](https://clawhub.ai/user/ljqdh)

### License/Terms of Use:

MIT-0

## Use Case:

External ERP operators and business managers use this skill through an agent to ask read-only Qianyi ERP management questions and receive business summaries, rankings, trend analysis, profit or gross-margin estimates when available, and operational follow-up guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backend-provided authorization links could mislead users if the destination is not official.

Mitigation: Users should verify authorization link destinations before opening them or granting access.

Risk: Backend responses can influence visible business results and data-provenance wording.

Mitigation: Operators should ensure backend responses clearly distinguish real business records from demo or sandbox data.

Risk: ERP fields or dimensions may be missing or incomplete in backend results.

Mitigation: The agent should report missing backend fields as data gaps and avoid fabricating sales, profit, or diagnostic conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljqdh/skills/q-erp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text business response, with Markdown authorization links when required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ERP responses should be based on the current q-claw backend result and should preserve backend-provided business lines when returned verbatim.]

## Skill Version(s):

1.0.34 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
