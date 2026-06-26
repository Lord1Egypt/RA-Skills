# Redux-Saga Anti-Patterns

## Table of Contents

- Missing yield
- Direct async calls
- Fork inside race
- Catching fork errors in parent
- Blanket auto-restart
- Wrong watcher for the job
- Mixing async patterns
- State path coupling
- Non-blocking inside race
- Side effects in generators without call
- Ignoring cancellation cleanup
- Monolithic root saga

## Missing yield

```javascript
// BAD: infinite synchronous loop — app freezes
while (true) {
  const action = take('REQUEST')
  call(fetchData, action.payload)
}

// GOOD: yield pauses the generator for the middleware
while (true) {
  const action = yield take('REQUEST')
  yield call(fetchData, action.payload)
}
```

## Direct async calls

```javascript
// BAD: not cancellable, not testable with deepEqual
function* fetchSaga() {
  const data = yield api.fetchData()
  yield put(dataLoaded(data))
}

// GOOD: use call() for middleware control
function* fetchSaga() {
  const data = yield call(api.fetchData)
  yield put(dataLoaded(data))
}
```

## Fork inside race

```javascript
// BAD: fork is non-blocking — always wins immediately
const { task, timeout } = yield race({
  task: fork(longRunning),
  timeout: delay(5000),
})

// GOOD: use blocking call inside race
const { result, timeout } = yield race({
  result: call(longRunning),
  timeout: delay(5000),
})

// GOOD: fork separately, join in race
const task = yield fork(longRunning)
const { done, timeout } = yield race({
  done: join(task),
  timeout: delay(5000),
})
if (timeout) yield cancel(task)
```

## Catching fork errors in parent

```javascript
// BAD: catch never reached — fork returns immediately
function* parent() {
  try {
    yield fork(failingSaga)
  } catch (e) {
    // NEVER REACHED
  }
}

// GOOD: catch at the call site
function* root() {
  try {
    yield call(parent)
  } catch (e) {
    // Errors from forks inside parent arrive here
  }
}

// GOOD: use spawn for isolation
function* root() {
  yield spawn(function* () {
    try {
      yield call(riskyWork)
    } catch (e) {
      yield put(workFailed(e.message))
    }
  })
}
```

## Blanket auto-restart

```javascript
// BAD: restarted sagas miss one-time actions (INIT, REHYDRATE)
function* restartable(saga) {
  yield spawn(function* () {
    while (true) {
      try {
        yield call(saga)
        break
      } catch (e) {
        console.error(`Restarting ${saga.name}`)
      }
    }
  })
}

// GOOD: handle errors explicitly, fail predictably
function* safeSaga(saga) {
  yield spawn(function* () {
    try {
      yield call(saga)
    } catch (e) {
      console.error(`${saga.name} failed:`, e)
      yield put(sagaCrashed(saga.name, e.message))
    }
  })
}
```

## Wrong watcher for the job

```javascript
// BAD: stale search results overwrite latest
yield takeEvery('SEARCH', performSearch)

// GOOD: only latest matters
yield takeLatest('SEARCH', performSearch)

// BAD: duplicate form submissions
yield takeEvery('SUBMIT_ORDER', processOrder)

// GOOD: ignore while processing
yield takeLeading('SUBMIT_ORDER', processOrder)
```

## Mixing async patterns

```javascript
// BAD: some features use thunks, some sagas, some direct fetch
// No consistent pattern for the team

// GOOD: pick one default
// - RTK Query for data fetching
// - Sagas only for complex workflows
// Document the decision and be consistent
```

## State path coupling

```javascript
// BAD: hardcoded state paths
function* saga() {
  const state = yield select()
  const user = state.auth.user
  const items = state.cart.items
}

// GOOD: reusable selectors
const getUser = (state) => state.auth.user
const getCartItems = (state) => state.cart.items

function* saga() {
  const user = yield select(getUser)
  const items = yield select(getCartItems)
}
```

## Non-blocking effects inside race

```javascript
// BAD: put is non-blocking — always resolves immediately
const { dispatched, timeout } = yield race({
  dispatched: put(action), // instant
  timeout: delay(5000),    // never reached
})

// GOOD: only use blocking effects in race
const { result, timeout } = yield race({
  result: call(asyncWork),
  timeout: delay(5000),
})
```

## Side effects without call

```javascript
// BAD: side effects inside the generator without call
function* saga() {
  localStorage.setItem('key', 'value') // not testable, not cancellable
  console.log('done') // can't be intercepted
}

// GOOD: wrap all side effects in call
function* saga() {
  yield call([localStorage, 'setItem'], 'key', 'value')
  yield call(console.log, 'done')
}
```

## Ignoring cancellation cleanup

```javascript
// BAD: leaves UI in loading state when cancelled
function* fetchSaga() {
  yield put(setLoading(true))
  const data = yield call(api.fetch)
  yield put(setLoading(false))
  yield put(dataLoaded(data))
  // If cancelled during api.fetch, setLoading(false) never fires
}

// GOOD: cleanup in finally
function* fetchSaga() {
  try {
    yield put(setLoading(true))
    const data = yield call(api.fetch)
    yield put(dataLoaded(data))
  } catch (e) {
    yield put(fetchFailed(e.message))
  } finally {
    yield put(setLoading(false))
    if (yield cancelled()) {
      yield put(fetchCancelled())
    }
  }
}
```

## Monolithic root saga

```javascript
// BAD: one crash kills everything
export default function* rootSaga() {
  yield all([
    watchAuth(),
    watchFetch(),
    watchAnalytics(),
  ])
}

// GOOD: isolated error boundaries
export default function* rootSaga() {
  yield spawn(watchAuth)
  yield spawn(watchFetch)
  yield spawn(watchAnalytics)
}
```
