## Description: <br>
Routes natural-language requests into SQL, SPARQL, SPASQL, SPARQL-FED, and GraphQL queries against live data spaces and knowledge graphs through OpenLink web services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidehen](https://clawhub.ai/user/kidehen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and knowledge-graph users use this skill to generate and route queries for databases, RDF stores, SPARQL endpoints, GraphQL endpoints, OpenLink Virtuoso, OPAL, and URIBurner data spaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated queries may be sent to external OpenLink or configured SQL, SPARQL, or GraphQL endpoints. <br>
Mitigation: Review generated queries and target endpoints before execution, and avoid including secrets or private data in prompts. <br>
Risk: Authenticated OpenLink or MCP configurations may expose broader data access than the task requires. <br>
Mitigation: Use least-privilege credentials and confirm the configured endpoint and permission scope before running authenticated requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kidehen/sql-sparql-graphql-skill) <br>
- [Data Twingler Protocol Routing](references/protocol-routing.md) <br>
- [Data Twingler Query Templates Reference](references/query-templates.md) <br>
- [OpenLink AI Layer (OPAL)](https://opal.openlinksw.com) <br>
- [OpenLink Virtuoso Platform](https://virtuoso.openlinksw.com) <br>
- [Data Twingler GPT Store listing](https://chatgpt.com/g/g-z8YBujVdf-openlink-data-twingler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with query snippets, tables, source links, citations, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL, SPARQL, SPASQL, SPARQL-FED, GraphQL, curl commands, endpoint settings, and tabulated query results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
