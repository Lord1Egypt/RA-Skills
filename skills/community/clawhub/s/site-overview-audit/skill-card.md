## Description:

Summarize one supported site's current snapshot records and highest-signal items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and local workspace consumers use this skill to summarize one supported imported campus snapshot site, including counts, high-signal records, and recent updates, without mutating site state or claiming live browser truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill summarizes imported campus snapshot data, which may include sensitive academic or personal information.

Mitigation: Use it only when the operator is comfortable letting the agent read the specific imported snapshot provided.

Risk: Readers may mistake a snapshot summary for live browser or current site truth.

Mitigation: Keep responses grounded in normalized snapshot entities and avoid claiming live browser truth from a snapshot alone.

Risk: Changing campus site state would exceed the skill's stated read-only purpose.

Mitigation: Restrict use to inspection and reporting; do not mutate site state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/site-overview-audit)
- [Publisher profile](https://clawhub.ai/user/xiaojiou176)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output grounded in normalized snapshot entities.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
