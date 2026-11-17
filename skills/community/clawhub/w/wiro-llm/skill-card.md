## Description:

Connect to language models through Wiro's gateway using OpenAI- or Anthropic-compatible clients, choose models, stream responses, use tools or structured output, and inspect call costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect applications and coding agents to language models through Wiro, configure supported request features, and understand usage costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests resend conversation history to Wiro, and calls are charged to the Wiro wallet.

Mitigation: Review and redact data before sending; check model pricing and limit usage, with automatic retries disabled for paid calls.

Risk: The skill includes optional image, audio, and video generation features beyond its stated chat and LLM purpose.

Mitigation: Review whether the media features are needed before using them and check their costs.

Risk: The supplied security analysis is incomplete because referenced local paths were missing.

Mitigation: Review the skill source and required behavior before installing it.

## Reference(s):

- [Wiro Completions API documentation](https://wiro.ai/docs/completions-api)
- [Wiro LLM models](https://wiro.ai/models?categories=llm-tool-call)
- [@wiro-ai/wiro-llm on npm](https://www.npmjs.com/package/@wiro-ai/wiro-llm)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code and bash, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover API requests, model selection, streaming, tools, structured output, and cost reporting.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
