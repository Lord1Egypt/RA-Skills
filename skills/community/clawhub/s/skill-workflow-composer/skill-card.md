## Description:

Scans installed and marketplace skills, composes them into session, scheduled, or reusable workflows, and suggests cross-skill combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

People planning workflows use this skill to discover available skills, combine them into a workable sequence, and choose between session execution, scheduled automation, or a reusable workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial use lists locally installed skills and queries the skill marketplace.

Mitigation: Install only if this discovery is acceptable; treat marketplace matches as sampled rather than exhaustive.

Risk: Proposed automations, file writes, publishing, or reusable skill creation could persist unwanted changes.

Mitigation: Review the proposed action and confirm it before execution.

## Reference(s):

- [Skill workflow catalog](artifact/references/skill-workflow-catalog.md)
- [Skill workflow requirements](artifact/references/skill-workflow-requirements.md)
- [Skill workflow exemplars](artifact/references/skill-workflow-exemplars.md)
- [Workflow plan template](artifact/templates/workflow-plan-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown tables, workflow plans, and suggested automation configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marketplace results are sampled; persistent actions require user confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; bundled frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
