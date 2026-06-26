## Description: <br>
Multi-model AI image generation on a visual canvas with support for Midjourney, Grok Imagine, nano-banana-2, Seedream 5.0, reference images, style transfer, batch generation, and aspect ratio control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative developers use this skill to generate, organize, and reuse AI images on a VPick visual canvas across supported cloud image models. It is suited for artwork, illustration, character design, style transfer, reference-driven composition, and batch image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP URL contains an embedded account token that can trigger VPick generation actions and spend account credits. <br>
Mitigation: Treat the MCP URL as a credential, keep it out of public logs or shared prompts, and regenerate it from VPick settings if exposed. <br>
Risk: Prompts and reference images are processed by VPick and routed to third-party image model providers. <br>
Mitigation: Avoid submitting sensitive prompts or images unless VPick and the downstream model providers are approved for that data. <br>
Risk: Generated images and uploaded references are stored under the user's VPick account and generations consume VPick credits. <br>
Mitigation: Review generated file history and generation statistics, monitor credit usage, and delete or avoid uploading content that should not be retained in the VPick project. <br>


## Reference(s): <br>
- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html) <br>
- [VPick app](https://vpick.10xboost.org) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/vpick-ai-image-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown with tool-call examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces VPick canvas workflow guidance and MCP tool-call examples for image generation, reference uploads, canvas organization, result browsing, and usage checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
