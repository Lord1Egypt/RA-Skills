## Description: <br>
Draft RDF or OWL ontologies and schemas for knowledge graph systems using domain descriptions, entity models, or schema requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge graph practitioners use this skill to translate domain descriptions, entity models, relational schemas, or data structures into RDF/OWL ontology drafts with classes, properties, domain and range constraints, and Turtle or RDF/XML serialization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Python helper can write generated ontology files to caller-provided paths. <br>
Mitigation: Run the helper in a trusted project environment and choose output paths deliberately. <br>
Risk: Generated RDF/OWL schemas may encode incorrect classes, relationships, ranges, or constraints if the source domain model is incomplete. <br>
Mitigation: Review ontology drafts with domain experts and validate them with normal RDF/OWL or SHACL tooling before production use. <br>
Risk: The helper depends on rdflib when executed. <br>
Mitigation: Install rdflib from the project's normal trusted package source and pin dependencies when used in a production workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/rdf-owl-schema-drafting) <br>
- [OWL ontology design patterns](references/ontology-patterns.md) <br>
- [Domain ontology examples](examples/example-ontologies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Turtle, RDF/XML, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce ontology files when the optional Python helper is run with an explicit output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
