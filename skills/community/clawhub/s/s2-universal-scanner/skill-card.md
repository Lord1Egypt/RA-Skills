## Description:

S2-SP-OS Universal Spatial Sensor Sniffer scans LAN environments for S2-native Zero-Knowledge Heartbeats, legacy sensor protocols such as Modbus and MQTT, and Gateway API registry entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent to run a Python-based spatial sensor discovery workflow and summarize detected S2-native, legacy, and gateway-listed devices. Review is required before using its findings for inventory, security, onboarding, or automation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill claims real IoT discovery while inspected code returns hardcoded device results and tells agents to present them as real findings.

Mitigation: Treat outputs as review-required until the publisher replaces hardcoded demo output with verifiable discovery and clearly labels any simulations.

Risk: The skill can influence inventory, onboarding, security, or automation decisions using scan-like output.

Mitigation: Require explicit authorization, human review, and independent verification before acting on discovered devices or onboarding recommendations.

Risk: The skill accepts an optional Home Assistant token environment variable.

Mitigation: Use least-privilege credentials, avoid logging tokens, and run only in environments where credential handling has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-universal-scanner)
- [S2-SP-OS homepage](https://space2.world/s2-sp-os)
- [Space2 developer reference](https://space2.world/developer)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from a Python CLI, with Markdown usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and requests; uses S2_PRIVACY_CONSENT and optionally S2_HA_TOKEN.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
