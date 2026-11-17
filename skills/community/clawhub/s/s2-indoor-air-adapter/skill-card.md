## Description:

Provides agent commands for discovering LAN air sensors, wrapping local MQTT/HTTP-style readings into spatial grid JSON, and presenting offline comfort or energy suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, smart-home operators, and agent users can use this skill to invoke a Python adapter for indoor air sensor discovery, consent-gated local readings, spatial labeling, and local linkage suggestions. Users should validate devices and readings before relying on the output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present simulated discovered devices or sensor readings as real data.

Mitigation: Treat all discovered devices and air-quality readings as untrusted until verified against known hardware or an independent monitoring source.

Risk: Discovery mode may broadcast on the user's LAN while running under local exec permissions.

Mitigation: Run discovery only on networks where scanning is authorized and keep the scan scope limited to the intended local subnet.

Risk: The artifact claims broad MQTT/HTTP device support but the included script uses mock data paths rather than real device integrations.

Mitigation: Confirm that real device communication and data provenance are implemented before using the skill for operational decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-indoor-air-adapter)
- [Publisher Profile](https://clawhub.ai/user/spacesq)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output from the adapter script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and local execution; discovery mode may broadcast on the user's LAN.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
