## Description: <br>
Call the Qwen text API (qwen3-next-80b-a3b-instruct) through RunAPI using the official OpenAI SDK or compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure OpenAI-compatible clients for RunAPI-hosted Qwen text chat, streaming completions, and protocol-compatible Anthropic or Gemini client surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes prompts to RunAPI and depends on a RunAPI API key. <br>
Mitigation: Store the token in a secret manager or local environment file, and scope OPENAI_BASE_URL=https://runapi.ai/v1 only to projects or shells that should use RunAPI. <br>


## Reference(s): <br>
- [RunAPI Qwen model page](https://runapi.ai/models/qwen) <br>
- [Qwen model documentation](https://runapi.ai/models/qwen.md) <br>
- [RunAPI Alibaba provider documentation](https://runapi.ai/providers/alibaba.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with dotenv, Python, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and OPENAI_BASE_URL; keep the RunAPI token in a secret manager or local environment file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
