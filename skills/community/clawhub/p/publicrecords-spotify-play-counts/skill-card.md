## Description:

Get Spotify play counts for every track on a track, album, playlist or artist link, plus an artist's monthly listeners and followers, with optional daily stream deltas (last 1, 7 and 30 days).

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT-0

## Use Case:

Listeners, music researchers, and artist teams use the skill to check track play counts, artist monthly listeners and followers, and recent stream growth from Spotify links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended Apify MCP connection exposes Actors beyond Spotify analytics; the security evidence also reports an external Apify API call and incomplete scan coverage.

Mitigation: Before connecting, review the available Actors and limit access to the Spotify analytics Actor where possible. Confirm the Apify endpoint and data handling are appropriate, account for possible charges, and review the skill configuration because scan coverage was incomplete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/geminigeorge22/skills/publicrecords-spotify-play-counts)
- [Spotify Play Count Scraper on Apify Store](https://apify.com/publicrecords/spotify-play-count-scraper)
- [Hosted Apify MCP server configuration](https://mcp.apify.com/?tools=publicrecords/company-social-profile-finder,publicrecords/govcon-opportunity-feed,publicrecords/grants-gov-scraper,publicrecords/usaspending-awards-scraper,publicrecords/uk-find-a-tender-scraper,publicrecords/eu-ted-notices-scraper,publicrecords/legistar-meetings-scraper,publicrecords/ashby-jobs-scraper,publicrecords/greenhouse-jobs-scraper,publicrecords/lever-jobs-scraper,publicrecords/smartrecruiters-jobs-scraper,publicrecords/etsy-search-scraper,publicrecords/etsy-shop-velocity,publicrecords/google-ads-transparency-scraper,publicrecords/sports-odds-api,publicrecords/spotify-play-count-scraper,publicrecords/calibration-ledger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise summaries and Markdown tables of play counts, artist audience figures, and optional stream deltas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and coverage depend on the Spotify links, selected options, and track limit.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
