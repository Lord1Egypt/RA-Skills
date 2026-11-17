## Description:

Provides Zhipu AI tools for image and video analysis, OCR, error screenshot diagnosis, UI-to-code conversion, technical diagram and data visualization analysis, UI comparison, web search, web page reading, GitHub repository lookup, CogView image generation, and CogVideoX video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangalexhy](https://clawhub.ai/user/zhangalexhy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Zhipu AI MCP services and related HTTP APIs for multimodal analysis, web and repository retrieval, and generated image or video outputs when Zhipu credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unpinned npm/MCP tooling while inheriting the parent process environment.

Mitigation: Review package resolution before installation, prefer pinned trusted package versions, and run with a minimal environment.

Risk: The skill reads a local Zhipu API key and passes it to MCP and HTTP calls.

Mitigation: Use a least-privilege Zhipu API key dedicated to this skill and rotate or revoke it if exposure is suspected.

Risk: Vision, OCR, video, search, and web-reading tools can transmit user-provided images, videos, URLs, code, or page content to remote services.

Mitigation: Avoid sending confidential screenshots, proprietary code, customer data, internal URLs, or other sensitive content unless the destination service is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangalexhy/skills/zhipu-coding-plan-mcp)
- [Zhipu AI Open Platform](https://open.bigmodel.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, text, code snippets, shell commands, configuration snippets, and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some operations call remote MCP or HTTP APIs and may return JSON-shaped responses, generated image URLs, or generated video URLs.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
