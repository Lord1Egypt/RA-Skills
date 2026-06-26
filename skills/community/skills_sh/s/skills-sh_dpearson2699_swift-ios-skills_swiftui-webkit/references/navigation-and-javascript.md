# Navigation and JavaScript

## Contents
- Navigation policy decisions
- Opening external links outside the embedded web view
- Calling JavaScript
- Passing arguments into JavaScript
- Coarse JS-to-native signaling

## Navigation policy decisions

Use `WebPage.NavigationDeciding` when the app needs to allow only owned URLs inside the embedded page.

```swift
import Observation
import WebKit

@Observable
@MainActor
final class ArticleNavigationDecider: WebPage.NavigationDeciding {
    var urlToOpenExternally: URL?

    func decidePolicy(
        for action: WebPage.NavigationAction,
        preferences: inout WebPage.NavigationPreferences
    ) async -> WKNavigationActionPolicy {
        guard let url = action.request.url else { return .allow }

        if url.host == "docs.example.com" {
            return .allow
        }

        urlToOpenExternally = url
        return .cancel
    }
}
```

This keeps app-owned pages embedded while still letting the app hand off external destinations.

## Opening external links outside the embedded web view

Bridge the decider back into SwiftUI with `openURL`.

```swift
struct ArticleView: View {
    @Environment(\.openURL) private var openURL
    @State private var decider: ArticleNavigationDecider
    @State private var page: WebPage

    init() {
        let decider = ArticleNavigationDecider()
        _decider = State(initialValue: decider)
        _page = State(initialValue: WebPage(configuration: .init(), navigationDecider: decider))
    }

    var body: some View {
        WebView(page)
            .onChange(of: decider.urlToOpenExternally) { _, url in
                guard let url else { return }
                openURL(url)
                decider.urlToOpenExternally = nil
            }
    }
}
```

Use this for external links, legal pages, or routes that should leave the embedded surface.

## Calling JavaScript

`callJavaScript` executes an async JavaScript function and returns an optional `Any`.
Pass only the function body. Do not wrap the script in `function foo() { ... }` or append a call expression.

```swift
let script = """
const headings = [...document.querySelectorAll('h1, h2')];
return headings.map(node => ({
    id: node.id,
    title: node.textContent?.trim()
}));
"""

let result = try await page.callJavaScript(script)
let headings = result as? [[String: Any]] ?? []
```

Cast immediately into the specific structure the app expects.
If the function body has no explicit return, the result is `nil`; if JavaScript explicitly returns `null`, handle `NSNull`.

## Passing arguments into JavaScript

Arguments become local variables inside the JavaScript function.
Use them for Swift-provided values instead of interpolating values into the script string. Supported values include numbers, strings, dates, and arrays, dictionaries, and optionals of those value types.

```swift
let topOffset = try await page.callJavaScript(
    "return document.getElementById(sectionID)?.getBoundingClientRect().top ?? null;",
    arguments: ["sectionID": selectedSectionID]
) as? Double
```

This is cleaner than interpolating untrusted values into the script string.

## Coarse JS-to-native signaling

The native SwiftUI WebKit API clearly supports Swift-to-JavaScript calls, but it does not expose an obvious direct equivalent to `WKScriptMessageHandler`.

For coarse event handoff, a custom navigation pattern can work:
- JavaScript navigates to a custom callback URL like `app-event://completed?id=123`
- `NavigationDeciding` intercepts the URL
- the decider extracts data and returns `.cancel`

Use this for simple completion or routing signals. Do not present it as a full structured messaging replacement for legacy `WKUserContentController` script handlers, and keep richer native/web messaging on a `WKWebView` fallback until the SwiftUI-facing API covers the need.
