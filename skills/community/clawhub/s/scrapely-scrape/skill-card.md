## Description:

Scrape websites and collect web data with Scrape.ly Store Actors. Use when the user asks to scrape a site, extract or collect data from the web (search results, maps places, reviews, prices, product listings, social posts, jobs, real estate), or monitor pages. Finds the right ready-made Actor, runs it with the user's SCRAPELY_TOKEN, and fetches the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapely-app](https://clawhub.ai/user/scrapely-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can find a ready-made Scrape.ly Store Actor, run it to collect web data, and review or page through the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests may send the API token to an unintended server after a redirect or API address override.

Mitigation: Verify that the API destination is trusted and that redirects or address overrides cannot route authenticated requests elsewhere.

## Reference(s):

- [Scrape.ly skill listing](https://clawhub.ai/scrapely-app/skills/scrapely-scrape)
- [Scrape.ly API](https://api.scrape.ly)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands]

**Output Format:** [JSON results with user-requested summaries, tables, CSV, or saved data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be paged; large datasets should be saved to a file and presented with a short sample.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
