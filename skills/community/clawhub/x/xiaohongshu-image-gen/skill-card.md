## Description: <br>
Generates Xiaohongshu-style images from text prompts, with style and aspect-ratio presets for home decor, food, fashion, and travel content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, ecommerce sellers, and personal-brand operators use this skill to turn short Chinese prompts into Xiaohongshu-ready image assets with platform-oriented style and sizing defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it bundles an unrelated Tushare financial-data API helper that uses a separate account token. <br>
Mitigation: Review or remove the Tushare helper before installation unless the publisher can justify why it belongs in this image-generation skill. <br>
Risk: Prompts may be sent to OpenAI or Stability AI when the corresponding API keys are configured. <br>
Mitigation: Avoid sending sensitive or private prompts to cloud providers unless that use is approved for the deployment environment. <br>
Risk: The local fallback delegates generation to a separately installed image-generate skill. <br>
Mitigation: Use the local fallback only after reviewing and trusting the installed image-generate skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/xiaohongshu-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>
- [Stability AI SDXL text-to-image endpoint](https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image) <br>
- [Tushare service referenced by bundled helper](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG image files with command-line status text and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports portrait, square, and landscape aspect ratios; may use OpenAI, Stability AI, or a local image-generate fallback depending on configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
