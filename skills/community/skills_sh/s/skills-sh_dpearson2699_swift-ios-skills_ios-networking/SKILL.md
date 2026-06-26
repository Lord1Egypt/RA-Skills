---
name: ios-networking
description: "Build, review, or improve networking code in iOS/macOS apps using URLSession with async/await, structured concurrency, and modern Swift patterns. Use when working with REST APIs, downloading files, uploading data, WebSocket connections, pagination, retry logic, request middleware, caching, background transfers, or network reachability monitoring. Also use when handling HTTP requests, API clients, network error handling, or data fetching in Swift apps."
---

# iOS Networking

Modern networking patterns for iOS 26+ using URLSession with async/await and
structured concurrency. All examples target Swift 6.3. No third-party
dependencies required -- URLSession covers the vast majority of networking
needs.

## Contents

- [Core URLSession async/await](#core-urlsession-asyncawait)
- [API Client Architecture](#api-client-architecture)
- [Error Handling](#error-handling)
- [Pagination](#pagination)
- [Network Reachability](#network-reachability)
- [Configuring URLSession](#configuring-urlsession)
- [App Transport Security (ATS)](#app-transport-security-ats)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Core URLSession async/await

URLSession gained native async/await overloads in iOS 15. Prefer these for
foreground data, upload, download, and streaming work. Background URLSession
transfers are the main exception: they still use task/delegate APIs so the
system can deliver events after suspension or relaunch.

### Data Requests

```swift
// Basic GET
let (data, response) = try await URLSession.shared.data(from: url)

// With a configured URLRequest
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.httpBody = try JSONEncoder().encode(payload)
request.timeoutInterval = 30
request.cachePolicy = .reloadIgnoringLocalCacheData

let (data, response) = try await URLSession.shared.data(for: request)
```

### Response Validation

Always validate the HTTP status code before decoding. URLSession does not
throw for 4xx/5xx responses -- it only throws for transport-level failures.

```swift
guard let httpResponse = response as? HTTPURLResponse else {
    throw NetworkError.invalidResponse
}

guard (200..<300).contains(httpResponse.statusCode) else {
    throw NetworkError.httpError(
        statusCode: httpResponse.statusCode,
        data: data
    )
}
```

### JSON Decoding with Codable

```swift
func fetch<T: Decodable>(_ type: T.Type, from url: URL) async throws -> T {
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          (200..<300).contains(httpResponse.statusCode) else {
        throw NetworkError.invalidResponse
    }

    let decoder = JSONDecoder()
    decoder.dateDecodingStrategy = .iso8601
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    return try decoder.decode(T.self, from: data)
}
```

### Downloads and Uploads

Use `download(for:)` for large files -- it streams to disk instead of
loading the entire payload into memory.

```swift
// Download to a temporary file
let (localURL, response) = try await URLSession.shared.download(for: request)

// Move or copy the returned temporary file promptly.
let destination = documentsDirectory.appendingPathComponent("file.zip")
try FileManager.default.moveItem(at: localURL, to: destination)
```

For delegate-based `URLSessionDownloadDelegate`, move or open the temporary
file before `urlSession(_:downloadTask:didFinishDownloadingTo:)` returns.

Background sessions are delegate-driven transfer queues. Use task creation
APIs such as `downloadTask(with:)` and file-backed `uploadTask(with:fromFile:)`,
then handle `URLSessionDelegate` / task delegate callbacks. Do not use async
convenience APIs such as `data(for:)`, `download(for:)`, or `upload(for:)` as
the durable background-session pattern.

```swift
// Upload data
let (data, response) = try await URLSession.shared.upload(for: request, from: bodyData)

// Upload from file
let (data, response) = try await URLSession.shared.upload(for: request, fromFile: fileURL)
```

### Streaming with AsyncBytes

Use `bytes(for:)` for streaming responses, progress tracking, or
line-delimited data (e.g., server-sent events).

```swift
let (bytes, response) = try await URLSession.shared.bytes(for: request)

for try await line in bytes.lines {
    // Process each line as it arrives (e.g., SSE stream)
    handleEvent(line)
}
```

## API Client Architecture

### Protocol-Based Client

Define a protocol for testability. This lets you swap implementations in
tests without mocking URLSession directly.

```swift
protocol APIClientProtocol: Sendable {
    func fetch<T: Decodable & Sendable>(
        _ type: T.Type,
        endpoint: Endpoint
    ) async throws -> T

    func send<T: Decodable & Sendable>(
        _ type: T.Type,
        endpoint: Endpoint,
        body: some Encodable & Sendable
    ) async throws -> T
}
```

```swift
struct Endpoint: Sendable {
    let path: String
    var method: String = "GET"
    var queryItems: [URLQueryItem] = []
    var headers: [String: String] = [:]

    func url(relativeTo baseURL: URL) -> URL {
        guard let components = URLComponents(
            url: baseURL.appendingPathComponent(path),
            resolvingAgainstBaseURL: true
        ) else {
            preconditionFailure("Invalid URL components for path: \(path)")
        }
        var mutableComponents = components
        if !queryItems.isEmpty {
            mutableComponents.queryItems = queryItems
        }
        guard let url = mutableComponents.url else {
            preconditionFailure("Failed to construct URL from components")
        }
        return url
    }
}
```

The client accepts a `baseURL`, optional custom `URLSession`, `JSONDecoder`,
and an array of `RequestMiddleware` interceptors. Each method builds a
`URLRequest` from the endpoint, applies middleware, executes the request,
validates the status code, and decodes the result. See
[references/urlsession-patterns.md](references/urlsession-patterns.md) for the complete `APIClient` implementation
with convenience methods, request builder, and test setup.

Production clients should receive an injected, configured `URLSession` instead
of calling `URLSession.shared` internally. Configure `URLSessionConfiguration`
with request/resource timeouts, cache policy or `URLCache`,
`waitsForConnectivity`, data-cost policy, and delegates when authentication
challenges, redirects, metrics, pinning, or background transfer handling matter.

### Lightweight Closure-Based Client

For apps using the MV pattern, use closure-based clients for testability
and SwiftUI preview support. See [references/lightweight-clients.md](references/lightweight-clients.md) for
the full pattern (struct of async closures, injected via init).

### Request Middleware / Interceptors

Middleware transforms requests before they are sent. Use this for
authentication, logging, analytics headers, and similar cross-cutting
concerns.

```swift
protocol RequestMiddleware: Sendable {
    func prepare(_ request: URLRequest) async throws -> URLRequest
}
```

```swift
struct AuthMiddleware: RequestMiddleware {
    let tokenProvider: @Sendable () async throws -> String

    func prepare(_ request: URLRequest) async throws -> URLRequest {
        var request = request
        let token = try await tokenProvider()
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        return request
    }
}
```

### Token Refresh Flow

Handle 401 responses by refreshing the token and retrying once.

```swift
func fetchWithTokenRefresh<T: Decodable & Sendable>(
    _ type: T.Type,
    endpoint: Endpoint,
    tokenStore: TokenStore
) async throws -> T {
    do {
        return try await fetch(type, endpoint: endpoint)
    } catch NetworkError.httpError(statusCode: 401, _) {
        try await tokenStore.refreshToken()
        return try await fetch(type, endpoint: endpoint)
    }
}
```

## Error Handling

### Structured Error Types

```swift
enum NetworkError: Error, Sendable {
    case invalidResponse
    case httpError(statusCode: Int, data: Data)
    case decodingFailed(Error)
    case noConnection
    case timedOut
    case cancelled

    /// Map a URLError to a typed NetworkError
    static func from(_ urlError: URLError) -> NetworkError {
        switch urlError.code {
        case .notConnectedToInternet, .networkConnectionLost:
            return .noConnection
        case .timedOut:
            return .timedOut
        case .cancelled:
            return .cancelled
        default:
            return .httpError(statusCode: -1, data: Data())
        }
    }
}
```

### Key URLError Cases

| URLError Code | Meaning | Action |
|---|---|---|
| `.notConnectedToInternet` | Device offline | Show offline UI, queue for retry |
| `.networkConnectionLost` | Connection dropped mid-request | Retry with backoff |
| `.timedOut` | Server did not respond in time | Retry once, then show error |
| `.cancelled` | Task was cancelled | No action needed; do not show error |
| `.cannotFindHost` | DNS failure | Check URL, show error |
| `.secureConnectionFailed` | TLS handshake failed | Check cert pinning, ATS config |
| `.userAuthenticationRequired` | Authentication required to access a resource | Trigger auth flow |

### Decoding Server Error Bodies

```swift
struct APIErrorResponse: Decodable, Sendable {
    let code: String
    let message: String
}

func decodeAPIError(from data: Data) -> APIErrorResponse? {
    try? JSONDecoder().decode(APIErrorResponse.self, from: data)
}

// Usage in catch block
catch NetworkError.httpError(let statusCode, let data) {
    if let apiError = decodeAPIError(from: data) {
        showError("Server error: \(apiError.message)")
    } else {
        showError("HTTP \(statusCode)")
    }
}
```

### Retry with Exponential Backoff

Use structured concurrency for retries. Respect task cancellation between
attempts. Skip retries for cancellation and 4xx client errors (except 429).

```swift
func withRetry<T: Sendable>(
    maxAttempts: Int = 3,
    initialDelay: Duration = .seconds(1),
    operation: @Sendable () async throws -> T
) async throws -> T {
    var lastError: Error?
    for attempt in 0..<maxAttempts {
        do {
            return try await operation()
        } catch {
            lastError = error
            if error is CancellationError { throw error }
            if case NetworkError.httpError(let code, _) = error,
               (400..<500).contains(code), code != 429 { throw error }
            if attempt < maxAttempts - 1 {
                try await Task.sleep(for: initialDelay * Int(pow(2.0, Double(attempt))))
            }
        }
    }
    throw lastError!
}
```

## Pagination

Build cursor-based or offset-based pagination with `AsyncSequence`.
Always check `Task.isCancelled` between pages. See
[references/urlsession-patterns.md](references/urlsession-patterns.md) for complete `CursorPaginator` and
offset-based implementations.

## Network Reachability

Use `NWPathMonitor` from the Network framework -- not third-party
Reachability libraries. On current OS targets it conforms to `AsyncSequence`;
wrap `pathUpdateHandler` only for compatibility or custom projections.

```swift
import Network

func observeNetworkStatus() async {
    let monitor = NWPathMonitor()

    for await path in monitor {
        handle(path.status)
    }
}
```

Check `path.isExpensive` (cellular) and `path.isConstrained` (Low Data
Mode) to adapt behavior (reduce image quality, skip prefetching).

Use Network.framework for low-level TCP, UDP, listeners, Bonjour, path
monitoring, or WebSocket protocol work -- not ordinary REST APIs. For iOS 26
`NetworkConnection<QUIC>`, `openStream(...)` and `inboundStreams(...)` are
async throwing APIs; see [references/network-framework.md#quic-multiplexed-streams](references/network-framework.md#quic-multiplexed-streams).

## Configuring URLSession

Create a configured session for production code. `URLSession.shared` is
acceptable only for simple, one-off requests.

```swift
let configuration = URLSessionConfiguration.default
configuration.timeoutIntervalForRequest = 30
configuration.timeoutIntervalForResource = 300
configuration.waitsForConnectivity = true
configuration.requestCachePolicy = .returnCacheDataElseLoad
configuration.httpAdditionalHeaders = [
    "Accept": "application/json",
    "Accept-Language": Locale.preferredLanguages.first ?? "en"
]

let session = URLSession(configuration: configuration)
```

`waitsForConnectivity = true` is valuable -- it makes the session wait for
a network path instead of failing immediately when offline. Combine with
`urlSession(_:taskIsWaitingForConnectivity:)` delegate callback for UI
feedback.

## App Transport Security (ATS)

ATS enforces HTTPS for all connections by default. Do not disable it.
ATS is URL Loading System policy, so it covers `URLSession` rather than making
lower-level `Network.framework` connections secure automatically. When using
Network.framework, configure secure TLS parameters and trust handling correctly
for that protocol stack.

Use domain-specific ATS exceptions only as a last resort.

**Rules:**
- Never set `NSAllowsArbitraryLoads` to `true` in production unless there is no narrower option.
- ATS exceptions require justification and may trigger additional App Store review.
- Use exception domains only for third-party servers you cannot upgrade to HTTPS.
- `NSAllowsLocalNetworking` is acceptable for local device communication (Bonjour, IoT).
- Prefer ATS `NSPinnedDomains` for declarative pinning when possible. Raw bytes
  from `SecKeyCopyExternalRepresentation` are not sufficient for SPKI pinning;
  correct SPKI pinning hashes Subject Public Key Info and belongs in `swift-security`.

## Common Mistakes

**DON'T:** Use `URLSession.shared` with custom configuration needs.
**DO:** Create a configured `URLSession` with appropriate timeouts, caching,
and delegate for production code.

**DON'T:** Force-unwrap `URL(string:)` with dynamic input.
**DO:** Use `URL(string:)` with proper error handling. Force-unwrap is
acceptable only for compile-time-constant strings.

**DON'T:** Decode JSON on the main thread for large payloads.
**DO:** Keep decoding on the calling context of the URLSession call, which
is off-main by default. Only hop to `@MainActor` to update UI state.

**DON'T:** Ignore cancellation in long-running network tasks.
**DO:** Check `Task.isCancelled` or call `try Task.checkCancellation()` in
loops (pagination, streaming, retry). Use `.task` in SwiftUI for automatic
cancellation.

**DON'T:** Use Alamofire or Moya when URLSession async/await handles the
need.
**DO:** Use URLSession directly. With async/await, the ergonomic gap that
justified third-party libraries no longer exists. Reserve third-party
libraries for genuinely missing features (e.g., image caching).

**DON'T:** Mock URLSession directly in tests.
**DO:** Use `URLProtocol` subclass for transport-level mocking, or use
protocol-based clients that accept a test double.

**DON'T:** Use `data(for:)` for large file downloads.
**DO:** Use `download(for:)` which streams to disk and avoids memory spikes.

**DON'T:** Fire network requests from `body` or view initializers.
**DO:** Use `.task` or `.task(id:)` to trigger network calls.

**DON'T:** Hardcode authentication tokens in requests.
**DO:** Inject tokens via middleware so they are centralized and refreshable.

**DON'T:** Ignore HTTP status codes and decode blindly.
**DO:** Validate status codes before decoding. A 200 with invalid JSON and
a 500 with an error body require different handling.

## Review Checklist

- [ ] Foreground transfers use async/await; background sessions use delegate/task APIs
- [ ] Error handling covers URLError cases (.notConnectedToInternet, .timedOut, .cancelled)
- [ ] Requests are cancellable (respect Task cancellation via `.task` modifier or stored Task references)
- [ ] Authentication tokens injected via middleware, not hardcoded
- [ ] Response HTTP status codes validated before decoding
- [ ] Large downloads use `download(for:)` not `data(for:)`
- [ ] Network calls happen off `@MainActor` (only UI updates on main)
- [ ] URLSession configured with appropriate timeouts and caching
- [ ] Production clients inject configured sessions instead of using `URLSession.shared`
- [ ] Background transfers use task/delegate APIs, not async convenience APIs
- [ ] Retry logic excludes cancellation and 4xx client errors
- [ ] Pagination checks `Task.isCancelled` between pages
- [ ] Sensitive tokens stored in Keychain (not UserDefaults or plain files)
- [ ] No force-unwrapped URLs from dynamic input
- [ ] Server error responses decoded and surfaced to users
- [ ] Network.framework code configures TLS/trust explicitly and keeps deep pinning work in `swift-security`
- [ ] `NetworkConnection<QUIC>` stream APIs are treated as async throwing
- [ ] Ensure network response model types conform to Sendable; use @MainActor for UI-updating completion paths

## References

- See [references/urlsession-patterns.md](references/urlsession-patterns.md) for complete API client
  implementation, multipart uploads, download progress, URLProtocol
  mocking, retry/backoff, certificate pinning, request logging, and
  pagination implementations.
- See [references/background-websocket.md](references/background-websocket.md) for background URLSession
  configuration, background downloads/uploads, WebSocket patterns with
  structured concurrency, and reconnection strategies.
- See [references/lightweight-clients.md](references/lightweight-clients.md) for the lightweight closure-based
  client pattern (struct of async closures, injected via init for testability
  and preview support).
- See [references/network-framework.md](references/network-framework.md) for Network.framework (NWConnection,
  NWListener, NWBrowser, NWPathMonitor) and low-level TCP/UDP/WebSocket patterns.
- See [references/file-storage-patterns.md](references/file-storage-patterns.md) for file system directory
  selection, FileProtectionType, backup exclusion, and storage pressure handling.
