---
name: swiftdata-patterns
description: SwiftData best practices, batch queries, N+1 avoidance, and model relationships for macOS/iOS apps
Data: SwiftData best practices, batch queries, N+1 avoidance, and model relationships for macOS/iOS apps
domain: ios-macos
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/swiftdata-patterns
metadata:
  clawdbot:
    emoji: 🗄️
---

# SwiftData Patterns

Expert-level SwiftData patterns for macOS/iOS applications. Optimized for performance, relationships, and production readiness.

## When to Use

Use this skill when:
- Designing SwiftData models
- Writing SwiftData queries
- Optimizing batch operations
- Setting up model relationships
- Handling persistence layer architecture
- Avoiding N+1 query problems

---

## Core Principles

### 1. Model Design

```swift
@Model
final class YourModel {
    @Attribute(.unique) var id: UUID

    // Use external storage for large data
    @Attribute(.externalStorage) var largeData: Data?

    // Relationships with cascade delete
    @Relationship(deleteRule: .cascade)
    var children: [ChildModel]?

    init(id: UUID = UUID()) {
        self.id = id
    }
}
```

### 2. FetchDescriptor Best Practices

```swift
// Use predicate for filtering
let descriptor = FetchDescriptor<YourModel>(
    predicate: #Predicate { $0.isActive && $0.createdAt >= startDate },
    sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
)

// Batch fetch by IDs (N+1 avoidance)
func fetchModels(by ids: [UUID]) -> [YourModel] {
    guard !ids.isEmpty else { return [] }

    let descriptor = FetchDescriptor<YourModel>(
        predicate: #Predicate { ids.contains($0.id) }
    )
    return (try? context.fetch(descriptor)) ?? []
}
```

### 3. In-Memory Testing Pattern

```swift
@MainActor
final class ModelTests: XCTestCase {
    var container: ModelContainer!
    var context: ModelContext!

    override func setUp() async throws {
        try await super.setUp()
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        container = try ModelContainer(for: YourModel.self, configurations: config)
        context = container.mainContext
    }

    override func tearDown() async throws {
        try await super.tearDown()
        container = nil
        context = nil
    }
}
```

### 4. Service Layer Pattern

```swift
@MainActor
final class DataService {
    nonisolated let container: ModelContainer
    let context: ModelContext

    init(inMemory: Bool = false) throws {
        let configuration = ModelConfiguration(isStoredInMemoryOnly: inMemory)
        container = try ModelContainer(for: YourModel.self, configurations: configuration)
        context = ModelContext(container)
        context.autosaveEnabled = false  // Manual save control
    }

    func save() throws {
        try context.save()
    }
}
```

---

## Performance Patterns

### Batch Insert with Chunking

```swift
extension ModelContext {
    func safeBatchInsert<T: PersistentModel>(
        _ objects: [T],
        batchSize: Int = 100
    ) throws {
        for (index, object) in objects.enumerated() {
            insert(object)
            if index % batchSize == 0 {
                try save()
            }
        }
        try save()
    }
}
```

### Avoid N+1 Queries

**Bad - N+1 problem:**
```swift
for reminder in reminders {
    let task = service.findIdentityMap(by: reminder.id)  // N queries!
    process(task)
}
```

**Good - Batch fetch:**
```swift
let ids = reminders.map { $0.id }
let tasks = service.fetchIdentityMaps(by: ids)  // 1 query!

for (index, reminder) in reminders.enumerated() {
    let task = tasks.first { $0.ekIdentifier == reminder.id }
    process(task)
}
```

### Shared Fetch Descriptors

```swift
@MainActor
final class DataService {
    // Nonisolated for thread-safe descriptor access
    nonisolated func descriptorForActiveItems() -> FetchDescriptor<YourModel> {
        FetchDescriptor<YourModel>(
            predicate: #Predicate { $0.isActive },
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )
    }

    // Use in @Observable ViewModels
    func fetchActiveItems() -> [YourModel] {
        try? context.fetch(descriptorForActiveItems()) ?? []
    }
}
```

---

## Model Relationships

### Bidirectional Links

```swift
@Model
final class Note {
    @Attribute(.unique) var id: UUID

    // Forward links
    @Relationship(inverse: \Note.backlinks)
    var forwardLinks: [Note]?

    // Backward links (auto-maintained)
    var backlinks: [Note]?

    init(id: UUID = UUID()) {
        self.id = id
    }
}
```

### Cascade Delete

```swift
@Model
final class Parent {
    @Attribute(.unique) var id: UUID

    @Relationship(deleteRule: .cascade)  // Auto-delete children
    var children: [Child]?
}

@Model
final class Child {
    @Attribute(.unique) var id: UUID
    var parent: Parent?
}
```

---

## Configuration Best Practices

### App Group Support

```swift
private static func createConfiguration(inMemory: Bool) throws -> ModelConfiguration {
    if inMemory {
        return ModelConfiguration(isStoredInMemoryOnly: true)
    }

    let appGroupID = "group.your.app.id"
    guard let containerURL = FileManager.default.containerURL(
        forSecurityApplicationGroupIdentifier: appGroupID
    ) else {
        // Fallback to sandbox
        return createSandboxConfiguration()
    }

    let dataURL = containerURL.appendingPathComponent("App_Data")
    try? FileManager.default.createDirectory(at: dataURL, withIntermediateDirectories: true)
    let storeURL = dataURL.appendingPathComponent("App.sqlite")

    return ModelConfiguration(url: storeURL, cloudKitDatabase: .automatic)
}
```

---

## Testing Guidelines

### Given-When-Then Pattern

```swift
func testBatchFetchPerformance() async throws {
    // Given: Create test data
    let ids = (0..<100).map { _ in
        let model = service.createModel()
        try? context.save()
        return model.id
    }

    // When: Batch fetch
    let start = Date()
    let results = service.fetchModels(by: ids)
    let duration = Date().timeIntervalSince(start)

    // Then: Verify
    XCTAssertEqual(results.count, 100)
    XCTAssertLessThan(duration, 0.5, "Batch fetch should be fast")
}
```

### Predicate Testing

```swift
func testPredicateFiltering() async throws {
    // Given
    let activeModel = service.createModel(isActive: true)
    let inactiveModel = service.createModel(isActive: false)
    try? context.save()

    // When
    let descriptor = FetchDescriptor<YourModel>(
        predicate: #Predicate { $0.isActive }
    )
    let results = try context.fetch(descriptor)

    // Then
    XCTAssertEqual(results.count, 1)
    XCTAssertEqual(results.first?.id, activeModel.id)
}
```

---

## Best Practices

| Practice | Reason |
|----------|---------|
| Use `@MainActor` on services | SwiftData context is main-thread bound |
| External storage for large data | Prevents database bloat |
| Batch fetch for relationships | Avoids N+1 queries |
| Manual autosave control | Prevents unwanted intermediate saves |
| In-memory config for tests | Isolated test state |
| Nonisolated fetch descriptors | Thread-safe descriptor access |

---

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| N+1 queries | Slow sync performance | Use batch `fetch(by: [ID])` |
| Forgetting `@MainActor` | Runtime crashes | All SwiftData services must be isolated |
| Large data inline | Database bloat | Use `@Attribute(.externalStorage)` |
| Auto-save conflicts | Unexpected state changes | Set `autosaveEnabled = false` |
| Missing cascade delete | Orphaned records | Use `deleteRule: .cascade` |

---

## Running SwiftData in Tests

```bash
# Test with SwiftData
xcodebuild test -scheme YourApp \
  -destination 'platform=macOS' \
  -only-testing:'YourAppTests/ModelTests/testBatchFetch'
```
