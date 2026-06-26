---
title: Polling Pattern
impact: MEDIUM
description: Implement cancellable polling with backoff on error using fork+take+cancel.
tags: recipes, polling, cancel, backoff
---

# Polling Pattern

## Problem

Polling needs to be cancellable, handle errors gracefully, and not leak tasks when the user navigates away.

## Incorrect

```javascript
// BAD: not cancellable, no error handling, runs forever
function* pollSaga() {
  while (true) {
    const data = yield call(api.fetchStatus)
    yield put(statusUpdated(data))
    yield delay(3000)
  }
}
```

## Correct

```javascript
function* pollWorker(id) {
  try {
    while (true) {
      try {
        const data = yield call(api.fetchStatus, id)
        yield put(statusUpdated(data))

        if (data.status === 'complete') return // stop when done

        yield delay(3000)
      } catch (e) {
        yield put(pollError(e.message))
        yield delay(10000) // back off on error
      }
    }
  } finally {
    if (yield cancelled()) {
      yield put(pollingStopped())
    }
  }
}

function* watchPoll() {
  while (true) {
    const action = yield take('START_POLLING')
    const task = yield fork(pollWorker, action.payload.id)
    yield take('STOP_POLLING')
    yield cancel(task)
  }
}
```

## Key Points

- Fork the poll worker so the watcher stays responsive
- Cancel on `STOP_POLLING` or component unmount
- Use `finally` + `cancelled()` for cleanup
- Back off on error to avoid hammering a failing server
- Check for completion inside the loop to stop naturally
