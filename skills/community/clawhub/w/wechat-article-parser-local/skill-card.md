## Description:

Parses WeChat public account articles to extract title, author, publication time, body content, image links, and optional Feishu table exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reknottycat](https://clawhub.ai/user/reknottycat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse WeChat article URLs, inspect extracted article metadata and text, and optionally save the results as local files or Feishu Bitable records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu save path can fetch arbitrary URLs.

Mitigation: Avoid private or internal URLs and review the URL before running the save command.

Risk: Saving to Feishu uploads article title, URL, summary, body content, source, and timestamp to an external table.

Mitigation: Use a dedicated Feishu table with least-privilege app credentials and treat saved article content as externally shared data.

Risk: The Feishu integration can create fields and delete blank rows in the configured table.

Mitigation: Consider removing or disabling automatic field creation and blank-row deletion before using the skill on important tables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reknottycat/skills/wechat-article-parser-local)
- [Publisher profile](https://clawhub.ai/user/reknottycat)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu Bitable record creation API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown guidance, JSON article records, and Feishu Bitable records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save parsed article data to local JSON/TXT files or upload title, URL, summary, body content, source, and timestamp to a configured Feishu table.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
