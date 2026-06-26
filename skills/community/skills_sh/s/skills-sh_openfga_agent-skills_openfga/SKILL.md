---
name: openfga
description: OpenFGA authorization modeling best practices for defining types and relations, writing relationship tuples, deriving can_* permissions, applying type restrictions and usersets, and authoring .fga.yaml check/list_objects/list_users tests. Use when authoring, reviewing, or refactoring OpenFGA models, tuples, permissions, .fga files, .fga.yaml test files, or OpenFGA SDK integrations in JavaScript, TypeScript, Go, Python, Java, or .NET.
license: Apache-2.0
metadata:
  author: openfga
  version: "1.2.1"
---

# OpenFGA Best Practices

Use this skill to design and review OpenFGA models end to end: define types and relations, write tuples, derive `can_*` permissions, choose usersets and inheritance patterns, and validate behavior with `.fga.yaml` tests and CLI checks.

## Quick Start Example

Minimal model:

```fga
model
  schema 1.1

type user

type organization
  relations
    define admin: [user]
    define member: [user] or admin

type document
  relations
    define organization: [organization]
    define owner: [user]
    define can_edit: owner or admin from organization
    define can_view: can_edit or member from organization
```

Example tuples:

```text
organization:acme#admin@user:alice
document:roadmap#organization@organization:acme
document:roadmap#owner@user:bob
```

Example test targets:
- `check` that `user:alice` can view and edit `document:roadmap`
- `check` that `user:bob` can edit their own document
- `list_users` for `document:roadmap#can_view`
- `list_objects` for documents `user:alice` can edit

## How to Use

When a workflow step points to a rule ID, open the matching file in `references/` for detailed guidance and examples.

**Note:** SDK references (`sdk-*.md`) are only needed for integration tasks — skip them during pure model authoring and testing.

## Rule Index

### Core
| File | Description |
|------|-------------|
| `references/core-types.md` | Define types for entity classes |
| `references/core-relations.md` | Relations belong on object types |
| `references/core-tuples.md` | Relationship tuples as facts |
| `references/core-separation.md` | Model vs data separation |
| `references/core-schema-version.md` | Schema version |

### Relations
| File | Description |
|------|-------------|
| `references/relation-direct.md` | Direct relationships |
| `references/relation-indirect.md` | Indirect relationships with X from Y |
| `references/relation-concentric.md` | Concentric relationships |
| `references/relation-usersets.md` | Usersets for group-based access |
| `references/relation-conditions.md` | Conditional relationships |
| `references/relation-wildcards.md` | Wildcards for public access |
| `references/relation-wildcards-as-booleans.md` | Wildcards for boolean attributes |

### Design
| File | Description |
|------|-------------|
| `references/design-permissions.md` | Define permissions with can_ relations |
| `references/design-hierarchy.md` | Hierarchical structures |
| `references/design-organization.md` | Organization-level access |
| `references/design-create-on-parent.md` | Check create permissions on parent objects |
| `references/design-naming.md` | Naming conventions |
| `references/design-modules.md` | Modularize models (only when asked) |

### Roles
| File | Description |
|------|-------------|
| `references/roles-simple.md` | Simple static roles |
| `references/roles-static-combo.md` | Combining static and custom roles |
| `references/roles-assignments.md` | Role assignments for resource-specific roles |
| `references/roles-when-to-use.md` | When to use each role pattern |

### Optimization
| File | Description |
|------|-------------|
| `references/optimize-simplify.md` | Simplify models |
| `references/optimize-tuples.md` | Minimize tuple count |
| `references/optimize-type-restrictions.md` | Type restrictions |

### Testing
| File | Description |
|------|-------------|
| `references/test-fga-yaml.md` | Structure tests in .fga.yaml |
| `references/test-check-assertions.md` | Check assertions |
| `references/test-list-objects.md` | List objects tests |
| `references/test-list-users.md` | List users tests |
| `references/test-conditions.md` | Testing conditions |
| `references/test-cli.md` | OpenFGA CLI usage |
| `references/workflow-validate.md` | Always validate models |

### SDKs (for integration tasks only)
| File | Description |
|------|-------------|
| `references/sdk-javascript.md` | JavaScript/TypeScript SDK |
| `references/sdk-go.md` | Go SDK |
| `references/sdk-python.md` | Python SDK |
| `references/sdk-java.md` | Java SDK |
| `references/sdk-dotnet.md` | .NET SDK |

## Recommended Workflow

1. Model the resource graph.
  Define types, direct relations, inheritance edges, and `can_*` permissions.
  Rules to check first: `core-*`, `relation-*`, `design-permissions`, `design-hierarchy`.

2. Add tuples and test intent.
  Add representative tuples and cover expected behavior with `check`, `list_objects`, and `list_users` tests.
  Rules to check next: `core-tuples`, `test-fga-yaml`, `test-check-assertions`, `test-list-objects`, `test-list-users`.

3. Review parent-child creation and deletion paths.
  Verify each parent -> child edge has create permissions on the parent and that no child permission is directly grantable unless intended.
  Rules to check: `design-create-on-parent`, `relation-direct`, `design-permissions`.

4. Simplify before removing schema.
  Before deleting any type or relation, confirm it is not referenced by permissions, tuples, or tests.
  If a simplification breaks a reference: restore the relation or update the model/tests, then re-run this step.
  Rules to check: `optimize-simplify`, `optimize-tuples`, `optimize-type-restrictions`.

5. Validate the model.
  Run:

```bash
fga model validate --file stores/<store>/model.fga
```

  If validation fails: read the reported relation or type errors, fix the model, and re-run validation before continuing.

6. Run the store tests.
  Run:

```bash
fga model test --tests stores/<store>/store.fga.yaml
```

  If tests fail: update tuples, assertions, or permission definitions, then re-run tests until all checks and list queries pass.

7. Only then finalize delivery.
  For touched stores, finish only after validation and tests are green.
  Final rule to check: `workflow-validate`.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
