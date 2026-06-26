# Vuact Configuration and Initialization

This document explains how to configure and initialize Vuact in a Vue 3 project.

## Prerequisites

- Vue version >= 3.5

## Install Dependencies

Install with pnpm (recommended):

```sh
pnpm add vuact vuact-dom
```

## Vite Configuration

This is the most common setup: use aliases to replace React-related dependencies with Vuact.

### Basic Configuration

```js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  resolve: {
    alias: {
      'react/jsx-runtime': 'vuact/jsx-runtime',
      'react/jsx-dev-runtime': 'vuact/jsx-dev-runtime',
      react: 'vuact',
      'react-dom/client': 'vuact-dom/client',
      'react-dom/server': 'vuact-dom/server',
      'react-dom': 'vuact-dom',
    },
  },
  optimizeDeps: {
    exclude: ['react', 'react-dom'],
  },
});
```

**Key notes**:
- `optimizeDeps.exclude` is critical. It prevents Vite from pre-bundling React-related deps, which would break the aliases.
- Without it, you may see:
  - Aliased `vuact` not updating automatically
  - Multiple copies of `vuact` being bundled
  - CJS modules importing Vuact ESM causing errors

### Support Both React JSX and Vue JSX

If you need to use both JSX flavors in the same project:

```js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';

export default defineConfig({
  resolve: {
    alias: {
      'react/jsx-runtime': 'vuact/jsx-runtime',
      'react/jsx-dev-runtime': 'vuact/jsx-dev-runtime',
      react: 'vuact',
      'react-dom/client': 'vuact-dom/client',
      'react-dom/server': 'vuact-dom/server',
      'react-dom': 'vuact-dom',
    },
  },
  plugins: [
    vue(),
    (() => {
      const reactJsxReg = [
        /^.+\.react\.(j|t)sx$/,
      ];
      const vueJsxPlugin = vueJsx({
        exclude: reactJsxReg,
      });
      const originConfig = vueJsxPlugin.config;
      vueJsxPlugin.config = function (config, env) {
        const result = originConfig(config, env);
        result.esbuild.include = [/\.ts$/, ...reactJsxReg];
        return result;
      };
      return vueJsxPlugin;
    })(),
  ],
  optimizeDeps: {
    exclude: ['react', 'react-dom'],
  },
});
```

**File naming convention**:
- `.react.tsx` / `.react.jsx`: handled by esbuild as React JSX
- Other `.tsx` / `.jsx`: handled by the `vueJsx` plugin as Vue JSX

### TypeScript Configuration

`tsconfig.json`：

```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react"
  }
}
```

This configuration only affects JSX handled by esbuild. It does not affect the `vueJsx` plugin.

## pnpm Overrides

Without relying on a bundler, you can replace packages directly in `package.json`:

```json
{
  "pnpm": {
    "overrides": {
      "react": "npm:vuact@^0.1.0",
      "react-dom": "npm:vuact-dom@^0.1.0"
    }
  }
}
```

This approach is more thorough: every `react` in the dependency tree will be replaced.

## Entry Initialization

Run the initialization code at the **very top** of your application entry file.

### Basic Initialization

```ts
import 'vuact/setup-scheduler';
import 'vuact-dom/register-dom-components';
```

**setup-scheduler**：
- Retrieves Vue's internal `flushJobs` function via a hack
- Enables emulation of APIs like `ReactDOM.flushSync`
- Must be imported before any other code runs

**register-dom-components**：
- Registers DOM components

### Enable setupRenderer (Optional, Recommended)

`setupRenderer` is used to support things like `input` change events.

Step 1: Replace `@vue/runtime-dom`

In `package.json`:

```json
{
  "pnpm": {
    "overrides": {
      "@vue/runtime-dom": "npm:@vuact/runtime-dom@3.5.28-vuact.2"
    }
  }
}
```

Step 2: Import it in the entry file

```ts
import 'vuact/setup-scheduler';
import 'vuact/setup-renderer';
import 'vuact-dom/register-dom-components';
```

What `setupRenderer` does:
- Extends Vue `rendererOptions`
- Partially aligns behavior with `react-dom`
- Enhances event handling
- Supports `input` change events, etc.

## Full Entry Example

```ts
import 'vuact/setup-scheduler';
import 'vuact/setup-renderer';
import 'vuact-dom/register-dom-components';
import { createApp } from 'vue';
import App from './App.vue';

createApp(App).mount('#app');
```

## Configuration Summary

| Item | Required | Notes |
|--------|----------|------|
| Install `vuact` + `vuact-dom` | Yes | Core dependencies |
| Vite alias | Yes | Replace `react` with `vuact` |
| `optimizeDeps.exclude` | Yes | Avoid pre-bundling issues |
| `setup-scheduler` | No | Recommended |
| `register-dom-components` | No | Recommended |
| `setupRenderer` | No | Recommended; requires replacing `@vuact/runtime-dom` |
