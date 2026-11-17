## Description:

Generates photorealistic PNG images with Stability AI's Stable Image Ultra or Stable Diffusion 3.5 Large models through AWS Bedrock, with prompt, negative prompt, aspect-ratio, seed, region, and AWS authentication options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate high-quality photorealistic images from English prompts through AWS Bedrock when AWS access to Stability AI models in us-west-2 is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's AWS account for paid Bedrock image generation and encourages broad high-quality default use.

Mitigation: Install only when this paid image-generation behavior is intended, and configure AWS cost controls before use.

Risk: The skill supports passing AWS secrets directly on the command line.

Mitigation: Prefer AWS profiles, SSO, IAM roles, environment-managed credentials, or tightly scoped temporary credentials.

Risk: The skill attempts to make itself the default image-generation option for all agents.

Mitigation: Review agent routing and keep this skill enabled only where Stable Image Ultra or SD 3.5 Large generation is appropriate.

## Reference(s):

- [Stable Image Ultra skill page](https://clawhub.ai/wujiaming88/skills/stable-image-ultra)
- [wujiaming88 publisher profile](https://clawhub.ai/user/wujiaming88)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [PNG image files with concise text status and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one to five generated images per run, fixed PNG output, selectable model, aspect ratio, seed, AWS region, and AWS credential source.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
