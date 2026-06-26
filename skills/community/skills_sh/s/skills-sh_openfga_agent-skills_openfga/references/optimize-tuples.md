---
title: Minimize Tuple Count
---

## Minimize Tuple Count

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
