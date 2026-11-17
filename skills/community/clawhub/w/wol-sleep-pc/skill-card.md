## Description:

Send Wake-on-LAN and Sleep-on-LAN UDP packets for a configured PC on a local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oblivisheee](https://clawhub.ai/user/oblivisheee)

### License/Terms of Use:


## Use Case:

Developers and technically capable users use this skill to wake or sleep a specific PC on a LAN by sending explicitly configured WOL or SOL packets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packets may be sent to the wrong device or network if MAC, sleep_mac, broadcast address, or port values are misconfigured.

Mitigation: Configure these values explicitly for a PC and LAN you control, and verify the target details before executing the helper scripts.

Risk: The skill does not verify target device status before or after sending WOL or SOL packets.

Mitigation: Confirm the device state through an independent local check when the result matters.

Risk: The optional local config file can reveal device identifiers and network details.

Mitigation: Keep the config file private and avoid committing or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oblivisheee/skills/wol-sleep-pc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local Python helper scripts that send UDP broadcast packets when explicitly requested.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
