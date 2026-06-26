---
title: Always Yield Effects
impact: CRITICAL
description: Every effect creator must be yielded. Missing yield freezes the app.
tags: effects, yield, freeze, blocking
---

# Always Yield Effects

## Problem

Calling an effect creator without `yield` executes synchronously, returns a plain object, and the middleware never processes it. In a `while(true)` loop, this freezes the app.

## Incorrect

```javascript
function* watchRequests() {
  while (true) {
    // BUG: missing yield — infinite synchronous loop, app freezes
    const action = take('FETCH_REQUESTED')
    call(fetchData, action.payload)
  }
}
```

## Correct

```javascript
function* watchRequests() {
  while (true) {
    const action = yield take('FETCH_REQUESTED')
    yield call(fetchData, action.payload)
  }
}
```

## Why

`take()` and `call()` without `yield` return plain JS objects but never pause the generator. The middleware never gets a chance to process them, so the `while` loop runs infinitely on the main thread.
