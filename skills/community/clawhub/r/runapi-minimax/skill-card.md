## Description:

Call the MiniMax text API (MiniMax-M3 through MiniMax-M2) through RunAPI using OpenAI-compatible Chat Completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure RunAPI credentials and call MiniMax text chat models through OpenAI-compatible Chat Completions, including streaming when needed. Existing clients can use the compatibility reference for Anthropic Messages or Gemini contents only when that protocol is already required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and outputs are sent to RunAPI's MiniMax service when the configured client uses this skill.

Mitigation: Confirm that using RunAPI for the target prompts and outputs is intended before installation or execution.

Risk: Using an unrelated OpenAI key or applying the RunAPI base URL globally could route unintended requests to the wrong provider.

Mitigation: Use a RunAPI API key and set OPENAI_BASE_URL to https://runapi.ai/v1 only for clients that should use this provider.

## Reference(s):

- [MiniMax on RunAPI documentation](https://runapi.ai/models/minimax.md)
- [MiniMax provider page](https://runapi.ai/providers/minimax.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI MiniMax homepage](https://runapi.ai/models/minimax)
- [Compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline code examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, environment variable, streaming, verification, retry, and stop-boundary guidance.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
