## Description:

RSS Sitemap helps agents discover website URLs, feed entries, and recent publications from sitemap, Atom, RSS, and robots.txt resources before falling back to general crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover crawlable URLs, recent posts, and feed entries from a named website before broader crawling or scraping. It is useful when recency, site coverage, or feed and sitemap provenance should guide downstream research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host execution can fetch arbitrary URLs and read or overwrite user-chosen local files.

Mitigation: Use allow-once for routine use, or grant persistent approval only with argument, network destination, and output path restrictions.

Risk: Exposing the skill in untrusted chat contexts could let others trigger network or local-file discovery workflows.

Mitigation: Limit access to trusted contexts and run the skill only for domains and files intentionally selected by the operator.

Risk: Some sites may block feed or sitemap fetches, require JavaScript, or require authentication, so discovery results can be incomplete.

Mitigation: Treat results as a crawl frontier, fall back to approved browser or scraping tools when needed, and respect robots, rate limits, authentication boundaries, and user instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carlosdelfino/skills/rss-sitemap)
- [Publisher profile](https://clawhub.ai/user/carlosdelfino)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON discovery output from the bundled Node.js preprocessor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The discovery output includes probed resources, normalized entries, dates when available, and per-entry source provenance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
