## Description:

Extract entities and relationships from unstructured text and convert them into graph-ready structures such as triples, nodes, and edges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to turn documents, articles, transcripts, or raw text into graph-ready entities, relationships, triples, and node-edge structures for knowledge graphs and semantic systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted graph outputs may preserve confidential, medical, legal, financial, or other sensitive details from source text.

Mitigation: Use appropriate privacy controls, review outputs before sharing, and avoid processing sensitive documents unless authorized.

Risk: Rule-based or pattern-based extraction can miss entities or produce incorrect relationships.

Mitigation: Validate extracted entities, relationships, triples, and confidence scores against source documents and domain knowledge before downstream use.

## Reference(s):

- [Text Extraction Design Patterns](references/extraction-patterns.md)
- [Text Entity Relation Extraction Examples](examples/example-extractions.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/text-entity-relation-extractor)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, plus optional JSON, RDF/Turtle, triples, and tabular extraction outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include entity types, relationships, confidence scores, normalized entity names, graph nodes and edges, and semantic triples.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
