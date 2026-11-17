## Description:

Converts Excel, CSV, XML, and YAML configuration tables into Protobuf-backed JSON, text protobuf, or binary protobuf outputs through the tableauc protogen and confgen pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenchy](https://clawhub.ai/user/wenchy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, troubleshoot, and regenerate tableau/tableauc configuration pipelines for game data, application configuration spreadsheets, and structured Protobuf-backed config files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run tableauc and create or modify conversion files in the active project.

Mitigation: Use it in a project sandbox and avoid running it from directories that contain unrelated sensitive files or credentials.

Risk: The skill may install tableauc with go install using an unpinned latest version if the command is missing.

Mitigation: Require a preinstalled or pinned tableauc version before using the skill for production work.

Risk: Incorrect conversion guidance can produce stale or invalid Protobuf schemas and config outputs.

Mitigation: Review generated inputs and run both protogen and confgen after changes so outputs stay synchronized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenchy/skills/tableau)
- [Official tableau documentation source](https://github.com/tableauio/tableauio.github.io)
- [Official tableau test cases](https://github.com/tableauio/tableau)
- [config.yaml / options.Options Reference](references/config.md)
- [Metasheet (@TABLEAU) Reference](references/metasheet.md)
- [Protoconf Annotation Reference](references/protoconf.md)
- [Type System Deep Dive](references/types.md)
- [Excel Input Format Reference](references/excel/index.md)
- [CSV Input Format Reference](references/csv/index.md)
- [XML Input Format Reference](references/xml/index.md)
- [YAML Input Format Reference](references/yaml/index.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks, command examples, and generated file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create input/config files and tableauc commands; generated conversion outputs depend on the installed tableauc CLI and local project files.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
