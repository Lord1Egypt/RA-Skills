# CloudKit Patterns

Advanced CloudKit patterns including incremental sync with
CKFetchRecordZoneChangesOperation, sharing with CKShare, record zone
management, CKAsset file storage, batch operations, and CloudKit Dashboard.

## Contents

- [CKFetchRecordZoneChangesOperation (Incremental Sync)](#ckfetchrecordzonechangesoperation-incremental-sync)
- [Server Change Token Management](#server-change-token-management)
- [CKShare and Collaboration](#ckshare-and-collaboration)
- [UICloudSharingController](#uicloudsharingcontroller)
- [Record Zone Management](#record-zone-management)
- [CKAsset File Storage](#ckasset-file-storage)
- [Batch Operations](#batch-operations)
- [Operation Queues and QoS](#operation-queues-and-qos)
- [Encrypted Fields](#encrypted-fields)
- [CloudKit Dashboard](#cloudkit-dashboard)
- [CKFetchDatabaseChangesOperation](#ckfetchdatabasechangesoperation)

## CKFetchRecordZoneChangesOperation (Incremental Sync)

Fetches only records that changed since the last sync. Works with private and
shared databases only. Provide a server change token per zone; use `nil` for
the initial fetch.

```swift
import CloudKit

final class IncrementalSyncManager {
    private let database: CKDatabase
    private var changeTokens: [CKRecordZone.ID: CKServerChangeToken] = [:]
    private let tokenCacheURL: URL

    init(database: CKDatabase, cacheDirectory: URL) {
        self.database = database
        self.tokenCacheURL = cacheDirectory.appendingPathComponent("changeTokens.data")
        loadTokens()
    }

    func fetchChanges(in zoneIDs: [CKRecordZone.ID]) async throws {
        var configs: [CKRecordZone.ID: CKFetchRecordZoneChangesOperation.ZoneConfiguration] = [:]
        for zoneID in zoneIDs {
            let config = CKFetchRecordZoneChangesOperation.ZoneConfiguration()
            config.previousServerChangeToken = changeTokens[zoneID]
            configs[zoneID] = config
        }

        let operation = CKFetchRecordZoneChangesOperation(
            recordZoneIDs: zoneIDs,
            configurationsByRecordZoneID: configs
        )
        operation.fetchAllChanges = true

        // Process changed records
        operation.recordWasChangedBlock = { recordID, result in
            switch result {
            case .success(let record):
                self.processChangedRecord(record)
            case .failure(let error):
                self.handleRecordError(recordID, error: error)
            }
        }

        // Process deleted records
        operation.recordWithIDWasDeletedBlock = { recordID, recordType in
            self.processDeletedRecord(recordID, type: recordType)
        }

        // Update change token as zones complete
        operation.recordZoneFetchResultBlock = { zoneID, result in
            switch result {
            case .success(let (serverChangeToken, _, _)):
                self.changeTokens[zoneID] = serverChangeToken
                self.saveTokens()
            case .failure(let error):
                if let ckError = error as? CKError,
                   ckError.code == .changeTokenExpired {
                    // Clear token and refetch from scratch
                    self.changeTokens[zoneID] = nil
                    self.saveTokens()
                }
            }
        }

        operation.fetchRecordZoneChangesResultBlock = { result in
            if case .failure(let error) = result {
                print("Fetch zone changes failed: \(error)")
            }
        }

        operation.qualityOfService = .utility
        database.add(operation)
    }

    // MARK: - Token Persistence

    private func loadTokens() {
        guard let data = try? Data(contentsOf: tokenCacheURL),
              let tokens = try? NSKeyedUnarchiver.unarchivedObject(
                  ofClasses: [NSDictionary.self, CKRecordZone.ID.self,
                              CKServerChangeToken.self],
                  from: data) as? [CKRecordZone.ID: CKServerChangeToken]
        else { return }
        changeTokens = tokens
    }

    private func saveTokens() {
        guard let data = try? NSKeyedArchiver.archivedData(
            withRootObject: changeTokens, requiringSecureCoding: true)
        else { return }
        try? data.write(to: tokenCacheURL)
    }
}
```

## Server Change Token Management

Change tokens are opaque pointers to a point in a zone's change history. Rules:

- Tokens conform to `NSSecureCoding` -- safe to persist to disk.
- Zone change tokens are NOT interchangeable with database change tokens.
- A `.changeTokenExpired` error means the token is too old; reset to `nil` and
  refetch all changes.
- On `recordZoneFetchResultBlock`, cache the returned token immediately.

```swift
// Persist token alongside zone ID
func cacheToken(_ token: CKServerChangeToken?, for zoneID: CKRecordZone.ID) {
    guard let token else {
        UserDefaults.standard.removeObject(forKey: "token-\(zoneID.zoneName)")
        return
    }
    let data = try? NSKeyedArchiver.archivedData(
        withRootObject: token, requiringSecureCoding: true)
    UserDefaults.standard.set(data, forKey: "token-\(zoneID.zoneName)")
}

func cachedToken(for zoneID: CKRecordZone.ID) -> CKServerChangeToken? {
    guard let data = UserDefaults.standard.data(forKey: "token-\(zoneID.zoneName)")
    else { return nil }
    return try? NSKeyedUnarchiver.unarchivedObject(
        ofClass: CKServerChangeToken.self, from: data)
}
```

## CKShare and Collaboration

CKShare manages shared access to records or entire record zones. Limit: 100
participants per share. Available iOS 10+.

### Hierarchy-Based Sharing

Share a root record and its children (linked via `parent` references).

```swift
import CloudKit

// Create a share for a root record
let rootRecord = CKRecord(recordType: "Album", recordID: albumRecordID)
let share = CKShare(rootRecord: rootRecord)
share.publicPermission = .readOnly

// Customize share appearance
share[CKShare.SystemFieldKey.title] = "Vacation Photos" as CKRecordValue
share[CKShare.SystemFieldKey.shareType] = "com.example.album" as CKRecordValue

// Save share and root record together
let operation = CKModifyRecordsOperation(
    recordsToSave: [rootRecord, share],
    recordIDsToDelete: nil
)
operation.modifyRecordsResultBlock = { result in
    switch result {
    case .success:
        print("Share URL: \(share.url?.absoluteString ?? "nil")")
    case .failure(let error):
        print("Sharing failed: \(error)")
    }
}
privateDB.add(operation)
```

### Zone-Wide Sharing

Share all records in a custom zone.

```swift
let zoneID = CKRecordZone.ID(zoneName: "SharedAlbums")
let share = CKShare(recordZoneID: zoneID)
share.publicPermission = .readWrite
```

### Adding Participants

```swift
// Look up participants by email
let lookupInfo = CKUserIdentity.LookupInfo(emailAddress: "friend@example.com")
let participants = try await container.shareParticipants(
    forEmailAddresses: ["friend@example.com"])

for participant in participants {
    participant.permission = .readWrite
    share.addParticipant(participant)
}

// Save the updated share
try await privateDB.save(share)
```

### Accepting a Share

```swift
// In AppDelegate or SceneDelegate
func userDidAcceptCloudKitShare(with metadata: CKShare.Metadata) {
    let container = CKContainer(identifier: metadata.containerIdentifier)
    Task {
        do {
            try await container.accept([metadata])
            // Fetch shared records from container.sharedCloudDatabase
        } catch {
            print("Accept failed: \(error)")
        }
    }
}
```

**Required**: add `CKSharingSupported = YES` to Info.plist so the system can
launch your app from share URLs.

## UICloudSharingController

Present the system sharing UI (iOS only).

```swift
import UIKit
import CloudKit

func presentSharingUI(for share: CKShare, container: CKContainer,
                      from viewController: UIViewController) {
    let sharingController = UICloudSharingController(share: share, container: container)
    sharingController.delegate = self
    sharingController.availablePermissions = [.allowReadOnly, .allowReadWrite, .allowPrivate]
    viewController.present(sharingController, animated: true)
}

// UICloudSharingControllerDelegate
extension MyClass: UICloudSharingControllerDelegate {
    func cloudSharingController(
        _ csc: UICloudSharingController,
        failedToSaveShareWithError error: Error
    ) {
        print("Save share error: \(error)")
    }

    func itemTitle(for csc: UICloudSharingController) -> String? {
        return "My Shared Album"
    }
}
```

## Record Zone Management

Custom record zones in the private database enable atomic commits, change
tracking with tokens, and record sharing.

```swift
// Create
let zoneID = CKRecordZone.ID(zoneName: "NotesZone", ownerName: CKCurrentUserDefaultName)
let zone = CKRecordZone(zoneID: zoneID)
try await privateDB.save(zone)

// Fetch all zones
let zones = try await privateDB.allRecordZones()

// Delete
try await privateDB.deleteRecordZone(withID: zoneID)
```

**Note**: the default zone does not support custom change tokens or atomic
operations. Always use custom zones for sync.

## CKAsset File Storage

Use CKAsset for files, images, and binary data larger than a few KB. Assets do
not count toward the 1 MB record limit.

```swift
// Save an image as a CKAsset
let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("photo.jpg")
try imageData.write(to: tempURL)

let record = CKRecord(recordType: "Photo")
record["image"] = CKAsset(fileURL: tempURL)
record["caption"] = "Sunset at the beach" as CKRecordValue
try await privateDB.save(record)

// Fetch and read the asset
let fetched = try await privateDB.record(for: record.recordID)
if let asset = fetched["image"] as? CKAsset,
   let fileURL = asset.fileURL {
    let data = try Data(contentsOf: fileURL)
    // Move to app container immediately -- staging area is temporary
    let permanentURL = documentsDir.appendingPathComponent("photo.jpg")
    try FileManager.default.moveItem(at: fileURL, to: permanentURL)
}

// Remove an asset (orphan it)
record["image"] = nil
try await privateDB.save(record)
// CloudKit periodically deletes orphaned assets from the server
```

**Exclude assets from fetch when not needed** using `desiredKeys` on operations
to save bandwidth.

## Batch Operations

Use `CKModifyRecordsOperation` for atomic saves and deletes.

```swift
let recordsToSave: [CKRecord] = [record1, record2, record3]
let idsToDelete: [CKRecord.ID] = [oldRecordID]

let operation = CKModifyRecordsOperation(
    recordsToSave: recordsToSave,
    recordIDsToDelete: idsToDelete
)
operation.savePolicy = .changedKeys       // Only upload modified fields
operation.isAtomic = true                 // All or nothing (custom zones only)

operation.perRecordSaveBlock = { recordID, result in
    switch result {
    case .success(let record): print("Saved: \(recordID)")
    case .failure(let error): print("Failed: \(recordID) \(error)")
    }
}

operation.perRecordDeleteBlock = { recordID, result in
    switch result {
    case .success: print("Deleted: \(recordID)")
    case .failure(let error): print("Delete failed: \(recordID) \(error)")
    }
}

operation.modifyRecordsResultBlock = { result in
    if case .failure(let error) = result {
        print("Batch failed: \(error)")
    }
}

// CloudKit limits: 400 records per operation
operation.qualityOfService = .userInitiated
privateDB.add(operation)
```

**Max 400 records per operation.** For larger batches, split into chunks.

## Operation Queues and QoS

Set appropriate quality of service:

| Scenario | QoS |
|----------|-----|
| User triggered action | `.userInitiated` |
| Background sync | `.utility` |
| Pre-fetch / maintenance | `.background` |

```swift
// Use operation groups for related operations
let group = CKOperationGroup()
group.expectedSendSize = .kilobytes
group.expectedReceiveSize = .megabytes

let config = CKOperation.Configuration()
config.qualityOfService = .utility
config.group = group

let operation = CKQueryOperation(query: query)
operation.configuration = config
database.add(operation)
```

## Encrypted Fields

Use `encryptedValues` (iOS 15+) for sensitive private or shared data that does
not need query or sort indexes. CloudKit can encrypt only new schema fields;
you cannot convert an existing field to encrypted storage, and encrypted values
are unavailable for public database records. `CKAsset` data is encrypted by
default, while `CKRecord.Reference` is not encrypted because CloudKit needs it
for server-side relationship handling.

```swift
let record = CKRecord(recordType: "HealthEntry")
record.encryptedValues["heartRate"] = 72 as CKRecordValue
record.encryptedValues["notes"] = "Resting" as CKRecordValue
// Non-sensitive fields remain in plain text
record["date"] = Date() as CKRecordValue

try await privateDB.save(record)

// Read encrypted values
let fetched = try await privateDB.record(for: record.recordID)
let heartRate = fetched.encryptedValues["heartRate"] as? Int
```

## CloudKit Dashboard

Access at [iCloud Dashboard](https://icloud.developer.apple.com/dashboard).
Key capabilities:

- **Schema**: view/edit record types, fields, indexes. Add indexes only for
  queried fields in production.
- **Records**: browse, create, edit, delete records in any database.
- **Subscriptions**: view active subscriptions.
- **Logs**: monitor API calls, errors, and latency.
- **Telemetry**: track request counts, error rates, latency percentiles.
- **Environment toggle**: switch between Development and Production. Simulator
  only works with Development.
- **Deploy to Production**: migrate schema changes from dev to prod. Production
  does not allow adding new record types or fields programmatically.

## CKFetchDatabaseChangesOperation

Discover which zones changed in a database. Use with shared database where you
do not know zone IDs in advance.

```swift
var dbChangeToken: CKServerChangeToken? = loadDatabaseChangeToken()

let operation = CKFetchDatabaseChangesOperation(
    previousServerChangeToken: dbChangeToken
)
operation.fetchAllChanges = true

var changedZoneIDs: [CKRecordZone.ID] = []
var deletedZoneIDs: [CKRecordZone.ID] = []

operation.recordZoneWithIDChangedBlock = { zoneID in
    changedZoneIDs.append(zoneID)
}

operation.recordZoneWithIDWasDeletedBlock = { zoneID in
    deletedZoneIDs.append(zoneID)
}

operation.fetchDatabaseChangesResultBlock = { result in
    switch result {
    case .success(let (token, _)):
        dbChangeToken = token
        saveDatabaseChangeToken(token)
        // Now fetch zone changes for changedZoneIDs
    case .failure(let error):
        if let ckError = error as? CKError,
           ckError.code == .changeTokenExpired {
            dbChangeToken = nil
            // Refetch from scratch
        }
    }
}

operation.qualityOfService = .utility
sharedDB.add(operation)
```
