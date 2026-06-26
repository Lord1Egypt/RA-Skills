---
name: riverpod
description: Flutter state management with Riverpod - declarative, type-safe, and code-generated providers. Use when building Flutter apps that need reactive state management, dependency injection, and testable business logic. Covers ProviderNotifier, AsyncNotifier, StreamProvider, Family modifiers, and code generation with @riverpod.
---

# Riverpod State Management

Riverpod is a declarative, type-safe state management solution for Flutter. It uses code generation for boilerplate reduction.

## Core Concepts

### 1. Declarative State with @riverpod

Mark classes or functions with `@riverpod` for code generation:

```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
}
```

### 2. Consuming State

Use `ConsumerWidget` or `ConsumerStatefulWidget`:

```dart
class CounterView extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### 3. Provider Types

| Type | Use For | Syntax |
|------|---------|--------|
| StateProvider | Simple state | `@riverpod class X extends _$X` |
| AsyncNotifier | Async loading | `@riverpod class X extends _$X` with Future |
| StreamProvider | Real-time data | `@riverpod Stream<T> func(Ref ref)` |
| Family providers | Parameterized | `@riverpod class X extends Family<X, Args>` |

## Code Patterns

### Pattern 1: AsyncNotifier for API Calls

```dart
@riverpod
class UserController extends _$UserController {
  @override
  Future<User> build(String userId) async {
    final dio = ref.watch(dioProvider);
    final response = await dio.get('/users/$userId');
    return User.fromJson(response.data);
  }

  Future<void> updateUser(User user) async {
    // Optimistic update
    final previous = await future;
    state = AsyncData(user);

    try {
      await ref.read(dioProvider).put('/users/${user.id}', user.toJson());
    } catch (e) {
      state = AsyncError(e, StackTrace.current);
    }
  }
}
```

### Pattern 2: Combining Providers

```dart
@riverpod
List<Todo> filteredTodos(Ref ref) {
  final todos = ref.watch(todosProvider);
  final filter = ref.watch(filterProvider);

  return switch (filter) {
    Filter.all => todos,
    Filter.completed => todos.where((t) => t.completed).toList(),
    Filter.uncompleted => todos.where((t) => !t.completed).toList(),
  };
}
```

### Pattern 3: Dependency Injection

```dart
@riverpod
Dio dio(Ref ref) {
  final baseUrl = ref.watch(baseUrlProvider);
  return Dio(BaseOptions(baseUrl: baseUrl));
}
```

### Pattern 4: AsyncValue Pattern Matching

```dart
class AsyncWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final data = ref.watch(asyncProvider);

    return switch (data) {
      AsyncData(:final value) => Text('$value'),
      AsyncError(:final error, :final stackTrace) => ErrorWidget(error),
      AsyncLoading() => const CircularProgressIndicator(),
    };
  }
}
```

## Provider Modifiers

### Family - Parameterized Providers

```dart
@riverpod
Future<User> user(UserRef ref, String userId) async {
  return await api.getUser(userId);
}

// Usage
ref.watch(userProvider('123'));
```

### AutoDispose - Automatic Cleanup

```dart
@Riverpod(keepAlive: false)
Future<User> temporaryUser(TemporaryUserRef ref, String id) async {
  ref.onDispose(() {
    // Cleanup logic
  });
  return await api.getUser(id);
}
```

## Widget Patterns

### ConsumerWidget Pattern

```dart
class MyWidget extends ConsumerWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(myProvider);
    return Text('$value');
  }
}
```

### ConsumerStatefulWidget Pattern

```dart
class MyPage extends ConsumerStatefulWidget {
  const MyPage({super.key});

  @override
  ConsumerState<MyPage> createState() => _MyPageState();
}

class _MyPageState extends ConsumerState<MyPage> {
  @override
  void initState() {
    super.initState();
    ref.read(myProvider.notifier).load();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(myProvider);
    return Scaffold(body: Text('$state'));
  }
}
```

### HookConsumerWidget (with flutter_hooks)

```dart
class HookWidget extends HookConsumerWidget {
  const HookWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = useTextController();
    final count = ref.watch(counterProvider);
    
    return TextField(controller: controller);
  }
}
```

## Code Generation Workflow

1. Add annotation: `@riverpod` or `@Riverpod()`
2. Define class extending `_$ClassName` or function
3. Run: `flutter pub run build_runner watch --delete-conflicting-outputs`
4. Generated file: `.g.dart` extension

## Essential Commands

```bash
# Generate once
flutter pub run build_runner build --delete-conflicting-outputs

# Watch for changes (recommended during development)
flutter pub run build_runner watch --delete-conflicting-outputs
```

## Testing

```dart
testWidgets('counter increments', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      child: MaterialApp(home: CounterView()),
    ),
  );

  expect(find.text('0'), findsOneWidget);
});
```

## ref Methods

| Method | Use For |
|--------|---------|
| ref.watch(provider) | Rebuild when value changes |
| ref.read(provider) | One-time read, no rebuild |
| ref.listen(provider, cb) | Side effects on change |
| ref.refresh(provider) | Force reload |
| ref.invalidate(provider) | Mark as needing refresh |

## Best Practices

See [BEST_PRACTICES.md](BEST_PRACTICES.md) for detailed guidelines on:
- Provider architecture
- Avoiding common pitfalls
- Performance optimization
- Testing strategies
