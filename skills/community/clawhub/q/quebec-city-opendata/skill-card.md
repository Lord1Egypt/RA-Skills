## Description:

Access 37+ datasets from the City of Quebec open data portal, including streets, permits, trees, infrastructure, and related city data via the CKAN API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to discover Ville de Quebec open datasets, inspect dataset metadata, and fetch queryable CKAN records for civic data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bash-backed helper contacts donneesquebec.ca and caches the public dataset catalog locally.

Mitigation: Run it only in environments where outbound access to donneesquebec.ca and a local public-data cache are acceptable.

Risk: CSV exports contain untrusted public data.

Mitigation: Inspect CSV output or import it as text before opening it in spreadsheet software.

## Reference(s):

- [Dataset Reference](references/datasets.md)
- [Ville de Quebec Open Data Portal](https://www.ville.quebec.qc.ca/services/donnees-services-ouverts/)
- [Donnees Quebec - Ville de Quebec](https://www.donneesquebec.ca/organisation/ville-de-quebec/)
- [Donnees Quebec CKAN API](https://www.donneesquebec.ca/api/3/action)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can contact donneesquebec.ca, cache the public dataset catalog locally, and print fetched records as JSON or CSV.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
