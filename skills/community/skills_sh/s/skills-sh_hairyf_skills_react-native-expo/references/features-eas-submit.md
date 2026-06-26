---
name: EAS Submit
description: Submit Android and iOS binaries to Google Play and App Store (TestFlight) with eas submit; eas.json submit profiles, CI usage.
---

# EAS Submit

EAS Submit uploads built binaries (AAB/IPA) to Google Play and App Store Connect (TestFlight). Use after `eas build` or with a local build path. Configure submit profiles in `eas.json`; use `--latest` or `--path` to choose the artifact.

## Usage

**Submit with latest build (by profile):**

```bash
eas submit --platform ios --profile production
eas submit --platform android --latest --non-interactive
```

**Submit a local binary:**

```bash
eas submit --platform ios --path ./build.ipa
eas submit --platform android --path ./app.aab
```

**eas.json submit profiles:**

```json
{
  "submit": {
    "production": {
      "android": {
        "track": "internal"
      },
      "ios": {
        "ascAppId": "your-app-store-connect-app-id"
      }
    }
  }
}
```

**Android:** First upload to Play Console may need to be done manually; EAS can use a Service Account for subsequent submissions. **iOS:** Set `ascAppId` (App Store Connect app id) for TestFlight; credentials are managed by EAS or your Apple account.

**CI / non-interactive:** Use `--non-interactive` and `--latest` (or `--path`) so the command does not prompt. Ensure the build exists for the chosen profile and platform.

## Key Points

- Default submit profile is `production` if not specified; use `--profile <name>` to pick another.
- Submit profiles can `extends` another profile. Use multiple profiles for different tracks or TestFlight vs production.
- For debugging submit config: run `eas submit` interactively once, or inspect `eas.json` and [Expo Submit docs](https://docs.expo.dev/submit/introduction/).

<!--
Source references:
- https://docs.expo.dev/submit/introduction/
- https://docs.expo.dev/submit/eas-json/
- https://docs.expo.dev/eas/json
-->
