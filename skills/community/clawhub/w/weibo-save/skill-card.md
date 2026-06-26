## Description: <br>
微博内容保存工作流，帮助代理在收到 t.cn 或 weibo.com 链接后展开微博、抓取正文和图片、保存为 Obsidian Markdown，并可按配置同步到飞书、Notion 或生成发芽笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violin86318](https://clawhub.ai/user/violin86318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preserve Weibo posts from short links or canonical post URLs as organized Obsidian Markdown, including post text and images. When configured, it can also sync captured content to Feishu Bitable or Notion and generate follow-up notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a browser profile and cloud credentials to capture, store, or sync Weibo content and images. <br>
Mitigation: Use a dedicated browser profile, least-privilege Feishu and Notion credentials, and leave optional sync tokens blank unless those destinations are required. <br>
Risk: The workflow includes a workaround for image fetching when direct Sinaimg downloads are blocked by network safety controls. <br>
Mitigation: Avoid the image-fetch workaround for private or sensitive posts and review captured image URLs before saving or syncing them. <br>
Risk: Broad auto-trigger behavior could save or transmit content from links the user did not intend to archive. <br>
Mitigation: Confirm the target Weibo URL before execution and use explicit user approval for private posts or optional external sync steps. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter and image links, optional API sync actions, and a concise completion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Obsidian files and images; optional Feishu, Notion, Jina, and browser-profile use depends on user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
