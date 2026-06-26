---
title: Root Saga Error Boundaries
impact: HIGH
description: Structure root sagas with proper error isolation. Don't let one saga crash everything.
tags: error-handling, root-saga, spawn, error-boundaries
---

# Root Saga Error Boundaries

## Problem

Using `all()` or `fork()` in the root saga means one failing watcher kills all watchers.

## Incorrect

```javascript
// One crash kills everything
export default function* rootSaga() {
  yield all([
    watchAuth(),
    watchFetch(),     // if this throws, watchAuth is cancelled too
    watchAnalytics(),
  ])
}
```

## Correct — Spawn for Isolation

```javascript
export default function* rootSaga() {
  // Each watcher is independent — one crash doesn't affect others
  yield spawn(watchAuth)
  yield spawn(watchFetch)
  yield spawn(watchAnalytics)
}
```

## Correct — Spawn with Error Logging

```javascript
function* safeSaga(saga, ...args) {
  yield spawn(function* () {
    try {
      yield call(saga, ...args)
    } catch (e) {
      console.error(`Saga ${saga.name} failed:`, e)
      // Report to error tracking
    }
  })
}

export default function* rootSaga() {
  yield safeSaga(watchAuth)
  yield safeSaga(watchFetch)
  yield safeSaga(watchAnalytics)
}
```

## Caution: Don't Auto-Restart

```javascript
// RISKY: restarted sagas miss one-time actions like INIT or REHYDRATE
function* restartable(saga) {
  yield spawn(function* () {
    while (true) {
      try {
        yield call(saga)
        break
      } catch (e) {
        console.error(`Restarting ${saga.name}:`, e)
      }
    }
  })
}
```

Auto-restart can cause infinite crash loops if the saga depends on actions that were dispatched only once (e.g., during app initialization). Prefer explicit error handling over blanket restart.
