## Description:

Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition (for example, messages starting with "User talked via voice recognition on <device>").

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent speak concise responses when the latest message explicitly indicates Voice Wake or voice-recognition input. It is intended for macOS local speech with an optional cloud TTS fallback when local `say` is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cloud TTS fallback can send selected assistant response text to a third-party service.

Mitigation: Avoid or disable the cloud fallback when responses may contain secrets, private code, personal data, financial data, or other confidential content.

Risk: Spoken responses may expose sensitive content to people nearby.

Mitigation: Use voice output only in appropriate listening environments and speak summaries instead of full details for long or sensitive responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-voice-wake-say)
- [ClawHub publisher profile](https://clawhub.ai/user/quincygunter)
- [HeyBossAI SkillBoss API Hub TTS endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples, plus spoken text when TTS is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local macOS `say` when available; optional cloud TTS fallback requires `SKILLBOSS_API_KEY` and may send selected response text to HeyBossAI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
