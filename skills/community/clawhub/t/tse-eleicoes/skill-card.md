## Description:

Provides an asynchronous Python client for Brazil's TSE election APIs, covering DivulgaCandContas candidate and campaign-accounting endpoints plus CKAN open-data dataset discovery and download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantonov](https://clawhub.ai/user/olegantonov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to query Brazilian election, candidate, campaign finance, and open-data dataset information from public TSE APIs through async Python code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated usage may make outbound requests to public TSE and CKAN API domains.

Mitigation: Run it in an environment where those domains are expected and allowed, and review network policy before CI or production use.

Risk: Dependency ranges can change resolved package versions over time.

Mitigation: Pin or lock dependencies before use in CI or production.

Risk: Public API responses, available datasets, and election identifiers can change over time.

Mitigation: Validate important results against official TSE sources and update constants or references when the upstream APIs change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olegantonov/skills/tse-eleicoes)
- [DivulgaCandContas API reference](references/divulgacandcontas-api.md)
- [CKAN Dados Abertos TSE reference](references/ckan-api.md)
- [DivulgaCandContas REST base API](https://divulgacandcontas.tse.jus.br/divulga/rest/v1)
- [TSE Dados Abertos CKAN API](https://dadosabertos.tse.jus.br/api/3/action)
- [TSE open data portal](https://dadosabertos.tse.jus.br/)
- [CKAN API documentation](https://docs.ckan.org/en/2.10/api/)
- [Tribunal Superior Eleitoral](https://www.tse.jus.br/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated usage may make outbound HTTP requests to public TSE DivulgaCandContas and CKAN API domains.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
