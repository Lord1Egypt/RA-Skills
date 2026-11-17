## Description:

Send high-quality text-to-speech voice messages on WhatsApp in 40+ languages with automatic delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopyky](https://clawhub.ai/user/hopyky)

### License/Terms of Use:

MIT License

## Use Case:

External users and developers use this skill to generate text-to-speech audio and send it as WhatsApp voice messages to individuals or groups through Clawdbot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on external code and voice model downloads that can change outside this release.

Mitigation: Use pinned releases and checksums for the repository and model files before installation.

Risk: Normal use may automatically send generated audio to a default recipient or WhatsApp group.

Mitigation: Test with --no-send, avoid sensitive text, and verify target numbers or group IDs before sending.

Risk: The package evidence does not include the runnable implementation.

Mitigation: Review the installed implementation before enabling automatic delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hopyky/skills/tts-whatsapp)
- [Piper voice models](https://huggingface.co/rhasspy/piper-voices)
- [Piper voice samples](https://rhasspy.github.io/piper-samples/)
- [Clawdbot documentation](https://docs.clawd.bot)

## Skill Output:

**Output Type(s):** [audio, text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and configuration snippets; generated audio is OGG/Opus for WhatsApp.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate without sending by using --no-send; normal operation may automatically deliver messages to a configured recipient or WhatsApp group.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
