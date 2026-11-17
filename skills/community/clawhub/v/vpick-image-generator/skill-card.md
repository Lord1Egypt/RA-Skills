## Description:

VPick AI Image Generator helps agents create and iterate AI images on a visual canvas using VPick-supported models such as Midjourney, Grok Imagine, nano-banana-2, and Seedream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate, refine, and reuse AI images through a VPick canvas workflow with text prompts, reference images, style transfer, and batch generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP URL contains an embedded authentication token.

Mitigation: Treat the MCP URL as a secret and avoid sharing it in prompts, logs, screenshots, or public configuration.

Risk: Prompts and uploaded reference images are processed by VPick and downstream model providers.

Mitigation: Avoid sensitive prompts or private reference images unless that external processing is acceptable for the use case.

Risk: Generated images consume the user's VPick credit balance.

Mitigation: Monitor VPick credit usage and generation history, especially for batch generation or higher-cost model settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/vpick-image-generator)
- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html)
- [VPick app](https://vpick.10xboost.org)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image, image-to-image, multi-reference composition, style transfer, aspect ratio selection, batch generation, and generated-image reuse in downstream canvas workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
