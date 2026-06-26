---
title: Hierarchical Structures
---

## Hierarchical Structures

Model parent-child relationships to enable permission inheritance through hierarchies. Store parent links only where structurally necessary and propagate roles through the chain — never duplicate a parent relation at every level.

**Example (folder hierarchy):**

```dsl.openfga
model
  schema 1.1

type user

type organization
  relations
    define member: [user]
    define admin: [user]

type folder
  relations
    define organization: [organization]
    define parent_folder: [folder]
    define org_admin: admin from organization or org_admin from parent_folder
    define owner: [user] or owner from parent_folder
    define editor: [user] or owner or editor from parent_folder
    define viewer: [user] or editor or viewer from parent_folder or member from organization
    define can_delete: owner or org_admin

type document
  relations
    define parent_folder: [folder]
    define org_admin: org_admin from parent_folder
    define owner: [user] or owner from parent_folder
    define editor: [user] or owner or editor from parent_folder
    define viewer: [user] or editor or viewer from parent_folder
    define can_delete: owner or org_admin
```

**Tuples for nested structure:**

```yaml
# Organization setup
- user: user:cto
  relation: admin
  object: organization:acme

# Root folder belongs to organization
- user: organization:acme
  relation: organization
  object: folder:root

# Nested folder structure — only parent links, no organization tuple needed
- user: folder:root
  relation: parent_folder
  object: folder:engineering

- user: folder:engineering
  relation: parent_folder
  object: folder:backend

# Document in nested folder — only parent link needed
- user: folder:backend
  relation: parent_folder
  object: document:api-spec
```

The CTO can delete all documents in all nested folders because `org_admin` chains through the parent hierarchy automatically. No `organization` tuple is needed on `folder:engineering`, `folder:backend`, or `document:api-spec`.

**Key patterns:**
- Store the parent link to the root type (e.g. `organization`) only on the **top-level** object in the hierarchy
- Child types reference their **immediate parent**, not the root: `define parent_folder: [folder]`
- Propagate parent-level roles as local computed relations: `define org_admin: org_admin from parent_folder`
- Permissions use the local computed relation: `can_delete: owner or org_admin`
- Each level adds its own direct grants with `[user]`

**Incorrect (duplicating the parent at every level):**

```dsl.openfga
type document
  relations
    define organization: [organization]   # WRONG: duplicates parent link
    define parent_folder: [folder]
    define can_delete: owner or admin from organization
```

```yaml
# WRONG: requires an organization tuple on every single object
- user: organization:acme
  relation: organization
  object: document:api-spec
```

This forces you to write an `organization` tuple for every object in the system, which defeats the purpose of having a hierarchy.

**Correct (chain through the hierarchy):**

```dsl.openfga
type document
  relations
    define parent_folder: [folder]
    define org_admin: org_admin from parent_folder  # chains up automatically
    define can_delete: owner or org_admin
```

```yaml
# Only the parent link is needed — org_admin resolves through the chain
- user: folder:backend
  relation: parent_folder
  object: document:api-spec
```

**Propagate all relevant parent roles, not just org-level ones:**

Any role defined on a parent type that is meaningful to child resources should be chained down. This applies to roles like `owner`, `head`, `manager`, `lead` — not just organization-level roles like `admin`.

**Incorrect (parent role forgotten on child types):**

```dsl.openfga
type department
  relations
    define head: [user]
    define can_view: head

type job
  relations
    define department: [department]
    define recruiter: [user]
    define can_view: recruiter              # department head has no visibility!
```

The department head can see the department but is locked out of jobs within it.

**Correct (chain the parent role down):**

```dsl.openfga
type department
  relations
    define head: [user]
    define can_view: head

type job
  relations
    define department: [department]
    define department_head: head from department
    define recruiter: [user]
    define can_view: department_head or recruiter
```

**Prefer inheriting parent permissions when semantics match:**

If a child resource should grant the same permission to everyone who already has that permission on its parent, prefer reusing the parent's permission directly instead of re-listing the parent roles one by one.

This applies to any permission, not just `can_edit`. Common examples include `can_view`, `can_edit`, `can_delete`, `can_approve`, `can_publish`, and `can_share`.

**More verbose than necessary:**

```dsl.openfga
type campaign
  relations
    define owner: [user]
    define org_campaign_manager: campaign_manager from organization
    define org_admin: admin from organization
    define can_delete: org_admin
    define can_edit: owner or org_campaign_manager or can_delete

type ad_group
  relations
    define campaign: [campaign]
    define owner: [user]
    define campaign_owner: owner from campaign
    define org_campaign_manager: org_campaign_manager from campaign
    define org_admin: org_admin from campaign
    define can_delete: org_admin
    define can_edit: owner or campaign_owner or org_campaign_manager or can_delete
```

  **More succinct (`can_edit` example):**

