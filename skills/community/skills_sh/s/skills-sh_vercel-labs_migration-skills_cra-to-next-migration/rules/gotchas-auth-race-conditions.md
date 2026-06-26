---
title: Guard Against Auth/API Race Conditions
impact: CRITICAL
impactDescription: API calls failing before authentication/configuration completes is the most common migration breaking issue
tags: gotchas, auth, race-condition, api
---

## Guard Against Auth/API Race Conditions

The most critical migration issue: API calls executing before authentication or configuration is ready. In CRA, everything loads client-side so timing is predictable. In Next.js with SSR, components may render before async configuration completes.

**Problem: React Query hooks run immediately**

```tsx
// BAD - Hook runs immediately, before auth is configured
function MyComponent() {
  const { data } = useQuery({ queryKey: ['data'], queryFn: fetchData });
  // fetchData fails because auth isn't configured yet
}
```

**Solution 1: Guard API helpers with ensureConfigured pattern**

Create a singleton promise that ensures configuration happens exactly once:

```typescript
// src/config/auth.ts
let configured = false;
let configuring: Promise<void> | null = null;

export async function ensureAuthConfigured(): Promise<void> {
  if (configured) return;

  if (configuring) {
    await configuring;
    return;
  }

  configuring = (async () => {
    // Replace with your auth provider's configuration
    await initializeAuth();
    configured = true;
  })();

  await configuring;
}
```

**Examples for common auth providers:**

```typescript
// AWS Amplify
import { Amplify } from 'aws-amplify';
import amplifyConfig from './amplify-config';

configuring = (async () => {
  Amplify.configure(amplifyConfig);
  configured = true;
})();

// Firebase
import { initializeApp, getApps } from 'firebase/app';
import { firebaseConfig } from './firebase-config';

configuring = (async () => {
  if (!getApps().length) {
    initializeApp(firebaseConfig);
  }
  configured = true;
})();

// Auth0
import { Auth0Client } from '@auth0/auth0-spa-js';

let auth0Client: Auth0Client | null = null;

configuring = (async () => {
  auth0Client = new Auth0Client({
    domain: process.env.NEXT_PUBLIC_AUTH0_DOMAIN!,
    clientId: process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID!,
  });
  configured = true;
})();
```

Add the guard to ALL API functions:

```typescript
// src/actions/api.ts
export const fetchData = async () => {
  await ensureAuthConfigured(); // Add to ALL API functions
  return apiCall('/data');
};

export const updateData = async (params: UpdateParams) => {
  await ensureAuthConfigured(); // Must be in every function
  return apiCall('/data', { method: 'PATCH', body: params });
};
```

**Solution 2: Gate queries on auth state**

Use React Query's `enabled` flag to wait for auth:

```tsx
function MyComponent() {
  const { isAuthenticated, isLoading } = useAuth();

  const { data } = useQuery({
    queryKey: ['data'],
    queryFn: fetchData,
    enabled: !isLoading && isAuthenticated, // Wait for auth to complete
  });

  if (isLoading) return <LoadingSpinner />;

  return <div>{data?.value}</div>;
}
```

**Best practice: Use both approaches**

The `ensureConfigured` pattern protects against any code path calling the API too early, while `enabled` provides better UX by not showing loading states for queries that won't run yet.

```tsx
// API layer has guard
export const fetchUserData = async (userId: string) => {
  await ensureAuthConfigured();
  return apiCall(`/users/${userId}`);
};

// Component also gates on auth for better UX
function UserProfile({ userId }) {
  const { isAuthenticated, isLoading } = useAuth();

  const { data, isLoading: isQueryLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUserData(userId),
    enabled: isAuthenticated && !isLoading,
  });

  if (isLoading) return <AuthCheckingSpinner />;
  if (!isAuthenticated) return <LoginPrompt />;
  if (isQueryLoading) return <ProfileSkeleton />;

  return <Profile user={data} />;
}
```

**Common symptoms of this issue:**

- Auth provider "not configured" errors
- API calls returning 401/403 intermittently
- Data loading correctly on page refresh but not initial navigation
- Queries failing only in production or only on first load
