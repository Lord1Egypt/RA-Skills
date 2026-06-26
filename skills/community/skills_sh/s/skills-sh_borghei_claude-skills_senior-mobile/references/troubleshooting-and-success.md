# Troubleshooting & Success Criteria

Read this when debugging build, rendering, or store-submission problems, or validating a mobile project against the quality bar.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| App crashes on launch after adding a new dependency | Incompatible native module version or missing pod install / gradle sync | Run `npx pod-install` (iOS) or `cd android && ./gradlew clean` (Android). Verify dependency version compatibility in the changelog. |
| FlatList renders blank or flickers | Missing `keyExtractor`, unstable keys, or inline `renderItem` causing full re-renders | Add a stable `keyExtractor`, wrap `renderItem` in `useCallback`, and supply `getItemLayout` for fixed-height rows. |
| iOS build fails with "signing" error | Provisioning profile mismatch or expired certificate | Open Xcode > Signing & Capabilities, select the correct team and profile. Run `security find-identity -v -p codesigning` to verify certificates. |
| Android build OOM during dexing | Insufficient JVM heap for large projects | Add `org.gradle.jvmargs=-Xmx4096m` to `gradle.properties`. Enable `dexOptions { javaMaxHeapSize "4g" }` in `build.gradle`. |
| App Store rejection for missing privacy manifest | Apple requires PrivacyInfo.xcprivacy for apps using required reason APIs (UserDefaults, file timestamp, etc.) | Add a `PrivacyInfo.xcprivacy` file declaring each required reason API. Run `store_metadata_generator.py` to review privacy label guidance. |
| Slow cold start time (>3 seconds) | Too many synchronous operations on the main thread at launch, large bundle size, or unoptimized images | Defer non-critical initialization, lazy-load modules, compress images, and use `app_performance_analyzer.py` to identify bottlenecks. |
| Hot reload / fast refresh stops working | Syntax error in a module boundary, anonymous default export, or class component state | Check terminal for error messages, ensure named exports, and restart the Metro bundler or Flutter daemon with a cache clear. |

## Success Criteria

- **App startup time under 2 seconds** on cold launch (measured on mid-range devices, both iOS and Android).
- **Crash-free rate above 99.5%** across all supported OS versions, tracked via Crashlytics or Sentry.
- **Frame rendering at 60 fps** (16ms per frame) for scrolling lists and animations, with zero jank frames during typical user flows.
- **Bundle size under 50 MB** for the initial download (excluding on-demand resources), verified before each release.
- **Performance analyzer score of 75+** (Grade B or above) when running `app_performance_analyzer.py` against the project.
- **Zero critical issues** and fewer than 5 warnings reported by the performance analyzer before submitting to app stores.
- **App Store / Play Store approval on first submission** with complete metadata, correct privacy labels, and proper age rating, validated using `store_metadata_generator.py`.
