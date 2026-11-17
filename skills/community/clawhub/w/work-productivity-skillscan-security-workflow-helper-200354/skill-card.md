## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, analyses, and implementation support for SkillScan-style bug fixing, security hardening, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn SkillScan-style workflow demand into actionable work plans, templates, automation outlines, decision aids, checklists, analysis, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on ordinary words such as security, must, or before, which can be noisy in a multi-skill setup.

Mitigation: Review implicit invocation settings before installation and narrow or disable broad trigger terms where the host agent supports routing controls.

Risk: Workflow proposals, checklists, code changes, or security guidance may be incomplete or misleading for a user's specific environment.

Mitigation: Review generated outputs against the stated success criteria, scan any produced code or configuration before deployment, and validate security-sensitive changes in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-200354)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Pydantic AI issue: optional run_id on Agent and UIAdapter entrypoints](https://github.com/pydantic/pydantic-ai/issues/6493)
- [kagent issue: restricted Pod Security for regular Agent Deployments](https://github.com/kagent-dev/kagent/issues/2244)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, configuration snippets, templates, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated outcome, constraints, available inputs, and success criteria.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
