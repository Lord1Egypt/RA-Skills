---
title: Recipes and Common Patterns
impact: MEDIUM
tags: recipes, throttle, debounce, retry, undo, batching, login-flow, polling
---

# Recipes and Common Patterns

## Login / Logout Flow

Non-blocking auth with cancellation support:

```javascript
function* loginFlow() {
  while (true) {
    const { payload: { user, password } } = yield take('LOGIN_REQUEST')
    const task = yield fork(authorize, user, password)

    const action = yield take(['LOGOUT', 'LOGIN_ERROR'])
    if (action.type === 'LOGOUT') {
      yield cancel(task)
      yield call(api.clearToken)
    }
  }
}

function* authorize(user, password) {
  try {
    const token = yield call(api.login, user, password)
    yield put({ type: 'LOGIN_SUCCESS', token })
    yield call(api.saveToken, token)
  } catch (e) {
    yield put({ type: 'LOGIN_ERROR', error: e.message })
  } finally {
    if (yield cancelled()) {
      // cleanup on cancellation
    }
  }
}
```

## Polling

```javascript
function* pollSaga(action) {
  while (true) {
    try {
      const data = yield call(api.fetchStatus, action.payload.id)
      yield put(statusUpdated(data))

      if (data.status === 'complete') return

      yield delay(3000)
    } catch (e) {
      yield put(pollError(e.message))
      yield delay(10000) // back off on error
    }
  }
}

function* watchPoll() {
  while (true) {
    const action = yield take('START_POLLING')
    const task = yield fork(pollSaga, action)

    yield take('STOP_POLLING')
    yield cancel(task)
  }
}
```

## Optimistic Updates with Undo

```javascript
function* deleteSaga(action) {
  const { itemId } = action.payload

  // Optimistic: remove from UI immediately
  yield put(removeItem(itemId))
  yield put(showUndoToast(itemId))

  const { undo } = yield race({
    undo: take((a) => a.type === 'UNDO_DELETE' && a.payload.itemId === itemId),
    commit: delay(5000),
  })

  if (undo) {
    yield put(restoreItem(itemId))
  } else {
    yield call(api.deleteItem, itemId)
  }
}
```

## Pagination / Infinite Scroll

```javascript
function* loadMoreSaga() {
  let page = 1
  let hasMore = true

  while (hasMore) {
    yield take('LOAD_MORE')
    yield put(setLoading(true))

    const { items, total } = yield call(api.fetchItems, { page, limit: 20 })
    yield put(appendItems(items))

    page += 1
    hasMore = items.length > 0 && (page - 1) * 20 < total
    yield put(setLoading(false))
  }
}
```

## Request Deduplication

```javascript
const pending = new Map()

function* fetchWithDedup(action) {
  const key = action.payload.url

  if (pending.has(key)) {
    // Wait for the existing request
    const result = yield join(pending.get(key))
    yield put(fetchSuccess(result))
    return
  }

  const task = yield fork(function* () {
    try {
      const result = yield call(api.fetch, key)
      pending.delete(key)
      return result
    } catch (e) {
      pending.delete(key)
      throw e
    }
  })

  pending.set(key, task)
  const result = yield join(task)
  yield put(fetchSuccess(result))
}
```

## Batching Actions

Process multiple buffered actions as a single batch:

```javascript
function* batchProcessor() {
  const chan = yield actionChannel('ANALYTICS_EVENT')

  while (true) {
    yield delay(5000) // wait 5 seconds
    const events = yield flush(chan)
    if (events.length > 0) {
      yield call(api.sendAnalyticsBatch, events)
    }
  }
}
```

## Parallel Data Loading

```javascript
function* dashboardSaga() {
  yield put(dashboardLoading())

  const [users, stats, notifications] = yield all([
    call(api.fetchUsers),
    call(api.fetchStats),
    call(api.fetchNotifications),
  ])

  yield put(dashboardLoaded({ users, stats, notifications }))
}
```

## Timeout Wrapper

```javascript
function* withTimeout(saga, ms, ...args) {
  const { result, timeout } = yield race({
    result: call(saga, ...args),
    timeout: delay(ms),
  })

  if (timeout) {
    throw new Error(`Saga timed out after ${ms}ms`)
  }

  return result
}

// Usage
function* fetchSaga() {
  const data = yield call(withTimeout, api.fetchData, 5000)
  yield put(dataLoaded(data))
}
```
