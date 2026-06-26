# CoreMotion Extended Patterns

Overflow reference for the `core-motion` skill. Contains advanced patterns that
exceed the main skill file's scope.

## Contents

- [SwiftUI Integration with `@Observable`](#swiftui-integration-with-observable)
- [CMBatchedSensorManager (High-Frequency)](#cmbatchedsensormanager-high-frequency)
- [Headphone Motion](#headphone-motion)
- [Pedometer SwiftUI View](#pedometer-swiftui-view)
- [Activity-Based Navigation](#activity-based-navigation)
- [Water Submersion (watchOS)](#water-submersion-watchos)

## SwiftUI Integration with `@Observable`

### Motion Manager Service

```swift
import CoreMotion
import SwiftUI

@Observable
@MainActor
final class MotionService {
    static let shared = MotionService()

    private let manager = CMMotionManager()

    var pitch: Double = 0
    var roll: Double = 0
    var yaw: Double = 0
    var userAcceleration: CMAcceleration = CMAcceleration()
    var isActive = false

    func startDeviceMotion(interval: TimeInterval = 1.0 / 60.0) {
        guard manager.isDeviceMotionAvailable, !isActive else { return }

        manager.deviceMotionUpdateInterval = interval
        manager.startDeviceMotionUpdates(
            using: .xArbitraryZVertical,
            to: .main
        ) { [weak self] motion, error in
            guard let self, let motion else { return }
            self.pitch = motion.attitude.pitch
            self.roll = motion.attitude.roll
            self.yaw = motion.attitude.yaw
            self.userAcceleration = motion.userAcceleration
        }
        isActive = true
    }

    func stop() {
        manager.stopDeviceMotionUpdates()
        isActive = false
    }
}
```

### SwiftUI View Using Motion

```swift
struct TiltView: View {
    @State private var motionService = MotionService.shared

    var body: some View {
        VStack {
            Circle()
                .fill(.blue)
                .frame(width: 60, height: 60)
                .offset(
                    x: motionService.roll * 100,
                    y: motionService.pitch * 100
                )

            Text("Roll: \(motionService.roll, format: .number.precision(.fractionLength(2)))")
            Text("Pitch: \(motionService.pitch, format: .number.precision(.fractionLength(2)))")
        }
        .onAppear { motionService.startDeviceMotion() }
        .onDisappear { motionService.stop() }
    }
}
```

### Level Indicator

```swift
struct LevelIndicator: View {
    @State private var motionService = MotionService.shared

    private var isLevel: Bool {
        abs(motionService.pitch) < 0.05 && abs(motionService.roll) < 0.05
    }

    var body: some View {
        ZStack {
            Circle()
                .stroke(isLevel ? .green : .gray, lineWidth: 3)
                .frame(width: 200, height: 200)

            Circle()
                .fill(isLevel ? .green : .red)
                .frame(width: 20, height: 20)
                .offset(
                    x: motionService.roll * 100,
                    y: motionService.pitch * -100
                )
        }
        .onAppear { motionService.startDeviceMotion(interval: 1.0 / 30.0) }
        .onDisappear { motionService.stop() }
    }
}
```

## CMBatchedSensorManager (High-Frequency)

`CMBatchedSensorManager` delivers batches of high-frequency accelerometer and
device-motion data for workout-style motion analysis, such as golf swings or bat
swings. The async update sequences are watchOS 10+ APIs; check availability and
authorization before starting updates.

### AsyncSequence Pattern

```swift
import CoreMotion

@Observable
@MainActor
final class BatchedMotionService {
    private let batchedManager = CMBatchedSensorManager()
    private var updateTask: Task<Void, Never>?

    var latestAcceleration: CMAcceleration?

    func startBatchedAccelerometer() {
        let authorization = CMBatchedSensorManager.authorizationStatus
        guard CMBatchedSensorManager.isAccelerometerSupported,
              authorization != .denied,
              authorization != .restricted else { return }

        updateTask = Task {
            for await batch in batchedManager.accelerometerUpdates() {
                guard !Task.isCancelled else { break }
                // Process entire batch
                for sample in batch {
                    // sample.acceleration, sample.timestamp
                }
                // Update UI with most recent
                if let latest = batch.last {
                    latestAcceleration = latest.acceleration
                }
            }
        }
    }

    func stop() {
        updateTask?.cancel()
        updateTask = nil
        batchedManager.stopAccelerometerUpdates()
    }
}
```

### Reading Frequency

```swift
let batchedManager = CMBatchedSensorManager()

// Start updates, then read the frequency the device reports.
batchedManager.startAccelerometerUpdates()
let reportedHz = batchedManager.accelerometerDataFrequency
```

`accelerometerDataFrequency` and `deviceMotionDataFrequency` are read-only. Do
not assign them; use the reported values to size buffers, throttle UI updates, or
downsample processed results.

## Headphone Motion

Track head motion using AirPods Pro / AirPods Max via `CMHeadphoneMotionManager`.
On iOS and macOS, include `NSMotionUsageDescription`. Use connection-status
updates when the app needs connect/disconnect events outside an active motion
session.

```swift
import CoreMotion

@Observable
@MainActor
final class HeadphoneMotionService: NSObject {
    private let headphoneManager = CMHeadphoneMotionManager()

    var isConnected = false
    var headPitch: Double = 0
    var headYaw: Double = 0

    func start() {
        guard headphoneManager.isDeviceMotionAvailable else { return }

        headphoneManager.delegate = self
        headphoneManager.startConnectionStatusUpdates()
        headphoneManager.startDeviceMotionUpdates(to: .main) { [weak self] motion, error in
            guard let self, let motion else { return }
            self.headPitch = motion.attitude.pitch
            self.headYaw = motion.attitude.yaw
        }
    }

    func stop() {
        headphoneManager.stopDeviceMotionUpdates()
        headphoneManager.stopConnectionStatusUpdates()
    }
}

extension HeadphoneMotionService: CMHeadphoneMotionManagerDelegate {
    nonisolated func headphoneMotionManagerDidConnect(
        _ manager: CMHeadphoneMotionManager
    ) {
        Task { @MainActor in isConnected = true }
    }

    nonisolated func headphoneMotionManagerDidDisconnect(
        _ manager: CMHeadphoneMotionManager
    ) {
        Task { @MainActor in isConnected = false }
    }
}
```

## Pedometer SwiftUI View

### Step Counter Dashboard

```swift
import CoreMotion
import SwiftUI

@Observable
@MainActor
final class PedometerService {
    private let pedometer = CMPedometer()

    var todaySteps: Int = 0
    var todayDistance: Double = 0
    var floorsAscended: Int = 0

    func fetchToday() {
        guard CMPedometer.isStepCountingAvailable() else { return }

        let startOfDay = Calendar.current.startOfDay(for: Date())

        pedometer.queryPedometerData(from: startOfDay, to: Date()) { [weak self] data, error in
            guard let self, let data else { return }
            Task { @MainActor in
                self.todaySteps = data.numberOfSteps.intValue
                self.todayDistance = data.distance?.doubleValue ?? 0
                self.floorsAscended = data.floorsAscended?.intValue ?? 0
            }
        }
    }

    func startLiveUpdates() {
        guard CMPedometer.isStepCountingAvailable() else { return }

        let startOfDay = Calendar.current.startOfDay(for: Date())

        pedometer.startUpdates(from: startOfDay) { [weak self] data, error in
            guard let self, let data else { return }
            Task { @MainActor in
                self.todaySteps = data.numberOfSteps.intValue
                self.todayDistance = data.distance?.doubleValue ?? 0
                self.floorsAscended = data.floorsAscended?.intValue ?? 0
            }
        }
    }

    func stopLiveUpdates() {
        pedometer.stopUpdates()
    }
}
```

### SwiftUI Dashboard View

```swift
struct StepDashboard: View {
    @State private var pedometerService = PedometerService()

    var body: some View {
        List {
            Section("Today") {
                LabeledContent("Steps") {
                    Text("\(pedometerService.todaySteps)")
                }
                LabeledContent("Distance") {
                    Text(
                        Measurement(value: pedometerService.todayDistance, unit: UnitLength.meters),
                        format: .measurement(width: .abbreviated)
                    )
                }
                if CMPedometer.isFloorCountingAvailable() {
                    LabeledContent("Floors Climbed") {
                        Text("\(pedometerService.floorsAscended)")
                    }
                }
            }
        }
        .onAppear { pedometerService.startLiveUpdates() }
        .onDisappear { pedometerService.stopLiveUpdates() }
    }
}
```

## Activity-Based Navigation

Switch between driving and walking modes automatically:

```swift
import CoreMotion

@Observable
@MainActor
final class NavigationModeService {
    private let activityManager = CMMotionActivityManager()

    enum Mode: String {
        case walking, driving, cycling, unknown
    }

    var currentMode: Mode = .unknown

    func startMonitoring() {
        guard CMMotionActivityManager.isActivityAvailable() else { return }

        activityManager.startActivityUpdates(to: .main) { [weak self] activity in
            guard let self, let activity,
                  activity.confidence != .low else { return }

            Task { @MainActor in
                if activity.automotive {
                    self.currentMode = .driving
                } else if activity.cycling {
                    self.currentMode = .cycling
                } else if activity.walking || activity.running {
                    self.currentMode = .walking
                } else if activity.stationary {
                    // Keep previous mode when stationary (e.g., at a stoplight)
                }
            }
        }
    }

    func stopMonitoring() {
        activityManager.stopActivityUpdates()
    }
}
```

## Water Submersion (watchOS)

Track water depth and temperature for dive apps on supported Apple Watch
hardware. Use `waterSubmersionAvailable` rather than hard-coding model checks:
Apple Watch Ultra supports submersion data, and Apple Watch Series 10 supports
the Shallow Depth and Pressure capability.

Setup checklist:

- Add `NSMotionUsageDescription`.
- Add the Shallow Depth and Pressure capability for dives up to 6 meters, or
  apply for the full Submerged Depth and Pressure entitlement for dives up to
  40 meters.
- Add `WKBackgroundModes` with `underwater-depth` so the app can remain
  frontmost and eligible for dive autolaunch.
- Check availability before instantiating `CMWaterSubmersionManager`.

```swift
import CoreMotion

@Observable
@MainActor
final class DiveService: NSObject {
    private var submersionManager: CMWaterSubmersionManager?

    var isSubmerged = false
    var currentDepth: Double?
    var waterTemperature: Double?

    func start() {
        guard CMWaterSubmersionManager.waterSubmersionAvailable else { return }
        let manager = CMWaterSubmersionManager()
        manager.delegate = self
        submersionManager = manager
    }
}

extension DiveService: CMWaterSubmersionManagerDelegate {
    nonisolated func manager(
        _ manager: CMWaterSubmersionManager,
        didUpdate event: CMWaterSubmersionEvent
    ) {
        Task { @MainActor in
            isSubmerged = event.state == .submerged
        }
    }

    nonisolated func manager(
        _ manager: CMWaterSubmersionManager,
        didUpdate measurement: CMWaterSubmersionMeasurement
    ) {
        Task { @MainActor in
            currentDepth = measurement.depth?.value
        }
    }

    nonisolated func manager(
        _ manager: CMWaterSubmersionManager,
        didUpdate temperature: CMWaterTemperature
    ) {
        Task { @MainActor in
            waterTemperature = temperature.temperature.value
        }
    }

    nonisolated func manager(
        _ manager: CMWaterSubmersionManager,
        errorOccurred error: any Error
    ) {
        print("Submersion error: \(error)")
    }
}
```

**Important:** `CMWaterSubmersionManager` requires the
Shallow Depth and Pressure capability or the full Submerged Depth and Pressure
entitlement. If the app lacks the entitlement, the delegate receives
`CMError.notEntitled` and no submersion data.
