---
name: EAS Build
description: Build Android and iOS binaries in the cloud with EAS Build; eas.json profiles, first build, and when to use development vs preview vs production.
---

# EAS Build

EAS Build is a hosted service that compiles your Expo/React Native project into Android and iOS binaries. It can manage credentials, support internal distribution, and integrate with EAS Update and EAS Submit.

## Usage

**Configure project for EAS (creates eas.json):**

```bash
eas build:configure
```

**Build for all platforms:**

```bash
eas build --platform all
```

**Build with a specific profile:**

```bash
eas build --platform ios --profile preview
eas build --profile development
```

**Example eas.json build profiles:**

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  }
}
```

**Development:** `developmentClient: true` → includes `expo-dev-client`; use for day-to-day dev. **Preview:** internal testing (e.g. ad hoc/enterprise on iOS, APK on Android). **Production:** store submission (AAB/IPA).

**iOS Simulator build:** in a profile:

```json
"ios": { "simulator": true }
```

## Key points

- **First-time setup:** install EAS CLI (`npm install -g eas-cli`), run `eas login`, then `eas build:configure`. For store builds you need Apple/Google developer accounts; EAS can generate or use your credentials.
- **When to use EAS Build:** production binaries, internal distribution, consistent builds across team/CI, managed signing. For deep native debugging, local builds (`npx expo run:android|ios`) or `eas build --local` are better.
- **Prebuild:** if **android** and **ios** are missing, EAS Build runs prebuild before compiling. To always use CNG, keep those directories out of the repo (e.g. in .gitignore) and let EAS generate them.
- **Updates:** EAS Build works with **expo-updates** and runtime versions; configure updates in app config and use channels/branches that match your build profiles.

<!--
Source references:
- https://docs.expo.dev/build/introduction/
- https://docs.expo.dev/build/setup/
- https://docs.expo.dev/build/eas-json/
-->
