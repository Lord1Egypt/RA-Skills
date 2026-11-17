## Description:

Guides agents in calling Claude models through RunAPI using Anthropic Messages, with conditional guidance for compatible OpenAI and Gemini clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure RunAPI credentials and call Claude models for chat, streaming, vision, tools, reasoning, and token counting. Existing OpenAI or Gemini clients can consult the compatibility guidance where applicable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A RunAPI key and model requests are sent through a third-party provider.

Mitigation: Confirm RunAPI is the intended provider, protect the API key, and review what data is sent before use.

Risk: A model or protocol mismatch can yield an invalid request or misleading result.

Mitigation: Use an exact supported model and protocol, and check the final response and usage before relying on it.

## Reference(s):

- [ClawHub release](https://clawhub.ai/runapi-ai/skills/runapi-claude)
- [RunAPI Claude model page](https://runapi.ai/models/claude)
- [RunAPI Claude documentation](https://runapi.ai/models/claude.md)
- [RunAPI Anthropic provider documentation](https://runapi.ai/providers/anthropic.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Code]

**Output Format:** [Markdown with configuration steps and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides response-verification and retry boundaries; does not execute code or persist changes.]

## Skill Version(s):

0.2.18 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
