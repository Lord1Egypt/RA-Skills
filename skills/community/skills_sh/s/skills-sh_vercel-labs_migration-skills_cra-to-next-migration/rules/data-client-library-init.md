---
title: Initialize Client-Only Libraries in useEffect
impact: MEDIUM
impactDescription: Module-level initialization of client libraries crashes on server
tags: data, initialization, ssr, client, i18n, analytics
---

## Initialize Client-Only Libraries in useEffect

Module-level initialization of client-only libraries runs on the server where browser APIs may not be available. Initialize these libraries in a client component's useEffect instead.

**Problem: Module-level initialization**

```typescript
// BAD - Runs on server during import
import i18n from 'i18next';

i18n.init({
  lng: localStorage.getItem('lang') || 'en', // localStorage undefined on server!
});

export default i18n;
```

```tsx
// This import triggers initialization on server
import '@/lib/i18n'; // Crashes: localStorage is not defined
```

**Solution: Initialize in useEffect with guard**

```tsx
// providers/ClientLibraryProvider.tsx
'use client';

import { useEffect, useState } from 'react';

export function ClientLibraryProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const init = async () => {
      // Safe to access browser APIs here
      await initializeLibrary();
      setReady(true);
    };

    init();
  }, []);

  if (!ready) {
    return null; // Or a loading skeleton
  }

  return <>{children}</>;
}
```

**Example: i18next**

```typescript
// lib/i18n.ts - Configuration only, no init call
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n.use(initReactI18next);

export const i18nConfig = {
  resources: { /* ... */ },
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
};

export default i18n;
```

```tsx
// providers/I18nProvider.tsx
'use client';

import { I18nextProvider } from 'react-i18next';
import { useEffect, useState } from 'react';
import i18n, { i18nConfig } from '@/lib/i18n';

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(i18n.isInitialized);

  useEffect(() => {
    if (!i18n.isInitialized) {
      i18n.init({
        ...i18nConfig,
        lng: localStorage.getItem('lang') || 'en',
      }).then(() => setReady(true));
    }
  }, []);

  if (!ready) return null;

  return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>;
}
```

**Example: Analytics (Segment, Mixpanel, etc.)**

```tsx
// providers/AnalyticsProvider.tsx
'use client';

import { useEffect, useRef } from 'react';
import { AnalyticsBrowser } from '@segment/analytics-next';

export const analytics = AnalyticsBrowser.load({ writeKey: '' }); // Lazy, doesn't run yet

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    // Now safe to initialize with browser context
    analytics.load({ writeKey: process.env.NEXT_PUBLIC_SEGMENT_KEY! });
  }, []);

  return <>{children}</>;
}
```

**Example: Feature flags (LaunchDarkly)**

```tsx
// providers/FeatureFlagProvider.tsx
'use client';

import { LDProvider } from 'launchdarkly-react-client-sdk';
import { useEffect, useState } from 'react';

export function FeatureFlagProvider({ children }: { children: React.ReactNode }) {
  const [clientId, setClientId] = useState<string | null>(null);

  useEffect(() => {
    // Can read from localStorage, cookies, or other browser APIs
    const userId = localStorage.getItem('userId') || 'anonymous';
    setClientId(userId);
  }, []);

  if (!clientId) return null;

  return (
    <LDProvider
      clientSideID={process.env.NEXT_PUBLIC_LD_CLIENT_ID!}
      context={{ kind: 'user', key: clientId }}
    >
      {children}
    </LDProvider>
  );
}
```

**Pattern summary:**

1. **Don't call initialization at module level** - It runs on the server
2. **Use `isInitialized` checks** - Many libraries provide this
3. **Initialize in useEffect** - Browser APIs are available
4. **Show loading state** - Return null or skeleton until ready
5. **Use refs for idempotency** - Prevent double-init in StrictMode

**Libraries that commonly need this pattern:**

- i18next / react-i18next
- Analytics (Segment, Mixpanel, Amplitude)
- Feature flags (LaunchDarkly, Split)
- Error tracking (Sentry browser SDK)
- Real-time services (Pusher, Ably)
- Any library that reads localStorage/cookies on init
