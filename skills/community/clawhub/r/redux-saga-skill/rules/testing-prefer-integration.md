---
title: Prefer Integration Tests Over Step-by-Step
impact: HIGH
description: Use expectSaga for integration tests that don't couple to implementation order. Reserve testSaga for critical ordering.
tags: testing, expectSaga, testSaga, redux-saga-test-plan
---

# Prefer Integration Tests Over Step-by-Step

## Problem

Step-by-step generator tests (`testSaga`, manual `.next()`) break when you reorder yielded effects, even if behavior is unchanged. This creates brittle tests that resist refactoring.

## Incorrect

```javascript
// Brittle: breaks if you reorder the put/select/call
it('fetches user', () => {
  const gen = fetchUserSaga(action)
  expect(gen.next().value).toEqual(call(api.fetchUser, 1))
  expect(gen.next(user).value).toEqual(put(fetchUserSuccess(user)))
  expect(gen.next().done).toBe(true)
})
```

## Correct

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches user successfully', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([
      [matchers.call.fn(api.fetchUser), user],
    ])
    .put(fetchUserSuccess(user))
    .run()
})

it('handles fetch failure', () => {
  const error = new Error('Network error')
  return expectSaga(fetchUserSaga, action)
    .provide([
      [matchers.call.fn(api.fetchUser), throwError(error)],
    ])
    .put(fetchUserFailure('Network error'))
    .run()
})
```

## When to Use Step-by-Step

Use `testSaga` only when **effect ordering is part of the contract** (e.g., optimistic updates that must dispatch before the API call):

```javascript
import { testSaga } from 'redux-saga-test-plan'

it('dispatches optimistic update before API call', () => {
  testSaga(optimisticSubmitSaga, action)
    .next()
    .put(optimisticUpdate(action.payload)) // must come first
    .next()
    .call(api.submit, action.payload) // then the API call
    .next()
    .isDone()
})
```
