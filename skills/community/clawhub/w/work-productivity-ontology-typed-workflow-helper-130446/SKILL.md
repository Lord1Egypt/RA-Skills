---
name: work-productivity-ontology-typed-workflow-helper
description: >-
  Design typed ontology and knowledge-graph workflows for agent memory, structured notes, domain models, and retrieval systems. Use when a user needs entity types, relations, schemas, examples, validation rules, migration plans, or query patterns.
---

# Typed Ontology Workflow Helper

## Requirement

Use this skill when a user needs to turn loose notes, agent memory, business objects, or research material into a typed ontology that can be validated, queried, and maintained.

The validated demand came from popular ontology-style ClawHub workflows and corroborating developer requests around structured knowledge, composable memory, and safer agent workflows. This skill provides an explicit modeling process instead of a generic productivity checklist.

## Workflow

1. Define the domain boundary, users, decisions the ontology must support, and examples of source material.
2. Extract candidate entity types, relation types, attributes, identifiers, and event types from the examples.
3. Separate stable ontology concepts from project-specific labels, temporary tags, and free-text notes.
4. Produce a typed schema: type names, required fields, optional fields, relation cardinality, constraints, and provenance fields.
5. Add examples for each type, including at least one invalid example that explains what should be rejected.
6. Design maintenance rules for merge/dedupe, versioning, migration, naming, and conflict resolution.
7. Provide query patterns or retrieval prompts that use the ontology without leaking implementation details to end users.

## Expected Outputs

- A compact ontology specification with entity and relation definitions.
- JSON Schema, YAML schema, table definitions, or TypeScript types when useful.
- Example records and validation checks.
- Migration and governance notes for maintaining the model over time.

## Validation

- Every relation has a source type, target type, meaning, and cardinality.
- The schema includes identifiers and provenance so records can be merged safely.
- Examples demonstrate real use, edge cases, and rejection criteria.
- The model stays small enough to operate locally in notes, files, SQLite, or a lightweight graph store.

## Triggers

Keywords: `ontology`, `typed knowledge`, `knowledge graph`, `agent memory`, `schema`, `entity relation`, `structured notes`, `retrieval model`.

Example trigger sentences:

- `Use $work-productivity-ontology-typed-workflow-helper to design a schema for my agent memory.`
- `Turn these messy project notes into typed entities and relations.`
- `Create validation rules for this lightweight knowledge graph.`
