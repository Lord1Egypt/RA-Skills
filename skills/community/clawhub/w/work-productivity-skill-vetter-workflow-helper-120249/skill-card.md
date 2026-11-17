## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, analyses, or implementation support for Skill Vetter-style work such as bug fixing, setup hardening, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn Skill Vetter-style needs into concise plans, templates, checklists, analysis, code changes, or decision support. It is intended for practical workflow support around bug fixing, setup hardening, reliability improvement, security review, and related skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation could route ordinary security, GitHub, or bug-fix requests into this workflow unintentionally.

Mitigation: Narrow or disable implicit triggers before deployment, and review invocation behavior during installation.

Risk: Workflow outputs may introduce incorrect or misleading guidance into skills if accepted without review.

Mitigation: Review outputs against the user's success criteria and scan any resulting skill before deployment.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-120249)
- [Publisher profile](https://clawhub.ai/user/kyro-ma)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub skill demand signal](https://clawhub.ai/skills/github)
- [SkillScan demand signal](https://clawhub.ai/skills/skillscan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, templates, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
