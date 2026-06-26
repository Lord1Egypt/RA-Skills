---
name: features-clipboard
description: uni-app 剪贴板 setClipboardData、getClipboardData
---

# 剪贴板

## uni.setClipboardData(OBJECT)

设置系统剪贴板内容。参数：`data`（必填，字符串）、`showToast`（是否弹出「已复制」提示，App/H5 3.2.13+ 可配，默认 true）、success/fail/complete。不传回调则返回 Promise。

## uni.getClipboardData(OBJECT)

获取系统剪贴板内容。success 返回 `res.data`（字符串）。不传回调则返回 Promise。

## 示例

```javascript
uni.setClipboardData({ data: '复制内容' });
const res = await uni.getClipboardData();
console.log(res.data);
```

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/system/clipboard
-->
