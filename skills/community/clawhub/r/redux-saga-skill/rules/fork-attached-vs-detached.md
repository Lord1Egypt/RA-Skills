---
title: Attached vs Detached Forks
impact: CRITICAL
description: Understand fork() vs spawn() — attached forks share lifecycle and errors, spawned tasks are independent.
tags: fork, spawn, lifecycle, error-propagation
---

# Attached vs Detached Forks

## Problem

Using `fork` when you need independence causes a failing child to crash the entire parent tree. Using `spawn` when you need coordination causes orphaned tasks that leak.

## Incorrect

```javascript
// BUG: analytics failure crashes the checkout flow
function* checkoutFlow() {
  yield fork(processPayment)
  yield fork(trackAnalytics) // if this throws, processPayment is cancelled
}

// BUG: spawned task ignores parent cancellation — leaked task
function* authFlow() {
  const task = yield spawn(refreshTokenLoop)
  yield take('LOGOUT')
  // cancel(task) won't auto-happen — must cancel manually
}
```

## Correct

```javascript
// Independent: analytics failure doesn't affect checkout
function* checkoutFlow() {
  yield fork(processPayment) // attached — must complete
  yield spawn(trackAnalytics) // detached — fire and forget
}

// Attached: token refresh is cancelled when auth flow ends
function* authFlow() {
  const task = yield fork(refreshTokenLoop)
  yield take('LOGOUT')
  yield cancel(task) // explicit cancel — or automatic when parent ends
}
```

## Rules

| | `fork` (attached) | `spawn` (detached) |
|---|---|---|
| Parent waits for child | Yes | No |
| Child error crashes parent | Yes | No |
| Parent cancel cancels child | Yes | No |
| Use when | Child is part of the workflow | Child is independent/optional |
