---
name: teamgram-client-e2e-flow
description: Documents the KHF Android client architecture and complete end-to-end data flows for login, messaging, and file operations through all Teamgram Server layers.
compatibility: Documentation/knowledge skill only. No executable code. Reference material for Teamgram Server developers.
metadata:
  author: zhihang9978
  version: "1.0.0"
  source: https://github.com/teamgram/teamgram-server
  homepage: https://github.com/teamgram/teamgram-server
  openclaw:
    requires:
      env: []
      bins: []
    securityNotes: |
      Documentation-only skill. Contains no executable code, no network calls, no credential handling.
      APP_ID and APP_HASH are public application identifiers, not secrets.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# KHF Android 客户端架构与端到端数据流

## KHF 客户端关键常量

从 KHF 源码提取（必须与服务端兼容）：
- `TLRPC.LAYER = 222`
- `BuildVars.APP_ID = 4`
- `BuildVars.APP_HASH = "014b35b6184100b085b0d0572f9b5103"`

## tgnet/ConnectionsManager：Java → JNI → Native MTProto

ConnectionsManager 负责：
- `native_init(...)` 初始化 MTProto（layer/api_id/设备信息）
- `native_sendRequest(...)` 发送 RPC
- DC/网络状态管理

客户端通过 JNI 调用 Native C++ 层实现 MTProto 协议，包括：
- 加密/解密（AES-IGE）
- 握手（DH 密钥交换生成 auth_key）
- 消息序列化/反序列化（TL 二进制格式）
- 网络连接管理（TCP/WebSocket）
- 重连与退避策略

## MessagesController：业务层

MessagesController 负责 dialogs/messages/users/chats 的本地模型与网络请求，典型方法：
- loadAppConfig — 加载应用配置
- loadDialogs — 加载对话列表
- loadMessages — 加载消息
- loadFullChat — 加载群组完整信息
- loadFullUser — 加载用户完整信息

## 端到端数据流示例

### 登录流程：auth.sendCode → auth.signIn

```text
Client (KHF)
  -> TL: auth.sendCode(phone_number, api_id, api_hash, settings)
  -> MTProto encrypted message
  -> gnetway decrypt + QuickAck + SendDataToSession
  -> session decode TLMessage2 -> route to /mtproto.RPCAuthorization via IDMap
  -> bff.authorization.AuthSendCode
       -> biz.user (check phone registered)
       -> status (online sessions)
       -> verify-code plugin (sms) OR app code
  <- bff returns auth.SentCode or error
  <- session wraps rpc_result
  <- gnetway encrypts + send back
  <- client parses auth.SentCode
```

### 消息发送流程：messages.sendMessage

```text
Client
  -> TL: messages.sendMessage / messages.sendMedia / ...
  -> gnetway -> session -> bff.messages
  -> bff.messages
       -> biz_service (dialog/message/chat/user)
       -> msg service (异步投递 + Kafka)
  -> messenger.msg produces to Kafka Inbox-T
  -> inbox consumes Inbox-T, writes inbox/outbox state
  -> produces updates to Kafka Sync-T
  -> sync consumes Sync-T, decides UpdatesMe/NotMe/PushRpcResult
  -> sync calls session (gRPC) to push updates/rpc_result
  -> session routes to correct sessionId
  -> gnetway encrypt -> client
```

### 文件上传下载流程

```text
Client
  -> files.upload* / upload.getFile
  -> bff.files
       -> dfs 保存/获取 file parts
       -> media 生成缩略图/元数据
       -> db 写入 documents/photos/photo_sizes/...
  <- 返回 inputFile / fileLocation / document/photo

DFS
  - Minio buckets: documents/photos/videos/encryptedfiles
  - MiniHttp 0.0.0.0:11701 提供 HTTP 下载入口
```

## 客户端与服务端兼容性要点

1. **LAYER 版本**：客户端 LAYER=222 必须与服务端 session.yaml 中的 layer 配置一致
2. **APP_ID/APP_HASH**：必须与服务端 BFF 配置中的 ApiId/ApiHash 匹配
3. **MTProto 握手**：客户端使用 obfuscated2 + AES-IGE 加密
4. **TL 序列化**：客户端和服务端必须使用相同的 TL Schema 版本

## 常见错误与排查

| 错误 | 含义 | 排查方向 |
|---|---|---|
| PHONE_NUMBER_INVALID | 手机号格式不正确 | 检查国际格式（+86...） |
| PHONE_NUMBER_BANNED | 手机号被封禁 | 检查 predefined_users 表 |
| SESSION_PASSWORD_NEEDED | 需要两步验证 | 用户设置了密码 |
| AUTH_KEY_UNREGISTERED | auth_key 未注册 | 清除客户端数据重新握手 |
| CONNECTION_NOT_INITED | 未调用 initConnection | 客户端需先发 initConnection |
| ERR_ENTERPRISE_IS_BLOCKED | 企业版功能锁定 | 需要解除企业版拦截（修改 biz_service 中的企业版检查逻辑） |
| METHOD_NOT_IMPL | RPC 方法未实现 | 检查 BFF handler 和 session IDMap 路由是否配置 |

## 企业版锁定模式

Teamgram 社区版中部分功能被企业版锁定拦截，表现为：
- `ERR_ENTERPRISE_IS_BLOCKED` 错误
- 在 biz_service 层的 helper 中通过 `checkEnterprise()` 函数拦截

解锁方法：修改 biz_service 中对应 helper 的企业版检查逻辑，移除或绕过 `checkEnterprise()` 调用。

## 关键代码路径

### 客户端 (KHF)
- ConnectionsManager：`TMessagesProj/jni/tgnet/ConnectionsManager.cpp`
- MessagesController：`TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java`
- TLRPC 定义：`TMessagesProj/src/main/java/org/telegram/tgnet/TLRPC.java`
- BuildVars：`TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java`

### 服务端 (HD/Teamgram)
- gnetway 入口：`app/interface/gnetway/`
- session 路由：`app/interface/session/`
- BFF 模块：`app/bff/`
- biz_service：`app/service/biz/`
- messenger：`app/messenger/`
- 配置文件：`teamgramd/etc/`
- SQL schema：`teamgramd/deploy/sql/`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
