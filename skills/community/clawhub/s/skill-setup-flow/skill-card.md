## Description:

Creates standardized setup flows for installed OpenClaw skills, including directory structures, configuration templates, core file integration guidance, and setup logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengcareergmail](https://clawhub.ai/user/tengcareergmail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this meta-skill to initialize installed skills with consistent setup steps, configuration and state templates, setup logs, and integration guidance for core agent files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to edit persistent core behavior, memory, or tool files.

Mitigation: Require a preview of every planned change and approve updates before writing to SOUL.md, AGENTS.md, MEMORY.md, or TOOLS.md.

Risk: Setup templates can encourage storing sensitive configuration values in Markdown files.

Mitigation: Keep secrets out of generated Markdown templates and use dedicated secret storage for credentials or tokens.

Risk: A mistyped or ambiguous target skill name can lead to setup files being created or integrated for the wrong skill.

Mitigation: Validate the target skill name and path before creating directories, templates, logs, or integration notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengcareergmail/skills/skill-setup-flow)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [setup-template.md](artifact/setup-template.md)
- [Self-improving setup example](artifact/examples/self-improving-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent edits to core behavior, memory, or tool files; review planned changes before applying them.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
