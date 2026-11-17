## Description:

Analyze the current conversation history and local installed skills to identify missed skill triggers, overlapping or duplicate skills, weak metadata, stale or risky skills, and workflow gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangchenchen](https://clawhub.ai/user/zhangchenchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to audit visible conversation and local skill evidence, identify trigger, metadata, duplication, stale-file, safety, and installation workflow issues, and produce an action queue for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects the current thread and visible local skill directories, which may expose sensitive local context to the audit output.

Mitigation: Review the generated audit before sharing it, and avoid providing logs or directories that contain secrets unless they are necessary for the audit.

Risk: Recommended Fix, Merge, or Delete actions could change skill behavior or remove useful local skill files if approved without review.

Mitigation: Use the generated action queue as a proposal only, review each recommended action, and confirm any edit or deletion before authorizing changes.

## Reference(s):

- [Report Schema](references/report-schema.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with structured findings and an action queue]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits user-facing action choices to Fix, Merge, Delete, or Keep and Skip.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
