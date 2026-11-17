## Description:

Discover website sitemaps from robots.txt and common sitemap locations, choose the right sitemap or content family such as docs, blog, help center, academy, or changelog, and scrape selected public pages into a local folder as Markdown plus a manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quareth](https://clawhub.ai/user/quareth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover public website sitemap inventories, select a content family such as documentation, blog, or help-center content, and scrape the selected public pages into a traceable local corpus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound scraping and local corpus writes can touch more content than intended if scope and limits are too broad.

Mitigation: Use trusted public sites, set a small explicit --limit, apply narrow include filters, and choose an output directory inside the workspace.

Risk: Network safeguards and resource limits were flagged as weak by the authoritative security evidence.

Mitigation: Avoid running the skill where internal services or cloud metadata endpoints are reachable until DNS rebinding and resource-limit issues are fixed.

Risk: HTML-first extraction may produce weak or incomplete Markdown for heavily client-rendered pages.

Mitigation: Review the generated Markdown and manifest, and warn users when saved content is empty, navigation-heavy, or missing the visible article body.

## Reference(s):

- [Sitemap Selection Reference](artifact/references/sitemap-selection.md)
- [ClawHub skill page](https://clawhub.ai/quareth/skills/sitemap-content-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown files, manifest JSON, and concise agent-facing status text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one Markdown file per scraped page plus manifest.json containing saved, skipped, and failed page details.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
