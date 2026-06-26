---
name: features-navigation-tabbar
description: uni-app 导航栏与 TabBar API setNavigationBarTitle、setTabBarItem、hideTabBar
---

# 导航栏与 TabBar API

## 导航栏

- **uni.setNavigationBarTitle(OBJECT)**：动态设置当前页标题，object 中传 `title`。若在页面进入时设置，建议在 **onReady** 内执行，避免被框架覆盖；在 onShow 内设需延迟。
- **uni.setNavigationBarColor(OBJECT)**：设置导航条前景色与背景色。参数：frontColor（仅 #fff/#000）、backgroundColor。进入页即改色时建议延迟执行。
- **uni.showNavigationBarLoading()** / **uni.hideNavigationBarLoading()**：在导航条显示/隐藏加载动画。

## TabBar

- **uni.setTabBarItem(OBJECT)**：动态设置某一项。参数：index、text、iconPath、selectedIconPath 等。
- **uni.setTabBarStyle(OBJECT)**：设置整体样式，如 color、selectedColor、backgroundColor、borderStyle。
- **uni.hideTabBar(OBJECT)** / **uni.showTabBar(OBJECT)**：隐藏/显示 tabBar，可设 animation。
- **uni.setTabBarBadge(OBJECT)** / **uni.removeTabBarBadge(OBJECT)**：为某项设置/移除右上角文字。object 传 index、text。
- **uni.showTabBarRedDot(OBJECT)** / **uni.hideTabBarRedDot(OBJECT)**：显示/隐藏某项右上角红点，object 传 index。

以上 API 仅对已在 pages.json 的 tabBar.list 中配置的页面生效。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/navigationbar
- https://uniapp.dcloud.net.cn/api/ui/tabbar
-->
