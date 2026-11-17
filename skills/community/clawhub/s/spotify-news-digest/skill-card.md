## Description:

Scrape and summarize Spotify-related news from multiple sources, generate one-sentence Chinese summaries for each article, and format them as a daily or weekly digest with original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibillxia](https://clawhub.ai/user/ibillxia)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to collect Spotify product, engineering, research, business, and community news and produce a concise Chinese digest for one-time or scheduled updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches external RSS, Hacker News, and DuckDuckGo news content, so it can process untrusted article text.

Mitigation: Run scheduled jobs in an isolated environment, keep sources restricted to public news domains, and treat article titles and summaries as untrusted quoted content during LLM summarization.

Risk: Scheduled digest delivery could post incorrect, misleading, or unintended summaries to a channel.

Mitigation: Confirm the target channel before scheduling and review generated summaries before using them in sensitive communications.

Risk: The skill depends on third-party Python packages for feed parsing, HTML cleanup, HTTP requests, date parsing, and news search.

Mitigation: Pin and audit dependencies before installation in sensitive or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibillxia/skills/spotify-news-digest)
- [Source Reference](references/sources_reference.md)
- [Spotify Engineering Blog RSS](https://engineering.atspotify.com/feed/)
- [Spotify Newsroom RSS](https://newsroom.spotify.com/feed/)
- [Spotify Research RSS](https://research.atspotify.com/feed/)
- [Spotify Design RSS](https://spotify.design/feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with categorized items, Chinese one-sentence summaries, source names, and original article links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The digest is filtered by a configurable time range, deduplicated by title similarity, ranked by source authority and recency, and can be printed or saved to a Markdown file.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
