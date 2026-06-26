---
title: Use Providers for Mocking
impact: HIGH
description: Use redux-saga-test-plan providers to mock side effects. Prefer static providers and partial matchers.
tags: testing, providers, mocking, redux-saga-test-plan
---

# Use Providers for Mocking

## Problem

Without providers, `expectSaga` tries to execute real side effects (API calls, delays). Tests become slow, flaky, and dependent on external services.

## Incorrect

```javascript
// BUG: makes real API calls in tests
it('fetches data', () => {
  return expectSaga(fetchDataSaga)
    .put(fetchSuccess(data)) // fails — real API may return different data
    .run()
})
```

## Correct — Static Providers

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

const mockData = { id: 1, name: 'Test' }

it('fetches data successfully', () => {
  return expectSaga(fetchDataSaga)
    .provide([
      // Partial matcher: matches any call to api.fetchData regardless of args
      [matchers.call.fn(api.fetchData), mockData],
    ])
    .put(fetchSuccess(mockData))
    .run()
})

it('handles errors', () => {
  return expectSaga(fetchDataSaga)
    .provide([
      [matchers.call.fn(api.fetchData), throwError(new Error('500'))],
    ])
    .put(fetchFailure('500'))
    .run()
})
```

## Correct — Dynamic Providers

```javascript
it('handles conditional logic', () => {
  return expectSaga(complexSaga)
    .provide({
      call(effect, next) {
        if (effect.fn === api.fetchUser) {
          return { id: 1, name: 'Alice' }
        }
        return next() // let other calls pass through
      },
      select({ selector }, next) {
        if (selector === getAuthToken) {
          return 'mock-token'
        }
        return next()
      },
    })
    .put(userLoaded({ id: 1, name: 'Alice' }))
    .run()
})
```

## Provider Tips

| Matcher | Use When |
|---------|----------|
| `matchers.call.fn(fn)` | Match by function, ignore args |
| `matchers.call(fn, ...args)` | Match function + exact args |
| `matchers.select(selector)` | Mock a selector |
| `[effect, throwError(err)]` | Simulate error |
| `[matchers.call.fn(fn), dynamic(() => val)]` | Dynamic return value |
