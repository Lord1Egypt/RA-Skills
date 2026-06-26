# Expo setup templates (NativeWind v4)

> Use these as “known-good” templates. Always adapt `content` globs and CSS import paths to the repo.

## 0) New project shortcut (Expo)

If you are creating a brand new Expo project and want to skip manual setup, use:

```sh
npx rn-new --nativewind
```

## 1) Install dependencies

Minimum set:

- `nativewind`
- `tailwindcss` (dev dependency)
- `react-native-reanimated`
- `react-native-safe-area-context`
- `prettier-plugin-tailwindcss` (optional dev dependency)

Notes:
- Prefer `npx expo install` for Expo-managed native libraries if the repo uses Expo SDK pinning.
- If the repo already pins `react-native-reanimated` / `react-native-safe-area-context`, do not “fight” the existing versions unless you have a clear incompatibility.

## 2) tailwind.config.js

### Classic Expo (`App.tsx` entry)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  // NOTE: Update this to include the paths to all files that contain Nativewind classes.
  content: ["./App.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: { extend: {} },
  plugins: [],
};
```

### Expo Router (`app/` directory)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  // NOTE: Update this to include the paths to all files that contain Nativewind classes.
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: { extend: {} },
  plugins: [],
};
```

## 3) global.css

Create a single CSS entry file (commonly `global.css`) and add Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

If you choose a different filename/location, use that same relative path in BOTH `metro.config.js` `input` and your root import.

## 4) babel.config.js (Expo)

```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [["babel-preset-expo", { jsxImportSource: "nativewind" }], "nativewind/babel"],
  };
};
```

If the repo already has a `babel.config.js`, merge carefully:
- Keep `babel-preset-expo` as the base preset.
- Keep existing plugins/presets required by other tooling.
- Keep `nativewind/babel` in `presets` (not `plugins`).

## 5) metro.config.js (Expo)

```js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativeWind } = require("nativewind/metro");

const config = getDefaultConfig(__dirname);

module.exports = withNativeWind(config, { input: "./global.css" });
```

## 6) app.json (web support)

If the project targets web, set Metro as the web bundler:

```json
{
  "expo": {
    "web": {
      "bundler": "metro"
    }
  }
}
```

## 7) Import the CSS entry file

### Classic Expo (App.tsx)

```tsx
import "./global.css";
```

### Expo Router (app/_layout.tsx)

```tsx
import "../global.css";
```

Only import the CSS once at the top of the entry component.

## 8) TypeScript types (optional)

Create `nativewind-env.d.ts`:

```ts
/// <reference types="nativewind/types" />
```

Do **not** name it `nativewind.d.ts`, and avoid naming collisions like `app.d.ts` when an `/app` directory exists.
