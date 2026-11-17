## Description:

Save WeChat public account articles to a Notion database by fetching title, cover image, body content, keywords, review comments, and ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gevtolev](https://clawhub.ai/user/gevtolev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive WeChat official account articles into a Notion database, including article content, metadata, generated keywords, a short quality comment, and a star rating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send fetched article text, images, metadata, generated keywords, rating, and comments to a Notion workspace.

Mitigation: Use it only with links and workspaces the user explicitly wants to archive, and confirm before saving sensitive or private content.

Risk: The workflow exposes avoidable credential and temporary-file handling risks.

Mitigation: Check only that NOTION_API_KEY is present, avoid printing key prefixes, and use a unique private temporary file for fetched article JSON.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gevtolev/skills/wechat-to-notion)
- [Publisher profile](https://clawhub.ai/user/gevtolev)
- [OpenClaw](https://github.com/nicholasgriffintn/OpenClaw)
- [Notion integrations](https://notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Markdown instructions with shell commands and generated text values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTION_API_KEY, python3, curl, a WeChat article URL, and a Notion database URL.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
