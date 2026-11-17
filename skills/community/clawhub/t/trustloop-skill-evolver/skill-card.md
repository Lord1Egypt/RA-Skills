## Description:

Let OpenClaw capture reusable workflows as managed skill candidates, support review or revision, and evolve safely through manual, assisted, or autonomous modes inside the current workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haocheng0126](https://clawhub.ai/user/haocheng0126)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture repeatable workspace workflows as reviewed managed skill candidates, publish approved learned skills, and roll back changes while controlling autonomy level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist workflow records and change future agent behavior through managed learned skills.

Mitigation: Keep the skill in manual mode for normal use and require human review before publishing learned skills.

Risk: Autonomous mode can publish low-risk changes without per-change review.

Mitigation: Enable autonomous mode only in workspaces where automatic changes to learned skills are acceptable.

Risk: Candidate or audit files may capture details from repeated workflows.

Mitigation: Review ./.skill-evolver candidate and audit files before publishing or sharing the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haocheng0126/skills/trustloop-skill-evolver)
- [README](artifact/README.md)
- [Evolution Rules](artifact/references/evolution-rules.md)
- [Review Policy](artifact/references/review-policy.md)
- [Managed Skill Tool Interface](artifact/references/skill-manage-managed-tool.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, managed skill drafts, candidate records, JSON audit entries, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are workspace-scoped and may include review prompts, rollback guidance, and mode-specific publish behavior.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
