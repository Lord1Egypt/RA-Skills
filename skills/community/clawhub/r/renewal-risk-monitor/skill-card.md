## Description:

Identifies renewal risk signals and distinguishes recoverable risks from high-probability churn signals for renewal, risk, and customer-success workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-success and renewal teams use this skill to turn customer usage, feedback, and interaction history into a structured renewal-risk brief with risk signals, recoverable items, high-risk factors, suggested actions, timing, and escalation criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process customer-success materials that may contain sensitive customer or personal information.

Mitigation: Provide scoped, relevant inputs and redact sensitive material before use when possible.

Risk: Broad directory inputs may include unrelated repositories, folders, or customer records outside the renewal-risk task.

Mitigation: Use narrowly scoped input files or directories and prefer dry-run or stdout output unless an output file is intentionally needed.

Risk: Unused audit code in the helper script may confuse reviewers about the active behavior of the release.

Mitigation: Treat the shipped configuration as the behavior boundary and ask the publisher to remove or document unused audit paths in a future release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/renewal-risk-monitor)
- [Skill Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown brief, with optional JSON output from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write to stdout by default or to an output file when explicitly requested.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
