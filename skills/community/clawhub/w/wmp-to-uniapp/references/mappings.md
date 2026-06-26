# WeChat Mini Program → uni-app Mapping Reference Table

## 1. Configuration File Mapping (app.json → pages.json/manifest.json)

| WeChat Mini Program (app.json)        | uni-app (manifest.json / pages.json)       |
|----------------------------------------|--------------------------------------------|
| `pages`                                | `pages.json > pages` (first is home page)   |
| `subPackages` / `subpackages`          | `pages.json > subPackages`                  |
| `window.navigationBarTitleText`        | `pages.json > globalStyle.navigationBarTitleText` |
| `window.navigationBarBackgroundColor`  | `pages.json > globalStyle.navigationBarBackgroundColor` |
| `window.navigationBarTextStyle`        | `pages.json > globalStyle.navigationBarTextStyle` |
| `window.backgroundColor`               | `pages.json > globalStyle.backgroundColor`  |
| `window.backgroundTextStyle`           | `pages.json > globalStyle.backgroundTextStyle` |
| `window.enablePullDownRefresh`         | `pages.json > globalStyle.enablePullDownRefresh` |
| `window.onReachBottomDistance`         | `pages.json > globalStyle.onReachBottomDistance` |
| `tabBar`                               | `pages.json > tabBar` (structure basically the same) |
| `permission`                           | `manifest.json > mp-weixin.permission`      |
| `plugins`                              | `manifest.json > mp-weixin.plugins`         |
| `navigateToMiniProgramAppIdList`       | `manifest.json > mp-weixin.navigateToMiniProgramAppIdList` |
| `requiredBackgroundModes`              | `manifest.json > mp-weixin.requiredBackgroundModes` |
| `usingComponents` (global)             | `pages.json > globalStyle.usingComponents` (easycom handles automatically) |
| `style` (page-level)                   | `pages.json > pages[].style`                |
| `preloadRule`                          | `pages.json > preloadRule`                  |
| `workers`                              | `manifest.json > mp-weixin.workers`         |
| `lazyCodeLoading`                      | Not supported, manual handling required     |
| `renderer`                             | Ignored (uni-app handles automatically)     |
| `componentFramework`                   | Ignored                                    |

## 2. Page File Mapping

| WeChat Mini Program | uni-app + Vue3            |
|---------------------|---------------------------|
| `page.wxml`         | `page.vue` (`<template>`) |
| `page.wxss`         | `page.vue` (`<style scoped>`) |
| `page.js`           | `page.vue` (`<script setup>`) |
| `page.json`         | `pages.json` page `style` configuration |

## 3. WXML → Vue Template Syntax Mapping

| WeChat Mini Program (WXML)              | uni-app + Vue3 (Template)                    |
|------------------------------------------|----------------------------------------------|
| `<view>`                                 | `<view>`                                     |
| `<text>`                                 | `<text>`                                     |
| `<image src="{{url}}">`                  | `<image :src="url">`                         |
| `<block>`                                | `<template>` or remove directly               |
| `wx:if="{{condition}}"`                  | `v-if="condition"`                           |
| `wx:elif="{{condition}}"`                | `v-else-if="condition"`                      |
| `wx:else`                                | `v-else`                                     |
| `wx:for="{{list}}"`                      | `v-for="item in list"`                       |
| `wx:for-item="item"`                     | `v-for="(item, index) in list"` (default)    |
| `wx:for-index="idx"`                     | `v-for="(item, idx) in list"`                |
| `wx:key="id"`                            | `:key="item.id"`                             |
| `bind:tap="handler"`                     | `@tap="handler"`                             |
| `bindtap="handler"`                      | `@tap="handler"`                             |
| `catch:tap="handler"`                    | `@tap.stop="handler"`                        |
| `catchtap="handler"`                     | `@tap.stop="handler"`                        |
| `bind:input="onInput"`                   | `@input="onInput"`                           |
| `bind:change="onChange"`                 | `@change="onChange"`                         |
| `bind:submit="onSubmit"`                 | `@submit="onSubmit"`                         |
| `bind:touchstart="handler"`              | `@touchstart="handler"`                      |
| `data-xxx="{{value}}"`                   | `data-xxx="value"` or `:data-xxx="value"`    |
| `hidden="{{flag}}"`                      | `v-show="!flag"` (semantic inversion)        |
| `{{ expression }}`                       | `{{ expression }}`                           |
| `import` / `include`                     | Use `<import src="...">` or component reference |

