## Description: <br>
Convert local .docx or Markdown files into WeChat-ready HTML and generate a publish folder with source files, assets, cover images, WeChat HTML, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockbotclub](https://clawhub.ai/user/rockbotclub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to package local .docx, Markdown, or HTML articles into WeChat public account publishing folders with localized assets and copy-paste-ready HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted documents or HTML image references can trigger outbound URL fetches or copy local files into the generated publish folder. <br>
Mitigation: Run the skill only on trusted documents and cover URLs, and inspect the generated assets and cover directories before sharing or publishing. <br>
Risk: .docx conversion depends on a local pandoc executable and may fail when pandoc is unavailable. <br>
Mitigation: Confirm pandoc is installed before using .docx inputs, or use Markdown or HTML inputs when pandoc is not available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rockbotclub/wechat-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Files, HTML, JSON metadata, Shell commands, Guidance] <br>
**Output Format:** [Publish folder containing source, assets, cover, wechat/article.html, and meta.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pandoc for .docx conversion; can download external images and optionally generate cover variants when Pillow is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
