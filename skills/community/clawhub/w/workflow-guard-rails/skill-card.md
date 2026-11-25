## Description:

Wrap multi-step agent workflows with pre-execution checks, checkpoints, queued side effects, bounded retries, result validation, audit logs, and gated failure-rule accumulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add recovery and validation safeguards to multi-step agent workflows, especially unattended workflows that perform external actions or need safe reruns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because its update guidance could lead to unreviewed changes to a persistent playbook; scanner coverage was partial and did not establish malicious intent.

Mitigation: Review the playbook installation and update instructions, and confirm changes are staged and reviewed before they become authoritative.

## Reference(s):

- [Guardian Patterns](references/guardian-patterns.md)
- [Pinned Error Playbook](https://raw.githubusercontent.com/haiyangchenbj/error-playbook/d945aee01384c6163beb287446147ce768d50661/ERROR-PLAYBOOK.md)
- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/workflow-guard-rails)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown instructions, checklists, guardian reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include audit-log entries and staged failure-rule guidance for a guarded workflow.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
