---
title: Throttle and Debounce Patterns
impact: MEDIUM
description: Rate-limit saga execution for UI events like scroll, resize, and search input.
tags: throttle, debounce, rate-limiting, performance
---

# Throttle and Debounce Patterns

## Throttle — Max Once Per Interval

```javascript
import { throttle } from 'redux-saga/effects'

// Handle scroll events at most once every 200ms
yield throttle(200, 'WINDOW_SCROLLED', updateScrollPosition)
```

## Debounce — Wait for Silence

```javascript
import { debounce } from 'redux-saga/effects'

// Wait 300ms after last keystroke before searching
yield debounce(300, 'SEARCH_INPUT_CHANGED', performSearch)
```

## Retry with Backoff

```javascript
import { retry } from 'redux-saga/effects'

function* submitFormSaga(action) {
  try {
    // Retry up to 3 times with 2s between attempts
    const result = yield retry(3, 2000, api.submit, action.payload)
    yield put(submitSuccess(result))
  } catch (e) {
    yield put(submitFailed(e.message))
  }
}
```

## Manual Retry with Exponential Backoff

```javascript
function* fetchWithBackoff(fn, ...args) {
  for (let i = 0; i < 5; i++) {
    try {
      return yield call(fn, ...args)
    } catch (e) {
      if (i < 4) {
        const backoff = Math.min(1000 * Math.pow(2, i), 30000)
        yield delay(backoff)
      } else {
        throw e
      }
    }
  }
}
```

## Undo Pattern

```javascript
function* archiveThread(action) {
  yield put(showUndoToast())
  yield put(optimisticallyArchive(action.threadId))

  const { undo } = yield race({
    undo: take('UNDO_ARCHIVE'),
    commit: delay(5000),
  })

  if (undo) {
    yield put(restoreThread(action.threadId))
  } else {
    yield call(api.archiveThread, action.threadId)
  }
}
```
