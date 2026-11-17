## Description:

Adds seven safeguards to multi-step agent workflows, including pre-execution checks, checkpoints, queued side effects, bounded retries, result validation, audit logs, and staged failure rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building scheduled, event-driven, or repeatable agent workflows use it to check prerequisites, contain side effects, validate results, and recover safely from failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions download content directly to the authoritative global playbook path, which could replace existing guidance before it is reviewed.

Mitigation: Review the download and update flow first; preserve existing playbook content and require confirmation before replacing it or promoting rules.

## Reference(s):

- [Workflow Guard Rails on ClawHub](https://clawhub.ai/haiyangchenbj/skills/workflow-guard-rails)
- [Guardian patterns](references/guardian-patterns.md)
- [Pinned Error Playbook download referenced by the skill](https://raw.githubusercontent.com/haiyangchenbj/error-playbook/d945aee01384c6163beb287446147ce768d50661/ERROR-PLAYBOOK.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance with a structured Guardian Report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report summarizes checks, checkpoints, queued side effects, validation, retries, audit logging, rule capture, and release status.]

## Skill Version(s):

1.0.9 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
