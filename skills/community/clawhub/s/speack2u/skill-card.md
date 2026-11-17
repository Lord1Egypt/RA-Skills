## Description:

Configure TTS in OpenClaw and adapt speech output to user preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zktufo](https://clawhub.ai/user/zktufo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure text-to-speech behavior and maintain concise voice-output preferences for future spoken responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist learned voice-output preferences into its own instructions over time.

Mitigation: Require explicit confirmation before saving preferences, and periodically review or clear the Voice, Style, Spoken Text, and Avoid sections.

## Reference(s):

- [OpenClaw TTS Configuration](artifact/config.md)
- [Criteria for Voice Preferences](artifact/criteria.md)
- [ClawHub Skill Page](https://clawhub.ai/zktufo/skills/speack2u)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise preference entries for voice, style, spoken text, and avoided speech patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
