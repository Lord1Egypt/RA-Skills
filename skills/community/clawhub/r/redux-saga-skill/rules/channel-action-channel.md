---
title: Use actionChannel for Sequential Processing
impact: MEDIUM
description: Buffer Redux actions and process them one at a time using actionChannel.
tags: channels, actionChannel, sequential, buffering
---

# Use actionChannel for Sequential Processing

## Problem

With `takeEvery`, multiple instances of a saga run concurrently. If the order of processing matters or you need one-at-a-time execution, concurrent processing causes race conditions.

## Incorrect

```javascript
// BUG: concurrent requests may complete out of order
yield takeEvery('SAVE_DOCUMENT', saveDocument)
```

## Correct

```javascript
import { actionChannel, take, call } from 'redux-saga/effects'

function* watchSaves() {
  // Buffer all SAVE_DOCUMENT actions
  const chan = yield actionChannel('SAVE_DOCUMENT')

  while (true) {
    const action = yield take(chan) // take from buffer, not store
    yield call(saveDocument, action) // blocks until done, then processes next
  }
}
```

## Worker Pool (Limited Parallelism)

```javascript
function* watchRequests() {
  const chan = yield actionChannel('API_REQUEST')

  // 3 parallel workers consuming from the same channel
  for (let i = 0; i < 3; i++) {
    yield fork(worker, chan)
  }
}

function* worker(chan) {
  while (true) {
    const action = yield take(chan)
    yield call(processRequest, action)
  }
}
```
