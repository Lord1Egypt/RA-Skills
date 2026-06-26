# Composable Best Practices

## Naming

- Composable functions that emit UI must use **PascalCase**: `HomeScreen`, `BookCard`.
- Non-composable functions (even those returning `@Composable` lambdas) use camelCase.
- Composables that return a value (not Unit) follow the regular function naming convention.


## Single Responsibility

- Each composable should do one thing. A screen composable orchestrates layout and
  passes data down; it does not contain business logic.
- If a composable body exceeds ~80 lines, extract sub-composables.
- Name extracted composables for what they represent, not how they look
  (`AuthorSection`, not `LeftAlignedTextWithImage`).


## State Hoisting

- Composables should be **stateless** where possible: accept state and callbacks
  as parameters rather than creating state internally.
- This makes composables reusable, testable, and previewable.
- The "state holder" (ViewModel or `remember`) lives at the lowest ancestor that
  needs the state.

```kotlin
// Stateless — preferred for reusable components
@Composable
fun CounterButton(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Count: $count")
    }
}

// Stateful — acceptable at the screen level
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    CounterButton(count = uiState.count, onIncrement = viewModel::increment)
}
```


## No Side Effects in Composition

- Never perform side effects directly in a composable body (network calls, DB writes,
  launching coroutines). Use effect handlers (`LaunchedEffect`, `DisposableEffect`)
  — see `references/effects.md`.
- Never call `remember { }` with a lambda that has side effects (e.g., starts a
  coroutine or emits to a channel). Use `LaunchedEffect` instead.


## No Business Logic in Composables

- Composables handle UI only. Move filtering, sorting, mapping, and calculations
  to the ViewModel or a domain layer.
- It is acceptable to have simple UI-only logic (e.g., computing a string to display),
  but anything involving a repository, use case, or data transformation belongs outside.


## Slot APIs

- Use slot APIs (trailing `@Composable` lambda parameters) to make composables
  flexible without coupling them to specific child content.

```kotlin
@Composable
fun Card(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit
) {
    Surface(modifier = modifier, shape = MaterialTheme.shapes.medium) {
        Column(modifier = Modifier.padding(16.dp), content = content)
    }
}
```


## Previews

- Every non-trivial composable should have at least one `@Preview`.
- Use `@PreviewParameter` to supply preview data — do not hardcode preview data
  inline in the composable itself.
- Provide multiple preview configurations for important screens:

```kotlin
@Preview(name = "Light", showBackground = true)
@Preview(name = "Dark", showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Preview(name = "Large font", showBackground = true, fontScale = 1.5f)
@Composable
private fun HomeScreenPreview() {
    AppTheme { HomeScreen(uiState = HomeUiState.previewData()) }
}
```


## File Organization

- Each non-trivial composable lives in its own file, named after the composable.
- Group files by feature: `feature/home/HomeScreen.kt`, `feature/home/BookCard.kt`.
- Do not place multiple unrelated composables in the same file.


## Modifier Parameter

- Every composable that emits layout should accept a `modifier: Modifier = Modifier`
  parameter as its first non-required parameter (after required data params).
- Apply the caller-provided modifier to the **root** layout element only. Do not
  apply it to inner elements.

```kotlin
@Composable
fun BookCard(book: Book, modifier: Modifier = Modifier) {
    Card(modifier = modifier) { // Correct: applied to root
        Text(book.title)
    }
}
```
