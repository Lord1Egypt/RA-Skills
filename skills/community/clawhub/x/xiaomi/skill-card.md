## Description:

Control Xiaomi Home devices over the local network with miiocli, including status checks, power toggles, and MIOT property changes for smart plugs, humidifiers, and rice cookers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi)

### License/Terms of Use:


## Use Case:

Developers and smart-home operators use this skill to translate requests into miiocli commands for locally controlling configured Xiaomi devices and checking device status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaomi device tokens may be stored or shared in plaintext.

Mitigation: Treat tokens like passwords and keep them in a secret manager, ignored private config file, or owner-only permissioned storage.

Risk: Direct appliance control can affect plugs, heaters, cookers, or similar devices.

Mitigation: Require explicit confirmation and verify the target device name before issuing power or appliance-changing commands.

Risk: The install workflow depends on python-miio and a constrained click version.

Mitigation: Review and pin dependency versions before running the install command in a production or shared environment.

## Reference(s):

- [Xiaomi skill page on ClawHub](https://clawhub.ai/yiqiezhenxi/skills/xiaomi)
- [Publisher profile on ClawHub](https://clawhub.ai/user/yiqiezhenxi)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include miiocli commands that require device IP addresses and Xiaomi device tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
