---
title: Testing Redux Sagas
impact: HIGH
tags: testing, redux-saga-test-plan, expectSaga, testSaga, providers, vitest, jest
---

# Testing Redux Sagas

## Recommended Approach

Use `redux-saga-test-plan` with `expectSaga` for integration tests. It covers all three testing approaches (step-by-step, recorded effects, integration) and doesn't couple tests to implementation order.

```
npm install --save-dev redux-saga-test-plan
```

## Integration Testing with expectSaga

### Basic Pattern

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches and stores user', () => {
  const user = { id: 1, name: 'Alice' }

  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), user],
    ])
    .put(fetchUserSuccess(user))
    .run()
})
```

### Assertions Available

```javascript
expectSaga(saga)
  .put(action)              // dispatches this action
  .put.like({ action: { type: 'FOO' } }) // partial match
  .call(fn, ...args)        // calls this function with these args
  .call.fn(fn)              // calls this function (any args)
  .fork(fn, ...args)        // forks this function
  .select(selector)         // selects with this selector
  .take(pattern)            // takes this pattern
  .dispatch(action)         // simulate incoming action during test
  .not.put(action)          // does NOT dispatch this action
  .returns(value)           // saga returns this value
  .run()                    // execute (returns Promise)
```

### Providing Mock Values (Static Providers)

```javascript
.provide([
  // Exact match
  [call(api.fetchUser, 1), { id: 1, name: 'Alice' }],

  // Partial match by function (ignore args)
  [matchers.call.fn(api.fetchUser), { id: 1, name: 'Alice' }],

  // Mock select
  [matchers.select.selector(getAuthToken), 'mock-token'],

  // Simulate error
  [matchers.call.fn(api.fetchUser), throwError(new Error('500'))],
])
```

### Dynamic Providers

```javascript
.provide({
  call(effect, next) {
    if (effect.fn === api.fetchUser) {
      return { id: 1, name: 'Alice' }
    }
    return next() // pass through to other providers or real execution
  },
  select({ selector }, next) {
    if (selector === getAuthToken) return 'mock-token'
    return next()
  },
})
```

### Testing with Reducer

```javascript
import userReducer from './userSlice'

it('loads user into state', () => {
  return expectSaga(fetchUserSaga, action)
    .withReducer(userReducer)
    .withState({ user: null, loading: false })
    .provide([[matchers.call.fn(api.fetchUser), user]])
    .hasFinalState({ user, loading: false })
    .run()
})
```

### Dispatching Actions During Test

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
    .run()
})
```

## Unit Testing with testSaga

For when effect ordering is part of the contract:

```javascript
import { testSaga } from 'redux-saga-test-plan'

it('processes in correct order', () => {
  testSaga(checkoutSaga, action)
    .next()
    .put(showLoading())        // must come first
    .next()
    .call(api.validateCart)     // then validate
    .next({ valid: true })
    .call(api.processPayment)  // then charge
    .next({ id: 'txn_123' })
    .put(checkoutSuccess('txn_123'))
    .next()
    .isDone()
})
```

### Branching with clone

```javascript
import { testSaga } from 'redux-saga-test-plan'

it('handles both valid and invalid cart', () => {
  const saga = testSaga(checkoutSaga, action)
    .next()
    .call(api.validateCart)

  // Clone before branch point
  const validBranch = saga.clone()
  const invalidBranch = saga.clone()

  validBranch
    .next({ valid: true })
    .call(api.processPayment)

  invalidBranch
    .next({ valid: false })
    .put(cartInvalid())
})
```

## Testing Without Libraries

### Using runSaga

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

it('dispatches success action', async () => {
  jest.spyOn(api, 'fetchUser').mockResolvedValue({ id: 1 })
  const dispatched = await recordSaga(fetchUserSaga, fetchUser(1))
  expect(dispatched).toContainEqual(fetchUserSuccess({ id: 1 }))
})
```

### Manual Generator Testing

```javascript
it('yields correct effects', () => {
  const gen = fetchUserSaga({ payload: { userId: 1 } })

  // Step through
  expect(gen.next().value).toEqual(call(api.fetchUser, 1))

  // Feed result
  const user = { id: 1, name: 'Alice' }
  expect(gen.next(user).value).toEqual(put(fetchUserSuccess(user)))

  // Saga is done
  expect(gen.next().done).toBe(true)
})

// Test error path
it('handles errors', () => {
  const gen = fetchUserSaga({ payload: { userId: 1 } })
  gen.next() // advance to call
  const error = new Error('Not found')
  expect(gen.throw(error).value).toEqual(put(fetchUserFailure('Not found')))
})
```

## Testing Patterns

### Test Cancellation

```javascript
it('cancels on logout', () => {
  return expectSaga(loginFlowSaga)
    .provide([
      [matchers.call.fn(api.login), { token: 'abc' }],
    ])
    .dispatch({ type: 'LOGIN', payload: credentials })
    .dispatch({ type: 'LOGOUT' })
    .put(loginCancelled())
    .run()
})
```

### Test Race Effects

```javascript
it('times out after 5 seconds', () => {
  return expectSaga(fetchWithTimeoutSaga)
    .provide([
      [matchers.call.fn(api.fetch), delay(10000)], // simulate slow response
      [matchers.race.fn, { timeout: true }],
    ])
    .put(timeoutError())
    .run()
})
```

### Test Throttle/Debounce

```javascript
it('debounces search', () => {
  return expectSaga(watchSearchSaga)
    .dispatch({ type: 'SEARCH', query: 'a' })
    .dispatch({ type: 'SEARCH', query: 'ab' })
    .dispatch({ type: 'SEARCH', query: 'abc' })
    .provide([[matchers.call.fn(api.search), results]])
    // Only the last search should trigger
    .put(searchResults(results))
    .run({ timeout: 1000 })
})
```

## Vitest vs Jest

Both work identically with `redux-saga-test-plan`. The library returns Promises from `.run()`:

```javascript
// Jest: return the promise
it('works', () => {
  return expectSaga(saga).run()
})

// Vitest: async/await
it('works', async () => {
  await expectSaga(saga).run()
})
```
