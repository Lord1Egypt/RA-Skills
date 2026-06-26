---
title: Use Impersonation for Admin Operations
impact: MEDIUM
impactDescription: Safe admin access to user data without password sharing
tags: authentication, admin, impersonation, superuser
---

## Use Impersonation for Admin Operations

Impersonation allows superusers to generate tokens for other users, enabling admin support tasks and API key functionality without sharing passwords.

**Incorrect (sharing credentials or bypassing auth):**

```javascript
// Bad: sharing user passwords for support
async function helpUser(userId, userPassword) {
  await pb.collection('users').authWithPassword(userEmail, userPassword);
  // Support team knows user's password!
}

// Bad: directly modifying records without proper context
async function fixUserData(userId) {
  // Bypasses user's perspective and rules
  await pb.collection('posts').update(postId, { fixed: true });
}
```

**Correct (using impersonation):**

```javascript
import PocketBase from 'pocketbase';

// Admin client with superuser auth (use environment variables, never hardcode)
const adminPb = new PocketBase(process.env.PB_URL);
await adminPb.collection('_superusers').authWithPassword(
  process.env.PB_SUPERUSER_EMAIL,
  process.env.PB_SUPERUSER_PASSWORD
);

async function impersonateUser(userId) {
  // Generate impersonation token (non-renewable)
  const impersonatedClient = await adminPb
    .collection('users')
    .impersonate(userId, 3600);  // 1 hour duration

  // impersonatedClient has user's auth context
  console.log('Acting as:', impersonatedClient.authStore.record.email);

  // Operations use user's permissions
  const userPosts = await impersonatedClient.collection('posts').getList();

  return impersonatedClient;
}

// Use case: Admin viewing user's data
async function adminViewUserPosts(userId) {
  const userClient = await impersonateUser(userId);

  // See exactly what the user sees (respects API rules)
  const posts = await userClient.collection('posts').getList();

  return posts;
}

// Use case: API keys for server-to-server communication
async function createApiKey(serviceUserId) {
  // Create a service impersonation token (use short durations, rotate regularly)
  const serviceClient = await adminPb
    .collection('service_accounts')
    .impersonate(serviceUserId, 86400);  // 24 hours max, rotate via scheduled task

  // Return token for service to use
  return serviceClient.authStore.token;
}

// Using API key token in another service
async function useApiKey(apiToken) {
  const pb = new PocketBase('http://127.0.0.1:8090');

  // Manually set the token
  pb.authStore.save(apiToken, null);

  // Now requests use the service account's permissions
  const data = await pb.collection('data').getList();
  return data;
}
```

**Important considerations:**

```javascript
// Impersonation tokens are non-renewable
const client = await adminPb.collection('users').impersonate(userId, 3600);

// This will fail - can't refresh impersonation tokens
try {
  await client.collection('users').authRefresh();
} catch (error) {
  // Expected: impersonation tokens can't be refreshed
}

// For continuous access, generate new token when needed
async function getImpersonatedClient(userId) {
  // Check if existing token is still valid
  if (cachedClient?.authStore.isValid) {
    return cachedClient;
  }

  // Generate fresh token
  return await adminPb.collection('users').impersonate(userId, 3600);
}
```

**Security best practices:**
- Use short durations for support tasks
- Log all impersonation events
- Restrict impersonation to specific admin roles
- Never expose impersonation capability in client code
- Use dedicated service accounts for API keys

Reference: [PocketBase Impersonation](https://pocketbase.io/docs/authentication/#impersonate-authentication)
