---
title: Naming Conventions
---

## Naming Conventions

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
