## Description:

Summarize Telegram channel messages by topic with structured output. Used by executor sub-agents spawned by telegram-parser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeykolbasuk](https://clawhub.ai/user/sergeykolbasuk)

### License/Terms of Use:

MIT-0

## Use Case:

Executor sub-agents use this skill to read Telegram message batches and produce concise, topic-grouped summaries in Russian. It is intended for summarizing channel updates, technical news, announcements, and job postings from batches supplied by a separate orchestrator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram message content and account access can include sensitive or unintended channel data.

Mitigation: Use only intended message batches and limit any Telethon session or account access to appropriate channels before installing or running the skill.

Risk: Concise topic grouping can omit nuance from source posts or merge distinct updates.

Mitigation: Review source messages before using summaries for operational or business decisions, especially when the summary covers jobs, compensation, or rapidly changing news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergeykolbasuk/skills/telegram-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown summary in Russian]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes channel, date or period, message count, topic sections, and optional job-posting bullets; links are omitted unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
