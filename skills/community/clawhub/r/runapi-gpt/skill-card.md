## Description: <br>
Guides agents to call GPT generation and embedding models through RunAPI using OpenAI-compatible, Anthropic Messages, Gemini contents, or standard HTTP clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure GPT chat, Responses, streaming, multimodal, function calling, Codex, and embedding requests through RunAPI-compatible endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to RunAPI as a third-party remote GPT/OpenAI-compatible provider. <br>
Mitigation: Avoid sending sensitive, regulated, or internal data unless your organization approves RunAPI's handling, retention, and privacy terms. <br>
Risk: API credentials are required for use and could be exposed if copied into prompts, logs, or source files. <br>
Mitigation: Store the RunAPI token in environment variables such as OPENAI_API_KEY and keep credential values out of shared code and transcripts. <br>


## Reference(s): <br>
- [RunAPI GPT model page](https://runapi.ai/models/gpt) <br>
- [RunAPI GPT documentation](https://runapi.ai/models/gpt.md) <br>
- [RunAPI OpenAI provider page](https://runapi.ai/providers/openai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint selection guidance and required environment variable names; no executable files are produced.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
