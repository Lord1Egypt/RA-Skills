## Description:

Reads sensor data and controls Tuya IoT devices through the Tuya Cloud API or local LAN, including device listing, environmental and status readings, moisture averages, and switch or valve commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minshi-veyt](https://clawhub.ai/user/minshi-veyt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and home automation operators use this skill to configure Tuya API credentials, discover linked Smart Life/Tuya devices, read sensor status, calculate soil-moisture averages, and send cloud or LAN control commands to switches and valves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud or LAN commands can operate real Tuya devices, including valves and switches.

Mitigation: Review each proposed command before execution, use a restricted Tuya project, and avoid running bundled tests against live devices.

Risk: Tuya access secrets and local_key values can grant device-control access if exposed.

Mitigation: Keep .env out of source control, avoid sharing logs or transcripts containing secrets, and prefer safer secret storage before LAN control.

Risk: Unpinned dependency ranges may change runtime behavior over time.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [Tuya Developer Platform](https://platform.tuya.com)
- [Tuya Cloud Controller installation guide](https://medium.com/@min.shi.happy/building-a-tuya-smart-home-controller-skill-for-openclaw-beadb796c05c)
- [ClawHub skill page](https://clawhub.ai/minshi-veyt/skills/tuya-cloud)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown instructions with shell commands; command results may be JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tuya credentials for cloud operations; local LAN read/control requires device ID, IP address, and local_key.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
