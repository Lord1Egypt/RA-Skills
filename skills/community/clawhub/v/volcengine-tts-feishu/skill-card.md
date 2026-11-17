## Description:

Synthesizes Chinese speech with Volcengine Doubao TTS 2.0, supports voice, emotion, and SSML controls, and can optionally send the generated audio as a Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate Chinese speech audio from text through Volcengine Doubao TTS and, when configured, deliver the result into Feishu as an audio message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu sending path uses local app credentials and has credential-handling weaknesses.

Mitigation: Use narrowly scoped Feishu app permissions, avoid sensitive text unless third-party processing is acceptable, and avoid passing tokens through command-line arguments.

Risk: Temporary audio handling and dependency declaration may need hardening before sensitive or production use.

Mitigation: Use atomically created temporary files, fixed dependency versions, and an in-process HTTP upload path instead of shelling out to curl.

## Reference(s):

- [Volcengine TTS voice list](https://www.volcengine.com/docs/6561/1257544)
- [Volcengine HTTP TTS API](https://www.volcengine.com/docs/6561/1598757)
- [Feishu OpenAPI](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of MP3 or Opus audio files and Feishu audio-message API calls when the user supplies credentials.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
