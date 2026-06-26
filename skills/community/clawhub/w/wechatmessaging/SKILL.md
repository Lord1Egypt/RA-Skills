name: wechat_messaging
description: 通过微信向好友发送消息。流程：查询好友 -> 确认目标 -> 发送内容。
# 这里填入你的 API 基础域名，例如 http://api.example.com
endpoint: https://192.168.29.1:8080
env:
  WECHAT_APPID: wx_KcD1dMEn7KidBemwN2lVh
---

# 微信消息助手技能说明

## 工具 1: 查询好友 (queryFriend)
- 路径: `GET /aiTest/queryFriend`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `name`: 用户提供的好友名称

## 工具 2: 发送消息 (sendText)
- 路径: `POST /aiTest/sendText`
- 参数:
    - `appid`: {{env.WECHAT_APPID}}
    - `contact`: 目标好友的 wxId (从 queryFriend 获取)
    - `content`: 文本内容

## 强制逻辑流程
1. 收到发消息请求，必须先执行 `queryFriend`。
2. 若返回多个好友，展示列表让用户选。
3. 若返回一个好友，告知用户并询问“确定发送吗？”。
4. 得到确认后，再执行 `sendText`。