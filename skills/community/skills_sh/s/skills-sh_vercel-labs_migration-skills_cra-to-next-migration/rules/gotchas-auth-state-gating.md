---
title: Wait for Auth State Before Checking Roles
impact: CRITICAL
impactDescription: Premature redirects during auth loading cause incorrect access denials
tags: gotchas, auth, roles, redirect, loading
---

## Wait for Auth State Before Checking Roles

Always wait for authentication to complete before checking roles or permissions. During initial render, auth state is typically undefined, causing premature redirects.

**Problem: Role check during auth loading**

```tsx
// BAD - Role is undefined during initial render
function ProtectedRoute({ children }) {
  const { userRole } = useAuth();

  if (userRole !== 'admin') {
    return <Navigate to="/" />; // Premature redirect!
  }

  return children;
}
```

This redirects users away before their actual role is loaded, even if they are admins.

**Solution: Check authenticating state first**

```tsx
// GOOD - Wait for auth to complete before checking role
function ProtectedRoute({ children }) {
  const { userRole, authenticating, authenticated } = useAuth();

  // 1. Still loading auth state - show loading
  if (authenticating) {
    return <LoadingSpinner />;
  }

  // 2. Auth complete, not logged in - redirect to login
  if (!authenticated) {
    return <Navigate to="/login" />;
  }

  // 3. Auth complete, wrong role - redirect to home
  if (userRole !== 'admin') {
    return <Navigate to="/" />;
  }

  // 4. Auth complete, correct role - render content
  return children;
}
```

**Pattern for Next.js App Router**

```tsx
// app/(protected)/layout.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

export default function ProtectedLayout({ children }) {
  const router = useRouter();
  const { authenticated, authenticating, userRole } = useAuth();

  useEffect(() => {
    // Only redirect after auth completes
    if (!authenticating) {
      if (!authenticated) {
        router.push('/login');
      } else if (userRole !== 'admin') {
        router.push('/');
      }
    }
  }, [authenticating, authenticated, userRole, router]);

  // Show loading while checking auth
  if (authenticating) {
    return <LoadingSpinner />;
  }

  // Don't render children until we know user has access
  if (!authenticated || userRole !== 'admin') {
    return null; // Will redirect via useEffect
  }

  return children;
}
```

**Auth state flow**

```
Initial render:
  authenticating: true
  authenticated: undefined
  userRole: undefined
  -> Show loading spinner

After auth check:
  authenticating: false
  authenticated: true/false
  userRole: 'admin' | 'user' | undefined
  -> Now safe to check roles and redirect
```

**Common mistakes:**

1. Using `||` instead of explicit checks:
   ```tsx
   // BAD - undefined || 'guest' evaluates to 'guest'
   const role = userRole || 'guest';
   ```

2. Not distinguishing between "not loaded" and "no role":
   ```tsx
   // BAD - Can't tell if role is loading or user has no role
   if (!userRole) redirect('/');
   ```

3. Checking auth in render without loading state:
   ```tsx
   // BAD - No loading state means flash of redirected content
   if (!authenticated) return <Navigate to="/login" />;
   ```
