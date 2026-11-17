## Description:

Control and monitor Red Sea ReefBeat aquarium equipment directly over the local HTTP API, with support for ReefLED, ReefDose, ReefMat, ReefRun, ReefATO+, and ReefWave devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piwi3910](https://clawhub.ai/user/piwi3910)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover, monitor, and operate Red Sea ReefBeat aquarium equipment on their own local network. It is suited for local HTTP status checks and explicitly confirmed control actions for supported aquarium devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue write actions to aquarium life-support equipment, including pumps, dosing, auto top-off, firmware, reset, maintenance, emergency, and cloud-related endpoints.

Mitigation: Prefer read-only status checks first and require explicit user confirmation before any POST, PUT, DELETE, firmware, reset, maintenance, emergency, pump, dosing, ATO, or cloud-related action.

Risk: The supported devices use local HTTP on port 80 with no authentication.

Mitigation: Use the skill only for intended ReefBeat devices on a trusted local network and verify the target IP and endpoint before sending commands.

Risk: The security evidence says cloud credential examples require careful handling.

Mitigation: Do not provide ReefBeat cloud passwords through this skill and treat any documented cloud Basic credential as exposed.

## Reference(s):

- [ReefBeat Complete Local HTTP API Reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/piwi3910/skills/reefbeat)
- [Publisher profile](https://clawhub.ai/user/piwi3910)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local HTTP API calls that read status or change ReefBeat device state; write actions require user confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
