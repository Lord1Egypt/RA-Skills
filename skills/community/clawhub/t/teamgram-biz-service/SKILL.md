---
name: teamgram-biz-service
description: Documents the biz_service core business layer in Teamgram Server with 6 RPC helpers covering user, chat, dialog, message, updates, and verification code management.
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
      Config snippets show localhost-only addresses from the default development setup.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# 业务逻辑层：biz_service（6 个 helper）

## 概述

biz_service 是一个"组合服务"，在一个 gRPC server 中注册 6 个子服务：
- **RPCChat** — 群组/频道管理
- **RPCCode** — 验证码管理
- **RPCDialog** — 对话管理
- **RPCMessage** — 消息构造/权限校验/写DB
- **RPCUpdates** — Updates 构造
- **RPCUser** — 用户读取/搜索

## etcd 注册

它们都以 `service.biz_service` 注册到 etcd，供 BFF/msg/sync 等发现调用。

## 典型调用关系

| 调用方 | 目标 helper | 场景 |
|---|---|---|
| BFF.messages | biz_service.message | 构造消息/权限校验/写DB |
| BFF.users | biz_service.user | 用户读取/搜索 |
| BFF.contacts | biz_service.user + biz_service.dialog | 联系人与对话 |
| BFF.chats | biz_service.chat | 群/频道管理 |
| BFF.updates | biz_service.updates | updates 构造 |
| BFF.authorization | biz_service.code + biz_service.user | 登录注册流程 |

## 配置

```yaml
Name: service.biz_service
ListenOn: 127.0.0.1:20500
Etcd:
  Key: service.biz_service
  Hosts:
    - 127.0.0.1:2379
Mysql:
  DSN: root:@tcp(127.0.0.1:3306)/teamgram?charset=utf8mb4&parseTime=true
Cache:
  - Host: 127.0.0.1:6379
```

## 6 个 helper 详解

### RPCUser
- 用户注册、查询、搜索
- 手机号→用户映射
- 用户资料读写（名字、头像、简介等）
- 在线状态查询
- 被调用最频繁的 helper，几乎所有 BFF 模块都依赖

### RPCChat
- 创建/删除群组
- 群成员管理（添加/删除/设管理员）
- 群标题/头像/权限设置
- 群迁移到超级群
- 群禁言/封禁权限管理

### RPCDialog
- 对话列表查询（分页、筛选）
- 对话置顶/归档/标记未读
- 对话未读数管理（read_inbox_max_id / unread_count）
- 会话 TTL 设置
- 对话文件夹管理

### RPCMessage
- 消息构造与入库（inbox/outbox 双写模型）
- 消息权限校验（是否被禁言、是否被屏蔽等）
- 消息 ID 生成（依赖 idgen 服务的 Snowflake ID）
- 消息编辑/删除/转发
- 消息搜索（全文、hashtag）

### RPCUpdates
- Updates 序列号管理（pts/qts/seq）
- 差异更新构造（getDifference）
- 状态查询（getState）
- 确保客户端与服务端状态同步

### RPCCode
- 验证码生成与校验
- 短信/App code 管理
- 验证码过期与重试逻辑
- 支持自定义验证码发送插件（VerifyCodeInterface）

## 关键代码路径

- 主服务入口：`app/service/biz/`
- 各 helper 实现：`app/service/biz/internal/core/`
- DAO 层：`app/service/biz/internal/dao/`
- 配置文件：`teamgramd/etc/biz_service.yaml`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
