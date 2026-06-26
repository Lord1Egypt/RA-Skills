---
title: Configure Provider Hierarchy Correctly
impact: HIGH
impactDescription: Incorrect provider order causes context and styling failures
tags: gotchas, providers, context, layout
---

## Configure Provider Hierarchy Correctly

Provider order matters. Providers can only access context from providers above them in the tree. Incorrect ordering causes runtime errors, styling issues, or missing context.

**Recommended provider order:**

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>                              {/* 1. Auth (outermost) */}
          <CSSRegistryProvider>                     {/* 2. CSS-in-JS */}
            <DataProvider>                          {/* 3. Data fetching */}
              <ThemeProvider>                       {/* 4. Theme */}
                <I18nProvider>                      {/* 5. Internationalization */}
                  <Suspense fallback={<Loading />}> {/* 6. Suspense boundary */}
                    <AppContextProvider>            {/* 7. App-specific contexts */}
                      {children}
                    </AppContextProvider>
                  </Suspense>
                </I18nProvider>
              </ThemeProvider>
            </DataProvider>
          </CSSRegistryProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
```

**Why this order matters:**

1. **AuthProvider (outermost)** - Everything needs to know the current user. Data fetching needs auth tokens, themes may be user-specific, etc.

2. **CSSRegistryProvider** - CSS-in-JS libraries (styled-components, Emotion) must use `useServerInsertedHTML` for SSR. Needs to wrap everything that uses styled components.

3. **DataProvider (React Query/SWR)** - Provides cache for all components. May need auth context for authenticated requests.

4. **ThemeProvider** - UI components need theme context. May depend on user preferences from auth.

5. **I18nProvider** - Text throughout app needs translations. Must be client-side (`'use client'`).

6. **Suspense** - Required for `useSearchParams()`, lazy loading, and streaming. Should wrap app content.

7. **AppContextProvider** - Business-specific contexts (organization, notifications, feature flags). Can depend on all above.

**CSS-in-JS Registry pattern (styled-components):**

```tsx
// providers/CSSRegistryProvider.tsx
'use client';

import { useServerInsertedHTML } from 'next/navigation';
import { useState } from 'react';
import { ServerStyleSheet, StyleSheetManager } from 'styled-components';

export function CSSRegistryProvider({ children }: { children: React.ReactNode }) {
  const [sheet] = useState(() => new ServerStyleSheet());

  useServerInsertedHTML(() => {
    const styles = sheet.getStyleElement();
    sheet.instance.clearTag();
    return <>{styles}</>;
  });

  if (typeof window !== 'undefined') return <>{children}</>;

  return (
    <StyleSheetManager sheet={sheet.instance}>
      {children}
    </StyleSheetManager>
  );
}
```

**Common ordering mistakes:**

```tsx
// BAD - Theme can't access user preferences
<ThemeProvider>
  <AuthProvider>  {/* Auth inside Theme */}
    {children}
  </AuthProvider>
</ThemeProvider>

// BAD - Styled components won't SSR correctly
<DataProvider>
  <CSSRegistryProvider>  {/* Should be outside DataProvider */}
    {children}
  </CSSRegistryProvider>
</DataProvider>

// BAD - useSearchParams will error without Suspense
<AppProvider>
  {children}  {/* No Suspense boundary */}
</AppProvider>
```

**Client vs Server provider separation:**

```tsx
// app/layout.tsx (Server Component)
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>  {/* Can be server or client depending on auth lib */}
          <ClientProviders>  {/* All client providers in one wrapper */}
            {children}
          </ClientProviders>
        </AuthProvider>
      </body>
    </html>
  );
}

// providers/ClientProviders.tsx
'use client';

export function ClientProviders({ children }) {
  return (
    <CSSRegistryProvider>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <I18nProvider>
            <Suspense fallback={<Loading />}>
              {children}
            </Suspense>
          </I18nProvider>
        </ThemeProvider>
      </QueryClientProvider>
    </CSSRegistryProvider>
  );
}
```

**Debugging provider issues:**

| Symptom | Likely Cause |
|---------|--------------|
| `useContext` returning `undefined` | Component outside its provider |
| Styles not applying on first load | CSS-in-JS registry missing or misplaced |
| Hydration mismatch | Client-only provider rendering different content |
| `useSearchParams` throwing | Missing Suspense boundary |
| Auth state undefined in data fetching | DataProvider outside AuthProvider |
