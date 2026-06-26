---
title: Understand API Rule Types and Defaults
impact: CRITICAL
impactDescription: Prevents unauthorized access, data leaks, and security vulnerabilities
tags: api-rules, security, access-control, authorization
---

## Understand API Rule Types and Defaults

PocketBase uses five collection-level rules to control access. Understanding the difference between locked (null), open (""), and expression rules is critical for security.

**Incorrect (leaving rules open unintentionally):**

```javascript
// Collection with overly permissive rules
const collection = {
  name: 'messages',
  listRule: '',      // Anyone can list all messages!
  viewRule: '',      // Anyone can view any message!
  createRule: '',    // Anyone can create messages!
  updateRule: '',    // Anyone can update any message!
  deleteRule: ''     // Anyone can delete any message!
};
// Complete security bypass - all data exposed
```

**Correct (explicit, restrictive rules):**

```javascript
// Collection with proper access control
const collection = {
  name: 'messages',
  // null = locked, only superusers can access
  listRule: null,    // Default: locked to superusers

  // '' (empty string) = open to everyone (use sparingly)
  viewRule: '@request.auth.id != ""',  // Any authenticated user

  // Expression = conditional access
  createRule: '@request.auth.id != ""',  // Must be logged in
  updateRule: 'author = @request.auth.id',  // Only author
  deleteRule: 'author = @request.auth.id'   // Only author
};
```

**Rule types explained:**

| Rule Value | Meaning | Use Case |
|------------|---------|----------|
| `null` | Locked (superusers only) | Admin-only data, system tables |
| `''` (empty string) | Open to everyone | Public content, no auth required |
| `'expression'` | Conditional access | Most common - check auth, ownership |

**Common patterns:**

```javascript
// Public read, authenticated write (enforce ownership on create)
listRule: '',
viewRule: '',
createRule: '@request.auth.id != "" && @request.body.author = @request.auth.id',
updateRule: 'author = @request.auth.id',
deleteRule: 'author = @request.auth.id'

// Private to owner only
listRule: 'owner = @request.auth.id',
viewRule: 'owner = @request.auth.id',
createRule: '@request.auth.id != ""',
updateRule: 'owner = @request.auth.id',
deleteRule: 'owner = @request.auth.id'

// Read-only public data
listRule: '',
viewRule: '',
createRule: null,
updateRule: null,
deleteRule: null
```

**Error responses by rule type:**
- List rule fail: 200 with empty items
- View/Update/Delete fail: 404 (hides existence)
- Create fail: 400
- Locked rule violation: 403

Reference: [PocketBase API Rules](https://pocketbase.io/docs/api-rules-and-filters/)
