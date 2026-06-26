## Description: <br>
将用户提供的网页链接或本地文件转换为结构化 Markdown，并保存为飞书云文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and developers use this skill to archive user-provided web pages, social posts, media pages, and local files into Feishu cloud documents. It helps classify content, choose a target knowledge base or folder, and create a structured document after user confirmation when classification is unclear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied links or files and stores the resulting content in Feishu, which can persist sensitive or private material. <br>
Mitigation: Use it only with URLs and files intended for Feishu storage, and verify the destination space or folder before creating documents. <br>
Risk: The skill requires Feishu application credentials for cloud document creation. <br>
Mitigation: Configure credentials through environment variables, use a least-privilege Feishu app, and avoid hardcoding secrets in skill files or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/web-to-feishu-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content and concise conversational guidance, with commands or configuration snippets when setup is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent Feishu documents using Feishu credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
