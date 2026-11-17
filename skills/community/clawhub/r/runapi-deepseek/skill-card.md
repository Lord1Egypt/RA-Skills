## Description:

Call the DeepSeek API through RunAPI using OpenAI-compatible Chat Completions and Responses, with deepseek-flash as the current V4.1 Flash 1017 model and the v4 names as compatibility aliases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure clients and send and verify DeepSeek API requests through RunAPI, with optional Anthropic Messages or Gemini contents guidance for existing clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, messages, and supported images are sent to RunAPI, which may not be approved for all data.

Mitigation: Confirm RunAPI is approved for the data being sent and use a RunAPI-specific API key.

Risk: Environment settings could redirect unintended clients, and API usage may incur charges.

Mitigation: Scope environment settings to the intended client and monitor API usage.

## Reference(s):

- [RunAPI DeepSeek model page](https://runapi.ai/models/deepseek)
- [DeepSeek API documentation](https://runapi.ai/models/deepseek.md)
- [RunAPI DeepSeek provider page](https://runapi.ai/providers/deepseek.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [DeepSeek V4.1 Flash model reference](https://runapi.ai/models/deepseek/v4.1-flash.md)
- [Compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown instructions with Python code examples and API request recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model- and protocol-specific examples; no fixed output length]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
