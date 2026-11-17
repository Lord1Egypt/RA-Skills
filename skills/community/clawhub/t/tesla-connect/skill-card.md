## Description:

Connect and control Tesla vehicles via the tesla-cli. Handles guided setup (key generation, AgentGen hosting, partner registration, OAuth) and all vehicle commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyair1](https://clawhub.ai/user/lyair1)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to set up teslacli and ask an agent to inspect or control Tesla vehicle state, climate, charging, locks, lights, and horn through guided shell command workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install teslacli through an unverified remote shell installer.

Mitigation: Review the installer source before use and prefer a pinned, checksum-verified release when available.

Risk: The skill can issue commands that unlock, honk, change climate, or control charging on a real Tesla vehicle.

Mitigation: Require explicit user confirmation before executing vehicle-control commands with physical, privacy, safety, or cost impact.

Risk: The setup flow stores Tesla OAuth tokens and a private key under the local teslacli configuration directory.

Mitigation: Treat the teslacli configuration directory as sensitive and do not print, transmit, log, or move token or private-key material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyair1/skills/tesla-connect)
- [AgentGen Tesla control use case](https://www.agent-gen.com/use-cases/tesla-control)
- [tesla-cli installer source](https://raw.githubusercontent.com/Agent-Gen-com/tesla-cli/main/install.sh)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires teslacli and AGENTGEN_API_KEY; command workflows may affect a real vehicle.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
