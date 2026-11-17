## Description:

Aggregates Chinese-language trending topics from public web sources, classifies them by topic, scores their popularity, detects new items, and summarizes trends for manual or scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[19x19btr](https://clawhub.ai/user/19x19btr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to collect Chinese-language trending news, organize it into categories such as technology, finance, society, international, and entertainment, and receive concise trend summaries through manual runs or configured schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled or pushed news summaries may go to an unintended channel if delivery settings are enabled without review.

Mitigation: Confirm destination channels, credentials, schedule, and disable controls before enabling push delivery.

Risk: Trending-news output can be time-sensitive or misleading if source links expire or automated categorization is inaccurate.

Mitigation: Review generated summaries and source links before relying on them for decisions or redistribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/19x19btr/skills/trending-news-aggregator)
- [Publisher Profile](https://clawhub.ai/user/19x19btr)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style news summaries with categorized items, links, popularity scores, new-item markers, trend analysis, and optional scheduling or push configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; relies on public web search and optional user-configured push delivery channels.]

## Skill Version(s):

1.0.0 (source: server evidence, package.json, CHANGELOG, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
