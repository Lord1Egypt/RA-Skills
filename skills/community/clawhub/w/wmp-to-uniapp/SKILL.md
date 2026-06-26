---
name: wmp-to-uniapp
description:  Convert native WeChat Mini Program projects into uni-app + Vue3 + TypeScript cross-platform projects.
---

# WeChat Mini Program → uni-app + Vue3 + TypeScript Conversion

Convert a native WeChat Mini Program project into a complete, runnable uni-app + Vue3 + TypeScript project.

## Triggers

Triggers when user mentions converting, migrating, or porting a WeChat miniprogram / 微信小程序 to uni-app, or provides a miniprogram project path and asks to transform it. Also triggers for related tasks like analyzing a miniprogram project structure for conversion,or generating uni-app code from WXML/WXSS/JS source files.

## Conversion Flow

```
1. Analyze source project
       ↓
2. Initialize uni-app project skeleton (TypeScript)
       ↓
3. Convert config (app.json → pages.json + manifest.json)
       ↓
4. Convert pages (wxml/js/wxss → Vue3 SFC, <script setup lang="ts">)
       ↓
5. Convert components (Component() → Vue3 <script setup lang="ts">)
       ↓
6. Convert utils & API calls (wx.* → uni.*, .js → .ts)
       ↓
7. Finalize & verify
```

**Before starting**, ask the user:
- Source project root path
- Target output directory (default: `./output-uni-app` or adjacent to source)
- Whether to keep WeChat-only features (conditional compilation) or drop them

---

## Step 1: Analyze Source Project

Read these files to understand the project:

1. **`app.json`** — pages list, subPackages, tabBar, window config, globalStyle, usingComponents
2. **`project.config.json`** — appid, compile settings (reference only)
3. **`package.json`** (if exists) — npm dependencies, identify which can carry over
4. **All page directories** under `pages/` — each needs 1 .wxml + 1 .js + 1 .wxss (1 .json optional)
5. **All component directories** under `components/` or custom paths
6. **`utils/`** and any custom JS modules (utils, api wrappers, configs)
7. **`app.js`** — global logic, globalData, onLaunch/onShow lifecycle
8. **`app.wxss`** — global styles

**Output a structured catalog:**

```
Pages (N):  pages/index/index, pages/detail/detail, ...
Components (M):  components/star/star, components/list-item/list-item, ...
Utils (K):  utils/request.js, utils/util.js, utils/config.js, ...
SubPackages (optional):  pkgA/pages/...
TabBar:  yes/no, N tabs
Dependencies:  [list from package.json]
Cloud:  yes/no (wx.cloud usage detected)
Custom processing (WXS, plugins, workers):  [list]
```

This catalog drives all subsequent steps.

---

## Step 2: Initialize uni-app Project Skeleton (TypeScript)

Create an empty uni-app project with the standard structure:

```
<output-dir>/
├── pages/
├── components/
├── utils/
├── types/
│   └── global.d.ts
├── static/
│   └── images/
├── App.vue
├── main.ts
├── manifest.json
├── pages.json
├── tsconfig.json
└── uni.scss
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "esnext",
    "moduleResolution": "node",
    "strict": true,
    "jsx": "preserve",
    "sourceMap": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "lib": ["esnext", "dom"],
    "types": ["@dcloudio/types"],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    },
    "skipLibCheck": true
  },
  "include": [
    "*.vue",
    "**/*.ts",
    "**/*.tsx",
    "**/*.vue"
  ],
  "exclude": ["node_modules", "unpackage", "dist"]
}
```

### types/global.d.ts

```ts
/// <reference types="@dcloudio/types" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Extend App global properties
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $globalData: Record<string, any>
  }
}

export {}
```

### App.vue

```vue
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  onLaunch() {
    console.log('App Launch')
  },
  onShow() {
    console.log('App Show')
  },
  onHide() {
    console.log('App Hide')
  }
})
</script>

<style>
/* Global styles from original app.wxss go here */
</style>
```

### main.ts

```ts
import { createSSRApp } from 'vue'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  return { app }
}
```

### uni.scss

```scss
/* uni-app global style variables */
@import '@/uni.scss';
```

### manifest.json

Generate minimal manifest with WeChat mini program appid from `project.config.json`:

