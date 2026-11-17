## Description:

Guides agents through locking a product’s shape, surface, and motion in AI video prompts, checking generated clips for drift, and restoring exact packshot text in post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product marketers use this skill to prepare reference images and prompts for AI product videos, then check clips for product drift and preserve exact packaging text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product clips and descriptions sent to Varg for analysis may contain confidential material.

Mitigation: Review the clips and descriptions before submission, and exclude sensitive material unless it is approved for Varg processing.

Risk: The installer is unpinned, so installed content may change between releases.

Mitigation: Review the installation source and pin a version or commit you have assessed when your installation workflow supports it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vargai/skills/varg-product-lock)
- [Varg setup guide](https://varg.ai/how-to)
- [Varg MCP server](https://mcp.varg.ai/mcp)
- [Seedance product consistency guide](https://www.seedance.tv/blog/how-to-keep-product-shape-consistent-in-ai-video-ads)
- [AI product video reference examples](https://github.com/AuraJZ/ai-product-video)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown lock sheets and video prompts with inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use product images, generated clips, and VARG_API_KEY or Varg MCP access; clip analysis may incur usage charges.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
