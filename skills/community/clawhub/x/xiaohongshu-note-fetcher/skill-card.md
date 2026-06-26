## Description: <br>
抓取并整理小红书笔记公开页面信息（标题、正文摘要、作者、发布时间、互动数据、标签、封面图等）为结构化 JSON 或 Markdown。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2813223285](https://clawhub.ai/user/2813223285) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content operators, and developers use this skill to fetch Xiaohongshu notes from URLs or keyword searches, then turn note metadata and engagement signals into structured JSON, Markdown, CSV, or topic-planning materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require Xiaohongshu cookies or API tokens for authenticated fetching. <br>
Mitigation: Use short-lived, low-privilege credentials, avoid full personal browser cookies when possible, and remove secrets from command history and output files. <br>
Risk: The generic API mode can send requests and credentials to user-provided endpoints. <br>
Mitigation: Use only trusted API base URLs and avoid generic API mode with untrusted or unfamiliar services. <br>
Risk: Fetched outputs may contain account-accessible or third-party content. <br>
Mitigation: Keep generated JSON, Markdown, CSV, screenshots, and HTML private unless sharing is authorized and compliant with applicable platform terms and privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2813223285/xiaohongshu-note-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/2813223285) <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, CSV, text files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include fetched note fields, article lists, publish templates, screenshots, rendered HTML, and mind-map URLs depending on the selected script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
