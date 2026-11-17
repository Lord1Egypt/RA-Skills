# Setup — Swift

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Swift is safe by construction and unforgiving when you route around that safety. Write code that survives review: no silent force unwraps, no isolation holes, no error swallowed on the way out. Explain the failure mode, not just the fix.

## How To Load Preferences

1. Read `~/Clawic/data/swift/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `swift_language_mode: 6`, `build_tool: swiftpm`, `test_framework: swift-testing`, `target_platforms: apple`, `deployment_floor: none`, `force_unwrap_policy: tests-only`.
3. Read `~/Clawic/data/swift/memory.md` for prior context (their stack, recurring pain points). Absence is fine; proceed without comment.

Infer what the project already tells you before falling back to a default: `Package.swift` names the tools version, platforms, and language mode; the test target names the framework. What the repository states beats the table.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a language mode, build tool, test framework, target platform, OS floor, or unwrap policy → update the matching key in `~/Clawic/data/swift/config.yaml`.
- User expresses a habit or stance (formatter and rule set, access-control conventions, dependency appetite, diff vs full files, test-first) → record it under the relevant preference area in `~/Clawic/data/swift/memory.md`.
- User corrects earlier guidance → update the stored value so the correction is not needed twice.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their project shape (app, library, server), the frameworks in play, migration state, and recurring pain points — but only from what they actually reveal.
