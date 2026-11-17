## Description:

通用文生图技能，帮助 agents use MiniMax, OpenAI DALL-E, or Stability AI with user-provided API keys to generate images from text prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to configure an image-provider API key and request text-to-image generation in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed or misused if configured insecurely.

Mitigation: Keep provider API keys private, use environment variables or secret storage, and rotate keys if exposure is suspected.

Risk: Prompts are sent to the configured image provider and may incur usage charges.

Mitigation: Review provider data-handling terms before use and monitor provider usage or billing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/skills/xiaoxia-image-gen)
- [Publisher profile](https://clawhub.ai/user/xiaoliang1319-cloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MiniMax, OpenAI, or Stability AI API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
