## Description:

S2-SP-OS Light Radar uses real LAN UDP discovery and local Hue/Wiz API calls to create a 4sqm voxel light memory record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover smart lights on a local network, read authorized Hue or Wiz device state, and summarize lighting conditions into spatial JSON records with offline lighting suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can actively probe the local network for smart lights using UDP broadcast and SSDP multicast.

Mitigation: Run discovery only after explicit user approval and only on networks where the user is authorized to scan for Hue or Wiz devices.

Risk: Authorized reads accept a device IP, which could be used against unintended local network destinations.

Mitigation: Restrict reads to user-confirmed Hue or Wiz IP addresses on the user's own LAN and avoid arbitrary or internet-routed destinations.

Risk: The packaged Python file appears malformed as submitted.

Mitigation: Review and test the artifact before deployment, and do not rely on runtime behavior until the package format is corrected.

## Reference(s):

- [S2-SP-OS Homepage](https://space2.world/s2-sp-os)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-light-perception)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON responses and concise guidance generated after running Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery returns device IP, vendor, and protocol data; authorized reads return spatial light state, estimated lux, vendor status, and offline linkage suggestions.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
