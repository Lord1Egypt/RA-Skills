## Description:

Searches Upkuajing's map merchant database for offline businesses and local service providers using geography, radius, industry, keyword, business-name, rating, and contact-availability filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, channel, brand, and regional market teams use this skill to find merchant leads, assess local market density, plan offline coverage, support distributor sourcing, and compare store locations across countries, provinces, cities, districts, and nearby areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and store an API key for billable Upkuajing account actions without enforcing restrictive local file permissions.

Mitigation: Store the API key carefully, set ~/.upkuajing/.env permissions to 0600, and avoid sharing the file or account environment.

Risk: Merchant search calls can consume paid account balance, especially when a request asks for more than 100 records.

Mitigation: Confirm the estimated call count and obtain explicit user confirmation before running billable or large searches.

Risk: Error reports may include request or response context from failed skill calls.

Mitigation: Ask for confirmation before reporting and avoid including sensitive request or response data in the report context.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/upkuajing-map-merchants-search-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Merchant search API reference](references/merchants-search-api.md)
- [Country list API reference](references/country-list-api.md)
- [Province list API reference](references/province-list-api.md)
- [City list API reference](references/city-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; merchant search calls may be billable and large queries require explicit confirmation.]

## Skill Version(s):

1.0.6 (source: SKILL.md metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
