---
name: features-intersection-observer
description: uni-app 节点相交 createIntersectionObserver、relativeTo、observe、disconnect
---

# 节点相交（IntersectionObserver）

用于监听组件节点在布局上的相交状态，可推断节点是否可见、可见比例，常用于懒加载、曝光统计。

## uni.createIntersectionObserver([this], [options])

创建 IntersectionObserver 实例。自定义组件内传 **this**（支付宝不支持此参数）。options：thresholds（阈值数组，默认 [0]）、initialRatio、observeAll。

## 实例方法

- **relativeTo(selector, [margins])**：以选择器指定节点为参照区域；margins 可扩展/收缩边界（left/right/top/bottom）。
- **relativeToViewport([margins])**：以页面显示区域为参照。
- **observe(selector, callback)**：指定目标节点并开始监听；callback 收到相交结果（intersectionRatio 等）。
- **disconnect()**：停止监听。

在页面或组件销毁时建议 disconnect，避免泄漏。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/intersection-observer
-->
