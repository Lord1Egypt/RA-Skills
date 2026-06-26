## Description: <br>
Free AI text-to-image generation that turns text descriptions into images using Pollinations.ai models without requiring an API key. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn user image prompts into generated image files through Pollinations.ai, with controls for dimensions, model selection, watermark removal, and seed-based reproducibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Pollinations.ai and could expose secrets, personal information, regulated data, or confidential project details. <br>
Mitigation: Do not include sensitive or confidential information in prompts; review prompt content before execution. <br>
Risk: Generated images depend on an external free API that may queue, delay, fail, or change behavior. <br>
Mitigation: Set expectations for generation latency, retry failed requests deliberately, and review generated images before use. <br>
Risk: The artifact notes a non-commercial limitation for the Pollinations.ai free tier. <br>
Mitigation: Confirm Pollinations.ai terms before commercial deployment or use a service tier with suitable rights. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bustes01/text-to-image-free) <br>
- [Skill homepage metadata](https://clawhub.ai/BusTes01/text-to-image-free) <br>
- [Pollinations.ai image endpoint](https://image.pollinations.ai/prompt/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Generated image file with Markdown and bash command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt text, width, height, model, nologo, and optional seed parameters.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
