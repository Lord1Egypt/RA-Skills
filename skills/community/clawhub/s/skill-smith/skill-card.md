## Description:

Create new AI skill packages, audit existing skills, and upgrade them to platform standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yysws5566](https://clawhub.ai/user/yysws5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create a new AI skill package, check an existing package for structural and quality issues, or improve a skill through a bounded upgrade workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious because it found an unannounced automatic persistent ledger update and could not fully inspect a referenced script; this is not a finding of malicious intent.

Mitigation: Review the skill’s behavior before installing, account for the persistent ledger update, and inspect the partially reviewed script.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yysws5566/skills/skill-smith)
- [Skill creation playbook](references/create-playbook.md)
- [Audit rubric](references/audit-rubric.md)
- [Upgrade workflow](references/upgrade-loop.md)
- [Writing specification](references/writing-spec.md)
- [Skill audit script](scripts/skill-audit.js)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown skill packages and audit or upgrade reports, with JavaScript audit output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a skill skeleton, evidence-based quality findings, and before-and-after upgrade results.]

## Skill Version(s):

1.2.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
