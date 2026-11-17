## Description:

Manage OpenClaw and installed skill updates with scheduled checks, safe upgrade workflows, rollback-minded guidance, and clear reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw and installed skill versions, preview or apply ClawHub skill updates, configure recurring update checks, and report update outcomes clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring or bulk update workflows can change multiple installed skills and agent behavior at once.

Mitigation: Prefer dry-run or notification-only scheduled checks and require explicit approval before applying `clawhub update --all`.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Summary Examples](references/summary-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run recommendations, update status, failures, and manual follow-up steps.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
