---
title: Define Permissions with can_ Relations
---

## Define Permissions with can_ Relations

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
