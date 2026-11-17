## Description:

time-calc helps agents answer date and time questions by using local shell or PowerShell commands for current time, date metadata, relative weekday lookup, date arithmetic, differences, timezone conversion, and Unix timestamp conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrlyk](https://clawhub.ai/user/mrlyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to resolve natural-language date and time requests into precise results before answering or continuing a workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local shell or PowerShell date commands and does not spell out strict input validation for adversarial date strings.

Mitigation: Use clear date, offset, and timezone inputs, review generated commands before execution, and prefer a sandboxed agent environment for untrusted prompts.

## Reference(s):

- [Linux GNU date command reference](references/linux.md)
- [macOS BSD date command reference](references/macos.md)
- [Windows PowerShell date command reference](references/windows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise text or Markdown with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local platform date/time tooling and does not require external dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
