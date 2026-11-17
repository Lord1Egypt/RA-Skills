## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, skill authors, maintainers, and teams use this skill to turn SkillScan-style security and reliability needs into actionable workflows, checklists, implementation support, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation keywords may cause the skill to activate in situations where a narrower security workflow was not intended.

Mitigation: Prefer explicit invocation or narrow the trigger terms before deployment in shared agent environments.

Risk: Workflow or checklist guidance can be incomplete or misleading if applied without reviewing the user's actual security context.

Mitigation: Review generated plans and validation notes against local requirements before using them to approve or deploy a skill.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-150249)
- [SkillScan Demand Reference](https://clawhub.ai/skills/skillscan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflow plans, implementation notes, and verification summaries.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
