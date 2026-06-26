## Description: <br>
Convert Markdown text to beautiful Xiaohongshu (XHS) style card images with 5 themes, deterministic browser screenshot rules, auto-pagination, smart title extraction, and AI-generated decorative backgrounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhang122994917](https://clawhub.ai/user/zhang122994917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation users use this skill to turn Markdown articles or plain text into XHS-ready multi-page PNG card images with controlled pagination, themes, and optional decorative AI backgrounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content or derived prompts may be processed by configured external AI or image providers. <br>
Mitigation: Disable AI backgrounds or cloud upload for private material and use scoped API keys. <br>
Risk: Unpinned Python dependency ranges can reduce deployment reproducibility. <br>
Mitigation: Pin dependency versions before production deployment. <br>
Risk: Generated card images can clip or overflow if browser rendering is not stabilized. <br>
Mitigation: Follow the bundled browser screenshot contract, including font readiness checks, stable card geometry, element-only screenshots, and output-size validation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhang122994917/xhs-md2pic) <br>
- [Publisher profile](https://clawhub.ai/user/zhang122994917) <br>
- [API Reference](references/api-reference.md) <br>
- [Browser Screenshot Spec](references/browser-screenshot-spec.md) <br>
- [Theme Color Palettes](references/themes.md) <br>
- [Input Schema](templates/input-schema.json) <br>
- [DashScope image synthesis API](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis) <br>
- [Gemini generateContent API](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [JSON describing generated XHS card images, including page metadata and either image URLs or data URIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ordered PNG card pages with title, theme, total page count, dimensions, byte size, and upload status when available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
