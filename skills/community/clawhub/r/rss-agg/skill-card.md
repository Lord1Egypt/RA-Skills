## Description:

Parse, aggregate and process RSS/Atom feeds for tracking multiple feeds, creating personalized news digests, monitoring blog updates, or building newsletter content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to configure and run RSS/Atom feed aggregation with filtering for news monitoring, newsletter curation, trend tracking, and blog update notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided security summary says the helper fetches feeds insecurely.

Mitigation: Review or fix the helper before installation, keep TLS verification enabled, validate feed URLs before fetching, and avoid feed lists from untrusted sources.

Risk: The provided security summary says HTML output can be unsafe for untrusted feeds.

Mitigation: Avoid HTML output for untrusted feeds, or sanitize and escape feed-derived content before publishing or sharing generated HTML.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/rss-agg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, feed configuration snippets, and JSON, HTML, or Markdown output instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper accepts feed URLs, feed-list files, output path, output format, item limit, keyword filter, and date filter options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
