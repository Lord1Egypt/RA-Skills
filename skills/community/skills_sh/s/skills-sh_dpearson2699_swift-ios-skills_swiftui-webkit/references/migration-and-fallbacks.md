# Migration and Fallbacks

## Contents
- Migration goal
- Decision guide
- Migrating from `WKWebView` wrappers
- Incremental migration pattern
- When `SFSafariViewController` is still the right choice
- When `ASWebAuthenticationSession` is required
- When `WKWebView` remains justified
- Testing the migration
- Review checklist

## Migration goal

For SwiftUI apps targeting iOS 26+, the default for routine embedded web
content should be native SwiftUI WebKit APIs (`WebView`, `WebPage`) instead of
a custom `UIViewRepresentable` wrapper around `WKWebView`.

The goal is not "delete every `WKWebView` immediately." The goal is to move
routine embedded web content to the new native surface and keep legacy fallback
paths only where they are still justified.

## Decision guide

| Use case | Best default |
|---|---|
| Embedded app-owned web content in a SwiftUI screen | `WebView` + `WebPage` |
| OAuth or third-party sign-in | `ASWebAuthenticationSession` |
| External public site with Safari behavior on iOS/iPadOS | `SFSafariViewController` |
| External public site browse-out on macOS or visionOS | `openURL` / default browser |
| Back-deploying below iOS 26 or missing required capability | `WKWebView` fallback |

## Migrating from `WKWebView` wrappers

For SwiftUI apps targeting iOS 26+, start from `WebView` and `WebPage` for
routine embedded content instead of a `UIViewRepresentable` wrapper around
`WKWebView`.

Typical mapping:

| Older pattern | Modern default |
|---|---|
| `UIViewRepresentable` wrapper for `WKWebView` | `WebView(url:)` or `WebView(page)` |
| `WKNavigationDelegate` policy handling | `WebPage.NavigationDeciding` |
| KVO for `title`, `url`, or loading state | observable `WebPage` properties |
| `evaluateJavaScript` | `callJavaScript` |
| custom `WKWebViewConfiguration` usage | `WebPage.Configuration` |

Migrate first when the app is already SwiftUI-native and only kept `WKWebView`
because there was no native view before.

## Incremental migration pattern

A clean migration is usually screen-by-screen, not all-at-once.

### Start by separating page ownership from view ownership

If the current wrapper mixes:

- page state
- navigation policy
- JS calls
- UI embedding

split those concerns first. Once page logic is no longer trapped inside the
wrapper, moving to `WebPage` gets much easier.

### Move the simplest screens first

Best first migrations:

- static help center content
- app-owned account or legal pages
- embedded flows that only need URL loading, title, and progress

Leave these for later:

- auth flows
- highly customized legacy UIKit screens
- surfaces relying on a capability you have not yet mapped to the new API set

### Keep fallback boundaries explicit

Use availability and architecture boundaries instead of mixing two approaches in
one view body.

```swift
struct HelpCenterScreen: View {
    let page = WebPage()

    var body: some View {
        WebView(page)
            .task {
                try? await page.load(URLRequest(url: helpCenterURL))
            }
    }
}
```

If a fallback is still needed, isolate it in a separate type rather than
sprinkling `if #available` checks through the screen's core logic.

## When `SFSafariViewController` is still the right choice

Use `SFSafariViewController` on iOS and iPadOS when the app just needs to show
an external site with Safari behavior and does not need page-level control.

Good fits:

- help center article from a public website
- a legal page or blog post
- a temporary browse-out flow that should keep Safari chrome and reader behavior

Do not use `SFSafariViewController` when the app needs to:

- observe page state
- run JavaScript
- intercept navigation
- coordinate in-app page history

On macOS and visionOS, prefer platform default-browser behavior through
`openURL` instead of treating `SFSafariViewController` as the browse-out
surface.

## When `ASWebAuthenticationSession` is required

Use `ASWebAuthenticationSession` for OAuth and third-party sign-in.

This remains true even if the rest of the app uses `WebView` for embedded
content.

Do not replace auth sessions with embedded web views. The authentication skill
owns that flow because the product requirement is secure sign-in, not generic
web content.

## When `WKWebView` remains justified

A fallback `WKWebView` path can still make sense when:

- the app must back-deploy below iOS 26
- the codebase is still UIKit-first and not ready to move the surface into
  native SwiftUI WebKit APIs
- a required legacy-only WebKit capability is not yet available through the new
  SwiftUI-facing API surface
- a heavily customized existing surface would create churn without product value

When you keep `WKWebView`, treat it as a deliberate fallback, not the default
architecture for a modern iOS 26+ SwiftUI feature.

## Testing the migration

For each migrated screen, verify:

- title and URL state still update correctly
- JavaScript calls still reach the page when needed
- navigation policy behavior still matches product expectations
- loading and error states still render at the right time
- no auth flow accidentally moved from `ASWebAuthenticationSession` to an
  embedded view
- fallback `WKWebView` screens stay isolated instead of spreading wrapper logic
  back into new screens

## Review checklist

- [ ] New SwiftUI-native screens default to `WebView` and `WebPage`
- [ ] `SFSafariViewController` used only for browse-out Safari-style flows
- [ ] `ASWebAuthenticationSession` retained for OAuth and sign-in
- [ ] `WKWebView` kept only where back-deployment or capability gaps justify it
- [ ] Fallback paths isolated to dedicated wrapper types
- [ ] No new iOS 26+ feature starts from a `UIViewRepresentable` wrapper by default
