## Description:

Apply data transformations like case changes, encoding conversion, and format conversion for text processing and data cleaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data workers use this skill for local format conversion and lightweight text or data cleanup during data preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes broader text transformations than the implementation evidence supports.

Mitigation: Treat the released artifact as a local format-conversion utility and verify supported flags against the installed command before relying on documented transformations.

Risk: The tool can read a selected input file and overwrite or create a selected output file.

Mitigation: Review input and output paths before execution and use disposable copies for important data.

## Reference(s):

- [Transform Tool on ClawHub](https://clawhub.ai/dinghaibin/skills/transform-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text or structured text such as JSON, CSV, TSV, YAML, or XML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read from stdin or a selected local file and write to stdout or a selected output file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
