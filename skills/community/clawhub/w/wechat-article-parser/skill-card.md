## Description:

Parses WeChat public-account article URLs to extract article metadata, body text, image links, and optional Feishu table records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse public WeChat article links into readable article text, metadata, image references, and optional saved records in Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu save path can automatically alter table schema.

Mitigation: Use a dedicated test or disposable Feishu table until automatic field creation is reviewed or gated by explicit confirmation.

Risk: The Feishu save path can read all records and batch-delete blank rows.

Mitigation: Do not connect shared or important Feishu tables unless broad read/write access and blank-row deletion are acceptable.

Risk: Article parsing depends on remote public URLs and may return incomplete content.

Mitigation: Use the parser only with public article URLs you trust and review extracted content before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harven-droid/skills/wechat-article-parser)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu Bitable create record API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance with shell commands; parser output can be printed text or saved JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Feishu saving requires FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_APP_TOKEN, and FEISHU_TABLE_ID.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
