## Description:

Get the current system uptime using the native 'uptime' command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alamby](https://clawhub.ai/user/alamby)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operators use this skill to check local Unix-like system uptime and basic status when an agent is asked how long the current machine has been running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local system command to answer uptime questions.

Mitigation: Use it only in environments where running the standard uptime command is acceptable; the reviewed artifact does not request broad access, persistence, or network behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alamby/skills/system-uptime)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text uptime output, with optional Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local access to the standard uptime command.]

## Skill Version(s):

1.0.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
