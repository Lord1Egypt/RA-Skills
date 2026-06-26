---
name: Xcode
description: Avoid common Xcode mistakes — signing issues, build settings traps, and cache corruption fixes.
metadata: {"clawdbot":{"emoji":"🔨","requires":{"bins":["xcodebuild"]},"os":["darwin"]}}
---

## Signing Issues
- "Automatic" signing still needs team selected — set in Signing & Capabilities
- Provisioning profile mismatch — bundle ID must match exactly, including case
- "No signing certificate" — open Keychain, check certificate is valid and not expired
- Device not registered — add UDID in developer portal, regenerate profile
- CI/CD needs manual signing — automatic doesn't work in headless builds

## Derived Data Corruption
- Random build failures after Xcode update — delete `~/Library/Developer/Xcode/DerivedData`
- "Module not found" but it exists — clean Derived Data, restart Xcode
- Stale cache symptoms — builds work, then fail, then work again
- `xcodebuild clean` not enough — sometimes must delete DerivedData manually

## Build Settings Hierarchy
- Project → Target → xcconfig → command line — later overrides earlier
- `$(inherited)` to append not replace — forgetting it removes parent settings
- `SWIFT_ACTIVE_COMPILATION_CONDITIONS` for Swift flags — not `OTHER_SWIFT_FLAGS`
- `GCC_PREPROCESSOR_DEFINITIONS` for Obj-C — add to existing, don't replace

## Archive vs Build
- Archive uses Release config by default — build uses Debug
- "Works in simulator, fails in archive" — check Release build settings
- Archive requires valid signing — build doesn't for simulator
- `SKIP_INSTALL = YES` for frameworks — or archive includes them incorrectly

## Capabilities and Entitlements
- Capability in Xcode must match entitlements file — out of sync causes crashes
- Push notifications need both — App ID capability AND provisioning profile
- Associated domains needs apple-app-site-association file — hosted on your server
- Keychain sharing needs explicit group — default is just your app

## Dependencies
- SPM and CocoaPods can conflict — watch for duplicate symbols
- Pod update vs install — `install` uses Podfile.lock, `update` ignores it
- "Framework not found" — check Framework Search Paths, embed vs link
- SPM package resolution fails — delete Package.resolved, reset package caches

## Common Fixes
- Build fails with no clear error — check Report Navigator for details
- Simulator stuck — `xcrun simctl shutdown all`, then `xcrun simctl erase all`
- Indexing stuck — delete Index folder in DerivedData
- Autocomplete broken — restart Xcode, if persists delete DerivedData

## CLI Builds
- `xcodebuild -showBuildSettings` to debug — see resolved values
- `-allowProvisioningUpdates` for CI with auto-signing — needs keychain access
- `-destination` must be exact — `platform=iOS Simulator,name=iPhone 15`
- `xcrun altool` deprecated — use `xcrun notarytool` for notarization
