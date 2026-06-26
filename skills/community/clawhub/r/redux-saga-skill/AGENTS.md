# Redux-Saga — Complete Guide

> This document is for AI agents and LLMs to follow when writing, reviewing, or debugging redux-saga code. It compiles all rules and references into a single executable guide.

**Baseline:** redux-saga 1.4.2 with Redux Toolkit (`configureStore`)

---

## Abstract

Redux-Saga is generator-based middleware for managing complex side effects in Redux applications. Use it for workflow orchestration — parallel tasks, cancellation, racing, channels, and long-running background processes. For data fetching, prefer RTK Query. For simple async, prefer `createAsyncThunk`. For reactive slice logic, prefer `createListenerMiddleware`.

---

## Table of Contents

1. [Effects & Yielding](#1-effects--yielding) — CRITICAL
2. [Fork Model & Concurrency](#2-fork-model--concurrency) — CRITICAL
3. [Testing](#3-testing) — HIGH
4. [Error Handling](#4-error-handling) — HIGH
5. [Channels & External I/O](#5-channels--external-io) — MEDIUM
6. [Recipes & Patterns](#6-recipes--patterns) — MEDIUM
7. [RTK Integration](#7-rtk-integration) — MEDIUM
8. [Troubleshooting](#8-troubleshooting) — LOW

---

## 1. Effects & Yielding
**Impact: CRITICAL**

### Rule: Always Yield Effects

Every effect creator must be `yield`ed. Missing `yield` creates a synchronous infinite loop that freezes the app.

```javascript
// INCORRECT — app freezes
while (true) {
  const action = take('REQUEST')
  call(fetchData, action.payload)
}

// CORRECT
while (true) {
  const action = yield take('REQUEST')
  yield call(fetchData, action.payload)
}
```

### Rule: Use call() for Async Functions

Never call async functions directly. Use `yield call()` for testability, cancellation, and middleware control.

```javascript
// INCORRECT — not testable, not cancellable
const user = yield api.fetchUser(id)

// CORRECT
const user = yield call(api.fetchUser, id)
```

`call()` returns `{ CALL: { fn, args } }` — a plain object the middleware executes. Tests use `deepEqual` instead of mocks.

### Rule: Choose the Right Watcher

| Scenario | Watcher | Why |
|----------|---------|-----|
| Search / autocomplete | `takeLatest` | Cancel stale requests |
| Form submission / payment | `takeLeading` | Prevent duplicate processing |
| Notifications / logging | `takeEvery` | Process every event |
| Sequential queue | `actionChannel` + `take` | One at a time, in order |
| Rate-limited UI events | `throttle` | Max once per interval |
| Wait for typing to stop | `debounce` | After silence period |

### Effect Creators Quick Reference

| Effect | Blocking | Purpose |
|--------|----------|---------|
| `take(pattern)` | Yes | Wait for matching action |
| `takeMaybe(pattern)` | Yes | Like `take`, receives `END` |
| `takeEvery(pattern, saga)` | No | Concurrent on every match |
| `takeLatest(pattern, saga)` | No | Cancel previous, run latest |
| `takeLeading(pattern, saga)` | No | Ignore until current completes |
| `put(action)` | No | Dispatch action |
| `putResolve(action)` | Yes | Dispatch, wait for promise |
| `call(fn, ...args)` | Yes | Call, wait for result |
| `apply(ctx, fn, [args])` | Yes | Call with context |
| `cps(fn, ...args)` | Yes | Node-style callback |
| `fork(fn, ...args)` | No | Attached fork |
| `spawn(fn, ...args)` | No | Detached fork |
| `join(task)` | Yes | Wait for task |
| `cancel(task)` | No | Cancel task |
| `cancel()` | No | Self-cancel |
| `select(selector)` | Yes | Query store state |
| `actionChannel(pattern)` | No | Buffer actions |
| `flush(channel)` | Yes | Drain buffered messages |
| `cancelled()` | Yes | Check cancellation in `finally` |
| `delay(ms)` | Yes | Pause execution |
| `throttle(ms, pattern, saga)` | No | Rate-limit |
| `debounce(ms, pattern, saga)` | No | Wait for silence |
| `retry(n, delay, fn)` | Yes | Retry with backoff |
| `race(effects)` | Yes | First wins |
| `all([effects])` | Yes | Parallel, wait all |
| `setContext(props)` | No | Update context |
| `getContext(prop)` | Yes | Read context |

### Pattern Matching

`take`, `takeEvery`, `takeLatest`, `takeLeading`, `throttle`, `debounce` accept:

- `'*'` or omitted — all actions
- `'ACTION_TYPE'` — exact match
- `[type1, type2]` — any in array
- `fn => boolean` — custom predicate

---

## 2. Fork Model & Concurrency
**Impact: CRITICAL**

### Rule: Attached vs Detached Forks

| | `fork` (attached) | `spawn` (detached) |
|---|---|---|
| Parent waits for child | Yes | No |
| Child error crashes parent | Yes | No |
| Parent cancel cancels child | Yes | No |
| Use when | Child is part of the workflow | Child is independent |

```javascript
// Attached: analytics failure would crash checkout — BAD
yield fork(processPayment)
yield fork(trackAnalytics) // throws → processPayment cancelled

// Correct: analytics is independent
yield fork(processPayment)
yield spawn(trackAnalytics)
```

### Rule: Fork Error Propagation

You **cannot** catch errors from `fork()` in a try/catch around the fork. Errors bubble to the `call()` site that invoked the parent.

```javascript
// INCORRECT — catch never reached
try {
  yield fork(failingSaga)
} catch (e) { /* never reached */ }

// CORRECT — catch at the call site
function* root() {
  try {
    yield call(parentSaga) // errors from forks arrive here
  } catch (e) { ... }
}
```

### Rule: Never Fork Inside Race

`fork` is non-blocking — it always wins the race immediately. Use `call` inside `race`.

```javascript
// INCORRECT — fork always wins
yield race({ task: fork(work), timeout: delay(5000) })

// CORRECT
yield race({ result: call(work), timeout: delay(5000) })
```

### Concurrency Patterns

**actionChannel — Sequential Processing:**
```javascript
const chan = yield actionChannel('REQUEST')
while (true) {
  const action = yield take(chan)
  yield call(handleRequest, action)
}
```

**Worker Pool — Limited Parallelism:**
```javascript
const chan = yield actionChannel('REQUEST')
for (let i = 0; i < 3; i++) yield fork(worker, chan)
```

---

## 3. Testing
**Impact: HIGH**

### Rule: Prefer Integration Tests

Use `expectSaga` from `redux-saga-test-plan`. It doesn't couple tests to effect ordering.

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), user]])
    .put(fetchUserSuccess(user))
    .run()
})

it('handles error', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), throwError(new Error('500'))]])
    .put(fetchUserFailure('500'))
    .run()
})
```

### Rule: Use Providers for Mocking

Static providers with partial matchers are preferred:

```javascript
.provide([
  [matchers.call.fn(api.fetchUser), mockUser],       // match function, any args
  [matchers.select.selector(getToken), 'mock-token'], // mock selector
  [matchers.call.fn(api.save), throwError(error)],    // simulate error
])
```

### Rule: Test Sagas with Reducers

```javascript
it('loads users into state', () => {
  return expectSaga(loadUsersSaga)
    .withReducer(usersReducer)
    .provide([[matchers.call.fn(api.fetchUsers), users]])
    .hasFinalState({ users, loading: false, error: null })
    .run()
})
```

### Unit Testing (When Order Matters)

```javascript
import { testSaga } from 'redux-saga-test-plan'

