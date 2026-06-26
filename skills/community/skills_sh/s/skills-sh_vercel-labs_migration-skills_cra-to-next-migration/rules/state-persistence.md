---
title: Handle State Persistence
impact: MEDIUM
impactDescription: localStorage/sessionStorage patterns
tags: state, persistence, storage
---

## Handle State Persistence

Handle localStorage and sessionStorage properly to avoid hydration issues.

**CRA Pattern (before):**

```tsx
// Direct localStorage access works fine
const [value, setValue] = useState(() => {
  return localStorage.getItem('key') || 'default'
})

useEffect(() => {
  localStorage.setItem('key', value)
}, [value])
```

**Next.js Pattern (after):**

```tsx
'use client'

import { useState, useEffect } from 'react'

function useLocalStorage<T>(key: string, initialValue: T) {
  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(initialValue)
  const [isHydrated, setIsHydrated] = useState(false)

  // After hydration, read from localStorage
  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key)
      if (item) {
        setStoredValue(JSON.parse(item))
      }
    } catch (error) {
      console.error(error)
    }
    setIsHydrated(true)
  }, [key])

  // Save to localStorage
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue, isHydrated] as const
}

// Usage
function Settings() {
  const [theme, setTheme, isHydrated] = useLocalStorage('theme', 'light')

  if (!isHydrated) {
    return <SettingsSkeleton /> // Consistent SSR
  }

  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value)}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  )
}
```

**Using Zustand with persistence:**

```tsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'settings' }
  )
)
```

**Using cookies instead (SSR-friendly):**

```tsx
// Cookies work on server and client
import { cookies } from 'next/headers'

// Server Component
export default function Page() {
  const theme = cookies().get('theme')?.value || 'light'
  return <ThemeProvider theme={theme}>{/* ... */}</ThemeProvider>
}
```
