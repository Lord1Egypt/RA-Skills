# BrowserEngineKit Patterns

Extended patterns and recipes for BrowserEngineKit. Covers XPC communication,
text interaction, layer hosting, scroll views, drag interaction, content
filtering, accessibility, web app manifests, and full browser manager patterns.

## Contents

- [XPC Communication Patterns](#xpc-communication-patterns)
- [Text Input Integration](#text-input-integration)
- [Layer Hosting Patterns](#layer-hosting-patterns)
- [Scroll View Integration](#scroll-view-integration)
- [Drag Interaction](#drag-interaction)
- [Context Menus](#context-menus)
- [Content Filtering](#content-filtering)
- [Accessibility](#accessibility)
- [Web App Manifests](#web-app-manifests)
- [Download Management](#download-management)
- [Process Manager Pattern](#process-manager-pattern)
- [File Access in Extensions](#file-access-in-extensions)
- [Memory Attribution](#memory-attribution)

## XPC Communication Patterns

### Proxy Object Pattern

Create proxy objects that wrap XPC connections for type-safe messaging between
the host app and extensions:

```swift
import BrowserEngineKit

/// Proxy for sending messages from the host app to a web content extension.
final class WebContentProxy: Sendable {
    let connection: xpc_connection_t

    init(connection: xpc_connection_t) {
        self.connection = connection
        xpc_connection_set_event_handler(connection) { event in
            // Handle connection errors
        }
        xpc_connection_activate(connection)
    }

    func loadURL(_ url: URL) async throws -> Data {
        // Encode request as XPC dictionary, send, await reply
        let message = xpc_dictionary_create(nil, nil, 0)
        xpc_dictionary_set_string(message, "action", "load")
        xpc_dictionary_set_string(message, "url", url.absoluteString)

        return try await withCheckedThrowingContinuation { continuation in
            xpc_connection_send_message_with_reply(
                connection, message, .main
            ) { reply in
                // Decode reply
            }
        }
    }
}
```

### Brokering Anonymous Endpoints

The host app brokers direct connections between extensions by exchanging
anonymous XPC endpoints:

```swift
// Host app side
func bootstrapContentExtension() async throws {
    // 1. Get endpoints from networking and rendering extensions
    let networkConn = try networkProcess.makeLibXPCConnection()
    let networkProxy = NetworkingProxy(connection: networkConn)
    let networkEndpoint = try await networkProxy.getEndpoint()

    let renderConn = try renderingProcess.makeLibXPCConnection()
    let renderProxy = RenderingProxy(connection: renderConn)
    let renderEndpoint = try await renderProxy.getEndpoint()

    // 2. Send both endpoints to the content extension
    let contentConn = try contentProcess.makeLibXPCConnection()
    let contentProxy = WebContentProxy(connection: contentConn)
    try await contentProxy.bootstrap(
        networkEndpoint: networkEndpoint,
        renderEndpoint: renderEndpoint
    )
}
```

On the extension side, create the anonymous connection from the received
endpoint:

```swift
// Inside the web content extension
func handleBootstrap(
    networkEndpoint: xpc_endpoint_t,
    renderEndpoint: xpc_endpoint_t
) async throws {
    let networkConn = xpc_connection_create_from_endpoint(networkEndpoint)
    let renderConn = xpc_connection_create_from_endpoint(renderEndpoint)

    // Verify connections are alive
    try await networkConn.ping()
    try await renderConn.ping()

    self.networkProxy = NetworkingProxy(connection: networkConn)
    self.renderProxy = RenderingProxy(connection: renderConn)
}
```

### Extension-Side Connection Handling

Extensions receive incoming XPC connections via their `handle(xpcConnection:)`
implementation:

```swift
@main
final class MyWebContentExtension: WebContentExtension {
    private var hostConnection: xpc_connection_t?

    func handle(xpcConnection: xpc_connection_t) {
        hostConnection = xpcConnection
        xpc_connection_set_event_handler(xpcConnection) { [weak self] event in
            guard let self else { return }
            if xpc_get_type(event) == XPC_TYPE_DICTIONARY {
                self.handleMessage(event)
            }
        }
        xpc_connection_activate(xpcConnection)
    }

    private func handleMessage(_ message: xpc_object_t) {
        guard let action = xpc_dictionary_get_string(message, "action") else {
            return
        }
        switch String(cString: action) {
        case "load":
            // Handle page load request
            break
        case "bootstrap":
            // Handle bootstrap with extension endpoints
            break
        default:
            break
        }
    }
}
```

## Text Input Integration

### Adopting BETextInput

Implement `BETextInput` on a custom view to integrate with UIKit's text
system. This is required for any view that displays editable web content:

```swift
import BrowserEngineKit
import UIKit

final class BrowserTextView: UIView, BETextInput {
    var asyncInputDelegate: (any BETextInputDelegate)?
    var isEditable: Bool = true

    func handleKeyEntry(
        _ entry: BEKeyEntry,
        completionHandler: (BEKeyEntry, Bool) -> Void
    ) {
        let handled = entry.state == .down
            ? processKeyDown(entry.key)
            : processKeyUp(entry.key)
        completionHandler(entry, handled)
    }

    func shiftKeyStateChanged(
        fromState: BEKeyModifierFlags,
        toState: BEKeyModifierFlags
    ) {
        if toState == .shift { beginExtendingSelection() }
    }

    var selectedText: String?
    var selectedTextRange: UITextRange?
    var isSelectionAtDocumentStart: Bool = false

    func updateCurrentSelection(
        to point: CGPoint,
        from gesture: BEGestureType,
        in state: UIGestureRecognizer.State
    ) {
        switch gesture {
        case .oneFingerTap: moveCaret(to: point)
        case .oneFingerDoubleTap: selectWord(at: point)
        case .oneFingerTripleTap: selectParagraph(at: point)
        default: break
        }
    }

    var markedText: String?
    var attributedMarkedText: NSAttributedString?
    var markedTextRange: UITextRange?
    var hasMarkedText: Bool { markedText != nil }

    func setMarkedText(_ text: String?, selectedRange: NSRange) {
        markedText = text
    }

    func unmarkText() {
        markedText = nil
    }

    // Additional BETextInput requirements omitted for brevity.
    // See Apple docs for the full protocol surface.
}
```

### Text Interaction and Selection Navigation

`BETextInteraction` provides system-standard selection handles, edit menus,
and context menus. Adopt `BETextSelectionDirectionNavigation` for arrow-key
and gesture-based caret movement:

```swift
let textInteraction = BETextInteraction()
textInteraction.delegate = self
browserTextView.addInteraction(textInteraction)
```

The delegate receives `systemWillChangeSelection(for:)` and
`systemDidChangeSelection(for:)` callbacks.

### Extended Text Input Traits

Customize insertion point, selection handle, and highlight colors through
`BEExtendedTextInputTraits`. Set `isSingleLineDocument` and
`isTypingAdaptationEnabled` as appropriate for the content type.

## Layer Hosting Patterns

### Cross-Process Rendering

The rendering extension creates content in a `LayerHierarchy` that the host
app displays via `LayerHierarchyHostingView`. The handle is passed over XPC.

```swift
// Rendering extension: create layer hierarchy
import BrowserEngineKit
import QuartzCore

func createPageLayer() throws -> LayerHierarchyHandle {
    let hierarchy = try LayerHierarchy()

    let pageLayer = CALayer()
    pageLayer.bounds = CGRect(x: 0, y: 0, width: 390, height: 844)
    // ... populate layer with rendered content ...

    hierarchy.layer = pageLayer
    return hierarchy.handle
}
```

```swift
// Host app: display remote layer
func displayPage(handle: LayerHierarchyHandle) {
    let hostingView = LayerHierarchyHostingView()
    hostingView.handle = handle
    hostingView.frame = containerView.bounds
    containerView.addSubview(hostingView)
}
```

### Serializing Handles for XPC

`LayerHierarchyHandle` supports XPC serialization for transport between
processes:

```swift
// Sender
let xpcRep = handle.createXPCRepresentation()
xpc_dictionary_set_value(message, "layerHandle", xpcRep)

// Receiver
let xpcRep = xpc_dictionary_get_value(message, "layerHandle")
let handle = try LayerHierarchyHandle(xpcRepresentation: xpcRep)
```

### Synchronized Transactions

When both the host app and the rendering extension need to update layers
atomically, create one coordinator and pass its XPC representation to the other
process:

```swift
// Host app: create coordinator and send its XPC representation to rendering
let coordinator = try LayerHierarchyHostingTransactionCoordinator()
coordinator.add(hostingView)
let xpcRep = coordinator.createXPCRepresentation()
try await renderProxy.prepareTransaction(coordinatorRepresentation: xpcRep)

// Rendering extension: reconstruct from the received representation
let renderCoordinator = try LayerHierarchyHostingTransactionCoordinator(
    xpcRepresentation: xpcRep
)
renderCoordinator.add(hierarchy)

// Commit every coordinator instance after both processes add their participants
renderCoordinator.commit()
coordinator.commit()
```

The coordinator ensures that layer changes from both processes appear in the
same frame. Keep coordinator lifetimes short, and call `commit()` as the final
operation on each instance.

## Scroll View Integration

### Custom Scroll Handling

`BEScrollView` provides direct access to scroll events for browser engines
that implement their own scrolling:

```swift
import BrowserEngineKit

final class BrowserScrollView: BEScrollView {
    override init(frame: CGRect) {
        super.init(frame: frame)
        delegate = self
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        delegate = self
    }
}

extension BrowserScrollView: BEScrollViewDelegate {
    func scrollView(
        _ scrollView: BEScrollView,
        handle update: BEScrollViewScrollUpdate,
        completion: (Bool) -> Void
    ) {
        let translation = update.translation(in: self)

        switch update.phase {
        case .began:
            beginCustomScroll(at: update.location(in: self))
        case .changed:
            updateCustomScroll(by: translation)
        case .ended:
            endCustomScroll(velocity: translation)
        case .cancelled:
            cancelCustomScroll()
        @unknown default:
            break
        }

        // Return true if the browser handled the scroll
        completion(true)
    }

    func parentScrollView(for scrollView: BEScrollView) -> BEScrollView? {
        // Return parent scroll view for nested scrolling coordination
        superview?.firstScrollViewAncestor()
    }
}
```

## Drag Interaction

### Browser Drag Support

`BEDragInteraction` provides asynchronous drag preparation, which is important
for browser engines that need to determine drag content from the DOM:

```swift
import BrowserEngineKit

final class BrowserDragHandler: NSObject, BEDragInteractionDelegate {
    func dragInteraction(
        _ interaction: UIDragInteraction,
        itemsForBeginning session: any UIDragSession
    ) -> [UIDragItem] {
        []
    }

    func dragInteraction(
        _ interaction: BEDragInteraction,
        prepare session: any UIDragSession,
        completion: () -> Bool
    ) {
        // Asynchronously determine what content to drag
        // (e.g., hit-test the DOM at the drag point)
        let dragItems = prepareDragItems(for: session)
        session.items.append(contentsOf: dragItems)
        _ = completion()
    }

    func dragInteraction(
        _ interaction: BEDragInteraction,
        itemsForAddingTo session: any UIDragSession,
        forTouchAt point: CGPoint,
        completion: ([UIDragItem]) -> Bool
    ) {
        // Add more items to an existing drag session
        _ = completion([])
    }
}

// Attach to a browser view
let dragInteraction = BEDragInteraction(delegate: dragHandler)
browserView.addInteraction(dragInteraction)
```

## Context Menus

### Deferred Context Menu Configuration

`BEContextMenuConfiguration` supports deferred configuration, useful when the
browser engine needs to asynchronously determine context menu content:

```swift
import BrowserEngineKit

func handleContextMenu(at point: CGPoint) {
    let config = BEContextMenuConfiguration()

    // Asynchronously determine context menu content from DOM
    determineContextContent(at: point) { uiConfig in
        // Fulfill with UIKit configuration when ready
        config.fulfill(using: uiConfig)
    }
}
```

## Content Filtering

### Web Content Filtering

`BEWebContentFilter` integrates with system content restrictions (Screen Time,
parental controls). It is available on iOS 26.2+:

```swift
import BrowserEngineKit

func shouldLoadURL(_ url: URL, completion: @escaping (Bool) -> Void) {
    guard BEWebContentFilter.shouldEvaluateURLs else {
        completion(true)
        return
    }

    let filter = BEWebContentFilter()
    filter.evaluateURL(url) { isRestricted, filterData in
        if isRestricted {
            // URL is blocked by content filter
            completion(false)
        } else {
            completion(true)
        }
    }
}

func requestFilterBypass(for url: URL) {
    let filter = BEWebContentFilter()
    filter.allow(url) { allowed, error in
        if allowed {
            // User/parent approved access
        }
    }
}
```

## Accessibility

### Remote Accessibility Elements

For cross-process accessibility, use `BEAccessibilityRemoteElement` and
`BEAccessibilityRemoteHostElement` to bridge the accessibility tree across
the host app and rendering extension:

```swift
import BrowserEngineKit

// In the rendering extension
let remoteElement = BEAccessibilityRemoteElement(
    identifier: "page-content-\(pageID)",
    hostPid: hostProcessID
)

// In the host app
let hostElement = BEAccessibilityRemoteHostElement(
    identifier: "page-content-\(pageID)",
    remotePid: renderingProcessID
)
hostElement.accessibilityContainer = browserContainerView
```

### Accessibility Container Types

Map HTML semantic elements to `BEAccessibilityContainerType`:

| HTML Element | Container Type |
|---|---|
| `<nav>`, `<header>` | `.landmark` |
| `<table>` | `.table` |
| `<ul>`, `<ol>` | `.list` |
| `<fieldset>` | `.fieldset` |
| `<dialog>` | `.dialog` |
| `<article>` | `.article` |
| `<dl>` | `.descriptionList` |
| `<iframe>` | `.frame` |

## Web App Manifests

Parse web app manifests for Progressive Web App support using
`BEWebAppManifest(jsonData:manifestURL:)`. Access `jsonData` and
`manifestURL` properties to extract app name, icons, theme color, etc.

## Download Management

### Monitoring Downloads with System Integration

`BEDownloadMonitor` integrates downloads with the system download UI and
Live Activities:

```swift
import BrowserEngineKit
import UniformTypeIdentifiers

func startDownload(from url: URL, to destination: URL) async throws {
    let progress = Progress(totalUnitCount: 100)

    guard let token = BEDownloadMonitor.createAccessToken() else {
        // Handle token creation failure
        return
    }

    let monitor = BEDownloadMonitor(
        sourceURL: url,
        destinationURL: destination,
        observedProgress: progress,
        liveActivityAccessToken: token
    )

    // Request a placeholder in the Downloads folder
    monitor.useDownloadsFolder(
        placeholderType: UTType.data
    ) { location in
        if let location {
            // System created a placeholder file
            // Move final file to location.url when complete
        }
    }

    // Begin monitoring - shows system download UI
    let location = try await monitor.beginMonitoring()

    // Update progress as download proceeds
    // progress.completedUnitCount = bytesReceived
}
```

### Resuming Interrupted Downloads

```swift
func resumeDownload(monitor: BEDownloadMonitor, placeholder: URL) async throws {
    try await monitor.resumeMonitoring(placeholderURL: placeholder)
    // Continue updating progress
}
```

## Process Manager Pattern

A complete process manager coordinates all extension lifecycles using an
actor for thread safety:

```swift
import BrowserEngineKit

actor BrowserProcessManager {
    private var contentProcesses: [String: WebContentProcess] = [:]
    private var networkProcess: NetworkingProcess?
    private var renderingProcess: RenderingProcess?

    func getOrLaunchNetworkProcess() async throws -> NetworkingProcess {
        if let existing = networkProcess { return existing }
        let process = try await NetworkingProcess(
            bundleIdentifier: nil
        ) { [weak self] in
            Task { await self?.handleNetworkInterruption() }
        }
        networkProcess = process
        return process
    }

    func getOrLaunchRenderingProcess() async throws -> RenderingProcess {
        if let existing = renderingProcess { return existing }
        let process = try await RenderingProcess(
            bundleIdentifier: nil
        ) { [weak self] in
            Task { await self?.handleRenderingInterruption() }
        }
        renderingProcess = process
        return process
    }

    func launchContentProcess(tabID: String) async throws -> WebContentProcess {
        let process = try await WebContentProcess(
            bundleIdentifier: nil
        ) { [weak self] in
            Task { await self?.handleContentInterruption(tabID: tabID) }
        }
        contentProcesses[tabID] = process
        return process
    }

    func closeTab(_ tabID: String) {
        contentProcesses[tabID]?.invalidate()
        contentProcesses.removeValue(forKey: tabID)
    }

    func bootstrapContentProcess(tabID: String) async throws {
        guard let content = contentProcesses[tabID] else { return }
        let network = try await getOrLaunchNetworkProcess()
        let rendering = try await getOrLaunchRenderingProcess()

        let networkProxy = NetworkingProxy(
            connection: try network.makeLibXPCConnection()
        )
        let renderProxy = RenderingProxy(
            connection: try rendering.makeLibXPCConnection()
        )

        let contentProxy = WebContentProxy(
            connection: try content.makeLibXPCConnection()
        )
        try await contentProxy.bootstrap(
            networkEndpoint: try await networkProxy.getEndpoint(),
            renderEndpoint: try await renderProxy.getEndpoint()
        )
    }

    private func handleNetworkInterruption() { networkProcess = nil }
    private func handleRenderingInterruption() { renderingProcess = nil }
    private func handleContentInterruption(tabID: String) {
        contentProcesses.removeValue(forKey: tabID)
    }

    func shutdownAll() {
        contentProcesses.values.forEach { $0.invalidate() }
        contentProcesses.removeAll()
        networkProcess?.invalidate()
        networkProcess = nil
        renderingProcess?.invalidate()
        renderingProcess = nil
    }
}
```

## File Access in Extensions

Web content extensions run in a restricted sandbox. To access user-selected
files, send a minimal bookmark from the host app. Resolving the bookmark in the
extension grants access for that extension process lifetime:

```swift
// Host app: create bookmark for a file URL
func sendFileToExtension(
    url: URL,
    via proxy: WebContentProxy
) async throws {
    let bookmarkData = try url.bookmarkData(
        options: .minimalBookmark,
        includingResourceValuesForKeys: nil,
        relativeTo: nil
    )
    try await proxy.sendBookmark(bookmarkData)
}

// Web content extension: resolve and access the file
func handleBookmark(_ data: Data) throws {
    var isStale = false
    let url = try URL(
        resolvingBookmarkData: data,
        options: .withoutUI,
        bookmarkDataIsStale: &isStale
    )
    defer { url.stopAccessingSecurityScopedResource() }

    let fileData = try Data(contentsOf: url)
    // Process the file content
}
```

## Memory Attribution

When the rendering extension consumes memory on behalf of a specific tab's
content, attribute that memory to the content extension to avoid the rendering
extension exceeding its memory limit:

```swift
// Requires entitlements:
// - com.apple.developer.memory.transfer_send on rendering extension
// - com.apple.developer.memory.transfer_accept on web content extension
//   (both with the host app's bundle identifier as value)

// The actual memory transfer is performed via Mach VM operations
// coordinated over the XPC connection between the extensions.
// See Apple's sample project for the full implementation.
```

This prevents the OS from terminating the rendering extension when it renders
large pages, because the memory is attributed to the per-tab content extension
instead.
