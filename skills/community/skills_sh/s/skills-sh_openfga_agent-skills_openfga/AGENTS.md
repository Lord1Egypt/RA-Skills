# OpenFGA Best Practices

**Version 1.0.0**
OpenFGA Community
April 2026

> **Note:**
> This document is mainly for agents and LLMs to follow when authoring,
> generating, or refactoring OpenFGA authorization models. Humans
> may also find it useful, but guidance here is optimized for automation
> and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive guide for authoring OpenFGA authorization models, designed for AI agents and LLMs. Covers core concepts, relationship patterns, testing methodologies, custom roles, and model optimization. Each section includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific guidance to ensure correct authorization modeling.

---

## Table of Contents

1. [Core](#1-core)
   - 1.1 [Define Types for Entity Classes](#11-define-types-for-entity-classes)
   - 1.2 [Relations Belong on Object Types](#12-relations-belong-on-object-types)
   - 1.3 [Relationship Tuples as Facts](#13-relationship-tuples-as-facts)
   - 1.4 [Model vs Data Separation](#14-model-vs-data-separation)
   - 1.5 [Schema Version](#15-schema-version)
2. [Relations](#2-relations)
   - 2.1 [Direct Relationships](#21-direct-relationships)
   - 2.2 [Indirect Relationships with X from Y](#22-indirect-relationships-with-x-from-y)
   - 2.3 [Concentric Relationships](#23-concentric-relationships)
   - 2.4 [Usersets for Group-Based Access](#24-usersets-for-group-based-access)
   - 2.5 [Conditional Relationships](#25-conditional-relationships)
   - 2.6 [Wildcards for Public Access](#26-wildcards-for-public-access)
   - 2.7 [Wildcards for boolean attributes](#27-wildcards-for-boolean-attributes)
3. [Design](#3-design)
   - 3.1 [Define Permissions with can_ Relations](#31-define-permissions-with-can_-relations)
   - 3.2 [Hierarchical Structures](#32-hierarchical-structures)
   - 3.3 [Organization-Level Access](#33-organization-level-access)
   - 3.4 [Check Create Permissions on Parent Objects](#34-check-create-permissions-on-parent-objects)
   - 3.5 [Naming Conventions](#35-naming-conventions)
   - 3.6 [Modularize your modules with 'modules'](#36-modularize-your-modules-with-modules)
4. [Roles](#4-roles)
   - 4.1 [Simple Static Roles](#41-simple-static-roles)
   - 4.2 [Combining Static and Custom Roles](#42-combining-static-and-custom-roles)
   - 4.3 [Role Assignments for Resource-Specific Roles](#43-role-assignments-for-resource-specific-roles)
   - 4.4 [When to Use Each Role Pattern](#44-when-to-use-each-role-pattern)
5. [Optimization](#5-optimization)
   - 5.1 [Simplify Models](#51-simplify-models)
   - 5.2 [Minimize Tuple Count](#52-minimize-tuple-count)
   - 5.3 [Type Restrictions](#53-type-restrictions)
6. [Testing](#6-testing)
   - 6.1 [Structure Tests in .fga.yaml](#61-structure-tests-in-fgayaml)
   - 6.2 [Check Assertions](#62-check-assertions)
   - 6.3 [List Objects Tests](#63-list-objects-tests)
   - 6.4 [List Users Tests](#64-list-users-tests)
   - 6.5 [Testing Conditions](#65-testing-conditions)
   - 6.6 [OpenFGA CLI Usage](#66-openfga-cli-usage)
   - 6.7 [Always Validate Models](#67-always-validate-models)
7. [SDKs (for integration tasks only)](#7-sdks-for-integration-tasks-only)
   - 7.1 [JavaScript/TypeScript SDK](#71-javascripttypescript-sdk)
   - 7.2 [Go SDK](#72-go-sdk)
   - 7.3 [Python SDK](#73-python-sdk)
   - 7.4 [Java SDK](#74-java-sdk)
   - 7.5 [.NET SDK](#75-net-sdk)

---

## 1. Core

Understanding core concepts is fundamental to creating correct and maintainable authorization models.

### 1.1 Define Types for Entity Classes

Types define classes of objects in your system. Every entity that participates in authorization should have a type.

**Incorrect (missing types):**

```dsl.openfga
model
  schema 1.1

type user

type document
  relations
    define owner: [user]
    define viewer: [user]
```

This model is missing types for organizational structure that documents might belong to.

**Correct (comprehensive types):**

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
    define owner: [user]
    define viewer: [user]

type document
  relations
    define parent_folder: [folder]
    define organization: [organization]
    define owner: [user]
    define viewer: [user]
```

Identify all relevant entities: users, resources, organizational units, groups, and any containers.

### 1.2 Relations Belong on Object Types

Relations are defined on the types that represent resources being accessed, not on user types.

**Incorrect (relations on user type):**

```dsl.openfga
model
  schema 1.1

type user
  relations
    define owns_document: [document]  # Wrong! Relations go on the resource
```

**Correct (relations on resource type):**

```dsl.openfga
model
  schema 1.1

type user

type document
  relations
    define owner: [user]  # Correct! Defined on the resource
```

Ask "Can user U perform action A on object O?" — the relation belongs on type O.

### 1.3 Relationship Tuples as Facts

Relationship tuples represent facts about who has what relationship to what object. They are the data that brings your model to life.

**Model defines possibilities:**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
```

**Tuples establish facts:**

```yaml
tuples:
  - user: user:anne
    relation: owner
    object: document:roadmap
  - user: user:bob
    relation: editor
    object: document:roadmap
```

Without tuples, authorization checks will fail because the model only defines what is *possible*, not what *currently exists*.

**Key distinction:**
- Model = static schema defining possible relationships
- Tuples = dynamic data representing actual relationships

### 1.4 Model vs Data Separation

The authorization model (schema) is static and defines structure. Relationship tuples (data) are dynamic and change frequently.

**Model characteristics:**
- Immutable; each modification creates a new version
- Changes rarely; only when product features change
- Defines the *possible* relationships

**Tuple characteristics:**
- Mutable; written and deleted as application state changes
- Changes frequently; as users gain/lose access
- Represents the *actual* relationships

**Example:**

```dsl.openfga
# Model (changes rarely)
type document
  relations
    define owner: [user]
    define viewer: [user] or owner
```

```yaml
# Tuples (change frequently)
- user: user:anne
  relation: owner
  object: document:roadmap
# This tuple can be added/removed as permissions change
```

This separation enables efficient permission evaluation and decouples core logic changes from specific user permission modifications.

### 1.5 Schema Version

Always use schema version 1.1 to access all OpenFGA features.

**Incorrect (missing schema version):**

```dsl.openfga
model

type user

type document
  relations
    define owner: [user]
```

**Correct (explicit schema version):**

```dsl.openfga
model
  schema 1.1

type user

type document
  relations
    define owner: [user]
```

Schema 1.1 enables conditions, intersection, exclusion, and other advanced features.

---
## 2. Relations

The building blocks for expressing authorization logic in OpenFGA.

### 2.1 Direct Relationships

Direct relationships require explicit relationship tuples. Use type restrictions to control what can be directly assigned.

**Type restriction patterns:**

| Pattern | Meaning | Example |
|---------|---------|---------|
| `[user]` | Only individual users | `define owner: [user]` |
| `[user, team#member]` | Users or team members | `define editor: [user, team#member]` |
| `[organization]` | Only organizations | `define parent: [organization]` |

**Example:**

```dsl.openfga
type document
  relations
    define owner: [user]
```

**Tuple to grant access:**

```yaml
- user: user:anne
  relation: owner
  object: document:roadmap
```

Without a tuple, user:anne has no owner relationship to document:roadmap.

**Common mistake:** Forgetting that direct relationships require explicit tuples. The model only defines what is *possible*.

### 2.2 Indirect Relationships with X from Y

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

### 2.3 Concentric Relationships

Use `or` to create nested permissions where one relation implies another. This applies both to roles and to `can_*` permissions.

### Concentric roles

**Incorrect (redundant tuples required):**

```dsl.openfga
type document
  relations
    define editor: [user]
    define viewer: [user]
```

This requires separate tuples for both editor and viewer access.

**Correct (editors inherit viewer access):**

```dsl.openfga
type document
  relations
    define editor: [user]
    define viewer: [user] or editor
```

Now editors automatically have viewer access without additional tuples.

**Typical hierarchy:**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user] or owner
    define viewer: [user] or editor
```

Owners can edit and view. Editors can view. Each level inherits from the one above.

### Concentric permissions

Apply the same principle to `can_*` permissions: each permission should reference the next more-powerful permission instead of repeating the same roles. Order permissions from most restrictive (most powerful) first, then build less restrictive ones on top.

**Incorrect (repeating roles across permissions):**

```dsl.openfga
type campaign
  relations
    define owner: [user]
    define org_campaign_manager: campaign_manager from organization
    define org_analyst: analyst from organization
    define org_admin: admin from organization
    define can_view: owner or org_analyst or org_campaign_manager or org_admin
    define can_edit: owner or org_campaign_manager or org_admin
    define can_delete: org_admin
```

`org_campaign_manager` and `org_admin` are repeated in both `can_view` and `can_edit`. If you add a new role that can edit, you must remember to add it to `can_view` too.

**Correct (each permission references the next more-powerful one):**

```dsl.openfga
type campaign
  relations
    define owner: [user]
    define org_campaign_manager: campaign_manager from organization
    define org_analyst: analyst from organization
    define org_admin: admin from organization
    define can_delete: org_admin
    define can_edit: owner or org_campaign_manager or can_delete
    define can_view: org_analyst or can_edit
```

`can_view` includes everyone who `can_edit`, which includes everyone who `can_delete`. Each role appears exactly once.

**Ordering rule:** define the most restrictive permission first (`can_delete`), then build up:

```
can_delete  →  can_edit  →  can_view
(strongest)    (medium)     (weakest)
```

Less restrictive permissions reference more restrictive ones via `or can_<more_restrictive>`, adding only the roles unique to that level.

### Include parent roles in concentric role chains

When a parent type defines a role like `owner`, include it in the child type's concentric role hierarchy rather than chaining it separately. This ensures the role cascades to all permissions automatically.

**Incorrect (owner excluded from the role chain):**

```dsl.openfga
type store
  relations
    define owner: [user]
    define manager: [user] or store_manager from organization
    define staff: [user] or manager

type product
  relations
    define store: [store]
    define can_edit: manager from store        # owner has no access!
```

The store owner can't edit products because `owner` doesn't feed into `manager`.

**Correct (owner included in the role chain):**

```dsl.openfga
type store
  relations
    define owner: [user]
    define manager: [user] or owner or store_manager from organization
    define staff: [user] or manager

type product
  relations
    define store: [store]
    define can_edit: manager from store        # owner gets access via manager
```

Now the owner is a manager, which is staff, so `manager from store` and `staff from store` on child types automatically include the owner.

**Benefits:**
- Fewer tuples needed
- Consistent permission semantics
- Easier to reason about access levels
- Each role appears exactly once — no risk of forgetting to add a role at every level
- Adding a new role requires changing only one permission
- Parent roles like owner cascade through concentric chains to all child resources

### 2.4 Usersets for Group-Based Access

Usersets (`type#relation`) represent collections of users, enabling group-based access control.

**Syntax:** `type#relation` means "all users who have this relation to objects of this type"

**Example (team-based access):**

```dsl.openfga
type team
  relations
    define member: [user]

type document
  relations
    define editor: [user, team#member]
```

**Tuples:**

```yaml
# Add users to team
- user: user:anne
  relation: member
  object: team:engineering

- user: user:bob
  relation: member
  object: team:engineering

# Grant team access to document
- user: team:engineering#member
  relation: editor
  object: document:roadmap
```

Both Anne and Bob can edit the roadmap through their team membership.

**Important:** `team#member` means "members of a specific team". It does NOT mean "must be a team member to be an editor". Only use it when assigning access to a group.

**Common mistake:**

```dsl.openfga
# This does NOT mean "only team members can be editors"
define editor: [team#member]

# It means "you can assign all members of a specific team as editors"
```

### 2.5 Conditional Relationships

Conditions use CEL (Common Expression Language) to add runtime context to authorization decisions.

**Example (time-based access):**

```dsl.openfga
model
  schema 1.1

type user

type organization
  relations
    define admin: [user with non_expired_grant]

condition non_expired_grant(current_time: timestamp, grant_time: timestamp, grant_duration: duration) {
  current_time < grant_time + grant_duration
}
```

**Important:** Conditions must be defined at the end of the model, after all type definitions.

**Conditional tuple:**

```yaml
- user: user:peter
  relation: admin
  object: organization:acme
  condition:
    name: non_expired_grant
    context:
      grant_time: "2024-02-01T00:00:00Z"
      grant_duration: 1h
```

**Check with context:**

```yaml
check:
  - user: user:peter
    object: organization:acme
    context:
      current_time: "2024-02-01T00:10:00Z"
    assertions:
      admin: true  # Within the 1-hour window
```

**Common use cases:**
- Time-based access (expiring grants)
- IP-based restrictions
- Feature flags
- Attribute-based conditions

### 2.6 Wildcards for Public Access

Wildcards (`type:*`) grant access for all instances of a user type to a specific object.

**Example (public documents):**

```dsl.openfga
type document
  relations
    define viewer: [user, user:*]
```

**Tuple for public access:**

```yaml
- user: user:*
  relation: viewer
  object: document:public-readme
```

All users can view the public-readme document.

**Correct usage scenarios:**
- Public documentation
- Shared resources everyone should access
- Anonymous/guest access patterns

**Incorrect usage (avoid):**

```dsl.openfga
# Don't use wildcards as a shortcut for "any user can be assigned"
type document
  relations
    define editor: [user:*]  # Too permissive for editing
```

### 2.7 Wildcards for boolean attributes

Wildcards (`type:*`) grant access for all instances of a user type to a specific object. They can be used to simulate boolean attributes. 

**Example (feature entitlements):**

```dsl.openfga
type organization
  relations
    define member: [user]
    define feature_sso: [user:*] 
    define can_access_sso : feature_sso and member
```

Note that if the permission needs to check both for the 'boolean attribute' (feature_sso) and verify the user is a member of the organization.


**Tuples **

```yaml
- user: user:anne
  relation: member
  object: organization:acme

- user: user:*
  relation: feature_sso
  object: organization:acme
```

All members from the acme organization can access the 'feature_sso' feature.

**Correct usage scenarios:**
- Feature Flags
- Entitlements
- Boolean states ('enabled', 'active', 'published')

---
## 3. Design

Design patterns that lead to maintainable and correct authorization models.

### 3.1 Define Permissions with can_ Relations

Define specific permissions using `can_<action>` relations that cannot be directly assigned. Permissions should only reference roles and computed relations — never have direct type assignments like `[user]`.

**Incorrect (checking relations directly):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user] or owner
    define viewer: [user] or editor
```

Application checks `editor` relation but semantics are unclear.

**Correct (explicit permissions):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user] or owner
    define viewer: [user] or editor

    define can_view: viewer
    define can_edit: editor
    define can_delete: owner
    define can_share: owner
```

**Application code:**

```typescript
// Clear intent - checking specific permissions
await fga.check({ user, relation: 'can_view', object: doc })
await fga.check({ user, relation: 'can_edit', object: doc })
await fga.check({ user, relation: 'can_delete', object: doc })
```

**Never put direct type assignments on `can_*` relations:**

`can_*` relations are permissions — they answer "can this user do X?" They should only combine roles and other permissions, never accept direct tuple assignments.

**Incorrect (direct assignment on permission):**

```dsl.openfga
type product
  relations
    define store: [store]
    define can_view: [user] or staff from store     # WRONG: [user] on a permission
```

This blurs the line between roles and permissions. You can't tell from the model what role grants view access — it's an anonymous direct grant.

**Correct (named role for direct assignments):**

```dsl.openfga
type product
  relations
    define store: [store]
    define viewer: [user]                           # role that can be assigned
    define can_view: viewer or staff from store      # permission references the role
```

Now the model is clear: `viewer` is a role you assign, `can_view` is a permission you check. If you need to audit who can view a product, you can inspect the `viewer` role.

**Rule:** if a `can_*` relation needs `[user]` or `[type#relation]`, create a named role (e.g. `viewer`, `editor`, `participant`) and reference it from the permission instead.

**Benefits:**
- Clear separation between roles and permissions
- Permissions can combine multiple roles
- Easier to evolve without breaking applications
- Self-documenting model
- Roles are auditable — you can query who has a specific role

**Make permissions concentric:**

When multiple `can_*` permissions share roles, don't repeat them — reference the more powerful permission instead. Order from most restrictive first, and build less restrictive permissions on top:

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define parent_folder: [folder]
    define org_admin: org_admin from parent_folder

    # Most restrictive first
    define can_delete: owner or org_admin
    define can_edit: editor or can_delete
    define can_view: viewer or can_edit
```

**Incorrect (repeating roles):**

```dsl.openfga
    define can_view: owner or editor or viewer or org_admin
    define can_edit: owner or editor or org_admin
    define can_delete: owner or org_admin
```

**Correct (concentric references):**

```dsl.openfga
    define can_delete: owner or org_admin
    define can_edit: editor or can_delete
    define can_view: viewer or can_edit
```

Each role appears exactly once. Adding a new role that can edit only requires changing `can_edit` — `can_view` picks it up automatically.

**Reuse parent permissions when the child shares the same semantics:**

If a child resource should grant the same permission as its parent to the same set of users, prefer reusing the parent's permission directly with `can_<action> from <parent_relation>` instead of re-listing the parent roles on the child.

Example:

```dsl.openfga
type folder
  relations
    define viewer: [user]
    define can_view: viewer

type document
  relations
    define parent_folder: [folder]
    define viewer: [user]
    define can_view: viewer or can_view from parent_folder
```

This keeps the child permission aligned with the parent and avoids duplicating the parent's permission logic. For detailed guidance on when this is safe and when child semantics should stay explicit, see `references/design-hierarchy.md`.

### 3.2 Hierarchical Structures

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

### 3.3 Organization-Level Access

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

### 3.4 Check Create Permissions on Parent Objects

Creation permissions should usually live on the parent or container object, not on the leaf resource being created. If the child object does not exist yet, checking `can_create` on that child forces the application to invent an object identifier before authorization and makes the permission harder to reason about.

**Incorrect (create on the leaf object):**

```dsl.openfga
type organization
  relations
    define admin: [user]
    define accountant: [user]

type payment
  relations
    define organization: [organization]
    define can_create: accountant from organization or admin from organization
    define can_edit: can_create
```

This requires checking whether a user can create `payment:future-id`, even though that object is not real yet.

**Correct (create on the parent object):**

```dsl.openfga
type organization
  relations
    define admin: [user]
    define accountant: [user]
    define can_create_payment: accountant or admin

type payment
  relations
    define organization: [organization]
    define creator: [user]
    define can_edit: creator or accountant from organization or admin from organization
```

Now the application checks creation against the real parent object it already knows about:

```typescript
await fga.check({
  user,
  relation: 'can_create_payment',
  object: 'organization:acme',
})
```

**Another example with nested resources:**

```dsl.openfga
type store
  relations
    define manager: [user]
    define can_create_product: manager

type product
  relations
    define store: [store]
    define creator: [user]
    define can_edit: creator or can_create_product from store
```

**Rule:**
- Put create permissions on the object that contains or owns the new resource.
- Name them after the resource being created, for example `can_create_invoice`, `can_create_product`, or `can_create_report`.
- On the child resource, reference the parent-scoped create permission only if creators should also gain edit or manage rights after creation.

**Coverage checklist (required):**
1. Enumerate every parent -> child relation in the model.
2. For each pair, choose one:
   - Creation is enforced in OpenFGA: add `can_create_<child>` on the parent and test allow + deny cases.
   - Creation is enforced outside OpenFGA: document that assumption in tests or README.
3. Keep naming consistent: `can_create_room`, `can_create_reservation`, `can_create_diagnosis`, etc.

**Benefits:**
- Checks align with real objects that already exist
- No need to mint speculative child IDs just to authorize creation
- Cleaner API design for applications
- Better consistency across models with hierarchies

### 3.5 Naming Conventions

Use consistent naming conventions for clarity and maintainability.

**Types - use singular nouns in lowercase:**

```dsl.openfga
# Correct
type user
type document
type folder
type organization
type team
type project

# Incorrect
type Users      # No capitals
type documents  # Not plural
type FOLDER     # Not all caps
```

**Relations - use descriptive names:**

```dsl.openfga
type document
  relations
    # Roles (who someone is)
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define admin: [user]
    define member: [user]

    # Structural (relationships between objects)
    define parent_folder: [folder]
    define organization: [organization]
    define parent: [document]

    # Permissions (what someone can do)
    define can_view: viewer
    define can_edit: editor
    define can_delete: owner
    define can_share: owner
```

**Object identifiers - use meaningful, readable IDs:**

```yaml
# Good
- object: document:roadmap-2024
- object: organization:acme-corp
- object: folder:engineering-docs
- object: user:anne-smith

# Avoid
- object: document:12345      # Meaningless ID
- object: organization:org1   # Non-descriptive
- object: folder:f_001        # Cryptic
```

**Computed parent-role relations — prefix with the parent type name (when needed for child propagation):**

When a role must be propagated from a parent type to child types, name the local computed relation with a prefix matching the parent type:

```dsl.openfga
type project
  relations
    define organization: [organization]
    define org_admin: admin from organization           # "org_" prefix from "organization"
    define org_member: member from organization

type task
  relations
    define project: [project]
    define org_admin: org_admin from project             # same name, chains up
```

This makes it clear where the role originates and keeps names consistent across the hierarchy.

If no child type needs the role, do not create a computed alias just for naming. Use inline expressions such as `admin from organization` directly in permissions.

**Consistency guidelines:**
- Use snake_case for multi-word relations: `parent_folder`, `can_view`
- Use kebab-case for object IDs: `roadmap-2024`, `acme-corp`
- Prefix permissions with `can_`: `can_view`, `can_edit`, `can_delete`
- Use nouns for roles: `owner`, `editor`, `viewer`, `admin`
- Prefix computed parent-role relations with an abbreviation of the parent type: `org_admin`, `org_member`, `dept_head`

### 3.6 Modularize your modules with 'modules'

**CRITICAL**: Only do this when you are asked to modularize the model. By default, create models in a single file.

## Split the authorization model in modules

Create a module for each sub-domain an application. 

Define a 'core.fga' module with the types that should be used by all sub-domains (e.g. `organization`, `role`, `group`), and an individual '.fga' file for each sub-domain.

Create an 'fga.mod' file that includes all '.fga' files:

```yaml
schema: '1.2'
contents:
  - core.fga
  - wiki.fga
```

## Module Definition

Modules are stored in `.fga.` files and start with the `module` keyword

**core.fga**
```dsl.openfga
module core

type user

type organization
  relations
    define member: [user]
    define admin: [user]

type group
  relations
    define member: [user]
```

## Extending types from other modules

Each sub-domain frequently need to define top-level permission that are defined, for example, at the `organization` type. They can do by using the `extend type` syntax:

**wiki.fga**
```dsl.openfga
module wiki

extend type organization
  relations
    define can_create_space: admin


type space
  relations
    define organization: [organization]
    define can_view_pages: member from organization

type page
  relations
    define space: [space]
    define owner: [user]
```

- A single type can only be extended once per file
- The relations added must not already exist, or be part of another type extension

## Testing Models with Modules

When creating `.fga.yaml` files to test models that include modular models, you need to point to the `fga.mod` file:

```yaml
name: ModularDemo
model_file: ./fga.mod

tuples:
  - user: user:anne
    relation: admin
    object: organization:openfga
  - user: user:anne
    relation: admin
    object: project:openfga
tests:
  - name: Members can view projects
    check:
      - user: user:anne
        object: organization:openfga
        assertions:
          admin: true
          member: true
          can_create_space: true
```

---
## 4. Roles

Implement user-defined roles when applications need flexible permission structures.

### 4.1 Simple Static Roles

Always start with static roles defined in each type, unless you are asked to support custom-roles or user-defined roles

**Model:**

```dsl.openfga
model
  schema 1.1

type user

type organization
  relations
    define admin: [user]  # Static role
    define member: [user]  # Static role

type project
  relations
    define organization: [organization]
    define owner: [user]
    define editor: [user]
```

**Setting up a static role:**

```yaml
# 1. Define role permissions
- user: user:anne
  relation: admin
  object: organization:acme

- user: user:bob
  relation: admin
  object: project:website
```

**Use when:**
- Roles apply at the organization level
- Same role permissions everywhere
- Simple permission structure

### 4.2 Combining Static and Custom Roles

Combine pre-defined static roles with user-defined custom roles for practical authorization systems.

**Model:**

```dsl.openfga
model
  schema 1.1

type user

type role
  relations
    define assignee: [user]

type organization
  relations
    # Static roles - known at design time
    define owner: [user]
    define admin: [user] or owner
    define member: [user] or admin

    # Permissions: combine static roles and custom roles
    define can_manage_billing: [role#assignee] or owner
    define can_manage_members: [role#assignee] or admin
    define can_view_analytics: [role#assignee] or member
    define can_create_projects: [role#assignee] or member
```

**Static roles provide baseline permissions:**

```yaml
# Org owner has all permissions through static role
- user: user:founder
  relation: owner
  object: organization:acme

# Admin has member permissions through concentric relationship
- user: user:cto
  relation: admin
  object: organization:acme
```

**Custom roles extend for specific needs:**

```yaml
# Create a "billing-admin" custom role
- user: role:acme-billing-admin#assignee
  relation: can_manage_billing
  object: organization:acme

# Assign user to the custom role
- user: user:accountant
  relation: assignee
  object: role:acme-billing-admin
```

**Benefits:**
- Static roles handle common patterns (owner, admin, member)
- Custom roles allow organizational flexibility
- Clear separation of concerns
- Easier to understand and audit

**Recommendation:** Always define static roles for known, common access patterns. Use custom roles for organization-specific extensions.

### 4.3 Role Assignments for Resource-Specific Roles

For roles that can have different members on different levels of a resource hierarchy. DO NOT use this for top-level types like organizations.

**Model:**

```dsl.openfga
model
  schema 1.1

type user

type role
  relations
    define can_view_project: [user:*]
    define can_edit_project: [user:*]

type role_assignment
  relations
    define assignee: [user]
    define role: [role]

    define can_view_project: assignee and can_view_project from role
    define can_edit_project: assignee and can_edit_project from role

type organization
  relations
    define admin: [user]

type project
  relations
    define organization: [organization]
    define role_assignment: [role_assignment]

    define can_edit_project: can_edit_project from role_assignment or admin from organization
    define can_view_project: can_view_project from role_assignment or admin from organization
```

**Step 1: Define the role's permissions:**

```yaml
- user: user:*
  relation: can_view_project
  object: role:project-admin

- user: user:*
  relation: can_edit_project
  object: role:project-admin
```

**Step 2: Create role assignment with user and role:**

```yaml
- user: user:anne
  relation: assignee
  object: role_assignment:project-admin-website

- user: role:project-admin
  relation: role
  object: role_assignment:project-admin-website
```

**Step 3: Link role assignment to project:**

```yaml
- user: role_assignment:project-admin-website
  relation: role_assignment
  object: project:website
```

**Step 4: Link project to organization:**

```yaml
- user: organization:acme
  relation: organization
  object: project:website
```

**Use when:**
- Different users need the same role on different resources
- Per-project or per-team role membership varies

### 4.4 When to Use Each Role Pattern

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| **Simple Static Roles** | Organization-wide roles with consistent permissions | Simple, efficient | Less flexible for per-resource customization |
| **Simple Custom Roles** | Custom organization-wide roles with consistent permissions | Simple, efficient | Less flexible for per-resource customization |
| **Role Assignments** | Custom resource-specific roles with different members per resource | Highly flexible | More complex, more tuples |

**Choose Simple Roles when:**
- Roles apply at the organization level
- Same users have the role everywhere
- Permission structure is straightforward
- You want minimal tuple management

**Example:** Organization billing admin, HR manager

**Choose Custom Roles when:**
- You need to let end-users define their own roles at the organization level
- Same users have the role everywhere
- Permission structure is straightforward
- You want minimal tuple management

**Example:** End-users can create a billing admin or HR admin role

**Choose Role Assignments when:**
- You need to let end-users define their own roles at the organization level
- Different users need the same role on different resources
- Per-project or per-team role membership varies
- Fine-grained resource-level control is required
- Role membership changes frequently per resource

**Example:** Project lead (different for each project)

**Migration strategies when evolving roles:**

1. **Additive approach:** Introduce custom roles alongside existing static roles
2. **Gradual migration:** Move permissions one at a time to custom roles
3. **Backwards compatibility:** Maintain existing static role behavior during transition

**Common mistake:** Using role assignments for organization-level roles. This adds unnecessary complexity. Use simple user-defined roles instead.

---
## 5. Optimization

Optimize your models for clarity and efficiency.

### 5.1 Simplify Models

Remove unused types and relations from your model.

**Incorrect (unused relations):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define commenter: [user]     # Never used in application
    define legacy_admin: [user]  # Deprecated, no tuples exist

    define can_view : owner or editor or viewer
```

**Correct (minimal model):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define can_view : owner or editor or viewer
```

**Audit checklist:**

1. **Unused types:** Remove types that have no tuples and aren't referenced
2. **Unused relations:** Remove relations that are never checked or written
3. **Unreferenced conditions:** Remove conditions not used in any relation
4. **Dead paths:** Remove `X from Y` paths where Y relation is never used
5. **Downstream relations:** Before deleting relation `r`, verify no relation in this type or child types uses `r from <parent>`
6. **Propagation aliases:** Keep computed aliases (for example, `org_admin`) when they are used to chain permissions across hierarchy levels

**Safety rule:**
- Do not delete a relation only because it is not directly asserted in tests.
- A relation may be required as a transit dependency in inherited paths.
- Always run a dependency scan before removal.

```bash
rg -n "<relation_name>|<relation_name> from" stores/<store>/{model.fga,store.fga.yaml}
```

**After generating models and tests:**


```bash
# Run tests
fga model test --tests store.fga.yaml
```

**Benefits:**
- Easier to understand and maintain
- Faster validation
- Clearer documentation
- Reduced confusion for developers

### 5.2 Minimize Tuple Count

Use indirect relationships to reduce the number of tuples needed.

**Incorrect (tuple explosion):**

```yaml
# Granting viewer access to 100 documents individually
- user: user:anne
  relation: viewer
  object: document:doc-1
- user: user:anne
  relation: viewer
  object: document:doc-2
# ... 98 more tuples (100 total!)
```

**Correct (hierarchical access):**

```yaml
# Grant folder access once
- user: user:anne
  relation: viewer
  object: folder:engineering

# Documents inherit from folder (structural tuples)
- user: folder:engineering
  relation: parent_folder
  object: document:doc-1
- user: folder:engineering
  relation: parent_folder
  object: document:doc-2
# ... link documents to folder
```

One permission tuple + structural tuples scales better than individual grants.

**Team-based access:**

```yaml
# Instead of 50 individual user grants:
- user: user:alice
  relation: viewer
  object: document:spec
- user: user:bob
  relation: viewer
  object: document:spec
# ... 48 more

# Use team membership:
- user: team:engineering#member
  relation: viewer
  object: document:spec

# Add users to team separately
- user: user:alice
  relation: member
  object: team:engineering
```

**Avoid duplicating parent relations across the hierarchy:**

```yaml
# WRONG: writing a parent tuple on every child object
- user: organization:acme
  relation: organization
  object: project:website
- user: organization:acme
  relation: organization
  object: task:fix-bug        # redundant — task is already under project
- user: organization:acme
  relation: organization
  object: comment:c-001       # redundant — comment is already under task
```

```yaml
# CORRECT: parent relation only on the top-level type
- user: organization:acme
  relation: organization
  object: project:website

# Children only need their immediate parent link
- user: project:website
  relation: project
  object: task:fix-bug
- user: task:fix-bug
  relation: task
  object: comment:c-001
```

The model should define local computed relations that chain up through the hierarchy (e.g. `define org_admin: org_admin from project`), so parent roles resolve automatically without extra tuples.

**Benefits:**
- Fewer tuples to store and query
- Easier permission management
- Single point of revocation
- No redundant parent tuples on child objects
- Better performance at scale

### 5.3 Type Restrictions

Apply appropriate type restrictions to prevent invalid tuples.

**Incorrect (overly permissive):**

```dsl.openfga
type document
  relations
    define parent: [folder, document, user, organization]  # Too broad
```

**Correct (precise restrictions):**

```dsl.openfga
type document
  relations
    define parent_folder: [folder]      # Only folders can be parents
    define organization: [organization] # Only organizations
    define owner: [user]                # Only users can own
```

If business rules imply that a resource can belong to different kinds of parents, then it is OK to represent it in the model:

```dsl.openfga
type organization
  define member: [user]
type business_unit
  define member: [user]

type document
  relations
    define parent_entity: [organization, business_unit]
    define parent_folder: [folder]      # Only folders can be parents
    define owner: [user]                # Only users can own
    define can_view: owner or member from parent_entity
```


**Common type restriction patterns:**

```dsl.openfga
# Only users
define owner: [user]

# Users or usersets (team members)
define editor: [user, team#member]

# Only organizational objects
define parent: [organization]

# Users with conditions
define admin: [user with time_based]

# Public access (use carefully)
define viewer: [user, user:*]
```

**Type restrictions:**
- Prevent invalid tuples from being written
- Make the model self-documenting
- Enable better tooling support
- Catch errors at write time, not check time

**Anti-pattern - kitchen sink:**

```dsl.openfga
# Don't do this - too permissive
define viewer: [user, user:*, team, team#member, organization, organization#member, role#assignee]
```

Instead, be specific about what types make sense for each relation.

---
## 6. Testing

Thorough testing ensures your authorization model behaves as expected.

### 6.1 Structure Tests in .fga.yaml

The `.fga.yaml` file defines both your model and tests in a single file.

**Basic structure:**

```yaml
name: My Authorization Model Tests

model: |
  model
    schema 1.1

  type user

  type document
    relations
      define owner: [user]
      define editor: [user] or owner
      define viewer: [user] or editor

tuples:
  - user: user:anne
    relation: owner
    object: document:roadmap

  - user: user:bob
    relation: editor
    object: document:roadmap

tests:
  - name: Document access tests
    check:
      # Check assertions here
    list_objects:
      # List objects assertions here
    list_users:
      # List users assertions here
```

**Alternative (external files):**

```yaml
name: Model Tests
model_file: model.fga
tuple_file: tuples.yaml
```

**Alternative when using Modular Models:**

```yaml
name: Model Tests
model_file: fga.mod
tuple_file: tuples.yaml
```


**Multiple tuple files:**

```yaml
tuple_files:
  - ./users.yaml
  - ./permissions.yaml
  - ./org-structure.yaml
```

**Benefits:**
- Self-contained test definitions
- Version-controlled authorization logic
- Enables test-driven development for authorization

### 6.2 Check Assertions

Check assertions verify whether a user has a specific relation to an object.

**Example:**

```yaml
tests:
  - name: Owner permissions
    check:
      - user: user:anne
        object: document:roadmap
        assertions:
          owner: true
          editor: true   # Inherited through concentric relationship
          viewer: true   # Inherited through concentric relationship
          can_delete: true

      - user: user:bob
        object: document:roadmap
        assertions:
          owner: false
          editor: true
          viewer: true
          can_delete: false
```

**Always test both positive and negative cases:**

```yaml
check:
  # Positive: user HAS access
  - user: user:anne
    object: document:secret
    assertions:
      viewer: true

  # Negative: user does NOT have access
  - user: user:mallory
    object: document:secret
    assertions:
      viewer: false
      editor: false
      owner: false
```

**Test boundary conditions:**

```yaml
check:
  # User with no tuples at all
  - user: user:unknown
    object: document:roadmap
    assertions:
      viewer: false

  # Object with no tuples at all
  - user: user:anne
    object: document:nonexistent
    assertions:
      viewer: false
```

### 6.3 List Objects Tests

List objects tests verify which objects a user has access to.

**Example:**

```yaml
tests:
  - name: List accessible documents
    list_objects:
      - user: user:anne
        type: document
        assertions:
          owner:
            - document:roadmap
          viewer:
            - document:roadmap
            - document:public-doc

      - user: user:bob
        type: document
        assertions:
          owner: []  # Empty list - no owned documents
          editor:
            - document:roadmap
```

**Test empty results:**

```yaml
list_objects:
  - user: user:unknown
    type: document
    assertions:
      owner: []
      viewer: []
```

**Test multiple object types:**

```yaml
list_objects:
  - user: user:anne
    type: document
    assertions:
      viewer:
        - document:roadmap
        - document:spec

  - user: user:anne
    type: folder
    assertions:
      viewer:
        - folder:engineering
```

**Use cases:**
- Building UI that shows accessible resources
- Auditing user access across the system
- Verifying hierarchical inheritance works correctly

### 6.4 List Users Tests

List users tests verify which users have access to an object.

**Example:**

```yaml
tests:
  - name: List document users
    list_users:
      - object: document:roadmap
        user_filter:
          - type: user
        assertions:
          owner:
            users:
              - user:anne
          editor:
            users:
              - user:anne
              - user:bob
          viewer:
            users:
              - user:anne
              - user:bob
```

**Test empty results:**

```yaml
list_users:
  - object: document:private
    user_filter:
      - type: user
    assertions:
      viewer:
        users: []
```

**User filter with relation (for usersets):**

```yaml
list_users:
  - object: document:roadmap
    user_filter:
      - type: team
        relation: member
    assertions:
      editor:
        users:
          - team:engineering#member
```

**User filter formats:**
- `type: user` - List individual users
- `type: team` with `relation: member` - List team usersets
- `type: user` with `user:*` - Include public access

**Use cases:**
- Auditing who has access to sensitive resources
- Building share dialogs showing current collaborators
- Compliance reporting

### 6.5 Testing Conditions

Test conditional relationships by providing context in your assertions.

**Example model:**

```dsl.openfga
model
  schema 1.1

type user

type resource
  relations
    define viewer: [user with in_allowed_ip_range]

condition in_allowed_ip_range(user_ip: string, allowed_range: string) {
  user_ip.startsWith(allowed_range)
}
```

**Conditional tuple:**

```yaml
tuples:
  - user: user:anne
    relation: viewer
    object: resource:internal
    condition:
      name: in_allowed_ip_range
      context:
        allowed_range: "192.168."
```

**Tests with context:**

```yaml
tests:
  - name: Conditional access tests
    check:
      # Access granted - IP matches
      - user: user:anne
        object: resource:internal
        context:
          user_ip: "192.168.1.100"
        assertions:
          viewer: true

      # Access denied - IP doesn't match
      - user: user:anne
        object: resource:internal
        context:
          user_ip: "10.0.0.50"
        assertions:
          viewer: false
```

**Time-based condition testing:**

```yaml
tests:
  - name: Time-based access
    check:
      # Within valid window
      - user: user:peter
        object: organization:acme
        context:
          current_time: "2024-02-01T00:10:00Z"
        assertions:
          admin: true

      # After window expired
      - user: user:peter
        object: organization:acme
        context:
          current_time: "2024-02-02T00:00:00Z"
        assertions:
          admin: false
```

**Always test both passing and failing condition evaluations.**

### 6.6 OpenFGA CLI Usage

Use the OpenFGA CLI to validate and test your models.

**MANDATORY**: Always run `fga model test` after creating or modifying any `.fga` or `.fga.yaml` file. Do not consider any OpenFGA task complete until tests pass.

Use the OpenFGA CLI to validate and test your models.

**Installation:**

```bash
# macOS
brew install openfga/tap/fga

# Debian
sudo apt install ./fga_<version>_linux_<arch>.deb

# Docker
docker pull openfga/cli
docker run -it openfga/cli
```

**Validate model syntax:**

```bash
fga model validate --file model.fga
```

**Run tests:**

```bash
fga model test --tests store.fga.yaml
```

**Transform between formats:**

```bash
# DSL to JSON
fga model transform --input model.fga --output model.json

# JSON to DSL
fga model transform --input model.json --output model.fga
```

**Example test run:**

```bash
$ fga model test --tests store.fga.yaml
# Test Summary #
Tests 1/1 passing
Checks 5/5 passing
```

**CI/CD integration:**

```bash
# Fail the build if tests don't pass
fga model test --tests store.fga.yaml || exit 1
```

You can also use the [OpenFGA Model Test GitHub actions](https://github.com/marketplace/actions/openfga-model-testing-action). 

**Verbose output for debugging:**

```bash
fga model test --tests store.fga.yaml --verbose
```

### 6.7 Always Validate Models

**CRITICAL**: After creating or modifying any `.fga` or `.fga.yaml` file, you MUST immediately run tests to validate the model. Never deliver an untested model.

### Incorrect: Delivering Untested Model

```
1. Create/modify .fga model
2. Create/modify .fga.yaml tests
3. Deliver to user ❌ WRONG
```

The model may have syntax errors, logical errors, or test assertions that don't match actual behavior.

### Correct: Validate Before Delivery

```
1. Create/modify .fga model
2. Create/modify .fga.yaml tests
3. Run: fga model test --tests <file>.fga.yaml ✓
4. If tests fail: fix model or tests, go to step 3
5. Deliver to user with test results ✓
```

### Command

```bash
fga model test --tests <filename>.fga.yaml
```

### Why This Matters

- **Syntax errors**: The DSL parser will catch invalid syntax
- **Logical errors**: Tests verify permissions work as intended
- **Inheritance bugs**: Complex `from` relationships may not behave as expected
- **Missing tuples**: Tests ensure all required tuples exist for assertions

### Example Workflow

```bash
# After creating notion.fga and notion.fga.yaml
$ fga model test --tests notion.fga.yaml

# Expected output for passing tests:
# Test Summary #
Tests 14/14 passing
Checks 123/123 passing
ListObjects 3/3 passing
ListUsers 1/1 passing

# If tests fail, fix the issues and re-run until all pass
```

### Non-Negotiable

This step is **not optional**. An untested authorization model may:
- Grant access to users who shouldn't have it
- Deny access to users who should have it
- Cause security vulnerabilities in production

Always run tests. Always report results to the user.

---
## 7. SDKs (for integration tasks only)

SDK implementations for integrating OpenFGA into your applications.

### 7.1 JavaScript/TypeScript SDK

The [@openfga/sdk](https://github.com/openfga/js-sdk) package provides the official OpenFGA client for JavaScript and TypeScript applications.

### Installation

```bash
npm install @openfga/sdk
```

### Client Initialization

**Basic setup:**

```typescript
const { OpenFgaClient } = require('@openfga/sdk');

const fgaClient = new OpenFgaClient({
  apiUrl: process.env.FGA_API_URL,
  storeId: process.env.FGA_STORE_ID,
  authorizationModelId: process.env.FGA_MODEL_ID,
});
```

**With API Token:**

```typescript
const { OpenFgaClient, CredentialsMethod } = require('@openfga/sdk');

const fgaClient = new OpenFgaClient({
  apiUrl: process.env.FGA_API_URL,
  storeId: process.env.FGA_STORE_ID,
  credentials: {
    method: CredentialsMethod.ApiToken,
    config: {
      token: process.env.FGA_API_TOKEN,
    }
  }
});
```

**With Client Credentials (OAuth2):**

```typescript
const fgaClient = new OpenFgaClient({
  apiUrl: process.env.FGA_API_URL,
  storeId: process.env.FGA_STORE_ID,
  credentials: {
    method: CredentialsMethod.ClientCredentials,
    config: {
      apiTokenIssuer: process.env.FGA_API_TOKEN_ISSUER,
      apiAudience: process.env.FGA_API_AUDIENCE,
      clientId: process.env.FGA_CLIENT_ID,
      clientSecret: process.env.FGA_CLIENT_SECRET,
    }
  }
});
```

### Load Authorization Model from File

**From JSON file:**

```typescript
const fs = require('fs');

// Read and parse JSON model
const modelJson = JSON.parse(fs.readFileSync('model.json', 'utf8'));

const { authorization_model_id } = await fgaClient.writeAuthorizationModel(modelJson);
```

**From DSL (.fga) file:**

Use the `@openfga/syntax-transformer` package to convert DSL to JSON:

```bash
npm install @openfga/syntax-transformer
```

```typescript
const fs = require('fs');
const { transformer } = require('@openfga/syntax-transformer');

// Read DSL file and transform to JSON
const dslContent = fs.readFileSync('model.fga', 'utf8');
const modelJson = transformer.transformDSLToJSON(dslContent);

const { authorization_model_id } = await fgaClient.writeAuthorizationModel(
  JSON.parse(modelJson)
);
```

**Alternative: Use CLI for conversion**

```bash
# Convert DSL to JSON using the FGA CLI
fga model transform --input model.fga --output model.json
```

Then load the JSON file as shown above.

### Check Permission

```typescript
const result = await fgaClient.check({
  user: "user:anne",
  relation: "viewer",
  object: "document:roadmap",
});
// result.allowed === true or false
```

### Batch Check

```typescript
const { result } = await fgaClient.batchCheck({
  checks: [
    { user: "user:anne", relation: "viewer", object: "document:roadmap" },
    { user: "user:bob", relation: "editor", object: "document:budget" }
  ]
});
```

### Write Tuples

```typescript
await fgaClient.write({
  writes: [
    { user: "user:anne", relation: "viewer", object: "document:roadmap" }
  ],
  deletes: [
    { user: "user:bob", relation: "editor", object: "document:budget" }
  ],
});

// Convenience methods
await fgaClient.writeTuples([
  { user: "user:anne", relation: "viewer", object: "document:roadmap" }
]);
await fgaClient.deleteTuples([
  { user: "user:bob", relation: "editor", object: "document:budget" }
]);
```

### List Objects

```typescript
const response = await fgaClient.listObjects({
  user: "user:anne",
  relation: "viewer",
  type: "document",
});
// response.objects = ["document:roadmap", "document:budget"]
```

### List Relations

```typescript
const response = await fgaClient.listRelations({
  user: "user:anne",
  object: "document:roadmap",
  relations: ["can_view", "can_edit", "can_delete"],
});
// response.relations = ["can_view", "can_edit"]
```

### List Users

```typescript
const response = await fgaClient.listUsers({
  object: { type: "document", id: "roadmap" },
  relation: "can_read",
  user_filters: [{ type: "user" }],
});
// response.users = [{ object: { type: "user", id: "anne" } }]
```

### Read Tuples

```typescript
const { tuples } = await fgaClient.read({
  user: "user:anne",
  relation: "viewer",
  object: "document:roadmap",
});
```

### Non-Transaction Write Mode

For large batch writes:

```typescript
const response = await fgaClient.write({
  writes: largeTupleArray,
}, {
  transaction: {
    disable: true,
    maxPerChunk: 100,
    maxParallelRequests: 10,
  }
});
```

### Handle Write Conflicts

```typescript
const { ClientWriteRequestOnDuplicateWrites } = require('@openfga/sdk');

await fgaClient.write({
  writes: [{ user: "user:anne", relation: "writer", object: "document:budget" }],
}, {
  conflict: {
    onDuplicateWrites: ClientWriteRequestOnDuplicateWrites.Ignore,
  }
});
```

### Retry Configuration

```typescript
const fgaClient = new OpenFgaClient({
  apiUrl: process.env.FGA_API_URL,
  retryParams: {
    maxRetry: 3,
    minWaitInMs: 250
  }
});
```

### Best Practices

- **Initialize once:** Create `OpenFgaClient` once and reuse throughout your application
- **Input format:** Parameters use camelCase
- **Response format:** API responses use snake_case
- **Retry behavior:** SDK auto-retries on 429 and 5xx errors (up to 3 times)
- **Batch operations:** Use `correlationId` to match responses to requests

### 7.2 Go SDK

The [`github.com/openfga/go-sdk](https://github.com/openfga/go-sdk) package provides the official OpenFGA client for Go applications.

### Installation

```bash
go get -u github.com/openfga/go-sdk
go mod tidy
```

### Client Initialization

**Basic setup:**

```go
import openfga "github.com/openfga/go-sdk"

fgaClient, err := NewSdkClient(&ClientConfiguration{
    ApiUrl:               os.Getenv("FGA_API_URL"),
    StoreId:              os.Getenv("FGA_STORE_ID"),
    AuthorizationModelId: os.Getenv("FGA_MODEL_ID"),
})
```

**With API Token:**

```go
import "github.com/openfga/go-sdk/credentials"

fgaClient, err := NewSdkClient(&ClientConfiguration{
    ApiUrl:  os.Getenv("FGA_API_URL"),
    StoreId: os.Getenv("FGA_STORE_ID"),
    Credentials: &credentials.Credentials{
        Method: credentials.CredentialsMethodApiToken,
        Config: &credentials.Config{
            ApiToken: os.Getenv("FGA_API_TOKEN"),
        },
    },
})
```

**With Client Credentials (OAuth2):**

```go
fgaClient, err := NewSdkClient(&ClientConfiguration{
    ApiUrl: os.Getenv("FGA_API_URL"),
    Credentials: &credentials.Credentials{
        Method: credentials.CredentialsMethodClientCredentials,
        Config: &credentials.Config{
            ClientCredentialsClientId:       os.Getenv("FGA_CLIENT_ID"),
            ClientCredentialsClientSecret:   os.Getenv("FGA_CLIENT_SECRET"),
            ClientCredentialsApiAudience:    os.Getenv("FGA_API_AUDIENCE"),
            ClientCredentialsApiTokenIssuer: os.Getenv("FGA_API_TOKEN_ISSUER"),
        },
    },
})
```

### Check Permission

```go
data, err := fgaClient.Check(context.Background()).
    Body(ClientCheckRequest{
        User:     "user:anne",
        Relation: "viewer",
        Object:   "document:roadmap",
    }).
    Execute()
fmt.Printf("allowed: %t", data.GetAllowed())
```

### Batch Check

```go
body := ClientBatchCheckRequest{
    Checks: []ClientBatchCheckItem{{
        CorrelationId: "check-1",
        User:          "user:anne",
        Relation:      "viewer",
        Object:        "document:roadmap",
    }},
}
data, err := fgaClient.BatchCheck(context.Background()).Body(body).Execute()
// Results keyed by correlationId
```

### Write Tuples

```go
body := ClientWriteRequest{
    Writes: &[]ClientTupleKey{{
        User:     "user:anne",
        Relation: "viewer",
        Object:   "document:roadmap",
    }},
    Deletes: &[]ClientTupleKeyWithoutCondition{{
        User:     "user:bob",
        Relation: "editor",
        Object:   "document:budget",
    }},
}
err := fgaClient.Write(context.Background()).Body(body).Execute()
```

### List Objects

```go
data, err := fgaClient.ListObjects(context.Background()).
    Body(ClientListObjectsRequest{
        User:     "user:anne",
        Relation: "can_read",
        Type:     "document",
    }).
    Execute()
// data.Objects contains accessible object IDs
```

### Streamed List Objects

```go
response, err := fgaClient.StreamedListObjects(context.Background()).
    Body(ClientStreamedListObjectsRequest{
        User:     "user:anne",
        Relation: "can_read",
        Type:     "document",
    }).
    Execute()
defer response.Close()

for obj := range response.Objects {
    objects = append(objects, obj.Object)
}
```

### List Relations

```go
data, err := fgaClient.ListRelations(context.Background()).
    Body(ClientListRelationsRequest{
        User:      "user:anne",
        Object:    "document:roadmap",
        Relations: []string{"can_view", "can_edit"},
    }).
    Execute()
// data.Relations contains applicable relations
```

### List Users

```go
data, err := fgaClient.ListUsers(context.Background()).
    Body(ClientListUsersRequest{
        Object:      openfga.FgaObject{Type: "document", Id: "roadmap"},
        Relation:    "can_read",
        UserFilters: []openfga.UserTypeFilter{{Type: "user"}},
    }).
    Execute()
```

### Read Tuples

```go
data, err := fgaClient.Read(context.Background()).
    Body(ClientReadRequest{
        User:     openfga.PtrString("user:anne"),
        Relation: openfga.PtrString("viewer"),
        Object:   openfga.PtrString("document:roadmap"),
    }).
    Execute()
```

### Non-Transaction Write Mode

```go
options := ClientWriteOptions{
    Transaction: &TransactionOptions{
        Disable:             true,
        MaxParallelRequests: 5,
        MaxPerChunk:         100,
    },
}
data, err := fgaClient.Write(context.Background()).
    Body(body).
    Options(options).
    Execute()
```

### Load Authorization Model from File

**From JSON file:**

```go
import (
    "encoding/json"
    "os"
    openfga "github.com/openfga/go-sdk"
)

// Read JSON file
jsonContent, err := os.ReadFile("model.json")
if err != nil {
    log.Fatal(err)
}

// Parse into request body
var body openfga.WriteAuthorizationModelRequest
if err := json.Unmarshal(jsonContent, &body); err != nil {
    log.Fatal(err)
}

// Write the model
response, err := fgaClient.WriteAuthorizationModel(context.Background()).
    Body(body).
    Execute()
```

**From DSL (.fga) file:**

Install the language transformer:

```bash
go get github.com/openfga/language/pkg/go/transformer
```

```go
import (
    "encoding/json"
    "os"
    "github.com/openfga/language/pkg/go/transformer"
    openfga "github.com/openfga/go-sdk"
)

// Read DSL file
dslContent, err := os.ReadFile("model.fga")
if err != nil {
    log.Fatal(err)
}

// Transform DSL to JSON
jsonModel, err := transformer.TransformDSLToJSON(string(dslContent))
if err != nil {
    log.Fatal(err)
}

// Parse into request body
var body openfga.WriteAuthorizationModelRequest
if err := json.Unmarshal([]byte(jsonModel), &body); err != nil {
    log.Fatal(err)
}

// Write the model
response, err := fgaClient.WriteAuthorizationModel(context.Background()).
    Body(body).
    Execute()
```

### Contextual Tuples

```go
body := ClientCheckRequest{
    User:     "user:anne",
    Relation: "viewer",
    Object:   "document:roadmap",
    ContextualTuples: &[]ClientTupleKey{{
        User:     "user:anne",
        Relation: "editor",
        Object:   "document:roadmap",
    }},
}
```

### Retry Configuration

```go
fgaClient, err := NewSdkClient(&ClientConfiguration{
    RetryParams: &openfga.RetryParams{
        MaxRetry:    3,
        MinWaitInMs: 250,
    },
})
```

### Best Practices

- **Initialize once:** Create the client once and reuse throughout your application
- **Use context:** Always pass `context.Context` for cancellation and timeouts
- **Pointer helpers:** Use `openfga.PtrString()` for optional string parameters
- **Retry behavior:** SDK auto-retries on 429 and 5xx errors (up to 3 times)
- **Streaming:** Use `StreamedListObjects` for large result sets

### 7.3 Python SDK

The [`openfga_sdk`](https://github.com/openfga/python-sdk) package provides the official OpenFGA client for Python applications with both async and sync support.

### Installation

```bash
pip install openfga_sdk
```

### Client Initialization

**Async client (recommended):**

```python
from openfga_sdk import ClientConfiguration, OpenFgaClient

async def main():
    configuration = ClientConfiguration(
        api_url="http://localhost:8080",
        store_id="YOUR_STORE_ID",
        authorization_model_id="YOUR_MODEL_ID"
    )
    async with OpenFgaClient(configuration) as fga_client:
        result = await fga_client.check(body)
        return result
```

**Synchronous client:**

```python
from openfga_sdk.client import ClientConfiguration
from openfga_sdk.sync import OpenFgaClient

def main():
    configuration = ClientConfiguration(
        api_url="http://localhost:8080",
        store_id="YOUR_STORE_ID"
    )
    with OpenFgaClient(configuration) as fga_client:
        result = fga_client.check(body)
        return result
```

**With API Token:**

```python
from openfga_sdk.credentials import Credentials, CredentialConfiguration

configuration = ClientConfiguration(
    api_url="http://localhost:8080",
    credentials=Credentials(
        method='api_token',
        configuration=CredentialConfiguration(
            api_token="YOUR_TOKEN"
        )
    )
)
```

**With Client Credentials (OAuth2):**

```python
configuration = ClientConfiguration(
    api_url="http://localhost:8080",
    credentials=Credentials(
        method='client_credentials',
        configuration=CredentialConfiguration(
            api_issuer="YOUR_ISSUER",
            api_audience="YOUR_AUDIENCE",
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET"
        )
    )
)
```

### Load Authorization Model from File

**From JSON file:**

```python
import json
from openfga_sdk import WriteAuthorizationModelRequest

# Read JSON file
with open('model.json', 'r') as f:
    model_json = json.load(f)

# Create request from JSON
body = WriteAuthorizationModelRequest(
    schema_version=model_json.get('schema_version', '1.1'),
    type_definitions=model_json['type_definitions'],
    conditions=model_json.get('conditions')
)

response = await fga_client.write_authorization_model(body)
# response.authorization_model_id contains the new model ID
```

**From DSL (.fga) file:**

The Python SDK does not include a built-in DSL parser. Convert DSL files to JSON using the OpenFGA CLI, then load the JSON file.

```bash
# Convert DSL to JSON using the FGA CLI
fga model transform --input model.fga --output model.json
```

Then load the JSON file as shown above.

### Check Permission

```python
from openfga_sdk.client.models import ClientCheckRequest

body = ClientCheckRequest(
    user="user:anne",
    relation="viewer",
    object="document:roadmap",
)

response = await fga_client.check(body)
# response.allowed = True/False
```

### Batch Check

```python
from openfga_sdk.client.models import (
    ClientBatchCheckItem,
    ClientBatchCheckRequest
)

checks = [
    ClientBatchCheckItem(
        user="user:anne",
        relation="viewer",
        object="document:roadmap"
    ),
    ClientBatchCheckItem(
        user="user:bob",
        relation="editor",
        object="document:budget"
    )
]

response = await fga_client.batch_check(
    ClientBatchCheckRequest(checks=checks)
)
```

### Write Tuples

```python
from openfga_sdk.client.models import ClientTuple, ClientWriteRequest

body = ClientWriteRequest(
    writes=[
        ClientTuple(
            user="user:anne",
            relation="viewer",
            object="document:roadmap"
        )
    ],
    deletes=[
        ClientTuple(
            user="user:bob",
            relation="editor",
            object="document:budget"
        )
    ]
)

response = await fga_client.write(body)
```

### List Objects

```python
from openfga_sdk.client.models import ClientListObjectsRequest

body = ClientListObjectsRequest(
    user="user:anne",
    relation="viewer",
    type="document"
)

response = await fga_client.list_objects(body)
# response.objects = ["document:roadmap", "document:budget"]
```

### Stream List Objects

```python
request = ClientListObjectsRequest(
    user="user:anne",
    relation="viewer",
    type="document"
)

results = []
async for response in fga_client.streamed_list_objects(request):
    results.append(response.object)
```

### List Relations

```python
from openfga_sdk.client.models import ClientListRelationsRequest

body = ClientListRelationsRequest(
    user="user:anne",
    object="document:roadmap",
    relations=["can_view", "can_edit"]
)

response = await fga_client.list_relations(body)
# response.relations = ["can_view"]
```

### List Users

```python
from openfga_sdk.client.models import ClientListUsersRequest, UserTypeFilter
from openfga_sdk.models.fga_object import FgaObject

request = ClientListUsersRequest(
    object=FgaObject(type="document", id="roadmap"),
    relation="can_read",
    user_filters=[
        UserTypeFilter(type="user"),
        UserTypeFilter(type="team", relation="member")
    ]
)

response = await fga_client.list_users(request)
```

### Read Tuples

```python
from openfga_sdk import ReadRequestTupleKey

body = ReadRequestTupleKey(
    user="user:anne",
    relation="viewer",
    object="document:roadmap"
)

response = await fga_client.read(body)
# response.tuples = [Tuple(...), ...]
```

### Non-Transaction Write Mode

```python
from openfga_sdk.client.models import WriteTransactionOpts

options = {
    "transaction": WriteTransactionOpts(
        disabled=True,
        max_parallel_requests=10,
        max_per_chunk=100
    )
}

response = await fga_client.write(body, options)
```

### Handle Write Conflicts

```python
from openfga_sdk.client.models.write_conflict_opts import (
    ConflictOptions,
    ClientWriteRequestOnDuplicateWrites,
    ClientWriteRequestOnMissingDeletes
)

options = {
    "conflict": ConflictOptions(
        on_duplicate_writes=ClientWriteRequestOnDuplicateWrites.IGNORE,
        on_missing_deletes=ClientWriteRequestOnMissingDeletes.IGNORE
    )
}

response = await fga_client.write(body, options)
```

### Retry Configuration

```python
from openfga_sdk.configuration import RetryParams

config = ClientConfiguration(
    api_url="http://localhost:8080",
    retry_params=RetryParams(
        max_retry=5,
        min_wait_in_ms=250
    )
)
```

### Error Handling

```python
from openfga_sdk.exceptions import ApiException

try:
    await fga_client.check(request)
except ApiException as e:
    if e.is_validation_error():
        print(f"Validation error: {e.error_message}")
    elif e.is_retryable():
        print(f"Temporary error (Request: {e.request_id})")
    else:
        print(f"Error: {e}")
```

### Best Practices

- **Use async:** Prefer async client for better performance
- **Context manager:** Use `async with` or `with` for proper resource cleanup
- **Retry behavior:** SDK auto-retries on 429 and 5xx errors (up to 3 times)
- **Streaming:** Use `streamed_list_objects` for large result sets

### 7.4 Java SDK

The [OpenFGA Java SDK](https://github.com/openfga/java-sdk) provides the official client for JVM applications. Requires Java 17+.

### Installation

**Maven:**

```xml
<dependency>
    <groupId>dev.openfga</groupId>
    <artifactId>openfga-sdk</artifactId>
    <version>0.9.7</version>
</dependency>
```

**Gradle:**

```groovy
implementation 'dev.openfga:openfga-sdk:0.9.7'
```

### Client Initialization

**Basic setup:**

```java
import dev.openfga.sdk.api.client.OpenFgaClient;
import dev.openfga.sdk.api.configuration.ClientConfiguration;

var config = new ClientConfiguration()
        .apiUrl(System.getenv("FGA_API_URL"))
        .storeId(System.getenv("FGA_STORE_ID"))
        .authorizationModelId(System.getenv("FGA_MODEL_ID"));

var fgaClient = new OpenFgaClient(config);
```

**With API Token:**

```java
import dev.openfga.sdk.api.configuration.Credentials;
import dev.openfga.sdk.api.configuration.ApiToken;

var config = new ClientConfiguration()
        .apiUrl(System.getenv("FGA_API_URL"))
        .storeId(System.getenv("FGA_STORE_ID"))
        .credentials(new Credentials(
            new ApiToken(System.getenv("FGA_API_TOKEN"))));

var fgaClient = new OpenFgaClient(config);
```

**With Client Credentials (OAuth2):**

```java
import dev.openfga.sdk.api.configuration.ClientCredentials;

var config = new ClientConfiguration()
        .apiUrl(System.getenv("FGA_API_URL"))
        .credentials(new Credentials(
            new ClientCredentials()
                    .apiTokenIssuer(System.getenv("FGA_API_TOKEN_ISSUER"))
                    .apiAudience(System.getenv("FGA_API_AUDIENCE"))
                    .clientId(System.getenv("FGA_CLIENT_ID"))
                    .clientSecret(System.getenv("FGA_CLIENT_SECRET"))));

var fgaClient = new OpenFgaClient(config);
```

### Load Authorization Model from File

**From JSON file:**

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.openfga.sdk.api.model.WriteAuthorizationModelRequest;
import java.io.File;

ObjectMapper mapper = new ObjectMapper();

// Read and parse JSON file
WriteAuthorizationModelRequest body = mapper.readValue(
    new File("model.json"),
    WriteAuthorizationModelRequest.class
);

var response = fgaClient.writeAuthorizationModel(body).get();
// response.getAuthorizationModelId() contains the new model ID
```

**From DSL (.fga) file:**

Use the `openfga-language` package to transform DSL to JSON.

**Maven:**

```xml
<dependency>
    <groupId>dev.openfga</groupId>
    <artifactId>openfga-language</artifactId>
    <version>0.2.0</version>
</dependency>
```

**Gradle:**

```groovy
implementation 'dev.openfga:openfga-language:0.2.0'
```

**Transform DSL to JSON:**

```java
import dev.openfga.language.DslToJsonTransformer;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.openfga.sdk.api.model.WriteAuthorizationModelRequest;
import java.nio.file.Files;
import java.nio.file.Path;

// Read DSL file
String dslContent = Files.readString(Path.of("model.fga"));

// Transform DSL to JSON
String jsonString = new DslToJsonTransformer().transform(dslContent);

// Parse JSON into request body
ObjectMapper mapper = new ObjectMapper();
WriteAuthorizationModelRequest body = mapper.readValue(
    jsonString,
    WriteAuthorizationModelRequest.class
);

var response = fgaClient.writeAuthorizationModel(body).get();
// response.getAuthorizationModelId() contains the new model ID
```

**Validate DSL before transforming:**

```java
import dev.openfga.language.validation.ModelValidator;
import dev.openfga.language.errors.DslErrorsException;

try {
    ModelValidator.validateDsl(dslContent);
} catch (DslErrorsException e) {
    // Handle validation errors
    System.err.println("DSL errors: " + e.getErrors());
}
```

**Alternative: Use CLI for conversion**

```bash
# Convert DSL to JSON using the FGA CLI
fga model transform --input model.fga --output model.json
```

Then load the JSON file as shown above.

### Check Permission

```java
import dev.openfga.sdk.api.client.model.ClientCheckRequest;

var request = new ClientCheckRequest()
    .user("user:anne")
    .relation("viewer")
    ._object("document:roadmap");

var response = fgaClient.check(request).get();
// response.getAllowed() returns true/false
```

### Batch Check

```java
import dev.openfga.sdk.api.client.model.ClientBatchCheckRequest;
import dev.openfga.sdk.api.client.model.ClientBatchCheckItem;

var request = new ClientBatchCheckRequest().checks(
    List.of(
        new ClientBatchCheckItem()
            .user("user:anne")
            .relation("viewer")
            ._object("document:roadmap")
            .correlationId("check-1"),
        new ClientBatchCheckItem()
            .user("user:bob")
            .relation("editor")
            ._object("document:budget")
            .correlationId("check-2")));

var options = new ClientBatchCheckOptions()
    .maxParallelRequests(5)
    .maxBatchSize(20);

var response = fgaClient.batchCheck(request, options).get();
```

### Write Tuples

```java
import dev.openfga.sdk.api.client.model.ClientWriteRequest;
import dev.openfga.sdk.api.model.TupleKey;

var request = new ClientWriteRequest()
    .writes(List.of(
        new TupleKey()
            .user("user:anne")
            .relation("viewer")
            ._object("document:roadmap")))
    .deletes(List.of(
        new TupleKey()
            .user("user:bob")
            .relation("editor")
            ._object("document:budget")));

var response = fgaClient.write(request).get();
```

### List Objects

```java
import dev.openfga.sdk.api.client.model.ClientListObjectsRequest;

var request = new ClientListObjectsRequest()
    .user("user:anne")
    .relation("viewer")
    .type("document");

var response = fgaClient.listObjects(request).get();
// response.getObjects() returns accessible document IDs
```

### List Relations

```java
import dev.openfga.sdk.api.client.model.ClientListRelationsRequest;

var request = new ClientListRelationsRequest()
    .user("user:anne")
    ._object("document:roadmap")
    .relations(List.of("can_view", "can_edit", "can_delete"));

var response = fgaClient.listRelations(request).get();
// response.getRelations() returns applicable relations
```

### List Users

```java
import dev.openfga.sdk.api.client.model.ClientListUsersRequest;
import dev.openfga.sdk.api.model.FgaObject;
import dev.openfga.sdk.api.model.UserTypeFilter;

var userFilters = new ArrayList<UserTypeFilter>() {{
    add(new UserTypeFilter().type("user"));
}};

var request = new ClientListUsersRequest()
    ._object(new FgaObject().type("document").id("roadmap"))
    .relation("can_read")
    .userFilters(userFilters);

var response = fgaClient.listUsers(request).get();
// response.getUsers() returns matching users
```

### Read Tuples

```java
import dev.openfga.sdk.api.client.model.ClientReadRequest;

var request = new ClientReadRequest()
    .user("user:anne")
    .relation("viewer")
    ._object("document:roadmap");

var response = fgaClient.read(request).get();
```

### Non-Transaction Write Mode

```java
var options = new ClientWriteOptions()
    .disableTransactions(true)
    .transactionChunkSize(5); // max requests per transaction chunk

var response = fgaClient.write(request, options).get();
```

### Handle Write Conflicts

```java
import dev.openfga.sdk.api.model.WriteRequestWrites;
import dev.openfga.sdk.api.model.WriteRequestDeletes;

var options = new ClientWriteOptions()
    .onDuplicate(WriteRequestWrites.OnDuplicateEnum.IGNORE)
    .onMissing(WriteRequestDeletes.OnMissingEnum.IGNORE);

var response = fgaClient.write(request, options).get();

// Can also be set independently for writes-only or deletes-only
var writeOnlyOptions = new ClientWriteOptions()
    .onDuplicate(WriteRequestWrites.OnDuplicateEnum.IGNORE);

var deleteOnlyOptions = new ClientWriteOptions()
    .onMissing(WriteRequestDeletes.OnMissingEnum.IGNORE);
```

### Contextual Tuples

```java
var request = new ClientCheckRequest()
    .user("user:anne")
    .relation("viewer")
    ._object("document:roadmap")
    .contextualTuples(List.of(
        new ClientTupleKey()
            .user("user:anne")
            .relation("editor")
            ._object("document:roadmap")));

var response = fgaClient.check(request).get();
```

### Retry Configuration

The SDK retries on 429 and 5xx errors (up to 3 times by default, max 15). It respects `Retry-After` headers and uses exponential backoff as fallback.

```java
import java.time.Duration;

var config = new ClientConfiguration()
        .apiUrl("http://localhost:8080")
        .maxRetries(3) // default: 3, maximum: 15
        .minimumRetryDelay(Duration.ofMillis(100)); // minimum wait between retries

var fgaClient = new OpenFgaClient(config);
```

### Best Practices

- **Initialize once:** Create `OpenFgaClient` once and reuse throughout your application
- **Async handling:** Use `.get()` to block or `.thenApply()` for async
- **Object naming:** Use `._object()` (with underscore) for object parameter
- **Retry behavior:** SDK auto-retries on 429 and 5xx errors (up to 3 times)
- **Java version:** Requires Java 17+

### 7.5 .NET SDK

The [OpenFga.Sdk](https://github.com/openfga/dotnet-sdk) package provides the official OpenFGA client for .NET applications.

### Installation

```powershell
dotnet add package OpenFga.Sdk
```

Supported frameworks: `net8.0`, `net9.0`, `netstandard2.0`, `net48`

### Client Initialization

**Basic setup:**

```csharp
using OpenFga.Sdk.Client;
using OpenFga.Sdk.Configuration;

var configuration = new ClientConfiguration() {
    ApiUrl = "http://localhost:8080",
    StoreId = Environment.GetEnvironmentVariable("FGA_STORE_ID"),
    AuthorizationModelId = Environment.GetEnvironmentVariable("FGA_MODEL_ID"),
};
var fgaClient = new OpenFgaClient(configuration);
```

**With API Token:**

```csharp
using OpenFga.Sdk.Configuration;

var configuration = new ClientConfiguration() {
    ApiUrl = Environment.GetEnvironmentVariable("FGA_API_URL"),
    StoreId = Environment.GetEnvironmentVariable("FGA_STORE_ID"),
    Credentials = new Credentials() {
        Method = CredentialsMethod.ApiToken,
        Config = new CredentialsConfig() {
            ApiToken = Environment.GetEnvironmentVariable("FGA_API_TOKEN"),
        }
    }
};
var fgaClient = new OpenFgaClient(configuration);
```

**With Client Credentials (OAuth2):**

```csharp
var configuration = new ClientConfiguration() {
    ApiUrl = Environment.GetEnvironmentVariable("FGA_API_URL"),
    Credentials = new Credentials() {
        Method = CredentialsMethod.ClientCredentials,
        Config = new CredentialsConfig() {
            ApiTokenIssuer = Environment.GetEnvironmentVariable("FGA_API_TOKEN_ISSUER"),
            ApiAudience = Environment.GetEnvironmentVariable("FGA_API_AUDIENCE"),
            ClientId = Environment.GetEnvironmentVariable("FGA_CLIENT_ID"),
            ClientSecret = Environment.GetEnvironmentVariable("FGA_CLIENT_SECRET"),
        }
    }
};
var fgaClient = new OpenFgaClient(configuration);
```

### Load Authorization Model from File

**From JSON file:**

```csharp
using OpenFga.Sdk.Client.Model;

// Read and parse JSON file
var jsonContent = await File.ReadAllTextAsync("model.json");
var body = ClientWriteAuthorizationModelRequest.FromJson(jsonContent);

var response = await fgaClient.WriteAuthorizationModel(body);
```

**From DSL (.fga) file:**

The .NET SDK does not include a built-in DSL parser. Convert DSL files to JSON using the OpenFGA CLI, then load the JSON file.

```bash
# Convert DSL to JSON using the FGA CLI
fga model transform --input model.fga --output model.json
```

Then load the JSON file as shown above.

### Check Permission

```csharp
using OpenFga.Sdk.Client.Model;

var body = new ClientCheckRequest {
    User = "user:anne",
    Relation = "viewer",
    Object = "document:roadmap"
};
var response = await fgaClient.Check(body);
// response.Allowed = true/false
```

### Batch Check

```csharp
var options = new ClientBatchCheckOptions {
    MaxParallelRequests = 5,
    MaxBatchSize = 20,
};
var body = new ClientBatchCheckRequest {
    Checks = new List<ClientBatchCheckItem>() {
        new() {
            User = "user:anne",
            Relation = "viewer",
            Object = "document:roadmap",
            CorrelationId = "check-1",
        },
        new() {
            User = "user:bob",
            Relation = "editor",
            Object = "document:budget",
            CorrelationId = "check-2",
        }
    }
};
var response = await fgaClient.BatchCheck(body, options);
```

### Write Tuples

```csharp
var body = new ClientWriteRequest() {
    Writes = new List<ClientTupleKey> {
        new() {
            User = "user:anne",
            Relation = "viewer",
            Object = "document:roadmap",
        }
    },
    Deletes = new List<ClientTupleKeyWithoutCondition> {
        new() {
            User = "user:bob",
            Relation = "editor",
            Object = "document:budget",
        }
    },
};
var response = await fgaClient.Write(body);
```

### List Objects

```csharp
var body = new ClientListObjectsRequest {
    User = "user:anne",
    Relation = "viewer",
    Type = "document",
};
var response = await fgaClient.ListObjects(body);
// response.Objects contains accessible document IDs
```

### Streamed List Objects

```csharp
var options = new ClientListObjectsOptions {
    Consistency = ConsistencyPreference.HIGHERCONSISTENCY
};

var objects = new List<string>();
await foreach (var response in fgaClient.StreamedListObjects(
    new ClientListObjectsRequest {
        User = "user:anne",
        Relation = "can_read",
        Type = "document"
    },
    options)) {
    objects.Add(response.Object);
}
```

### List Relations

```csharp
var body = new ClientListRelationsRequest() {
    User = "user:anne",
    Object = "document:roadmap",
    Relations = new List<string> {"can_view", "can_edit", "can_delete"},
};
var response = await fgaClient.ListRelations(body);
// response.Relations contains applicable relations
```

### List Users

```csharp
using OpenFga.Sdk.Model;

var body = new ClientListUsersRequest() {
    Object = new FgaObject() {
        Type = "document",
        Id = "roadmap"
    },
    Relation = "can_read",
    UserFilters = new List<UserTypeFilter> {
        new() { Type = "user" }
    },
};
var response = await fgaClient.ListUsers(body);
```

### Read Tuples

```csharp
var body = new ClientReadRequest() {
    User = "user:anne",
    Relation = "viewer",
    Object = "document:roadmap",
};
var response = await fgaClient.Read(body);
```

### Non-Transaction Write Mode

```csharp
var options = new ClientWriteOptions {
    Transaction = new TransactionOptions() {
        Disable = true,
        MaxParallelRequests = 5,
        MaxPerChunk = 100,
    }
};
var response = await fgaClient.Write(body, options);
```

### Handle Write Conflicts

```csharp
var options = new ClientWriteOptions {
    Conflict = new ConflictOptions {
        OnDuplicateWrites = OnDuplicateWrites.Ignore,
        OnMissingDeletes = OnMissingDeletes.Ignore
    }
};
var response = await fgaClient.Write(body, options);
```

### Contextual Tuples

```csharp
var body = new ClientCheckRequest {
    User = "user:anne",
    Relation = "viewer",
    Object = "document:roadmap",
    ContextualTuples = new List<ClientTupleKey> {
        new() {
            User = "user:anne",
            Relation = "editor",
            Object = "document:roadmap",
        },
    },
};
var response = await fgaClient.Check(body);
```

### Retry Configuration

```csharp
var configuration = new ClientConfiguration() {
    ApiUrl = "http://localhost:8080",
    RetryParams = new RetryParams() {
        MaxRetry = 3,
        MinWaitInMs = 250
    }
};
var fgaClient = new OpenFgaClient(configuration);
```

### Per-Request Headers

```csharp
var options = new ClientCheckOptions {
    Headers = new Dictionary<string, string> {
        { "X-Request-ID", "123e4567-e89b-12d3-a456-426614174000" }
    }
};
var response = await fgaClient.Check(body, options);
```

### Best Practices

- **Initialize once:** Create `OpenFgaClient` once and reuse throughout your application
- **Async/await:** All methods are async - use `await` properly
- **Streaming:** Use `StreamedListObjects` with `await foreach` for large result sets
- **Retry behavior:** SDK auto-retries on 429 and 5xx errors (up to 3 times)
- **Retry-After:** SDK respects the `Retry-After` header with exponential backoff

---
## References

1. [OpenFGA Documentation](https://openfga.dev/docs)
2. [OpenFGA DSL Reference](https://openfga.dev/docs/configuration-language)
3. [OpenFGA CLI](https://github.com/openfga/cli)
4. [OpenFGA Sample Stores](https://github.com/openfga/sample-stores)
5. [Google Zanzibar Paper](https://research.google/pubs/pub48190/)
