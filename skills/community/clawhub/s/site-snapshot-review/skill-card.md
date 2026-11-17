## Description:

Review one supported site's exported snapshot records without reopening live browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and reviewers use this skill to summarize an exported Campus Copilot workspace snapshot for one supported site, including record counts and high-signal assignments, messages, or events, without treating the snapshot as live browser truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot reports may expose or summarize private site records such as assignments, messages, or events.

Mitigation: Provide only snapshots the user is authorized to review and keep outputs scoped to the selected exported site data.

Risk: A snapshot can be mistaken for current live browser state.

Mitigation: Treat outputs as read-only summaries of exported snapshot data and avoid claims about live browser truth.

## Reference(s):

- [Site Snapshot Review ClawHub listing](https://clawhub.ai/xiaojiou176/skills/site-snapshot-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; based only on exported snapshot data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
