## Description: <br>
RSS聚合摘要免费版 helps an agent fetch RSS/Atom feeds, filter entries by keywords and time range, deduplicate results, and produce Markdown or plain-text digests for personal information workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, developers, and knowledge workers use this skill to generate daily or topic-specific RSS/Atom digests from a small set of trusted feeds. It is suited for lightweight news monitoring, competitor updates, and research feed aggregation without a database or complex configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches network content from user-provided RSS or Atom URLs, which may expose feed choices or retrieve untrusted content. <br>
Mitigation: Use trusted feed URLs and review digest output before relying on it or sharing it. <br>
Risk: Embedding credentials in private feed URLs could expose secrets in shell history, files, or logs. <br>
Mitigation: Avoid credentials in URLs and prefer secure credential handling outside this free version. <br>
Risk: Writing output to a chosen path may overwrite an existing file. <br>
Mitigation: Choose output paths carefully and inspect commands before execution. <br>
Risk: Recurring execution through crontab can repeatedly fetch feeds or write files without interactive review. <br>
Mitigation: Review any crontab entry before enabling scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-feed-digest-tool-free) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text digest with optional shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write digest files to user-selected paths; requires network access to configured RSS or Atom feed URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
