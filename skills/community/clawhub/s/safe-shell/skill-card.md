## Description:

Safe Shell helps an agent propose read-only shell commands for inspecting files, system state, network configuration, and environment information while blocking commands described as destructive or execution-oriented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyusheng188](https://clawhub.ai/user/chengyusheng188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators can use this skill when an assistant needs to inspect directories, files, host status, or network settings through read-only command suggestions. It is intended for cautious diagnostic and monitoring workflows rather than system modification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the validator can approve unsafe command strings.

Mitigation: Do not rely on the skill as a hard safety boundary until command parsing is structured and shell control syntax is rejected.

Risk: The security evidence says the skill permits broad environment-variable disclosure.

Mitigation: Remove, disable, or redact environment-variable output before using the skill in environments that may contain secrets.

Risk: The security guidance calls for a pinned, verifiable installer.

Mitigation: Install only from a verified release or pinned artifact and review the package before deployment.

## Reference(s):

- [ClawHub Safe Shell release](https://clawhub.ai/chengyusheng188/skills/safe-shell)
- [ClawHub publisher profile](https://clawhub.ai/user/chengyusheng188)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes allowed and blocked command patterns; actual execution depends on the hosting agent or tool environment.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
