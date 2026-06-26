---
name: features-timer
description: uni-app 定时器 setTimeout、setInterval、clearTimeout、clearInterval
---

# 定时器

与标准 JS 一致，支持 **setTimeout**、**setInterval**、**clearTimeout**、**clearInterval**。参数：callback、delay（ms）、rest（附加参数）。返回值：timeoutID / intervalID，用于 clear。

## 最佳实践

定时器应在**组件/页面销毁时取消**（onUnload、beforeDestroy 等），否则会成为游离定时器无法回收。选项式 API 中在 data 或实例上保存 timer 引用，在 onUnload 中 clearTimeout(timer) 或 clearInterval(timer)。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/timer
-->
