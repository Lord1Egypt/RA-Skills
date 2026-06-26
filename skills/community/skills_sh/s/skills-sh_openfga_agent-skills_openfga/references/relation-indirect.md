---
title: Indirect Relationships with X from Y
---

## Indirect Relationships with X from Y

The `X from Y` pattern grants access through an intermediary object, enabling hierarchical permissions.

**Incorrect (requires tuples on every document):**

```dsl.openfga
type folder
  relations
    define viewer: [user]

type document
  relations
    define viewer: [user]
```

Each document needs its own viewer tuples even if they're in the same folder.

**Correct (inherit from parent folder):**

```dsl.openfga
type folder
  relations
    define viewer: [user]

type document
  relations
    define parent_folder: [folder]
    define viewer: [user] or viewer from parent_folder
```

**Tuples:**

```yaml
# Grant folder access once
- user: user:anne
  relation: viewer
  object: folder:engineering

# Link documents to folder
- user: folder:engineering
  relation: parent_folder
  object: document:spec
- user: folder:engineering
  relation: parent_folder
  object: document:design
```

Anne can view all documents in the engineering folder with just one permission tuple.

**Common patterns:**
- `viewer from parent_folder` - Folder inheritance
- `admin from organization` - Parent-level admin access (on the top-level type)
- `org_admin from parent_folder` - Chaining a parent role through a hierarchy
- `member from team` - Team membership propagation

**Chain parent roles through computed relations:**

When a hierarchy has multiple levels, avoid repeating `admin from organization` on every child type. Define a local computed relation only when that role must be propagated to child types.

If there is no child type consuming the role, keep it inline in permissions (for example, `can_delete: admin from organization`).

When child types do need that role, define a local computed relation that chains up through the parent:

```dsl.openfga
type organization
  relations
    define admin: [user]

type project
  relations
    define organization: [organization]
    define org_admin: admin from organization
    define can_delete: org_admin

type task
  relations
    define project: [project]
    define org_admin: org_admin from project   # chains through parent
    define can_delete: org_admin
```

This way, `task` doesn't need its own `organization` relation or tuple — it resolves the parent role by traversing up: `task` → `project` → `organization`.

**Propagate all relevant parent roles, not just org-level ones:**

The chaining pattern applies to any role on a parent type that is relevant to child resources — not just organization-level roles like `admin`. Roles like `owner`, `head`, `manager`, and `lead` should also be chained:

```dsl.openfga
type department
  relations
    define head: [user]

type job
  relations
    define department: [department]
    define department_head: head from department   # chains the head role
    define can_view: department_head or recruiter
```

**Audit rule:** for each parent-child relationship, check if the parent defines roles that are meaningful to children. If so, chain them down as computed relations.

**Benefits:**
- Dramatically reduces tuple count
- Simplifies permission management
- Enables revoking access by deleting a single tuple
- No redundant parent tuples on child objects
- Parent roles like owner, head, manager are not accidentally excluded from child resources
