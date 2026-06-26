---
title: Troubleshooting Frozen Apps and Missed Actions
impact: LOW
description: Common debugging scenarios — app freezes, missed actions, unreadable stack traces.
tags: troubleshooting, debugging, freeze, missed-actions, stack-traces
---

# Troubleshooting Frozen Apps and Missed Actions

## App Freezes After Adding a Saga

**Cause:** Missing `yield` before an effect in a `while` loop.

```javascript
// BUG: take() returns plain object, never pauses — infinite loop
while (true) {
  const action = take('REQUEST') // missing yield
}

// FIX: add yield
while (true) {
  const action = yield take('REQUEST')
}
```

## Saga Misses Dispatched Actions

**Cause:** Saga is blocked on a `call` when the action arrives.

```javascript
// BUG: during the blocking call, LOGIN_ERROR actions are dropped
function* loginSaga() {
  const token = yield call(api.login, credentials) // blocked here
  // If LOGIN_ERROR is dispatched during the call, saga never sees it
}

// FIX: use fork for non-blocking execution
function* loginSaga() {
  const task = yield fork(api.login, credentials)
  const action = yield take(['LOGIN_SUCCESS', 'LOGIN_ERROR', 'LOGOUT'])
  if (action.type === 'LOGOUT') {
    yield cancel(task)
  }
}
```

## Unreadable Error Stack Traces

**Cause:** Async generator chains lose stack context.

**Fix 1:** Use `onError` callback:

```javascript
const sagaMiddleware = createSagaMiddleware({
  onError: (error, { sagaStack }) => {
    console.error('Saga error:', error.message)
    console.error('Saga stack:', sagaStack)
  },
})
```

**Fix 2:** Install `babel-plugin-redux-saga` for development:

```javascript
// babel.config.js
module.exports = {
  plugins: [
    process.env.NODE_ENV === 'development' && 'redux-saga',
  ].filter(Boolean),
}
```

## Saga Doesn't Start

**Cause:** `sagaMiddleware.run()` called before store is created, or saga is not a generator function.

```javascript
// BUG: run() before configureStore
sagaMiddleware.run(rootSaga)
const store = configureStore(...)

// FIX: run() after store creation
const store = configureStore(...)
sagaMiddleware.run(rootSaga)
```
