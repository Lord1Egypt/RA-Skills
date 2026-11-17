## Description:

Helps agent users, skill authors, maintainers, and teams create SkillScan-style workflows, checklists, analyses, and implementation support for setup hardening, safety, reliability, and adjacent skill work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn security and productivity workflow requests into concrete plans, checklists, analysis, code changes, or verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation terms may cause the skill to activate during unrelated security or productivity conversations.

Mitigation: Invoke the skill explicitly for SkillScan-style workflow help, or narrow or disable implicit activation when tighter routing control is required.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-060415)
- [SkillScan Demand Signal](https://clawhub.ai/skills/skillscan)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [Threat Modeling for Terraform/IaC](https://news.ycombinator.com/item?id=48972048)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by user request and should include assumptions, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
