---
name: core-setup
description: Naive-ui installation, auto-import setup, and global configuration
---

# Installation & Setup

## Installation

```bash
pnpm add naive-ui
```

## Basic Usage

> **Warning (UMD):** There is a self-closing bug in the UMD version of naive-ui. Please close tags explicitly like `<n-input></n-input>`.
> **Warning (Experimental):** Experimental features (like `TuSimple` theme) are explicitly unstable. Use them only if absolutely necessary and be prepared to follow API breaking changes.

### Full Import (Not Recommended)

```ts
import { createApp } from 'vue'
import naive from 'naive-ui'
import App from './App.vue'

const app = createApp(App)
app.use(naive)
app.mount('#app')
```

### Auto Import (Recommended)

Use `unplugin-vue-components` and `unplugin-auto-import`:

```bash
npm install -D unplugin-vue-components unplugin-auto-import
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import AutoImport from 'unplugin-auto-import/vite'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [NaiveUiResolver()]
    }),
    AutoImport({
      imports: [
        'vue',
        {
          'naive-ui': [
            'useDialog',
            'useMessage',
            'useNotification',
            'useLoadingBar',
            'useThemeVars'
          ]
        }
      ],
      dts: true  // Generate TypeScript declarations
    })
  ]
})
```

### Global Config Provider

Wrap your app with `n-config-provider`:

```vue
<template>
  <n-config-provider
    :theme="theme"
    :theme-overrides="themeOverrides"
    :locale="locale"
    :date-locale="dateLocale"
    :hljs="hljs"
    inline-theme-disabled
  >
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <app />
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { darkTheme, lightTheme, zhCN, dateZhCN } from 'naive-ui'
import hljs from 'highlight.js/lib/core'

const isDark = useDark()
const theme = computed(() => isDark.value ? darkTheme : lightTheme)

const themeOverrides = {
  common: {
    primaryColor: '#2080f0',
    borderRadius: '6px'
  }
}

const locale = zhCN
const dateLocale = dateZhCN
</script>
```

## TypeScript Support

All components are fully typed. Import types when needed:

```ts
import type {
  DataTableColumns,
  DataTableRowKey,
  FormInst,
  FormRules,
  SelectOption,
  TreeOption,
  UploadFileInfo,
  MenuOption,
  TabsInst
} from 'naive-ui'
```

## Nuxt 3 Setup

```ts
// plugins/naive-ui.ts
import { setup } from '@css-render/vue3-ssr'
import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin((nuxtApp) => {
  if (process.server) {
    const { collect } = setup(nuxtApp.vueApp)
    const originalRenderToString = renderToString
    renderToString = async (input, context) => {
      const html = await originalRenderToString(input, context)
      return html + collect()
    }
  }
})
```

```vue

<template>
  <client-only>
    <n-config-provider :theme-overrides="themeOverrides">
      <nuxt-page />
    </n-config-provider>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </client-only>
</template>
```


