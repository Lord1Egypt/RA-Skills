## Description:

Use this skill to request an independent, focused review of a code change before merging or between planned tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to obtain an independent review of a scoped code change before merging or between planned tasks. The reviewer receives the diff and requirements rather than the author's session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing a review range may expose private code or sensitive information.

Mitigation: Share only an authorized, bounded code range and check the review context for secrets before dispatching a reviewer.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown code-review findings and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Independent review scoped to the supplied code range and requirements.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
