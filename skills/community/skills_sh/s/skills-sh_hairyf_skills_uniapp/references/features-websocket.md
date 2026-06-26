---
name: features-websocket
description: uni-app WebSocket connectSocket、SocketTask、onOpen/onMessage/send/close
---

# WebSocket

小程序端使用前需配置 **域名白名单**；连接地址须为 **wss://**（小程序要求）。全局 socket 只能有一个，**推荐使用 SocketTask**（需至少传入 success/fail/complete 之一才会返回 task，否则返回 Promise）。

## uni.connectSocket(OBJECT)

- **url**（必填）：服务器地址，小程序须 wss。
- **header**：请求头，不能设 Referer。
- **protocols**：子协议数组（部分平台支持）。
- 返回：传入 success/fail/complete 时返回 **SocketTask**；否则返回 Promise。

## SocketTask

- **SocketTask.send(OBJECT)**：发送数据，data 可为字符串或 ArrayBuffer。
- **SocketTask.close(OBJECT)**：关闭连接，可传 code、reason。
- **SocketTask.onOpen(callback)**：连接打开。
- **SocketTask.onMessage(callback)**：收到消息，callback 收到 res.data。
- **SocketTask.onError(callback)**：错误。
- **SocketTask.onClose(callback)**：连接关闭。

## 注意

- 各端同时存在的 WebSocket 连接数有限制（如微信最多 5 个），详见各端文档。
- uni-push 等会占用 socket，需多连接时务必用 SocketTask 多实例。
- 超时可在 manifest 的 networkTimeout.connectSocket 中配置。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/request/websocket
- https://uniapp.dcloud.net.cn/api/request/socket-task
-->
