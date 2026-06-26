# AppMigrationKit Patterns

Extended patterns and recipes for AppMigrationKit. Covers combined
export/import extensions, versioned data migration, directory enumeration,
platform-specific handling, error recovery, and SwiftUI integration for
migration status.

## Contents

- [Combined Export and Import Extension](#combined-export-and-import-extension)
- [Versioned Data Migration](#versioned-data-migration)
- [Directory Enumeration for Export](#directory-enumeration-for-export)
- [Platform-Specific Export](#platform-specific-export)
- [Selective Export with Options](#selective-export-with-options)
- [Error Recovery on Import](#error-recovery-on-import)
- [Migration Status in SwiftUI](#migration-status-in-swiftui)
- [Testing Export and Import Round-Trip](#testing-export-and-import-round-trip)
- [File Size Estimation](#file-size-estimation)

## Combined Export and Import Extension

A single extension type can conform to both export and import protocols.
This is the typical pattern when the same app handles both directions of
migration.

```swift
import AppMigrationKit
import Foundation

struct AppDataMigration: ResourcesExportingWithOptions, ResourcesImporting {
    typealias OptionsType = MigrationDefaultSupportedOptions
    private let importProgress = Progress(totalUnitCount: 100)

    // MARK: - Export Properties

    var resourcesSizeEstimate: Int {
        estimateTotalExportSize()
    }

    var resourcesVersion: String {
        "2.0"
    }

    var resourcesCompressible: Bool {
        true
    }

    // MARK: - Export

    func exportResources(
        to archiver: sending ResourcesArchiver,
        request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
    ) async throws {
        let docs = appContainer.documentsDirectory
        let appSupport = appContainer.applicationSupportDirectory

        // Export user data
        try await archiver.appendItem(
            at: docs.appending(path: "profile.json"),
            pathInArchive: "user/profile.json"
        )

        // Export preferences
        try await archiver.appendItem(
            at: appSupport.appending(path: "settings.json"),
            pathInArchive: "config/settings.json"
        )

        // Export media directory
        let mediaDir = docs.appending(path: "media")
        if FileManager.default.fileExists(atPath: mediaDir.path()) {
            try await archiver.appendItem(
                at: mediaDir,
                pathInArchive: "media"
            )
        }
    }

    // MARK: - Import

    var resourcesImportProgress: Progress { importProgress }

    func importResources(
        at importedDataURL: URL,
        request: ResourcesImportRequest
    ) async throws {
        let docs = appContainer.documentsDirectory
        let appSupport = appContainer.applicationSupportDirectory
        let fm = FileManager.default

        // Phase 1: Import user data (40%)
        let profileSource = importedDataURL.appending(path: "user/profile.json")
        if fm.fileExists(atPath: profileSource.path()) {
            try fm.copyItem(
                at: profileSource,
                to: docs.appending(path: "profile.json")
            )
        }
        importProgress.completedUnitCount = 40

        // Phase 2: Import settings (20%)
        let settingsSource = importedDataURL.appending(path: "config/settings.json")
        if fm.fileExists(atPath: settingsSource.path()) {
            try fm.copyItem(
                at: settingsSource,
                to: appSupport.appending(path: "settings.json")
            )
        }
        importProgress.completedUnitCount = 60

        // Phase 3: Import media (40%)
        let mediaSource = importedDataURL.appending(path: "media")
        if fm.fileExists(atPath: mediaSource.path()) {
            try fm.copyItem(
                at: mediaSource,
                to: docs.appending(path: "media")
            )
        }
        importProgress.completedUnitCount = 100
    }

    // MARK: - Helpers

    private func estimateTotalExportSize() -> Int {
        let docs = appContainer.documentsDirectory
        let appSupport = appContainer.applicationSupportDirectory
        return directorySize(docs) + directorySize(appSupport)
    }

    private func directorySize(_ url: URL) -> Int {
        let fm = FileManager.default
        guard let enumerator = fm.enumerator(
            at: url,
            includingPropertiesForKeys: [.fileSizeKey],
            options: [.skipsHiddenFiles]
        ) else { return 0 }

        var total = 0
        for case let fileURL as URL in enumerator {
            let size = (try? fileURL.resourceValues(forKeys: [.fileSizeKey]))?.fileSize ?? 0
            total += size
        }
        return total
    }
}
```

## Versioned Data Migration

When the exported data format evolves over time, use `resourcesVersion` on
export and `sourceVersion` on import to handle format differences.

```swift
struct VersionedMigration: ResourcesExportingWithOptions, ResourcesImporting {
    typealias OptionsType = MigrationDefaultSupportedOptions

    // Current export format version
    var resourcesVersion: String { "3.0" }
    var resourcesSizeEstimate: Int { estimateSize() }
    var resourcesCompressible: Bool { true }

    func exportResources(
        to archiver: sending ResourcesArchiver,
        request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
    ) async throws {
        // Always export in the latest format
        let manifest = ExportManifest(
            version: resourcesVersion,
            exportDate: Date(),
            fileCount: countExportableFiles()
        )
        let manifestURL = writeManifest(manifest)
        try await archiver.appendItem(at: manifestURL, pathInArchive: "manifest.json")

        // Export data files
        try await exportCurrentFormatFiles(to: archiver)
    }

    func importResources(
        at importedDataURL: URL,
        request: ResourcesImportRequest
    ) async throws {
        let sourceVersion = request.sourceVersion

        switch sourceVersion {
        case "3.0":
            try await importV3(from: importedDataURL)
        case "2.0":
            try await importV2(from: importedDataURL)
        case "1.0":
            try await importV1(from: importedDataURL)
        default:
            throw MigrationError.unsupportedVersion(sourceVersion)
        }
    }

    // MARK: - Version-specific import

    private func importV3(from url: URL) async throws {
        // Direct import -- current format
        let docs = appContainer.documentsDirectory
        try copyContents(from: url, to: docs)
    }

    private func importV2(from url: URL) async throws {
        // V2 used a flat file structure; remap to V3 directories
        let docs = appContainer.documentsDirectory
        let fm = FileManager.default

        let files = try fm.contentsOfDirectory(at: url, includingPropertiesForKeys: nil)
        for file in files {
            let name = file.lastPathComponent
            let destination: URL
            if name.hasSuffix(".json") {
                destination = docs.appending(path: "data/\(name)")
            } else {
                destination = docs.appending(path: "assets/\(name)")
            }
            try fm.createDirectory(
                at: destination.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            try fm.copyItem(at: file, to: destination)
        }
    }

    private func importV1(from url: URL) async throws {
        // V1 used a single archive file
        let archiveURL = url.appending(path: "data.archive")
        guard FileManager.default.fileExists(atPath: archiveURL.path()) else {
            throw MigrationError.missingArchive
        }
        try await unpackLegacyArchive(at: archiveURL)
    }
}

enum MigrationError: Error {
    case unsupportedVersion(String)
    case missingArchive
    case importFailed(String)
}
```

## Directory Enumeration for Export

When exporting a large number of files, enumerate directories and append
each file individually. This keeps the archiver progressing and avoids
timeouts.

```swift
func exportResources(
    to archiver: sending ResourcesArchiver,
    request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
) async throws {
    let docs = appContainer.documentsDirectory
    let fm = FileManager.default

    guard let enumerator = fm.enumerator(
        at: docs,
        includingPropertiesForKeys: [.isRegularFileKey],
        options: [.skipsHiddenFiles, .skipsPackageDescendants]
    ) else { return }

    for case let fileURL as URL in enumerator {
        let resourceValues = try fileURL.resourceValues(forKeys: [.isRegularFileKey])
        guard resourceValues.isRegularFile == true else { continue }

        // Compute relative path for archive
        let relativePath = fileURL.path().replacingOccurrences(
            of: docs.path(),
            with: ""
        )
        let archivePath = "documents\(relativePath)"

        try await archiver.appendItem(at: fileURL, pathInArchive: archivePath)
    }
}
```

Append files one at a time rather than collecting them first. The system
monitors for continuous progress and may terminate the extension if it
stalls.

## Platform-Specific Export

Use `MigrationRequestWithOptions.destinationPlatform` to tailor exports.
This is useful when the same app exists on multiple platforms with different
data format expectations.

```swift
func exportResources(
    to archiver: sending ResourcesArchiver,
    request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
) async throws {
    let docs = appContainer.documentsDirectory

    // Common data -- exported regardless of platform
    try await archiver.appendItem(
        at: docs.appending(path: "user_profile.json"),
        pathInArchive: "common/user_profile.json"
    )

    // Platform-specific data
    switch request.destinationPlatform {
    case .android:
        // Android app expects a specific database format
        try await archiver.appendItem(
            at: docs.appending(path: "app.sqlite"),
            pathInArchive: "database/app.db"
        )
    default:
        // iOS/default format
        try await archiver.appendItem(
            at: docs.appending(path: "app.sqlite"),
            pathInArchive: "database/app.sqlite"
        )
    }
}
```

### Custom Platforms

For platforms beyond Android, create custom `MigrationPlatform` values:

```swift
let customPlatform = MigrationPlatform("windows")

// In export:
if request.destinationPlatform == customPlatform {
    // Windows-specific export
}
```

## Selective Export with Options

`ResourcesExportingWithOptions` supports a custom `OptionsType` to let the
destination device request specific data categories. For most apps,
`MigrationDefaultSupportedOptions` is sufficient.

```swift
struct MyMigration: ResourcesExportingWithOptions {
    typealias OptionsType = MigrationDefaultSupportedOptions

    var resourcesSizeEstimate: Int { estimateSize() }
    var resourcesVersion: String { "1.0" }
    var resourcesCompressible: Bool { true }

    func exportResources(
        to archiver: sending ResourcesArchiver,
        request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
    ) async throws {
        let options = request.options
        let docs = appContainer.documentsDirectory

        // Check which categories the destination requested
        for (option, _) in options {
            switch option {
            case _ where MigrationDefaultSupportedOptions.allCases.contains(option):
                // Handle known option
                break
            default:
                break
            }
        }

        // Export core data regardless of options
        try await archiver.appendItem(at: docs.appending(path: "core_data.json"))
    }
}
```

Use `ResourcesExporting` (without options) when the extension always exports
the same data regardless of what the destination requests:

```swift
struct SimpleMigration: ResourcesExporting {
    var resourcesSizeEstimate: Int { estimateSize() }
    var resourcesVersion: String { "1.0" }
    var resourcesCompressible: Bool { true }

    func exportResources(
        to archiver: sending ResourcesArchiver,
        request: MigrationRequest
    ) async throws {
        // MigrationRequest has destinationPlatform but no options
        try await archiver.appendItem(at: appContainer.documentsDirectory)
    }
}
```

## Error Recovery on Import

The system clears the app's data container on import failure but does not
touch app group containers. Implement defensive import to handle this.

```swift
struct DefensiveMigration: ResourcesImporting {
    private let importProgress = Progress(totalUnitCount: 100)

    var resourcesImportProgress: Progress { importProgress }

    func importResources(
        at importedDataURL: URL,
        request: ResourcesImportRequest
    ) async throws {
        let fm = FileManager.default

        // Step 1: Clear shared containers before any writes
        clearAppGroupContainers()
        importProgress.completedUnitCount = 10

        // Step 2: Validate imported data before committing
        let manifest = try loadManifest(from: importedDataURL)
        try validateManifest(manifest, sourceVersion: request.sourceVersion)
        importProgress.completedUnitCount = 20

        // Step 3: Import with file-level error handling
        let files = try fm.contentsOfDirectory(
            at: importedDataURL,
            includingPropertiesForKeys: nil
        )
        let filesExcludingManifest = files.filter { $0.lastPathComponent != "manifest.json" }

        let progressPerFile = Int64(80 / max(filesExcludingManifest.count, 1))

        for file in filesExcludingManifest {
            do {
                try importFile(file)
                importProgress.completedUnitCount += progressPerFile
            } catch {
                // Log optional-file failures only when the app can safely
                // regenerate or omit that data after launch.
                if isCriticalFile(file) {
                    throw error  // System clears container on throw
                }
                logImportWarning(file: file, error: error)
            }
        }
        importProgress.completedUnitCount = 100
    }

    private func clearAppGroupContainers() {
        let fm = FileManager.default
        let groupIDs = ["group.com.example.myapp"]

        for groupID in groupIDs {
            guard let groupURL = fm.containerURL(
                forSecurityApplicationGroupIdentifier: groupID
            ) else { continue }

            // Remove migration-related data only, preserve other shared state
            let migrationDataURL = groupURL.appending(path: "migrated_data")
            try? fm.removeItem(at: migrationDataURL)
        }
    }

    private func isCriticalFile(_ url: URL) -> Bool {
        let criticalNames = ["user_profile.json", "account.json", "core_data.sqlite"]
        return criticalNames.contains(url.lastPathComponent)
    }
}
```

### Deciding What Constitutes a Critical Failure

- Missing user account data, authentication tokens, or primary database --
  throw to trigger container cleanup. The user can retry migration.
- Missing thumbnails, caches, or preference files -- log and continue.
  The app can regenerate these on first launch.

## Migration Status in SwiftUI

Check migration status from a SwiftUI app's entry point or root view and
present appropriate UI.

```swift
import SwiftUI
import AppMigrationKit

@main
struct MyApp: App {
    @State private var migrationResult: MigrationResult?

    var body: some Scene {
        WindowGroup {
            ContentView()
                .task {
                    checkMigration()
                }
                .sheet(item: $migrationResult) { result in
                    MigrationResultView(result: result)
                }
        }
    }

    private func checkMigration() {
        guard let status = MigrationStatus.importStatus else { return }

        switch status {
        case .success:
            migrationResult = MigrationResult(succeeded: true, errorMessage: nil)
        case .failure(let error):
            migrationResult = MigrationResult(
                succeeded: false,
                errorMessage: error.localizedDescription
            )
        }

        MigrationStatus.clearImportStatus()
    }
}

struct MigrationResult: Identifiable {
    let id = UUID()
    let succeeded: Bool
    let errorMessage: String?
}

struct MigrationResultView: View {
    let result: MigrationResult
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack {
            Image(systemName: result.succeeded ? "checkmark.circle.fill" : "xmark.circle.fill")
                .font(.system(size: 60))
                .foregroundStyle(result.succeeded ? .green : .red)

            Text(result.succeeded ? "Migration Complete" : "Migration Failed")
                .font(.title2)

            if let errorMessage = result.errorMessage {
                Text(errorMessage)
                    .font(.body)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }

            if result.succeeded {
                Text("Your data has been transferred from your previous device.")
                    .font(.body)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }

            Button("Continue") {
                dismiss()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

## Testing Export and Import Round-Trip

Use `AppMigrationTester` to validate the full export-then-import cycle in
unit tests. The tester is an actor and must be used from async contexts.

```swift
import Testing
import AppMigrationKit
import Foundation

struct MigrationTests {
    @Test func roundTripMigrationPreservesData() async throws {
        // Set up test data in the app container
        let testData = ["name": "Test User", "email": "test@example.com"]
        let testDataURL = FileManager.default.temporaryDirectory
            .appending(path: "test_profile.json")
        let jsonData = try JSONSerialization.data(withJSONObject: testData)
        try jsonData.write(to: testDataURL)

        let tester = try await AppMigrationTester(platform: .android)

        // Test export
        let exportResult = try await tester.exportController.exportResources(
            request: nil,
            progress: nil
        )

        // Verify export produced output
        let props = exportResult.exportProperties
        #expect(props.uncompressedBytes > 0)
        #expect(props.version == "2.0")

        // Verify compressed size if compressible
        if let compressed = props.compressedBytes {
            #expect(compressed <= props.uncompressedBytes)
        }

        // Test import with the exported data
        let importProgress = Progress(totalUnitCount: 100)
        try await tester.importController.importResources(
            from: exportResult.extractedResourcesURL,
            importRequest: nil,
            progress: importProgress
        )

        // Verify progress reached completion
        #expect(importProgress.completedUnitCount == 100)

        // Register success
        try await tester.importController.registerImportCompletion(with: .success)
    }

    @Test func exportWithCustomRequest() async throws {
        let tester = try await AppMigrationTester(platform: .android)

        let request = MigrationRequestWithOptions<MigrationDefaultSupportedOptions>(
            destinationPlatform: .android,
            options: [:]
        )

        let result = try await tester.exportController.exportResources(
            request: request,
            progress: nil
        )

        #expect(result.exportProperties.sizeEstimate > 0)
    }

    @Test func importWithSourceIdentifier() async throws {
        let tester = try await AppMigrationTester(platform: .android)

        // Export data first
        let exportResult = try await tester.exportController.exportResources(
            request: nil,
            progress: nil
        )

        // Create an import request with source app info
        let sourceApp = MigrationAppIdentifier(
            storeIdentifier: .googlePlay,
            bundleIdentifier: "com.example.androidapp",
            platform: .android
        )
        let importRequest = ResourcesImportRequest(
            sourceAppIdentifier: sourceApp,
            sourceVersion: "2.0"
        )

        try await tester.importController.importResources(
            from: exportResult.extractedResourcesURL,
            importRequest: importRequest,
            progress: nil
        )

        try await tester.importController.registerImportCompletion(with: .success)
    }

    @Test func importFailureRegistersCorrectStatus() async throws {
        let tester = try await AppMigrationTester(platform: .android)

        // Register a failure status
        let error = MigrationError.importFailed("Test failure")
        try await tester.importController.registerImportCompletion(
            with: .failure(error)
        )

        // In production, the app would see MigrationStatus.importStatus == .failure
    }
}
```

## File Size Estimation

Accurate size estimation improves the user experience during migration. The
system uses `resourcesSizeEstimate` for progress display and free-space
checks on the destination device.

```swift
struct AccurateSizeMigration: ResourcesExportingWithOptions {
    typealias OptionsType = MigrationDefaultSupportedOptions

    var resourcesSizeEstimate: Int {
        let docs = appContainer.documentsDirectory
        let appSupport = appContainer.applicationSupportDirectory

        // Calculate size of directories to export
        var total = 0
        total += sizeOfDirectory(docs, excludingPaths: ["Caches", "tmp"])
        total += sizeOfFile(appSupport.appending(path: "settings.json"))
        return total
    }

    var resourcesVersion: String { "1.0" }
    var resourcesCompressible: Bool { true }

    func exportResources(
        to archiver: sending ResourcesArchiver,
        request: MigrationRequestWithOptions<MigrationDefaultSupportedOptions>
    ) async throws {
        // Export implementation
    }

    // MARK: - Size calculation

    private func sizeOfDirectory(_ url: URL, excludingPaths: [String] = []) -> Int {
        let fm = FileManager.default
        guard let enumerator = fm.enumerator(
            at: url,
            includingPropertiesForKeys: [.fileSizeKey, .isRegularFileKey],
            options: [.skipsHiddenFiles]
        ) else { return 0 }

        var total = 0
        for case let fileURL as URL in enumerator {
            // Skip excluded paths
            let relativePath = fileURL.path().replacingOccurrences(of: url.path(), with: "")
            if excludingPaths.contains(where: { relativePath.hasPrefix("/\($0)") }) {
                continue
            }

            let values = try? fileURL.resourceValues(forKeys: [.fileSizeKey, .isRegularFileKey])
            if values?.isRegularFile == true {
                total += values?.fileSize ?? 0
            }
        }
        return total
    }

    private func sizeOfFile(_ url: URL) -> Int {
        let values = try? url.resourceValues(forKeys: [.fileSizeKey])
        return values?.fileSize ?? 0
    }
}
```

Estimation guidelines:

- Exclude caches and temporary files from the estimate if they are not
  exported.
- Overestimating is better than underestimating -- the destination device
  may reject migration if it runs out of space mid-transfer.
- The estimate does not need to be exact. A margin of 10-20% over actual
  size is reasonable.
