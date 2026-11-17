## Description:

Scrape and extract structured data from public creator profiles across platforms such as YouTube, Instagram, TikTok, Twitter/X, LinkedIn, Twitch, Substack, GitHub, Patreon, and personal websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and creator operations teams use this skill to resolve public creator handles or URLs, collect profile metadata and stats, and compare creators for research, reporting, or exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-provided creator profile URLs and collect public profile data over the network.

Mitigation: Use it only for public creator profiles and avoid logged-in browser sessions unless necessary for a legitimate user request.

Risk: Apify fallback may send requested profile URLs and scrape inputs to a third-party scraping service.

Mitigation: Require confirmation before Apify fallback and use a narrowly scoped APIFY_API_TOKEN.

Risk: Saved JSON or CSV exports may be unsafe until path and spreadsheet-formula handling is reviewed.

Mitigation: Treat saved exports as untrusted data, review output paths before writing, and sanitize CSV content before opening it in spreadsheet tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahqazi-dev/skills/scrape-creator-profile)
- [Platform Selectors Reference](references/platform-selectors.md)
- [Apify Actors Fallback Reference](references/apify-actors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Files, Guidance]

**Output Format:** [Markdown summaries, normalized JSON objects, Markdown comparison tables, CSV exports, and saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process one profile or a sequence of profiles; fields not publicly available are returned as null.]

## Skill Version(s):

1.0.0 (source: frontmatter, README, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
