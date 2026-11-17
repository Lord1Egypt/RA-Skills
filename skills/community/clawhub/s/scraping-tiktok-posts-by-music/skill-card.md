## Description:

Extracts TikTok posts using a specific audio track or sound with apidojo's TikTok Music Scraper on Apify, returning post details, creator information, hashtags, and song metadata for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, music marketers, trend analysts, and viral sound trackers use this skill to collect TikTok posts associated with a specific music or sound URL for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok music URLs and run parameters are sent to Apify/apidojo.

Mitigation: Use a scoped Apify token and avoid including sensitive query data.

Risk: Broad or uncapped scrapes may return very large datasets.

Mitigation: Set maxItems when a full scrape is not needed.

Risk: Copyrighted, regional, trending, or removed sounds may produce partial, very large, or empty results.

Mitigation: Check result coverage and handle empty datasets before relying on downstream analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tiktok-posts-by-music)
- [Apify actor run endpoint](https://api.apify.com/v2/acts/apidojo~tiktok-music-scraper/runs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced Apify actor can return raw TikTok post datasets as table, CSV, or JSON when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
