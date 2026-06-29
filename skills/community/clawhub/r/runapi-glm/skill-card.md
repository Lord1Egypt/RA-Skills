## Description: <br>
Call the GLM API through RunAPI using the official OpenAI SDK or compatible clients for chat, streaming completions, Anthropic-compatible requests, and Gemini-compatible requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure GLM model calls through RunAPI with OpenAI-compatible defaults and protocol compatibility notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunAPI credentials could be exposed if real API keys are committed, pasted into shared logs, or stored in shell history. <br>
Mitigation: Use a secret manager or environment variables for OPENAI_API_KEY, avoid committing real tokens, and rotate any key that may have been exposed. <br>
Risk: Requests may be sent to the wrong service if OPENAI_BASE_URL is not set to the intended RunAPI endpoint. <br>
Mitigation: Set OPENAI_BASE_URL deliberately to https://runapi.ai/v1 for this integration and verify endpoint configuration before use. <br>


## Reference(s): <br>
- [RunAPI GLM model page](https://runapi.ai/models/glm) <br>
- [RunAPI GLM documentation](https://runapi.ai/models/glm.md) <br>
- [RunAPI Z.ai provider page](https://runapi.ai/providers/z-ai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-glm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable names and OpenAI-compatible endpoint examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
