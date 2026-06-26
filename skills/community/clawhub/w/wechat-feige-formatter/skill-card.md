## Description: <br>
Formats draft, plain-text, or Markdown articles into WeChat public-account HTML by adding supported formatting marks and running a Python converter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tracevan](https://clawhub.ai/user/tracevan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to prepare WeChat public-account articles from rough drafts, plain text, Markdown, or uploaded files. It helps identify article structure, add formatter-specific Markdown marks, and produce HTML suitable for review and copying into a WeChat editor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner verdict is suspicious because file and image handling is broader and less clearly controlled than users may expect. <br>
Mitigation: Review the skill before installing and limit use to WeChat/public-account article formatting. <br>
Risk: Generated HTML may contain embedded local file contents if image embedding is used with local image paths. <br>
Mitigation: Use trusted Markdown and image paths only, and inspect generated HTML before copying, publishing, or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tracevan/wechat-feige-formatter) <br>
- [排版优化规则](references/排版优化规则.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Optimized Markdown, generated HTML files, shell commands, and brief usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may include inline styling, a preview/copy interface, theme color options, and embedded local images when image embedding is used.] <br>

## Skill Version(s): <br>
2.3.5 (source: server release evidence and clawhub.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
