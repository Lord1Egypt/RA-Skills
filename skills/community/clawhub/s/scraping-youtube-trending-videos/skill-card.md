## Description:

Extracts YouTube trending videos by category and country using apidojo's YouTube Trending Scraper on Apify and returns video title, URL, view count, like count, channel information, description, and thumbnails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, trend analysts, YouTube marketers, and developers use this skill to collect point-in-time YouTube trending video data by category, country, language, and result limit for downstream analysis or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Apify for YouTube trending data collection and may require an APIFY_TOKEN for REST API execution.

Mitigation: Install only when Apify use is acceptable and provide tokens through normal secret-handling practices.

Risk: Export commands can overwrite an existing CSV or JSON file if a reused path is supplied.

Mitigation: Choose deliberate output filenames or directories before exporting results.

Risk: Trending results are point-in-time data and may be empty, unavailable for a category, or vary by region and session.

Mitigation: Validate country and language codes, fall back to the general trending category when needed, and retry or timestamp collected datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-trending-videos)
- [Apify YouTube Trending Scraper REST API](https://api.apify.com/v2/acts/apidojo~youtube-trending-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of category, country, language, maximum item count, and optional custom JavaScript mapping inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
