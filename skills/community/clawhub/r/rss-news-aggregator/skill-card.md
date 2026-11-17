## Description:

Aggregates multiple RSS and Atom feeds, filters articles by keyword or source, deduplicates results, and generates news summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to combine multiple RSS or Atom sources into a single stream, monitor keywords across feeds, and produce readable Markdown or text news reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted feed URLs can be used in shared or server-side environments without URL, host, or network-range safeguards.

Mitigation: Use only trusted feed URLs unless the integration adds scheme and host validation, private/internal/metadata address blocking, request timeouts, and response-size limits.

Risk: Dependency versions are specified as minimum ranges rather than pinned versions.

Mitigation: Pin and review dependency versions before deployment, then update them through the normal security patch process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/rss-news-aggregator)
- [Publisher profile](https://clawhub.ai/user/kaiyuelv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Python API results plus Markdown or plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-dependent feed fetching; article fields include title, link, summary, source, published date, and author when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
