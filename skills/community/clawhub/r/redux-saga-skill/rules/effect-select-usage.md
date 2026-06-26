---
title: Use Selectors with select()
impact: HIGH
description: Always use reusable selector functions with select(). Never access state paths directly.
tags: effects, select, selectors, state
---

# Use Selectors with select()

## Problem

Accessing state shape directly in sagas couples them to the store structure. Any refactor to the state tree breaks all sagas.

## Incorrect

```javascript
// BAD: hardcoded state path — breaks if store shape changes
function* checkoutSaga() {
  const state = yield select()
  const cartItems = state.cart.items
  const userId = state.auth.user.id
  yield call(api.checkout, userId, cartItems)
}
```

## Correct

```javascript
// Selectors in a shared file
const getCartItems = (state) => state.cart.items
const getUserId = (state) => state.auth.user?.id

function* checkoutSaga() {
  const cartItems = yield select(getCartItems)
  const userId = yield select(getUserId)
  yield call(api.checkout, userId, cartItems)
}
```

## With RTK Slices

```typescript
// usersSlice.ts
export const selectCurrentUser = (state: RootState) => state.users.current

// saga.ts
const user = yield select(selectCurrentUser)
```

## With Parameters

```javascript
const getItemById = (state, id) => state.items.byId[id]

function* updateItemSaga(action) {
  const item = yield select(getItemById, action.payload.id)
  // ...
}
```
