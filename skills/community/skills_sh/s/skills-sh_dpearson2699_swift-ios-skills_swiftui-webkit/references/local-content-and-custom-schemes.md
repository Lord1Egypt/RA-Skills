# Local Content and Custom URL Schemes

## Contents
- When to use custom schemes
- Registering a scheme handler
- Returning responses and data
- Loading bundled content
- Cancellation behavior

## When to use custom schemes

Use `URLSchemeHandler` when the app owns the content source and needs WebKit to resolve resources under a custom scheme.

Good fits:
- bundled HTML, CSS, and JavaScript assets
- offline documentation
- app-owned rich content assembled on device

Do not use custom schemes for ordinary server-hosted pages that should just load over HTTPS.

## Registering a scheme handler

```swift
import Foundation
import WebKit

@MainActor
func makeDocsPage() -> WebPage {
    var configuration = WebPage.Configuration()
    configuration.urlSchemeHandlers[URLScheme("docs")!] = DocsSchemeHandler(bundle: .main)
    return WebPage(configuration: configuration)
}
```

If WebKit already owns a scheme, `URLScheme("https")` style registration does not work. Use a genuinely custom scheme.

## Returning responses and data

A handler replies with an async sequence of intermixed response and data values.

```swift
struct DocsSchemeHandler: URLSchemeHandler {
    let bundle: Bundle

    func reply(for request: URLRequest) -> some AsyncSequence<URLSchemeTaskResult> {
        AsyncStream { continuation in
            guard let url = request.url,
                  let fileURL = bundle.url(forResource: url.host, withExtension: "html", subdirectory: "Docs")
            else {
                continuation.finish()
                return
            }

            do {
                let data = try Data(contentsOf: fileURL)
                let response = URLResponse(
                    url: url,
                    mimeType: "text/html",
                    expectedContentLength: data.count,
                    textEncodingName: "utf-8"
                )
                continuation.yield(.response(response))
                continuation.yield(.data(data))
                continuation.finish()
            } catch {
                continuation.finish()
            }
        }
    }
}
```

Keep MIME type and encoding aligned with the actual content you serve.

## Loading bundled content

Once registered, load the custom URL like any other page.

```swift
let page = makeDocsPage()
for try await _ in page.load(URL(string: "docs://welcome")!) {
}

```

This works well when the HTML references other assets with the same custom scheme.

## Cancellation behavior

If WebKit no longer needs the resource, it cancels the task producing the async sequence. Treat cancellation as normal behavior when:
- the user navigates away
- the page reloads before the previous request completes
- the resource is no longer needed by the page

Do not build logic that assumes every scheme-handled request runs to completion.
