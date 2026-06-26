---
title: Use eventChannel for External Events
impact: MEDIUM
description: Connect WebSockets, timers, and other non-Redux event sources to sagas via eventChannel.
tags: channels, eventChannel, websocket, external-io
---

# Use eventChannel for External Events

## Problem

Sagas only react to Redux actions by default. External event sources (WebSocket, DOM events, timers) need to be bridged into the saga world.

## Incorrect

```javascript
// BUG: callback can't yield effects — this doesn't work
function* watchSocket() {
  socket.on('message', (data) => {
    yield put(messageReceived(data)) // SyntaxError: yield outside generator
  })
}
```

## Correct

```javascript
import { eventChannel, END } from 'redux-saga'
import { take, put, call } from 'redux-saga/effects'

function createSocketChannel(socket) {
  return eventChannel((emit) => {
    socket.on('message', (data) => emit(data))
    socket.on('close', () => emit(END)) // closes the channel

    // Return unsubscribe function
    return () => socket.close()
  })
}

function* watchSocket() {
  const socket = yield call(connectSocket)
  const channel = yield call(createSocketChannel, socket)

  try {
    while (true) {
      const data = yield take(channel)
      yield put(messageReceived(data))
    }
  } finally {
    channel.close()
  }
}
```

## With Buffer

```javascript
import { buffers } from 'redux-saga'

// Sliding buffer: keeps latest 10 messages, drops older ones
const channel = eventChannel(subscribe, buffers.sliding(10))
```

## Buffer Types

| Buffer | Behavior |
|--------|----------|
| `buffers.none()` | Drops messages when no taker |
| `buffers.fixed(n)` | Fixed queue, errors on overflow |
| `buffers.expanding(n)` | Grows dynamically |
| `buffers.dropping(n)` | Drops new messages on overflow |
| `buffers.sliding(n)` | Drops oldest messages on overflow |
