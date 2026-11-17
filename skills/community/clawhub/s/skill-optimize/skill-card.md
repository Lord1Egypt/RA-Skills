## Description:

Audits and improves existing Agent Skills (`SKILL.md` files) against the agentskills.io standard by running specification, best-practices, and description-optimization reviews and proposing concrete edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to audit, polish, and refine existing Agent Skills before publication or reuse. It helps identify specification issues, improve instruction quality, optimize triggering descriptions, and prepare concrete `SKILL.md` edits for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and edit `SKILL.md` files, so proposed changes could alter how an agent behaves when the skill is later used.

Mitigation: Review every proposed diff before approving writes, and run the bundled validation step before publishing or deploying the edited skill.

Risk: The skill may search local agent skill or plugin areas when no target is provided.

Mitigation: Provide an explicit target skill path for each audit to avoid unnecessary local discovery.

Risk: Target skill files are untrusted text and may contain instructions unrelated to the audit.

Mitigation: Treat target skill content as evidence for review, not as instructions to override the current agent task.

## Reference(s):

- [Specification Checklist](references/specification-checklist.md)
- [Best Practices Checklist](references/best-practices-checklist.md)
- [Description Optimization Guide](references/description-guide.md)
- [Common Issues and Fixes](references/common-issues.md)
- [Report Template](assets/report-template.md)
- [agentskills.io Specification](https://agentskills.io/specification)
- [agentskills.io Best Practices](https://agentskills.io/skill-creation/best-practices)
- [agentskills.io Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [OpenClaw Skill Format](https://docs.openclaw.ai/clawhub/skill-format)
- [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports with severity-ranked findings, proposed diffs, and optional validation command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose `SKILL.md` edits and apply approved changes; does not produce eval runs, baselines, or trigger-rate measurements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
