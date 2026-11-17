## Description:

Generates text, supports conversations, writes code, reasons, and uses function calling with Qwen models through QwenCloud's OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to generate QwenCloud chat/completions requests, choose text models, troubleshoot execution, and run bundled Python or curl workflows for text generation, coding, reasoning, structured output, and function calling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API credentials are sent to QwenCloud when the skill executes model requests.

Mitigation: Install and use the skill only when sending prompts and credentials to QwenCloud is acceptable; keep API keys in environment variables or local .env files and avoid plaintext disclosure.

Risk: A custom QWEN_BASE_URL can redirect requests away from the default QwenCloud endpoint.

Mitigation: Review or unset QWEN_BASE_URL before use in untrusted project directories, and allow endpoint overrides only for trusted deployments.

Risk: The update workflow can suggest an npx skills add command for qwencloud/qwencloud-ai packages.

Mitigation: Run update commands only after verifying the exact package source and version; decline or suppress the prompt when the source has not been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-text)
- [Qwen Text Chat API Supplementary Guide](references/api-guide.md)
- [Qwen Text Chat Execution Guide](references/execution-guide.md)
- [Text Chat Prompt Guide](references/prompt-guide.md)
- [Qwen Text Chat Official Documentation](references/sources.md)
- [Qwen API reference](https://docs.qwencloud.com/api-reference/chat/dashscope)
- [OpenAI compatibility with DashScope](https://docs.qwencloud.com/api-reference/chat/openai-responses#compatibility-with-openai)
- [Function calling](https://docs.qwencloud.com/developer-guides/text-generation/function-calling)
- [QwenCloud model list](https://www.qwencloud.com/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples; optional JSON API responses saved by the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script can stream generated text to stdout and save response JSON with choices, usage, reasoning, and tool call fields to output/qwencloud-text/response.json.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