testSaga(checkoutSaga, action)
  .next()
  .put(showLoading())       // must be first
  .next()
  .call(api.processPayment) // must be second
  .next()
  .isDone()
```

### Testing Without Libraries (runSaga)

```javascript
async function recordSaga(saga, action, state = {}) {
  const dispatched = []
  await runSaga(
    { dispatch: (a) => dispatched.push(a), getState: () => state },
    saga, action,
  ).toPromise()
  return dispatched
}
```

### Vitest / Jest

Both work identically. `expectSaga.run()` returns a Promise:
- Jest: `return expectSaga(saga).run()`
- Vitest: `await expectSaga(saga).run()`

---

## 4. Error Handling
**Impact: HIGH**

### Rule: Cancellation Cleanup with finally

```javascript
function* syncSaga() {
  try {
    while (true) {
      yield call(fetchData)
      yield delay(10000)
    }
  } finally {
    if (yield cancelled()) {
      yield put(syncCancelled())
    }
  }
}
```

Cancellation propagates **downward** through attached forks. Each cancelled generator jumps to its `finally` block.

### Rule: Root Saga Error Boundaries

```javascript
// INCORRECT — one crash kills all
yield all([watchAuth(), watchFetch(), watchAnalytics()])

// CORRECT — isolated error boundaries
function* safeSaga(saga) {
  yield spawn(function* () {
    try {
      yield call(saga)
    } catch (e) {
      console.error(`${saga.name} failed:`, e)
    }
  })
}

