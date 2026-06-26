---
name: advanced-worker
description: uni-app 多线程 Worker、各端实现差异
---

# Worker 多线程

**需分平台编写**，无统一跨端 Worker API。

- **微信/支付宝/抖音/QQ 小程序**：各有自己的 Worker 规范（如 wx.createWorker、tt.createWorker），见各端开发文档。
- **H5**：可使用标准 **Web Worker**（new Worker(url)）。
- **App**：JS 运行在 JSCore，若需另一线程运行 JS，可用 **web-view 组件**或 **renderjs**（运行在 webview，与 JSCore 不同线程）；注意多 webview 间 JS 同进程，可能影响视图。插件市场有原生多线程插件可选用。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/worker
-->
