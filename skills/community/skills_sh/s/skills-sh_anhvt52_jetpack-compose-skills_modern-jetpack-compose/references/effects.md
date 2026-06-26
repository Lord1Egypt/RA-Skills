# Side Effects in Compose

Side effects are operations that affect state outside of the current composable's
scope. Compose provides structured effect handlers to run side effects safely,
tied to the composable's lifecycle.


## Rule: Never Run Side Effects Directly in Composition

Code in a composable body runs during **composition** and may run multiple times.
Never perform network calls, database writes, navigation, or coroutine launches
directly in the composable body.

```kotlin
// Wrong — side effect in composition
@Composable
fun HomeScreen(viewModel: HomeViewModel) {
    viewModel.loadData() // Called on every recomposition!
}

// Correct — side effect in LaunchedEffect
@Composable
fun HomeScreen(viewModel: HomeViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
}
```


## LaunchedEffect

**Use for:** async work that should start when the composable enters composition
and cancel when it leaves, or when a key changes.

- Takes one or more `key` parameters. Re-launches when any key changes.
- The coroutine is cancelled and re-launched on key change.
- Use `Unit` as the key for one-time setup on entry.

```kotlin
// Runs once when the composable enters composition
LaunchedEffect(Unit) {
    viewModel.loadUserProfile()
}

// Re-runs whenever userId changes
LaunchedEffect(userId) {
    viewModel.loadUserProfile(userId)
}
```

**Key choice matters:**
- `Unit` — runs once on entry
- A stable value (ID, enum) — re-runs when that value changes
- Do NOT use an unstable value (lambda, object reference) as a key — it will
  re-launch on every recomposition.


## DisposableEffect

**Use for:** effects that need explicit cleanup when the composable leaves
composition or when the key changes (event listeners, subscriptions, callbacks).

- Must end with `onDispose { }` — this is required and enforced by the compiler.

```kotlin
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event ->
        if (event == Lifecycle.Event.ON_RESUME) viewModel.onResume()
    }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose {
        lifecycleOwner.lifecycle.removeObserver(observer)
    }
}
```


## SideEffect

**Use for:** synchronizing Compose state with non-Compose managed objects on every
**successful** recomposition. Runs after every recomposition where composition
did not fail.

- Does **not** take keys. Runs on every recomposition.
- Use sparingly — usually only needed for interop with non-Compose systems.

```kotlin
SideEffect {
    // Sync Compose color scheme to the legacy analytics library
    analyticsTracker.setCurrentScreen(screenName)
}
```


## rememberCoroutineScope

**Use for:** launching coroutines in response to **user events** (button clicks,
swipe actions) where the work should be cancelled if the composable leaves.

- Returns a `CoroutineScope` that is cancelled when the composable leaves composition.
- Use this instead of `LaunchedEffect` for user-triggered one-off async actions.

```kotlin
val scope = rememberCoroutineScope()

Button(onClick = {
    scope.launch { viewModel.saveChanges() }
}) {
    Text("Save")
}
```

**Do not** use `rememberCoroutineScope` for initial data loading — use
`LaunchedEffect` or trigger from the ViewModel.


## produceState

**Use for:** converting non-Compose async data sources (callbacks, futures) into
Compose `State<T>`.

```kotlin
val bookState by produceState<Result<Book>>(initialValue = Result.Loading, bookId) {
    value = repository.getBook(bookId)
}
```


## Never Use GlobalScope

Never launch coroutines with `GlobalScope` in Compose code. Always use:
- `rememberCoroutineScope()` for UI-triggered work
- `viewModelScope` in the ViewModel
- `LaunchedEffect` for lifecycle-tied work


## Decision Guide

| Scenario | Use |
|---|---|
| Load data when screen opens | `LaunchedEffect(Unit)` or ViewModel init |
| Re-load when an ID changes | `LaunchedEffect(id)` |
| Register/unregister a listener | `DisposableEffect` |
| Sync with a non-Compose system | `SideEffect` |
| User taps a button, async action | `rememberCoroutineScope` |
| Convert callback API to State | `produceState` |
