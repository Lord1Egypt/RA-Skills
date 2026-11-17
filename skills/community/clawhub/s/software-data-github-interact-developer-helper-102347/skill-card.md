## Description:

Helps agent users and maintainers handle GitHub-style developer workflows by clarifying requirements, proposing implementation steps, producing artifacts or code guidance, and validating results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, skill authors, and agent users use this skill to plan and execute GitHub-style workflow support, including bug fixes, setup hardening, reliability improvements, adjacent workflow creation, and practical verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers and implicit invocation may select the skill for loosely related GitHub, CLI, issue, or PR tasks.

Mitigation: Confirm the user's intended outcome, constraints, and success criteria before applying the workflow.

Risk: The skill may suggest code changes, setup changes, or shell commands that affect a local project.

Mitigation: Review proposed changes and commands before execution, and run appropriate tests or verification checks afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-102347)
- [Requirement plan](references/requirement-plan.md)
- [Popular ClawHub GitHub skill demand signal](https://clawhub.ai/skills/github)
- [GitHub CI risk demand signal](https://news.ycombinator.com/item?id=48624574)
- [Multi-agent developer workflow demand signal](https://www.v2ex.com/t/1222186)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include checklists, workflows, assumptions, verification notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
