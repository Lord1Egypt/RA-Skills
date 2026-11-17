## Description:

Transforms natural language questions into SPARQL queries for DBpedia, executes read-only queries, and formats results as JSON, Markdown tables, or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidehen](https://clawhub.ai/user/kidehen)

### License/Terms of Use:


## Use Case:

Developers, researchers, and knowledge graph users use this skill to ask plain-English questions against DBpedia and receive structured query results. It supports entity lookups, research tables, and generated HTML reports with DBpedia attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and query terms may be sent to the public DBpedia endpoint.

Mitigation: Do not include secrets, private names, internal project terms, or sensitive personal data in DBpedia questions or generated queries.

Risk: Generated HTML reports may contain unsanitized or misleading content from query results.

Mitigation: Review or sanitize generated HTML before opening, publishing, or sharing reports.

## Reference(s):

- [DBpedia SPARQL Endpoint](https://dbpedia.org/sparql)
- [DBpedia](https://dbpedia.org)
- [DBpedia Documentation](https://www.dbpedia.org/resources/documentation/)
- [Sample DBpedia Query Patterns](artifact/examples/sample-queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SPARQL and shell command code blocks, plus optional JSON results, Markdown tables, or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include DBpedia endpoint requests and generated HTML reports for local review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
