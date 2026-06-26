---
title: Vitest and Jest Setup for Saga Tests
impact: HIGH
description: Configure redux-saga-test-plan with Vitest or Jest. Both work identically with async/await.
tags: testing, vitest, jest, setup, redux-saga-test-plan
---

# Vitest and Jest Setup for Saga Tests

## Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
})
```

```typescript
// sagas/__tests__/fetchUser.test.ts
import { describe, it, expect } from 'vitest'
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { fetchUserSaga } from '../fetchUserSaga'
import * as api from '../../api'

describe('fetchUserSaga', () => {
  it('fetches and dispatches user', async () => {
    const user = { id: 1, name: 'Alice' }

    // expectSaga.run() returns a Promise — works with async/await
    await expectSaga(fetchUserSaga, { payload: { userId: 1 } })
      .provide([[matchers.call.fn(api.fetchUser), user]])
      .put({ type: 'user/loaded', payload: user })
      .run()
  })
})
```

## Jest Setup

```typescript
// sagas/__tests__/fetchUser.test.ts
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'

describe('fetchUserSaga', () => {
  it('fetches and dispatches user', () => {
    const user = { id: 1, name: 'Alice' }

    // Return the promise so Jest waits for it
    return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
      .provide([[matchers.call.fn(api.fetchUser), user]])
      .put({ type: 'user/loaded', payload: user })
      .run()
  })
})
```

## Testing Without redux-saga-test-plan

Use `runSaga` directly for lightweight tests:

```typescript
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

it('dispatches success', async () => {
  vi.spyOn(api, 'fetchUser').mockResolvedValue({ id: 1 })
  const dispatched = await recordSaga(fetchUserSaga, { payload: { userId: 1 } })
  expect(dispatched).toContainEqual({ type: 'user/loaded', payload: { id: 1 } })
})
```
