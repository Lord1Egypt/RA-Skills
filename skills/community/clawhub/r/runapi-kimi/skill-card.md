## Description:

Call the Kimi API (kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5) through RunAPI using OpenAI-compatible Chat Completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure Kimi access through RunAPI for text chat, streaming responses, coding workloads, and compatibility clients that require Anthropic Messages or Gemini contents shapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests may be sent with the wrong credential or endpoint, causing authentication failures or unintended provider routing.

Mitigation: Use a scoped RunAPI key and confirm OPENAI_BASE_URL is set to https://runapi.ai/v1 for OpenAI-compatible Kimi clients.

Risk: Unsupported request shapes, automatic model changes, or protocol hopping can produce unreliable behavior.

Mitigation: Follow the documented stop boundaries: correct one rejected shape, retry transport once only when safe, and stop without changing model or protocol automatically.

## Reference(s):

- [Kimi model documentation](https://runapi.ai/models/kimi.md)
- [Moonshot AI provider page](https://runapi.ai/providers/moonshot-ai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Kimi on RunAPI homepage](https://runapi.ai/models/kimi)
- [Kimi compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python and endpoint configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenAI-compatible Chat Completions guidance plus conditional Anthropic Messages and Gemini compatibility notes.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
