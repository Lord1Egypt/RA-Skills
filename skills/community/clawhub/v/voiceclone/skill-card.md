## Description: <br>
Voice cloning and TTS using MiniMax API. User must provide a voice name when cloning; after success, voice_name->voice_id is written back to this skill doc for reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SocketNet](https://clawhub.ai/user/SocketNet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to clone a user-provided voice with MiniMax, synthesize text with a cloned or existing voice, and reuse saved display-name to voice-id mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads voice samples to MiniMax for cloning and stores reusable voice mappings, which can involve sensitive voice data and consent obligations. <br>
Mitigation: Use only voice data the user has rights and consent to clone, keep MiniMax API keys in environment variables, and review saved voice mappings before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SocketNet/voiceclone) <br>
- [MiniMax upload clone audio endpoint](https://api.minimax.io/v1/files/upload) <br>
- [MiniMax voice clone endpoint](https://api.minimax.io/v1/voice_clone) <br>
- [MiniMax text-to-speech endpoint](https://api.minimax.io/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, audio files] <br>
**Output Format:** [Markdown instructions with Python CLI commands; the script can produce audio files and update SKILL.md voice mappings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key and user-provided audio that meets the documented format, duration, and size limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
