---
title: Never Fork Inside Race
impact: HIGH
description: fork() inside race() is always a bug — forks are non-blocking and win immediately.
tags: fork, race, anti-pattern
---

# Never Fork Inside Race

## Problem

`fork` is non-blocking — it returns a Task immediately. Inside `race`, the fork always "wins" because it resolves before any blocking effect has a chance to complete.

## Incorrect

```javascript
// BUG: fork returns immediately, always wins the race
const { task, timeout } = yield race({
  task: fork(longRunningWork),
  timeout: delay(5000),
})
// timeout is always cancelled — fork always wins
```

## Correct

```javascript
// Use call (blocking) inside race
const { result, timeout } = yield race({
  result: call(longRunningWork),
  timeout: delay(5000),
})

if (timeout) {
  yield put(timeoutError())
}
```

## Alternative: Fork + Take Pattern

```javascript
const task = yield fork(longRunningWork)
const { timeout } = yield race({
  done: join(task),
  timeout: delay(5000),
})
if (timeout) {
  yield cancel(task)
}
```
