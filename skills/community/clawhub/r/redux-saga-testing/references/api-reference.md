# Redux-Saga Testing API Reference

## Table of Contents

- Setup (Jest / Vitest)
- expectSaga (Integration Testing)
- testSaga (Unit Testing)
- Providers (Static / Dynamic)
- Matchers
- Reducer Integration
- Dispatching Actions
- Testing Patterns (Cancellation, Race, Throttle)
- runSaga (No Library)
- Manual Generator Testing

---

## Setup

### Installation

```bash
npm install --save-dev redux-saga-test-plan
```

### Jest

```javascript
// Return the promise
it('works', () => {
  return expectSaga(mySaga).run()
})
```

### Vitest

```javascript
// async/await
it('works', async () => {
  await expectSaga(mySaga).run()
})
```

Both runners work identically — `expectSaga.run()` returns a Promise.

---

## expectSaga — Integration Testing

### Basic Usage

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches user', () => {
  const user = { id: 1, name: 'Alice' }

  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), user],
    ])
    .put(fetchUserSuccess(user))
    .run()
})
```

### Assertion Methods

```javascript
expectSaga(saga, ...args)
  // Effect assertions
  .put(action)                    // saga dispatches this action
  .put.like({ action: { type } }) // partial match on action
  .put.actionType('TYPE')         // match action type only
  .call(fn, ...args)              // saga calls fn with exact args
  .call.fn(fn)                    // saga calls fn (any args)
  .call.like({ fn, args })        // partial match
  .fork(fn, ...args)              // saga forks fn
  .fork.fn(fn)                    // saga forks fn (any args)
  .spawn(fn, ...args)             // saga spawns fn
  .select(selector, ...args)      // saga selects with selector
  .take(pattern)                  // saga takes pattern
  .race(effects)                  // saga races effects
  .all(effects)                   // saga runs all effects

  // Negative assertions
  .not.put(action)                // does NOT dispatch
  .not.call.fn(fn)                // does NOT call fn
  .not.fork.fn(fn)                // does NOT fork fn

  // Return value
  .returns(value)                 // saga returns this value

  // Action simulation
  .dispatch(action)               // simulate action during test

  // Reducer integration
  .withReducer(reducer)           // hook up reducer
  .withState(initialState)        // set initial state
  .hasFinalState(expectedState)   // assert final state

  // Execution
  .run()                          // run saga (returns Promise)
  .run({ timeout: 500 })          // with custom timeout (default: 250ms)
  .silentRun()                    // suppress timeout warnings
  .silentRun(500)                 // suppress + custom timeout
```

### Run Options

```javascript
const { effects, storeState, returnValue } = await expectSaga(saga)
  .provide(providers)
  .run()

// effects contains all yielded effects for inspection
// storeState is the final state (if withReducer used)
// returnValue is the saga's return value
```

---

## testSaga — Unit Testing

Tests exact effect ordering. Use when order is part of the contract.

```javascript
import { testSaga } from 'redux-saga-test-plan'

it('processes in order', () => {
  testSaga(checkoutSaga, action)
    .next()                           // start generator
    .put(showLoading())               // first yield must be this put
    .next()
    .call(api.validateCart)            // second must be this call
    .next({ valid: true })            // feed result
    .call(api.processPayment)         // third
    .next({ id: 'txn_123' })
    .put(checkoutSuccess('txn_123'))   // fourth
    .next()
    .isDone()                         // generator is done
})
```

### Branching with Clone

```javascript
it('handles both branches', () => {
  const saga = testSaga(mySaga, action)
    .next()
    .call(api.validate)

  const validBranch = saga.clone()
  const invalidBranch = saga.clone()

  validBranch.next({ valid: true }).put(success())
  invalidBranch.next({ valid: false }).put(failure())
})
```

### Error Testing

```javascript
testSaga(mySaga, action)
  .next()
  .call(api.fetch)
  .throw(new Error('Network error'))   // simulate thrown error
  .put(fetchFailed('Network error'))
  .next()
  .isDone()
