## Description:

Transcribe uploaded audio through RunAPI with an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to transcribe audio through RunAPI for one-off results, subtitle output, multilingual hints, or application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the RunAPI CLI, Homebrew tap, and SDK sources.

Mitigation: Install and use it only when those RunAPI distribution sources are trusted for the target environment.

Risk: RunAPI authentication may expose a reusable API key if handled carelessly.

Mitigation: Prefer environment authentication or saved CLI configuration with a dedicated RunAPI API key where possible.

Risk: A transcription response could point the agent to unexpected non-transcript media.

Mitigation: Validate requested deliverables against the discovered response contract and expected MIME type before treating downloads as complete.

Risk: Retrying a submitted service request can create cost or duplicate work.

Mitigation: Submit once, retry transport failures only when evidence shows no task was created or billed, and request user authorization before another paid submission.

## Reference(s):

- [RunAPI OpenAI Transcription model overview](https://runapi.ai/models/openai-transcription.md)
- [RunAPI OpenAI provider overview](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI OpenAI Transcription homepage](https://runapi.ai/models/openai-transcription)
- [OpenAI Transcription SDK](https://github.com/runapi-ai/openai-transcription-sdk)
- [gpt-transcribe variant](https://runapi.ai/models/openai-transcription/gpt-transcribe.md)
- [whisper-1 variant](https://runapi.ai/models/openai-transcription/whisper-1.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to preserve transcription results in the requested JSON, text, SRT, VTT, or other discovered response format.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
