## Description:

Consulta promociones de viajes desde Argentina using the Anduin Promos API and helps agents filter, rank, and present current flights, hotels, cars, and package deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferminrp](https://clawhub.ai/user/ferminrp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve public Argentina-focused travel promotions, apply local filters or ranking, and present concise summaries with relevant timestamps and promo links.

### Deployment Geography for Use:

Global, with travel promotion data focused on Argentina.

## Known Risks and Mitigations:

Risk: The skill contacts an external public API and may show third-party travel deal links.

Mitigation: Expect requests only to https://anduin.ferminrp.com, avoid sending private credentials, and review outbound links before acting on them.

Risk: Travel promotions can become stale, unavailable, or incomplete after the API snapshot is fetched.

Mitigation: Present lastUpdated or response timestamps, avoid purchase recommendations or availability guarantees, and treat results as informational.

Risk: Expanded behavior beyond the documented flow could create unintended actions such as booking, scraping, alerts, or private account use.

Mitigation: Keep use to fetching the documented public promos endpoint, local filtering or sorting, and concise presentation of results.

## Reference(s):

- [Anduin Promos API OpenAPI](https://anduin.ferminrp.com/docs/openapi.json)
- [Anduin Promos API endpoint](https://anduin.ferminrp.com/api/v1/promos)
- [ClawHub skill page](https://clawhub.ai/ferminrp/skills/travel-promos-argentinas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with tables, timestamps, promo links, and optional inline curl/jq commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a public JSON API; filtering and sorting are performed locally by the agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
