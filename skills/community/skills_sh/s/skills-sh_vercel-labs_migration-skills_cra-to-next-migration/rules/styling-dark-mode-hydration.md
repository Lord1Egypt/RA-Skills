---
title: Handle Dark Mode Without Hydration Mismatch
impact: HIGH
impactDescription: Reading theme from localStorage during SSR causes hydration errors
tags: styling, dark-mode, hydration, localStorage, theme
---

## Handle Dark Mode Without Hydration Mismatch

Dark mode implementations that read from localStorage during render cause hydration mismatches. The server doesn't have access to localStorage, so it renders a different theme than the client.

**Problem: Immediate localStorage access**

```tsx
// BAD - Server renders 'light', client may render 'dark'
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(
    localStorage.getItem('theme') || 'light'  // localStorage undefined on server!
  );

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}
```

**Solution: Use mounted state pattern**

```tsx
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext<{
  theme: string;
  setTheme: (theme: string) => void;
}>({ theme: 'light', setTheme: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Read from localStorage only after mount
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
    document.documentElement.classList.toggle('dark', saved === 'dark');
    setMounted(true);
  }, []);

  const updateTheme = (newTheme: string) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return null; // Or a theme-neutral skeleton
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme: updateTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

**Theme toggle component:**

```tsx
'use client';

import { useTheme } from './ThemeProvider';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  // Component only renders after ThemeProvider is mounted
  const toggle = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <button onClick={toggle} aria-label="Toggle theme">
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

**Tailwind dark mode configuration:**

```typescript
// tailwind.config.ts
const config = {
  darkMode: 'selector', // Uses .dark class on html element
  // ...
};

export default config;
```

```css
/* styles/globals.css */
:root {
  --background: #ffffff;
  --foreground: #000000;
}

.dark {
  --background: #0a0a0a;
  --foreground: #ededed;
}

body {
  background: var(--background);
  color: var(--foreground);
}
```

**Skeleton approach for less layout shift:**

```tsx
export function ThemeProvider({ children }) {
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
    document.documentElement.classList.toggle('dark', saved === 'dark');
    setMounted(true);
  }, []);

  if (!mounted) {
    // Return a neutral skeleton that works in both themes
    return (
      <div className="min-h-screen bg-neutral-100 dark:bg-neutral-900">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

**Script-based flash prevention (advanced):**

To prevent any flash at all, inject a blocking script in the head:

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                const theme = localStorage.getItem('theme') || 'light';
                document.documentElement.classList.toggle('dark', theme === 'dark');
              })();
            `,
          }}
        />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

Note: `suppressHydrationWarning` on `<html>` is needed because the script modifies the DOM before React hydrates.
