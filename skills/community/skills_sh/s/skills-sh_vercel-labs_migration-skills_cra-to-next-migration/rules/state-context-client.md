---
title: Context Requires 'use client'
impact: HIGH
impactDescription: Context API needs client directive
tags: state, context, use-client
---

## Context Requires 'use client'

React Context uses hooks which require `'use client'`. Provider components must be Client Components.

**CRA Pattern (before):**

```tsx
// src/context/ThemeContext.tsx
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext(null)

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)

// src/App.tsx
function App() {
  return (
    <ThemeProvider>
      <Routes>{/* ... */}</Routes>
    </ThemeProvider>
  )
}
```

**Next.js Pattern (after):**

```tsx
// context/ThemeContext.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{
  theme: string
  setTheme: (theme: string) => void
} | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
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

// app/layout.tsx (Server Component)
import { ThemeProvider } from '@/context/ThemeContext'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

**Using context (requires 'use client'):**

```tsx
// components/ThemeToggle.tsx
'use client'

import { useTheme } from '@/context/ThemeContext'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle to {theme === 'light' ? 'dark' : 'light'}
    </button>
  )
}
```
