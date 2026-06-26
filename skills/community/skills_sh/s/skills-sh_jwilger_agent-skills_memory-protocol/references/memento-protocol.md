# Memento MCP Protocol Reference

Detailed guidance for the Memento MCP knowledge graph approach described in
`memory-protocol` SKILL.md. Use this when Memento MCP tools are available
(`mcp__memento__*`).

---

## Entity Types

| Type | Use for |
|------|---------|
| `debugging_insight` | Non-obvious error solutions, workarounds for tool bugs, timeout fixes, env quirks |
| `architecture_decision` | Design choices and their rationale (why X over Y) |
| `project_convention` | Patterns or rules discovered during work (naming, structure, formatting) |
| `user_preference` | Workflow, style, or tooling preferences expressed by the user |
| `tool_quirk` | Unexpected behavior of CLIs, build tools, test runners, external services |
| `test_pattern` | Effective test structures, helpers, or strategies for this codebase |
| `domain_concept` | Domain-specific terminology, rules, or invariants |
| `feature_implementation` | How a particular feature is built — location, approach, key files |

---

## Observation Format

Each observation must be a **complete, self-contained statement** — readable
without the entity name or other observations as context.

**Project-specific observation:**
```
Project: <name> | Path: <path> | Scope: PROJECT_SPECIFIC | Date: YYYY-MM-DD | <insight>
```

**General (cross-project) observation:**
```
Scope: GENERAL | Date: YYYY-MM-DD | <insight>
```

**For `debugging_insight` entities, always include:**
- The error message or symptom (exact text when possible)
- The root cause
- The fix or workaround taken
- Any conditions that trigger the issue

**Example observation:**
```
Project: TaskFlow | Path: /home/user/projects/taskflow | Scope: PROJECT_SPECIFIC | Date: 2026-01 | cargo test times out after 60s when integration tests run in parallel; fix: set RUST_TEST_THREADS=1 in .cargo/config.toml
```

---

## Relationship Types

| Type | Use for |
|------|---------|
| `implements` | Entity A is a concrete realization of entity B |
| `extends` | Entity A adds to or builds on entity B |
| `depends_on` | Entity A requires entity B to function |
| `discovered_during` | Entity A was found while working on task/feature B |
| `contradicts` | Entity A conflicts with or disproves entity B |
| `supersedes` | Entity A replaces or makes entity B obsolete |
| `validates` | Entity A confirms or supports entity B |
| `part_of` | Entity A is a component of the larger entity B |
| `related_to` | Entity A and B are related but without a stronger typed relationship |
| `derived_from` | Entity A was derived or inferred from entity B |

Always create at least one relationship after creating or updating an entity.
When no strong typed relationship applies, use `related_to`.

---

## Relationship Traversal Strategy

When `mcp__memento__open_nodes` returns entities with `relations`, traverse
them selectively:

| Relation type | Follow? | Why |
|---------------|---------|-----|
| `supersedes` | Always | The newer entity has more accurate information |
| `contradicts` | Always | Understand the conflict before proceeding |
| `extends` | Often | May contain additional relevant context |
| `depends_on` | Sometimes | Useful if the dependency itself has known quirks |
| `discovered_during` | Rarely | Usually provides only historical context |
| `related_to` | Sometimes | If the task is directly relevant |

Stop traversing when returned entities are no longer relevant to the current
task. Depth of 2–3 hops is usually sufficient.

---

## Examples

### Create a new entity

```
mcp__memento__create_entities([{
  name: "Cargo Test Timeout Fix TaskFlow 2026-01",
  entityType: "debugging_insight",
  observations: [
    "Project: TaskFlow | Path: /home/user/projects/taskflow | Scope: PROJECT_SPECIFIC | Date: 2026-01-15 | cargo test times out after 60s when integration tests run concurrently; root cause: shared SQLite file lock contention; fix: RUST_TEST_THREADS=1 in .cargo/config.toml"
  ]
}])
```

Then immediately create a relationship:

```
mcp__memento__create_relations([{
  from: "Cargo Test Timeout Fix TaskFlow 2026-01",
  to: "TaskFlow CI Configuration 2025-12",
  relationType: "part_of"
}])
```

### Add observations to an existing entity

When search returns a relevant entity, extend it rather than duplicating:

```
mcp__memento__add_observations([{
  entityName: "Cargo Test Timeout Fix TaskFlow 2026-01",
  contents: [
    "Project: TaskFlow | Path: /home/user/projects/taskflow | Scope: PROJECT_SPECIFIC | Date: 2026-02-03 | confirmed: timeout also occurs in CI; RUST_TEST_THREADS=1 already set in .cargo/config.toml resolves it in GitHub Actions as well"
  ]
}])
```

### Recall and traverse

```
# 1. Search
mcp__memento__semantic_search({ query: "cargo test timeout integration", limit: 10 })

# 2. Open relevant results by name
mcp__memento__open_nodes(["Cargo Test Timeout Fix TaskFlow 2026-01"])

# 3. Check relations — if it has a `supersedes` or `contradicts` relation, open those too
mcp__memento__open_nodes(["<related entity name>"])

# 4. Apply the recalled knowledge; update or extend entities if new information emerged
```
