# AccessorySetupKit Patterns

Extended patterns and recipes for AccessorySetupKit. Covers custom filtering,
multiple accessory types, removal handling, accessory images, batch setup,
error handling, authorization management, and picker display settings.

## Contents

- [Custom Filtering](#custom-filtering)
- [Multiple Accessory Types](#multiple-accessory-types)
- [Removal and Lifecycle Management](#removal-and-lifecycle-management)
- [Accessory Images](#accessory-images)
- [Picker Display Settings](#picker-display-settings)
- [Authorization Management](#authorization-management)
- [Error Handling](#error-handling)
- [Full Manager Pattern](#full-manager-pattern)
- [SwiftUI Integration](#swiftui-integration)

## Custom Filtering

The default picker shows all matching accessories automatically. For apps that
need to inspect over-the-air data before showing an accessory (e.g., verifying
authenticity, checking pairing mode), use custom filtering with
`ASPickerDisplaySettings` on iOS 26+. Showing filtered discovered accessories
requires `ASDiscoveredAccessory`, `ASDiscoveredDisplayItem`, `updatePicker`, and
`finishPickerDiscovery` on iOS 26.1+.

### Enabling Filtered Discovery

```swift
import AccessorySetupKit

let settings = ASPickerDisplaySettings.default
settings.options.insert(.filterDiscoveryResults)
settings.discoveryTimeout = .unbounded  // No time limit for filtering
session.pickerDisplaySettings = settings
```

### Processing Discovered Accessories

When filtering is enabled, the session delivers `.accessoryDiscovered` events
instead of automatically populating the picker. Inspect each accessory and
decide whether to display it:

```swift
session.activate(on: .main) { [weak self] event in
    guard let self else { return }

    switch event.eventType {
    case .accessoryDiscovered:
        guard let discovered = event.accessory as? ASDiscoveredAccessory else { return }
        processDiscoveredAccessory(discovered)
    case .accessoryAdded:
        guard let accessory = event.accessory else { return }
        handleAccessoryAdded(accessory)
    @unknown default:
        break
    }
}
```

### Validating and Displaying Accessories

Use advertisement data and RSSI to validate accessories before adding them to
the picker:

```swift
func processDiscoveredAccessory(_ discovered: ASDiscoveredAccessory) {
    // Check RSSI for proximity
    guard let rssi = discovered.bluetoothRSSI, rssi > -60 else { return }

    // Inspect manufacturer data for authenticity
    guard let advertisementData = discovered.bluetoothAdvertisementData,
          isAuthentic(advertisementData) else { return }

    // Create a customized display item for this specific accessory
    let displayItem = ASDiscoveredDisplayItem(
        name: extractProductName(from: advertisementData),
        productImage: loadImageForModel(advertisementData),
        accessory: discovered
    )

    session.updatePicker(showing: [displayItem]) { error in
        if let error {
            print("Failed to update picker: \(error)")
        }
    }
}

private func isAuthentic(_ advertisementData: [AnyHashable: Any]?) -> Bool {
    guard let data = advertisementData,
          let manufacturerData = data["kCBAdvDataManufacturerData"] as? Data else {
        return false
    }
    // Verify manufacturer-specific authentication bytes
    return manufacturerData.count >= 4
}
```

### Finishing Discovery Early

If the app completes filtering before the timeout, or if no accessories pass
validation, end discovery explicitly:

```swift
func finishFilteredDiscovery() {
    session.finishPickerDiscovery { error in
        if let error {
            print("Finish discovery error: \(error)")
        }
        // If no items were added, the picker shows a timeout message
    }
}
```

### Retry After Timeout

If the expected accessory was not found, wait for picker dismissal and try
again. Suggest the user verify the accessory is powered on and nearby:

```swift
case .pickerDidDismiss:
    if !accessoryFound {
        // Prompt user to check that the accessory is powered on
        showRetryPrompt()
    }
```

## Multiple Accessory Types

Apps supporting multiple accessory models create separate display items with
distinct descriptors for each model. The picker shows all matching devices in
a scrollable carousel.

### Distinct Models with Different Service UUIDs

```swift
func showMultiModelPicker() {
    let sensorDescriptor = ASDiscoveryDescriptor()
    sensorDescriptor.bluetoothServiceUUID = CBUUID(string: "AAAA1111-...")
    sensorDescriptor.bluetoothNameSubstring = "TempSensor"

    let hubDescriptor = ASDiscoveryDescriptor()
    hubDescriptor.bluetoothServiceUUID = CBUUID(string: "BBBB2222-...")
    hubDescriptor.bluetoothNameSubstring = "SmartHub"

    let sensorItem = ASPickerDisplayItem(
        name: "Temperature Sensor",
        productImage: UIImage(named: "sensor-image")!,
        descriptor: sensorDescriptor
    )

    let hubItem = ASPickerDisplayItem(
        name: "Smart Hub",
        productImage: UIImage(named: "hub-image")!,
        descriptor: hubDescriptor
    )

    session.showPicker(for: [sensorItem, hubItem]) { error in
        if let error {
            print("Picker error: \(error)")
        }
    }
}
```

### Mixed Bluetooth and Wi-Fi Accessories

A single descriptor can specify both Bluetooth and Wi-Fi properties. The
system grants access to both interfaces with one tap:

```swift
var descriptor = ASDiscoveryDescriptor()
descriptor.bluetoothServiceUUID = CBUUID(string: "AAAA1111-...")
descriptor.ssid = "MyAccessory-WiFi"
descriptor.supportedOptions = [.bluetoothPairingLE]
```

### Using Company Identifiers

When multiple accessories share a company identifier but differ by
manufacturer data:

```swift
var modelA = ASDiscoveryDescriptor()
modelA.bluetoothCompanyIdentifier = ASBluetoothCompanyIdentifier(0x1234)
modelA.bluetoothManufacturerDataBlob = Data([0x01, 0x00])
modelA.bluetoothManufacturerDataMask = Data([0xFF, 0x00])

var modelB = ASDiscoveryDescriptor()
modelB.bluetoothCompanyIdentifier = ASBluetoothCompanyIdentifier(0x1234)
modelB.bluetoothManufacturerDataBlob = Data([0x02, 0x00])
modelB.bluetoothManufacturerDataMask = Data([0xFF, 0x00])
```

Manufacturer data filters require a company identifier. The blob and mask must
be the same length. The system performs a bitwise AND with the mask on the
scanned data and compares to the blob.

### Service Data Matching

Match accessories by service data instead of manufacturer data. Service data
filters require a service UUID, and the blob and mask must have the same length:

```swift
var descriptor = ASDiscoveryDescriptor()
descriptor.bluetoothServiceUUID = CBUUID(string: "AAAA1111-...")
descriptor.bluetoothServiceDataBlob = Data([0xAB, 0xCD])
descriptor.bluetoothServiceDataMask = Data([0xFF, 0xFF])
```

## Removal and Lifecycle Management

### Removing an Accessory Programmatically

```swift
func removeAccessory(_ accessory: ASAccessory) {
    session.removeAccessory(accessory) { error in
        if let error {
            print("Removal failed: \(error)")
        }
    }
}
```

After removal, the session fires `.accessoryRemoved`. Clean up any
CoreBluetooth or NetworkExtension state associated with the accessory.

### Handling External Removal

Users can remove accessories from Settings > Privacy & Security > Accessories.
Handle this in the event handler:

```swift
case .accessoryRemoved:
    guard let accessory = event.accessory else { return }
    disconnectAndCleanUp(accessory)
```

### Renaming Accessories

Rename an accessory programmatically:

```swift
func renameAccessory(_ accessory: ASAccessory) {
    session.renameAccessory(accessory, options: []) { error in
        if let error {
            print("Rename failed: \(error)")
        }
    }
}
```

For Wi-Fi accessories, pass `.ssid` in rename options to also update the SSID:

```swift
session.renameAccessory(accessory, options: .ssid) { error in
    // SSID updated along with display name
}
```

After renaming, the session fires `.accessoryChanged`.

### Session Invalidation

An invalidated session cannot be reused. Create a new session when needed:

```swift
case .invalidated:
    // Clean up references
    currentSession = nil
    // Create a new session if the app needs to continue
    if shouldRestart {
        currentSession = ASAccessorySession()
        currentSession?.activate(on: .main, eventHandler: handleEvent)
    }
```

## Accessory Images

The picker displays product images in a 180x120 point container. The system
scales the image to fit.

### Image Requirements

- Use PNG with transparent background
- Provide sufficient resolution for 3x displays (540x360 pixels minimum)
- Test in both light mode and dark mode
- Use transparent borders around the product to control apparent size

### Dynamic Image Loading

When using custom filtering, load images dynamically based on the discovered
accessory's advertisement data:

```swift
func loadImageForModel(_ advertisementData: [AnyHashable: Any]?) -> UIImage {
    guard let data = advertisementData,
          let modelByte = (data["kCBAdvDataManufacturerData"] as? Data)?.first else {
        return UIImage(named: "generic-accessory")!
    }

    switch modelByte {
    case 0x01: return UIImage(named: "model-a")!
    case 0x02: return UIImage(named: "model-b")!
    default: return UIImage(named: "generic-accessory")!
    }
}
```

## Picker Display Settings

### Discovery Timeout

Control how long the picker searches before timing out:

```swift
let settings = ASPickerDisplaySettings.default
settings.discoveryTimeout = .medium  // Moderate search duration
session.pickerDisplaySettings = settings
```

| Timeout | Use Case |
|---|---|
| `.short` | Accessory expected to be immediately nearby |
| `.medium` | Standard discovery |
| `.long` | Accessory may take time to become discoverable |
| `.unbounded` | Custom filtering, no automatic timeout |

Custom timeout values use `TimeInterval`:

```swift
settings.discoveryTimeout = ASPickerDisplaySettings.DiscoveryTimeout(rawValue: 30.0)
```

### Combining Settings

```swift
let settings = ASPickerDisplaySettings.default
settings.discoveryTimeout = .unbounded
settings.options.insert(.filterDiscoveryResults)
session.pickerDisplaySettings = settings
```

## Authorization Management

### Authorization States

Each accessory tracks its authorization state:

| State | Meaning |
|---|---|
| `.unauthorized` | Not authorized for use |
| `.awaitingAuthorization` | Authorization in progress |
| `.authorized` | Fully authorized, ready to use |

### Finishing Authorization

For accessories using `.finishInApp` setup option, complete authorization
after the picker closes:

```swift
func finishSetup(for accessory: ASAccessory) {
    let settings = ASAccessorySettings.default
    session.finishAuthorization(for: accessory, settings: settings) { error in
        if let error {
            print("Authorization failed: \(error)")
        }
    }
}
```

### Failing Authorization

If app-side validation fails after the picker closes, reject the accessory:

```swift
func rejectAccessory(_ accessory: ASAccessory) {
    session.failAuthorization(for: accessory) { error in
        if let error {
            print("Fail authorization error: \(error)")
        }
    }
}
```

### Updating Authorization

Update the discovery descriptor for an already-authorized accessory:

```swift
func updateAccessoryDescriptor(_ accessory: ASAccessory) {
    var updatedDescriptor = ASDiscoveryDescriptor()
    updatedDescriptor.bluetoothServiceUUID = CBUUID(string: "NEW-UUID-...")

    session.updateAuthorization(
        for: accessory,
        descriptor: updatedDescriptor
    ) { error in
        if let error {
            print("Update failed: \(error)")
        }
    }
}
```

### Transport Bridging

For accessories that support transport bridging between Bluetooth and Wi-Fi,
configure the bridging identifier in accessory settings:

```swift
let settings = ASAccessorySettings.default
settings.bluetoothTransportBridgingIdentifier = bridgingData

session.finishAuthorization(for: accessory, settings: settings) { error in
    if let error {
        print("Bridging setup failed: \(error)")
    }
}
```

## Error Handling

### ASError Codes

| Error | Meaning | Recovery |
|---|---|---|
| `.activationFailed` | Session activation failed | Retry activation |
| `.invalidated` | Session was invalidated | Create a new session |
| `.invalidRequest` | Invalid picker/descriptor configuration | Check descriptor and plist values |
| `.extensionNotFound` | Required system extension missing | Verify OS version and entitlements |
| `.pickerRestricted` | Picker restricted by MDM or parental controls | Inform the user |
| `.pickerAlreadyActive` | Another picker is already showing | Wait for current picker to dismiss |
| `.userCancelled` | User dismissed the picker | No action needed |
| `.userRestricted` | User restricted from adding accessories | Inform the user |
| `.connectionFailed` | Failed to connect to selected accessory | Prompt retry |
| `.discoveryTimeout` | Discovery timed out without results | Suggest user check accessory power |

### Robust Error Handling

```swift
session.showPicker(for: items) { error in
    guard let error = error as? ASError else { return }

    switch error.code {
    case .userCancelled:
        // Normal dismissal, no action needed
        break
    case .pickerAlreadyActive:
        // Wait for current picker to finish
        break
    case .discoveryTimeout:
        self.showRetryPrompt(
            message: "Accessory not found. Check that it's powered on and nearby."
        )
    case .connectionFailed:
        self.showRetryPrompt(
            message: "Connection failed. Move closer and try again."
        )
    case .invalidRequest:
        // Developer error — check descriptor and Info.plist configuration
        assertionFailure("Invalid AccessorySetupKit request")
    @unknown default:
        self.showErrorAlert(error)
    }
}
```

### Handling Picker Events for Error States

```swift
case .pickerSetupFailed:
    if let error = event.error {
        handleSetupFailure(error)
    }
```

## Full Manager Pattern

A complete `AccessoryManager` class handling the full lifecycle:

```swift
import AccessorySetupKit
import CoreBluetooth
import UIKit

@Observable
final class AccessoryManager {
    private(set) var pairedAccessories: [ASAccessory] = []
    private(set) var isPickerPresented = false

    private var session = ASAccessorySession()
    private var pendingAccessory: ASAccessory?
    private var centralManager: CBCentralManager?
    private var onAccessoryReady: ((ASAccessory) -> Void)?

    func activate() {
        session.activate(on: .main) { [weak self] event in
            self?.handleEvent(event)
        }
    }

    func showPicker(
        items: [ASPickerDisplayItem],
        onReady: @escaping (ASAccessory) -> Void
    ) {
        onAccessoryReady = onReady
        session.showPicker(for: items) { error in
            if let error {
                print("Picker error: \(error)")
            }
        }
    }

    func remove(_ accessory: ASAccessory) {
        session.removeAccessory(accessory) { error in
            if let error {
                print("Remove error: \(error)")
            }
        }
    }

    private func handleEvent(_ event: ASAccessoryEvent) {
        switch event.eventType {
        case .activated:
            pairedAccessories = session.accessories
        case .accessoryAdded:
            pendingAccessory = event.accessory
            if let accessory = event.accessory {
                pairedAccessories.append(accessory)
            }
        case .accessoryRemoved:
            if let accessory = event.accessory {
                pairedAccessories.removeAll { $0 == accessory }
            }
        case .accessoryChanged:
            if let accessory = event.accessory,
               let index = pairedAccessories.firstIndex(of: accessory) {
                pairedAccessories[index] = accessory
            }
        case .pickerDidPresent:
            isPickerPresented = true
        case .pickerDidDismiss:
            isPickerPresented = false
            if let accessory = pendingAccessory {
                pendingAccessory = nil
                onAccessoryReady?(accessory)
            }
        case .invalidated:
            session = ASAccessorySession()
            activate()
        @unknown default:
            break
        }
    }
}
```

## SwiftUI Integration

### AccessorySetupKit in a SwiftUI View

```swift
import SwiftUI
import AccessorySetupKit
import CoreBluetooth

struct AccessorySetupView: View {
    @State private var manager = AccessoryManager()
    @State private var showError = false
    @State private var errorMessage = ""

    var body: some View {
        List {
            Section("Paired Accessories") {
                ForEach(manager.pairedAccessories, id: \.displayName) { accessory in
                    HStack {
                        Text(accessory.displayName)
                        Spacer()
                        Text(accessory.state == .authorized ? "Connected" : "Pending")
                            .foregroundStyle(.secondary)
                    }
                }
            }

            Section {
                Button("Add Accessory") {
                    addAccessory()
                }
                .disabled(manager.isPickerPresented)
            }
        }
        .onAppear {
            manager.activate()
        }
        .alert("Error", isPresented: $showError) {
            Button("OK") { }
        } message: {
            Text(errorMessage)
        }
    }

    private func addAccessory() {
        var descriptor = ASDiscoveryDescriptor()
        descriptor.bluetoothServiceUUID = CBUUID(string: "ABCD1234-...")

        guard let image = UIImage(named: "my-accessory") else { return }

        let item = ASPickerDisplayItem(
            name: "My Accessory",
            productImage: image,
            descriptor: descriptor
        )

        manager.showPicker(items: [item]) { accessory in
            print("Accessory ready: \(accessory.displayName)")
        }
    }
}
```

### Tracking Picker State

Disable UI elements while the picker is active to prevent double presentation:

```swift
Button("Add Accessory") {
    addAccessory()
}
.disabled(manager.isPickerPresented)
```

The picker runs in a separate process and occludes part of the app. Avoid
making UI updates that would not be visible while the picker is shown. Use
`.pickerDidPresent` and `.pickerDidDismiss` events to track visibility.
