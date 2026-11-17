## Description:

Search and extract high-value posts from X (Twitter) with engagement-based ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghostwritten](https://clawhub.ai/user/ghostwritten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search X/Twitter for a topic, collect candidate posts, and return higher-engagement highlights for monitoring, research, or content curation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation runs JavaScript inside a logged-in X.com session.

Mitigation: Review before installing, use a dedicated low-privilege browser profile for X, and avoid attacker-supplied search strings or unusual numeric parameters.

Risk: Search quality, rate limits, and lazy loading can produce incomplete or unstable result sets.

Mitigation: Treat outputs as curated search highlights rather than comprehensive evidence, and adjust scroll counts or retry timing when results are sparse.

Risk: Unbounded or malformed numeric arguments can increase scraping volume or produce unreliable behavior.

Mitigation: Prefer a version that validates numeric bounds and JSON-encodes text inputs before browser evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghostwritten/skills/x-search-highlights)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON search-result summaries with post text, author, date, engagement metrics, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks extracted X posts by engagement and requires bb-browser, Chrome/Chromium, and an X.com login state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
