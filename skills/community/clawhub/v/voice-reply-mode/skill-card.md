## Description: <br>
Adds same-modality conversation behavior to an agent so voice messages receive voice replies and text messages receive text replies, using Edge TTS guidance and gateway configuration snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nasplycc](https://clawhub.ai/user/nasplycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure agents for Telegram, Feishu, or similar voice-note workflows where inbound voice/audio should trigger TTS voice replies while inbound text remains text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled configuration defaults to a Chinese Edge TTS voice and locale, which may not match every deployment or user preference. <br>
Mitigation: Confirm the desired language and voice before producing audio, and replace the default voice or locale in the workspace snippets and gateway configuration when needed. <br>
Risk: Same-modality replies depend on gateway TTS settings, channel permissions, plugin support, and media upload behavior; workspace snippets alone may not enable automatic voice replies. <br>
Mitigation: Enable and verify the gateway messages.tts settings, confirm channel audio permissions, then test with one text message and one voice message before rollout. <br>


## Reference(s): <br>
- [Voice Reply Mode release page](https://clawhub.ai/nasplycc/voice-reply-mode) <br>
- [Workspace snippets](references/workspace-snippets.md) <br>
- [Gateway config](references/gateway-config.md) <br>
- [Channel notes](references/channel-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline configuration snippets and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workspace documentation snippets, gateway configuration examples, and an Edge TTS helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
