## Description:

Voice Broadcast controls text-to-speech playback for AI replies, including manual reading, automatic voice broadcast, mute, and unmute behavior for Feishu channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-zz](https://clawhub.ai/user/gabriel-zz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive AI responses as voice messages when audio delivery is preferable, such as on iOS or when hands-free access is needed. It supports command-based and automatic playback control within Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can override mute for undefined urgent content and send Feishu audio despite a silence preference.

Mitigation: Review the urgent-content broadcast rule before installation and require explicit opt-in or remove the mute override in shared, workplace, or sensitive environments.

Risk: Automatic voice broadcast may expose reply content in Feishu channels where nearby listeners can hear the audio.

Mitigation: Use manual reading or keep mute enabled for sensitive conversations, and limit installation to Feishu contexts where audio playback is appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gabriel-zz/skills/voice-broadcast)
- [Publisher profile](https://clawhub.ai/user/gabriel-zz)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with command-triggered state changes and text-to-speech behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update voice_state.json and send Feishu voice messages when triggered.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
