## Description:

解析用户输入中的 docs.qq.com 链接，逐个下载腾讯文档到桌面目录，并更新 Excel 归档台账。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pufanuzhu-hash](https://clawhub.ai/user/pufanuzhu-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Users who receive Tencent Docs links use this skill to extract docs.qq.com URLs from free-form text, download each document, save local archive copies, and maintain an Excel ledger of archived links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and stores local copies of Tencent Docs, which can expose private document contents if provided links are sensitive or unauthorized.

Mitigation: Review the extracted docs.qq.com link list before download and only archive documents the user is authorized to access.

Risk: The Excel ledger records links from user-provided input, and untrusted entries may be unsafe to open or follow later.

Mitigation: Avoid opening ledger entries from untrusted inputs and keep the ledger in a controlled local folder.

Risk: The ledger helper depends on openpyxl in the local Python environment.

Mitigation: Install openpyxl only from a trusted Python package source or managed environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown-style archive report with local file paths and ledger update status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local document copies and an Excel ledger under Desktop/腾讯文档 when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
