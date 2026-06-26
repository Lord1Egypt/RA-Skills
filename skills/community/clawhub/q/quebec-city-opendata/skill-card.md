## Description: <br>
Access 37+ datasets from the City of Quebec open data portal. Search, fetch, and analyze city data on streets, permits, trees, infrastructure, and more via the CKAN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and civic-data users use this skill to discover Ville de Québec datasets, inspect dataset metadata, and fetch CKAN datastore records for analysis or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a Python CLI through Bash, performs public web requests to donneesquebec.ca, and writes a small cached catalog under the OpenClaw workspace data directory. <br>
Mitigation: Install and run it only in environments where Bash execution, public CKAN API access, and local cache storage are acceptable. <br>


## Reference(s): <br>
- [Ville de Québec Open Data Portal](https://www.ville.quebec.qc.ca/services/donnees-services-ouverts/) <br>
- [Ville de Québec Data Hub](https://www.donneesquebec.ca/organisation/ville-de-quebec/) <br>
- [CKAN API endpoint](https://www.donneesquebec.ca/api/3/action) <br>
- [Dataset reference](references/datasets.md) <br>
- [ClawHub skill page](https://clawhub.ai/raychanpmp/quebec-city-opendata) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, CSV, analysis] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON or CSV data output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public CKAN API requests and may cache the dataset catalog locally for one hour.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
