## Description:

RoomSound helps agents play audio through speakers, starting with YouTube playback and Bluetooth speaker switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icecat2005](https://clawhub.ai/user/icecat2005)

### License/Terms of Use:


## Use Case:

Developers and end users use RoomSound to let an agent initialize audio dependencies, discover Bluetooth and system audio outputs, switch speakers, and build YouTube playback queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install packages, change audio or Bluetooth state, start long playback queues, and write persistent configuration.

Mitigation: Review setup and repair actions before approval, and confirm disruptive speaker switching or persistent configuration changes with the user.

Risk: User-provided media arguments can create command-execution risk if they are not validated before playback.

Mitigation: Validate URLs and MAC addresses before use, and prefer playback commands that separate mpv options from user-provided media arguments.

## Reference(s):

- [RoomSound ClawHub Skill Page](https://clawhub.ai/icecat2005/skills/roomsound)
- [RoomSound Quick Start Guide](artifact/QUICK-START-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include playback queues, speaker-discovery summaries, install hints, and persistent audio configuration guidance.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
