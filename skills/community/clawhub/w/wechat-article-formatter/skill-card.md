## Description: <br>
Generates, normalizes, themes, and previews HTML-first WeChat Official Account articles so the body can be copied into the WeChat backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacktian89](https://clawhub.ai/user/zacktian89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, editors, and developers use this skill to turn topics, briefs, notes, outlines, Markdown, or existing HTML into WeChat-friendly article-body HTML. It can create a local preview page, apply reusable theme presets, inline local images, and prepare a copy-ready article#wechatArticle body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preview copy actions may request image URLs from the browser when imported HTML or Markdown contains external, localhost, private-network, or tracking image sources. <br>
Mitigation: Review untrusted inputs before previewing or copying, inline trusted local images as Base64 Data URLs, and verify copied images in the WeChat backend before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zacktian89/wechat-article-formatter) <br>
- [Theme Presets](references/theme-presets.md) <br>
- [Visual and Formatting Guidelines](references/visual-guidelines.md) <br>
- [Preview Page Contract](references/preview-implementation.md) <br>
- [Image Rules](references/image-rules.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Style Completeness Checklist](references/completeness-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML files or article#wechatArticle HTML with concise Markdown handoff notes and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default preview files are written under dist/; final article content should be self-contained and copy-ready for the WeChat backend.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
