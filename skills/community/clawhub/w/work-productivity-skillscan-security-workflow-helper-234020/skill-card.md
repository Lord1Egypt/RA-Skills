## Description:

Helps agent users, skill authors, maintainers, and teams create SkillScan-style workflows for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, skill authors, maintainers, and teams use this skill to turn SkillScan-style security and reliability needs into practical workflows, checklists, analysis, code changes, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad activation terms such as security, must, before, and bug fix may cause the skill to be selected too often.

Mitigation: Confirm that the user's request needs a SkillScan-style workflow before applying the skill, and prefer narrower triggers in future releases.

Risk: Workflow guidance could be mistaken for completed security verification.

Mitigation: Use the skill's validation step to document assumptions, limits, remaining risks, and any required review before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-234020)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [Self-improving Agent demand signal](https://clawhub.ai/skills/self-improving-agent)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Analysis]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow helper; no credential requests, code execution, persistence, or sensitive-data access indicated by security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
