## Description: <br>
微信公众号文章保存工作流：当用户发送微信公众号文章链接时，抓取正文并保存为 Markdown 到知识库，可选推送链接到飞书多维表格，也可选生成独立发芽笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violin86318](https://clawhub.ai/user/violin86318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who archive WeChat public account articles use this skill to fetch an article from an mp.weixin.qq.com link, save it as Markdown in an Obsidian vault, optionally write metadata to Feishu, and optionally generate a separate note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can access the configured Obsidian folder and Feishu table. <br>
Mitigation: Install only when those locations are intended for this workflow, and use least-privilege Feishu credentials. <br>
Risk: The workflow relies on external command-line tooling and a configured baoyu script path. <br>
Mitigation: Verify the configured script path and source before use, and review command behavior in the target environment. <br>
Risk: The workflow includes optional authority to delete Feishu table records. <br>
Mitigation: Review the matched record title and identifier carefully, and proceed only after explicit user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violin86318/wechat-article-save) <br>
- [WeChat public article URL pattern](https://mp.weixin.qq.com/) <br>
- [Jina Reader fallback endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, Feishu record fields, and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu records when configured and may delete Feishu records only through the documented confirmation flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
