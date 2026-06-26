# MetricKit Extended Patterns

Overflow reference for the `metrickit` skill. Contains deeper payload analysis, export patterns, custom signpost metrics, and extended launch measurement.

## Contents

- [Call Stack Trees](#call-stack-trees)
- [Custom Signpost Metrics](#custom-signpost-metrics)
- [Exporting and Uploading Payloads](#exporting-and-uploading-payloads)
- [Past Payloads](#past-payloads)
- [Extended Launch Measurement](#extended-launch-measurement)
- [Xcode Organizer Integration](#xcode-organizer-integration)

## Call Stack Trees

`MXCallStackTree` is attached to each diagnostic (crash, hang, CPU exception,
disk write, app launch). Use `jsonRepresentation()` to extract and symbolicate.

```swift
func handleCrash(_ crash: MXCrashDiagnostic) {
    let tree = crash.callStackTree
    let treeJSON = tree.jsonRepresentation()

    let exceptionType = crash.exceptionType
    let signal = crash.signal
    let reason = crash.terminationReason

    uploadDiagnostic(
        type: "crash",
        exceptionType: exceptionType,
        signal: signal,
        reason: reason,
        callStack: treeJSON
    )
}

func handleHang(_ hang: MXHangDiagnostic) {
    let tree = hang.callStackTree
    let duration = hang.hangDuration  // Measurement<UnitDuration>
    uploadDiagnostic(type: "hang", duration: duration, callStack: tree.jsonRepresentation())
}
```

The JSON structure contains an array of call stack frames with binary name,
offset, and address. Symbolicate using `atos` or upload dSYMs to your
analytics service.

**Availability**: `MXCallStackTree` — iOS 14.0+, iPadOS 14.0+,
Mac Catalyst 14.0+, macOS 12.0+, visionOS 1.0+

## Custom Signpost Metrics

Use `mxSignpost` with a MetricKit log handle to capture custom performance
intervals. These appear in the daily `MXMetricPayload` under `signpostMetrics`.

### Creating a Log Handle

```swift
let metricLog = MXMetricManager.makeLogHandle(category: "Networking")
```

### Emitting Signposts

```swift
import os

func fetchData() async throws -> Data {
    mxSignpost(.begin, log: metricLog, name: "DataFetch")
    let data = try await URLSession.shared.data(from: url).0
    mxSignpost(.end, log: metricLog, name: "DataFetch")

    return data
}
```

For MetricKit custom metrics, create the log with
`MXMetricManager.makeLogHandle(category:)` and leave the `mxSignpost` overload's
advanced `dso`, `signpostID`, and `format` parameters at their documented
defaults.

### Reading Custom Metrics from Payload

```swift
if let signposts = payload.signpostMetrics {
    for metric in signposts {
        let name = metric.signpostName       // "DataFetch"
        let category = metric.signpostCategory // "Networking"
        let count = metric.totalCount
        if let intervalData = metric.signpostIntervalData {
            let avgMemory = intervalData.averageMemory
            let cumulativeCPUTime = intervalData.cumulativeCPUTime
        }
    }
}
```

> The system limits the number of custom signpost metrics per log to reduce
> on-device overhead. Reserve custom metrics for critical code paths.

## Exporting and Uploading Payloads

Both payload types conform to `NSSecureCoding` and provide
`jsonRepresentation()` for easy serialization.

```swift
func persistPayload(_ jsonData: Data, from: Date? = nil, to: Date? = nil) {
    let fileName = "metrics_\(ISO8601DateFormatter().string(from: Date())).json"
    let url = FileManager.default.temporaryDirectory.appending(path: fileName)
    try? jsonData.write(to: url)
}

func uploadPayloads(_ jsonData: Data) {
    Task.detached(priority: .utility) {
        var request = URLRequest(url: URL(string: "https://api.example.com/metrics")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        _ = try? await URLSession.shared.data(for: request)
    }
}
```

## Past Payloads

If the subscriber was not registered when payloads arrived, retrieve them
using `pastPayloads` and `pastDiagnosticPayloads`. These return reports
generated since the last allocation of the shared manager instance.

```swift
let pastMetrics = MXMetricManager.shared.pastPayloads
let pastDiags = MXMetricManager.shared.pastDiagnosticPayloads
```

## Extended Launch Measurement

Track post-first-draw setup work (loading databases, restoring state) as part
of the launch metric using extended launch measurement on iOS 16+, iPadOS 16+,
Mac Catalyst 16+, macOS 13+, and visionOS 1+.

```swift
let taskID = MXLaunchTaskID("com.example.app.loadDatabase")

try MXMetricManager.extendLaunchMeasurement(forTaskID: taskID)
defer { try? MXMetricManager.finishExtendedLaunchMeasurement(forTaskID: taskID) }

restoreCachedState()
connectInitialSceneData()
```

Extended launch times appear under `histogrammedExtendedLaunch` in
`MXAppLaunchMetric`.

Use these throwing type methods on the main thread. Start the first task before
or during state restoration, or before the first scene becomes active. The
system supports up to 16 tasks; task windows need to overlap, and extended
launch measurement ends when all running tasks finish.

## Xcode Organizer Integration

Xcode Organizer shows the same MetricKit data aggregated across all users
who have opted in to share diagnostics. Use Organizer for trend analysis:

- **Metrics tab**: Battery, performance, and disk-write metrics over time
- **Regressions tab**: Automatic detection of metric regressions per version
- **Crashes tab**: Crash logs with symbolicated stack traces

MetricKit on-device collection complements Organizer by letting you route
raw data to your own backend for custom dashboards, alerting, and filtering
by user cohort.

## Apple Documentation Links

- [MetricKit framework](https://sosumi.ai/documentation/metrickit)
- [MXMetricManager](https://sosumi.ai/documentation/metrickit/mxmetricmanager)
- [MXMetricManagerSubscriber](https://sosumi.ai/documentation/metrickit/mxmetricmanagersubscriber)
- [MXCallStackTree](https://sosumi.ai/documentation/metrickit/mxcallstacktree)
- [MXSignpostMetric](https://sosumi.ai/documentation/metrickit/mxsignpostmetric)
- [MXAppLaunchMetric](https://sosumi.ai/documentation/metrickit/mxapplaunchmetric)
- [MXCrashDiagnostic](https://sosumi.ai/documentation/metrickit/mxcrashdiagnostic)
- [Analyzing the performance of your shipping app](https://sosumi.ai/documentation/xcode/analyzing-the-performance-of-your-shipping-app)
