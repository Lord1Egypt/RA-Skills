## Description:

Helps detect security-relevant changes in AI skills after installation by tracking deltas between the audited version and current version, flagging updates that expand permissions, add new network endpoints, or alter behavior in ways that bypass install-time security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to compare an audited skill version against a newer version and identify security-relevant changes in permissions, endpoints, dependencies, instructions, and update velocity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delta reports may flag legitimate feature updates, telemetry, or dependency changes as suspicious.

Mitigation: Use the report as a review trigger and confirm intent against release notes, source diffs, and the skill publisher before taking rollback action.

Risk: The skill may guide an agent to inspect local skill files, git history, dependency changes, and endpoint references.

Mitigation: Run reviews in a workspace scoped to the target skill and avoid exposing unrelated private repositories or credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/skills/skill-update-delta-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown delta report with risk classification and review recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports permission scope diffs, new network endpoints, dependency changes, instruction drift score, version velocity, and CLEAN / WATCH / REVIEW / ROLLBACK classification.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
