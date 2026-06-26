---
name: react-native-update
description: Integrate and troubleshoot React Native Update OTA for Pushy and Cresc. Use when wiring react-native-update into React Native CLI, Expo prebuild, HarmonyOS, brownfield, monorepo, or mixed native apps; configuring update.json/appKey, Pushy/Cresc clients, UpdateProvider/useUpdate, iOS/Android/Harmony bundle loading, release baseline upload, checkStrategy/updateStrategy, canary/metaInfo flows, expo-updates conflicts, or OTA diagnostics.
---

# React Native Update / Pushy / Cresc

## Overview
Use this skill to get a project from "not integrated" to "hot update works in release builds".
Prioritize copy-paste-safe steps, smallest viable changes, and explicit verification checkpoints.

## Service routing
- Use **Pushy** for the China service: `pushy` CLI, `new Pushy(...)`, Pushy dashboard.
- Use **Cresc** for the global service: `cresc` CLI, `new Cresc(...)`, Cresc dashboard.
- Keep CLI, dashboard, app records, `update.json`, and JS client class on the same service. Do not mix `pushy createApp` with `new Cresc(...)`, or the reverse.
- If the service is unknown, infer from user wording, existing imports, registry/domain, or docs locale. If still unknown, implement the neutral structure and call out the one line the user must choose: `Pushy` vs `Cresc`.

## Workflow
1. Detect app root, package manager, React Native/Expo versions, service, and target platforms (`ios`, `android`, `harmony`).
2. Read `references/integration-playbook.md` before giving or applying steps.
3. Install `react-native-update` and ensure `react-native-update-cli` is available.
4. Configure native bundle loading for the detected platform and app shape:
   - iOS `RCTPushy.bundleURL()` or Expo auto integration.
   - Android `UpdateContext.getBundleUrl(...)` through `ReactHost`, `ReactNativeHost`, or custom instance manager.
   - Harmony package/provider/bundle-provider wiring.
   - Brownfield runtime hook instead of changing host inheritance.
5. Add a single `Pushy` or `Cresc` client outside the root component and wrap the real app tree with `UpdateProvider`.
6. Run `scripts/integration_doctor.sh <app-root>` and fix actionable misses.
7. Finish with release-build verification, baseline upload, and hot-update publish checks when the user wants an end-to-end integration.

## Guardrails
- Keep user code changes minimal and localized.
- Do not promise apply-update behavior in debug mode. `debug: true` can help check/download in development, but applying patches requires a release build.
- Warn about `expo-updates` conflict in Expo projects.
- Prefer `useUpdate()` methods and state over direct `client` calls. Only call the client directly for a clearly necessary low-level integration escape hatch, and explain why.
- Treat `checkUpdate()` as a trigger, not as the source of truth. Do not branch on its return value; read `updateInfo`/`lastError` from `useUpdate()` in `useEffect` or render state.
- Preserve existing app architecture; adapt snippets to current project style.
- If native files differ heavily (monorepo/mixed native), provide targeted patch guidance instead of broad rewrites.
- Treat JS/assets as OTA-safe. Native code, native config, native assets, pods, Gradle settings, HAR/AAR/XCFramework contents, and manifests require a new native release and baseline upload.

## Outputs to provide
- Minimal integration diff with exact files and snippets.
- Verification checklist: release build, baseline upload, check update, download, switch now/later, rollback behavior.
- Troubleshooting hints for common failures.
- Scenario examples when requested: class component root, custom UI, `metaInfo` rollout gates, QR/deep-link testing, brownfield integration, canary rollout.

## Resources
- Read `references/integration-playbook.md` before giving steps.
- Use `scripts/integration_doctor.sh` for quick project diagnosis.
