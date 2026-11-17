## Description:

Controls Xiaomi Home devices on the local network using miiocli, including status checks, power toggles, and MIOT property changes for devices such as smart plugs, humidifiers, and rice cookers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pegasus02](https://clawhub.ai/user/pegasus02)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to operate Xiaomi Home devices through local LAN miiocli commands and to collect the device IP and token data needed for those commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the release ships and encourages plaintext Xiaomi device credentials.

Mitigation: Remove private device inventories from the release, rotate any exposed Xiaomi tokens or BLE keys, and keep device credentials out of Markdown and source files.

Risk: The token extraction workflow can collect cloud device data and credentials across Xiaomi regions.

Mitigation: Run extraction only for accounts and devices the user owns or is authorized to administer, scope the selected server region deliberately, and delete or protect generated exports.

Risk: Secret-bearing logs or plaintext exports may expose Xiaomi tokens, BLE keys, router details, camera details, or service token data.

Mitigation: Use non-debug logging by default, avoid sharing generated output files, and redact tokens, keys, IPs, and account identifiers before support or review.

Risk: Local miiocli commands can change the state of physical home devices such as plugs, humidifiers, rice cookers, routers, and cameras.

Mitigation: Require explicit user confirmation for device-changing actions and verify the target device, IP, token source, and intended MIOT property before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pegasus02/skills/xiaomi-home)
- [Device inventory template](references/devices.md)
- [Artifact-declared GitHub link](https://github.com/Pegasus02/clawdbot-xiaomi-home)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline miiocli and Python shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires miiocli; setup guidance installs python-miio with a pinned click dependency workaround and may use Xiaomi device IPs and tokens.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
