# Optimization


## Improve performance and reduce bundle size with runtime build only

As described in "[installation](../../installation##from-cdn-or-without-a-bundler)" section, Vue I18n offer the following two built ES modules for Bundler.

- message compiler + runtime: **`vue-i18n.esm-bundler.js`**
- runtime only: **`vue-i18n.runtime.esm-bundler.js`**

For bundler, it’s configured to bundle `vue-i18n.esm-bundler.js` by default. If you want to reduce the bundle size further, you can configure the bundler to use `vue-i18n.runtime.esm-bundler.js`, which is runtime only.

The use of this ES Module means that **all locale messages have to pre-compile to Message functions**.

:::danger NOTE
In the CSP environment, `vue-i18n.esm-bundler.js` does not work with compiler due to policy, so you need to use `vue-i18n.runtime.esm-bundler.js` in that environment as well.
:::

### vite

In vite, use `alias` option as below:

```js
import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueI18n from '@intlify/vite-plugin-vue-i18n'

export default defineConfig({
  // ...
  alias: {
    'vue-i18n': 'vue-i18n/dist/vue-i18n.runtime.esm-bundler.js'
  },
  plugins: [
    vue(),
    vueI18n({
      include: path.resolve(__dirname, './path/to/src/locales/**')
    })
  ],
  // ...
})
```

:::tip NOTE
If you are using Vite, you can do the same thing by specifying the option in the plugin provided officially.
:::

### webpack

In webpack, use `resolve.alias` as below:

```js
module.exports = {
  // ...
  resolve: {
    alias: {
      'vue-i18n': 'vue-i18n/dist/vue-i18n.runtime.esm-bundler.js'
    }
  },
  // ...
}
```

:::tip NOTE
For more information about pre-compiling locale messages, see `@intlify/vue-i18n-loader`
:::

### rollup

In rollup, use `@rollup/plugin-alias` as below:

```js
import path from 'path'
import alias from '@rollup/plugin-alias'

module.exports = {
  // ...
  plugins: [
    alias({
      entries: {
        'vue-i18n': path.resolve(__dirname, './node_modules/vue-i18n/dist/vue-i18n.runtime.esm-bundler.js')
      }
    })
  ],
  // ...
}
```

### Quasar CLI

No need to do anything. Quasar CLI takes care of the optimizations for you.

## Reduce bundle size with feature build flags

The `esm-bundler` builds now exposes global feature flags that can be overwritten at compile time:

- `__VUE_I18N_FULL_INSTALL__` (enable/disable, in addition to vue-i18n APIs, components and directives all fully support installation: `true`)
- `__VUE_I18N_LEGACY_API__` (enable/disable vue-i18n legacy style APIs support, default: `true`)
- `__INTLIFY_PROD_DEVTOOLS__` (enable/disable intlify-devtools and vue-devtools support in production, default: `false`)

The build will work without configuring these flags, however it is **strongly recommended** to properly configure them in order to get proper tree shaking in the final bundle. To configure these flags:

- webpack: use DefinePlugin
- Rollup: use @rollup/plugin-replace
- Vite: configured by default, but can be overwritten using the `define` option
- Quasar CLI: configured by default, but can be overwritten using quasar.conf.js > build > env option

:::tip NOTE
If you are using Vite, you can do the same thing by specifying the option in the plugin provided officially.

Also, if you are using the Vue CLI, you can use the officially provided plugin to optimize the settings in `vue.config.js`.
:::

:::tip NOTE
The replacement value **must be boolean literals** and cannot be strings, otherwise the bundler/minifier will not be able to properly evaluate the conditions.
:::

## Pre translations with extensions

You can pre-translation with vue-i18n-extensions.

About how to usage, see here.
