## Description:

Call GPT generation and OpenAI text embedding models through RunAPI using OpenAI-compatible clients. Use for chat, Responses, embeddings, streaming, tools, vision, or an existing compatibility client that needs the conditional reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure OpenAI-compatible clients for GPT generation and embeddings through RunAPI, or to apply its conditional Anthropic Messages and Gemini compatibility guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests, including compatibility-client messages, are sent to RunAPI; the artifact review does not verify the service's retention practices.

Mitigation: Use a RunAPI-issued key scoped to the intended client and confirm RunAPI's data-handling terms before sending confidential content.

## Reference(s):

- [RunAPI GPT model documentation](https://runapi.ai/models/gpt.md)
- [RunAPI GPT service page](https://runapi.ai/models/gpt)
- [RunAPI OpenAI provider guide](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [GPT compatibility protocols](references/compatibility-protocols.md)
- [ClawHub release page](https://clawhub.ai/runapi-ai/skills/runapi-gpt)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with configuration examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-specific endpoint, transport, and response-verification guidance.]

## Skill Version(s):

0.2.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
