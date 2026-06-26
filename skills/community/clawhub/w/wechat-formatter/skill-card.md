## Description: <br>
将 Markdown 文章转换为微信公众号编辑器粘贴格式，保留段落层次和基础格式（加粗、列表、代码块）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and developers use this skill to convert Markdown drafts into plain text formatted for pasting into the WeChat public account editor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown passed from private memory or workspace files may be printed to stdout or copied onward by shell pipelines. <br>
Mitigation: Review input content before formatting or piping output to clipboard tools, especially before publishing. <br>
Risk: The formatter only handles a subset of Markdown and may change presentation details. <br>
Mitigation: Preview the converted text in the WeChat editor and manually adjust formatting before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/wechat-formatter) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code] <br>
**Output Format:** [Plain text emitted to stdout, with optional Python function integration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converts headings, bold, italics, unordered lists, and fenced code blocks; it does not preserve full Markdown styling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
