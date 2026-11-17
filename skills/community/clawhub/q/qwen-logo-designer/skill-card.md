## Description:

Qwen Logo Designer helps an agent collect business logo requirements, write image-generation prompts, call Alibaba Cloud DashScope Qwen Image, and save generated logo images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imnull](https://clawhub.ai/user/imnull)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, developers, and agents use this skill to turn brand, industry, style, color, and logo-type requirements into commercial logo image prompts and generated logo files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing the DashScope API key with the --api-key argument can expose it through local process listings or shell history.

Mitigation: Use a protected environment or secret mechanism for DASHSCOPE_API_KEY, keep the key tightly scoped, and apply quota limits.

Risk: The helper may make the output directory traversable and generated files readable by other local users.

Mitigation: Save generated logos only into a dedicated non-sensitive output directory and review file permissions after execution.

Risk: Logo prompts and generation requests are sent to the documented DashScope API.

Mitigation: Avoid including confidential brand strategy or unreleased product details in prompts unless the deployment policy permits that API use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imnull/skills/qwen-logo-designer)
- [DashScope multimodal generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated image file paths or JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally, normally as MD5-named PNG files.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
