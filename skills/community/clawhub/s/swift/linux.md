# Linux and Server-Side Swift

The language is identical; the platform is not. What breaks a macOS-developed package on Linux is almost always one of four things: an Objective-C runtime dependency, a Foundation module split, a case-sensitive filesystem, or a missing runtime library in the container.

## What Simply Does Not Exist

- The Objective-C runtime: `@objc`, `@objcMembers`, `dynamic`, KVO, `NSSelectorFromString`, method swizzling, and Core Foundation bridging (`interop.md`).
- Apple frameworks: UIKit, AppKit, SwiftUI, Combine, Core Data, Security, os.log. `import os` fails; use swift-log.
- Some Foundation corners behave differently even where they exist — `NSKeyedArchiver`, locale and formatter behavior, and `URL` resource-value APIs are the usual suspects.

Guard with capability checks rather than OS checks: `#if canImport(FoundationNetworking)` says what you actually need, while `#if os(Linux)` breaks the day you add Windows or Android.

## The Foundation Module Split

On Linux, corelibs-Foundation is split, and the pieces are separate modules:

```swift
import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking   // URLSession, URLRequest
#endif
#if canImport(FoundationXML)
import FoundationXML          // XMLParser, XMLDocument
#endif
```

Missing these is the single most common "compiles on my Mac, fails in CI" error, and the diagnostic just says the symbol is unknown. Newer toolchains ship a Swift-native Foundation that narrows the behavioral gap between platforms, but the module split still governs what you must import.

## Filesystem and Environment

- Case-sensitive filesystem: `import MyModule` vs a directory named `mymodule`, or `Bundle.module.url(forResource: "Data")` against `data.json`, work on macOS and fail on Linux. This is the second most common CI-only failure.
- Path separators are the same, but `~` is not expanded by the shell in a Swift string — use `FileManager.default.homeDirectoryForCurrentUser`.
- No app bundle: `Bundle.main.resourcePath` points next to the executable. Package resources still work through `Bundle.module` (`packages.md`).
- Signals, process handling, and `Glibc` APIs come from `import Glibc`, mirrored by `import Darwin` on Apple platforms — wrap the difference in one small shim rather than at every call site.

## Building and Shipping

- Multi-stage container: build with the full `swift` image, run on a slim base. The runtime image needs the Swift runtime libraries plus whatever your code links (`libcurl`, `libxml2`, `zlib`, `ca-certificates` are the frequent ones) unless you link statically.
- `--static-swift-stdlib` embeds the Swift runtime so the runtime image needs no Swift toolchain. The fully static route (a musl-based Swift SDK, `swift >=6.0`) produces a binary that runs on a distroless or scratch base — the smallest and most portable option when your dependencies allow it.
- Cross-compiling from macOS to Linux uses installable Swift SDKs (`swift build --swift-sdk <id>`); it removes the "works on my Mac" gap earlier than CI does.
- Build in release for anything measured; debug on Linux is as unrepresentative as anywhere else.
- Backtraces: the runtime backtracer is enabled via the `SWIFT_BACKTRACE` environment variable and turns an opaque crash in a container into a symbolicated stack — set it in the image, not per-incident.

## Concurrency and Runtime Differences

- Swift concurrency works on Linux, and the cooperative pool is sized to the machine's cores. In a container that means the **host's** cores unless CPU limits are respected by the runtime — an over-subscribed pool in a 0.5-CPU container behaves badly, so set limits and verify.
- Dispatch is available, but there is no main runloop unless you create one: a command-line tool that fires async work and returns exits before the work runs. Use `await` in `@main`'s async entry point, not a semaphore (SKILL.md rule 4).
- There is no stable ABI on Linux: the standard library ships with your app, and toolchain upgrades require a rebuild — which also means no back-deployment constraints.
- Thread Sanitizer is available on Linux and is worth keeping in CI even after a Swift 6 migration.

## Server Practicalities

- Keep the HTTP framework at the edge and the domain logic in a plain, framework-free target: it stays testable on macOS and portable across framework versions.
- Logging goes through swift-log with a backend chosen by the executable, metrics through swift-metrics; libraries depend on the API packages only, never on a backend.
- Graceful shutdown means catching SIGTERM, cancelling the root task, and awaiting in-flight work — the container will SIGKILL after its grace period regardless.
- Foundation's `JSONDecoder` is portable and adequate; if it becomes the bottleneck, measure before swapping.
- CI matrix: build and test on both a Linux image and macOS if you claim both. A package that only runs its tests on macOS will break on Linux, on a schedule set by your users.
