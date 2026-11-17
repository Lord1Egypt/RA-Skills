## Description:

Generate multi-speaker speech with Gemini TTS through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize dialogue or integrate Gemini TTS through RunAPI, choosing between CLI-based one-off generation and SDK-based application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted prompts or media may be sent to RunAPI's service and may incur usage charges.

Mitigation: Confirm trust in RunAPI and its Homebrew tap before installation, and use an API key with appropriate billing limits.

Risk: The skill depends on RunAPI authentication and the installed runapi command catalog matching the requested Gemini TTS operation.

Mitigation: Check authentication and inspect the current CLI/API contract before submitting a request; stop on missing services or contract mismatches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-gemini-tts)
- [RunAPI Gemini TTS model overview](https://runapi.ai/models/gemini-tts)
- [RunAPI Gemini TTS model documentation](https://runapi.ai/models/gemini-tts.md)
- [RunAPI Google provider overview](https://runapi.ai/providers/google.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Gemini TTS SDK](https://github.com/runapi-ai/gemini-tts-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create request, task, result, and downloaded media files when executing Gemini TTS workflows.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
