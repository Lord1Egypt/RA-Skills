---
title: Use Auth Collections for User Accounts
impact: CRITICAL
impactDescription: Built-in authentication, password hashing, OAuth2 support
tags: collections, auth, users, authentication, design
---

## Use Auth Collections for User Accounts

Auth collections provide built-in authentication features including secure password hashing, email verification, OAuth2 support, and token management. Using base collections for users requires reimplementing these security-critical features.

**Incorrect (using base collection for users):**

```javascript
// Base collection loses all auth features
const usersCollection = {
  name: 'users',
  type: 'base',  // Wrong! No auth capabilities
  schema: [
    { name: 'email', type: 'email' },
    { name: 'password', type: 'text' },  // Stored in plain text!
    { name: 'name', type: 'text' }
  ]
};

// Manual login implementation - insecure
const user = await pb.collection('users').getFirstListItem(
  `email = "${email}" && password = "${password}"`  // SQL injection risk!
);
```

**Correct (using auth collection):**

```javascript
// Auth collection with built-in security
const usersCollection = {
  name: 'users',
  type: 'auth',  // Enables authentication features
  schema: [
    { name: 'name', type: 'text' },
    { name: 'avatar', type: 'file', options: { maxSelect: 1 } }
  ],
  options: {
    allowEmailAuth: true,
    allowOAuth2Auth: true,
    requireEmail: true,
    minPasswordLength: 8
  }
};

// Secure authentication with password hashing
const authData = await pb.collection('users').authWithPassword(
  'user@example.com',
  'securePassword123'
);

// Token automatically stored in authStore
// NOTE: Never log tokens in production - shown here for illustration only
console.log('Authenticated as:', pb.authStore.record.id);
```

**When to use each type:**
- **Auth collection**: User accounts, admin accounts, any entity that needs to log in
- **Base collection**: Regular data like posts, products, orders, comments
- **View collection**: Read-only aggregations or complex queries

Reference: [PocketBase Auth Collections](https://pocketbase.io/docs/collections/#auth-collection)
