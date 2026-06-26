## Description: <br>
Voice Broadcast lets an agent read replies aloud through Feishu voice messages, with commands to read the latest reply, enable or disable automatic readout, and mute or unmute playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gabriel-ZZ](https://clawhub.ai/user/Gabriel-ZZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill when they want assistant replies delivered as Feishu voice audio, especially when reading text is inconvenient or hands-free playback is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant replies may contain sensitive information that becomes audible when converted to Feishu voice audio. <br>
Mitigation: Use the skill only in contexts where voice playback is acceptable and where recipients understand that replies may be sent as audio. <br>
Risk: Urgent-content handling can override mute behavior. <br>
Mitigation: Review or remove the mute override before using the skill in private, medical, regulated, or shared-audio environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration, API calls] <br>
**Output Format:** [Agent instructions that produce Feishu voice audio behavior and short text status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains voice broadcast state for automatic readout and mute behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
