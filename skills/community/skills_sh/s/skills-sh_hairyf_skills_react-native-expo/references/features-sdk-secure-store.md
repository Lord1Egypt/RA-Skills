---
name: expo-secure-store
description: Store encrypted key-value pairs with expo-secure-store; optional biometric auth.
---

# expo-secure-store

**expo-secure-store** stores key-value pairs in the platform secure store (Android Keystore, iOS Keychain). Use for tokens, pins, or small secrets. Values are encrypted; avoid storing very large payloads (e.g. iOS historically ~2048 bytes).

## Usage

```bash
npx expo install expo-secure-store
```

```js
import * as SecureStore from 'expo-secure-store';

await SecureStore.setItemAsync('userToken', token);
const token = await SecureStore.getItemAsync('userToken');
await SecureStore.deleteItemAsync('userToken');

// Optional: require device unlock or biometric to read
await SecureStore.setItemAsync('pin', pin, {
  keychainAccessible: SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
});
const pin = await SecureStore.getItemAsync('pin', {
  requireAuthentication: true,
});
```

**Options:** `keychainAccessible` (iOS), `requireAuthentication` (prompt for biometric/device auth when reading). For Face ID you must set `faceIDPermission` via the config plugin.

## Key points

- **Config plugin:** Add to `plugins` to set `faceIDPermission` (iOS) and `configureAndroidBackup` (exclude SecureStore from Android Auto Backup so restored data is decryptable). Required for `requireAuthentication` in production.
- **Persistence:** On iOS, data can persist across app uninstalls (same bundle ID). On Android, data is removed on uninstall. Do not rely on iOS persistence for critical-only-once data.
- **Export compliance (iOS):** If using only expo-secure-store for encryption, set `ios.config.usesNonExemptEncryption: false` in app config to simplify App Store Connect export compliance.

<!--
Source references:
- https://docs.expo.dev/versions/latest/sdk/securestore/
-->
