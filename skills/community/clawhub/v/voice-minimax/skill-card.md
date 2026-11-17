## Description:

Generates MiniMax text-to-speech audio, converts it to OPUS or MP3, and sends it to a specified Feishu/Lark user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn supplied text into spoken audio for self-introductions, message readouts, and content broadcasts delivered through Feishu/Lark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send generated audio to a default Feishu/Lark recipient, which may disclose user content to the wrong destination.

Mitigation: Replace the recipient with an explicitly chosen user, confirm the destination before each send, and use the skill only with non-sensitive text.

Risk: Inline command patterns can expose credentials or leave generated audio in temporary files.

Mitigation: Keep the MiniMax key out of command strings, use reviewed scripts with secure temporary files, and clean up generated MP3 and OPUS files after delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/voice-minimax)
- [MiniMax TTS API endpoint](https://api.minimaxi.com/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may create temporary MP3 and OPUS audio files before delivery through Feishu/Lark.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
