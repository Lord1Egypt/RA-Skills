## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows, artifacts, checklists, analyses, or implementation support for security, reliability, and productivity tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, skill authors, maintainers, and AI-agent users use this skill to turn security, hardening, reliability, and SkillScan-style productivity requests into concrete workflows, checklists, analyses, code changes, or decision aids. It is intended for local-hardware-friendly planning and execution support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly because its trigger words are generic and implicit invocation is enabled.

Mitigation: Prefer explicit invocation by skill name and narrow trigger language before relying on automatic routing.

Risk: Workflow and checklist output may be incomplete or mismatched if the user's constraints, inputs, or success criteria are unclear.

Mitigation: Restate the outcome, assumptions, limits, and validation criteria before producing or applying the artifact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-040328)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub Skill Demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Support Scaffolding Issue](https://github.com/kanshi-dev/core/issues/13)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's immediate context and should state assumptions, limits, validation results, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
