---
title: Handle Context Providers Properly
impact: HIGH
impactDescription: Context requires special setup
tags: components, context, providers
---

## Handle Context Providers Properly

React Context uses `useContext` which requires `'use client'`. Wrap providers at the right level in your app.

**CRA Pattern (before):**

```tsx
// src/App.tsx
import { ThemeProvider } from './ThemeContext'
import { AuthProvider } from './AuthContext'

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <Router>
          <Routes>{/* ... */}</Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  )
}
```

**Next.js Pattern (after):**

```tsx
// providers/Providers.tsx
'use client'

import { ThemeProvider } from './ThemeContext'
import { AuthProvider } from './AuthContext'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </AuthProvider>
  )
}

// app/layout.tsx (Server Component)
import { Providers } from '@/providers/Providers'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

**Creating a context:**

```tsx
// contexts/ThemeContext.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{
  theme: string
  setTheme: (theme: string) => void
} | null>(null)

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}
```

**Using context (requires 'use client'):**

```tsx
// components/ThemeToggle.tsx
'use client'

import { useTheme } from '@/contexts/ThemeContext'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>
}
```
