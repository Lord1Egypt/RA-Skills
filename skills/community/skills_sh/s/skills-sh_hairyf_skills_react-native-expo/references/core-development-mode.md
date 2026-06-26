---
name: Development and production modes
description: How Expo runs in development vs production mode, __DEV__, and simulating production locally.
---

# Development and production modes

Expo projects run in either **development** or **production** mode. This affects performance, tooling, and how closely the run matches what users see.

## Usage

**Default (development mode):**

```bash
npx expo start
```

**Simulate production locally (no dev tools, minified JS):**

```bash
npx expo start --no-dev --minify
```

- `--no-dev` sets `__DEV__` to `false` in the bundle (disables dev warnings, red box, etc.).
- `--minify` minifies JS and strips comments/unused code.

Close and reopen the app after switching mode for the change to take effect.

## When to use each

| Goal | Mode |
|------|------|
| Day-to-day development, debugging, hot reload | Development |
| Testing performance or production-only bugs | Production (`--no-dev --minify`) |
| Store/standalone build behavior | Build with EAS Build or `npx expo run` (production bundle) |

**Important:** Development mode is slower. When measuring performance or tracking down production-only issues, always use `npx expo start --no-dev --minify` or a real production build.

## Key points

- **Development mode:** Live reload, dev menu, React DevTools, extra validations and warnings. App runs slower.
- **Production mode:** No dev tools, minified code, `__DEV__ === false`. Use for performance testing and catching production-only crashes.
- **Standalone/published app:** Always runs in production mode. EAS Update publishes production bundles; development builds still load JS in dev or prod depending on how you start the dev server.

<!--
Source references:
- https://docs.expo.dev/workflow/development-mode/
-->
