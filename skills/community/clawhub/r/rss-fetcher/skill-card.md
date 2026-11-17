## Description:

RSS Fetcher helps agents configure, fetch, deduplicate, tag, query, and report on RSS/Atom feed articles using local Python scripts and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain RSS source lists, fetch recent articles into SQLite, apply tags, query results, and generate a local filterable HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted feed content can become executable JavaScript in generated HTML reports.

Mitigation: Treat generated reports as untrusted, review them before sharing, and escape feed-derived title, URL, source, category, and tag values before rendering.

Risk: Configured feed URLs are not safely constrained and could target private networks, localhost, or internal services.

Mitigation: Audit sources before fetching, prefer HTTPS-only public feeds, and reject localhost, private-network, and internal-service URLs.

Risk: The aggregator can make broad outbound requests to many configured RSS feeds.

Mitigation: Run fetch and health-check commands in a network-restricted environment and keep the source list limited to trusted feeds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/rss-fetcher)
- [SQLite schema reference](artifact/references/schema.sql)
- [Configured RSS sources](artifact/config/sources.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with shell commands; scripts emit terminal text, optional JSON, SQLite data, and a static HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; fetches configured RSS/Atom URLs and writes local SQLite and HTML report artifacts.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
