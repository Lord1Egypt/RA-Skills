## Description:

Set up real-time voice conversations. Phone calls, voice agents, live speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure OpenClaw real-time voice experiences for phone calls, web voice chat, or voice agents. It helps choose an appropriate provider path and produce configuration guidance for services such as ElevenLabs, Twilio, Telnyx, OpenAI TTS, and webhook tunnels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys, account SIDs, auth tokens, and voice service credentials could be exposed during setup.

Mitigation: Keep provider secrets out of source control and use environment variables or a secrets manager.

Risk: Public webhook routes and temporary tunnels can expose voice endpoints more broadly than intended.

Mitigation: Validate webhook signatures, restrict exposed routes, and disable temporary tunnels when setup or testing is finished.

Risk: The optional external phone-voice skill may add behavior beyond this documentation-only setup guidance.

Mitigation: Review or pin the external phone-voice skill before installing it.

## Reference(s):

- [Talk Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/talk)
- [Twilio](https://www.twilio.com/)
- [Telnyx](https://telnyx.com/)
- [ElevenLabs](https://elevenlabs.io/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider-specific setup steps, webhook tunnel commands, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
