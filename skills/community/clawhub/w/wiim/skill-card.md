## Description:

Control WiiM audio devices (play, pause, stop, next, prev, volume, mute, play URLs, presets). Use when the user wants to control music playback, adjust volume, discover WiiM/LinkPlay speakers on the network, or play audio from a URL on a WiiM device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geodeterra](https://clawhub.ai/user/geodeterra)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to discover and control WiiM or LinkPlay audio devices on a local network, including playback, volume, presets, and direct audio URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install or run the third-party wiim-cli package without pinning a version.

Mitigation: Verify that wiim-cli is the package intended for use, pin a trusted version in managed environments, and grant only the local network and account access needed to control WiiM devices.

Risk: Device discovery and control operate on the local network and can affect available WiiM or LinkPlay speakers.

Mitigation: Use --host when targeting a specific device and run commands only on trusted local networks.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