```dsl.openfga
type campaign
  relations
    define owner: [user]
    define org_campaign_manager: campaign_manager from organization
    define org_admin: admin from organization
    define can_delete: org_admin
    define can_edit: owner or org_campaign_manager or can_delete

type ad_group
  relations
    define campaign: [campaign]
    define owner: [user]
    define can_edit: owner or can_edit from campaign
```

This keeps the child permission aligned with the parent and avoids duplicating the parent's edit rules.

The same pattern works for other permissions when the semantics match:

```dsl.openfga
type folder
  relations
    define parent_folder: [folder]
    define viewer: [user]
    define can_view: viewer

type document
  relations
    define parent_folder: [folder]
    define viewer: [user]
    define can_view: viewer or can_view from parent_folder
```

Here, `document#can_view` inherits `folder#can_view` directly because the parent and child share the same viewing semantics.

**Use this only when the child and parent truly share the same permission semantics:**

If the child has different semantics for that permission, keep the child permission explicit. For example, if the child should be editable by the parent owner and managers but not by the child owner, or if the child adds extra editors like `creator`, then `can_edit from parent` may be too broad or too narrow. The same applies to other permissions: `can_view from parent` is only correct when the child's view policy should match the parent's view policy.

**Include parent roles in concentric role hierarchies:**

When a parent type defines an `owner` or similar role, include it in the child type's role hierarchy so it cascades automatically:

```dsl.openfga
type store
  relations
    define owner: [user]
    define manager: [user] or owner           # owner is a manager
    define staff: [user] or manager           # manager is staff

type product
  relations
    define store: [store]
    define can_edit: manager from store        # owner gets access via manager
```

This is better than chaining `owner` separately because it uses the existing concentric role chain — the owner automatically gets staff and manager access to all child resources.

**Unified parent relation for multi-type hierarchies:**

When a type can appear in multiple hierarchies — or its parent can be one of several types — use a single `parent` relation with multiple type restrictions instead of separate relations for each parent type. This lets all role and permission chains use one `X from parent` expression regardless of which type the parent actually is.

**Incorrect (separate relations per parent type):**

```dsl.openfga
type folder
  relations
    define drive: [drive]
    define parent_folder: [folder]
    define organization_admin: organization_admin from drive or organization_admin from parent_folder
    define owner: [user] or owner from parent_folder
    define writer: [user, group#member] or owner or writer from parent_folder
    define reader: [user, group#member] or writer or reader from parent_folder or reader from drive
```

Every chain must reference both `drive` and `parent_folder`, making the model verbose and error-prone — it's easy to forget one of the two sources when adding a new role.

**Correct (single parent relation with multiple allowed types):**

```dsl.openfga
type folder
  relations
    define parent: [drive, folder]
    define organization_admin: organization_admin from parent
    define owner: [user] or owner from parent
    define writer: [user, group#member] or owner or writer from parent
    define reader: [user, group#member] or writer or reader from parent
```

Root folders link `parent` to a `drive`, nested folders link `parent` to another `folder`. All chains go through the single `parent` relation.

**When to use this pattern:**
- A type sits at a junction of two hierarchies (e.g., a folder can live inside a drive or inside another folder)
- Both parent types define the same roles or permissions that the child needs to chain (e.g., both `drive` and `folder` define `organization_admin`, `owner`, `writer`, `reader`)
- You want to avoid duplicating `X from drive or X from parent_folder` for every chained relation

**Requirements:**
- All allowed parent types must define the relations being chained (e.g., if `parent: [drive, folder]` and you write `owner from parent`, both `drive` and `folder` must define `owner`)
- Keep the relation name generic (`parent`) rather than type-specific (`parent_folder`, `drive`) since it now serves multiple types

**Audit checklist for hierarchies:**

When reviewing a model, for each parent-child relationship check:
1. Does the parent type define roles (owner, head, manager, lead, etc.)?
2. Are those roles relevant to the child resources?
3. Does the parent define permissions whose semantics should carry over to the child?
4. If yes, are those roles or permissions chained down as computed relations, reused via `X from parent`, or included in a concentric role chain?

**Benefits:**
- Single permission grant propagates to entire subtree
- Revoke access by removing one tuple
- No redundant tuples — parent roles resolve through the chain
- Parent roles like owner, head, manager are not accidentally excluded from child resources
- Natural mapping to file system and organizational structures
