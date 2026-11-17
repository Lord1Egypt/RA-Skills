## Description:

Convert Markdown text to beautiful Xiaohongshu (XHS) style card images with 5 themes, deterministic browser screenshot rules, auto-pagination, smart title extraction, and AI-generated decorative backgrounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang122994917](https://clawhub.ai/user/zhang122994917)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert Markdown articles or plain text into Xiaohongshu-style multi-page PNG card images with controlled themes, pagination, and screenshot sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User Markdown may be rendered as active browser HTML without documented sanitization or network blocking.

Mitigation: Use sanitized HTML, block scripts and unexpected network requests, and render shared or untrusted content in an isolated browser context.

Risk: The skill can use external LLM or image-generation services and optional OSS upload.

Mitigation: Confirm provider use is acceptable, scope API and OSS credentials narrowly, and disable AI backgrounds or upload paths when they are not needed.

Risk: Dependencies are listed as open version ranges.

Mitigation: Pin and scan dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhang122994917/skills/xhs-md2pic)
- [Input schema](templates/input-schema.json)
- [Browser screenshot spec](references/browser-screenshot-spec.md)
- [Theme color palettes](references/themes.md)
- [Image generation API reference](references/api-reference.md)
- [DashScope Wanx image synthesis API](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis)
- [Gemini generateContent API](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent)

## Skill Output:

**Output Type(s):** [Images, JSON metadata, Files]

**Output Format:** [PNG card images with JSON page metadata, URLs, or data URIs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is one or more 1125x1500 PNG cards at export_scale=3; optional OSS upload can return page URLs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
