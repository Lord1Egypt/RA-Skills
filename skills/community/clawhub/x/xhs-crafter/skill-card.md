## Description:

Converts Markdown articles into 3:4 image cards and a compressed text draft for WeChat Official Account and Xiaohongshu image-post publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and publishing teams use this skill to transform Markdown drafts into locally rendered PNG card sets plus a short companion text draft for social publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local rendering workflow uses browser automation with Chromium sandboxing disabled.

Mitigation: Use the skill in a constrained workspace and run it only on trusted Markdown and image inputs.

Risk: The image-download workflow is less restricted than claimed by the skill documentation.

Mitigation: Review downloaded image sources and generated files before use, and prefer user-provided local images for sensitive drafts.

Risk: Optional image search, AI image generation, and Feishu upload can send search terms, prompts, or generated files to external services.

Mitigation: Keep optional external capabilities disabled for sensitive or proprietary content unless the user explicitly accepts that data transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/xhs-crafter)
- [README](README.md)
- [Style system](references/style-system.md)
- [Category cookbook](references/category-cookbook.md)
- [Content planning](references/content-planning.md)
- [Image sources](references/image-sources.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, shell commands, and local file-output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PNG image cards and a compressed text draft; optional image search, AI image generation, and Feishu upload require explicit user consent.]

## Skill Version(s):

7.8.0 (source: frontmatter, server release metadata, changelog released 2026-07-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
