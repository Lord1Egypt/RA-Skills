## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, security hardening, reliability improvement, and adjacent skill planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent teams use this skill to turn SkillScan-style security and workflow needs into concise plans, checklists, implementation support, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to trigger for general security or workflow requests.

Mitigation: Use explicit SkillScan-style workflow prompts or narrow invocation policy before deployment.

Risk: Generated plans or code changes for security workflows may be incomplete or mismatched to the user's environment.

Mitigation: Review outputs against local success criteria and run the stated validation steps before adopting changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-120220)
- [SkillScan Demand Signal](https://clawhub.ai/skills/skillscan)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [Threat Modeling for Terraform and IaC Discussion](https://news.ycombinator.com/item?id=48972048)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise plans, checklists, analysis, code snippets, shell commands, or configuration examples as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
