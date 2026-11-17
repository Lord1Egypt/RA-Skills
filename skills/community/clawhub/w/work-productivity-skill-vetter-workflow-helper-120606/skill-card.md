## Description:

Helps AI-agent users and skill authors create practical workflows, checklists, analysis, and implementation support for Skill Vetter-style safety, reliability, setup, and adjacent skill work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn skill-vetting and reliability needs into local-friendly plans, checklists, analysis, code changes, or workflow artifacts with validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation may trigger on generic security or GitHub prompts.

Mitigation: Review activation behavior before use and narrow triggers or disable implicit invocation if it activates outside Skill Vetter-style workflow tasks.

Risk: Workflow or checklist guidance may be incomplete or mismatched to a user's repository, skill, or operational constraints.

Mitigation: Validate generated artifacts against the stated success criteria, scan any resulting skill before deployment, and keep assumptions visible for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-120606)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter Demand Signal](https://clawhub.ai/skills/skill-vetter)
- [GitHub Skill Demand Signal](https://clawhub.ai/skills/github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, configuration snippets, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and follow-up work]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
