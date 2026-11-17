## Description:

Research Brazil's Federal Senate using its official legislative and administrative open-data APIs. Use for senators, Senate bills and processes, votes, agendas, committees, speeches, mandates, CEAP expenses, contracts, or transparency records; use camara-deputados for Chamber-only records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantonov](https://clawhub.ai/user/olegantonov)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, journalists, and policy analysts use this skill to query official Brazilian Federal Senate legislative and administrative open-data APIs for senators, bills, votes, agendas, committees, speeches, CEAP expenses, contracts, and transparency records. It supports auditable research and reusable Python integrations that preserve official identifiers and source URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions may drift because the artifact has requirements but no lockfile or dependency hashes.

Mitigation: Install the skill in an isolated Python environment and review resolved dependency versions before operational use.

Risk: Public Senate API data can be time-sensitive or shaped differently across legislative and administrative endpoints.

Mitigation: Use exact official API URLs, preserve retrieval dates and official identifiers, and distinguish empty results from upstream API failures.

Risk: Financial or transparency summaries can be misleading if response fields or filters are normalized incorrectly.

Mitigation: Validate response shapes, state filters and currency handling, and cite the fields used for CEAP or administrative totals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olegantonov/skills/senado-federal)
- [Senate legislative API endpoint reference](references/api-endpoints.md)
- [Senate response shapes, identifiers, and dates](references/response-shapes.md)
- [Senate administrative and transparency API](references/administrative-api.md)
- [Tracking a process across the Senate and Chamber](references/cross-house.md)
- [Official Senate Legislative API](https://legis.senado.leg.br/dadosabertos)
- [Official Senate Legislative Swagger](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html)
- [Official Senate Administrative API](https://adm.senado.gov.br/adm-dadosabertos)
- [Official Senate Administrative Swagger](https://adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with API URLs, Python snippets, shell commands, or structured JSON-like summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact public Senate API URLs and retrieval dates for auditable outputs; no credentials required.]

## Skill Version(s):

1.1.0 (source: SKILL.md metadata, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
