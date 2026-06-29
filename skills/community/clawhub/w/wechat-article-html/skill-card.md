## Description: <br>
将 Markdown 文章转换为微信公众号兼容的纯 HTML 格式。当用户要求"转成微信格式"、"生成公众号文章 HTML"、"排版到微信草稿箱"、"微信粘贴格式"时触发。输出带内联样式的纯 HTML，微信编辑器可直接渲染，无需额外适配。支持标题、段落、列表、粗体、行内代码、表格、引用块、代码块、配图的完整转换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryaction](https://clawhub.ai/user/jerryaction) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content operators use this skill to convert Markdown articles into inline-styled HTML that can be pasted into the WeChat Official Account editor. It is intended for article formatting workflows that need headings, paragraphs, lists, tables, blockquotes, code blocks, and images converted without leaving Markdown syntax behind. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read the wrong Markdown file or overwrite an existing *_for_paste.html output file. <br>
Mitigation: Confirm the source Markdown path and intended output path before running the conversion, especially when a matching output file already exists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryaction/wechat-article-html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance and generated inline-styled HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces UTF-8 HTML for WeChat paste workflows and may write a *_for_paste.html output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
