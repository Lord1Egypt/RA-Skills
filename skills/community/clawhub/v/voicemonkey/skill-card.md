## Description: <br>
Control Alexa devices via VoiceMonkey API v2 to make announcements, trigger routines, start flows, and display media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayakumark](https://clawhub.ai/user/jayakumark) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare VoiceMonkey API calls and configuration for Alexa/Echo announcements, media playback, routine triggers, and flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VoiceMonkey tokens can authorize control of Alexa devices if exposed. <br>
Mitigation: Prefer Authorization headers over URL query tokens, keep the token private, and rotate it if exposed. <br>
Risk: Announcements, media playback, websites, routines, and flows may create unexpected noise or device actions. <br>
Mitigation: Require explicit confirmation of the target device, content, and action before execution. <br>
Risk: Alexa routines may control high-impact devices such as locks, alarms, purchases, or other connected systems. <br>
Mitigation: Apply extra review or restrict use before triggering routines tied to sensitive devices or irreversible actions. <br>


## Reference(s): <br>
- [VoiceMonkey Website](https://voicemonkey.io) <br>
- [Voice Monkey Console and API Playground](https://console.voicemonkey.io) <br>
- [VoiceMonkey API Base URL](https://api-v2.voicemonkey.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/jayakumark/voicemonkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples, JSON payloads, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the VOICEMONKEY_TOKEN environment variable and VoiceMonkey device or flow identifiers supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
