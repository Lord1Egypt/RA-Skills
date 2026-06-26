## Description: <br>
将任意网页链接或本地文件转为结构化 Markdown，并可保存到 Obsidian Vault、飞书云文档或腾讯 IMA 笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to convert web pages or local files into structured Markdown and route the result to a local Obsidian vault or configured cloud note destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu and Tencent IMA credentials can grant access to create or modify cloud documents and notes. <br>
Mitigation: Use least-privilege, revocable API credentials stored in environment variables, and rotate them when no longer needed. <br>
Risk: Private URLs or local files may be uploaded to cloud note services when those destinations are enabled. <br>
Mitigation: Use local-only operation with documented flags such as --no-feishu and --no-ima for private material. <br>
Risk: Generated Markdown is written to user-selected local paths and may include converted content from untrusted pages. <br>
Mitigation: Set the Obsidian vault path to an intended inbox location and review converted content before relying on or sharing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edwardwason/web-to-fim) <br>
- [飞书云文档 API 配置指南](references/feishu-setup.md) <br>
- [腾讯 ima 笔记 API 配置指南](references/ima-setup.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Tencent IMA Agent Interface](https://ima.qq.com/agent-interface) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, cloud note or document records, and concise command or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save locally to a configured Obsidian vault or upload to Feishu and Tencent IMA when credentials are configured.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
