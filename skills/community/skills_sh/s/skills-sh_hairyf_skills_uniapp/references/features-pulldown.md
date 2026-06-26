---
name: features-pulldown
description: uni-app 下拉刷新与上拉触底 onPullDownRefresh、onReachBottom、startPullDownRefresh、stopPullDownRefresh
---

# 下拉刷新与上拉触底

## 下拉刷新

- **配置**：在 pages.json 的当前页 `style` 中设置 `enablePullDownRefresh: true`。可配 `backgroundTextStyle`、`backgroundColor` 等；App 端还可在 app-plus 的 pullToRefresh 中配置样式、offset 等。
- **生命周期**：在页面中定义 **onPullDownRefresh**（与 onLoad 同级），用户下拉时触发。处理完数据后调用 **uni.stopPullDownRefresh()** 结束动画。
- **主动触发**：**uni.startPullDownRefresh()** 可代码触发下拉刷新，效果同用户下拉。

## 上拉触底

- **配置**：在 pages.json 的 globalStyle 或页面 style 中设置 **onReachBottomDistance**（默认 50px），表示距底部多少 px 时触发。
- **生命周期**：在页面中定义 **onReachBottom**，滚动到底部附近时触发，常用于分页加载更多。

## 注意

- 自定义导航栏（navigationStyle: custom）与原生下拉刷新搭配时，各端表现有差异；小程序下若要从导航栏下方下拉，可能需用前端模拟（如 mescroll 插件），详见官方「自定义导航栏」说明。
- 下拉刷新与上拉触底仅对当前页生效；tabBar 页切换时需注意是否重复请求。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/pulldown
- https://uniapp.dcloud.net.cn/collocation/pages?id=globalstyle
-->
