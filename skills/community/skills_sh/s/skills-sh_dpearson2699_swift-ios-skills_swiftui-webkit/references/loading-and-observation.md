# Loading and Observation

## Contents
- Simple `WebView(url:)`
- Controlled `WebPage` loading
- Observing progress and title
- Observing navigation events
- Ephemeral pages and custom user agents

## Simple `WebView(url:)`

Use `WebView(url:)` when the app only needs to display a URL and does not need explicit page control.

```swift
import SwiftUI
import WebKit

struct MarketingPageView: View {
    let url: URL

    var body: some View {
        WebView(url: url)
            .webViewBackForwardNavigationGestures(.enabled)
    }
}
```

This is the lowest-friction path for embedded content.

## Controlled `WebPage` loading

Create a `WebPage` when the app needs to drive loading itself.

Keep page ownership one-to-one with presentation: a `WebPage` can be bound to only one visible `WebView` at a time.

```swift
@Observable
@MainActor
final class ArticleModel {
    let page = WebPage()
    var lastError: String?

    func load(_ url: URL) async {
        do {
            for try await _ in page.load(URLRequest(url: url)) {
            }
        } catch {
            lastError = error.localizedDescription
        }
    }
}
```

```swift
struct ArticleDetailView: View {
    @State private var model = ArticleModel()
    let url: URL

    var body: some View {
        WebView(model.page)
            .task {
                await model.load(url)
            }
    }
}
```

You can also load:
- `for try await _ in page.load(url) { }`
- `for try await _ in page.load(html: htmlString, baseURL: baseURL) { }`
- `for try await _ in page.load(data, mimeType: "text/html", characterEncoding: "utf-8", baseURL: baseURL) { }`

Use the async sequence returned by a `load` call when you need to track that specific programmatic navigation. Use `page.navigations` for a broader stream covering both user and programmatic navigations.

## Observing progress and title

`WebPage` is observable, so SwiftUI can bind directly to its state.

```swift
struct ReaderView: View {
    @State private var page = WebPage()

    var body: some View {
        WebView(page)
            .navigationTitle(page.title ?? "Loading")
            .overlay(alignment: .top) {
                if page.isLoading {
                    ProgressView(value: page.estimatedProgress)
                        .padding()
                }
            }
            .task {
                do {
                    for try await _ in page.load(URLRequest(url: URL(string: "https://example.com/docs")!)) {
                    }
                } catch {
                    // Handle load failure.
                }
            }
    }
}
```

Useful properties:
- `title`
- `url`
- `isLoading`
- `estimatedProgress`
- `themeColor`
- `hasOnlySecureContent`
- `backForwardList`

## Observing navigation events

Use `currentNavigationEvent` for a lightweight current-state view. Use `navigations` to observe the full sequence of navigation events.

```swift
@MainActor
func observeNavigations(for page: WebPage) {
    Task {
        do {
            for try await event in page.navigations {
                switch event {
                case .startedProvisionalNavigation:
                    print("Navigation started")
                case .receivedServerRedirect:
                    print("Navigation redirected")
                case .committed:
                    print("Navigation committed")
                case .finished:
                    print("Navigation finished")
                @unknown default:
                    break
                }
            }
        } catch {
            print("Navigation failed: \(error)")
        }
    }
}
```

This is the right place to trigger follow-up work like parsing headings after a finished navigation. Treat thrown errors as normal navigation failures such as invalid URLs, provisional navigation failures, page closure, or web content process termination.

## Ephemeral pages and custom user agents

Use `WebPage.Configuration` when you need a nonpersistent page, custom user agent, or tighter loading rules.

```swift
@MainActor
func makeMetadataPage() -> WebPage {
    var configuration = WebPage.Configuration()
    configuration.loadsSubresources = false
    configuration.defaultNavigationPreferences.allowsContentJavaScript = false
    configuration.websiteDataStore = .nonPersistent()

    let page = WebPage(configuration: configuration)
    page.customUserAgent = "MetadataBot/1.0"
    return page
}
```

Use nonpersistent pages when you want an isolated web session or metadata fetch path without shared cookies or long-lived website data.