```json
{
  "name": "",
  "appid": "",
  "description": "",
  "versionName": "1.0.0",
  "versionCode": "100",
  "transformPx": false,
  "mp-weixin": {
    "appid": "<from-project.config.json>",
    "setting": {
      "urlCheck": false
    },
    "usingComponents": true
  }
}
```

---

## Step 3: Convert Configuration Files

### 3.1 app.json → pages.json

Map each field using the reference table in [mappings.md](references/mappings.md#1-配置文件映射-appjson--pagesjsonmanifestjson).

**Key rules:**
- `pages` array: first entry is the home page. Convert path `pages/index/index` to `pages/index/index`.
- `subPackages`: preserve structure, prefix paths correctly.
- `window` → `globalStyle`: flatten all `window.*` fields into `globalStyle.*`.
- `tabBar`: copy verbatim (uni-app compatible). Append `.selectedIconPath` entries if missing.
- **Per-page config**: each page's `.json` file → `pages[n].style`. If page has `usingComponents`, map to page-level component registration.

### 3.2 app.js → App.vue

- `App({ onLaunch, onShow, onHide, globalData, ... })` → `App.vue <script lang="ts">` with equivalent lifecycle methods using `defineComponent`.
- `globalData` → typed reactive object exported from a shared module `utils/globalData.ts`, or use `getApp().globalData`.
- Any initial API calls in `onLaunch` carry over.

### 3.3 app.wxss → App.vue `<style>`

- Copy content into `App.vue` `<style>` block (no scoped).
- Convert WXSS-only syntax:
  - Remove `@import` statements, convert to CSS `@import` in `<style>`.
  - Keep `rpx` as-is (uni-app supports it).

---

## Step 4: Convert Pages (WXML/JS/WXSS → Vue SFC + TypeScript)

For each page `pages/foo/foo.{wxml,js,wxss,json}`:

### 4.1 Create `pages/foo/foo.vue`

Template structure:

```vue
<template>
  <view class="page-foo">
    <!-- converted WXML content -->
  </view>
</template>

<script setup lang="ts">
// converted JS content, fully typed
</script>

<style scoped>
/* converted WXSS content */
</style>
```

### 4.2 WXML → `<template>`

Use mappings from [mappings.md](references/mappings.md#3-wxml--vue-template-语法映射):

- `wx:if` → `v-if`; `wx:else` → `v-else`; `wx:elif` → `v-else-if`
- `wx:for="{{list}}"` → `v-for="(item, index) in list"`; `wx:key="id"` → `:key="item.id"`
- `bind:tap="fn"` → `@tap="fn"`; `catch:tap="fn"` → `@tap.stop="fn"`
- `hidden="{{v}}"` → **`v-show="!v"`** (semantic inversion)
- `data-xxx="{{v}}"` → `:data-xxx="v"` or `data-xxx="v"` for static strings
- `<block>` → `<template>` or remove (Vue fragment behavior)
- `{{ }}` interpolation → keep as `{{ }}` (same)
- `import src` / `include src` → Vue component imports

### 4.3 JS → `<script setup lang="ts">`

Convert `Page({ data, onLoad, methods, ... })`:

```js
// Source (page.js) — JavaScript, untyped:
Page({
  data: {
    count: 0,
    list: [],
    userInfo: null,
    loading: false
  },
  onLoad(options) {
    this.fetchData()
  },
  onShow() { /* ... */ },
  onPullDownRefresh() {
    this.fetchData()
  },
  increment() {
    this.setData({ count: this.data.count + 1 })
  },
  fetchData() {
    this.setData({ loading: true })
    wx.request({
      url: 'https://api.example.com/list',
      success: (res) => {
        this.setData({ list: res.data, loading: false })
      }
    })
  }
})
```

```vue
<!-- Target (page.vue) — TypeScript -->
<script setup lang="ts">
import { ref, type Ref } from 'vue'

// --- Type definitions ---
interface ListItem {
  id: number
  title: string
  coverUrl: string
  createdAt: string
}

interface UserInfo {
  nickName: string
  avatarUrl: string
}

// --- Reactive state (typed) ---
const count = ref<number>(0)
const list = ref<ListItem[]>([])
const userInfo = ref<UserInfo | null>(null)
const loading = ref<boolean>(false)

// --- Lifecycle ---
onLoad((options?: AnyObject) => {
  fetchData()
})

onShow(() => {
  // ...
})

onPullDownRefresh(() => {
  fetchData()
})

// --- Methods ---
const increment = (): void => {
  count.value++
}

const fetchData = async (): Promise<void> => {
  loading.value = true
  try {
    const res = await uni.request<ListItem[]>({
      url: 'https://api.example.com/list'
    })
    list.value = res.data as ListItem[]
  } catch (err) {
    uni.showToast({ title: '加载失败', icon: 'none' })
    console.error('fetchData error:', err)
  } finally {
    loading.value = false
    uni.stopPullDownRefresh()
  }
}
</script>
```

**Rules:**
- `data` fields → `ref<T>(initialValue)` with explicit generic types
- `this.setData({ k: v })` → direct assignment `data.value = v` (Vue reactivity handles updates)
- `this.data.k` → `data.value`
- Lifecycle hooks: import from `@dcloudio/uni-app` — `onLoad`, `onShow`, `onReady`, `onHide`, `onUnload`, `onPullDownRefresh`, `onReachBottom`, `onPageScroll`, `onShareAppMessage`, `onShareTimeline`
- Callbacks → `async` functions with `Promise<T>` return types
- Define interfaces/types at the top of `<script setup>` for all data structures
- `onShareAppMessage` returns `{ title, path, imageUrl }` (same format)

### 4.4 WXSS → `<style scoped>`

- Copy content into `<style scoped>` block.
- Change `lang` to `scss` if original uses SCSS-style nesting.
- `rpx` stays as-is.
- Convert `@import "xxx.wxss"` to `@import "xxx.css"` or drop (styles are scoped per-component).

### 4.5 Page-level JSON → pages.json per-page style

If a page has `foo.json` with `{ navigationBarTitleText, usingComponents, ... }`, migrate:
- `navigationBarTitleText` etc. → `pages.json` > `pages[n].style`
- `usingComponents` → page-level component registration (or rely on easycom)

---

## Step 5: Convert Components (Component() → Vue3 SFC + TypeScript)

For each component `components/foo/foo.{wxml,js,wxss,json}`:

### 5.1 Component JS → `<script setup lang="ts">`

```js
// Source — JavaScript Component():
Component({
  properties: {
    title: String,
    count: { type: Number, value: 0 },
    list: { type: Array, value: [] }
  },
  data: {
    internalState: false,
    expanded: false
  },
  methods: {
    onTap() {
      this.setData({ internalState: true })
      this.triggerEvent('change', { value: 1 })
    },
    toggleExpand() {
      this.setData({ expanded: !this.data.expanded })
    }
  },
  observers: {
    'count'(val) {
      this.handleCountChange(val)
    }
  },
  lifetimes: {
    attached() {
      this.loadData()
    },
    detached() {
      this.cleanup()
    }
  }
})
```

```vue
<!-- Target — TypeScript -->
<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, type Ref } from 'vue'

// --- Typed Props ---
interface Props {
  title: string
  count?: number
  list?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  list: () => []
})

// --- Typed Emits ---
const emit = defineEmits<{
  change: [value: number]
}>()

// --- Internal state ---
const internalState = ref<boolean>(false)
const expanded = ref<boolean>(false)

// --- Methods ---
const onTap = (): void => {
  internalState.value = true
  emit('change', 1)
}

const toggleExpand = (): void => {
  expanded.value = !expanded.value
}

const handleCountChange = (val: number | undefined): void => {
  console.log('count changed to', val)
}

const loadData = (): void => {
  // init logic
}

const cleanup = (): void => {
  // cleanup logic
}

// --- Watchers (was observers) ---
watch(() => props.count, (val: number | undefined) => {
  handleCountChange(val)
})

// --- Lifecycle (was lifetimes) ---
onMounted(() => {
  loadData()
})

onUnmounted(() => {
  cleanup()
})
</script>
```

**Rules (see [mappings.md §5](references/mappings.md#5-生命周期映射)):**
- `properties` → `defineProps<Interface>()` with interface, or `defineProps({...})` for runtime validation. Use `withDefaults(defineProps<>(), {...})` for defaults.
- `data` → `ref<T>()` / `reactive<T>()`
- `methods` → typed functions (`(): void => {...}`)
- `this.triggerEvent(name, detail)` → `emit(name, value)` with typed `defineEmits<{ event: [payloadType] }>()`
- `observers` → `watch()` / `watchEffect()`
- `behaviors` → typed composables (`use*.ts`)
- `lifetimes.created` → code in `<script setup lang="ts">` top-level
- `lifetimes.attached` → `onMounted()`
- `lifetimes.detached` → `onUnmounted()`
- `this.selectComponent(id)` → template refs with `ref<InstanceType<typeof Comp>>()`
- `externalClasses` → props-based class passing + `:deep()` selectors
- `relations` → typed `provide`/`inject` with injection keys

### 5.2 WXML / WXSS

Same as page conversion (Step 4), with this key difference:

- WXML slot: `<slot>` → `<slot>` (same in Vue)
- Multiple named slots: `<slot name="header">` → `<slot name="header">` (same)

### 5.3 Component Registration

uni-app auto-registers components placed in `components/` via easycom. Ensure component filename matches its usage name:

```
components/star/star.vue  →  <star /> (auto-registered)
```

If using custom paths, register explicitly in `pages.json` > `globalStyle.usingComponents` or page-level style.

---

## Step 6: Convert Utils & API Calls (JS → TypeScript)

### 6.1 File Migration: `.js` → `.ts`

Rename all utility files and add type annotations:

```ts
// utils/request.ts (was utils/request.js)
interface RequestConfig {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, any>
  header?: Record<string, string>
}

interface RequestResponse<T = any> {
  code: number
  data: T
  message: string
}

const BASE_URL = 'https://api.example.com'

export const request = <T = any>(config: RequestConfig): Promise<RequestResponse<T>> => {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + config.url,
      method: config.method || 'GET',
      data: config.data,
      header: {
        'Content-Type': 'application/json',
        ...config.header
      },
      success: (res) => {
        const data = res.data as RequestResponse<T>
        if (data.code === 0) {
          resolve(data)
        } else {
          uni.showToast({ title: data.message || '请求失败', icon: 'none' })
          reject(data)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络异常', icon: 'none' })
        reject(err)
      }
    })
  })
}
```

```ts
// utils/config.ts (was utils/config.js)
export interface AppConfig {
  baseUrl: string
  version: string
  debug: boolean
}

export const config: AppConfig = {
  baseUrl: 'https://api.example.com',
  version: '1.0.0',
  debug: false
}
```

### 6.2 Global `wx.*` → `uni.*` Replacement

Use the API mapping table in [mappings.md §6](references/mappings.md#6-api-映射-wx--uni). Most APIs are a direct namespace swap.

Walk through every file and replace:
- `wx.setStorageSync` → `uni.setStorageSync`
- `wx.request` → `uni.request`
- `wx.navigateTo` → `uni.navigateTo`
- `wx.showToast` → `uni.showToast`
- (all 100+ commonly used APIs)

For APIs that don't have a uni-app equivalent, keep them inside conditional compilation:

```ts
// #ifdef MP-WEIXIN
wx.cloud.init()
const db = wx.cloud.database()
// #endif
```

### 6.3 Promise + TypeScript

Convert callbacks to async/await with types:

```ts
// Before:
wx.getSystemInfo({
  success(res: WechatMiniprogram.SystemInfo) {
    console.log(res.screenWidth)
  }
})

// After:
const info = await uni.getSystemInfo()
console.log(info.screenWidth)

// With explicit type:
const info = await uni.getSystemInfo() as UniApp.GetSystemInfoResult
console.log(info.windowWidth)
```

### 6.4 getApp() and getCurrentPages()

These work identically in uni-app. No changes needed unless accessing WeChat-specific fields.

For typed access:

```ts
const app = getApp<{ globalData: { userId: string; token: string } }>()
console.log(app.globalData.userId)
```

### 6.5 WXS Scripts → TypeScript

WXS has no direct Vue equivalent. For each `.wxs` file:

- **Simple data formatting** → TypeScript utility functions with explicit types, imported into `<script setup lang="ts">`, used in `computed` or template expressions
- **Event handlers in WXS** → move to Vue methods (typed)
- **Complex WXS logic** → extract as a standalone `.ts` module, import where needed

```ts
// utils/format.ts (was utils/filter.wxs)
export const formatPrice = (price: number): string => {
  return `¥${price.toFixed(2)}`
}

export const formatTime = (timestamp: number, fmt: string = 'YYYY-MM-DD HH:mm:ss'): string => {
  const d = new Date(timestamp)
  const pad = (n: number): string => n.toString().padStart(2, '0')
  return fmt
    .replace('YYYY', d.getFullYear().toString())
    .replace('MM', pad(d.getMonth() + 1))
    .replace('DD', pad(d.getDate()))
    .replace('HH', pad(d.getHours()))
    .replace('mm', pad(d.getMinutes()))
    .replace('ss', pad(d.getSeconds()))
}
```

### 6.6 Dependencies

Check `package.json` dependencies:
- 3rd-party miniprogram components: find uni-app equivalents or keep inside `#ifdef MP-WEIXIN`
- Utility libs (lodash, dayjs, etc.): carry over directly — install with `@types/*` packages for TypeScript support
- WeChat-specific SDKs: conditional compilation

---

## Step 7: Finalize & Verify

### 7.1 Write the Complete Project

Write all converted files to the output directory. For **every text file write**, use the `scripts/write_file.py` script from the `qclaw-text-file` skill to ensure correct encoding and line endings.

### 7.2 Verification Checklist

Run through this checklist:

- [ ] `pages.json` has correct first page and all pages listed
- [ ] All page `.vue` files exist with `<script setup lang="ts">`
- [ ] All component `.vue` files exist with typed `defineProps<>()` / `defineEmits<>()`
- [ ] No `setData()` calls remain (replaced with direct `.value` assignment)
- [ ] No untyped `ref()` calls — all use `ref<T>(...)` with explicit generics
- [ ] No `wx.xxx` calls remain unhandled (mapped to `uni.xxx` or conditional compilation)
- [ ] All `bind:` → `@`, `catch:` → `@.stop`, `wx:if` → `v-if`
- [ ] `hidden` attributes inverted for `v-show`
- [ ] Page lifecycles use correct imports from `@dcloudio/uni-app`
- [ ] WXS logic extracted to typed `.ts` modules
- [ ] WeChat-specific features wrapped in `#ifdef MP-WEIXIN`
- [ ] Static assets (images, fonts) copied to `static/`
- [ ] `manifest.json` has WeChat appid set
- [ ] `App.vue` uses `<script lang="ts">` with `defineComponent`
- [ ] `tsconfig.json` present with correct paths and strict mode
- [ ] `types/global.d.ts` present with `.vue` module declaration
- [ ] All `.js` utils renamed to `.ts` with interfaces and type annotations

### 7.3 Report Summary

Output a summary table:

```
Total pages converted:  N  (<script setup lang="ts">)
Total components converted:  M  (defineProps<>() / defineEmits<>())
Total utils converted:  K  (.js → .ts with types)
Custom interfaces/types defined:  X
Wx.* → uni.* replacements:  Y
Conditional-compilation blocks added:  Z
Lines of WXS converted to TS utils:  W
Pending manual review items:  [list]
```

### 7.4 Manual Review Items

Flag these for manual review:
- `wx.cloud` calls (needs uniCloud migration or conditional compile)
- Custom `getApp().globalData` patterns — add type assertions
- Third-party miniprogram UI libraries (see if uni-app alternatives exist)
- Complex animation logic (`wx.createAnimation`) — types may need manual adjustment
- `requirePlugin` usages — no TypeScript types available
- Canvas API uses (API signatures may differ slightly)
- Complex selectors or DOM manipulation that may not translate cleanly
- Any inferred `any` types that need explicit annotation

---

## Post-Conversion: Run the Project

After conversion, tell the user to:

```bash
cd <output-dir>
npm install
npm install -D @dcloudio/types @types/node

# Run in HBuilderX or with CLI:
npx @dcloudio/uvm
npm run dev:mp-weixin
```

Import `dist/dev/mp-weixin` into WeChat DevTools to test.

---

## Resources

### references/mappings.md

Complete API, component, lifecycle, config, and syntax mapping tables with TypeScript examples. **Always consult this file during conversion** for exact field-to-field mappings. Load it at the start of Step 3 and reference throughout Steps 3-6.

Key sections:
- §1: Config mapping (app.json → pages.json/manifest.json)
- §2: File structure mapping
- §3: WXML → Vue template syntax
- §4: Data binding & events
- §5: Lifecycle mapping (pages & components)
- §6: API mapping (wx.* → uni.*)
- §7: WXSS → CSS/SCSS
- §8: uni-app added APIs
- §9: Conditional compilation syntax (with TS)
- §10: Common problem patterns
- §11: TypeScript-specific patterns & composables
