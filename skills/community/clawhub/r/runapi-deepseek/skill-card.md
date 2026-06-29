## Description: <br>
Call DeepSeek API models through RunAPI using OpenAI-compatible, Anthropic-compatible, or Gemini-compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure DeepSeek chat, streaming completions, model listing, and SDK-compatible requests through RunAPI. It is useful when adapting existing OpenAI-compatible or Anthropic-compatible client code to RunAPI endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are routed through an external API provider and may include sensitive prompts or outputs. <br>
Mitigation: Avoid sending secrets, private data, or regulated content unless authorized, and confirm the external API is approved for the use case. <br>
Risk: API tokens or base URLs can be misconfigured or exposed in code, commits, or shell history. <br>
Mitigation: Keep tokens in environment variables or a secret manager, verify the RunAPI base URL before use, and avoid inlining credentials. <br>


## Reference(s): <br>
- [RunAPI DeepSeek model documentation](https://runapi.ai/models/deepseek.md) <br>
- [RunAPI DeepSeek model page](https://runapi.ai/models/deepseek) <br>
- [RunAPI DeepSeek provider page](https://runapi.ai/providers/deepseek.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-deepseek) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with dotenv, Python, TypeScript, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and OPENAI_BASE_URL for OpenAI-compatible use; includes optional Anthropic-compatible settings and streaming guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
