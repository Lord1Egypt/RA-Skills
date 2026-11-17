## Description:

Helps agent users, skill authors, maintainers, and teams create practical Skill Vetter-style workflows for bug fixing, safety hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Skill Vetter-style needs into concise plans, checklists, templates, code changes, or decision aids that can be checked against explicit success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly because its trigger terms include generic words such as security, GitHub, first, and bug fix.

Mitigation: Use explicit invocation or narrow the trigger configuration when the agent environment supports trigger controls.

Risk: The skill produces planning, checklist, code, shell, and configuration guidance that may be incorrect or incomplete for a user's specific environment.

Mitigation: Review proposed changes before execution and validate outputs against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-234912)
- [Skill Vetter Demand Source](https://clawhub.ai/skills/skill-vetter)
- [GitHub Skill Demand Source](https://clawhub.ai/skills/github)
- [GitHub Account Malware Discussion](https://news.ycombinator.com/item?id=48548530)
- [No-Secret-In-Config Issue](https://github.com/Elevarq/Arq-Signals/issues/101)
- [Credential Provider Design Issue](https://github.com/Elevarq/Arq-Signals/issues/93)
- [Systemd Socket Activation Issue](https://github.com/mudler/LocalAI/issues/10372)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated outcome, constraints, available inputs, and success criteria.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
