## Description:

Aggregates news from configured RSS feeds and public URLs, filters items by keywords, generates a daily Markdown digest, and can push the digest to Feishu.

This skill is for research and development only.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users can configure trusted public news sources and keyword categories to collect, deduplicate, summarize, and optionally share a daily Feishu news brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configurable network fetching can contact unintended or private URLs.

Mitigation: Use only trusted public HTTPS news feeds, avoid internal or private URLs, and run with restricted outbound network access where possible.

Risk: Feishu sharing can disclose generated digest content to the wrong chat or with an exposed token.

Mitigation: Review the configured Feishu chat destination, keep FEISHU_BOT_TOKEN in the environment, and rotate or scope the token according to local policy.

Risk: Generated news data, digests, and push history remain on local disk.

Mitigation: Review retention requirements and delete or protect local data files when the digest contents are sensitive.

Risk: Dependency findings may require review before installation.

Mitigation: Update the flagged dependencies before use and reinstall from a trusted package source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/quannwang-news-aggregator)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Markdown, JSON files, Shell commands, Configuration guidance]

**Output Format:** [Markdown daily digest, JSON news/history files, console logs, and optional Feishu text message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest text sent to Feishu is truncated to 4000 characters; generated news data, digests, and 30 days of push history may remain on disk.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
