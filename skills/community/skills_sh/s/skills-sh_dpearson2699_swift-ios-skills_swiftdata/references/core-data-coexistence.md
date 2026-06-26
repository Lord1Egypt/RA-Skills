# Core Data Coexistence

Guidance for using SwiftData alongside an existing Core Data store and for
planning a transition from Core Data to SwiftData. For apps that are staying on
Core Data without SwiftData, use the sibling `core-data` skill instead.

When a request says "Core Data" but the actual work is shared-store
coexistence, gradual screen migration to `@Model`, or mapping a `.xcdatamodeld`
to SwiftData types, route to this SwiftData skill. Answer only the high-level
boundary first; do not turn the response into a full SwiftData migration plan
unless the user asks for implementation detail.

## Contents

- [Core Data + SwiftData Coexistence](#core-data--swiftdata-coexistence)
- [Migration from Core Data to SwiftData](#migration-from-core-data-to-swiftdata)

## Core Data + SwiftData Coexistence

Apple's current coexistence sample is documented as iOS 27 / Xcode 27 beta.
Use it as source-grounded migration guidance, not as an unconditional iOS 26
platform guarantee. For shipping work on earlier SDKs, verify the exact
deployment target and test against copies of real stores.

Docs: [Adopting SwiftData for a Core Data app](https://sosumi.ai/documentation/coredata/adopting-swiftdata-for-a-core-data-app)

### Using the Same Underlying Store

Both stacks must point to the same SQLite file and agree on the schema. The
Core Data `.xcdatamodeld` and SwiftData `@Model` classes must describe the
same entities and properties.

```swift
import SwiftData
import CoreData

// 1. Determine the store URL that Core Data already uses
let storeURL = NSPersistentContainer.defaultDirectoryURL()
    .appendingPathComponent("MyAppModel.sqlite")

// 2. Point SwiftData at the same store
let config = ModelConfiguration(
    "MyAppModel",
    url: storeURL
)

let container = try ModelContainer(
    for: Trip.self,
    configurations: config
)
```

### ModelConfiguration Pointing to Existing Core Data Store

Key rules for coexistence:

1. The `@Model` class name must match the Core Data entity name.
2. Property names, relationship shapes, and value types must match the existing
   store schema.
3. Use `@Attribute(originalName:)` when the SwiftData property name differs
   from the persisted Core Data property name.
4. Both stacks should use the same store file.
5. Standalone Core Data remains the right scope for apps that are not adopting
   SwiftData.

```swift
// Core Data entity: CDTrip (entity name "Trip" in .xcdatamodeld)
// Attributes: name (String), destination (String), startDate (Date),
//             isFavorite (Boolean), imageData (Binary Data)

// Matching SwiftData model
@Model
class Trip {
    var name: String
    var destination: String
    var startDate: Date
    var isFavorite: Bool = false
    @Attribute(.externalStorage) var imageData: Data?

    init(name: String, destination: String, startDate: Date) {
        self.name = name
        self.destination = destination
        self.startDate = startDate
    }
}
```

### Gradual Coexistence Strategy

```swift
// Phase 1: Core Data stack still handles writes;
//          SwiftData reads the same store for new UI
@main
struct MyApp: App {
    let existingCoreDataStoreURL = NSPersistentContainer.defaultDirectoryURL()
        .appendingPathComponent("MyAppModel.sqlite")

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        // SwiftData reads from the same store
        .modelContainer(for: Trip.self, configurations:
            ModelConfiguration(url: existingCoreDataStoreURL)
        )
    }
}

// Phase 2: New features use SwiftData for both reads and writes
// Phase 3: Migrate remaining Core Data code to SwiftData
// Phase 4: Remove Core Data stack and .xcdatamodeld
```

### Important Coexistence Rules

- **Do not write to the same entity from both stacks simultaneously.** Pick
  one stack per entity for writes to avoid conflicts.
- Enable persistent history tracking on the Core Data side when using Apple's
  beta coexistence pattern; SwiftData history can then detect relevant changes.
- Test thoroughly -- schema mismatches between the `.xcdatamodeld` and
  `@Model` cause crashes.

## Migration from Core Data to SwiftData

### Step 1: Map Core Data Entities to `@Model` Classes

Create a `@Model` class for each Core Data entity. Property names and types
must align with the `.xcdatamodeld` definition.

```swift
// Core Data entity "Article"
// Attributes: id (UUID), title (String), body (String),
//             createdAt (Date), isDraft (Boolean)
// Relationships: author (to-one → Author), tags (to-many → Tag)

@Model
class Article {
    @Attribute(.unique) var id: UUID
    var title: String
    var body: String
    var createdAt: Date
    var isDraft: Bool = true

    @Relationship(deleteRule: .nullify, inverse: \Author.articles)
    var author: Author?

    @Relationship(deleteRule: .nullify, inverse: \Tag.articles)
    var tags: [Tag] = []

    init(id: UUID = UUID(), title: String, body: String, createdAt: Date = .now) {
        self.id = id
        self.title = title
        self.body = body
        self.createdAt = createdAt
    }
}

@Model
class Author {
    @Attribute(.unique) var id: UUID
    var name: String
    var articles: [Article] = []

    init(id: UUID = UUID(), name: String) {
        self.id = id
        self.name = name
    }
}

@Model
class Tag {
    @Attribute(.unique) var id: UUID
    var name: String
    var articles: [Article] = []

    init(id: UUID = UUID(), name: String) {
        self.id = id
        self.name = name
    }
}
```

### Type Mapping Reference

| Core Data Type | SwiftData Type |
|---|---|
| String | String |
| Boolean | Bool |
| Integer 16/32/64 | Int |
| Float / Double | Float / Double |
| Date | Date |
| Binary Data | Data |
| UUID | UUID |
| URI | URL |
| Decimal | Decimal |
| Transformable | Compatible `Codable` value type; `Schema.CompositeAttribute` is iOS 17+, while `@Attribute(.codable)` is iOS 27 beta |
| To-one relationship | Optional reference to `@Model` |
| To-many relationship | Array of `@Model` |

### Step 2: Schema Versioning Considerations

If the Core Data store has existing data, SwiftData must be able to open it.
Use `VersionedSchema` and `SchemaMigrationPlan` for non-trivial changes.

```swift
// If the SwiftData model exactly matches the Core Data schema,
// no migration is needed -- SwiftData opens the store directly.

// For schema differences, define versioned schemas:
enum SchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] { [Article.self, Author.self] }

    @Model class Article {
        var id: UUID
        var title: String
        var body: String
        var createdAt: Date
        init(id: UUID, title: String, body: String, createdAt: Date) {
            self.id = id; self.title = title
            self.body = body; self.createdAt = createdAt
        }
    }

    @Model class Author {
        var id: UUID
        var name: String
        init(id: UUID, name: String) { self.id = id; self.name = name }
    }
}

enum SchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] { [Article.self, Author.self, Tag.self] }

    @Model class Article {
        var id: UUID
        var title: String
        var body: String
        var createdAt: Date
        var isDraft: Bool = true  // New property
        init(id: UUID, title: String, body: String, createdAt: Date) {
            self.id = id; self.title = title
            self.body = body; self.createdAt = createdAt
        }
    }

    @Model class Author {
        var id: UUID
        var name: String
        init(id: UUID, name: String) { self.id = id; self.name = name }
    }

    @Model class Tag {
        var id: UUID
        var name: String
        init(id: UUID, name: String) { self.id = id; self.name = name }
    }
}

enum ArticleMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [SchemaV1.self, SchemaV2.self] }
    static var stages: [MigrationStage] {
        [MigrationStage.lightweight(fromVersion: SchemaV1.self, toVersion: SchemaV2.self)]
    }
}
```

### Step 3: Testing Migration Paths

Always test migration with real production data copies before shipping.

```swift
import XCTest
import SwiftData

final class MigrationTests: XCTestCase {

    func testCoreDataToSwiftDataMigration() throws {
        // 1. Copy a known Core Data store into the test bundle
        let sourceURL = Bundle(for: type(of: self))
            .url(forResource: "TestStore", withExtension: "sqlite")!

        let tempDir = FileManager.default.temporaryDirectory
            .appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)

        let destURL = tempDir.appendingPathComponent("TestStore.sqlite")
        try FileManager.default.copyItem(at: sourceURL, to: destURL)

        // Copy WAL and SHM if they exist
        for ext in ["-wal", "-shm"] {
            let src = sourceURL.deletingLastPathComponent()
                .appendingPathComponent("TestStore.sqlite\(ext)")
            if FileManager.default.fileExists(atPath: src.path) {
                try FileManager.default.copyItem(
                    at: src,
                    to: tempDir.appendingPathComponent("TestStore.sqlite\(ext)")
                )
            }
        }

        // 2. Open with SwiftData
        let config = ModelConfiguration(url: destURL)
        let container = try ModelContainer(
            for: SchemaV2.Article.self,
            migrationPlan: ArticleMigrationPlan.self,
            configurations: config
        )

        // 3. Verify data survived migration
        let context = ModelContext(container)
        let articles = try context.fetch(FetchDescriptor<SchemaV2.Article>())
        XCTAssertFalse(articles.isEmpty, "Migration should preserve existing articles")

        // 4. Verify new properties have defaults
        for article in articles {
            XCTAssertTrue(article.isDraft, "New isDraft property should default to true")
        }

        // Cleanup
        try FileManager.default.removeItem(at: tempDir)
    }
}
```

### Migration Checklist

- [ ] Every Core Data entity has a matching `@Model` class with identical property names and types
- [ ] Relationship inverse properties are specified in both directions
- [ ] `VersionedSchema` and `SchemaMigrationPlan` defined for non-trivial schema changes
- [ ] `ModelConfiguration` points to the existing Core Data SQLite file
- [ ] Tested migration with a copy of production data
- [ ] Only one stack writes to each entity during coexistence
- [ ] `automaticallyMergesChangesFromParent` enabled on Core Data's `viewContext`
- [ ] `.xcdatamodeld` removed only after full migration is verified
