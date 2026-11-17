## Description:

Access 194+ datasets from the City of Vancouver open data portal. Search, fetch, and analyze city data on parking, transit, permits, demographics, and more via the Opendatasoft API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and civic data users use this skill to search City of Vancouver datasets, inspect dataset metadata, fetch rows with filters, and export public data for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and filters are sent to the public City of Vancouver Open Data API.

Mitigation: Use the skill only for intended public-data queries and avoid including private or sensitive information in dataset filters.

Risk: The skill writes a small local cache of dataset listings under the script directory.

Mitigation: Review or clear the cache when local retention of queried catalog metadata is undesirable.

## Reference(s):

- [City of Vancouver Open Data Portal](https://opendata.vancouver.ca)
- [Opendatasoft API endpoint used by the skill](https://opendata.vancouver.ca/api/explore/v2.1)
- [Curated Vancouver dataset list](references/datasets.md)
- [ClawHub skill page](https://clawhub.ai/raychanpmp/skills/vancouver-opendata)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or CSV data returned by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound requests to opendata.vancouver.ca and write a local catalog cache under the skill script directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
