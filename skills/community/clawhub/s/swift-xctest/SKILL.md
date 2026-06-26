---
name: swift-xctest
description: Swift 6 + XCTest testing patterns for macOS/iOS apps using SwiftData, EventKit, and SwiftUI
domain: ios-macos
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/swift-xctest
metadata:
  clawdbot:
    emoji: 🧩
---

# Swift/XCTest Testing Skill

Expert-level XCTest patterns for Swift 6 macOS/iOS applications. Specialized for SwiftData, EventKit, SwiftUI, and strict concurrency.

## When to Use

Use this skill when:
- Writing XCTest for Swift 6 applications
- Testing SwiftData models with in-memory containers
- Testing Swift 6 actors and `@MainActor` isolation
- Testing EventKit integrations
- Testing SwiftUI views and @Observable ViewModels
- Writing performance tests for macOS apps

## Core Principles

### 1. SwiftData Testing Pattern

```swift
import SwiftData
import XCTest

@MainActor
final class ModelTests: XCTestCase {
    var container: ModelContainer!
    var context: ModelContext!

    override func setUp() async throws {
        try await super.setUp()
        // Use in-memory config for isolated tests
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        container = try ModelContainer(for: YourModel.self, configurations: config)
        context = container.mainContext
    }

    override func tearDown() async throws {
        container = nil
        context = nil
        try await super.tearDown()
    }
}
```

### 2. Swift 6 Actor Testing

```swift
@MainActor
final class ServiceTests: XCTestCase {
    var service: YourActor!

    override func setUp() async throws {
        try await super.setUp()
        service = YourActor()
    }

    func testActorMethod() async throws {
        // Actor-isolated tests work naturally with async
        let result = try await service.method()
        XCTAssertEqual(result, expected)
    }
}
```

### 3. Given-When-Then Pattern

```swift
func testFeature() async throws {
    // Given: Set up initial state
    let task = service.createTask(title: "Test")

    // When: Perform action
    task.complete()

    // Then: Verify result
    XCTAssertTrue(task.isCompleted)
}
```

### 4. Test Organization

```swift
@MainActor
final class FeatureTests: XCTestCase {
    // MARK: - Properties
    // Test dependencies

    // MARK: - Setup & Teardown
    // setUp/tearDown methods

    // MARK: - Unit Tests
    // Isolated tests

    // MARK: - Integration Tests
    // Tests across components

    // MARK: - Edge Cases
    // Boundary and error conditions

    // MARK: - Performance Tests
    // Performance benchmarks
}
```

## Testing Guidelines

### SwiftData Models
- Always use `ModelConfiguration(isStoredInMemoryOnly: true)`
- Mark test classes with `@MainActor`
- Use `try context.save()` after mutations
- Verify state with `FetchDescriptor` and `#Predicate`

### Actors & Concurrency
- Test classes interacting with actors should be `@MainActor`
- Use `await` for all actor methods
- Test isolation boundaries with `nonisolated` tests where appropriate

### SwiftData Services
- Use in-memory mode: `YourService(inMemory: true)`
- Test fetch, create, update, delete operations
- Verify `FetchDescriptor` queries with predicates

### EventKit Mocking
- Mock `EKEventStore` for isolated testing
- Test permission handling scenarios
- Verify `EKReminder` to model mapping

### SwiftUI Views
- Use `@Testable import` to access internal types
- Test `@Observable` ViewModel behavior
- Test state transitions and side effects

## Best Practices

1. **Isolation**: Each test should be independent
2. **Async-Safety**: Use `async/await` for all async operations
3. **MainActor**: Mark SwiftData tests with `@MainActor`
4. **Performance**: Use `measure` blocks for critical paths
5. **Readability**: Use Given-When-Then comments
6. **Organization**: Group tests with `// MARK:` sections

## Performance Testing

```swift
func testPerformance() async throws {
    measure {
        // Code to measure
        _ = service.process(data: largeDataSet)
    }
}
```

## Common Test Patterns

### Batch Query Testing
```swift
func testBatchFetchEfficiency() async throws {
    let ids = (0..<100).map { "ID-\($0)" }
    let start = Date()
    let results = service.fetch(by: ids)
    let duration = Date().timeIntervalSince(start)

    XCTAssertEqual(results.count, 100)
    XCTAssertLessThan(duration, 0.5, "Batch fetch should be fast")
}
```

### Predicate Testing
```swift
func testPredicateFiltering() async throws {
    let descriptor = FetchDescriptor<IdentityMap>(
        predicate: #Predicate { $0.isDirty == true }
    )
    let results = try context.fetch(descriptor)
    XCTAssertEqual(results.count, expectedCount)
}
```

## Running Tests

```bash
# Run all tests
xcodebuild test -scheme YourApp -destination 'platform=macOS'

# Run specific test
xcodebuild test -scheme YourApp -destination 'platform=macOS' \
  -only-testing:'YourAppTests/FeatureTests/testMethod'

# Run with performance output
xcodebuild test -scheme YourApp -destination 'platform=macOS' \
  -resultBundlePath ~/TestResults.xcresult
```
