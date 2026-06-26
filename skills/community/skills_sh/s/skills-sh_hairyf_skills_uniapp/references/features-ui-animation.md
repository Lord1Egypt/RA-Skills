---
name: features-ui-animation
description: uni-app 动画 createAnimation、animation 实例、export、组件 animation 属性
---

# 动画 API

**nvue、HarmonyOS Next 不支持**；京东、快手小程序不支持。

## uni.createAnimation(OBJECT)

创建动画实例。参数：duration（时长 ms）、timingFunction（linear/ease/ease-in/ease-out/ease-in-out 等）、delay、transformOrigin。返回 **animation** 对象。

## animation 实例

调用实例方法描述动画，方法返回自身，可链式调用。常用：opacity、backgroundColor、width、height、top、left、right、bottom、rotate、scale、skew、translate 等。最后调用 **animation.export()** 导出动画数据，将返回值赋给组件的 **animation** 属性，即可在组件上播放。

注意：每次调用 **export()** 会清掉此前在该实例上的动画描述，需重新链式调用后再 export。

## 使用步骤

1. 在 data 中定义变量如 `animationData: {}`。
2. `const animation = uni.createAnimation({ duration: 300 })`；链式调用如 `animation.opacity(0.5).step()`。
3. `this.animationData = animation.export()`（或 setData）。
4. 在 template 中给组件绑定 `:animation="animationData"`。

step() 表示一组动画结束；可多次 step 实现多段动画。详见官方「animation」文档。

## 页面滚动

**uni.pageScrollTo(OBJECT)**：将页面滚动到指定位置，object 中可设 scrollTop、duration 等。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/animation
- https://uniapp.dcloud.net.cn/api/ui/scroll
-->
