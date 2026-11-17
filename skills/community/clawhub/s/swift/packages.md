# Packages — SwiftPM, Manifests, Resources, Plugins

`Package.swift` is executable Swift, evaluated in a sandbox against a manifest API selected by its first line. That line is the most consequential in the file: `// swift-tools-version:` decides which APIs exist, which defaults apply, and whether newer features are even parseable by older toolchains.

## Manifest Shape That Ages Well

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Core",
    platforms: [.iOS(.v17), .macOS(.v14)],
    products: [.library(name: "Core", targets: ["Core"])],
    dependencies: [
        .package(url: "https://github.com/apple/swift-collections", from: "1.1.0")
    ],
    targets: [
        .target(
            name: "Core",
            dependencies: [.product(name: "Collections", package: "swift-collections")],
            resources: [.process("Resources")],
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
        .testTarget(name: "CoreTests", dependencies: ["Core"])
    ]
)
```

- `platforms:` sets the **minimum** the package supports; it does not pin consumers. Omitting it means the oldest version the toolchain supports, which is usually not what you tested.
- A dependency's module name rarely equals its package name — `.product(name:package:)` is required whenever they differ, and the error when you guess is unhelpfully generic.
- `swiftLanguageMode` per target is the ratchet handle for the Swift 6 migration (`swift6-migration.md`).

## Dependency Resolution

| Requirement | Resolves to | Use |
|---|---|---|
| `from: "1.2.0"` | `>=1.2.0 <2.0.0` | Default for libraries |
| `.upToNextMinor(from:)` | `>=1.2.0 <1.3.0` | Dependency whose minors have burned you |
| `exact:` | One version | Apps pinning a known-good build; poison in a library |
| `branch:`/`revision:` | A git ref | Local development only |
| `.package(path:)` | A directory | Local override during development |

- A package that depends on a **branch** cannot be consumed as a versioned dependency by anyone else. This is the most common "why can't they add my package" answer.
- `Package.resolved` belongs in git for apps and executables; for libraries it is ignored by consumers, so its value is only reproducible CI.
- A local `.package(path:)` overrides every version requirement in the graph — great for debugging a dependency, catastrophic if committed.
- Resolution conflicts are almost always one shared transitive dependency with incompatible majors. `swift package show-dependencies` prints the graph; the fix is upgrading whoever pinned old, not adding another pin.
- `unsafeFlags` in any target makes the package unusable as a versioned dependency. If you need a flag, gate it behind a trait, or move it to the consuming app.
- Recovery order when resolution goes strange: `swift package resolve`, then `swift package update`, then delete `.build`, then `swift package purge-cache` — in that order, stopping when it works.

## Resources

- Nothing in `Sources/` ships unless declared. `.process("Resources")` applies platform-appropriate handling (asset catalogs, storyboards, plist compaction) and flattens the directory structure; `.copy("Folder")` preserves the tree verbatim — the choice that matters when your code builds paths.
- `Bundle.module` is synthesized only for targets that declare resources; referencing it elsewhere fails to compile with a message that does not say so.
- `Bundle.main` inside a package is the **host app's** bundle, not the package's. Loading a package resource with `Bundle.main` works in tests and fails in the app.
- Test fixtures are resources too: declare them on the test target, load with `Bundle.module`.
- Localized resources go in `.lproj` directories plus `defaultLocalization:` on the package.

## Targets, Modules, and Layout

- One language per target. Mixing Objective-C and Swift in a single target is not supported: make a C/ObjC target with headers in `include/`, and depend on it from the Swift target (`interop.md`).
- A C target's public headers must live in `include/` (or the declared `publicHeadersPath`), or the module is empty and the import fails.
- `internal` is per-module, and each target is a module: splitting a target for build parallelism silently forces API decisions. The `package` access level (`swift >=5.9`) exists exactly for symbols shared across targets of one package but hidden from consumers.
- Executable targets need a `main.swift` or a `@main` type — not both, and `@main` is not allowed in `main.swift`.
- Conditional dependencies use `.product(..., condition: .when(platforms: [.linux]))` in the manifest; `#if os(...)` inside sources handles the code side.

## Plugins

- **Build tool plugins** run during the build and must declare their outputs; anything they write outside the declared output directory is dropped or fails the sandbox.
- **Command plugins** are invoked explicitly (`swift package my-plugin`) and need `--allow-writing-to-package-directory` to modify sources — a formatter plugin without that flag appears to run and change nothing.
- Plugins add their own dependency graph to the build. A plugin depending on swift-syntax pays the same build cost as a macro.
- Prebuilt binaries: `binaryTarget` with an XCFramework and an exact `checksum:`. The checksum changes on every release, so an automated bump must recompute it (`swift package compute-checksum`).

## Build and CI Behaviour

- `swift build -c release` enables whole-module optimization; debug builds do not, so all performance claims must come from release.
- `--disable-sandbox` is occasionally needed for plugins on macOS; needing it for a normal build means something is writing where it should not.
- Caches live in `.build/` (per package) and a shared toolchain cache. CI caches `.build` for speed; when a stale cache produces impossible errors, clearing it is the first move, not the last.
- Xcode and `swift build` use different derived paths and settings, so "works in Xcode, fails in `swift build`" usually means a resource, a flag, or a platform condition that only one of them applies. Reproduce in the failing one before changing code.
- `swift package diagnose-api-breaking-changes <baseline>` compares the public API against a git ref — the cheap gate that stops accidental major-version breaks.
