---
title: Manage Auth Tokens Properly
impact: CRITICAL
impactDescription: Prevents unauthorized access, handles token expiration gracefully
tags: authentication, tokens, refresh, security, session
---

## Manage Auth Tokens Properly

Auth tokens should be refreshed before expiration, validated on critical operations, and properly cleared on logout. The SDK's authStore handles most of this automatically.

**Incorrect (ignoring token expiration):**

```javascript
// Bad: never checking token validity
async function fetchUserData() {
  // Token might be expired!
  const records = await pb.collection('posts').getList();
  return records;
}

// Bad: manually managing tokens
let authToken = localStorage.getItem('token');
fetch('/api/posts', {
  headers: { 'Authorization': authToken }  // Token might be invalid
});
```

**Correct (proper token management):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// Check token validity before operations
async function fetchSecureData() {
  // authStore.isValid is a client-side check only (JWT expiry parsing).
  // Always verify server-side with authRefresh() for critical operations.
  if (!pb.authStore.isValid) {
    throw new Error('Please log in');
  }

  return pb.collection('posts').getList();
}

// Refresh token periodically or before expiration
async function refreshAuthIfNeeded() {
  if (!pb.authStore.isValid) {
    return false;
  }

  try {
    // Verifies current token and returns fresh one
    await pb.collection('users').authRefresh();
    console.log('Token refreshed');
    return true;
  } catch (error) {
    // Token invalid - user needs to re-authenticate
    pb.authStore.clear();
    return false;
  }
}

// Auto-refresh on app initialization
async function initializeAuth() {
  if (pb.authStore.token) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }
}

// Listen for auth changes and handle expiration
pb.authStore.onChange((token, record) => {
  if (!token) {
    // User logged out or token cleared
    redirectToLogin();
  }
});

// Setup periodic refresh (e.g., every 10 minutes)
setInterval(async () => {
  if (pb.authStore.isValid) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }
}, 10 * 60 * 1000);
```

**SSR / Server-side token handling:**

```javascript
// Server-side: create fresh client per request
export async function handleRequest(request) {
  const pb = new PocketBase('http://127.0.0.1:8090');

  // Load auth from cookie
  pb.authStore.loadFromCookie(request.headers.get('cookie') || '');

  // Validate and refresh
  if (pb.authStore.isValid) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }

  // ... handle request ...

  // Send updated cookie with secure options
  const response = new Response();
  response.headers.set('set-cookie', pb.authStore.exportToCookie({
    httpOnly: true,   // Prevent XSS access to auth token
    secure: true,     // HTTPS only
    sameSite: 'Lax',  // CSRF protection
  }));
  return response;
}
```

**Token configuration (Admin UI or migration):**

```javascript
// Configure token durations (superuser only)
await pb.collections.update('users', {
  authToken: {
    duration: 1209600  // 14 days in seconds
  },
  verificationToken: {
    duration: 604800   // 7 days
  }
});
```

Reference: [PocketBase Auth Store](https://pocketbase.io/docs/authentication/)
