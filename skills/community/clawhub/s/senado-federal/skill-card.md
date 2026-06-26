## Description: <br>
Monitor and research Brazilian Senate legislative activity, including bills, agendas, senators, votes, committees, speeches, mandates, and public accountability data via open Senate APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegantonov](https://clawhub.ai/user/olegantonov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, journalists, policy analysts, and developers use this skill to query Brazilian Senate open data for legislative tracking, senator research, voting history, committee activity, and transparency review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query public administrative transparency data that may include names, compensation, pension, office, supplier, tax identifier, telephone, or email details. <br>
Mitigation: Use results for legitimate transparency and legislative research; avoid bulk profiling, doxxing, harassment, or unsolicited outreach. <br>
Risk: Dependency hygiene is not fully pinned by a lockfile in the release evidence. <br>
Mitigation: Install in an isolated environment and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olegantonov/senado-federal) <br>
- [Senado Federal Open Data API](https://legis.senado.leg.br/dadosabertos) <br>
- [Senado Federal Open Data Swagger UI](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html) <br>
- [Senado Federal Administrative Open Data Swagger UI](https://adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html) <br>
- [Complete endpoint reference](references/api-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with API examples, Python snippets, shell commands, and summarized public-data results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live API queries against public Senado Federal endpoints; no authentication is required by the documented APIs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter declares 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
