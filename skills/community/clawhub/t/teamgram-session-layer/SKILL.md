---
name: teamgram-session-layer
description: Documents the session routing layer and authsession service in Teamgram Server, covering auth_key aggregation, IDMap routing, MainAuthWrapper, and backpressure mechanisms.
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
      Config snippets show localhost-only listen addresses from the default development setup.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# 会话层：session（interface.session）与认证服务（authsession）

## session 服务职责

session 的职责是把来自 gnetway 的 TLMessage2 流：
- 按 `auth_key_id`（Perm/Temp/MediaTemp）聚合
- 按 `session_id` 维护多个 session（一个 authKey 下可以有多个会话）
- 维护 salt 缓存（future_salt）
- 构造 go-zero RPC metadata 并把请求丢到 RPC 队列
- 把 sync 服务推送回来的 updates/rpcResult 分发到具体 session 连接

## session → BFF 的路由机制（IDMap）

`teamgramd/etc/session.yaml` 中的 `BFFProxyClients.IDMap` 是关键：所有 `/mtproto.RPC*` 都路由到 `bff.bff`。

```yaml
BFFProxyClients:
  Clients:
    - Etcd:
        Key: bff.bff
  IDMap:
    "/mtproto.RPCTos": "bff.bff"
    "/mtproto.RPCConfiguration": "bff.bff"
    "/mtproto.RPCAuthorization": "bff.bff"
    "/mtproto.RPCMessages": "bff.bff"
    "/mtproto.RPCContacts": "bff.bff"
    "/mtproto.RPCChats": "bff.bff"
    "/mtproto.RPCUsers": "bff.bff"
    "/mtproto.RPCUpdates": "bff.bff"
    "/mtproto.RPCFiles": "bff.bff"
    "/mtproto.RPCDialogs": "bff.bff"
    "/mtproto.RPCDrafts": "bff.bff"
    "/mtproto.RPCNotification": "bff.bff"
    "/mtproto.RPCAccount": "bff.bff"
    "/mtproto.RPCAutodownload": "bff.bff"
    "/mtproto.RPCNsfw": "bff.bff"
    "/mtproto.RPCChatInvites": "bff.bff"
    "/mtproto.RPCPrivacySettings": "bff.bff"
    "/mtproto.RPCUsernames": "bff.bff"
    "/mtproto.RPCPassport": "bff.bff"
    "/mtproto.RPCQrcode": "bff.bff"
    "/mtproto.RPCMiscellaneous": "bff.bff"
    "/mtproto.RPCSponsoredMessages": "bff.bff"
    "/mtproto.RPCPremium": "bff.bff"
    "/mtproto.RPCSavedMessageDialogs": "bff.bff"
    "/mtproto.RPCUserChannelProfiles": "bff.bff"
    "/mtproto.RPCPasskey": "bff.bff"
    "/mtproto.RPCVoipCalls": "bff.bff"
```

**重要**：如果新增 BFF 模块，必须在此 IDMap 中添加对应路由，否则 session 层会返回 `METHOD_NOT_IMPL` 错误。

## MainAuthWrapper：三种 auth key 统一管理

`MainAuthWrapper` 内部维护三个 `SessionList`：
- `mainAuth` (PermAuthKey) — 主持久授权密钥
- `tempAuth` — 临时授权密钥
- `mediaTempAuth` — 媒体临时授权密钥

通过以下 channel 解耦：
- `sessionDataChan`（数据面：来自 gnetway/sync 的 payload）
- `rpcQueue`（控制面：批量 RPC 调用队列）

## 背压与可靠性：runLoop + rpcRunLoop

- `runLoop`：消费 sessionDataChan，按类型调用 `onSessionData/onSyncData/...`
- `rpcRunLoop`：从 rpcQueue Pop 一批 rpcApiMessage，统一调用 `doRpcRequest`

在 channel 满时返回 `ErrDataChannelFull`，让上游感知"拥塞"而不是 silent drop。

---

## 认证状态：authsession（service.authsession）

authsession 服务的定位是：
- 持久化与管理 auth_key 与用户绑定（AuthKeyId ↔ UserId）
- 记录客户端 initConnection / layer / device 信息（供风控、推送、在线状态等使用）
- 支撑 session 层的 QueryAuthKey / SetLayer / BindAuthKeyUser 等调用

配置（`teamgramd/etc/authsession.yaml`）要点：

```yaml
Name: service.authsession
ListenOn: 127.0.0.1:20450
Etcd:
  Key: service.authsession
Mysql:
  DSN: root:@tcp(127.0.0.1:3306)/teamgram?charset=utf8mb4&parseTime=true
Cache:
  - Host: 127.0.0.1:6379
KV:
  - Host: 127.0.0.1:6379
```

## 关键代码路径

- session 主服务入口：`app/interface/session/`
- session 配置文件：`teamgramd/etc/session.yaml`
- authsession 服务：`app/service/authsession/`
- authsession 配置：`teamgramd/etc/authsession.yaml`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
