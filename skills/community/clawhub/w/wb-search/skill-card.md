## Description:

按关键词及筛选条件搜索微博公开内容，汇总互动数据，并导出 CSV。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户可按关键词、微博类型、排序和日期筛选公开微博，用于选题调研、竞品监测或达人初筛，并将结果导出为 CSV。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags collection behavior beyond the stated Weibo search purpose and a broad activation trigger.

Mitigation: Clarify the collection scope and activate the skill only for explicit Weibo search requests.

Risk: The security review flags insecure connection settings; the documentation says the default HTTP service can expose the account token in transit.

Mitigation: Use HTTPS with certificate verification enabled, and avoid sending account tokens over HTTP or with TLS verification disabled.

## Reference(s):

- [Weibo Search](https://s.weibo.com)
- [Skill release page](https://clawhub.ai/mystery77777777/skills/wb-search)

## Skill Output:

**Output Type(s):** [JSON, CSV, Markdown tables]

**Output Format:** [JSON task results, CSV exports, and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include post text, author, publication time, engagement counts, and links; CSV is formatted for spreadsheet use.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
