# Specialization: Mobile App

Apply this guidance for iOS, Android, Flutter, React Native, and cross-platform mobile application designs.

## Phase 3 — Mobile Architecture Patterns

| Pattern | When to choose |
|---------|---------------|
| MVC | Simple apps, small team, quick prototype |
| MVVM | Data-binding heavy, testable ViewModels needed |
| MVI / Redux (Unidirectional) | Complex state, predictable state transitions, large team |
| Clean Architecture | Long-lived app, multiple teams, strict separation of concerns |
| Modular (feature modules) | Large app, multiple teams, independent feature delivery |

Platform-specific defaults:
- **iOS**: MVVM + Combine / SwiftUI, or UIKit + Coordinator
- **Android**: MVVM + Jetpack (ViewModel, LiveData/Flow, Room)
- **Flutter**: BLoC or Riverpod
- **React Native**: Redux Toolkit or Zustand

## Phase 5 — Critical Flows for Mobile

1. **App launch flow**: cold start → splash → auth check → deep link / home
2. **Auth flow**: login → token storage → refresh → logout
3. **Data sync flow**: local cache check → stale? → fetch remote → merge → display
4. **Offline flow**: no network → local data → queue mutations → sync on reconnect
5. **Push notification flow**: receive → parse → route → display or background action

## Phase 6 — Mobile Storage

| Data type | Storage option | Notes |
|-----------|---------------|-------|
| Structured app data | SQLite (Room, Core Data, sqflite) | |
| User preferences / settings | SharedPreferences / UserDefaults / Hive | |
| Secure credentials / tokens | Keychain (iOS) / Keystore (Android) | Never plain SharedPreferences |
| Media / files | App sandbox file system | |
| Large blobs / remote media | Object storage + local disk cache (with eviction) | |

## Phase 7 — Mobile-Specific Decision Points

| Decision | Options | Key differentiator |
|----------|---------|-------------------|
| Native vs cross-platform | Native iOS/Android vs Flutter vs React Native | Team language, performance requirement, platform API depth |
| State management | Local state vs global store | Scope of shared state across screens |
| Offline-first vs online-first | Cache-then-network vs network-only | Network reliability of target environment |
| Image loading | Platform SDKs vs Glide/Picasso/Kingfisher | Cache strategy and memory management |
| API: REST vs GraphQL | REST | GraphQL | Multiple query shapes needed → GraphQL |

## Phase 8 — Mobile Interface Design

- **API contract**: same REST/GraphQL standards as web backend, but also define:
  - Pagination (cursor-based recommended for feeds)
  - Partial response (field projection to reduce payload)
  - Offline mutation queue schema (local ID → server ID mapping)
- **Push notifications**: platform (APNs / FCM), payload schema, silent vs user-facing
- **Deep link schema**: URL scheme or universal links, parameter mapping to screens
- **App ↔ native module interface** (React Native / Flutter only): method channel contracts

## Phase 9 — Mobile Deployment

| Artifact | Notes |
|----------|-------|
| App binary | iOS: .ipa (App Store / TestFlight); Android: .aab (Play Store) / .apk |
| Signing | iOS: provisioning profile + certificate; Android: keystore |
| Distribution | TestFlight / Firebase App Distribution for beta; App Store / Play Store for production |
| OTA updates | React Native: CodePush; Flutter: not supported for native code |
| CI/CD | Fastlane + GitHub Actions; automate signing, build number bump, upload |

## Phase 10 — Mobile NFR

- **App size**: define target APK/IPA size; consider asset compression and code splitting
- **Startup time**: cold start < 2s on median device; measure on low-end device
- **Offline capability**: define which features work offline; which require network
- **Background execution**: battery impact; use Background Fetch / WorkManager constraints
- **Accessibility**: define WCAG 2.1 AA target; test with VoiceOver / TalkBack
- **Crash rate target**: define acceptable crash-free session rate (e.g., ≥ 99.5%)
- **Minimum OS version**: define and document; affects available APIs
