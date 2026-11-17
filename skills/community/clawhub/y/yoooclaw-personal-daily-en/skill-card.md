## Description:

Generates a concise daily news report in English based on user-specified topics, highlighting key events and trends with authoritative sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn configured interest topics into a daily briefing that identifies important same-day news, notable developments, and trend signals. It is suited for recurring personal or professional morning news review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured interest topics may be sent as web-search keywords.

Mitigation: Confirm topics are appropriate for web search and remove sensitive subjects before installing, scheduling, or running the skill.

Risk: Broad current-news prompts may invoke this daily-news workflow.

Mitigation: Use explicit invocation language or review configured triggers when broad prompts such as 'what's new today' should not run the briefing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-personal-daily-en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown daily news briefing with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session text only; no file is generated. The report is capped at 1,500 words, with each news summary limited to 2-3 sentences.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
