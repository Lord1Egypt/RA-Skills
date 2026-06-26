# Data Flow and State Management

## Architecture: Manager Pattern

Use `@Observable` manager classes injected via `@Environment`:

```swift
@Observable @MainActor
final class TabManager {
    private(set) var tabs: [Tab] = []
    var activeTabID: Tab.ID?

    func createTab(url: URL) { ... }
    func closeTab(_ id: Tab.ID) { ... }
}

// Environment key
extension EnvironmentValues {
    @Entry var tabManager: TabManager?
}

// Injection at app level
WindowGroup {
    ContentView()
        .environment(\.tabManager, appState.tabManager)
}

// Usage in views
struct TabBar: View {
    @Environment(\.tabManager) private var tabManager
}
```

This replaces MVVM's ViewModel layer. Managers own state and logic; views are pure presentation that read from environment and call manager methods.

## Property Wrapper Rules

| Wrapper | Purpose | Key rule |
|---|---|---|
| `@State` | Creates and owns source of truth | Must be `private`. Only the declaring view owns it. |
| `@Binding` | Read-write reference to parent's state | Passed from parent via `$`. |
| `@Bindable` | Creates `$` bindings from `@Observable` objects | Required when the observable isn't `@State`-owned. |
| `@Environment` | Reads injected values from ancestor views | For managers, settings, system values. |
| `@Entry` | Defines custom environment/focus/transaction keys | Replaces manual `EnvironmentKey` boilerplate. |

### @Bindable

Required to create `$` bindings from `@Observable` objects not owned via `@State`:

```swift
struct DetailView: View {
    @Environment(\.settings) private var settings

    var body: some View {
        // settings isn't @State, so $settings.darkMode won't compile directly
        @Bindable var settings = settings
        Toggle("Dark Mode", isOn: $settings.darkMode)
    }
}
```

## Bindings

Avoid `Binding(get:set:)` in body. Use `@State`/`@Binding` with `onChange`:

```swift
// Bad: fragile manual binding
TextField("Name", text: Binding(
    get: { model.name },
    set: { model.name = $0; model.save() }
))

// Good: clean separation
TextField("Name", text: $model.name)
    .onChange(of: model.name) { model.save() }
```

## SwiftData

### Model Design

```swift
@Model
final class Tab {
    var title: String = ""
    var url: URL?

    @Relationship(deleteRule: .cascade, inverse: \Page.tab)
    var pages: [Page] = []

    @Transient
    var runtimeState: RuntimeState?  // Not persisted
}
```

- `@Transient` for runtime-only properties on persistent models.
- Specify delete rules explicitly: `.cascade`, `.nullify`, `.deny`.
- Relationships are lazy-loaded by default.

### Saving Strategy

Never save on every mutation. Debounce writes:

```swift
@Observable @MainActor
final class PersistenceManager {
    private var saveTask: Task<Void, Never>?
    private let modelContext: ModelContext

    func scheduleSave() {
        saveTask?.cancel()
        saveTask = Task {
            try? await Task.sleep(for: .seconds(1.5))
            guard !Task.isCancelled else { return }
            try? modelContext.save()
        }
    }
}
```

### CloudKit Constraints

When using SwiftData with CloudKit sync:

- Never use `@Attribute(.unique)` — conflicts with sync.
- All properties must have defaults or be optional.
- All relationships must be optional.

### Querying

- `@Query` for simple, declarative fetches in views.
- `FetchDescriptor` for complex queries with predicates, sort, and limits.
- Relationship traversal for connected data — no separate fetch needed.

### @ModelActor for Background Operations

`@ModelActor` creates an actor with its own `ModelContext` — use for batch operations, imports, or any persistence work that shouldn't block the main actor.

```swift
@ModelActor
actor DataImporter {
    // modelContext and modelContainer are synthesized by the macro

    func importItems(_ dtos: [ItemDTO]) throws {
        for dto in dtos {
            let item = Item(title: dto.title, url: dto.url)
            modelContext.insert(item)
        }
        try modelContext.save()
    }

    func pruneOldItems(before date: Date) throws -> Int {
        let descriptor = FetchDescriptor<Item>(
            predicate: #Predicate { $0.lastAccessed < date }
        )
        let stale = try modelContext.fetch(descriptor)
        for item in stale {
            modelContext.delete(item)
        }
        try modelContext.save()
        return stale.count
    }
}

// Usage from MainActor:
let importer = DataImporter(modelContainer: modelContainer)
try await importer.importItems(parsed)
```

**Key rules:**
- Pass `PersistentIdentifier` across actor boundaries, not model objects — models are not `Sendable`. Re-fetch on the other side.
- Each `@ModelActor` instance has its own `ModelContext`. Changes are isolated until `save()` is called.
- Don't share `ModelContext` between actors — each actor must use its own.

## @AppStorage

- Only works inside `View` structs. Does NOT trigger updates inside `@Observable` classes, even with `@ObservationIgnored`.
- Never store sensitive data (passwords, tokens) — use Keychain.

## Identifiable

Prefer conforming types to `Identifiable` rather than specifying `id: \.property` in `ForEach`.
