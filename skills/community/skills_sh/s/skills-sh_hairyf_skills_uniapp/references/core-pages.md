---
name: core-pages
description: pages.json 页面路由、globalStyle、tabBar、easycom
---

# pages.json 页面路由

用于全局配置：页面路径、窗口样式、原生导航栏、底部 tabBar 等。类似微信小程序 `app.json` 的页面管理部分；权限等则在 manifest 中配置。

## 主要配置项

| 属性 | 类型 | 说明 |
|------|------|------|
| globalStyle | Object | 默认页面窗口表现（导航栏、背景色、下拉刷新等） |
| pages | Array | **必填**。页面路径及每页 style，首项为首页 |
| tabBar | Object | 底部 tab 表现（list 中为 pagePath、icon、text 等） |
| easycom | Object | 组件自动引入规则（2.5.5+） |
| subPackages | Array | 分包配置（H5 不支持） |
| preloadRule | Object | 分包预下载（部分小程序支持） |
| condition | Object | 开发期启动模式 |
| leftWindow / topWindow / rightWindow | Object | H5 大屏多窗口 |

## 页面项与 style

每个 `pages` 项：`path`（如 `pages/index/index`）、`style`（该页导航栏标题、下拉刷新、动画等）。  
页面路径对应项目中的 `.vue` 文件路径，无需写后缀。

## tabBar

- `list` 中每项需 `pagePath`、`text`，及 `iconPath` / `selectedIconPath`（或 iconfont 配置）。
- 跳转 tabBar 页面**只能**用 `uni.switchTab`，且 url 不能带参数。
- tabBar 页面首次加载后常驻内存，再次切换只触发 onShow，不再次 onLoad。

## easycom

在 `pages.json` 的 `easycom` 中可自定义组件匹配规则，例如：

```json
"easycom": {
  "autoscan": true,
  "custom": {
    "^uni-(.*)": "@/components/uni-$1.vue"
  }
}
```

符合目录结构 `components/组件名/组件名.vue` 的组件可免注册直接使用。

## 注意

- 新建页面后需在 `pages` 中增加一项，否则无法访问。
- 导航栏高度约 44px（不含状态栏），tabBar 高度约 50px（不含安全区）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/collocation/pages
-->
