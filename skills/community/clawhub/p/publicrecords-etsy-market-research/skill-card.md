## Description:

Research Etsy markets with two public-data Actors: live Etsy search, market and category listing rows (price, rating, reviews, Bestseller and Star Seller badges, ad flag, search rank) and daily, 7-day and 28-day sales for Etsy shops measured from each shop's public sales counter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT

## Use Case:

Ecommerce researchers and Etsy sellers can use the skill to inspect current listing positions, prices, ratings, badges and ad placement, then track shops' daily, 7-day and 28-day sales from their public sales counters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended Apify MCP connection can expose unrelated Actor tools alongside the Etsy research tools.

Mitigation: Review the available MCP tools and restrict the connection to the Etsy tools needed for the task.

Risk: The security analysis was partial because referenced local configuration paths could not be resolved.

Mitigation: Review the MCP configuration and referenced paths before installation.

## Reference(s):

- [Etsy Search Scraper on Apify Store](https://apify.com/publicrecords/etsy-search-scraper)
- [Etsy Shop Velocity on Apify Store](https://apify.com/publicrecords/etsy-shop-velocity)
- [ClawHub skill release](https://clawhub.ai/geminigeorge22/skills/publicrecords-etsy-market-research)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Markdown summaries and tables, with structured listing and shop data as returned by the Actors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Etsy research; Actor runs are pay-per-event on the user's Apify account.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
