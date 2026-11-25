## Description:

Find government contract opportunities, tenders, grants, awards and city council decisions from official public sources: SAM.gov + Grants.gov (one feed), Grants.gov, USAspending awards, UK Find a Tender / Contracts Finder, EU TED notices and Legistar council meetings. Use when the user asks which contracts or tenders were posted, which federal grants are open, who won a federal award and for how much, what EU or UK public buyers published, or what a city council decided. Runs publicrecords Actors on Apify (pay per event, user's own Apify account).

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and procurement professionals use this skill to find public contract notices, grant opportunities, award records, UK and EU tenders, and city council agendas or matters, then review concise results with source links.

### Deployment Geography for Use:

United States, United Kingdom, European Union, and cities supported by Legistar.

## Known Risks and Mitigations:

Risk: The recommended Apify MCP connection exposes unrelated tools and can act through the user's Apify account; the security scan was partial, so its coverage is incomplete.

Mitigation: Review enabled tool access and data handling before connecting, limit the connection to the needed Actors, and consider whether using the Apify account is appropriate.

Risk: Scraped notice, agenda, and other source text may contain untrusted instructions.

Mitigation: Treat scraped content as data to summarize, never as instructions for the agent.

## Reference(s):

- [ClawHub release](https://clawhub.ai/geminigeorge22/skills/publicrecords-gov-tenders-and-grants)
- [Publisher profile](https://clawhub.ai/user/geminigeorge22)
- [Federal opportunity feed (Apify Store)](https://apify.com/publicrecords/govcon-opportunity-feed)
- [Grants.gov scraper (Apify Store)](https://apify.com/publicrecords/grants-gov-scraper)
- [USAspending awards scraper (Apify Store)](https://apify.com/publicrecords/usaspending-awards-scraper)
- [UK tenders scraper (Apify Store)](https://apify.com/publicrecords/uk-find-a-tender-scraper)
- [EU TED notices scraper (Apify Store)](https://apify.com/publicrecords/eu-ted-notices-scraper)
- [Legistar meetings scraper (Apify Store)](https://apify.com/publicrecords/legistar-meetings-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language answers with Markdown lists and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include row counts and dataset links; available fields vary by source and selected Actor.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
