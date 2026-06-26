---
title: Organization-Level Access
---

## Organization-Level Access

Model organization membership and propagate access to owned resources. When a hierarchy exists, store the parent link (e.g. `organization`) only on the top-level type and chain roles down through local computed relations — never duplicate the parent relation on every child type.

**Single-level model (no hierarchy):**

When there is only one resource type directly under the parent, a direct `organization` relation is fine:

```dsl.openfga
model
  schema 1.1

type user

type organization
  relations
    define member: [user]
    define admin: [user]

type project
  relations
    define organization: [organization]
    define owner: [user] or admin from organization
    define editor: [user] or owner
    define viewer: [user] or editor or member from organization
```

In single-level models, keep parent-role references inline (for example, `admin from organization`) unless a child type needs to inherit that role. Only introduce computed aliases like `org_admin` when they are required for chaining into child types.

**Tuples:**

```yaml
# Organization membership
- user: user:anne
  relation: admin
  object: organization:acme

- user: user:bob
  relation: member
  object: organization:acme

# Project belongs to organization
- user: organization:acme
  relation: organization
  object: project:website
```

**Access results:**
- Anne (admin): can own, edit, and view the project
- Bob (member): can view the project
- All through organization membership

**Rule of thumb:**
- No child type depends on this type's parent role: keep `admin from organization` inline.
- Child types must inherit this role through the parent: define `org_admin` (or equivalent) on the parent and chain it on children.

**Multi-level model (hierarchy of types):**

When child types exist below the top-level type, chain the parent roles down — don't add a direct `organization` relation on every child.

```dsl.openfga
type organization
  relations
    define member: [user]
    define admin: [user]

type project
  relations
    define organization: [organization]
    define org_admin: admin from organization
    define org_member: member from organization
    define owner: [user] or org_admin
    define viewer: [user] or owner or org_member

type task
  relations
    define project: [project]
    define org_admin: org_admin from project
    define assignee: [user]
    define can_view: assignee or viewer from project
    define can_delete: org_admin
```

**Incorrect (duplicating the parent on child types):**

```dsl.openfga
type task
  relations
    define organization: [organization]   # WRONG: duplicates parent
    define project: [project]
    define can_delete: admin from organization
```

```yaml
# WRONG: must write an organization tuple for every task
- user: organization:acme
  relation: organization
  object: task:fix-bug
```

**Correct tuples for the multi-level model:**

```yaml
# Organization on the top-level type only
- user: organization:acme
  relation: organization
  object: project:website

# Child types only need their immediate parent link
- user: project:website
  relation: project
  object: task:fix-bug
```

The `org_admin` role resolves through: `task` → `project` → `organization` automatically.

**Extended pattern with teams:**

```dsl.openfga
type team
  relations
    define organization: [organization]
    define member: [user]

type project
  relations
    define organization: [organization]
    define team: [team]
    define org_member: member from organization
    define viewer: [user] or member from team or org_member
```

**Multi-tenant isolation:**

```dsl.openfga
type organization
  relations
    define member: [user]

type resource
  relations
    define organization: [organization]
    # Only org members can have any access
    define viewer: member from organization
```

This ensures resources are only visible within their organization.
