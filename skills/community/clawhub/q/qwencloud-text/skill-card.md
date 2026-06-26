## Description: <br>
Generates text, conducts conversations, writes code, reasons, and calls functions with Qwen models through the QwenCloud OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send text, chat, coding, reasoning, and function-calling requests to QwenCloud models while keeping API credentials in environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and outputs may be sent to QwenCloud or DashScope using sensitive API credentials. <br>
Mitigation: Install only if the QwenCloud integration is trusted, keep keys in environment variables or placeholder .env entries, and never print credential values. <br>
Risk: Update-management behavior can prompt installing another skill and write persistent local state. <br>
Mitigation: Review update prompts before approving them and require explicit confirmation before installing extra skills or modifying persistent agent configuration. <br>
Risk: An untrusted QWEN_BASE_URL could redirect requests away from the intended QwenCloud endpoint. <br>
Mitigation: Avoid untrusted base URL values and verify endpoint configuration before sending requests. <br>


## Reference(s): <br>
- [API guide](references/api-guide.md) <br>
- [Execution guide](references/execution-guide.md) <br>
- [Prompt guide](references/prompt-guide.md) <br>
- [Agent compatibility](references/agent-compatibility.md) <br>
- [Official documentation sources](references/sources.md) <br>
- [Qwen API reference](https://docs.qwencloud.com/api-reference/chat/dashscope) <br>
- [OpenAI compatibility with DashScope](https://docs.qwencloud.com/api-reference/chat/openai-responses#compatibility-with-openai) <br>
- [Function calling](https://docs.qwencloud.com/developer-guides/text-generation/function-calling) <br>
- [QwenCloud model list](https://www.qwencloud.com/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API requests, shell commands, and generated model text or saved JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream responses; can save JSON response files when requested.] <br>

## Skill Version(s): <br>
0.2.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
