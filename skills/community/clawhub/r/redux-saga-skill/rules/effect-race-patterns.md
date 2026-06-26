---
title: Race Effect Patterns
impact: HIGH
description: Use race for timeouts, cancellation, and competing effects. Losing effects are auto-cancelled.
tags: effects, race, timeout, cancellation
---

# Race Effect Patterns

## Timeout Pattern

```javascript
function* fetchWithTimeout(url) {
  const { response, timeout } = yield race({
    response: call(api.fetch, url),
    timeout: delay(5000),
  })

  if (timeout) {
    throw new Error('Request timed out')
  }

  return response
}
```

## Cancel on User Action

```javascript
function* uploadSaga(action) {
  const { success, cancel } = yield race({
    success: call(api.upload, action.payload.file),
    cancel: take('CANCEL_UPLOAD'),
  })

  if (cancel) {
    yield put(uploadCancelled())
  } else {
    yield put(uploadComplete(success))
  }
}
```

## Incorrect — Non-Blocking Inside Race

```javascript
// BAD: fork always wins instantly (non-blocking)
const result = yield race({
  task: fork(work),     // returns Task object immediately
  timeout: delay(5000), // never gets a chance
})

// BAD: put always wins instantly (non-blocking)
const result = yield race({
  dispatch: put(action), // completes immediately
  wait: take('OTHER'),   // never reached
})
```

## Key Rules

- All effects in `race` should be **blocking** (`call`, `take`, `delay`, `join`)
- The first to resolve wins; all others are **automatically cancelled**
- Array form: `yield race([call(a), delay(5000)])` — returns `[result, undefined]`
- Object form (preferred): named keys make intent clear
