# Troubleshooting NativeWind v4 in Expo

## Always start here

1) Restart Metro without cache:

```sh
npx expo start --clear
```

2) Confirm Tailwind CLI works *independently of NativeWind*:

```sh
npx tailwindcss --input ./global.css --output output.css
```

If the class you expect is not present in `output.css`, your issue is Tailwind config/content, not NativeWind runtime.

## Quick checks (90% of issues)

### “className not applying” / everything looks unstyled
- Confirm `global.css` exists.
- Confirm `metro.config.js` `withNativeWind(..., { input: "./global.css" })` points to it.
- Confirm the entry component imports it exactly once.
- Confirm `tailwind.config.js` `content` globs include all files that contain `className` strings:
  - `./App.{js,jsx,ts,tsx}`
  - `./app/**/*.{js,jsx,ts,tsx}` (Expo Router)
  - `./components/**/*.{js,jsx,ts,tsx}`
- Clear cache and restart.

### Web looks unstyled
- Confirm `app.json` sets:
  - `expo.web.bundler = "metro"`

## Verify the NativeWind install from inside the app

NativeWind exposes a helper:

```tsx
import { verifyInstallation } from "nativewind";

export default function App() {
  verifyInstallation(); // call inside component scope, not globally
  return null;
}
```

Remove it after you confirm the setup.

## Enable debug logs

Run your start command with `DEBUG=nativewind`:

```sh
DEBUG=nativewind npx expo start --clear
```

## Common React Native gotchas (looks like “NativeWind is broken”)

### Colour classes don’t “cascade”
React Native doesn’t cascade text colour from a `<View>` to a nested `<Text>`.
Move `text-*` classes onto the `<Text>` element.

### Conditional styles
React Native can behave oddly when styles appear/disappear. Prefer explicit style pairs (both light + dark) rather than only setting one side.

## Safe area utilities not working
- If you are **not** using Expo Router, ensure you wrap the root in `SafeAreaProvider`.
- If you **are** using Expo Router, do not add another provider; Router already wraps routes.

## Expo Router breaks after adding babel/metro config
If the Router stops finding routes, confirm:
- Babel still uses `babel-preset-expo` as the base preset.
- You restarted with `npx expo start --clear`.

If you see `EXPO_ROUTER_APP_ROOT` missing, consult Expo Router troubleshooting and ensure your entry point/babel config still matches Router expectations.
