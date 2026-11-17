## Description:

Provides a basic hex and ASCII dump helper for inspecting binary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers can use this skill to inspect local binary files as offset, hexadecimal, and ASCII output during troubleshooting, protocol debugging, or binary analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation claims reverse conversion, patching, bit dump, JSON, include, and formatting modes that are not supported by the bundled script.

Mitigation: Verify required behavior before relying on those modes; for any patching workflow, work on a copy or keep a backup of the target file.

Risk: Hex-dump output can expose sensitive file contents in terminal history, logs, or shared transcripts.

Mitigation: Avoid running the helper on confidential files in shared environments, and redact or limit output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/xxd-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text hex-dump output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits offset, hexadecimal byte, and ASCII columns for local file or stdin input.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
