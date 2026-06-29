## Description: <br>
Calls MiniMax text chat models through RunAPI using the official OpenAI SDK or compatible clients, including streaming and OpenAI-, Anthropic-, and Gemini-compatible request surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure OpenAI-compatible clients for MiniMax text chat through RunAPI, including streaming, model listing, and protocol-compatible calls for existing Anthropic or Gemini tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if tokens are hard-coded, committed, or left in shell history. <br>
Mitigation: Store the RunAPI token in an environment variable or secret manager and avoid inlining credentials in source files or commands. <br>
Risk: Prompts and responses are sent to RunAPI/MiniMax when the skill is used. <br>
Mitigation: Use the skill only for data appropriate for that external service and review organizational privacy and compliance requirements before use. <br>
Risk: Misconfigured client settings can route requests to the wrong endpoint or fail unexpectedly. <br>
Mitigation: Set OPENAI_BASE_URL to https://runapi.ai/v1 and verify the intended MiniMax model ID before deployment. <br>


## Reference(s): <br>
- [RunAPI MiniMax homepage](https://runapi.ai/models/minimax) <br>
- [MiniMax model overview, pricing, and rate limits](https://runapi.ai/models/minimax.md) <br>
- [RunAPI MiniMax provider comparison](https://runapi.ai/providers/minimax.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill listing](https://clawhub.ai/runapi-ai/skills/runapi-minimax) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, TypeScript, dotenv, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and OPENAI_BASE_URL; prompts and responses are sent to RunAPI/MiniMax when used.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
