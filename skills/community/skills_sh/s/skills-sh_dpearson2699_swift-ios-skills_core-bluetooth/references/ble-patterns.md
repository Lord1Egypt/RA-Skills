# Core Bluetooth Extended Patterns

Overflow reference for the `core-bluetooth` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [SwiftUI BLE Integration](#swiftui-ble-integration)
- [Reconnection Strategies](#reconnection-strategies)
- [Data Parsing Helpers](#data-parsing-helpers)
- [Write Flow Control](#write-flow-control)
- [Multiple Peripheral Management](#multiple-peripheral-management)
- [L2CAP Channels](#l2cap-channels)
- [Peripheral Role: Responding to Requests](#peripheral-role-responding-to-requests)

## SwiftUI BLE Integration

### Observable Bluetooth Manager

```swift
import CoreBluetooth
import SwiftUI

@Observable
@MainActor
final class BLEViewModel: NSObject {
    private var centralManager: CBCentralManager!
    private var connectedPeripheral: CBPeripheral?

    var isBluetoothOn = false
    var isScanning = false
    var isConnected = false
    var discoveredDevices: [DiscoveredDevice] = []
    var heartRate: Int = 0

    struct DiscoveredDevice: Identifiable {
        let id: UUID
        let name: String
        let rssi: Int
        let peripheral: CBPeripheral
    }

    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }

    func startScan() {
        guard isBluetoothOn else { return }
        discoveredDevices.removeAll()
        isScanning = true
        centralManager.scanForPeripherals(
            withServices: [CBUUID(string: "180D")],
            options: nil
        )
    }

    func stopScan() {
        centralManager.stopScan()
        isScanning = false
    }

    func connect(to device: DiscoveredDevice) {
        stopScan()
        connectedPeripheral = device.peripheral
        centralManager.connect(device.peripheral)
    }

    func disconnect() {
        guard let peripheral = connectedPeripheral else { return }
        centralManager.cancelPeripheralConnection(peripheral)
    }
}

extension BLEViewModel: CBCentralManagerDelegate {
    nonisolated func centralManagerDidUpdateState(_ central: CBCentralManager) {
        Task { @MainActor in
            isBluetoothOn = central.state == .poweredOn
        }
    }

    nonisolated func centralManager(
        _ central: CBCentralManager,
        didDiscover peripheral: CBPeripheral,
        advertisementData: [String: Any],
        rssi RSSI: NSNumber
    ) {
        Task { @MainActor in
            let name = peripheral.name ?? "Unknown"
            let device = DiscoveredDevice(
                id: peripheral.identifier,
                name: name,
                rssi: RSSI.intValue,
                peripheral: peripheral
            )
            if !discoveredDevices.contains(where: { $0.id == device.id }) {
                discoveredDevices.append(device)
            }
        }
    }

    nonisolated func centralManager(
        _ central: CBCentralManager,
        didConnect peripheral: CBPeripheral
    ) {
        Task { @MainActor in
            isConnected = true
            peripheral.delegate = self
            peripheral.discoverServices([CBUUID(string: "180D")])
        }
    }

    nonisolated func centralManager(
        _ central: CBCentralManager,
        didDisconnectPeripheral peripheral: CBPeripheral,
        timestamp: CFAbsoluteTime,
        isReconnecting: Bool,
        error: Error?
    ) {
        Task { @MainActor in
            isConnected = false
            connectedPeripheral = nil
        }
    }
}

extension BLEViewModel: CBPeripheralDelegate {
    nonisolated func peripheral(
        _ peripheral: CBPeripheral,
        didDiscoverServices error: Error?
    ) {
        guard let services = peripheral.services else { return }
        for service in services {
            peripheral.discoverCharacteristics(
                [CBUUID(string: "2A37")],
                for: service
            )
        }
    }

    nonisolated func peripheral(
        _ peripheral: CBPeripheral,
        didDiscoverCharacteristicsFor service: CBService,
        error: Error?
    ) {
        guard let characteristics = service.characteristics else { return }
        for char in characteristics where char.properties.contains(.notify) {
            peripheral.setNotifyValue(true, for: char)
        }
    }

    nonisolated func peripheral(
        _ peripheral: CBPeripheral,
        didUpdateValueFor characteristic: CBCharacteristic,
        error: Error?
    ) {
        guard let data = characteristic.value, data.count >= 2 else { return }
        let flags = data[0]
        let bpm: Int
        if (flags & 0x01) != 0 {
            guard data.count >= 3 else { return }
            bpm = Int(data[1]) | (Int(data[2]) << 8)
        } else {
            bpm = Int(data[1])
        }
        Task { @MainActor in
            heartRate = bpm
        }
    }
}
```

### SwiftUI View

```swift
struct HeartRateView: View {
    @State private var viewModel = BLEViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isConnected {
                    VStack {
                        Image(systemName: "heart.fill")
                            .font(.system(size: 60))
                            .foregroundStyle(.red)
                        Text("\(viewModel.heartRate) BPM")
                            .font(.largeTitle.monospacedDigit())
                        Button("Disconnect") { viewModel.disconnect() }
                    }
                } else {
                    List(viewModel.discoveredDevices) { device in
                        Button {
                            viewModel.connect(to: device)
                        } label: {
                            HStack {
                                Text(device.name)
                                Spacer()
                                Text("\(device.rssi) dBm")
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }
            .navigationTitle("Heart Rate Monitor")
            .toolbar {
                if !viewModel.isConnected {
                    Button(viewModel.isScanning ? "Stop" : "Scan") {
                        viewModel.isScanning ? viewModel.stopScan() : viewModel.startScan()
                    }
                }
            }
        }
    }
}
```

## Reconnection Strategies

### Auto-Reconnect on Disconnect

```swift
func centralManager(
    _ central: CBCentralManager,
    didDisconnectPeripheral peripheral: CBPeripheral,
    timestamp: CFAbsoluteTime,
    isReconnecting: Bool,
    error: Error?
) {
    if !isReconnecting {
        // Attempt to reconnect
        central.connect(peripheral, options: nil)
    }
}
```

### Reconnecting to Known Peripherals

Store the peripheral's UUID and reconnect at next launch using
`retrievePeripherals(withIdentifiers:)`.

```swift
func reconnectToKnownDevice(uuid: UUID) {
    let peripherals = centralManager.retrievePeripherals(
        withIdentifiers: [uuid]
    )
    if let peripheral = peripherals.first {
        connectedPeripheral = peripheral
        centralManager.connect(peripheral, options: nil)
    }
}
```

### Retrieving Already-Connected Peripherals

If another app has connected to the peripheral, you can retrieve it by service.

```swift
func findConnectedHeartRateMonitors() -> [CBPeripheral] {
    centralManager.retrieveConnectedPeripherals(
        withServices: [CBUUID(string: "180D")]
    )
}
```

## Data Parsing Helpers

### Generic Data Reader

```swift
extension Data {
    func readUInt8(at offset: Int) -> UInt8? {
        guard offset < count else { return nil }
        return self[offset]
    }

    func readUInt16LE(at offset: Int) -> UInt16? {
        guard offset + 1 < count else { return nil }
        return UInt16(self[offset]) | (UInt16(self[offset + 1]) << 8)
    }

    func readUInt32LE(at offset: Int) -> UInt32? {
        guard offset + 3 < count else { return nil }
        return UInt32(self[offset])
            | (UInt32(self[offset + 1]) << 8)
            | (UInt32(self[offset + 2]) << 16)
            | (UInt32(self[offset + 3]) << 24)
    }
}
```

### Battery Level Parser

```swift
func parseBatteryLevel(_ data: Data) -> Int? {
    data.readUInt8(at: 0).map { Int($0) }
}
```

## Write Flow Control

Use `.withResponse` for commands that need delivery confirmation. Reserve
`.withoutResponse` for streaming or fire-and-forget payloads, and pause when the
peripheral cannot accept more unacknowledged writes.

```swift
func writeChunks(_ chunks: [Data],
                 to characteristic: CBCharacteristic,
                 on peripheral: CBPeripheral) {
    for chunk in chunks {
        guard chunk.count <= peripheral.maximumWriteValueLength(for: .withoutResponse),
              peripheral.canSendWriteWithoutResponse else { return }
        peripheral.writeValue(chunk, for: characteristic, type: .withoutResponse)
    }
}

func peripheralIsReady(toSendWriteWithoutResponse peripheral: CBPeripheral) {
    // Continue draining queued chunks here.
}
```

## Multiple Peripheral Management

### Managing Several Connections

```swift
@MainActor
final class MultiDeviceManager: NSObject {
    private var centralManager: CBCentralManager!
    private var connectedPeripherals: [UUID: CBPeripheral] = [:]

    func centralManager(
        _ central: CBCentralManager,
        didDiscover peripheral: CBPeripheral,
        advertisementData: [String: Any],
        rssi RSSI: NSNumber
    ) {
        let id = peripheral.identifier
        guard connectedPeripherals[id] == nil else { return }
        connectedPeripherals[id] = peripheral
        central.connect(peripheral)
    }

    func centralManager(
        _ central: CBCentralManager,
        didConnect peripheral: CBPeripheral
    ) {
        peripheral.delegate = self
        peripheral.discoverServices(nil)
    }

    func disconnectAll() {
        for peripheral in connectedPeripherals.values {
            centralManager.cancelPeripheralConnection(peripheral)
        }
        connectedPeripherals.removeAll()
    }
}
```

## L2CAP Channels

Use L2CAP channels for higher-throughput, stream-oriented data transfer.

### Central Side

```swift
func peripheral(
    _ peripheral: CBPeripheral,
    didOpen channel: CBL2CAPChannel?,
    error: Error?
) {
    guard let channel else { return }
    let inputStream = channel.inputStream
    let outputStream = channel.outputStream

    inputStream.delegate = self
    outputStream.delegate = self
    inputStream.schedule(in: .main, forMode: .default)
    outputStream.schedule(in: .main, forMode: .default)
    inputStream.open()
    outputStream.open()
}

// Open a channel to a known PSM
peripheral.openL2CAPChannel(CBL2CAPPSM(0x0025))
```

### Peripheral Side

```swift
// Publish a channel listener
peripheralManager.publishL2CAPChannel(withEncryption: true)

func peripheralManager(
    _ peripheral: CBPeripheralManager,
    didPublishL2CAPChannel PSM: CBL2CAPPSM,
    error: Error?
) {
    // Share the PSM with centrals via a characteristic value
    print("Published L2CAP channel on PSM: \(PSM)")
}
```

## Peripheral Role: Responding to Requests

When acting as a peripheral, respond to read and write requests from connected centrals.

```swift
extension BLEPeripheralManager: CBPeripheralManagerDelegate {
    func peripheralManager(
        _ peripheral: CBPeripheralManager,
        didReceiveRead request: CBATTRequest
    ) {
        if request.characteristic.uuid == charUUID {
            let value = currentSensorData()
            request.value = value.subdata(
                in: request.offset..<value.count
            )
            peripheral.respond(to: request, withResult: .success)
        } else {
            peripheral.respond(to: request, withResult: .attributeNotFound)
        }
    }

    func peripheralManager(
        _ peripheral: CBPeripheralManager,
        didReceiveWrite requests: [CBATTRequest]
    ) {
        for request in requests {
            if let value = request.value {
                handleIncomingData(value)
            }
        }
        // Respond to the first request -- Core Bluetooth sends the
        // response for all requests in the batch
        if let first = requests.first {
            peripheral.respond(to: first, withResult: .success)
        }
    }

    func peripheralManager(
        _ peripheral: CBPeripheralManager,
        central: CBCentral,
        didSubscribeTo characteristic: CBCharacteristic
    ) {
        // Central subscribed to notifications -- start sending updates
        startSendingUpdates()
    }

    func peripheralManager(
        _ peripheral: CBPeripheralManager,
        central: CBCentral,
        didUnsubscribeFrom characteristic: CBCharacteristic
    ) {
        stopSendingUpdates()
    }
}
```
