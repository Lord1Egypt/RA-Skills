name: wechat_operate
description: 通过微信进行社交管理与消息发送。流程：查询目标（好友/群聊/成员） -> 确认目标 -> 发送内容（文本/图片/文件）。
endpoint: http://192.168.29.1:8080
env:
  WECHAT_APPID: wx_KcD1dMEn7KidBemwN2lVh

---

# 微信消息助手技能说明

## 工具 1: 查询好友 (queryFriend)
- 路径: `GET /aiTest/queryFriend`
- 参数:
    - `appid`: {{env.WECHAT_APPID}} (当前微信的appid)
    - `name`: 好友的名称

## 工具 2: 查询最近联系人 (queryRecentContact)
- 路径: `GET /aiTest/queryRecentContact`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}

## 工具 3: 查询我的群聊 (queryChatroom)
- 路径: `GET /aiTest/queryChatroom`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}

## 工具 4: 查询群成员 (queryChatroomMembers)
- 路径: `GET /aiTest/queryChatroomMembers`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `chatroomId`: 群id

## 工具 5: 发送文本消息 (sendText)
- 路径: `POST /aiTest/sendText`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `contact`: 目标好友或群聊的 wxId
    - `content`: 发送消息内容

## 工具 6: 发送图片消息 (sendImg)
- 路径: `POST /aiTest/sendImg`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `contact`: 目标好友或群聊的 wxId
    - `content`: 图片的连接信息

## 工具 7: 发送文件消息 (sendFile)
- 路径: `POST /aiTest/sendFile`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `contact`: 目标好友或群聊的 wxId
    - `fileUrl`: 文件的连接信息
    - `fileName`: 文件名称（若为 null 则从 fileUrl 中解析）

---

## 强制逻辑流程
1. **查询目标**：收到发送请求后，必须先根据场景执行 `queryFriend` 或 `queryChatroom` 获取 `wxId`。
2. **多结果处理**：若返回多个结果，需展示列表让用户选择。
3. **二次确认**：
    - 文本消息：告知目标名称并询问“确定发送吗？”。
    - 图片/文件：展示文件信息/预览，并询问“确定发送给 [名称] 吗？”。
4. **最终发送**：得到确认后，再执行对应的 `send` 接口。