# Modern Kotlin for Android

## Null Safety

- Prefer `?.let`, `?:`, `requireNotNull()`, `checkNotNull()` over force-unwrap `!!`.
- Use `!!` only when a null value represents an unrecoverable programming error.
  Even then, add a comment explaining why.
- Use `requireNotNull(value) { "Descriptive message" }` as a safe assertion at
  function entry points.


## Sealed Interfaces for State

Prefer `sealed interface` over `sealed class` for UI state unions — it is more
flexible (a class can implement multiple sealed interfaces):

```kotlin
sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Success(val books: List<Book>) : HomeUiState
    data class Error(val message: String) : HomeUiState
}
```

Use `data object` for singleton states (no properties) and `data class` for
states with data.


## Coroutines

- All ViewModel async work goes in `viewModelScope.launch { }` or `viewModelScope.async { }`.
- Use `Dispatchers.IO` for disk/network operations. Switch back to `Main` only if needed.
- Prefer `flow { }` + `flowOn(Dispatchers.IO)` over `withContext` inside a flow.
- Always handle exceptions — use `catch` on flows or `try/catch` in coroutine blocks.
  Never silently swallow exceptions.

```kotlin
// Good — exception handled and exposed to UI
viewModelScope.launch {
    _uiState.update { it.copy(isLoading = true) }
    try {
        val books = repository.getBooks()
        _uiState.update { it.copy(books = books, isLoading = false) }
    } catch (e: Exception) {
        _uiState.update { it.copy(error = e.message, isLoading = false) }
    }
}
```


## Flow Operators

- Use `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), initialValue)`
  to convert a cold flow to `StateFlow` in the ViewModel.
- Prefer `WhileSubscribed(5000)` over `Eagerly` — it cancels upstream collection
  5 seconds after the last subscriber leaves, surviving configuration changes
  without leaking.


## Data Classes for State

Use `data class` with `copy()` for immutable state updates:

```kotlin
_uiState.update { it.copy(isLoading = false, books = newBooks) }
```


## Extension Functions

Use extension functions to extend `Modifier`, `String`, `Context`, etc. with
reusable logic. Keep them in focused files named for the type they extend
(`ModifierExtensions.kt`, `ContextExtensions.kt`).


## When Expressions

Prefer `when` over long `if/else if` chains, especially for sealed class/interface
exhaustive matching. The compiler enforces exhaustiveness on sealed types:

```kotlin
val content = when (val state = uiState) {
    is HomeUiState.Loading -> LoadingScreen()
    is HomeUiState.Success -> SuccessScreen(state.books)
    is HomeUiState.Error -> ErrorScreen(state.message)
}
```


## String Formatting

- Never use `String.format()` for user-facing values. Use `pluralStringResource()`,
  `stringResource()`, or Compose `Text` format parameters.
- Use `stringResource(R.string.greeting, userName)` for interpolated strings.