```

### Save and Restore

```javascript
testSaga(mySaga)
  .next()
  .take('ACTION')
  .save('before branch')              // save point
  .next(actionA)
  .put(resultA())
  .restore('before branch')           // go back
  .next(actionB)
  .put(resultB())
```

---

## Providers

### Static Providers (Array of Tuples)

```javascript
.provide([
  // Exact effect match
  [call(api.fetchUser, 1), { id: 1, name: 'Alice' }],

  // Partial match by function (recommended — ignores args)
  [matchers.call.fn(api.fetchUser), { id: 1, name: 'Alice' }],

  // Mock selector
  [matchers.select.selector(getAuthToken), 'mock-token'],

  // Simulate error
  [matchers.call.fn(api.save), throwError(new Error('500'))],

  // Mock select without selector (full state)
  [matchers.select(), { auth: { token: 'abc' } }],
])
```

### Dynamic Providers (Object)

```javascript
.provide({
  call(effect, next) {
    if (effect.fn === api.fetchUser) {
      return { id: 1, name: 'Alice' }
    }
    // Pass through to other providers or real execution
    return next()
  },
  select({ selector }, next) {
    if (selector === getAuthToken) return 'mock-token'
    return next()
  },
  fork(effect, next) {
    if (effect.fn === backgroundSync) return createMockTask()
    return next()
  },
})
```

### Composing Providers

```javascript
import { combineProviders } from 'redux-saga-test-plan/providers'

const authProviders = [
  [matchers.select.selector(getToken), 'mock-token'],
  [matchers.call.fn(api.refreshToken), 'new-token'],
]

const dataProviders = [
  [matchers.call.fn(api.fetchUsers), mockUsers],
]

expectSaga(saga)
  .provide([...authProviders, ...dataProviders])
  .run()
```

---

## Matchers

```javascript
import * as matchers from 'redux-saga-test-plan/matchers'

matchers.call(fn, ...args)          // exact match
matchers.call.fn(fn)                // function only (any args)
matchers.call.like({ fn, args })    // partial match

matchers.fork(fn, ...args)
matchers.fork.fn(fn)

matchers.spawn(fn, ...args)
matchers.spawn.fn(fn)

matchers.select()                   // any select
matchers.select.selector(sel)       // specific selector

matchers.put(action)                // exact action
matchers.put.like({ action })       // partial action match
matchers.put.actionType(type)       // type only

matchers.take(pattern)              // specific pattern
```

---

## Reducer Integration

```javascript
import usersReducer from './usersSlice'

it('loads users into state', () => {
  return expectSaga(loadUsersSaga)
    .withReducer(usersReducer)
    .withState({ users: [], loading: false, error: null })
    .provide([
      [matchers.call.fn(api.fetchUsers), [{ id: 1, name: 'Alice' }]],
    ])
    .hasFinalState({
      users: [{ id: 1, name: 'Alice' }],
      loading: false,
      error: null,
    })
    .run()
})
```

### Combined Reducers

```javascript
import { combineReducers } from '@reduxjs/toolkit'

const rootReducer = combineReducers({ users: usersReducer, auth: authReducer })

expectSaga(saga)
  .withReducer(rootReducer)
  .withState({ users: initialUsersState, auth: initialAuthState })
  .hasFinalState(expectedState)
  .run()
