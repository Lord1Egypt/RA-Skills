---
title: Wildcards for boolean attributes
---

## Wildcards for Public Access

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
