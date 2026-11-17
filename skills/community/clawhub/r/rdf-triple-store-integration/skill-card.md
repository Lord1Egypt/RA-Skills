## Description:

Connect to RDF triple stores and execute SPARQL queries for storing, retrieving, and managing semantic knowledge graph data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agents to RDF triple stores, execute SPARQL queries, manage named graphs, and work with semantic knowledge graph data. It is suited for linked data integration, ontology-based applications, enterprise data integration, and RDF-backed knowledge representation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to insert, update, delete, or drop RDF store data.

Mitigation: Use read-only credentials by default, require explicit confirmation for INSERT, DELETE, DROP, and UPDATE operations, and test write operations against non-production graphs first.

Risk: Federated SPARQL SERVICE calls can query external endpoints and may expose sensitive data or rely on untrusted services.

Mitigation: Allow federated SERVICE calls only to approved endpoints and only with data that is safe to share externally.

Risk: Dynamically constructed SPARQL can produce unsafe or unintended queries when untrusted input is copied into examples.

Mitigation: Validate SPARQL before execution and avoid copying f-string query construction patterns with untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/rdf-triple-store-integration)
- [RDF SPARQL Design Patterns](artifact/references/rdf-sparql-patterns.md)
- [RDF Triple Store Examples](artifact/examples/rdf-tripple-examples.md)
- [W3C SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [W3C RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)
- [W3C OWL 2 Overview](https://www.w3.org/TR/owl2-overview/)
- [SPARQL By Example](https://www.w3.org/2009/sparql/wiki/SPARQL_By_Example)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with SPARQL, Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SPARQL queries that read from or modify RDF stores; review write operations before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
