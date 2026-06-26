---
name: core-lifecycle
description: uni-app 页面生命周期 onLoad、onShow、onReady、onHide、onUnload
---

# 页面生命周期

除 Vue 组件生命周期外，uni-app 页面还支持下列页面级生命周期（组合式 API 在 Vue2/Vue3 下用法见官方文档）。

## 常用生命周期

| 函数名 | 说明 |
|--------|------|
| onLoad | 页面加载，参数为上一页通过路由或 EventChannel 传递的 Object |
| onShow | 页面每次显示时触发（含从下级页返回、tab 切换显示） |
| onReady | 页面首次渲染完成，DOM 可用，可安全使用 ref 等 |
| onHide | 页面隐藏（跳转到其他页、进后台等） |
| onUnload | 页面卸载 |

其他：onPullDownRefresh（下拉刷新）、onReachBottom（上拉触底）、onTabItemTap（tab 项点击）、onShareAppMessage（分享）等，见官方「页面生命周期」文档。

## 顺序与时机

- 进入页面：先 onLoad，再 onShow，随后首屏渲染完成后 onReady。onReady 与转场动画先后不固定，取决于 DOM 复杂度。
- 跳转新页：当前页 onHide，新页 onLoad → onShow → onReady。
- 返回：新页 onUnload，上一页 onShow（不再 onLoad）。
- tab 切换：切走的页 onHide，切到的页 onShow（已加载过的 tab 不会再次 onLoad）。

## 使用建议

- **传参与初始化**：在 onLoad 的 option 中接收路由参数，做数据请求或状态初始化。
- **联网**：在 onLoad 里尽早发起请求，不要在 onReady 里才请求，否则首屏偏慢。
- **耗时计算**：避免在 onLoad 中执行大量同步计算，会阻塞转场动画；uni-app x 在 Android 上 onLoad 默认在 UI 线程。
- **事件监听**：在 onLoad 里 `uni.$on` 的，要在 onUnload 里 `uni.$off`，或使用 `uni.$once` 避免泄漏。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/lifecycle
- https://uniapp.dcloud.net.cn/tutorial/page.html#lifecycle
-->
