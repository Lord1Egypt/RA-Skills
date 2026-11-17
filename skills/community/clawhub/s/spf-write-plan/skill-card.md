## Description:

Use when you have a spec or requirements for a multi-step task, before touching code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mok888](https://clawhub.ai/user/mok888)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to turn requirements into durable implementation plans with task breakdowns, file targets, test commands, and handoff guidance before coding begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update visible planning files in a repository, especially under .superpower-with-files.

Mitigation: Specify an output path when the default location is not desired and review generated planning files before keeping or sharing them.

Risk: Generated plans can contain incorrect or misleading implementation guidance if the requirements or repository context are incomplete.

Mitigation: Review plans before execution, then use normal code review, scanning, and test gates before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mok888/skills/spf-write-plan)
- [SKILL.md](artifact/SKILL.md)
- [Python CLI template](artifact/templates/python-cli.md)
- [Python FastAPI template](artifact/templates/python-fastapi.md)
- [React component template](artifact/templates/react-component.md)
- [Rust Axum template](artifact/templates/rust-axum.md)
- [Rust CLI template](artifact/templates/rust-cli.md)
- [Session handoff template](artifact/templates/handoff.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown implementation plans with code snippets, command blocks, task guides, and handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning artifacts for review before execution; no code execution is part of the planning behavior.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
