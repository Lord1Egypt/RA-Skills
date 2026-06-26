## Description: <br>
Relive helps an agent create and converse with AI digital replicas from chat logs, reference audio, and optional images, with text, voice, or video output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoonasKahnwald](https://clawhub.ai/user/JoonasKahnwald) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Relive to build a persona from authorized chat, voice, and image materials, then converse with that persona through text, voice, or video while preserving character-specific context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists imported chats, derived personality profiles, voice references, generated media, and future conversations for each character. <br>
Mitigation: Install only when persistent local storage is acceptable, and manually inspect or delete character storage and USER.md entries when they are no longer needed. <br>
Risk: The skill can create replicas of real people from sensitive chat, voice, and image material. <br>
Mitigation: Use it only with clear authorization from the person represented or another lawful basis, and avoid non-consensual impersonation, deception, or forgery. <br>
Risk: Voice and video flows may send content or configuration to third-party services such as OpenAI or Volc Engine. <br>
Mitigation: Review OpenAI and Volc Engine API settings before use and do not process sensitive material through those services without appropriate consent and authorization. <br>


## Reference(s): <br>
- [ClawHub Relive release page](https://clawhub.ai/JoonasKahnwald/relive) <br>
- [CosyVoice repository](https://github.com/FunAudioLLM/CosyVoice.git) <br>
- [Volc Engine video generation documentation](https://www.volcengine.com/docs/82379/1099522) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, audio, video] <br>
**Output Format:** [JSON command files, Markdown profile and chat files, text replies, and optional generated audio or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice mode requires reference audio with matching transcript text; video mode requires reference image configuration and a configured Volc Engine endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
