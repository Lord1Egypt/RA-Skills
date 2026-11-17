---
name: web-to-apk-research
description: "Gunakan saat membutuhuhkan kemampuan terkait web-to-apk-research (lihat When to Use di bawah)."v2.0.0: Rewrite from research note into actionable skill — decision matrix, executable PWA/Capacitor workflows, reference split. v1.0.0: Initial research"
metadata:
  openclaw:
    version: 2.0.0
author: pmuhammadagus-byte
license: MIT

---




# Web to APK — Termux Edition

## When to Use

User wants to convert a web app/website into an Android app, especially from Termux where Java, Gradle, and the Android SDK are NOT available locally. Triggers: "web to apk", "buat APK dari website", "jadikan web jadi aplikasi", "PWA", "installable web app", "Capacitor build".

## Decision Matrix — Ask First, Then Execute

| User need | Path | Effort |
|---|---|---|
| Install on own phone, works today | **A. PWA + WebAPK** | ~15 min |
| Shareable real `.apk` file | **B. Capacitor + GitHub Actions** | ~30 min |
| Play Store distribution | **C. TWA (Bubblewrap) + CI** | Medium |
| Full native control | D. Manual WebView app | High |

**ALWAYS confirm the target with the user before executing.** Default recommendation: Path A first (it is the foundation for B and C), then B if a shareable APK is required.

## Path A — PWA + WebAPK (default, do first)

1. Add `manifest.json` to the web project (name, short_name, start_url, display: standalone, icons 192/512).
2. Add `service-worker.js` (cache app shell; network-first for API calls).
3. Register the service worker in `index.html`.
4. Deploy to HTTPS hosting — GitHub Pages is free and provides HTTPS automatically.
5. Verify on Android Chrome: menu → "Install app" → icon appears in app drawer, fullscreen, offline-capable.

### manifest.json template

```json
{
  "name": "App Name",
  "short_name": "App",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

## Path B — Capacitor + GitHub Actions (real .apk)

1. `npm init @capacitor/app` in the project; `npx cap add android`.
2. Commit `.github/workflows/build-apk.yml` — Ubuntu runners already have Java/Gradle/Android SDK.
3. Push → wait 5-10 min → download APK from Actions artifacts.
4. Never attempt a local Gradle build in Termux — it will fail; CI is the build environment.

### Minimal workflow (build-apk.yml)

```yaml
name: build-apk
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci && npx cap sync android
      - run: cd android && ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with: { name: app-debug-apk, path: android/app/build/outputs/apk/debug/*.apk }
```

## Detailed Options Analysis

For the full comparison of all 5 options (PWA, Capacitor, TWA, manual WebView, Tauri Mobile) with pros/cons, read `references/options-analysis.md`.

## Environment Reality Check (Termux)

- ✅ Node.js, npm, git, curl, python — available
- ❌ Java/JDK, Gradle, Android SDK, Rust — NOT available locally → all native builds go through CI

## Red Flags — STOP

- Do not `pkg install openjdk`/gradle in Termux to build locally — broken toolchains waste hours; use CI
- Do not skip HTTPS — PWA install prompts and service workers require it (localhost excepted)
- Do not promise Play Store upload without Digital Asset Links setup (Path C)
- Tauri Mobile is experimental — never recommend it for production

## Version History

- **v1.0.0** — Initial research notes (5 options compared)
- **v2.0.0** — Actionable rewrite: decision matrix, executable workflows, progressive disclosure
