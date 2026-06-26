## Description: <br>
Access 194+ datasets from the City of Vancouver open data portal. Search, fetch, and analyze city data on parking, transit, permits, demographics, and more via the Opendatasoft API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and civic data users use this skill to search Vancouver open datasets, inspect dataset metadata, and fetch records for analysis or CSV export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper sends queries to the City of Vancouver open data API and depends on that public service for availability and returned data. <br>
Mitigation: Review query parameters before execution and verify important results against the source portal when data quality, freshness, or availability matters. <br>
Risk: The helper may create a local catalog cache beside the script. <br>
Mitigation: Inspect or remove the local cache if stale dataset listings or local file hygiene are a concern. <br>


## Reference(s): <br>
- [City of Vancouver Open Data Portal](https://opendata.vancouver.ca) <br>
- [Opendatasoft API Endpoint](https://opendata.vancouver.ca/api/explore/v2.1) <br>
- [Popular Vancouver Open Data Datasets](references/datasets.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/raychanpmp/vancouver-opendata) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; command output can be plain text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python helper makes HTTPS requests to opendata.vancouver.ca and may cache the dataset catalog beside the script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
