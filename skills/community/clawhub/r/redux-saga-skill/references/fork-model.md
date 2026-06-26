---
title: Fork Model and Concurrency
impact: CRITICAL
tags: fork, spawn, cancellation, error-propagation, concurrency, task-lifecycle
---

# Fork Model and Concurrency

## Two Types of Forks

### Attached Forks (`fork`)

Created with `yield fork(fn, ...args)`. Attached to the parent saga.

**Lifecycle rules:**
1. Parent saga does not complete until all attached forks complete
2. Errors in any attached fork bubble up to the parent
3. When an error bubbles up, all sibling forks are cancelled
4. Cancelling the parent cancels all attached forks

```javascript
function* parentSaga() {
  // These are attached forks — parent waits for both
  const taskA = yield fork(workerA)
  const taskB = yield fork(workerB)
  // Parent body continues but won't "return" until both tasks finish

  // If workerA throws, workerB is cancelled and the error reaches here
}
```

**You cannot catch errors from forks directly.** The error propagates to whoever called the parent saga (the `call` site).

```javascript
// This does NOT work:
try {
  yield fork(failingSaga) // error won't be caught here
} catch (e) { /* never reached */ }

// Instead, catch at the call site:
function* rootSaga() {
  try {
    yield call(parentSaga) // errors from forks within parentSaga are caught HERE
  } catch (e) {
    console.error(e)
  }
}
```

### Detached Forks (`spawn`)

Created with `yield spawn(fn, ...args)`. Independent from parent.

**Lifecycle rules:**
1. Parent does not wait for spawned tasks
2. Errors do not bubble up
3. Cancelling the parent does not cancel spawned tasks
4. Behaves like a root saga started with `middleware.run()`

```javascript
function* parentSaga() {
  yield spawn(independentWorker) // fire and forget
  // If independentWorker fails, parent is unaffected
}
```

## Cancellation Semantics

### Manual Cancellation

```javascript
function* loginFlow() {
  while (true) {
    const { user, password } = yield take('LOGIN_REQUEST')
    const task = yield fork(authorize, user, password)

    const action = yield take(['LOGOUT', 'LOGIN_ERROR'])
    if (action.type === 'LOGOUT') {
      yield cancel(task) // cancel the auth task
    }
  }
}
```

### Cancellation Propagation

Cancellation propagates **downward** through the entire task tree:
- Cancelling a parent cancels all its attached forks
- Cancelling a task cancels any pending effect inside it
- Deeply nested `call` chains are unwound

Results and errors propagate **upward**.

### Cleanup After Cancellation

```javascript
function* backgroundSync() {
  try {
    while (true) {
      const data = yield call(fetchData)
      yield put(syncSuccess(data))
      yield delay(5000)
    }
  } finally {
    if (yield cancelled()) {
      // Cancellation-specific cleanup
      yield put(syncCancelled())
    }
    // Common cleanup runs on both normal exit and cancellation
  }
}
```

### Automatic Cancellation

Two scenarios trigger auto-cancellation:

1. **`race` effect** — losing effects are cancelled when the winner resolves
2. **`all` effect** — remaining effects are cancelled when any rejects

### Promise Cancellation

If a `call` effect is pending on a Promise when cancelled, redux-saga will invoke `promise[CANCEL]()` if defined. Libraries can use this for cleanup.

## Concurrency Patterns

### takeEvery — Concurrent Processing

Multiple saga instances run simultaneously. No ordering guarantee.

```javascript
yield takeEvery('FETCH_USER', fetchUser)
// If 3 FETCH_USER actions fire rapidly, 3 fetchUser instances run concurrently
```

**Use when:** all responses are needed, order doesn't matter.

### takeLatest — Latest Wins

New action cancels previous running instance.

```javascript
yield takeLatest('SEARCH', performSearch)
// Only the most recent search result is used
```

**Use when:** only the latest result matters (search, autocomplete).

### takeLeading — First Wins

Ignores actions while a saga instance is running.

```javascript
yield takeLeading('SUBMIT_ORDER', processOrder)
// Prevents duplicate order submissions
```

**Use when:** preventing duplicate work (form submissions, payments).

### actionChannel — Sequential Processing

Buffer actions and process one at a time.

```javascript
function* watchRequests() {
  const chan = yield actionChannel('REQUEST')
  while (true) {
    const action = yield take(chan)
    yield call(handleRequest, action) // blocks until done, then takes next
  }
}
```

**Use when:** requests must be processed in order, one at a time.

### Worker Pool — Limited Parallelism

Fork a fixed number of workers consuming from a shared channel.

```javascript
function* watchRequests() {
  const chan = yield actionChannel('REQUEST')
  // Fork 3 workers
  for (let i = 0; i < 3; i++) {
    yield fork(handleRequest, chan)
  }
}

function* handleRequest(chan) {
  while (true) {
    const action = yield take(chan)
    yield call(processRequest, action)
  }
}
```

## Root Saga Patterns

### Using `all` (blocks, error terminates all)

```javascript
export default function* rootSaga() {
  yield all([
    watchAuth(),
    watchFetch(),
    watchNotifications(),
  ])
}
```

If any saga throws, all are terminated. Simple but fragile.

### Using `fork` (non-blocking, error terminates all)

```javascript
export default function* rootSaga() {
  yield fork(watchAuth)
  yield fork(watchFetch)
  yield fork(watchNotifications)
}
```

Same error behavior as `all` but forks are non-blocking.

### Using `spawn` (isolated error boundaries)

```javascript
export default function* rootSaga() {
  yield spawn(watchAuth)
  yield spawn(watchFetch)
  yield spawn(watchNotifications)
}
```

Each saga is independent. Failure in one does not affect others. You must handle errors within each spawned saga.

### Spawn with Restart (use with caution)

```javascript
function* resilient(saga) {
  yield spawn(function* () {
    while (true) {
      try {
        yield call(saga)
        break // normal completion
      } catch (e) {
        console.error(`Saga ${saga.name} crashed, restarting:`, e)
      }
    }
  })
}

export default function* rootSaga() {
  yield resilient(watchAuth)
  yield resilient(watchFetch)
}
```

**Warning:** restarted sagas miss one-time actions dispatched before the crash. Use controlled failure over blanket restarts.
