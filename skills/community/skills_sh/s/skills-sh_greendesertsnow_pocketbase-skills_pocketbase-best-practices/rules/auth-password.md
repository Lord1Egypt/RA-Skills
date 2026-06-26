---
title: Implement Secure Password Authentication
impact: CRITICAL
impactDescription: Secure user login with proper error handling and token management
tags: authentication, password, login, security
---

## Implement Secure Password Authentication

Password authentication should include proper error handling, avoid exposing whether emails exist, and correctly manage the auth store.

**Incorrect (exposing information and poor error handling):**

```javascript
// Dangerous: exposes whether email exists
async function login(email, password) {
  const user = await pb.collection('users').getFirstListItem(`email = "${email}"`);
  if (!user) {
    throw new Error('Email not found');  // Reveals email doesn't exist
  }

  // Manual password check - never do this!
  if (user.password !== password) {
    throw new Error('Wrong password');  // Reveals password is wrong
  }

  return user;
}
```

**Correct (secure authentication):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

async function login(email, password) {
  try {
    // authWithPassword handles hashing and returns token
    const authData = await pb.collection('users').authWithPassword(email, password);

    // Token is automatically stored in pb.authStore
    console.log('Logged in as:', authData.record.email);
    console.log('Token valid:', pb.authStore.isValid);

    return authData;
  } catch (error) {
    // Generic error message - don't reveal if email exists
    if (error.status === 400) {
      throw new Error('Invalid email or password');
    }
    throw error;
  }
}

// Check if user is authenticated
function isAuthenticated() {
  return pb.authStore.isValid;
}

// Get current user
function getCurrentUser() {
  return pb.authStore.record;
}

// Logout
function logout() {
  pb.authStore.clear();
}

// Listen for auth changes
pb.authStore.onChange((token, record) => {
  console.log('Auth state changed:', record?.email || 'logged out');
}, true);  // true = fire immediately with current state
```

**Auth collection configuration for password auth:**

```javascript
// When creating auth collection via API (superuser only)
await pb.collections.create({
  name: 'users',
  type: 'auth',
  fields: [
    { name: 'name', type: 'text' },
    { name: 'avatar', type: 'file', options: { maxSelect: 1 } }
  ],
  passwordAuth: {
    enabled: true,
    identityFields: ['email', 'username']  // Fields that can be used to login
  },
  // Require minimum password length
  // (configured in Admin UI under collection options)
});
```

**Security considerations:**
- Never store passwords in plain text
- Use generic error messages
- Implement rate limiting on your server
- Consider adding MFA for sensitive applications

Reference: [PocketBase Auth](https://pocketbase.io/docs/authentication/)
