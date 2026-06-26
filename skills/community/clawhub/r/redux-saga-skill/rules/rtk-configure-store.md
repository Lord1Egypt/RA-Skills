---
title: Redux Toolkit Integration
impact: MEDIUM
description: Integrate redux-saga with configureStore from Redux Toolkit. Handle middleware defaults correctly.
tags: rtk, redux-toolkit, configureStore, middleware
---

# Redux Toolkit Integration

## Problem

Redux Toolkit's `configureStore` includes thunk middleware by default. Adding saga middleware incorrectly can break the default middleware chain or duplicate thunk.

## Incorrect

```javascript
// BUG: replaces all default middleware (loses thunk, serializability check, immutability check)
const store = configureStore({
  reducer: rootReducer,
  middleware: [sagaMiddleware],
})
```

## Correct

```javascript
import { configureStore } from '@reduxjs/toolkit'
import createSagaMiddleware from 'redux-saga'
import rootSaga from './sagas'

const sagaMiddleware = createSagaMiddleware()

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(sagaMiddleware),
})

sagaMiddleware.run(rootSaga)

export default store
```

## With TypeScript

```typescript
import { configureStore } from '@reduxjs/toolkit'
import createSagaMiddleware from 'redux-saga'
import rootSaga from './sagas'

const sagaMiddleware = createSagaMiddleware()

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      // Disable serializable check for saga effects if needed
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }).concat(sagaMiddleware),
})

sagaMiddleware.run(rootSaga)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

## When to Use Saga vs RTK Alternatives

| Need | Tool |
|------|------|
| Data fetching + caching | RTK Query |
| Simple async (submit → set status) | `createAsyncThunk` |
| Reactive logic within slices | `createListenerMiddleware` |
| Complex orchestration, cancellation, parallel tasks, channels | Redux-Saga |

Don't mix async patterns without reason. Pick one default for data fetching and use sagas only for workflow orchestration.
