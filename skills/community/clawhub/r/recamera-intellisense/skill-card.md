## Description:

Helps agents register and control reCamera Pro devices for detection, recording, capture, storage management, and GPIO automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichizer0](https://clawhub.ai/user/ichizer0)

### License/Terms of Use:

MIT-0

## Use Case:

Device owners and developers use this skill to configure and monitor reCamera Pro cameras, inspect detection events and recordings, capture media, and administer connected devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic device discovery may expose bearer tokens over plaintext or unverified connections.

Mitigation: Register known devices with an explicit protocol; use HTTP or unverified TLS with tokens only on a trusted LAN.

Risk: Saved device credentials and exported configuration backups may disclose access to cameras.

Mitigation: Treat the device registry and exported configuration archives as sensitive; restrict access and avoid sharing them.

Risk: Storage operations, deletion, reboot, app changes, GPIO, and model switching can disrupt devices or erase data.

Mitigation: Use only on devices you own or administer, and get explicit approval before disruptive or destructive actions.

## Reference(s):

- [reCamera Intellisense on ClawHub](https://clawhub.ai/ichizer0/skills/recamera-intellisense)
- [reCamera Intellisense API Reference](artifact/REFERENCE.md)
- [reCamera Pro getting started](https://wiki.seeedstudio.com/recamera_pro_getting_started/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Device responses can include JSON, captured media, or links to recordings.]

## Skill Version(s):

2.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
