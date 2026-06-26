## Description: <br>
Extract entities and relationships from unstructured text and convert them into graph-ready structures such as triples, nodes, and edges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data engineers use this skill to turn documents, articles, transcripts, and raw text into graph-ready entity and relationship structures for knowledge graphs, semantic systems, or graph databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to surface names, dates, diagnoses, organizations, and relationships from input text, which can expose sensitive personal or domain-specific information. <br>
Mitigation: Use only authorized inputs, prefer de-identified text for medical, legal, or personal records, and review extracted entities and relationships before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/text-entity-relation-extractor) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [Extraction patterns](references/extraction-patterns.md) <br>
- [Example extractions](examples/example-extractions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, configuration snippets, RDF/Turtle, graph JSON, triples, and tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include entity types, relationships, confidence scores, normalized entities, RDF triples, graph nodes and edges, and tabular summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
