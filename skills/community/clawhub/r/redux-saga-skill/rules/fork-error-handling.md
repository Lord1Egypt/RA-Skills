---
title: Fork Error Propagation
impact: CRITICAL
description: You cannot catch errors from fork() directly. Errors bubble to the parent's caller.
tags: fork, error-handling, try-catch, bubbling
---

# Fork Error Propagation

## Problem

Wrapping `fork()` in try/catch does nothing — the fork is non-blocking and returns immediately. The error surfaces at the `call()` site that invoked the parent.

## Incorrect

```javascript
function* parentSaga() {
  try {
    yield fork(failingSaga) // returns immediately — no error here
  } catch (e) {
    // NEVER REACHED — fork errors don't land here
    console.error(e)
  }
}
```

## Correct

```javascript
// Catch at the call site
function* rootSaga() {
  try {
    yield call(parentSaga) // errors from forks within parentSaga arrive HERE
  } catch (e) {
    yield put(globalError(e.message))
  }
}

function* parentSaga() {
  yield fork(workerA) // if this throws, error goes to rootSaga's catch
  yield fork(workerB) // workerB is cancelled when workerA throws
}
```

## Alternative: Spawn for Isolation

```javascript
function* rootSaga() {
  yield spawn(independentWorker) // errors are silenced — handle inside
}

function* independentWorker() {
  try {
    yield call(riskyOperation)
  } catch (e) {
    yield put(workerFailed(e.message)) // handle error within the spawned task
  }
}
```
