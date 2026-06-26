# Recomposition Stability

Compose skips recomposing a composable if all its parameters are **stable** and
unchanged. Understanding stability is key to writing performant Compose code.


## Stable vs Unstable Types

A type is **stable** if Compose can determine that its public properties will not
change without notification. Stable types are:

- Primitive types (`Int`, `String`, `Boolean`, `Float`, etc.)
- `@Stable` or `@Immutable` annotated classes
- Function types (lambdas) — but see lambda stability below
- Kotlin `data class` where all fields are stable types

A type is **unstable** if it contains mutable fields, non-stable types, or
standard collections (`List`, `Map`, `Set` without annotation).


## @Immutable and @Stable

- Use `@Immutable` on data classes where all properties are immutable and stable.
  This tells the Compose compiler the object will never change after construction.

```kotlin
@Immutable
data class Book(val id: String, val title: String, val author: String)
```

- Use `@Stable` on classes that are mutable but notify Compose when they change
  (e.g., `@Observable` style classes).

- Do not apply these annotations incorrectly — if a class is annotated `@Immutable`
  but its contents change, you will get silent stale UI bugs.


## Unstable Collections

Standard Kotlin `List`, `Map`, and `Set` are **unstable** in Compose because they
are backed by mutable implementations. Passing them to composables prevents skipping.

Options:
1. Use `kotlinx.collections.immutable` (`ImmutableList`, `ImmutableMap`):
```kotlin
@Immutable
data class HomeUiState(val books: ImmutableList<Book>)
```
2. Wrap in an `@Immutable` data class (the wrapper is stable, the list inside is hidden):
```kotlin
@Immutable
data class BookList(val items: List<Book>)
```


## derivedStateOf

Use `derivedStateOf` to avoid recomposing a composable when the **source** state
changes but the **derived** value does not.

```kotlin
// Recomposes on every scroll event — too frequent
val isAtTop = lazyListState.firstVisibleItemIndex == 0

// Recomposes only when isAtTop flips between true and false
val isAtTop by remember {
    derivedStateOf { lazyListState.firstVisibleItemIndex == 0 }
}
```

Always wrap `derivedStateOf` in `remember` — otherwise it creates a new derived
state object on every recomposition.


## key() in Lazy Lists

Always provide a `key` to `LazyColumn` / `LazyRow` items. Without a key, Compose
uses position-based identity, which causes incorrect animations and wasted recomposition
when the list is reordered or items are removed.

```kotlin
// Without key — position-based identity, causes issues on reorder
LazyColumn {
    items(books) { book -> BookCard(book) }
}

// With key — stable identity
LazyColumn {
    items(books, key = { it.id }) { book -> BookCard(book) }
}
```

The key must be:
- A primitive type or a `Parcelable` value
- Unique within the list
- Stable across recompositions (do not use random UUIDs or list indices)


## Defer State Reads

Read state as late (as deep) as possible to narrow the recomposition scope.

```kotlin
// Bad — reading scrollState here recomposes the whole parent on every scroll
@Composable
fun Parent(scrollState: ScrollState) {
    val offset = scrollState.value
    Child(offset = offset)
}

// Better — pass the state object, read inside the modifier lambda (deferred read)
@Composable
fun Parent(scrollState: ScrollState) {
    Box(
        modifier = Modifier.offset { IntOffset(0, scrollState.value) }
        // offset lambda reads scrollState — only the layout phase reruns, not composition
    )
}
```


## Lambda Stability

Lambdas defined inline in a composable are recreated on every recomposition,
making them unstable. For lambdas passed frequently to child composables, use
`remember` to stabilize them.

```kotlin
// Unstable — new lambda instance on every recomposition
LazyColumn {
    items(books, key = { it.id }) { book ->
        BookCard(book, onClick = { navigator.navigate(book.id) }) // new lambda each time
    }
}

// Stable — remembered lambda
val onBookClick = remember(navigator) { { bookId: String -> navigator.navigate(bookId) } }
LazyColumn {
    items(books, key = { it.id }) { book ->
        BookCard(book, onClick = { onBookClick(book.id) })
    }
}
```


## Composition Tracing

To profile recomposition in production builds, add the Compose tracing artifact:
`androidx.compose.runtime:runtime-tracing`. This enables recomposition traces in
Android Studio's Profiler and Perfetto.
