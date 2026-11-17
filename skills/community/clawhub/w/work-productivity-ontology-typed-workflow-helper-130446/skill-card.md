## Description:

Design typed ontology and knowledge-graph workflows for agent memory, structured notes, domain models, and retrieval systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, skill authors, and teams use this skill to turn loose notes, agent memory, domain objects, or research material into typed ontologies with validation, examples, maintenance rules, and query patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad localized or reference wording could lead users to apply the skill to generic bug-fixing or reliability work outside ontology design.

Mitigation: Invoke it explicitly for ontology, schema, entity-relation, validation, migration, or query-pattern tasks, and review the result against the intended domain boundary.

Risk: Ontology outputs may encode incorrect entity boundaries, relation cardinality, identifiers, or validation rules if the source material is incomplete.

Mitigation: Review generated schemas with domain examples, include invalid examples, and validate identifiers, provenance fields, and merge rules before relying on the model.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-ontology-typed-workflow-helper-130446)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Forked CozoDB to give agents cognitive primitives](https://news.ycombinator.com/item?id=48605896)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with optional JSON Schema, YAML schema, TypeScript types, table definitions, examples, and validation checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored ontology specifications, migration notes, governance guidance, and retrieval or query patterns.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
