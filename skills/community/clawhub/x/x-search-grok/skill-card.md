## Description:

Search X (Twitter) for account posts, trending topics, or topic discussions using Grok API. Outputs Obsidian-ready Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyue55](https://clawhub.ai/user/wangyue55)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search X accounts, trends, and topics through the xAI Grok API, then receive concise Markdown suitable for review or Obsidian notes. It also supports watchlist and scheduled monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X search prompts and the xAI API key are sent to xAI during execution.

Mitigation: Install only when this data sharing is acceptable, keep the key in environment variables, and use a virtual environment with reviewed dependencies.

Risk: Saved Markdown output can overwrite an existing same-day file at the chosen output path.

Mitigation: Choose output paths deliberately and use unique filenames when preserving earlier runs matters.

Risk: Scheduled runs can forward results to Telegram, Slack, or Discord channels.

Mitigation: Review cron announcements, destination channels, and recipient identifiers before enabling scheduled delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyue55/skills/x-search-grok)
- [Source repository from skill metadata](https://github.com/wangyue55/x-search-skill)
- [xAI Responses API endpoint used by the skill](https://api.x.ai/v1/responses)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with optional saved Markdown files and brief progress text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Obsidian-ready output can include summaries, translations, and keyword explanations; same-day output files may be overwritten when the same resolved path is reused.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
