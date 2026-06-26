# Background Task Patterns — Extended Reference

Overflow reference for the background-processing skill. Contains debugging tips,
advanced background URLSession patterns, background push best practices, and
SwiftUI integration patterns.

## Contents

- [Debugging Background Tasks](#debugging-background-tasks)
- [Advanced BGProcessingTask Patterns](#advanced-bgprocessingtask-patterns)
- [Background URLSession — Extended Patterns](#background-urlsession--extended-patterns)
- [Background Push — Extended Patterns](#background-push--extended-patterns)
- [SwiftUI BackgroundTask Modifier](#swiftui-backgroundtask-modifier)
- [BGContinuedProcessingTask — Extended Patterns](#bgcontinuedprocessingtask--extended-patterns)

## Debugging Background Tasks

### Simulating Task Launches in Xcode

Use the LLDB console to trigger tasks instantly during development. The app must
be running on a device in the debugger with a breakpoint hit or paused.

These are Apple-documented private functions for development only. Do not
include references to them in App Store-submitted code.

```swift
e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateLaunchForTaskWithIdentifier:@"com.example.app.refresh"]
```

For processing tasks:

```swift
e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateLaunchForTaskWithIdentifier:@"com.example.app.db-cleanup"]
```

To simulate early termination (expiration):

```swift
e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateExpirationForTaskWithIdentifier:@"com.example.app.refresh"]
```

### Verifying Pending Tasks

Check what tasks are currently scheduled:

```swift
BGTaskScheduler.shared.getPendingTaskRequests { requests in
    for request in requests {
        print("Pending: \(request.identifier), earliest: \(String(describing: request.earliestBeginDate))")
    }
}
```

### Common Debugging Issues

| Symptom | Cause | Fix |
|---|---|---|
| Task never fires | Identifier not in Info.plist | Add to `BGTaskSchedulerPermittedIdentifiers` |
| Task never fires | Background modes not enabled | Enable `fetch` and/or `processing` in capabilities |
| Task never fires on device | Background App Refresh disabled or Low Power Mode active | Check `UIApplication.shared.backgroundRefreshStatus`; Low Power Mode reduces background runtime |
| `.notPermitted` error | Identifier mismatch | Verify exact string match between code and plist |
| `.unavailable` error | Running in extension | BGTaskScheduler not available in app extensions |
| `.tooManyPendingTaskRequests` | More than 1 refresh task or 10 processing tasks scheduled in total | Cancel old requests before submitting new ones |

Submitting an unexecuted task request with the same identifier replaces the
previous request.

## Advanced BGProcessingTask Patterns

### Conditional Requirements

Use `requiresExternalPower` and `requiresNetworkConnectivity` to ensure the
system only launches your task when conditions are met:

```swift
func scheduleSyncTask() {
    let request = BGProcessingTaskRequest(
        identifier: "com.example.app.full-sync"
    )
    // Only run when charging and connected to network
    request.requiresExternalPower = true
    request.requiresNetworkConnectivity = true
    // Don't run before 2 AM
    var components = DateComponents()
    components.hour = 2
    if let twoAM = Calendar.current.nextDate(
        after: Date(),
        matching: components,
        matchingPolicy: .nextTime
    ) {
        request.earliestBeginDate = twoAM
    }

    do {
        try BGTaskScheduler.shared.submit(request)
    } catch {
        print("Failed to schedule sync: \(error)")
    }
}
```

### Incremental Work with Checkpointing

Design tasks to save progress so they can resume if terminated:

```swift
func handleMigration(task: BGProcessingTask) {
    let work = Task {
        let lastProcessed = UserDefaults.standard.integer(
            forKey: "migrationLastIndex"
        )
        let items = try await loadItems()

        for (index, item) in items.dropFirst(lastProcessed).enumerated() {
            try Task.checkCancellation()
            try await migrate(item)
            // Checkpoint progress
            UserDefaults.standard.set(
                lastProcessed + index + 1,
                forKey: "migrationLastIndex"
            )
        }

        task.setTaskCompleted(success: true)
    }

    task.expirationHandler = {
        work.cancel()
        // Progress is saved -- next launch picks up where we left off
        task.setTaskCompleted(success: false)
    }
}
```

## Background URLSession — Extended Patterns

### Configuration Best Practices

```swift
let config = URLSessionConfiguration.background(
    withIdentifier: "com.example.app.background-transfer"
)

// isDiscretionary = true: system picks optimal time (WiFi, power)
// Use for non-urgent transfers
config.isDiscretionary = true

// sessionSendsLaunchEvents = true: app relaunched when transfer completes
config.sessionSendsLaunchEvents = true

// Set reasonable timeouts
config.timeoutIntervalForResource = 60 * 60 * 24 * 7  // 7 days

// Allow cellular (default is true)
config.allowsCellularAccess = true
```

### Upload with Background Session

```swift
func uploadFile(at fileURL: URL) {
    var request = URLRequest(url: URL(string: "https://api.example.com/upload")!)
    request.httpMethod = "POST"
    let uploadTask = session.uploadTask(with: request, fromFile: fileURL)
    uploadTask.resume()
}
```

**Important:** Background sessions only support `uploadTask(with:fromFile:)` and
`downloadTask(with:)`. Data tasks, `uploadTask(with:from:)` (Data), and
closure/async-based tasks are **not** supported.

### Handling App Relaunch

When the system completes a background transfer and your app is not running, it
relaunches the app. You must:

1. Store the completion handler from
   `application(_:handleEventsForBackgroundURLSession:completionHandler:)`
2. Recreate the `URLSession` with the **same identifier**
3. Call the stored completion handler in `urlSessionDidFinishEvents`

```swift
// AppDelegate
func application(
    _ application: UIApplication,
    handleEventsForBackgroundURLSession identifier: String,
    completionHandler: @escaping () -> Void
) {
    // Recreating session with the same identifier reconnects to the transfer
    _ = DownloadManager.shared.session  // trigger lazy init
    DownloadManager.shared.completionHandler = completionHandler
}

// In your URLSessionDelegate
func urlSessionDidFinishEvents(forBackgroundURLSession session: URLSession) {
    Task { @MainActor in
        self.completionHandler?()
        self.completionHandler = nil
    }
}
```

### Handling Download Errors and Retries

```swift
func urlSession(
    _ session: URLSession,
    task: URLSessionTask,
    didCompleteWithError error: (any Error)?
) {
    guard let error else { return }  // Success handled in didFinishDownloadingTo

    let nsError = error as NSError

    // Check if download can be resumed
    if let resumeData = nsError.userInfo[NSURLSessionDownloadTaskResumeData] as? Data {
        // Store resumeData and retry later
        let downloadTask = session.downloadTask(withResumeData: resumeData)
        downloadTask.resume()
        return
    }

    // Non-resumable error -- retry from scratch or notify user
    if nsError.code == NSURLErrorNetworkConnectionLost {
        // Re-enqueue the download
        if let url = task.originalRequest?.url {
            let newTask = session.downloadTask(with: url)
            newTask.resume()
        }
    }
}
```

### Progress Tracking

```swift
func urlSession(
    _ session: URLSession,
    downloadTask: URLSessionDownloadTask,
    didWriteData bytesWritten: Int64,
    totalBytesWritten: Int64,
    totalBytesExpectedToWrite: Int64
) {
    let progress = Double(totalBytesWritten) / Double(totalBytesExpectedToWrite)
    // Update UI on main actor if app is in foreground
    Task { @MainActor in
        DownloadProgressStore.shared.update(
            taskID: downloadTask.taskIdentifier,
            progress: progress
        )
    }
}
```

## Background Push — Extended Patterns

### Push Payload Requirements

The `content-available: 1` flag is required. You can include custom data:

```json
{
    "aps": {
        "content-available": 1
    },
    "type": "new-message",
    "conversation-id": "abc-123"
}
```

**Do not** include `alert`, `badge`, or `sound` if you only want a silent push.
Including visual notification keys changes the push behavior.

Send background notification requests with APNs headers:

```http
apns-push-type: background
apns-priority: 5
```

### Rate Limiting

Apple throttles background push delivery. Guidelines:

- Delivery is low priority and not guaranteed.
- Do not send more than two or three background notifications per hour.
- The system may hold only the newest background notification and discard older
  held notifications.
- If the user force-quits the app, background pushes stop until the next manual
  launch.
- Use `apns-priority: 5`; high-priority pushes are for user-visible
  notifications, not silent refresh.

### Handling Push with Async Work

```swift
func application(
    _ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any],
    fetchCompletionHandler completionHandler:
        @escaping (UIBackgroundFetchResult) -> Void
) {
    guard let type = userInfo["type"] as? String else {
        completionHandler(.noData)
        return
    }

    Task {
        do {
            switch type {
            case "new-message":
                let conversationID = userInfo["conversation-id"] as? String
                let fetched = try await MessageService.shared
                    .fetchMessages(for: conversationID)
                completionHandler(fetched ? .newData : .noData)

            case "config-update":
                try await ConfigService.shared.refreshConfig()
                completionHandler(.newData)

            default:
                completionHandler(.noData)
            }
        } catch {
            completionHandler(.failed)
        }
    }
}
```

**Important:** You have approximately 30 seconds to call `completionHandler`.
Failure to do so causes the system to penalize your app's background push
budget.

## SwiftUI BackgroundTask Modifier

SwiftUI provides a `.backgroundTask` modifier as an alternative to manual
`BGTaskScheduler` registration:

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .backgroundTask(.appRefresh("com.example.app.refresh")) {
                await refreshFeed()
                // Schedule the next one
                scheduleAppRefresh()
            }
    }
}
```

This is a SwiftUI handler for matching background tasks. You still need the
Info.plist identifiers, background modes, scheduling, and cancellation-safe work
patterns.

## BGContinuedProcessingTask — Extended Patterns

### Checking Supported Resources

Before requesting GPU or other resources, verify the device supports them and
enable Background GPU Access
(`com.apple.developer.background-tasks.continued-processing.gpu`) for GPU work:

```swift
let supported = BGTaskScheduler.supportedResources
if supported.contains(.gpu) {
    request.requiredResources = .gpu
}
```

### Submission Strategies

`BGContinuedProcessingTaskRequest.SubmissionStrategy` controls behavior when the
system cannot run the task immediately:

| Strategy | Behavior |
|---|---|
| `.queue` | Task is queued and starts as soon as possible |
| `.fail` | Submission fails immediately if can't run now |

Use `.fail` when the work is only relevant in the current moment (e.g., a user
is waiting). Use `.queue` for work that can start whenever the system allows.

### Cancellation by the User

The system shows a Live Activity for continued processing tasks. The user can
cancel the task from there. Handle this in your expiration handler:

```swift
task.expirationHandler = {
    // Clean up partial work
    cleanupPartialExport()
    task.setTaskCompleted(success: false)
}
```

### Progress Reporting

The system uses your `Progress` object to decide termination priority. Tasks
with no progress updates are terminated first under resource pressure:

```swift
// Report fine-grained progress
let progress = task.progress
progress.totalUnitCount = Int64(totalItems)

for (index, item) in items.enumerated() {
    try Task.checkCancellation()
    await process(item)
    progress.completedUnitCount = Int64(index + 1)
}
```
