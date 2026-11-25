## Description:

See a competitor's Google ads from the Google Ads Transparency Center: enter a website or advertiser ID and get its new, running and stopped ads with first and last shown dates, days shown, format and ad links, optionally by region. Use when the user asks what ads a competitor is running on Google, which ads are new this week, or how long an ad has run. Runs publicrecords/google-ads-transparency-scraper on Apify (pay per event, user's own Apify account).

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and analysts use this skill to look up a competitor's Google ads by website, advertiser ID, Ads Transparency Center link, or exact advertiser name, then summarize ad activity by date, status, or region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because the advertised Google Ads lookup does not match the supplied Apify request, and the recommended MCP connection exposes many unrelated tools.

Mitigation: Before use, confirm the actor and input configuration match the advertised lookup and limit the MCP connection to the tools needed for it. The scan was partial, so treat its evidence as incomplete.

## Reference(s):

- [Apify Google Ads Transparency Scraper](https://apify.com/publicrecords/google-ads-transparency-scraper)
- [ClawHub skill release](https://clawhub.ai/geminigeorge22/skills/publicrecords-google-ads-transparency)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown instructions and summaries of retrieved ad listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ad coverage depends on query filters and source data. Apify runs are pay per event on the user's account.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
