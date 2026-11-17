## Description:

Quick system diagnostics: CPU, memory, disk, uptime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers, operators, and support agents use this skill to request quick local system diagnostics for CPU, memory, disk, and uptime checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes local machine status such as CPU, memory, disk, and uptime.

Mitigation: Use it only in environments where sharing basic local system diagnostics with the agent and user is acceptable.

Risk: The artifact documents a system-info command but does not bundle an implementation.

Mitigation: Verify that the system-info command exists in the target environment before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/system-info)
- [Publisher profile](https://clawhub.ai/user/xejrax)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the free binary and standard Linux system utilities; no bundled command implementation is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
