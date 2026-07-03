## Description: <br>
将微信公众号文章自动转为个人知识库笔记，输入公众号文章链接后抓取正文、生成 AI 多维度总结，并输出结构化 Markdown 笔记保存到本地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal knowledge workers use this skill to convert WeChat public-account article links into structured Markdown notes for a local Obsidian vault, including article metadata, summaries, tags, quotes, and related-note prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted article URL could trigger unintended shell command execution during article fetching. <br>
Mitigation: Process only trusted WeChat article links until command handling is fixed, and prefer preview or explicit output paths before saving. <br>
Risk: The skill can write generated notes into a local Obsidian vault. <br>
Mitigation: Set an explicit vault or output path, confirm the resolved destination, and review generated notes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afeicn/wechat-article-to-txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, JSON article data, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated Markdown notes to a configured local Obsidian vault or to an explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
