---
title: Wildcards for Public Access
---

## Wildcards for Public Access

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

