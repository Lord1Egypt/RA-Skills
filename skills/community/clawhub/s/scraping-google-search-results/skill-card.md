## Description:

Scrapes Google search results for any query using apidojo's Google Search scraper on Apify, returning URL, title, snippet, position, and SERP feature type per result for SEO, research, journalism, and competitive intelligence workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO analysts, researchers, journalists, and competitive intelligence teams use this skill to collect Google SERP datasets for one or more queries. It helps agents run an Apify Google Search scraper, retrieve results, and present URLs, titles, snippets, positions, and SERP feature types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and related run data are sent to Apify when the scraper runs.

Mitigation: Avoid sensitive or regulated queries, disclose the external service dependency, and use the skill only when sending the query data to Apify is acceptable.

Risk: Token-in-URL curl examples can expose an Apify token through shell history, logs, or copied command output.

Mitigation: Use a scoped Apify token where possible and prefer safer authentication patterns over placing secrets directly in URLs.

Risk: SERP results can vary by country, language, device mode, time, and personalization, which may affect comparisons.

Mitigation: Set countryCode, languageCode, mobileResults, maxPagesPerQuery, and collection time explicitly when reproducible analysis is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-google-search-results)
- [Apify actor: apidojo/google-search-scraper](https://apify.com/apidojo/google-search-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown tables with optional JSON or CSV datasets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include query, position, URL, title, description, SERP feature type, sitelinks, rating, and review count.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
