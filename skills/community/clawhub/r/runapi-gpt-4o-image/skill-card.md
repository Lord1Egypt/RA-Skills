## Description: <br>
Generate and edit images with GPT-4o Image through RunAPI, using the RunAPI CLI for one-off tasks and RunAPI SDKs for application integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to route GPT-4o image generation and editing requests through RunAPI. It helps agents choose the CLI for one-off tasks and SDK packages for application or backend integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, inputs, and generated content may be sent to RunAPI when the CLI or SDK is used. <br>
Mitigation: Review RunAPI pricing, privacy terms, and account settings before authenticating or submitting sensitive material. <br>
Risk: The skill can rely on a saved RunAPI login or optional RUNAPI_API_KEY. <br>
Mitigation: Use trusted environments, avoid exposing API keys in logs or prompts, and rotate credentials if they may have been disclosed. <br>
Risk: The workflow depends on the RunAPI command-line tool. <br>
Mitigation: Install the CLI only from the declared runapi-ai/tap/runapi Homebrew source and review commands before execution. <br>


## Reference(s): <br>
- [RunAPI GPT-4o Image model overview](https://runapi.ai/models/gpt-4o-image) <br>
- [RunAPI GPT-4o Image documentation](https://runapi.ai/models/gpt-4o-image.md) <br>
- [RunAPI OpenAI provider comparison](https://runapi.ai/providers/openai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill listing](https://clawhub.ai/runapi-ai/runapi-gpt-4o-image) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with CLI command examples and integration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference request JSON files, RunAPI task IDs, and optional RunAPI authentication.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
