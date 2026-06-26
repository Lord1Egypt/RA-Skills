---
name: teamgram-architecture
description: Overview of Teamgram Server's 6-layer microservice architecture with 11 services, gRPC/Kafka communication, and etcd service discovery for Telegram-compatible messaging backends.
compatibility: Documentation/knowledge skill only. No executable code. Reference material for Teamgram Server developers.
metadata:
  author: zhihang9978
  version: "1.0.1"
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

# Teamgram Server 总体架构概览

## 系统定位

Teamgram Server 是一个 Telegram/MTProto 兼容的微服务系统，配合 KHF Android 客户端使用。

## 分层架构

```text
[KHF Android Client]
    |
    |  MTProto (obfuscated2 / tcp / websocket)
    v
[gnetway: interface.gateway]
    |
    |  gRPC (go-zero zrpc, etcd discovery: interface.session)
    v
[session: interface.session]
    |
    |  gRPC proxy by IDMap (mtproto.RPC* -> bff.bff)
    v
[bff: bff.bff]
    |
    |  gRPC calls (etcd): service.biz_service / service.authsession / service.status / messenger.msg / service.dfs / service.media / service.idgen
    v
[biz_service + others]
    |
    |  Kafka topics:
    |    - Inbox-T (write path)
    |    - Sync-T  (fanout/push path)
    v
[messenger.msg] -> [Kafka Inbox-T] -> [inbox helper]
                         |
                         v
                      [Kafka Sync-T] -> [messenger.sync] -> [session] -> [gnetway] -> [client]
```

## 6 层职责

| 层 | 服务 | 职责 |
|---|---|---|
| **入口层** | gnetway | TCP/WebSocket/HTTP MTProto 网关 |
| **会话路由层** | session | 按 auth_key / session_id 聚合与路由，作为 gnetway 与 BFF 的桥 |
| **BFF 聚合层** | bff.bff | 实现 Telegram RPC 接口的 27 个模块 |
| **核心业务层** | biz_service | 6 个 helper（user/chat/dialog/message/updates/code） |
| **消息投递层** | messenger.msg + inbox | Kafka Inbox-T 写入 inbox/outbox/未读等状态 |
| **同步分发层** | messenger.sync | Kafka Sync-T → 推送 updates/rpcResult 回 session |

## 11 个核心微服务清单

| 服务名 | etcd Key | 端口 | 职责 |
|---|---|---|---|
| **gnetway** | interface.gateway | 10443/5222/11443 | MTProto 网关（TCP/WS/HTTP） |
| **session** | interface.session | 20120 | 会话聚合与 RPC 路由 |
| **authsession** | service.authsession | 20450 | auth_key 管理 |
| **bff** | bff.bff | 20010 | 27个RPC模块聚合层 |
| **biz_service** | service.biz_service | 20500 | 6个helper（user/chat/dialog/message/updates/code） |
| **msg** | messenger.msg | 20030 | 消息投递 + Kafka生产 |
| **inbox** | (Kafka consumer) | - | Inbox-T 消费者（写入 inbox/outbox/未读等状态） |
| **sync** | messenger.sync | 20420 | 同步分发（Kafka→session） |
| **idgen** | service.idgen | 20660 | Snowflake/Seq ID生成 |
| **status** | service.status | 20670 | 在线状态/会话TTL |
| **dfs** | service.dfs | 20640 + 11701 | Minio 文件存储 + HTTP 网关 |
| **media** | service.media | 20650 | 媒体元数据/缩略图处理 |

> 注：msg/inbox/sync 属于 messenger 域的不同子服务/角色。

## 服务间通信方式

1. **gRPC (go-zero zrpc)**：所有微服务间同步调用均使用 gRPC，通过 etcd 服务发现
2. **Kafka 异步消息**：消息投递（Inbox-T）和同步分发（Sync-T）使用 Kafka 解耦
3. **MTProto 二进制协议**：客户端与 gnetway 之间的通信协议

## 配置与服务发现

- 所有服务通过 YAML 声明 `Etcd.Hosts` + `Etcd.Key` 注册到 etcd
- 调用端用同 Key 发现目标服务
- 关键 etcd Key 列表：interface.gateway, interface.session, bff.bff, service.biz_service, service.authsession, service.idgen, service.status, service.dfs, service.media, messenger.msg, messenger.sync


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
