## Description:

Helps agents provide cautious Windows TrueCrypt command-line commands for mounting, dismounting, inspecting, and automating legacy containers or encrypted partitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining legacy TrueCrypt volumes use this skill to get cautious Windows CLI mount, dismount, install-detection, and scripting guidance without exposing secrets unnecessarily.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-line passwords may be exposed through process listings, logs, or shell history.

Mitigation: Avoid using the /p switch unless the user explicitly accepts the exposure risk, and avoid placing real passwords in saved scripts.

Risk: TrueCrypt is discontinued and no longer receives long-term security maintenance.

Mitigation: Use this skill only when legacy TrueCrypt CLI support is intentionally required, and keep the discontinued status visible when security is relevant.

Risk: Mount and dismount commands can affect encrypted volumes and drive-letter state.

Mitigation: Confirm the TrueCrypt executable path, volume or device path, target drive letter, and keyfile requirements before proposing commands; prefer non-destructive checks first.

## Reference(s):

- [TrueCrypt command cookbook](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with inline PowerShell or batch command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install-detection steps, switch explanations, and cautious validation plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
