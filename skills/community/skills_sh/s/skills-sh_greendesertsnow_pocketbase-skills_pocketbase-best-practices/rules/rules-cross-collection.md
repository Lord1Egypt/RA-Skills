---
title: Use @collection for Cross-Collection Lookups
impact: HIGH
impactDescription: Enables complex authorization without denormalization
tags: api-rules, security, cross-collection, relations
---

## Use @collection for Cross-Collection Lookups

The `@collection` reference allows rules to query other collections, enabling complex authorization patterns like role-based access, team membership, and resource permissions.

**Incorrect (denormalizing data for access control):**

```javascript
// Duplicating team membership in every resource
const documentsSchema = [
  { name: 'title', type: 'text' },
  { name: 'team', type: 'relation' },
  // Duplicated member list for access control - gets out of sync!
  { name: 'allowedUsers', type: 'relation', options: { maxSelect: 999 } }
];

// Rule checks duplicated data
listRule: 'allowedUsers ?= @request.auth.id'
// Problem: must update allowedUsers whenever team membership changes
```

**Correct (using @collection lookup):**

```javascript
// Clean schema - no duplication
const documentsSchema = [
  { name: 'title', type: 'text' },
  { name: 'team', type: 'relation', options: { collectionId: 'teams' } }
];

// Check team membership via @collection lookup
listRule: '@collection.team_members.user ?= @request.auth.id && @collection.team_members.team ?= team'

// Alternative: check if user is in team's members array
listRule: 'team.members ?= @request.auth.id'

// Role-based access via separate roles collection
listRule: '@collection.user_roles.user = @request.auth.id && @collection.user_roles.role = "admin"'
```

**Common patterns:**

```javascript
// Team-based access
// teams: { name, members (relation to users) }
// documents: { title, team (relation to teams) }
viewRule: 'team.members ?= @request.auth.id'

// Organization hierarchy
// orgs: { name }
// org_members: { org, user, role }
// projects: { name, org }
listRule: '@collection.org_members.org = org && @collection.org_members.user = @request.auth.id'

// Permission-based access
// permissions: { resource, user, level }
updateRule: '@collection.permissions.resource = id && @collection.permissions.user = @request.auth.id && @collection.permissions.level = "write"'

// Using aliases for complex queries
listRule: '@collection.memberships:m.user = @request.auth.id && @collection.memberships:m.team = team'
```

**Performance considerations:**
- Cross-collection lookups add query complexity
- Ensure referenced fields are indexed
- Consider caching for frequently accessed permissions
- Test performance with realistic data volumes

Reference: [PocketBase Collection Reference](https://pocketbase.io/docs/api-rules-and-filters/#collection-fields)
