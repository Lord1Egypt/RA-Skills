## Description: <br>
Push text notifications to Windows Azure TTS service for audio broadcast via Bluetooth speakers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmosakg](https://clawhub.ai/user/cmosakg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send spoken reminders, alarms, and announcements from an OpenClaw agent to a configured Windows TTS server on their network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text may cross the local network over HTTP and be heard by people near the speaker. <br>
Mitigation: Use the skill only on a trusted LAN, prefer authenticated or encrypted transport where available, and avoid sensitive or embarrassing message content. <br>
Risk: Scheduled announcements can disclose private reminders or play in the wrong physical context. <br>
Mitigation: Use neutral wording for scheduled reminders and test speaker placement, volume, and timing before relying on recurring broadcasts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cmosakg/windows-tts) <br>
- [Publisher profile](https://clawhub.ai/user/cmosakg) <br>
- [README](artifact/README.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON responses from TTS tools with Markdown and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends configured text, voice, volume, status, and voice-list requests to a Windows TTS server.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
