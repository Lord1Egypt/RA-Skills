## Description:

Helps agent users, skill authors, maintainers, and teams create practical SkillScan-style workflows for bug fixing, setup hardening, reliability improvement, and adjacent skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agent users, skill authors, maintainers, and teams use this skill to turn broad security and productivity requests into concrete workflows, checklists, automation outlines, analysis, code changes, or decision support. It emphasizes local-hardware-friendly implementation and visible validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic trigger terms and implicit invocation can cause the skill to appear during unrelated security, bug-fix, or workflow requests.

Mitigation: Review and narrow activation rules before deployment, especially the generic keywords such as security, gate, every, must, pass, before, activate, and bug fix.

Risk: Workflow outputs may include proposed code, shell commands, configuration, or security guidance that need local validation.

Mitigation: Review proposed changes, run appropriate tests or scans, and confirm assumptions before applying outputs to production systems.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skillscan-security-workflow-helper-100358)
- [Popular ClawHub skill demand: SkillScan](https://clawhub.ai/skills/skillscan)
- [Popular ClawHub skill demand: Skill Vetter](https://clawhub.ai/skills/skill-vetter)
- [GitHub issue: generated workflow silent failures](https://github.com/EffortlessMetrics/ripr-swarm/issues/2009)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, checklists, workflow steps, validation notes, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tailored artifacts, reusable checklists, automation outlines, decision aids, assumptions, limits, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
