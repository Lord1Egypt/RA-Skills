## Description:

Access 537+ datasets from the City of Toronto open data portal. Search, fetch, and analyze city data on transit, traffic, housing, environment, and more via the CKAN API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and civic data users use this skill to search City of Toronto open datasets, inspect dataset metadata, and fetch CKAN datastore records for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Results depend on live City of Toronto CKAN responses and a temporary local cache, so data may be stale or unavailable.

Mitigation: Refresh or clear the cache for time-sensitive work and verify important outputs against the City of Toronto Open Data Portal.

## Reference(s):

- [Popular & Useful Toronto Open Data Datasets](references/datasets.md)
- [City of Toronto Open Data Portal](https://open.toronto.ca)
- [City of Toronto CKAN API](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action)
- [ClawHub skill page](https://clawhub.ai/raychanpmp/skills/toronto-opendata)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands; fetched records may be JSON or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query public CKAN endpoints and create a temporary local cache for dataset catalog results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
