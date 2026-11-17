## Description:

Generate MP3 speech with OpenAI TTS through RunAPI. Use for one-off speech generation or application integration. Prefer the RunAPI CLI for one-off requests and the target-language SDK for production integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate OpenAI TTS MP3 audio through RunAPI for one-off speech artifacts or to plan SDK-based application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunAPI is an intermediary for OpenAI TTS requests and generated audio delivery.

Mitigation: Install and use the skill only when routing text, authentication, and generated audio through RunAPI is acceptable.

Risk: Requests may create paid RunAPI or OpenAI TTS work and consume account quota.

Mitigation: Review request JSON before submission, submit once, and require user authorization before any additional paid request.

Risk: The skill relies on RunAPI authentication through an API key or existing CLI auth.

Mitigation: Prefer environment auth or saved CLI configuration, avoid browser login unless explicitly chosen, and do not expose credentials in outputs.

## Reference(s):

- [OpenAI TTS model overview](https://runapi.ai/models/openai-tts.md)
- [RunAPI OpenAI provider overview](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [OpenAI TTS homepage](https://runapi.ai/models/openai-tts)
- [OpenAI TTS SDK integration](https://github.com/runapi-ai/openai-tts-sdk)
- [tts-1 variant](https://runapi.ai/models/openai-tts/tts-1.md)
- [tts-1-hd variant](https://runapi.ai/models/openai-tts/tts-1-hd.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to preserve complete RunAPI responses and verify downloaded audio deliverables.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
