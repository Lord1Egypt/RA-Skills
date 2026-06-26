## Description: <br>
RoomSound helps an agent play YouTube audio, build playback queues, discover speakers, and switch Bluetooth or local audio outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icecat2005](https://clawhub.ai/user/icecat2005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use RoomSound to let an agent initialize local audio tooling, discover available speakers, create speaker aliases, queue YouTube audio, and switch playback between Bluetooth or system audio outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install local audio and Bluetooth packages and write persistent yt-dlp configuration. <br>
Mitigation: Ask for user confirmation before package installs or persistent configuration writes when tighter control is needed. <br>
Risk: The skill can switch Bluetooth speakers or audio sinks, which may disrupt active playback or route audio to an unintended device. <br>
Mitigation: Confirm before switching active speakers, validate speaker aliases and MAC addresses, and summarize detected devices before changes. <br>
Risk: The skill constructs shell commands from user-provided YouTube searches, URLs, speaker aliases, and MAC addresses. <br>
Mitigation: Strip shell metacharacters from user-supplied text and validate MAC addresses before command execution. <br>


## Reference(s): <br>
- [RoomSound ClawHub release page](https://clawhub.ai/icecat2005/roomsound) <br>
- [RoomSound Quick Start Guide](artifact/QUICK-START-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and concise user-facing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installation, persistent yt-dlp configuration, Bluetooth speaker changes, and speaker alias storage.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
