---
name: features-nodes-info
description: uni-app 节点信息 createSelectorQuery、boundingClientRect、scrollOffset
---

# 节点信息

用于查询组件位置、尺寸、滚动位置等，需在**生命周期 mounted 之后**调用。默认选择器只选页面节点，不包含自定义组件内节点，需用 `selectorQuery.in(component)` 限定到组件内。

## uni.createSelectorQuery()

返回 SelectorQuery 实例。链式调用：`.in(component)`（可选，限定范围）→ `.select(selector)` 或 `.selectAll(selector)` 或 `.selectViewport()` → `.boundingClientRect(callback)` / `.scrollOffset(callback)` / `.fields(...)` → 最后 `.exec()` 执行。

## 选择器

支持：`#id`、`.class`、`.parent > .child`、`.ancestor .descendant`、跨组件后代 `.ancestor >>> .descendant`（H5 暂不支持）、多选 `#a, .b`。支付宝小程序不支持 `in(component)`。

## NodesRef 方法

- **boundingClientRect(callback)**：节点布局位置与尺寸（width、height、top、left、right、bottom 等）。
- **scrollOffset(callback)**：滚动位置（scrollTop、scrollLeft）。
- **fields(fields, callback)**：获取指定字段，如 id、dataset、size、scrollOffset 等。

组合式 API 中需用 `getCurrentInstance().proxy` 作为 `in()` 的参数。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/nodes-info
-->
