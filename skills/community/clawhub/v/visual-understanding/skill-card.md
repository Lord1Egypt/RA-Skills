## Description:

Integrates the Zhipu GLM-4.6V multimodal vision model for image understanding through the zai Python SDK or cURL, supporting local Base64 images and public image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isabellazhangym](https://clawhub.ai/user/isabellazhangym)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to connect agent workflows to GLM-4.6V for image description, multi-image comparison, and visual information extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, and Base64-encoded local images may be sent to Zhipu's external API.

Mitigation: Use only approved images, remove sensitive or personal data before upload, and avoid confidential content unless the external API use is authorized.

Risk: The skill depends on the external zai Python package.

Mitigation: Install a pinned, reviewed zai version in a virtual environment or container.

Risk: The ZHIPUAI_API_KEY credential is required for API access.

Mitigation: Keep the API key in an environment variable and do not hard-code or commit it.

## Reference(s):

- [GLM-V homepage](https://github.com/zai-org/GLM-V)
- [GLM-V repository](https://github.com/zai-org/GLM-V.git)
- [Zhipu chat completions API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPUAI_API_KEY and may send selected prompts, public image URLs, or Base64-encoded images to Zhipu's external API.]

## Skill Version(s):

0.0.5 (source: ClawHub release metadata; artifact frontmatter declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
