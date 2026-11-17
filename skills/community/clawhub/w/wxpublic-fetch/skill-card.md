## Description:

从微信公众号按名称和日期范围查询文章，抓取正文与图片并保存为本地 Markdown 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongweixp](https://clawhub.ai/user/xiongweixp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect WeChat public-account articles for a selected account and date range. It saves local Markdown files and images so the agent can later summarize or answer questions about the fetched articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials for wxpub.aibana.art may be exposed if pasted into chat or shell history.

Mitigation: Prefer environment variables or a secret store, use narrowly scoped or disposable credentials, and avoid sharing command transcripts that contain secrets.

Risk: The skill sends credentials, target account names, date ranges, and article URLs to external services.

Mitigation: Install and run it only when those services are trusted, and use the smallest practical date range for the task.

Risk: Untrusted account names or output paths can lead to unsafe command or file behavior.

Mitigation: Choose an output directory you control and sanitize externally supplied account names or paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiongweixp/skills/wxpublic-fetch)
- [wxpub service](https://wxpub.aibana.art/)
- [anything-md conversion service](https://anything-md.doocs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Progress text and summary output, with fetched articles saved as Markdown files and images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful fetch records include article date, URL, and local Markdown path for later agent use.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
