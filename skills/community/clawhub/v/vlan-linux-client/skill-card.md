## Description:

Helps agents provide guidance for installing, authenticating, operating, and troubleshooting the VLAN.CN Linux client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxf-oss](https://clawhub.ai/user/sxf-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and support engineers use this skill to guide VLAN.CN Linux client setup, login, virtual network connection management, service control, and network diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents an unverified HTTP installer piped directly into a shell.

Mitigation: Independently trust and verify the VLAN.CN installer before use; prefer an official HTTPS package or a downloaded script with a published checksum or signature.

Risk: The uninstall guidance includes privileged recursive deletion.

Mitigation: Verify the exact target path and service state before running sudo deletion commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxf-oss/skills/vlan-linux-client)
- [VLAN.CN Linux client guide](https://www.vlan.cn/guide/linux-client)
- [VLAN.CN management portal](https://www.vlan.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational cautions for credential handling, installer verification, privileged commands, and network diagnostics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
