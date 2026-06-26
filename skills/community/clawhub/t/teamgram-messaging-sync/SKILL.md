---
name: teamgram-messaging-sync
description: Documents the message delivery and sync distribution layer in Teamgram Server, covering Kafka Inbox-T/Sync-T topics, inbox/outbox model, and the complete message send flow.
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

# 消息投递与同步层：messenger.msg / inbox / sync

## 概述

Teamgram 的消息投递使用 Kafka 做异步解耦，分为两个主要 topic：
- **Inbox-T**：写路径（发送/编辑/删除等异步投递）
- **Sync-T**：推路径（updates/rpcResult 分发回在线 session）

## messenger.msg 配置

`teamgramd/etc/msg.yaml` 要点：

```yaml
InboxConsumer:
  Topics:
    - "Inbox-T"
  Brokers:
    - 127.0.0.1:9092
  Group: "Inbox-MainCommunity-S"
InboxClient:
  Topic:   "Inbox-T"
SyncClient:
  Topic:   "Sync-T"
```

## 消息发送完整链路

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

## inbox helper：消费 Kafka Inbox-T

inbox 服务通过 Kafka ConsumerGroup 收到消息后，根据 protobuf messageName 分发到对应 core 方法（threading.RunSafe）。

典型模式：
```go
case proto.MessageName((*inbox.TLInboxSendUserMessageToInboxV2)(nil)):
    threading.RunSafe(func() {
        c := core.New(ctx, svcCtx)
        r := new(inbox.TLInboxSendUserMessageToInboxV2)
        json.Unmarshal(value, r)
        c.InboxSendUserMessageToInboxV2(r)
    })
```

inbox 的核心职责：
- 写入收件方的 inbox 消息记录
- 更新未读计数
- 触发通知推送
- 生成 Sync-T 消息通知在线用户

## msg gRPC Service：TL 签名即接口契约

msg 子服务的 gRPC service impl 文件会保留 TL 签名注释，例如：
- `// msg.sendMessageV2 ... = Updates;`

这就是跨服务调用时请求/响应的"格式契约"。

## 同步分发层：messenger.sync（Kafka Sync-T）

sync 服务消费 Kafka `Sync-T`，按 protobuf message name 分发到：
- **SyncUpdatesMe** — 推送给发送者自己（确认消息已发送）
- **SyncUpdatesNotMe** — 推送给非发送者（对方收到新消息通知）
- **SyncPushUpdates** — 通用推送（状态变化等）
- **SyncPushRpcResult** — RPC 结果推送（异步 RPC 的响应）
- **SyncBroadcastUpdates** — 广播推送（群消息等多人场景）

最终通过 gRPC 调用 session 把 updates/rpc_result 推回在线会话。

典型模式：
```go
case proto.MessageName((*sync.TLSyncPushRpcResult)(nil)):
    threading.RunSafe(func() {
        c := core.New(ctx, svcCtx)
        r := new(sync.TLSyncPushRpcResult)
        json.Unmarshal(value, r)
        c.SyncPushRpcResult(r)
    })
```

## Kafka 事件总线总结

| Topic | 生产者 | 消费者 | 内容 |
|---|---|---|---|
| Inbox-T | messenger.msg | inbox helper | 消息投递（发送/编辑/删除） |
| Sync-T | inbox helper / messenger.msg | messenger.sync | Updates/RPC结果分发 |

## 消息存储模型

Teamgram 使用 **inbox/outbox 双写模型**：
- 发送方写入 outbox（自己的消息记录）
- 接收方通过 Kafka Inbox-T 异步写入 inbox（对方的消息记录）
- 每条消息在 messages 表中按 user_id + peer 维度存储
- dialog_message_id 为每个对话内的消息序号（递增）

## 关键代码路径

- msg 服务：`app/messenger/msg/`
- inbox 服务：`app/messenger/msg/internal/dao/inbox/` (Kafka consumer)
- sync 服务：`app/messenger/sync/`
- 配置文件：`teamgramd/etc/msg.yaml`, `teamgramd/etc/sync.yaml`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
