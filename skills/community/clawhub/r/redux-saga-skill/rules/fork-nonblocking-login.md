---
title: Non-Blocking Auth Flow
impact: HIGH
description: Use fork+take+cancel for login flows that stay responsive to logout during auth.
tags: fork, auth, login, non-blocking, cancel
---

# Non-Blocking Auth Flow

## Problem

A blocking `call` during login prevents the saga from responding to `LOGOUT` dispatched while the API request is in flight.

## Incorrect

```javascript
// BAD: blocked during login — LOGOUT is missed
function* loginFlow() {
  while (true) {
    const { payload } = yield take('LOGIN_REQUEST')
    const token = yield call(api.login, payload) // blocked here
    // If user dispatches LOGOUT during api.login, it's ignored
    yield put(loginSuccess(token))
    yield take('LOGOUT')
    yield call(api.clearToken)
  }
}
```

## Correct

```javascript
function* loginFlow() {
  while (true) {
    const { payload } = yield take('LOGIN_REQUEST')
    const task = yield fork(authorize, payload)

    const action = yield take(['LOGOUT', 'LOGIN_ERROR'])
    if (action.type === 'LOGOUT') {
      yield cancel(task)
      yield call(api.clearToken)
    }
  }
}

function* authorize({ user, password }) {
  try {
    const token = yield call(api.login, user, password)
    yield put(loginSuccess(token))
    yield call(api.saveToken, token)
  } catch (e) {
    yield put(loginError(e.message))
  } finally {
    if (yield cancelled()) {
      // cleanup if cancelled during API call
    }
  }
}
```

## Why This Works

1. `fork(authorize)` returns immediately — saga stays responsive
2. `take(['LOGOUT', 'LOGIN_ERROR'])` listens for either event
3. If `LOGOUT` arrives during the API call, the auth task is cancelled
4. The `authorize` generator runs its `finally` block for cleanup
