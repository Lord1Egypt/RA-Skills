## Description:

Tech Morning Briefing collects, scores, categorizes, and summarizes daily technology news, then sends an 8-10 item morning brief to Feishu and appends it to an archive document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uuoov](https://clawhub.ai/user/uuoov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and tech teams use this skill to automate a daily technology news briefing across AI, products, industry, hardware, and policy. It is intended for scheduled Feishu delivery and ongoing archive updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to run as a daily scheduled job that sends generated summaries to Feishu and appends them to a Feishu archive document.

Mitigation: Confirm the schedule, timezone, recipients, and archive destination before enabling the cron job.

Risk: The workflow depends on Tavily and Feishu credentials.

Mitigation: Protect the Tavily API key and use a Feishu app with only the permissions needed for chat push and document creation or append.

Risk: Generated news summaries and scores may omit context or overstate the importance of a story.

Mitigation: Review source links and scoring before relying on the brief for decisions or broad redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uuoov/skills/tech-morning-briefing)
- [OpenClaw](https://openclaw.ai)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown briefing with grouped news items, Feishu message content, Feishu document append entries, and JSON state updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects 8-10 high-value items from 50+ recent search results and maintains bounded local state for deduplication, carryover, and quote rotation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
