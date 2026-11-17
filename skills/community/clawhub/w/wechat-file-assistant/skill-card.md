## Description:

在本地 Windows 电脑上查找、索引、检查并继续处理微信文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and their agents use this skill to find WeChat or Weixin files by name or content, maintain a local searchable index for repeated queries, detect exact duplicate files, and continue with requested summarization, extraction, comparison, or organization tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local index can store sensitive WeChat file paths, hashes, extracted text, timestamps, and optional metadata under LOCALAPPDATA.

Mitigation: Use narrow explicit roots for sensitive accounts and remove the local index when it is no longer needed.

Risk: Indexing untrusted Office or PDF files may expose sensitive content during local extraction or produce incomplete extraction results.

Mitigation: Avoid indexing untrusted Office files when possible and report extraction statuses such as unsupported_type or no_text_or_scanned_pdf instead of treating extraction failure as a negative content match.

Risk: Sender, chat, or sent-time metadata can be misleading if inferred from file paths, directory names, hashes, or file modification timestamps.

Mitigation: Use sender, chat, and sent_at only from a trusted metadata index with a verified path match; otherwise state that those fields are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocxf/skills/wechat-file-assistant)
- [Local index workflow](references/index-workflow.md)
- [Trusted metadata index](references/metadata-index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline PowerShell commands, local file paths, and optional structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, file metadata, duplicate groups, extraction status, and follow-up task guidance.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
