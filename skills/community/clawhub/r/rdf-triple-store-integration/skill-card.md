## Description: <br>
Connect to RDF triple stores and execute SPARQL queries for storing, retrieving, and managing semantic knowledge graph data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge graph engineers use this skill to connect agents to RDF triple stores, run SPARQL queries, manage triples and named graphs, and work with ontology or linked data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SPARQL update operations can change or remove graph data. <br>
Mitigation: Use read-only credentials by default, require explicit review before INSERT, DELETE, UPDATE, or DROP operations, scope writes to named graphs, and keep production graph backups. <br>
Risk: Federated SERVICE queries or non-HTTPS endpoints can expose query data to remote services. <br>
Mitigation: Avoid federated SERVICE queries and non-HTTPS endpoints unless the remote service is trusted. <br>
Risk: Authenticated endpoints may require sensitive credentials. <br>
Mitigation: Use scoped credentials and avoid embedding secrets in prompts, files, or examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/rdf-triple-store-integration) <br>
- [RDF SPARQL Design Patterns](references/rdf-sparql-patterns.md) <br>
- [W3C SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) <br>
- [RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/) <br>
- [OWL 2 Web Ontology Language Overview](https://www.w3.org/TR/owl2-overview/) <br>
- [SPARQL By Example](https://www.w3.org/2009/sparql/wiki/SPARQL_By_Example) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SPARQL, Python, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SPARQL endpoint configuration, credential handling guidance, query/update examples, and Python connector usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
