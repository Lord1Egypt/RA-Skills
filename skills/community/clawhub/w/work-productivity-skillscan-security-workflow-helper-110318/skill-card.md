## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, security hardening, reliability improvement, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, skill authors, maintainers, and teams use this skill to turn SkillScan-style needs into local-friendly workflows, checklists, analysis, code changes, or decision support. It is suited to repeatable security and productivity tasks where assumptions, validation criteria, and next steps need to be explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation wording that can match unrelated productivity or security requests.

Mitigation: Install and invoke it intentionally for SkillScan-style workflow help, and review whether implicit invocation is appropriate before use.

Risk: The skill produces workflow guidance, checklists, code changes, commands, or configuration suggestions that may be incomplete or context-sensitive.

Mitigation: Review outputs against the stated success criteria and scan or test any generated code, commands, or configuration before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-110318)
- [Popular ClawHub Skill Demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub Skill Demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Ask HN: Threat Modeling for Terraform/IaC](https://news.ycombinator.com/item?id=48972048)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should surface assumptions, limits, required inputs, validation checks, and follow-up work when helpful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
