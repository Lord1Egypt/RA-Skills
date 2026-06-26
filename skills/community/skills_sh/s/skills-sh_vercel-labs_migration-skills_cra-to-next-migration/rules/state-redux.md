---
title: Configure Redux with Next.js
impact: MEDIUM
impactDescription: Redux requires special setup
tags: state, redux, configuration
---

## Configure Redux with Next.js

Redux requires special configuration for Next.js to handle server-side rendering properly.

**CRA Pattern (before):**

```tsx
// src/store.ts
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './features/counter'

export const store = configureStore({
  reducer: { counter: counterReducer },
})

// src/index.tsx
import { Provider } from 'react-redux'
import { store } from './store'

<Provider store={store}>
  <App />
</Provider>
```

**Next.js Pattern (after):**

```tsx
// lib/store.ts
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './features/counter'

export const makeStore = () => {
  return configureStore({
    reducer: { counter: counterReducer },
  })
}

export type AppStore = ReturnType<typeof makeStore>
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']

// lib/hooks.ts
import { useDispatch, useSelector, useStore } from 'react-redux'
import type { AppDispatch, RootState, AppStore } from './store'

export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
export const useAppSelector = useSelector.withTypes<RootState>()
export const useAppStore = useStore.withTypes<AppStore>()

// lib/StoreProvider.tsx
'use client'

import { useRef } from 'react'
import { Provider } from 'react-redux'
import { makeStore, AppStore } from './store'

export default function StoreProvider({ children }: { children: React.ReactNode }) {
  const storeRef = useRef<AppStore>()
  if (!storeRef.current) {
    storeRef.current = makeStore()
  }

  return <Provider store={storeRef.current}>{children}</Provider>
}

// app/layout.tsx
import StoreProvider from '@/lib/StoreProvider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <StoreProvider>{children}</StoreProvider>
      </body>
    </html>
  )
}
```

**Using Redux (requires 'use client'):**

```tsx
// components/Counter.tsx
'use client'

import { useAppSelector, useAppDispatch } from '@/lib/hooks'
import { increment } from '@/lib/features/counter'

export function Counter() {
  const count = useAppSelector((state) => state.counter.value)
  const dispatch = useAppDispatch()

  return <button onClick={() => dispatch(increment())}>{count}</button>
}
```

## Redux Toolkit v2 Breaking Changes

When upgrading to React 19, you must upgrade to `@reduxjs/toolkit` v2 and `react-redux` v9. RTK v2 removes the object notation for `extraReducers`:

**RTK v1 (no longer works):**

```tsx
const slice = createSlice({
  name: 'leads',
  initialState,
  extraReducers: {
    [getLeadsContent.pending]: (state) => { state.isLoading = true },
    [getLeadsContent.fulfilled]: (state, action) => {
      state.isLoading = false
      state.data = action.payload
    }
  }
})
```

**RTK v2 (builder callback required):**

```tsx
const slice = createSlice({
  name: 'leads',
  initialState,
  extraReducers: (builder) => {
    builder
      .addCase(getLeadsContent.pending, (state) => {
        state.isLoading = true
      })
      .addCase(getLeadsContent.fulfilled, (state, action) => {
        state.isLoading = false
        state.data = action.payload
      })
  }
})
```
