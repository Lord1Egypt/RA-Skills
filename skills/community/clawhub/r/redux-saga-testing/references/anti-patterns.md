# Redux-Saga Testing Anti-Patterns

## Table of Contents

- Step-by-step tests that break on reorder
- Missing providers
- Testing implementation instead of behavior
- Forgetting async
- Not testing error paths
- Not testing cancellation
- Inline mocking instead of providers
- Wrong assertion methods
- Over-mocking with dynamic providers
- Not using partial matchers
- Missing negative assertions
- Not testing reducer integration

## Step-by-step tests that break on reorder

```javascript
// BAD: breaks if you swap the order of put and select
it('fetches user', () => {
  const gen = fetchUserSaga(action)
  expect(gen.next().value).toEqual(select(getToken))
  expect(gen.next('token').value).toEqual(call(api.fetchUser, 1))
  expect(gen.next(user).value).toEqual(put(fetchUserSuccess(user)))
})

// GOOD: integration test — order doesn't matter
it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([
      [matchers.select.selector(getToken), 'token'],
      [matchers.call.fn(api.fetchUser), user],
    ])
    .put(fetchUserSuccess(user))
    .run()
})
```

## Missing providers

```javascript
// BAD: makes real API calls — slow, flaky, environment-dependent
it('fetches data', () => {
  return expectSaga(fetchDataSaga)
    .put(fetchSuccess(data))
    .run()
})

// GOOD: mock all external calls
it('fetches data', () => {
  return expectSaga(fetchDataSaga)
    .provide([
      [matchers.call.fn(api.fetchData), mockData],
    ])
    .put(fetchSuccess(mockData))
    .run()
})
```

## Testing implementation instead of behavior

```javascript
// BAD: testing that specific effects are yielded in order
testSaga(saga)
  .next()
  .select(getToken)
  .next('token')
  .put(setLoading(true))
  .next()
  .call(api.fetch)
  // ... 10 more assertions for internal details

// GOOD: test what the saga DOES, not HOW
expectSaga(saga)
  .provide(providers)
  .put(fetchSuccess(data))      // observable outcome
  .not.put(fetchFailure())      // didn't fail
  .run()
```

## Forgetting async

```javascript
// BAD: Jest — test passes before saga finishes
it('fetches data', () => {
  expectSaga(saga).provide(providers).put(action).run()
  // Missing return! Jest doesn't wait for the promise
})

// GOOD: Jest — return the promise
it('fetches data', () => {
  return expectSaga(saga).provide(providers).put(action).run()
})

// GOOD: Vitest — await
it('fetches data', async () => {
  await expectSaga(saga).provide(providers).put(action).run()
})
```

## Not testing error paths

```javascript
// BAD: only tests happy path
it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), user]])
    .put(fetchUserSuccess(user))
    .run()
})

// GOOD: test both paths
it('fetches user successfully', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), user]])
    .put(fetchUserSuccess(user))
    .not.put.actionType('FETCH_USER_FAILURE')
    .run()
})

it('handles fetch failure', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), throwError(new Error('500'))]])
    .put(fetchUserFailure('500'))
    .not.put.actionType('FETCH_USER_SUCCESS')
    .run()
})
```

## Not testing cancellation

```javascript
// BAD: doesn't verify cleanup on cancel
it('syncs data', () => {
  return expectSaga(syncSaga)
    .provide([[matchers.call.fn(api.sync), data]])
    .put(syncSuccess(data))
    .run()
})

// GOOD: verify cancellation cleanup
it('cleans up when cancelled', () => {
  return expectSaga(syncSaga)
    .provide([[matchers.call.fn(api.sync), data]])
    .dispatch({ type: 'START_SYNC' })
    .dispatch({ type: 'STOP_SYNC' })
    .put(syncStopped())
    .silentRun()
})
```

## Inline mocking instead of providers

```javascript
// BAD: using jest.mock for saga dependencies
jest.mock('../api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1 }),
}))

it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .put(fetchUserSuccess({ id: 1 }))
    .run()
})

// GOOD: use providers — no global mock pollution
it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .provide([[matchers.call.fn(api.fetchUser), { id: 1 }]])
    .put(fetchUserSuccess({ id: 1 }))
    .run()
})
```

## Wrong assertion methods

```javascript
// BAD: using jest expect on generator values manually with expectSaga
it('fetches user', async () => {
  const result = await expectSaga(fetchUserSaga, action)
    .provide(providers)
    .run()
  expect(result.effects.put).toContainEqual(put(fetchUserSuccess(user)))
})

// GOOD: use built-in assertions
it('fetches user', () => {
  return expectSaga(fetchUserSaga, action)
    .provide(providers)
    .put(fetchUserSuccess(user))
    .run()
})
```

## Over-mocking with dynamic providers

```javascript
// BAD: dynamic provider intercepts everything — hides bugs
.provide({
  call() { return 'mocked' },  // ALL calls return 'mocked'
  select() { return {} },       // ALL selects return empty object
})

// GOOD: mock only what you need, let the rest pass through
.provide({
  call(effect, next) {
    if (effect.fn === api.fetchUser) return mockUser
    return next()  // other calls execute normally or hit other providers
  },
})
```

## Not using partial matchers

```javascript
// BAD: breaks when API args change (e.g., adding a header param)
.provide([
  [call(api.fetchUser, 1, { headers: { auth: 'token' } }), user],
])

// GOOD: match by function only — resilient to arg changes
.provide([
  [matchers.call.fn(api.fetchUser), user],
])
```

## Missing negative assertions

```javascript
// BAD: only checks what happens — doesn't verify what SHOULDN'T happen
it('successful login', () => {
  return expectSaga(loginSaga, credentials)
    .provide(providers)
    .put(loginSuccess(token))
    .run()
})

// GOOD: verify both positive and negative outcomes
it('successful login', () => {
  return expectSaga(loginSaga, credentials)
    .provide(providers)
    .put(loginSuccess(token))
    .not.put.actionType('LOGIN_FAILURE')
    .not.put.actionType('LOGIN_ERROR')
    .run()
})
```

## Not testing reducer integration

```javascript
// BAD: tests dispatched actions but not resulting state
it('loads users', () => {
  return expectSaga(loadUsersSaga)
    .provide(providers)
    .put(usersLoaded(users))
    .run()
})

// GOOD: verify final state through reducer
it('loads users into state', () => {
  return expectSaga(loadUsersSaga)
    .withReducer(usersReducer)
    .withState({ users: [], loading: true })
    .provide(providers)
    .hasFinalState({ users: mockUsers, loading: false })
    .run()
})
```
