---
title: Test Sagas with Reducers
impact: HIGH
description: Use withReducer to test saga + reducer integration and assert final state.
tags: testing, reducer, integration, state, redux-saga-test-plan
---

# Test Sagas with Reducers

## Problem

Testing sagas in isolation only verifies dispatched actions. It doesn't verify the reducer handles those actions correctly or that the final state is what you expect.

## Incorrect

```javascript
// Only tests that the saga dispatches the right actions — doesn't verify state
it('loads users', () => {
  return expectSaga(loadUsersSaga)
    .provide([[matchers.call.fn(api.fetchUsers), [{ id: 1 }]]])
    .put(usersLoaded([{ id: 1 }]))
    .run()
})
```

## Correct

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import usersReducer from './usersSlice'

it('loads users into state', () => {
  return expectSaga(loadUsersSaga)
    .withReducer(usersReducer)
    .provide([[matchers.call.fn(api.fetchUsers), [{ id: 1, name: 'Alice' }]]])
    .hasFinalState({
      users: [{ id: 1, name: 'Alice' }],
      loading: false,
      error: null,
    })
    .run()
})

it('sets error state on failure', () => {
  return expectSaga(loadUsersSaga)
    .withReducer(usersReducer)
    .withState({ users: [], loading: false, error: null })
    .provide([
      [matchers.call.fn(api.fetchUsers), throwError(new Error('Failed'))],
    ])
    .hasFinalState({
      users: [],
      loading: false,
      error: 'Failed',
    })
    .run()
})
```

## Benefits

- Tests the full saga→reducer pipeline
- Catches mismatches between action payloads and reducer expectations
- `.withState()` sets initial state for the test
- `.hasFinalState()` asserts the end state after the saga completes
