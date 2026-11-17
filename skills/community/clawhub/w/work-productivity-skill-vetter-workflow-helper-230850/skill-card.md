## Description:

Helps agent users, skill authors, maintainers, and teams adapt Skill Vetter-style productivity workflows for bug fixing, setup hardening, safety, reliability, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn skill-vetting and work-productivity requests into practical workflows, checklists, artifacts, analysis, code support, and verification notes. It is especially suited to requests about fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too easily for generic security or GitHub-related requests.

Mitigation: Prefer explicit invocation for skill-vetting tasks and narrow trigger keywords when maintaining or packaging this skill.

Risk: Workflow outputs can include implementation or hardening guidance that may not fit the user context without review.

Mitigation: Validate outputs against the stated success criteria and keep assumptions, limits, and follow-up risks visible before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-230850)
- [Requirement plan](references/requirement-plan.md)
- [Skill Vetter demand source](https://clawhub.ai/skills/skill-vetter)
- [SkillScan demand source](https://clawhub.ai/skills/skillscan)
- [GitHub skill demand source](https://clawhub.ai/skills/github)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, checklists, templates, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow helper; no executable payload is bundled.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
