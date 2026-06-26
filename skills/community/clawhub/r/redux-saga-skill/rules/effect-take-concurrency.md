---
title: Choose the Right Watcher
impact: CRITICAL
description: Pick takeEvery, takeLatest, or takeLeading based on your concurrency needs.
tags: takeEvery, takeLatest, takeLeading, concurrency
---

# Choose the Right Watcher

## Problem

Using `takeEvery` when only the latest result matters causes stale responses to overwrite fresh data. Using `takeLatest` when all results are needed drops work silently.

## Incorrect

```javascript
// BUG: stale search results can overwrite the latest
yield takeEvery('SEARCH_INPUT_CHANGED', performSearch)

// BUG: duplicate form submissions processed
yield takeEvery('SUBMIT_ORDER', processOrder)
```

## Correct

```javascript
// Search: only latest result matters
yield takeLatest('SEARCH_INPUT_CHANGED', performSearch)

// Form submit: prevent duplicates
yield takeLeading('SUBMIT_ORDER', processOrder)

// Notifications: process all of them
yield takeEvery('NOTIFICATION_RECEIVED', showNotification)
```

## Decision Table

| Scenario | Watcher | Why |
|----------|---------|-----|
| Search / autocomplete | `takeLatest` | Cancel stale requests |
| Form submission / payment | `takeLeading` | Prevent duplicate processing |
| Notifications / logging | `takeEvery` | Process every event |
| Sequential queue | `actionChannel` + `take` | Process in order, one at a time |
| Rate-limited UI events | `throttle` | Max once per interval |
| Wait for typing to stop | `debounce` | After silence period |
