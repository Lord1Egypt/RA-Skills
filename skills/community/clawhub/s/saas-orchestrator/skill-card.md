## Description:

Orchestrates SaaS factory operations by creating subagent task prompts, tracking projects, managing revenue targets, and coordinating development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juniorxcoder](https://clawhub.ai/user/juniorxcoder)

### License/Terms of Use:


## Use Case:

Developers, founders, and operators use this skill to plan SaaS product research, generate MVP build tasks, review portfolio status, and coordinate revenue-focused launch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate broad research, build, marketing, and launch tasks that may be unsuitable if followed without review.

Mitigation: Review each generated task before execution and confirm scope, assumptions, and business constraints.

Risk: Generated workflows may propose actions involving accounts, payments, public posting, or real business systems.

Mitigation: Require explicit human approval before creating accounts, configuring payments, posting publicly, or modifying production business systems.

Risk: The artifact describes subagent orchestration without clear confirmation boundaries.

Mitigation: Use it as a planning aid and keep agent spawning or command execution under manual operator control.

## Reference(s):

- [Proven SAAS Niches That Print Money](references/saas-niches.md)
- [Revenue Models That Actually Work](references/revenue-models.md)
- [MVP Patterns That Get You to Revenue Fast](references/mvp-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated task text and optional local text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local research, build, or factory status reports when helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