## 4. Data Binding and Events

| WeChat Mini Program                     | uni-app + Vue3                          |
|----------------------------------------|-----------------------------------------|
| `this.setData({ key: value })`         | `data.key = value` (automatically reactive) |
| `this.data.key`                        | `data.key`                               |
| `e.detail.value` (input event)         | `e.detail.value` (same)                  |
| `e.currentTarget.dataset`              | `e.currentTarget.dataset` (same)         |
| `e.mark`                               | `e.mark` (same)                          |
| `wx:model` (simple two-way binding)    | `v-model`                                 |

## 5. Lifecycle Mapping

| WeChat Mini Program (Page)    | uni-app + Vue3 (Page/Component)               |
|-------------------------------|-----------------------------------------------|
| `onLoad(options)`             | `onLoad(options)`                              |
| `onShow()`                    | `onShow()`                                    |
| `onReady()`                   | `onReady()`                                   |
| `onHide()`                    | `onHide()`                                    |
| `onUnload()`                  | `onUnload()`                                  |
| `onPullDownRefresh()`         | `onPullDownRefresh()`                         |
| `onReachBottom()`             | `onReachBottom()`                             |
| `onShareAppMessage()`         | `onShareAppMessage()`                         |
| `onShareTimeline()`           | `onShareTimeline()`                           |
| `onPageScroll()`              | `onPageScroll()`                              |
| `onResize()`                  | `onResize()`                                  |
| `onTabItemTap()`              | `onTabItemTap()`                              |
| `onSaveExitState()`           | Not supported, manual handling required       |

| WeChat Mini Program (Component) | uni-app + Vue3 (Component)                    |
|--------------------------------|-----------------------------------------------|
| `Component({...})`             | `<script setup>` + `defineProps/defineEmits`  |
| `properties`                   | `const props = defineProps({...})`            |
| `data`                         | `ref()` / `reactive()`                        |
| `methods`                      | Regular functions (directly callable in template) |
| `lifetimes.created`            | `setup()` top-level execution                 |
| `lifetimes.attached`           | `onMounted()`                                 |
| `lifetimes.ready`              | `onMounted()` + `nextTick()`                  |
| `lifetimes.detached`           | `onUnmounted()`                               |
| `observers`                    | `watch()` / `watchEffect()`                   |
| `behaviors`                    | Composables                                   |
| `this.triggerEvent()`          | `const emit = defineEmits([...])` + `emit()`  |
| `this.selectComponent()`       | `ref` + `defineExpose()`                      |
| `externalClasses`              | Pass class via props or `:deep()` penetrate   |
| `relations`                    | `provide` / `inject`                          |

## 6. API Mapping (wx.* → uni.*)

**Navigation:**

| WeChat Mini Program API          | uni-app API                   |
|----------------------------------|-------------------------------|
| `wx.navigateTo({url})`           | `uni.navigateTo({url})`       |
| `wx.redirectTo({url})`           | `uni.redirectTo({url})`       |
| `wx.reLaunch({url})`             | `uni.reLaunch({url})`         |
| `wx.switchTab({url})`            | `uni.switchTab({url})`        |
| `wx.navigateBack({delta})`       | `uni.navigateBack({delta})`   |
| `wx.navigateToMiniProgram()`     | Only supported on WeChat platform |

**Storage:**

