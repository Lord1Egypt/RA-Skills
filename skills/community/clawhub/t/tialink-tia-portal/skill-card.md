## Description:

Operate a Siemens TIA Portal (V17 / V18 / V19 / V20 / V21) project from an AI agent - hardware and network configuration, FB/FC/DB/UDT creation with SCL, compile, download to S7-PLCSIM, read-back verification. Use when the user mentions TIA Portal, Siemens PLC automation, SCL programming, rack configuration or Openness, or wants an agent to work inside a PLC project. Requires the TiaLink gateway on the TIA Portal machine (commercial software; read-only without a licence).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tia-forge](https://clawhub.ai/user/tia-forge)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Developers and controls engineers use this skill to guide an AI agent through inspecting and working with Siemens TIA Portal PLC projects via a TiaLink gateway. It covers hardware configuration, PLC block and SCL work, compilation, simulation downloads, and read-back checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned `npx tialink-mcp` invocation as a supply-chain risk; the scan did not establish malicious intent and was partial.

Mitigation: Review the package and its permissions, prefer an exact reviewed version with integrity checks over an unpinned invocation, and limit access to tokens and local files.

Risk: The gateway uses plain HTTP with a long-lived bearer token, so exposing it beyond a trusted local network can expose credentials.

Mitigation: Keep the gateway on the TIA Portal machine or a trusted LAN, do not expose port 8080 to the internet, and use an SSH tunnel, VPN, or TLS termination for remote access. Store the token outside prompts, commits, screenshots, and shared logs.

Risk: PLC project writes and downloads can affect industrial equipment, and the skill states that TIA Portal has no undo for a bad download.

Mitigation: Use a scratch project for initial work, default to simulation, compile and read back each change, and require an operator to confirm the target and maintenance window before downloading to real hardware.

## Reference(s):

- [TiaLink product page](https://tia.hubwiz.com/tia-link?utm_source=clawhub&utm_medium=skill)
- [TiaLink project repository (declared in skill metadata)](https://github.com/tia-forge/tialink)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code]

**Output Format:** [Markdown instructions with JSON, shell command, and SCL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for agent actions through a TiaLink gateway; write, compile, and download operations require a licence.]

## Skill Version(s):

1.0.9 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
