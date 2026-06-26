---
title: Use call() for Async Functions
impact: CRITICAL
description: Never call async functions directly in a saga. Use yield call() for testability and middleware control.
tags: effects, call, async, testability
---

# Use call() for Async Functions

## Problem

Calling async functions directly bypasses the middleware. The saga can't be cancelled mid-call, and tests require mocking the actual function.

## Incorrect

```javascript
function* fetchUserSaga(action) {
  try {
    // BUG: direct call — not cancellable, not testable with deepEqual
    const user = yield api.fetchUser(action.payload.userId)
    yield put(fetchUserSuccess(user))
  } catch (e) {
    yield put(fetchUserFailure(e.message))
  }
}
```

## Correct

```javascript
function* fetchUserSaga(action) {
  try {
    const user = yield call(api.fetchUser, action.payload.userId)
    yield put(fetchUserSuccess(user))
  } catch (e) {
    yield put(fetchUserFailure(e.message))
  }
}
```

## Why

`call()` returns a plain object `{ CALL: { fn, args } }` that the middleware executes. This enables:
- **Testability** — assert with `deepEqual(gen.next().value, call(api.fetchUser, id))`
- **Cancellation** — middleware can cancel the pending call
- **Consistency** — all side effects flow through the middleware
