## Description:

将论文和摘要保存到 Zotero 文库。需配置 ZOTERO_CREDENTIALS 环境变量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gottenzzp](https://clawhub.ai/user/gottenzzp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save paper metadata, authors, URLs, abstracts, AI-generated summaries, and tags into a Zotero library from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zotero credentials can grant write access to the user's library.

Mitigation: Use a Zotero API key scoped to the minimum permissions needed and rotate it if it is exposed.

Risk: The automatic PDF attachment path can fetch unintended URLs before uploading the file to Zotero.

Mitigation: Use trusted paper URLs only, and require strict arXiv hostname validation, size and type checks, and explicit opt-in before enabling PDF uploads.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [ClawHub skill page](https://clawhub.ai/gottenzzp/skills/zotero-sholar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Command-line output and Zotero API writes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS formatted as userID:apiKey.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