export default function* rootSaga() {
  yield safeSaga(watchAuth)
  yield safeSaga(watchFetch)
  yield safeSaga(watchAnalytics)
}
```

---

## 5. Channels & External I/O
**Impact: MEDIUM**

### eventChannel — External Events

```javascript
function createSocketChannel(socket) {
  return eventChannel((emit) => {
    socket.on('message', emit)
    socket.on('close', () => emit(END))
    return () => socket.close()
  })
}
```

### Buffer Types

| Buffer | On Overflow |
|--------|------------|
| `buffers.none()` | Drops |
| `buffers.fixed(n)` | Throws |
| `buffers.expanding(n)` | Grows |
| `buffers.dropping(n)` | Drops newest |
| `buffers.sliding(n)` | Drops oldest |

### runSaga — Outside Redux

```javascript
runSaga({ channel, dispatch, getState }, mySaga)
```

---

## 6. Recipes & Patterns
**Impact: MEDIUM**

- **Login flow:** `fork` auth + `take(['LOGOUT', 'LOGIN_ERROR'])` + `cancel`
- **Polling:** `while(true)` + `call` + `delay` in a forked task, cancel on `STOP`
- **Optimistic update:** `put(optimistic)` + `race({ undo: take('UNDO'), commit: delay(5000) })`
- **Pagination:** `take('LOAD_MORE')` in a loop, track page/hasMore
- **Batching:** `actionChannel` + `flush` on interval
- **Timeout wrapper:** `race({ result: call(saga), timeout: delay(ms) })`
- **Parallel loading:** `yield all([call(a), call(b), call(c)])`

See `references/recipes.md` for full code examples.

---

## 7. RTK Integration
**Impact: MEDIUM**

### configureStore Setup

```javascript
import createSagaMiddleware from 'redux-saga'
import { configureStore } from '@reduxjs/toolkit'

const sagaMiddleware = createSagaMiddleware()

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefault) => getDefault().concat(sagaMiddleware),
})

sagaMiddleware.run(rootSaga) // AFTER store creation
```

### Sagas with RTK Slices

Use action creators from `createSlice` — no string duplication:

```typescript
import { fetchUsers } from './usersSlice'

yield takeLatest(fetchUsers.type, fetchUsersSaga)
yield put(fetchUsersSuccess(users))
```

### When to Use What

| Need | Tool |
|------|------|
| Data fetching + caching | RTK Query |
| Simple async | `createAsyncThunk` |
| Reactive slice logic | `createListenerMiddleware` |
| Workflows, cancellation, channels | Redux-Saga |

---

## 8. Troubleshooting
**Impact: LOW**

| Symptom | Cause | Fix |
|---------|-------|-----|
| App freezes | Missing `yield` in loop | Add `yield` before every effect |
| Missed actions | Saga blocked on `call` | Use `fork` to stay responsive |
| Bad stack traces | Async generators | `onError` with `sagaStack`, `babel-plugin-redux-saga` |
| Saga doesn't start | `run()` before store | Call `run()` after `configureStore` |
| `yield` returns `any` (TS) | TS can't infer generators | Type manually or use `typed-redux-saga` |
| Effect not executing | Missing `yield` before effect | `yield put(action)` not `put(action)` |

---

## Prerequisites

- `redux-saga` ^1.4.2
- `@reduxjs/toolkit` (recommended)
- `redux-saga-test-plan` (for testing)
- Node.js with ES2015 generator support (all modern runtimes)

## License

MIT
