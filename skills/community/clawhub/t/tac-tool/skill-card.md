## Description:

Displays local file contents in reverse line order so recent log entries or reversed file content appear first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local files in reverse line order, especially when viewing log files from newest entries first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local files selected by the user or agent, which can expose unintended file contents if paths are chosen carelessly.

Mitigation: Review file paths before execution and use the tool only on files intended for inspection.

Risk: The documented multi-file example is broader than the bundled script behavior.

Mitigation: Test expected command behavior on sample files before relying on multi-file workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/tac-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local files selected by the user or agent and emits reversed line order.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
