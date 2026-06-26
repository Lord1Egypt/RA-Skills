## Description: <br>
Access 537+ datasets from the City of Toronto open data portal, and search, fetch, and analyze city data on transit, traffic, housing, environment, and more via the CKAN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and civic data users can use this skill to discover City of Toronto datasets, inspect dataset metadata, and fetch public CKAN datastore records for analysis or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a Python helper through Bash and contacts the public City of Toronto open data API. <br>
Mitigation: Review the command before execution and use it only when network access to the public CKAN API is expected. <br>
Risk: Fetched public datasets may be incomplete, changed, or unsuitable for a specific operational decision. <br>
Mitigation: Check the returned dataset metadata and source portal context before relying on results. <br>
Risk: The helper may store a small local catalog cache in the skill script directory. <br>
Mitigation: Clear the cache if stale catalog data is suspected or if local workspace cleanliness is required. <br>


## Reference(s): <br>
- [City of Toronto Open Data Portal](https://open.toronto.ca) <br>
- [City of Toronto CKAN API](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action) <br>
- [Popular Toronto Open Data Datasets](references/datasets.md) <br>
- [ClawHub skill page](https://clawhub.ai/raychanpmp/toronto-opendata) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Terminal output, JSON records, or CSV rows from public CKAN datasets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local catalog cache under the skill script directory; no credentials are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
