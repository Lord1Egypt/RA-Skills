## Description:

Use when the user needs to create or refine a feature SPEC SDD before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn ambiguous feature, bugfix, refactor, API, infrastructure, frontend, or documentation requests into an approved Spec-Driven Development document before implementation begins. It is especially suited to pt-BR planning workflows that need structured requirements, acceptance criteria, validation strategy, and optional GitHub issue handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read repository context and create or update SPEC files as part of requirements planning.

Mitigation: Run it only in repositories where the agent is allowed to inspect project files, and review generated SPEC content before approval.

Risk: The workflow can coordinate GitHub issue creation and label synchronization after SPEC approval.

Mitigation: Require explicit user approval for issue handoff and review any GitHub issue or label changes, especially in shared or public repositories.

Risk: The skill forces Portuguese user-facing interaction, which may cause misunderstandings for teams that do not work in pt-BR.

Mitigation: Use it where Portuguese communication is acceptable, or have a pt-BR-capable reviewer confirm the generated questions and SPEC before implementation.

## Reference(s):

- [SPEC SDD Template](references/spec-sdd-template.md)
- [Source repository](https://github.com/afonsoft/skills)
- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/write-specs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Portuguese user-facing text and Markdown SPEC SDD files, with occasional inline shell commands for GitHub issue label synchronization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates SPEC documents under .specs/ and may coordinate GitHub issue creation or label changes after user approval.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
