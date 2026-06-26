---
name: teamgram-gnetway-gateway
description: Documents the gnetway network gateway layer in Teamgram Server, covering TCP/WS/HTTP listeners, connection lifecycle, MTProto decryption, QuickAck, and session dispatch.
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
      All content references the open-source teamgram-server project (Apache-2.0).
---

# 网络层：gnetway（interface.gateway）

## 监听端口与协议

来自配置 `teamgramd/etc/gnetway.yaml`：

```yaml
Gnetway:
  Server:
    - Proto: tcp
      Addresses:
        - 0.0.0.0:10443
        - 0.0.0.0:5222
    - Proto: websocket
      Addresses:
        - 0.0.0.0:11443
```

| 协议 | 端口 | 说明 |
|---|---|---|
| TCP | 0.0.0.0:10443 | 主要 MTProto TCP 端口 |
| TCP | 0.0.0.0:5222 | 备用 TCP 端口 |
| WebSocket | 0.0.0.0:11443 | WebSocket 连接入口 |

- gnetway 通过 etcd 发现 session：`Key: interface.session`

## 连接生命周期

### OnOpen
- 根据本地监听地址判断连接类型（tcp/ws/http）
- 创建 connContext
- 设置 closeDate
- 放入 timewheel 管理超时

### OnClose
- 对非 HTTP 连接，如果已存在 perm_auth_key
- 通知 session.CloseSession（回收会话、清理在线状态等）

## 加密消息处理流程

```text
收到加密数据
  → authKey.AesIgeDecrypt 解密
  → 提取 salt、sessionId、msgId
  → SessionDispatcher.SendData (gRPC) 转发给 session 服务
```

核心点：
- 通过 `authKey.AesIgeDecrypt` 解密
- 从解密后 payload 头部提取：`salt`、`sessionId`、`msgId`
- 通过 `SessionDispatcher.SendData`（gRPC）把 `payload[16:]` 转发给 session

## auth_key 缓存与 QueryAuthKey

当 connContext 中没有 authKey（首次连接或缓存未命中）：
1. 异步调用 session 的 `QueryAuthKey`
2. 获取 authKey 后存入 connContext
3. 执行 `onEncryptedMessage` 处理加密消息

## QuickAck

QuickAck token 通过 SHA256(authKey[88:120] + encryptedData) 前 4 字节计算，最高位置 1。
必须通过 codec 编码发送，否则 obfuscated CTR 计数器不同步，导致客户端解密失败。

## 关键代码路径

- 主服务入口：`app/interface/gnetway/`
- gnet 服务器实现：`app/interface/gnetway/internal/server/gnet/server_gnet.go`
- 配置文件：`teamgramd/etc/gnetway.yaml`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
