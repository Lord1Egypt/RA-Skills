# File Storage Patterns

Guidance on choosing the right directory, applying file protection, managing
backup exclusions, and handling storage pressure on iOS.

## Contents

- [Directory Selection Guide](#directory-selection-guide)
- [FileProtectionType Levels](#fileprotectiontype-levels)
- [Backup Exclusion (isExcludedFromBackup)](#backup-exclusion-isexcludedfrombackup)
- [Storage Pressure Handling](#storage-pressure-handling)

## Directory Selection Guide

iOS provides four primary directories for app data. Choose based on whether
the data is user-generated, re-creatable, or temporary.

| Directory | Backed Up | Purged by System | Use For |
|---|---|---|---|
| `Documents/` | Yes | No | User-generated content (documents, exports, user files) |
| `Library/Application Support/` | Yes | No | App-generated supporting files (databases, config, caches that should survive updates) |
| `Library/Caches/` | No | Yes (low storage) | Re-creatable data (downloaded images, API responses, computed data) |
| `tmp/` | No | Yes (anytime) | Truly temporary files (in-progress uploads, scratch files) |

### Accessing Standard Directories

Use `FileManager.default.urls(for:in:)` to get the correct path. Never
hardcode paths.

```swift
import Foundation

// Documents/ — user-generated content, backed up by iCloud/iTunes
let documentsURL = FileManager.default.urls(
    for: .documentDirectory, in: .userDomainMask
).first!

// Library/Application Support/ — app-generated supporting data, backed up
let appSupportURL = FileManager.default.urls(
    for: .applicationSupportDirectory, in: .userDomainMask
).first!
// Create if it doesn't exist (not auto-created)
try FileManager.default.createDirectory(
    at: appSupportURL, withIntermediateDirectories: true
)

// Library/Caches/ — re-creatable data, not backed up, may be purged
let cachesURL = FileManager.default.urls(
    for: .cachesDirectory, in: .userDomainMask
).first!

// tmp/ — temporary files, purged by system periodically
let tmpURL = FileManager.default.temporaryDirectory
```

### Choosing the Right Directory

```swift
// User's exported PDF — Documents/
let exportURL = documentsURL.appendingPathComponent("Report.pdf")
try pdfData.write(to: exportURL)

// App's SQLite database — Library/Application Support/
let dbURL = appSupportURL.appendingPathComponent("AppData.sqlite")

// Downloaded thumbnail cache — Library/Caches/
let thumbURL = cachesURL.appendingPathComponent("thumbnails/\(imageID).jpg")

// In-progress upload — tmp/
let uploadURL = tmpURL.appendingPathComponent(UUID().uuidString + ".tmp")
```

## FileProtectionType Levels

iOS encrypts files at rest using Data Protection. The protection level
determines when the file is accessible relative to the device lock state.

Docs: [FileProtectionType](https://sosumi.ai/documentation/foundation/fileprotectiontype),
[Encrypting Your App's Files](https://sosumi.ai/documentation/uikit/encrypting-your-app-s-files)

| Level | Constant | When Accessible | Use For |
|---|---|---|---|
| Complete | `.complete` | Only when device is unlocked | Sensitive user data (health records, financial data) |
| Complete Unless Open | `.completeUnlessOpen` | Can finish if opened before lock | Active downloads, recordings in progress |
| Until First Auth | `.completeUntilFirstUserAuthentication` | After first unlock (default) | Most app data; background-accessible content |
| None | `.none` | Always, even before first unlock | Non-sensitive system-required data |

### Setting File Protection

```swift
import Foundation

// Option 1: Set protection when writing data
try sensitiveData.write(to: fileURL, options: .completeFileProtection)

// Option 2: Set protection via FileManager attributes
try FileManager.default.setAttributes(
    [.protectionKey: FileProtectionType.complete],
    ofItemAtPath: fileURL.path
)

// Option 3: Set protection on a directory (applies to new files within)
try FileManager.default.setAttributes(
    [.protectionKey: FileProtectionType.complete],
    ofItemAtPath: secureDirectoryURL.path
)
```

### Checking Current Protection Level

```swift
let attributes = try FileManager.default.attributesOfItem(atPath: fileURL.path)
if let protection = attributes[.protectionKey] as? FileProtectionType {
    switch protection {
    case .complete:
        print("File is fully protected")
    case .completeUnlessOpen:
        print("Protected unless already open")
    case .completeUntilFirstUserAuthentication:
        print("Protected until first unlock (default)")
    case .none:
        print("No encryption")
    default:
        break
    }
}
```

### Handling Protected Data Availability

Files with `.complete` protection are inaccessible when the device is locked.
Check availability before accessing:

```swift
import UIKit

// Check if protected data is currently available
if UIApplication.shared.isProtectedDataAvailable {
    // Safe to read .complete files
    let data = try Data(contentsOf: protectedFileURL)
} else {
    // Wait for device unlock
}

// Observe availability changes
NotificationCenter.default.addObserver(
    forName: UIApplication.protectedDataDidBecomeAvailableNotification,
    object: nil,
    queue: .main
) { _ in
    // Protected files are now accessible
}

NotificationCenter.default.addObserver(
    forName: UIApplication.protectedDataWillBecomeUnavailableNotification,
    object: nil,
    queue: .main
) { _ in
    // Close file handles to .complete files
}
```

## Backup Exclusion (isExcludedFromBackup)

Exclude large re-downloadable content from iCloud/iTunes backup to avoid
bloating the user's backup. Apple may reject apps that back up excessive
re-creatable data.

Docs: [URLResourceValues](https://sosumi.ai/documentation/foundation/urlresourcevalues)

### Setting the Exclusion Flag

```swift
import Foundation

// Exclude a file or directory from backup
func excludeFromBackup(_ url: URL) throws {
    var resourceValues = URLResourceValues()
    resourceValues.isExcludedFromBackup = true
    var mutableURL = url
    try mutableURL.setResourceValues(resourceValues)
}

// Usage
let largeCache = cachesURL.appendingPathComponent("video-cache")
try excludeFromBackup(largeCache)
```

### Checking the Exclusion Flag

```swift
func isExcludedFromBackup(_ url: URL) throws -> Bool {
    let values = try url.resourceValues(forKeys: [.isExcludedFromBackupKey])
    return values.isExcludedFromBackup ?? false
}
```

### When to Exclude from Backup

| Exclude | Keep in Backup |
|---|---|
| Downloaded media (images, videos, audio) | User-created documents |
| API response caches | User preferences and settings |
| Generated thumbnails or previews | App databases with user data |
| Offline map tiles | In-app purchase receipts |
| Pre-computed search indexes | User-generated content |

### Common Pattern: Application Support with Exclusion

Store re-downloadable data in Application Support but exclude from backup:

```swift
let offlineDataURL = appSupportURL.appendingPathComponent("OfflineData")
try FileManager.default.createDirectory(
    at: offlineDataURL, withIntermediateDirectories: true
)
try excludeFromBackup(offlineDataURL)

// Files in this directory persist across app updates but don't bloat backup
try downloadedData.write(to: offlineDataURL.appendingPathComponent("map-tiles.db"))
```

## Storage Pressure Handling

When the device runs low on storage, iOS may purge files in `Library/Caches/`
and `tmp/`. Apps should proactively manage storage and respond to low-space
conditions.

### Checking Available Storage

```swift
import Foundation

func availableDiskSpace() throws -> Int64 {
    let values = try URL(fileURLWithPath: NSHomeDirectory())
        .resourceValues(forKeys: [.volumeAvailableCapacityForImportantUsageKey])
    return values.volumeAvailableCapacityForImportantUsage ?? 0
}

// Use .volumeAvailableCapacityForImportantUsageKey for important operations
// Use .volumeAvailableCapacityForOpportunisticUsageKey for optional operations
// The opportunistic value is always <= the important value

func hasSpaceForDownload(bytes: Int64) throws -> Bool {
    let available = try availableDiskSpace()
    return available > bytes
}
```

### Responding to Low Storage Notifications

```swift
import UIKit

// iOS posts this when storage is critically low (UIKit apps)
NotificationCenter.default.addObserver(
    forName: UIApplication.didReceiveMemoryWarningNotification,
    object: nil,
    queue: .main
) { _ in
    // Clear in-memory caches; consider trimming disk caches too
    clearImageCache()
}

// Check storage proactively at app launch or before large operations
func checkStorageAndCleanup() throws {
    let availableBytes = try availableDiskSpace()
    let threshold: Int64 = 100 * 1024 * 1024  // 100 MB

    if availableBytes < threshold {
        try performCleanup()
    }
}
```

### Implementing Cleanup Strategies

```swift
import Foundation

struct StorageCleaner {
    let cachesURL: URL
    let maxCacheAge: TimeInterval  // e.g., 7 days
    let maxCacheSize: Int64        // e.g., 500 MB

    /// Remove files older than maxCacheAge
    func removeExpiredFiles() throws {
        let contents = try FileManager.default.contentsOfDirectory(
            at: cachesURL,
            includingPropertiesForKeys: [.contentModificationDateKey, .fileSizeKey],
            options: .skipsHiddenFiles
        )

        let cutoff = Date.now.addingTimeInterval(-maxCacheAge)

        for fileURL in contents {
            let values = try fileURL.resourceValues(
                forKeys: [.contentModificationDateKey]
            )
            if let modified = values.contentModificationDate, modified < cutoff {
                try FileManager.default.removeItem(at: fileURL)
            }
        }
    }

    /// Trim cache to maxCacheSize using LRU eviction
    func trimToSize() throws {
        let contents = try FileManager.default.contentsOfDirectory(
            at: cachesURL,
            includingPropertiesForKeys: [.contentModificationDateKey, .fileSizeKey],
            options: .skipsHiddenFiles
        )

        // Sort oldest first
        let sorted = try contents.sorted { a, b in
            let aDate = try a.resourceValues(forKeys: [.contentModificationDateKey])
                .contentModificationDate ?? .distantPast
            let bDate = try b.resourceValues(forKeys: [.contentModificationDateKey])
                .contentModificationDate ?? .distantPast
            return aDate < bDate
        }

        // Calculate total size
        var totalSize: Int64 = 0
        for fileURL in sorted {
            let values = try fileURL.resourceValues(forKeys: [.fileSizeKey])
            totalSize += Int64(values.fileSize ?? 0)
        }

        // Delete oldest files until under budget
        for fileURL in sorted {
            guard totalSize > maxCacheSize else { break }
            let values = try fileURL.resourceValues(forKeys: [.fileSizeKey])
            let fileSize = Int64(values.fileSize ?? 0)
            try FileManager.default.removeItem(at: fileURL)
            totalSize -= fileSize
        }
    }

    /// Full cleanup: expired files first, then trim to size
    func performCleanup() throws {
        try removeExpiredFiles()
        try trimToSize()
    }
}

// Usage
let cleaner = StorageCleaner(
    cachesURL: FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask).first!,
    maxCacheAge: 7 * 24 * 60 * 60,   // 7 days
    maxCacheSize: 500 * 1024 * 1024    // 500 MB
)
try cleaner.performCleanup()
```
