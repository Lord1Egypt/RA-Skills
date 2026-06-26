# Network.framework

Low-level networking with the Network framework. Use when you need TCP/UDP
connections, WebSockets, Bonjour service discovery, local servers, or network
path monitoring beyond what URLSession provides. All examples target
Swift 6.3 / iOS 26+.

## Contents

- [NWConnection](#nwconnection)
- [NWListener](#nwlistener)
- [NWBrowser](#nwbrowser)
- [NWPathMonitor](#nwpathmonitor)
- [NWParameters Configuration](#nwparameters-configuration)
- [TLS Configuration](#tls-configuration)
- [WebSocket Support](#websocket-support)
- [NetworkConnection (iOS 26+)](#networkconnection-ios-26)

## NWConnection

A bidirectional data connection between a local and remote endpoint. Supports
TCP, UDP, TLS, DTLS, QUIC, and WebSocket protocols.

**Documentation:**
[sosumi.ai/documentation/network/nwconnection](https://sosumi.ai/documentation/network/nwconnection)

### TCP Connection

```swift
import Network

let connection = NWConnection(
    host: "api.example.com",
    port: 443,
    using: .tls
)

connection.stateUpdateHandler = { state in
    switch state {
    case .ready:
        print("Connected")
    case .waiting(let error):
        print("Waiting: \(error.localizedDescription)")
    case .failed(let error):
        print("Failed: \(error.localizedDescription)")
    case .cancelled:
        print("Cancelled")
    default:
        break
    }
}

connection.start(queue: .main)
```

### Sending Data

```swift
func send(_ data: Data, on connection: NWConnection) {
    connection.send(
        content: data,
        contentContext: .defaultMessage,
        isComplete: true,
        completion: .contentProcessed { error in
            if let error {
                print("Send error: \(error)")
            }
        }
    )
}
```

### Receiving Data

```swift
func receive(on connection: NWConnection) {
    connection.receive(
        minimumIncompleteLength: 1,
        maximumLength: 65536
    ) { content, contentContext, isComplete, error in
        if let data = content {
            handleData(data)
        }
        if isComplete {
            connection.cancel()
        } else if let error {
            print("Receive error: \(error)")
        } else {
            // Continue receiving
            receive(on: connection)
        }
    }
}
```

### UDP Connection

```swift
let udpConnection = NWConnection(
    host: "239.0.0.1",
    port: 5000,
    using: .udp
)

udpConnection.stateUpdateHandler = { state in
    if case .ready = state {
        let message = "Hello".data(using: .utf8)!
        udpConnection.send(
            content: message,
            completion: .contentProcessed { _ in }
        )
    }
}

udpConnection.start(queue: .main)
```

### Connection Lifecycle

States flow in order: `setup` → `preparing` → `ready` → `cancelled`/`failed`.
A connection may enter `waiting(NWError)` if the network path is unavailable
and retry when connectivity returns.

Always cancel connections when done:

```swift
connection.cancel()  // Releases resources, transitions to .cancelled
```

## NWListener

An object that listens for incoming network connections. Use to create local
TCP/UDP servers.

**Documentation:**
[sosumi.ai/documentation/network/nwlistener](https://sosumi.ai/documentation/network/nwlistener)

### TCP Server

```swift
import Network

func startServer(port: UInt16) throws -> NWListener {
    let listener = try NWListener(using: .tcp, on: NWEndpoint.Port(rawValue: port)!)

    listener.stateUpdateHandler = { state in
        switch state {
        case .ready:
            print("Listening on port \(listener.port?.rawValue ?? 0)")
        case .failed(let error):
            print("Listener failed: \(error)")
            listener.cancel()
        default:
            break
        }
    }

    listener.newConnectionHandler = { connection in
        print("New connection from \(connection.endpoint)")
        connection.stateUpdateHandler = { state in
            if case .ready = state {
                receive(on: connection)
            }
        }
        connection.start(queue: .main)
    }

    listener.start(queue: .main)
    return listener
}
```

### Advertising via Bonjour

```swift
let listener = try NWListener(using: .tcp)
listener.service = NWListener.Service(
    name: "MyApp",
    type: "_myapp._tcp"
)
listener.serviceRegistrationUpdateHandler = { change in
    switch change {
    case .add(let endpoint):
        print("Service registered: \(endpoint)")
    default:
        break
    }
}
listener.start(queue: .main)
```

## NWBrowser

Discovers Bonjour/mDNS services on the local network.

**Documentation:**
[sosumi.ai/documentation/network/nwbrowser](https://sosumi.ai/documentation/network/nwbrowser)

### Service Discovery

```swift
import Network

let browser = NWBrowser(
    for: .bonjour(type: "_myapp._tcp", domain: nil),
    using: .tcp
)

browser.stateUpdateHandler = { state in
    if case .failed(let error) = state {
        print("Browser failed: \(error)")
    }
}

browser.browseResultsChangedHandler = { results, changes in
    for result in results {
        switch result.endpoint {
        case .service(let name, let type, let domain, _):
            print("Found: \(name).\(type)\(domain)")
        default:
            break
        }
    }

    for change in changes {
        switch change {
        case .added(let result):
            print("Added: \(result.endpoint)")
        case .removed(let result):
            print("Removed: \(result.endpoint)")
        default:
            break
        }
    }
}

browser.start(queue: .main)
```

### Connecting to a Discovered Service

```swift
// result is an NWBrowser.Result from browseResultsChangedHandler
let connection = NWConnection(to: result.endpoint, using: .tcp)
connection.start(queue: .main)
```

## NWPathMonitor

Monitors network path changes. Replaces the deprecated `SCNetworkReachability`
API. Use to detect connectivity changes, expensive paths (cellular), and
constrained paths (Low Data Mode).

**Documentation:**
[sosumi.ai/documentation/network/nwpathmonitor](https://sosumi.ai/documentation/network/nwpathmonitor)

### Basic Reachability with AsyncSequence

```swift
import Network

@MainActor @Observable
class ConnectivityModel {
    var isConnected = true
    var isExpensive = false
    var isConstrained = false

    func startMonitoring() async {
        let monitor = NWPathMonitor()

        for await path in monitor {
            isConnected = path.status == .satisfied
            isExpensive = path.isExpensive       // Cellular
            isConstrained = path.isConstrained   // Low Data Mode
        }
    }
}
```

### Monitor Specific Interface

```swift
// Monitor only Wi-Fi
let wifiMonitor = NWPathMonitor(requiredInterfaceType: .wifi)
wifiMonitor.pathUpdateHandler = { path in
    print("Wi-Fi: \(path.status)")
}
wifiMonitor.start(queue: .global())
```

### Key NWPath Properties

| Property | Description |
|---|---|
| `status` | `.satisfied`, `.unsatisfied`, or `.requiresConnection` |
| `isExpensive` | `true` on cellular or personal hotspot |
| `isConstrained` | `true` when Low Data Mode is enabled |
| `availableInterfaces` | Array of available `NWInterface` objects |
| `supportsDNS` | Whether DNS resolution is available |
| `supportsIPv4` / `supportsIPv6` | Protocol family support |

### Adapting Behavior

```swift
let monitor = NWPathMonitor()

for await path in monitor {
    if path.isConstrained {
        // Low Data Mode: reduce image quality, skip prefetch
        imageQuality = .low
    } else if path.isExpensive {
        // Cellular: use standard quality, skip video preload
        imageQuality = .standard
    } else {
        // Wi-Fi: full quality, prefetch aggressively
        imageQuality = .high
    }
}
```

## NWParameters Configuration

`NWParameters` defines the protocols and options for connections and listeners.

```swift
import Network

// TCP with custom options
let tcpParams = NWParameters.tcp
tcpParams.requiredInterfaceType = .wifi
tcpParams.prohibitExpensivePaths = true
tcpParams.prohibitConstrainedPaths = true

let tcpOptions = tcpParams.defaultProtocolStack
    .transportProtocol as! NWProtocolTCP.Options
tcpOptions.connectionTimeout = 10
tcpOptions.enableKeepalive = true
tcpOptions.keepaliveInterval = 30

let connection = NWConnection(
    host: "api.example.com",
    port: 8080,
    using: tcpParams
)
```

### UDP Parameters

```swift
let udpParams = NWParameters.udp
let udpOptions = udpParams.defaultProtocolStack
    .transportProtocol as! NWProtocolUDP.Options
udpOptions.preferNoChecksum = true

let connection = NWConnection(
    host: "239.0.0.1",
    port: 5000,
    using: udpParams
)
```

## TLS Configuration

Configure TLS for secure connections using `NWProtocolTLS.Options`.
Network.framework operates below the URL Loading System, so ATS does not
automatically enforce URLSession-style policy here. When you use
Network.framework for a secure protocol, configure TLS parameters and trust
handling for that protocol stack; keep deep certificate-trust and SPKI pinning
implementation in `swift-security`.

```swift
import Network

let tlsParams = NWParameters(tls: NWProtocolTLS.Options())

// Access TLS options for customization
let tlsOptions = tlsParams.defaultProtocolStack
    .applicationProtocols.first as! NWProtocolTLS.Options

sec_protocol_options_set_min_tls_protocol_version(
    tlsOptions.securityProtocolOptions,
    .TLSv13
)

let connection = NWConnection(
    host: "secure.example.com",
    port: 443,
    using: tlsParams
)
```

### Inspecting TLS Metadata

```swift
connection.stateUpdateHandler = { state in
    if case .ready = state {
        if let metadata = connection.metadata(
            definition: NWProtocolTLS.definition
        ) as? NWProtocolTLS.Metadata {
            let secMetadata = metadata.securityProtocolMetadata
            let negotiatedProtocol = sec_protocol_metadata_get_negotiated_tls_protocol_version(secMetadata)
            print("TLS version: \(negotiatedProtocol)")
        }
    }
}
```

## WebSocket Support

Network.framework supports WebSocket via `NWProtocolWebSocket`.

### WebSocket Client

```swift
import Network

func createWebSocketConnection(url: String) -> NWConnection {
    let wsOptions = NWProtocolWebSocket.Options()
    wsOptions.autoReplyPing = true

    let params = NWParameters.tls
    params.defaultProtocolStack.applicationProtocols.insert(
        wsOptions, at: 0
    )

    let connection = NWConnection(
        host: NWEndpoint.Host(url),
        port: 443,
        using: params
    )

    return connection
}
```

### Sending WebSocket Messages

```swift
func sendWebSocketMessage(_ text: String, on connection: NWConnection) {
    let metadata = NWProtocolWebSocket.Metadata(opcode: .text)
    let context = NWConnection.ContentContext(
        identifier: "textMessage",
        metadata: [metadata]
    )

    let data = text.data(using: .utf8)
    connection.send(
        content: data,
        contentContext: context,
        isComplete: true,
        completion: .contentProcessed { error in
            if let error {
                print("WebSocket send error: \(error)")
            }
        }
    )
}
```

### Receiving WebSocket Messages

```swift
func receiveWebSocketMessage(on connection: NWConnection) {
    connection.receiveMessage { data, context, isComplete, error in
        if let data,
           let metadata = context?.protocolMetadata(
               definition: NWProtocolWebSocket.definition
           ) as? NWProtocolWebSocket.Metadata {
            switch metadata.opcode {
            case .text:
                let text = String(data: data, encoding: .utf8) ?? ""
                print("Received text: \(text)")
            case .binary:
                print("Received binary: \(data.count) bytes")
            case .close:
                print("Connection closed")
                return
            default:
                break
            }
        }
        // Continue receiving
        receiveWebSocketMessage(on: connection)
    }
}
```

## NetworkConnection (iOS 26+)

`NetworkConnection` is a new Swift-native API introduced in iOS 26 that
provides a modern, type-safe alternative to `NWConnection`. It uses generics
over protocol stacks, supports structured concurrency patterns, and integrates
with async/await via closure-based state handlers.

**Documentation:**
[sosumi.ai/documentation/network/networkconnection](https://sosumi.ai/documentation/network/networkconnection)

### Key Differences from NWConnection

| | `NWConnection` | `NetworkConnection` |
|---|---|---|
| **Availability** | iOS 12+ | iOS 26+ |
| **Type safety** | Untyped protocol stack | Generic `ApplicationProtocol` parameter |
| **Streams** | Single connection | Built-in QUIC stream multiplexing |
| **State updates** | `stateUpdateHandler` callback | `onStateUpdate`, `onPathUpdate` closures |
| **Wi-Fi Aware** | Not supported | `wifiAware` property |
| **API style** | Callback-based | Closure-based with `Sendable` support |

### Basic Usage Shape

```swift
import Network

let endpoint = NWEndpoint.hostPort(host: "api.example.com", port: 443)
```

Use the initializer variant that matches your protocol stack. The documented
forms are:

```swift
// Protocol-stack builder form.
NetworkConnection(to: endpoint) {
    // ProtocolStackBuilder<ApplicationProtocol>
}

// Parameters-builder form.
NetworkConnection(to: endpoint, using: builder)
```

After constructing a concrete connection for your app's protocol stack, install
state handlers and start it:

```swift
func startConnection<ApplicationProtocol>(
    _ connection: NetworkConnection<ApplicationProtocol>
) where ApplicationProtocol: NetworkProtocolOptions {
    connection.onStateUpdate { state in
        switch state {
        case .ready:
            print("Connected")
        case .failed(let error):
            print("Failed: \(error)")
        case .cancelled:
            print("Cancelled")
        default:
            break
        }
    }

    connection.start()
}
```

`NetworkConnection` is for lower-level protocol stacks and QUIC-style transport
work. Keep ordinary HTTP APIs on `URLSession` unless you need capabilities that
the URL Loading System does not provide.

### QUIC Multiplexed Streams

`NetworkConnection<QUIC>` supports QUIC stream multiplexing natively.
Opening and accepting streams are asynchronous and throwing operations.

```swift
func openBidirectionalStream(
    on connection: NetworkConnection<QUIC>
) async throws -> QUIC.Stream<QUICStream> {
    try await connection.openStream(directionality: .bidirectional)
}

func handleInboundStreams(
    on connection: NetworkConnection<QUIC>
) async throws {
    try await connection.inboundStreams { stream in
        // Process each incoming QUIC stream.
    }
}
```

### Migration Guidance

For new iOS 26+ low-level networking work, evaluate `NetworkConnection` before
adding new `NWConnection` code:
- It provides stronger type safety through its generic `ApplicationProtocol`.
- Stream multiplexing is a first-class concept for QUIC.
- The API is designed for modern Swift with `Sendable` conformance.

For projects supporting iOS versions before 26, continue using `NWConnection`.
Both APIs coexist and `NWConnection` is not deprecated.
