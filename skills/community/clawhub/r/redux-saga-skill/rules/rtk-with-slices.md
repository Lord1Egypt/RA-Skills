---
title: Sagas with RTK Slices
impact: MEDIUM
description: Use action creators from createSlice to type-safely connect sagas to Redux Toolkit slices.
tags: rtk, slices, actions, typescript, modern-redux
---

# Sagas with RTK Slices

## Problem

Hardcoding action type strings in sagas creates a maintenance burden and misses TypeScript safety.

## Incorrect

```javascript
// BUG: string mismatch — 'users/fetchUsers' vs 'user/fetchUsers'
function* watchFetch() {
  yield takeLatest('users/fetchUsers', fetchUsersSaga)
}

function* fetchUsersSaga() {
  const data = yield call(api.fetchUsers)
  yield put({ type: 'users/setUsers', payload: data }) // typo-prone
}
```

## Correct

```typescript
// usersSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UsersState {
  list: User[]
  loading: boolean
  error: string | null
}

const usersSlice = createSlice({
  name: 'users',
  initialState: { list: [], loading: false, error: null } as UsersState,
  reducers: {
    fetchUsers(state) {
      state.loading = true
    },
    fetchUsersSuccess(state, action: PayloadAction<User[]>) {
      state.list = action.payload
      state.loading = false
    },
    fetchUsersFailure(state, action: PayloadAction<string>) {
      state.error = action.payload
      state.loading = false
    },
  },
})

export const { fetchUsers, fetchUsersSuccess, fetchUsersFailure } = usersSlice.actions
export default usersSlice.reducer
```

```typescript
// usersSaga.ts
import { takeLatest, call, put } from 'redux-saga/effects'
import { fetchUsers, fetchUsersSuccess, fetchUsersFailure } from './usersSlice'
import * as api from '../api'

function* fetchUsersSaga() {
  try {
    const users: User[] = yield call(api.fetchUsers)
    yield put(fetchUsersSuccess(users))
  } catch (e: any) {
    yield put(fetchUsersFailure(e.message))
  }
}

export function* watchUsers() {
  // Type-safe: fetchUsers.type is 'users/fetchUsers'
  yield takeLatest(fetchUsers.type, fetchUsersSaga)
}
```

## Benefits

- Action types are derived from the slice — no string duplication
- TypeScript catches mismatches at compile time
- Refactoring the slice name updates all references
- Action creators provide payload typing
