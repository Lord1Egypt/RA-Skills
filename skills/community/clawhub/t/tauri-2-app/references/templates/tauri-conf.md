# `src-tauri/tauri.conf.json`

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "{{ProductName}}",
  "version": "0.1.0",
  "identifier": "{{bundle.identifier}}",
  "build": {
    "beforeDevCommand": "npm run dev",
    "devUrl": "http://localhost:5173",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "app": {
    "security": {
      "csp": null
    },
    "windows": [
      {
        "label": "main",
        "title": "{{ProductName}}",
        "width": 1000,
        "height": 700,
        "minWidth": 600,
        "minHeight": 400,
        "center": true,
        "visible": true,
        "dragDropEnabled": true
      }
    ]
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "macOS": {
      "infoPlist": "./Info.plist",
      "entitlements": "./entitlements.plist",
      "minimumSystemVersion": "10.15",
      "hardenedRuntime": true
    },
    "windows": {
      "nsis": {
        "displayLanguageSelector": false,
        "installMode": "perMachine",
        "compression": "lzma"
      },
      "webviewInstallMode": {
        "type": "embedBootstrapper"
      }
    }
  }
}
```

## When the updater is enabled

Add (only if the user has generated a signing key with `npx tauri signer generate` AND has a manifest URL):

```json
"bundle": {
  // ... other fields
  "createUpdaterArtifacts": true
},
"plugins": {
  "updater": {
    "active": true,
    "endpoints": ["{{updater_manifest_url}}"],
    "dialog": false,
    "pubkey": "{{tauri_signing_pubkey}}"
  }
}
```

**Never** invent an `endpoints` URL or a `pubkey`. Both come from the user. The pubkey is a base64-encoded minisign public key produced by `tauri signer generate`. The endpoint is a JSON manifest the user controls (typical shape below).

## Updater manifest shape (the URL points at this)

```json
{
  "version": "1.0.0",
  "notes": "Initial release",
  "pub_date": "2026-01-15T10:30:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "{{full base64 contents of .sig file}}",
      "url": "{{cdn-url}}/{{ProductName}}_1.0.0_x64-setup.exe"
    },
    "darwin-aarch64": {
      "signature": "{{full base64 contents of .sig file}}",
      "url": "{{cdn-url}}/{{ProductName}}_1.0.0_aarch64.dmg"
    }
  }
}
```

## Why these defaults

- **`identifier`** is reverse-DNS (e.g. `com.example.myapp`) and **cannot change** after release — it's the OS-level identity for keychain entries, settings paths, notification permissions, and update channels. Always ask the user.
- **`csp: null`** is the Tauri default and works for many apps. If the WebView loads remote content, set an explicit CSP whitelisting `tauri://localhost` plus any trusted origins.
- **`windows[].devtools` is omitted** — Tauri's default is off in release. Adding `"devtools": true` ships an inspect-element surface to every user.
- **`bundle.targets: "all"`** lets `tauri build` pick the right installer format for the host OS (DMG on macOS, NSIS on Windows, AppImage/deb on Linux).
- **`macOS.hardenedRuntime: true`** is required for notarization. Pair with a minimal `entitlements.plist` listing **only** what the app uses.
- **`nsis.installMode: "perMachine"`** installs for all users on Windows. Use `"currentUser"` for per-user installs (no admin prompt, but registry keys live under `HKCU`).
- **`webviewInstallMode: "embedBootstrapper"`** ships the WebView2 bootstrapper inside the installer so users on stripped Windows builds without WebView2 can still install.

## Local config overlay

Tauri supports loading additional config files. Useful for local development with the updater disabled:

```bash
# src-tauri/tauri.local-no-updater.conf.json
{
  "$schema": "https://schema.tauri.app/config/2",
  "plugins": {
    "updater": {
      "active": false
    }
  }
}
```

Then build with:

```bash
npx @tauri-apps/cli build --config tauri.local-no-updater.conf.json
```

This avoids needing signing keys on every developer's machine.