| `wx.setStorageSync(k, v)`       | `uni.setStorageSync(k, v)`    |
| `wx.getStorageSync(k)`          | `uni.getStorageSync(k)`       |
| `wx.removeStorageSync(k)`       | `uni.removeStorageSync(k)`    |
| `wx.clearStorageSync()`         | `uni.clearStorageSync()`      |
| `wx.setStorage({key, data})`    | `uni.setStorage({key, data})` |
| `wx.getStorage({key})`          | `uni.getStorage({key})`       |
| `wx.removeStorage({key})`       | `uni.removeStorage({key})`    |
| `wx.clearStorage()`             | `uni.clearStorage()`          |

**Network Requests:**

| `wx.request({url, ...})`        | `uni.request({url, ...})`     |
| `wx.uploadFile({...})`          | `uni.uploadFile({...})`       |
| `wx.downloadFile({...})`        | `uni.downloadFile({...})`     |
| `wx.connectSocket({...})`       | `uni.connectSocket({...})`    |

**Media:**

| `wx.chooseImage({...})`         | `uni.chooseImage({...})`      |
| `wx.previewImage({...})`        | `uni.previewImage({...})`     |
| `wx.saveImageToPhotosAlbum()`   | `uni.saveImageToPhotosAlbum()`|
| `wx.chooseVideo({...})`         | `uni.chooseVideo({...})`      |
| `wx.saveVideoToPhotosAlbum()`   | `uni.saveVideoToPhotosAlbum()`|
| `wx.getRecorderManager()`       | `uni.getRecorderManager()`    |
| `wx.createInnerAudioContext()`  | `uni.createInnerAudioContext()`|
| `wx.createVideoContext()`       | `uni.createVideoContext()`    |
| `wx.createCameraContext()`      | `uni.createCameraContext()`   |

**UI:**

| `wx.showToast({...})`           | `uni.showToast({...})`        |
| `wx.showModal({...})`           | `uni.showModal({...})`        |
| `wx.showLoading({...})`         | `uni.showLoading({...})`      |
| `wx.hideLoading()`              | `uni.hideLoading()`           |
| `wx.showActionSheet({...})`     | `uni.showActionSheet({...})`  |
| `wx.setNavigationBarTitle()`    | `uni.setNavigationBarTitle()` |
| `wx.setNavigationBarColor()`    | `uni.setNavigationBarColor()` |
| `wx.showNavigationBarLoading()` | `uni.showNavigationBarLoading()`|
| `wx.hideNavigationBarLoading()` | `uni.hideNavigationBarLoading()`|
| `wx.pageScrollTo({...})`        | `uni.pageScrollTo({...})`     |
| `wx.startPullDownRefresh()`     | `uni.startPullDownRefresh()`  |
| `wx.stopPullDownRefresh()`      | `uni.stopPullDownRefresh()`   |
| `wx.createSelectorQuery()`      | `uni.createSelectorQuery()`   |

**Device:**

| `wx.getSystemInfoSync()`        | `uni.getSystemInfoSync()`     |
| `wx.getSystemInfo()`            | `uni.getSystemInfo()`         |
| `wx.getNetworkType()`           | `uni.getNetworkType()`        |
| `wx.onNetworkStatusChange()`    | `uni.onNetworkStatusChange()` |
| `wx.makePhoneCall()`            | `uni.makePhoneCall()`         |
| `wx.scanCode({...})`            | `uni.scanCode({...})`         |
| `wx.setClipboardData()`         | `uni.setClipboardData()`      |
| `wx.getClipboardData()`         | `uni.getClipboardData()`      |
| `wx.getLocation()`              | `uni.getLocation()`           |
| `wx.chooseLocation()`           | `uni.chooseLocation()`        |
| `wx.openLocation()`             | `uni.openLocation()`          |
| `wx.vibrateLong()`              | `uni.vibrateLong()`           |
| `wx.vibrateShort()`             | `uni.vibrateShort()`          |

**Open APIs:**

