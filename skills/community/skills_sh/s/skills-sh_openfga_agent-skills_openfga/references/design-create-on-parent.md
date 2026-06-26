---
title: Check Create Permissions on Parent Objects
---

## Check Create Permissions on Parent Objects

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
