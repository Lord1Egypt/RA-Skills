## Description:

Unified News aggregates Web3/Crypto, AI and technology, macroeconomic, finance, and market news, deduplicates items, formats bilingual summaries, and can send scheduled Feishu updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch, summarize, deduplicate, and deliver topical news briefings across Web3/Crypto, AI and technology, macroeconomics, finance, and market news. It supports on-demand briefings and scheduled Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled Feishu delivery can run indefinitely and send recurring external messages without per-send confirmation.

Mitigation: Enable the cron task only when recurring delivery is intended, verify the bot account and recipient, and add an expiry, removal procedure, or on-demand-only operating mode.

Risk: The skill calls external news sources and writes deduplication state to memory/news-sent.md.

Mitigation: Review external request expectations before use and monitor the deduplication record for retention and correctness.

## Reference(s):

- [Unified News on ClawHub](https://clawhub.ai/gaoren36-arch/skills/unified-news)
- [6551 API category endpoint](https://ai.6551.io/open/free_categories)
- [6551 API crypto news endpoint](https://ai.6551.io/open/free_hot?category=crypto)
- [6551 API AI news endpoint](https://ai.6551.io/open/free_hot?category=ai)
- [6551 API macro news endpoint](https://ai.6551.io/open/free_hot?category=macro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown news briefing with optional shell commands and JSON message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bilingual summaries, relevance tags, heat scores, related tokens or stocks when available, and a sent-item count.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