| `wx.login()`                    | `uni.login()`                 |
| `wx.getUserInfo()`              | `uni.getUserInfo()` (注意 platform differences) |
| `wx.getUserProfile()`           | Only WeChat, keep with conditional compilation |
| `wx.requestPayment()`           | `uni.requestPayment()`        |
| `wx.authorize()`                | `uni.authorize()`             |
| `wx.getSetting()`               | `uni.getSetting()`            |
| `wx.openSetting()`              | `uni.openSetting()`           |
| `wx.shareAppMessage()`          | `uni.share()` (or page onShareAppMessage) |

**Special Handling:**

| WeChat Mini Program              | Handling Method                               |
|----------------------------------|-----------------------------------------------|
| `getApp()`                       | `getApp()` (still usable)                     |
| `getCurrentPages()`              | `getCurrentPages()` (still usable)            |
| `wx.getAccountInfoSync()`        | `uni.getAccountInfoSync()`                    |
| `wx.getLaunchOptionsSync()`      | `uni.getLaunchOptionsSync()`                  |
| `wx.getEnterOptionsSync()`       | `uni.getEnterOptionsSync()`                   |
| `wx.createIntersectionObserver()`| `uni.createIntersectionObserver()`            |
| `requirePlugin()`                | Conditional compilation `// #ifdef MP-WEIXIN` keep |
| `wx.cloud.*`                     | Conditional compilation or migrate to uniCloud |

## 7. WXSS → CSS/SCSS Mapping

| WeChat Mini Program (WXSS)   | uni-app (CSS/SCSS)                              |
|------------------------------|--------------------------------------------------|
| `rpx`                        | `rpx` (same, 750rpx = screen width)             |
| `@import "xxx.wxss"`         | `@import "xxx.css"` or `@import` in `<style>`   |
| No `*` universal selector    | Supports `*` selector                           |
| No `> ~ +` combinators       | Supports all CSS selectors                      |
| No `attr()`                  | Supports `attr()`                               |

**Note:** uni-app supports SCSS/Less, directly usable in `<style lang="scss" scoped">`.

## 8. uni-app New APIs (Not in Native Mini Program)

| uni-app API                        | Purpose                         |
|-----------------------------------|------------------------------|
| `uni.$emit(event, ...args)`       | Global event communication     |
| `uni.$on(event, callback)`        | Listen to global events        |
| `uni.$once(event, callback)`      | One-time listen to global events|
| `uni.$off(event, callback)`       | Remove global event listener   |
| `uni.getProvider({service})`      | Get service provider           |
| `uni.onThemeChange(callback)`     | Listen to theme changes        |
| `uni.offThemeChange(callback)`    | Stop listening to theme changes|

## 9. Conditional Compilation Syntax

Use conditional compilation in uni-app to handle platform-specific code:

```vue
<!-- #ifdef MP-WEIXIN -->
// Code retained only for WeChat mini program
<!-- #endif -->

<!-- #ifndef H5 -->
// Code for non-H5 platforms
<!-- #endif -->
```

```js
// #ifdef MP-WEIXIN
wx.cloud.init()
getApp().globalData.xxx = 123
// #endif
```

## 10. Common Issue Solutions

| Issue                              | Solution                                           |
|------------------------------------|----------------------------------------------------|
| `Component()` constructor          | Migrate to Vue3 SFC (`<script setup>`)             |
| `behaviors` reusable logic         | Extract to Vue3 composables (`use*.js`)            |
| `observers` property watching      | Use `watch()` / `watchEffect()`                    |
| `relations` component relationships | Use `provide` / `inject`                          |
| `externalClasses` in custom components | Pass class name via props + `:deep()` or `:class` |
| `wx:model` simple two-way binding  | Replace with `v-model`                             |
| `picker` mode="region"             | Use `@uni-ui/picker` or `<picker mode="region">`   |
| Native components (camera/map/video, etc.) | Keep, uni-app natively supports them            |
| Custom tabBar                      | Conditional compilation `// #ifdef MP-WEIXIN` keep config |
| `template` + `data` (WXML templates) | Change to Vue component slots (`<slot>`) or extract as component |
| WXS script dependencies            | Migrate to methods / computed / standalone JS utility functions |
| `project.config.json`              | Ignore, uni-app generates via HBuilderX / CLI     |