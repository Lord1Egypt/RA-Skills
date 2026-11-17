## Description:

Wake-on-LAN skill for waking computers by name or IP address and managing stored device configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lroyia](https://clawhub.ai/user/lroyia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device administrators use this skill to let an agent wake known computers on a local network and list, add, show, or delete Wake-on-LAN device records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send Wake-on-LAN packets on the local network.

Mitigation: Require explicit user confirmation before wake actions and only use the skill on networks where Wake-on-LAN traffic is expected.

Risk: Device names, MAC addresses, and IP addresses are sensitive local-network data.

Mitigation: Use the script's list and show commands, which mask MAC addresses, and avoid exposing the raw devices.yaml contents in conversation.

Risk: The skill can modify the stored device list, including deleting records.

Mitigation: Confirm add, update, and delete requests before running them, and review device-list changes when operating in shared environments.

Risk: Security evidence notes shell invocation safety gaps.

Mitigation: Review generated shell commands before execution and pass user-provided values as explicit command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lroyia/skills/wol)
- [Device configuration template](artifact/references/devices.yaml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the local devices.yaml configuration through the provided command-line interface.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
