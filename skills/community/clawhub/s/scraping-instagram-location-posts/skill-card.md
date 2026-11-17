## Description:

Scrapes Instagram posts tagged at a specific location or place using apidojo's Instagram Location scraper on Apify, returning post URL, author handle, caption, likes, comments, and timestamp per post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, hospitality brands, event teams, and content collectors use this skill to collect Instagram posts associated with a location or venue for discovery, reporting, or user-generated content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram location targets and retrieved post metadata are sent through Apify and apidojo.

Mitigation: Install only when that third-party data flow is acceptable for the intended use case, and handle collected author, caption, and engagement metadata responsibly.

Risk: Token-bearing Apify URLs can expose credentials if copied into shells, logs, or chats.

Mitigation: Prefer Authorization headers, managed Apify tooling, or the APIFY_TOKEN environment variable instead of embedding tokens in URLs.

Risk: Unbounded scraping can collect more personal or venue-related metadata than intended.

Mitigation: Set explicit maxItems limits and scope collection to the minimum locations and dates needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-location-posts)
- [ClawHub publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor reference](https://apify.com/apidojo/instagram-location-scraper)
- [Instagram location search](https://www.instagram.com/explore/locations/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, and tabular post metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save retrieved post datasets as CSV or JSON when using the Apify runner workflow.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
