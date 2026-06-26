---
title: Cancellation Cleanup with finally
impact: HIGH
description: Always use try/finally with cancelled() check for proper cleanup on cancellation.
tags: error-handling, cancellation, finally, cleanup
---

# Cancellation Cleanup with finally

## Problem

When a saga is cancelled (via `cancel()`, `race` loser, or parent cancellation), any pending effect is aborted. Without cleanup, resources leak and state becomes inconsistent.

## Incorrect

```javascript
function* syncSaga() {
  while (true) {
    yield put(syncStarted())
    const data = yield call(fetchData)
    yield put(syncCompleted(data))
    yield delay(10000)
  }
  // If cancelled during fetchData, syncStarted was dispatched
  // but syncCompleted never fires — UI stuck in "syncing" state
}
```

## Correct

```javascript
function* syncSaga() {
  try {
    while (true) {
      yield put(syncStarted())
      const data = yield call(fetchData)
      yield put(syncCompleted(data))
      yield delay(10000)
    }
  } finally {
    if (yield cancelled()) {
      // Cancellation-specific cleanup
      yield put(syncCancelled())
    }
    // Common cleanup (runs on both normal exit and cancellation)
    yield put(syncStopped())
  }
}
```

## Cancellation Propagation

Cancellation flows **downward** through the task tree:

```
cancel(parentTask)
  → cancels parent's current pending effect
    → cancels all attached forks of parent
      → cancels all their attached forks (recursive)
```

Each cancelled generator jumps to its `finally` block.
