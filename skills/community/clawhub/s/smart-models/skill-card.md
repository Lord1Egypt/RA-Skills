## Description:

Intelligent multi-model router that automatically selects an AI model for vision, image generation, video generation, audio, reasoning, code, or general chat tasks through an OpenAI-compatible API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samstone908](https://clawhub.ai/user/samstone908)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to route prompts, images, generation requests, reasoning tasks, and code tasks to configured remote models. It supports automatic task classification, direct @alias model selection, and fallback within model categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send broad prompts and image URLs to a configured remote model provider.

Mitigation: Use trusted HTTPS providers, avoid routing sensitive or regulated content automatically, and confirm user consent before sending private prompts or attachments.

Risk: Provider credentials are required for remote API calls.

Mitigation: Configure a limited API key with spending controls and rotate or revoke it if the environment is shared or compromised.

## Reference(s):

- [Smart Router ClawHub release](https://clawhub.ai/samstone908/skills/smart-models)
- [samstone908 ClawHub profile](https://clawhub.ai/user/samstone908)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional URLs, generated file paths, and shell command output from configured model calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote model results depend on the configured OpenAI-compatible provider, selected model, request type, and API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
