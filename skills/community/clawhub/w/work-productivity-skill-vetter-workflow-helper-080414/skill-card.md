## Description:

Helps agent users, skill authors, maintainers, and teams create practical Skill Vetter-style workflows for bug fixing, setup hardening, safety review, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn Skill Vetter-style needs into concrete workflows, checklists, analyses, code-change support, and validation notes. It is intended for practical work-productivity tasks around vetting, fixing, hardening, and improving agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad trigger wording that may activate during unrelated security, GitHub, or bug-fix conversations.

Mitigation: Narrow or disable generic trigger terms before broad deployment, and keep invocation tied to explicit Skill Vetter-style workflow requests.

Risk: Workflow guidance for skill vetting, bug fixing, or hardening may be incomplete or misapplied without reviewer context.

Mitigation: Review generated workflows and code-change suggestions before execution, then validate them against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-skill-vetter-workflow-helper-080414)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, code snippets, shell commands, configuration snippets, checklists, or concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and follow-up work when useful.]

## Skill Version(s):

0.20260729.110214 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
