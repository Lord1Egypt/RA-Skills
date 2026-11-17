# Frontend configs: `vite.config.ts`, `tsconfig.json`, `package.json`, `index.html`

## `vite.config.ts`

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { readFileSync } from "fs";

// Read tauri.conf.json so the frontend has a single source of truth for version.
const tauriConfig = JSON.parse(
  readFileSync("./src-tauri/tauri.conf.json", "utf-8"),
);

// @ts-expect-error process is a Node global
const host = process.env.TAURI_DEV_HOST;

export default defineConfig({
  // Relative base so bundled HTML loads from tauri://localhost
  base: "./",

  plugins: [react()],

  // Don't hide Rust compiler errors
  clearScreen: false,

  server: {
    port: 5173,
    strictPort: true,                  // Tauri's devUrl pins 5173 — fail loudly if taken
    host: host || false,
    hmr: host
      ? { protocol: "ws", host, port: 1421 }
      : undefined,
    watch: {
      // Cargo handles src-tauri/ rebuilds; Vite ignoring it prevents HMR loops
      ignored: ["**/src-tauri/**"],
    },
  },

  esbuild: { jsx: "automatic" },

  define: {
    __APP_VERSION__: JSON.stringify(tauriConfig.version),
  },
});
```

Vanilla TypeScript (no React)? Drop the `react()` plugin and the `esbuild.jsx` line.

## `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "jsx": "react-jsx",

    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,

    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

`tsconfig.node.json` is a tiny companion for the `vite.config.ts` file itself:

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

## `package.json`

```json
{
  "name": "{{app-name}}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "tauri": "tauri",
    "tauri:dev": "tauri dev",
    "tauri:build": "tauri build",
    "clean": "rimraf node_modules/.vite dist",
    "test": "cd src-tauri && cargo test"
  },
  "dependencies": {
    "@tauri-apps/api": "<latest 2.x>",
    "@tauri-apps/plugin-dialog": "<latest 2.x>",
    "@tauri-apps/plugin-fs": "<latest 2.x>",
    "@tauri-apps/plugin-notification": "<latest 2.x>",
    "@tauri-apps/plugin-opener": "<latest 2.x>",
    "react": "<latest>",
    "react-dom": "<latest>"
  },
  "devDependencies": {
    "@tauri-apps/cli": "<latest 2.x>",
    "@types/react": "<latest>",
    "@types/react-dom": "<latest>",
    "@vitejs/plugin-react": "<latest>",
    "rimraf": "<latest>",
    "typescript": "<latest>",
    "vite": "<latest>"
  }
}
```

Resolve `<latest>` markers at scaffold time — never paste a literal version into a generated file.

## `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ProductName}}</title>

  <!-- Optional: anti-flash theme script. Runs BEFORE React mounts so the
       initial paint matches the user's preference. -->
  <script>
    (function() {
      const stored = localStorage.getItem("{{app-name}}-theme");
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const isDark = stored === "dark" || ((!stored || stored === "system") && prefersDark);
      if (isDark) document.documentElement.classList.add("dark");
    })();
  </script>

  <style>
    #app { opacity: 0; transition: opacity 0.15s ease-in; }
    #app.loaded { opacity: 1; }
  </style>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
```

```tsx
// src/main.tsx
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

const rootElement = document.getElementById("app");
if (rootElement) {
  createRoot(rootElement).render(<App />);
  requestAnimationFrame(() => rootElement.classList.add("loaded"));
}
```

## Why these choices

- **`base: './'`** — Tauri serves the bundled frontend from `tauri://localhost/`. Absolute paths (`base: '/'`) break asset URLs like `/assets/index.css` because they resolve against the protocol root.
- **`strictPort: true`** — Tauri's `devUrl` is `http://localhost:5173`. If Vite silently falls back to 5174, Tauri opens a blank window with no error.
- **`server.watch.ignored: ['**/src-tauri/**']`** — Cargo writes to `src-tauri/target/` constantly during dev. Without this, Vite's HMR triggers on every Cargo file write and reloads the frontend in a tight loop.
- **`clearScreen: false`** — Vite's default behavior clears the terminal on startup, hiding Rust compile errors. Tauri devs need both visible.
- **`isolatedModules: true`** — Required for Vite (which transpiles file-by-file, not whole-program).
- **`strict: true` + `noUnusedLocals` + `noUnusedParameters`** — Catches the kind of "I forgot to wire this up" mistakes that slip past code review.
- **Anti-flash script** — Without it, a dark-mode user sees a white flash before React's theme provider mounts. The script reads `localStorage` synchronously and applies the `dark` class before first paint.
- **Single `createRoot` call** — React 18+ doesn't tolerate multiple roots on the same node. Use one entry point.
