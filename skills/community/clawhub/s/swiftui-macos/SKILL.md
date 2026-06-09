---
name: swiftui-macos
description: Expert SwiftUI guidance for macOS apps — covers writing and reviewing code with runtime-level understanding of observation, concurrency, performance, and platform integration. Use when user asks to "build a SwiftUI view", "review my SwiftUI code", "fix observation issues", "bridge AppKit", "architect state management", "debug view updates", or works on any macOS SwiftUI project — building features, reviewing existing code, debugging view updates or performance, fixing concurrency issues, architecting state management, bridging AppKit, or making design decisions. Do NOT use for iOS/iPadOS-only SwiftUI, UIKit bridging, or basic Swift language questions. Focuses on non-obvious traps and deep patterns, not basics.
license: MIT
compatibility: Requires macOS 26+ targeting and Swift 6.2 with strict concurrency. Best suited for Claude Code and environments with filesystem access to load references on demand.
metadata:
  author: kageroumado
  version: 1.0.0
---

Guide SwiftUI development for macOS apps. Whether writing new code or reviewing existing code, apply deep understanding of SwiftUI's runtime behavior — how the observation registrar dispatches, how the attribute graph diffs view trees, how actor isolation interacts with view lifecycles.

## How to Use

**Writing code**: Load relevant references before implementation. The patterns here prevent bugs that are expensive to find later — observation cascades, identity thrashing, concurrency overhead. When making architecture decisions (state ownership, view decomposition, AppKit bridging), consult the relevant reference for tradeoffs.

**Reviewing code**: Check each reference area systematically. Focus on genuine problems — observation inefficiencies, deprecated API, accessibility gaps, concurrency anti-patterns. Don't flag obvious issues or invent problems.

**Partial scope**: Load only what the task needs. Not every change requires all eight references.

## References

| Reference | Load when |
|---|---|
| `references/observation.md` | `@Observable`, `@State`, `ForEach`, data-driven views, `Observations {}` streams |
| `references/concurrency.md` | `Task`, `async`/`await`, actors, `DispatchQueue`, `AsyncStream`, scheduling decisions |
| `references/performance.md` | View composition, animations, gestures, large collections, `Canvas`, `TimelineView` |
| `references/views.md` | View decomposition, navigation, `.task(id:)`, preference keys, custom `Layout` |
| `references/data.md` | State architecture, SwiftData, environment injection, bindings, persistence |
| `references/platform.md` | `NSViewRepresentable`, `NSHostingView`, multi-window, AppKit bridging, window chrome |
| `references/api.md` | API choice, deprecated patterns, modern Swift/SwiftUI idioms |
| `references/accessibility.md` | VoiceOver, keyboard navigation, Dynamic Type, Reduce Motion |

## Principles

- Target **macOS 26+**, Swift 6.2 with strict concurrency and `@MainActor` default isolation.
- Check whether the project enables **`NonisolatedNonsendingByDefault`** (SE-0461) — this changes where `nonisolated` async functions execute. See `references/concurrency.md`.
- Prefer SwiftUI-native solutions. Use AppKit (`NSViewRepresentable`, `NSHostingView`, `NSWindow`) only when SwiftUI has no equivalent.
- **Understand the mechanism.** When suggesting a pattern, know *why* it works — what the observation registrar does, what the attribute graph diffing costs, what `_modify` vs `set` means for notification. Rules without understanding produce cargo-culted code.
- Do not introduce third-party frameworks without asking. Apple's open-source Swift packages (`swift-collections`, `swift-algorithms`, `swift-async-algorithms`) are exceptions — prefer them over reimplementing non-trivial data structures or algorithms. See `references/api.md`.

## Examples

**User**: "Review observation patterns in these sidebar views"
→ Load `references/observation.md`. Check each file for: state capture in ForEach, non-Equatable types on observed properties, missing `@ObservationIgnored` on caches, `_modify` vs `set` notification waste.

**User**: "I need to embed an NSCollectionView in SwiftUI"
→ Load `references/platform.md`. Apply `NSViewRepresentable` lifecycle, `Equatable` conformance for update gating, `Coordinator` for delegates.

**User**: "This view is re-rendering too much, help me debug it"
→ Load `references/performance.md` and `references/observation.md`. Check view identity (structural vs explicit), observation scope (are unrelated properties tracked in the same body?), `@State` vs `@Observable` for gesture-driven values.

## Review Output

Organize findings by file. For each issue:

1. File and relevant line(s).
2. The pattern being violated and *why it matters* at the runtime level.
3. Brief before/after code fix.

Skip clean files. End with a prioritized summary of the most impactful changes.
