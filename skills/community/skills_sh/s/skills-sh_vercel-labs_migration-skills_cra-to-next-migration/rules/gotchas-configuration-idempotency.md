---
title: Ensure Configuration Idempotency with useRef
impact: HIGH
impactDescription: React StrictMode and fast refresh cause double initialization without guards
tags: gotchas, configuration, useRef, StrictMode, initialization
---

## Ensure Configuration Idempotency with useRef

Prevent duplicate initialization of services using refs. React 18+ StrictMode intentionally double-invokes effects in development, and Fast Refresh can re-run initialization code.

**Problem: Double initialization**

```tsx
// BAD - Runs twice in StrictMode, causes errors or duplicate side effects
function AppProviders({ children }) {
  useEffect(() => {
    configureAmplify();      // Called twice!
    initializeAnalytics();   // Duplicate events sent
    setupErrorTracking();    // Double initialization error
  }, []);

  return <>{children}</>;
}
```

**Solution: Use useRef to track initialization**

```tsx
// GOOD - Only initializes once regardless of StrictMode
function AppProviders({ children }) {
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    // One-time initialization - safe from double invocation
    configureAmplify();
    initializeAnalytics();
    setupErrorTracking();
  }, []);

  return <>{children}</>;
}
```

**Pattern for multiple services**

Track each service separately if they have different initialization requirements:

```tsx
'use client';

function AppProviders({ children }) {
  const amplifyInit = useRef(false);
  const analyticsInit = useRef(false);
  const knockInit = useRef(false);

  useEffect(() => {
    if (!amplifyInit.current) {
      amplifyInit.current = true;
      configureAmplify();
    }

    if (!analyticsInit.current) {
      analyticsInit.current = true;
      initializeAnalytics();
    }

    if (!knockInit.current) {
      knockInit.current = true;
      initializeKnock();
    }
  }, []);

  return <>{children}</>;
}
```

**Why this works:**

1. `useRef` values persist across re-renders
2. `useRef` values are NOT reset when StrictMode double-invokes effects
3. The check happens synchronously before any async work
4. Works correctly with Fast Refresh during development

**Alternative: Module-level singleton (for non-React code)**

For configuration that must happen outside React components:

```typescript
// src/config/amplify.ts
let configured = false;

export function configureAmplifyOnce() {
  if (configured) return;
  configured = true;

  Amplify.configure(amplifyConfig);
}
```

**When to use which pattern:**

| Scenario | Pattern |
|----------|---------|
| React component initialization | `useRef` in `useEffect` |
| Library that provides `isConfigured` check | Use library's built-in check |
| Module-level singletons | Module variable flag |
| Async configuration with race potential | Promise singleton (see `gotchas-auth-race-conditions`) |

**Common services that need idempotency:**

- AWS Amplify
- Firebase
- Analytics (GA, Segment, Mixpanel)
- Error tracking (Sentry)
- Real-time services (Pusher, Knock)
- Feature flags (LaunchDarkly)
