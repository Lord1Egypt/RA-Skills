## Description:

Guides developers in calling Gemini 2.5 and 3 models through RunAPI for chat, streaming, multimodal input, grounding, and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure RunAPI credentials and call Gemini models through the Gemini contents protocol, with compatibility guidance for existing OpenAI-style clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini prompts and included content are sent to RunAPI.

Mitigation: Use only when RunAPI data handling meets your requirements; avoid sending sensitive content otherwise.

Risk: RunAPI API keys can be exposed if handled carelessly.

Mitigation: Keep GEMINI_API_KEY and any OPENAI_API_KEY secret; do not include them in prompts, logs, or shared files.

## Reference(s):

- [RunAPI Gemini documentation](https://runapi.ai/models/gemini.md)
- [RunAPI Gemini model page](https://runapi.ai/models/gemini)
- [RunAPI Google provider documentation](https://runapi.ai/providers/google.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Compatibility protocols](artifact/references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes response-completeness checks and retry boundaries.]

## Skill Version(s):

0.2.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
