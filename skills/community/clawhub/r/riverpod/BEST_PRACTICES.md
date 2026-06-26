# Riverpod Best Practices

## Architecture

### 1. Provider Naming Convention

- Use `Controller` suffix for notifiers: `class UserController extends _$UserController`
- Use descriptive names: `filteredTodosProvider`, `currentUserProvider`
- Group related providers in the same file

### 2. File Organization

```
lib/
├── providers/
│   ├── user_providers.dart       # User-related providers
│   ├── todo_providers.dart       # Todo-related providers
│   └── app_providers.dart        # App-level providers
├── models/
│   └── user.dart
└── screens/
    └── user_screen.dart
```

### 3. Provider Scoping

- **Global providers** (keepAlive: true): Auth state, app config
- **Screen-level providers**: Screen-specific state
- **Widget-level providers** (autoDispose): Form state, temporary data

## Common Patterns

### Pattern: Form State Management

```dart
@riverpod
class FormController extends _$FormController {
  @override
  FormState build() => FormState();

  void updateField(String field, String value) {
    state = state.copyWith(field: field, value: value);
  }

  Future<void> submit() async {
    state = state.copyWith(isSubmitting: true);
    try {
      await api.submit(state);
      state = state.copyWith(isSubmitting: false, isSuccess: true);
    } catch (e) {
      state = state.copyWith(isSubmitting: false, error: e.toString());
    }
  }
}
```

### Pattern: Pagination

```dart
@riverpod
class PaginatedItems extends _$PaginatedItems {
  @override
  Future<ItemsPage> build() async {
    return _fetchPage(1);
  }

  Future<void> loadMore() async {
    final current = await future;
    final nextPage = current.page + 1;
    final newItems = await _fetchPage(nextPage);
    state = AsyncData(newItems.copyWith(
      items: [...current.items, ...newItems.items],
    ));
  }
}
```

### Pattern: Search with Debounce

```dart
@riverpod
Future<SearchResults> searchResults(SearchResultsRef ref, String query) async {
  // Cancel previous request after 500ms
  ref.onDispose(() => cancelToken.cancel());
  
  // Debounce
  await Future.delayed(const Duration(milliseconds: 500));
  
  return await api.search(query);
}
```

## Anti-Patterns to Avoid

### ❌ Don't: Listeners in build()

```dart
// BAD - Called on every rebuild
@override
Widget build(BuildContext context, WidgetRef ref) {
  ref.listen(counterProvider, (prev, next) {
    showSnackBar(context, 'Changed!');
  });
  return Container();
}
```

### ✅ Do: Listeners in initState or use ref.listen manually

```dart
class _MyState extends ConsumerState<MyWidget> {
  @override
  void initState() {
    super.initState();
    ref.listenManual(counterProvider, (_, __) {
      // Handle change
    });
  }
}
```

### ❌ Don't: Pattern match without handling all cases

```dart
// BAD - Missing AsyncLoading case
final value = switch (snapshot) {
  AsyncData(:final value) => value,
  AsyncError() => 'Error',
};
```

### ✅ Do: Always handle all AsyncValue states

```dart
final result = switch (snapshot) {
  AsyncData(:final value) => value,
  AsyncError(:final error) => 'Error: $error',
  AsyncLoading() => 'Loading...',
};
```

## Performance Tips

### 1. Use select() for Partial Rebuilds

```dart
// Rebuilds only when user's name changes
final name = ref.watch(userProvider.select((u) => u.name));
```

### 2. Cache Computed Values

```dart
@riverpod
List<Todo> sortedTodos(SortedTodosRef ref) {
  final todos = ref.watch(todosProvider);
  // Computed once and cached
  return todos..sort((a, b) => a.dueDate.compareTo(b.dueDate));
}
```

### 3. Avoid Watch in Lists

```dart
// Extract to Consumer widget
class TodoItem extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final todo = ref.watch(todoProvider);
    return ListTile(title: Text(todo.title));
  }
}
```

## Testing

### Provider Testing

```dart
test('counter increments', () async {
  final container = ProviderContainer();
  
  final controller = container.read(counterProvider.notifier);
  controller.increment();
  
  expect(container.read(counterProvider), equals(1));
});
```

### Widget Testing with Riverpod

```dart
testWidgets('shows loading then data', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        userProvider.overrideWithValue(
          AsyncData(User(name: 'Test')),
        ),
      ],
      child: const MyApp(),
    ),
  );

  expect(find.text('Test'), findsOneWidget);
});
```

## Migration Guide

### From Provider package to Riverpod

| Provider | Riverpod |
|----------|----------|
| `ChangeNotifierProvider` | `StateNotifier` / `@riverpod class` |
| `FutureProvider` | `@riverpod Future<T> func(Ref ref)` |
| `StreamProvider` | `@riverpod Stream<T> func(Ref ref)` |
| `MultiProvider` | `ProviderScope` with single override list |

## Error Handling

### Centralized Error Handler

```dart
@riverpod
class ErrorHandler extends _$ErrorHandler {
  @override
  void build() {
    ref.listen<AsyncValue>(globalProvider, (prev, next) {
      if (next is AsyncError) {
        // Log to analytics, show snackbar, etc.
        _handleError(next.error);
      }
    });
  }
}
```
