---
title: Channels and External I/O
impact: MEDIUM
tags: channels, eventChannel, actionChannel, multicast, websocket, external-io, buffers
---

# Channels and External I/O

## Channel Types

### actionChannel — Buffer Redux Actions

Queue Redux actions for sequential processing.

```javascript
import { actionChannel, take, call } from 'redux-saga/effects'

function* watchSaves() {
  const chan = yield actionChannel('SAVE_DOCUMENT')
  while (true) {
    const action = yield take(chan)
    yield call(saveDocument, action) // one at a time
  }
}
```

### eventChannel — External Event Sources

Bridge WebSockets, DOM events, timers into sagas.

```javascript
import { eventChannel, END } from 'redux-saga'

function createSocketChannel(socket) {
  return eventChannel((emit) => {
    socket.on('message', (data) => emit(data))
    socket.on('error', (err) => emit({ error: err }))
    socket.on('close', () => emit(END))
    return () => socket.close()
  })
}

function* watchSocket(socket) {
  const channel = yield call(createSocketChannel, socket)
  try {
    while (true) {
      const payload = yield take(channel)
      if (payload.error) {
        yield put(socketError(payload.error))
      } else {
        yield put(messageReceived(payload))
      }
    }
  } finally {
    channel.close()
  }
}
```

### channel — Generic Saga-to-Saga Communication

Manual put/take for direct communication between sagas.

```javascript
import { channel } from 'redux-saga'

function* producer(chan) {
  while (true) {
    const data = yield call(fetchData)
    yield put(chan, data)
    yield delay(5000)
  }
}

function* consumer(chan) {
  while (true) {
    const data = yield take(chan)
    yield call(processData, data)
  }
}

function* rootSaga() {
  const chan = yield call(channel)
  yield fork(producer, chan)
  yield fork(consumer, chan)
}
```

### multicastChannel — Broadcast to Multiple Consumers

Each message is delivered to all takers, not just one.

```javascript
import { multicastChannel } from 'redux-saga'

function* root() {
  const chan = yield call(multicastChannel)
  yield fork(workerA, chan) // both receive every message
  yield fork(workerB, chan)
  yield put(chan, { type: 'BROADCAST' })
}
```

## Buffer Strategies

```javascript
import { buffers } from 'redux-saga'

// No buffer: drops messages when no taker
eventChannel(sub, buffers.none())

// Fixed buffer: errors if queue exceeds limit
eventChannel(sub, buffers.fixed(10))

// Expanding buffer: grows dynamically
eventChannel(sub, buffers.expanding(10))

// Dropping buffer: silently drops new messages on overflow
eventChannel(sub, buffers.dropping(10))

// Sliding buffer: drops oldest messages on overflow
eventChannel(sub, buffers.sliding(10))
```

| Buffer | On Overflow | Use When |
|--------|------------|----------|
| `none()` | Drops message | Fire-and-forget events |
| `fixed(n)` | Throws error | Must process all, overflow is a bug |
| `expanding(n)` | Grows | Must process all, variable load |
| `dropping(n)` | Drops newest | Latest data not critical |
| `sliding(n)` | Drops oldest | Only latest messages matter |

## flush — Drain a Channel

```javascript
function* processBatch(chan) {
  while (true) {
    yield delay(5000) // wait 5 seconds
    const messages = yield flush(chan) // grab everything buffered
    if (messages.length > 0) {
      yield call(api.sendBatch, messages)
    }
  }
}
```

## runSaga — Connect to External I/O

Run a saga outside Redux, connected to any event system:

```javascript
import { runSaga, stdChannel } from 'redux-saga'
import { EventEmitter } from 'events'

const emitter = new EventEmitter()
const channel = stdChannel()
emitter.on('action', channel.put)

const task = runSaga(
  {
    channel,
    dispatch: (output) => emitter.emit('action', output),
    getState: () => ({ /* app state */ }),
  },
  mySaga,
)
```