```

---

## Dispatching Actions During Tests

Simulate user flows by dispatching actions:

```javascript
it('handles login then logout', () => {
  return expectSaga(loginFlowSaga)
    .provide([
      [matchers.call.fn(api.login), { token: 'abc' }],
    ])
    .dispatch({ type: 'LOGIN', payload: credentials })
    .dispatch({ type: 'LOGOUT' })
    .put(loginSuccess({ token: 'abc' }))
    .put(loggedOut())
    .run({ timeout: 500 })
})
```

---

## Testing Patterns

### Test Cancellation

```javascript
it('cleans up on cancel', () => {
  return expectSaga(syncSaga)
    .provide([
      [matchers.call.fn(api.sync), 'data'],
    ])
    .dispatch({ type: 'START_SYNC' })
    .dispatch({ type: 'STOP_SYNC' })
    .put(syncCancelled())
    .silentRun()
})
```

### Test Race / Timeout

```javascript
it('handles timeout', () => {
  return expectSaga(fetchWithTimeoutSaga)
    .provide([
      // Make API call take forever by not providing a value
      // delay will win the race
      [matchers.call.fn(api.fetch), new Promise(() => {})],
    ])
    .put(timeoutError())
    .run({ timeout: 10000 })
})
```

### Test with createMockTask

```javascript
import { createMockTask } from '@redux-saga/testing-utils'

it('cancels task on logout', () => {
  const mockTask = createMockTask()

  return testSaga(loginFlowSaga)
    .next()
    .take('LOGIN')
    .next({ type: 'LOGIN', payload: creds })
    .fork(authorizeSaga, creds)
    .next(mockTask)
    .take(['LOGOUT', 'LOGIN_ERROR'])
    .next({ type: 'LOGOUT' })
    .cancel(mockTask)
})
```

### Test Throttle / Debounce

```javascript
it('debounces search', () => {
  return expectSaga(watchSearchSaga)
    .provide([[matchers.call.fn(api.search), results]])
    .dispatch({ type: 'SEARCH', query: 'a' })
    .dispatch({ type: 'SEARCH', query: 'ab' })
    .dispatch({ type: 'SEARCH', query: 'abc' })
    .put(searchResults(results))
    .silentRun(1000)
})
```

### Test Saga with Channel

```javascript
it('processes from channel', () => {
  return expectSaga(watchRequestsSaga)
    .provide([
      [matchers.call.fn(handleRequest), 'processed'],
    ])
    .dispatch({ type: 'REQUEST', payload: { id: 1 } })
    .dispatch({ type: 'REQUEST', payload: { id: 2 } })
    .call.fn(handleRequest)
    .silentRun()
})
```

---

## runSaga — No Library Needed

```javascript
import { runSaga } from 'redux-saga'

async function recordSaga(saga, initialAction, state = {}) {
  const dispatched = []
  await runSaga(
    {
      dispatch: (action) => dispatched.push(action),
      getState: () => state,
    },
    saga,
    initialAction,
  ).toPromise()
  return dispatched
}

// Jest
it('dispatches success', async () => {
  jest.spyOn(api, 'fetchUser').mockResolvedValue({ id: 1 })
  const dispatched = await recordSaga(fetchUserSaga, fetchUser(1))
  expect(dispatched).toContainEqual(fetchUserSuccess({ id: 1 }))
})

// Vitest
it('dispatches success', async () => {
  vi.spyOn(api, 'fetchUser').mockResolvedValue({ id: 1 })
  const dispatched = await recordSaga(fetchUserSaga, fetchUser(1))
  expect(dispatched).toContainEqual(fetchUserSuccess({ id: 1 }))
})
```

---

## Manual Generator Testing

Last resort — most brittle, breaks on reorder:

```javascript
it('yields correct effects', () => {
  const gen = fetchUserSaga({ payload: { userId: 1 } })

  // Step through
  expect(gen.next().value).toEqual(call(api.fetchUser, 1))

  // Feed result
  const user = { id: 1, name: 'Alice' }
  expect(gen.next(user).value).toEqual(put(fetchUserSuccess(user)))

  expect(gen.next().done).toBe(true)
})

// Test error path
it('handles errors', () => {
  const gen = fetchUserSaga({ payload: { userId: 1 } })
  gen.next() // advance to call
  expect(gen.throw(new Error('404')).value).toEqual(
    put(fetchUserFailure('404'))
  )
})
```
