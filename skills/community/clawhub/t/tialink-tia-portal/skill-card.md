## Description:

Operate a Siemens TIA Portal (V19 / V20 / V21) project from an AI agent - hardware and network configuration, FB/FC/DB/UDT creation with SCL, compile, download to S7-PLCSIM, read-back verification. Use when the user mentions TIA Portal, Siemens PLC automation, SCL programming, rack configuration or Openness, or wants an agent to work inside a PLC project. Requires the TiaLink gateway on the TIA Portal machine (commercial software; read-only without a licence).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tia-forge](https://clawhub.ai/user/tia-forge)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Developers and industrial automation engineers use this skill to guide an AI agent through inspecting and changing Siemens TIA Portal projects via a TiaLink gateway, including SCL block creation, compile checks, and simulation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway uses bearer-token authentication, and remote connections can expose the token if they are not encrypted.

Mitigation: Keep the gateway private, protect the token, and use an SSH tunnel, VPN, or TLS for remote connections.

Risk: Changes to PLC projects or downloads to equipment can have production consequences.

Mitigation: Start in a scratch project and simulation, export backups, retain operator control over production changes, and verify changes with compile output and read-back results.

## Reference(s):

- [TiaLink product information](https://tia.hubwiz.com/tia-link?utm_source=clawhub&utm_medium=skill)
- [TiaLink repository](https://github.com/tia-forge/tialink)
- [ClawHub skill page](https://clawhub.ai/tia-forge/skills/tialink-tia-portal)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown checklists, configuration examples, shell commands, and SCL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TiaLink gateway on a Windows machine with TIA Portal and Siemens Openness; write operations require a gateway license.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
