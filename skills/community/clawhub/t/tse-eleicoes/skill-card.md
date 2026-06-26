## Description: <br>
Cliente Python assíncrono para as APIs do TSE (Tribunal Superior Eleitoral), integrating DivulgaCandContas REST election, candidate, and campaign finance data with CKAN open-data datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegantonov](https://clawhub.ai/user/olegantonov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to add asynchronous Python access to Brazilian TSE election data, including candidates, election metadata, campaign finance records, donor rankings, and bulk open-data downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to documented public TSE and CKAN endpoints. <br>
Mitigation: Install and run it only when outbound access to those public endpoints is acceptable for the environment. <br>
Risk: Public API availability, response shape, and election data freshness may affect generated code or analysis. <br>
Mitigation: Handle timeouts and API errors, and validate important results against official TSE sources before relying on them. <br>
Risk: The package does not require credentials, so unnecessary secrets could expand exposure without benefit. <br>
Mitigation: Use a virtual environment and do not provide credentials or private tokens for normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olegantonov/tse-eleicoes) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/olegantonov) <br>
- [DivulgaCandContas API reference](references/divulgacandcontas-api.md) <br>
- [CKAN Dados Abertos TSE reference](references/ckan-api.md) <br>
- [TSE website](https://www.tse.jus.br/) <br>
- [TSE Dados Abertos portal](https://dadosabertos.tse.jus.br/) <br>
- [CKAN API documentation](https://docs.ckan.org/en/2.10/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create or use Python code that performs outbound HTTP requests to public TSE and CKAN endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
