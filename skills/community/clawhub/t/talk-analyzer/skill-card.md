## Description:

Openclaw Talk Analyzer uses AI models to analyze business conversation transcripts and produce summaries, action items, decisions, sentiment, and sales or support insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sales teams, product managers, customer-success leaders, and executives use this skill to turn meeting, sales, support, negotiation, interview, or general conversation transcripts into structured analysis for follow-up and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable external installs can change after review.

Mitigation: Review or pin the exact Git commit or npm version, and avoid global installs when possible.

Risk: The cron example can enable unattended recurring analysis of sensitive conversations.

Mitigation: Use the cron job only intentionally, restrict input and output directories, and document how to remove the crontab entry.

Risk: Conversation transcripts may contain confidential, customer, employee, legal, medical, or regulated data.

Mitigation: Redact sensitive content before cloud analysis or use a local LLM for sensitive transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/talk-analyzer)
- [Project Documentation](https://github.com/ZhenRobotics/openclaw-talk-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON conversation-analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries, action items, decisions, sentiment, speaker analysis, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
