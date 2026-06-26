---
title: Troubleshooting
impact: LOW
tags: troubleshooting, debugging, freeze, missed-actions, stack-traces, common-errors
---

# Troubleshooting

## App Freezes After Adding a Saga

**Cause:** Missing `yield` before an effect in a loop.

```javascript
// BUG: synchronous infinite loop
while (true) {
  const action = take('REQUEST') // missing yield
}

// FIX
while (true) {
  const action = yield take('REQUEST')
}
```

## Saga Misses Dispatched Actions

**Cause:** Saga blocked on a `call` effect when the action arrives.

**Fix:** Use `fork` for non-blocking execution so the saga remains responsive to other actions.

```javascript
// Instead of blocking call:
const result = yield call(api.fetch, url) // blocked — misses actions

// Use fork + take:
const task = yield fork(fetchWorker, url)
const action = yield take(['CANCEL', 'SUCCESS'])
if (action.type === 'CANCEL') yield cancel(task)
```

## Unreadable Error Stack Traces

**Fix 1:** Use `onError` with `sagaStack`:

```javascript
createSagaMiddleware({
  onError: (error, { sagaStack }) => {
    console.error(error.message)
    console.error(sagaStack)
  },
})
```

**Fix 2:** Add `babel-plugin-redux-saga` for dev:

```json
{ "plugins": ["redux-saga"] }
```

## Saga Doesn't Start

**Cause:** `sagaMiddleware.run()` called before store is created.

```javascript
// WRONG order
sagaMiddleware.run(rootSaga)
const store = configureStore(...)

// CORRECT order
const store = configureStore(...)
sagaMiddleware.run(rootSaga)
```

## TypeScript: yield Returns `any`

**Cause:** TypeScript can't infer generator yield types.

**Fix:** Type the result manually:

```typescript
const user: User = yield call(api.fetchUser, id)
```

Or use `typed-redux-saga`:

```typescript
import { call } from 'typed-redux-saga'
const user = yield* call(api.fetchUser, id) // properly typed
```

## "Saga was provided undefined action" Warning

**Cause:** Action creator returns undefined instead of an action object.

**Fix:** Verify your action creators return `{ type: string, payload?: any }`.

## Effect Not Executing

**Cause:** Using effect creator result without yielding it.

```javascript
// BUG: creates effect object but doesn't execute it
put(myAction()) // returns { PUT: { action } } — never dispatched

// FIX
yield put(myAction())
```
