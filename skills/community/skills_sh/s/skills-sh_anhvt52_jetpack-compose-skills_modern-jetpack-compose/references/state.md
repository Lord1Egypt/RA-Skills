# State Management & Data Flow

## Architecture Pattern

Use **MVVM with Unidirectional Data Flow (UDF)**:

- **ViewModel** owns and exposes state as `StateFlow<UiState>`.
- **Composable** observes state via `collectAsStateWithLifecycle()`.
- **User events** flow up as function calls / callbacks into the ViewModel.
- **State** flows down as immutable `UiState` objects.

Never pass a ViewModel instance deep into the composable tree. Pass only state
and callbacks.


## UiState Modeling

Model screen state as a sealed interface or data class:

```kotlin
// Sealed interface for loading/success/error states
sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Success(val books: List<Book>) : HomeUiState
    data class Error(val message: String) : HomeUiState
}

// Or a single data class for simpler screens
data class ProfileUiState(
    val name: String = "",
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)
```


## ViewModel State

- Use `StateFlow`, not `LiveData`, for state in new code.
- Use `MutableStateFlow` privately; expose as `StateFlow`.

```kotlin
class HomeViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()
}
```

- Never use `mutableStateOf` in a ViewModel — it creates a Compose dependency
  in a non-UI class and does not survive configuration changes correctly.


## remember vs rememberSaveable

- `remember { }` — survives recomposition, lost on configuration change or
  process death. Use for in-memory UI state that can be re-derived.
- `rememberSaveable { }` — survives recomposition **and** configuration changes.
  Use for user input, scroll position, selected tab index, or any UI state that
  should survive rotation.

```kotlin
// Lost on rotation — only appropriate if it can be re-derived
var expanded by remember { mutableStateOf(false) }

// Survives rotation — appropriate for user input
var searchQuery by rememberSaveable { mutableStateOf("") }
```


## derivedStateOf

Use `derivedStateOf` when a state value is computed from other state, and
recomposition should only happen when the **computed result** changes (not every
time the source state changes).

```kotlin
// Without derivedStateOf: recomposes on every scroll event
val showFab = lazyListState.firstVisibleItemIndex > 0

// With derivedStateOf: recomposes only when the boolean flips
val showFab by remember {
    derivedStateOf { lazyListState.firstVisibleItemIndex > 0 }
}
```


## snapshotFlow

Use `snapshotFlow` to convert Compose state into a Flow, for use in effects or
to debounce/transform state changes.

```kotlin
LaunchedEffect(lazyListState) {
    snapshotFlow { lazyListState.firstVisibleItemIndex }
        .distinctUntilChanged()
        .collect { index -> /* react to scroll position */ }
}
```


## State Hoisting Rules

1. State should be owned at the **lowest common ancestor** of all composables that need it.
2. If only one composable needs the state, keep it there.
3. If multiple composables need the same state, hoist it to their shared parent.
4. If state outlives the composable (configuration change), move it to a ViewModel.


## What NOT to Do

- Do not use `ObservableMutableState` in ViewModels — use `StateFlow`.
- Do not read ViewModel state directly inside deeply nested composables — pass
  it down or use a scoped ViewModel.
- Do not store derived data in a separate `MutableStateFlow` and manually sync it —
  use `map` on the source flow or `derivedStateOf` in composition.
