## Description:

Aggregates recent Donald Trump-related news from multiple sources, deduplicates and categorizes stories, and produces a concise Chinese-language briefing with source attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunsuy](https://clawhub.ai/user/tunsuy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to obtain timely Chinese-language summaries of Donald Trump-related actions, policies, statements, and political developments with attribution across multiple news sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses and summarizes fast-moving political news, so stale or single-source reporting could lead to incomplete or misleading briefings.

Mitigation: Use the skill's source-diversity and cross-referencing guidance, check publication timestamps, and flag claims that are not confirmed by multiple independent sources.

Risk: The skill defaults to Chinese-language output and a broad Trump news scope, which may not match every user's language or source expectations.

Mitigation: Explicitly request a different output language, time window, topic focus, or source set when needed.

## Reference(s):

- [Trump News Sources Reference](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/tunsuy/skills/trump-news-tracker)
- [Publisher profile](https://clawhub.ai/user/tunsuy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown briefing with cited source names, publication dates, highlights, categorized details, and short analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aims for 800-1500 Chinese characters, emphasizes recency, and flags unverified or contradictory reports.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
