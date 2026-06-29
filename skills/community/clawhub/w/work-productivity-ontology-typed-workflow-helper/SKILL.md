---
name: work-productivity-ontology-typed-workflow-helper
description: Design typed ontologies and lightweight knowledge graphs for agent workflows. Use when the user needs entity and relationship modeling, schema decisions, controlled vocabularies, graph migration plans, validation rules, or structured memory design.
---

# Work Productivity Ontology Typed Workflow Helper

Use this skill when unstructured notes, tool outputs, or workflow records need a typed model that agents and humans can query consistently.

Read `references/requirement-plan.md` for source evidence and scoring background.

## Modeling Inputs

Clarify:

- Domain scope and the questions the model must answer.
- Core entity types, relationship types, and event types.
- Required identifiers, provenance fields, timestamps, and confidence levels.
- Storage target: Markdown, JSON, SQLite, graph database, RDF, or another local format.

## Workflow

1. Start from user questions, not from abstract taxonomy.
2. Draft a minimal entity-relationship model with names, definitions, and examples.
3. Specify cardinality, required fields, optional fields, and validation rules.
4. Add provenance for every fact so imported data can be audited or corrected.
5. Design migration steps from current notes or data into the typed structure.
6. Provide sample records and queries that prove the ontology answers the target questions.

## Guardrails

- Avoid over-modeling; add types only when they improve retrieval, validation, or automation.
- Keep schemas local and portable unless the user selects a specific graph platform.
- Distinguish ontology terms from instance data.
- Preserve source links and confidence when converting messy text into structured facts.

## Outputs

- Typed schema or ontology draft.
- Entity and relationship glossary.
- Migration plan with validation checks.
- Example records and query patterns.

## Validation Checklist

- Each type supports a real user question.
- Required fields are justified and not excessive.
- Provenance and confidence are represented.
- Example records can be validated against the schema.

## Triggers

Keywords: ontology, knowledge graph, schema, typed memory, entities, relationships, controlled vocabulary, graph model, provenance.

Example requests:

- `Design a lightweight ontology for my agent memory.`
- `Use $work-productivity-ontology-typed-workflow-helper to turn these notes into typed graph records.`
- `Create validation rules for entities and relationships in this knowledge base.`
