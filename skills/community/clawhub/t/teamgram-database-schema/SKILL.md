---
name: teamgram-database-schema
description: Complete database schema reference for Teamgram Server with all 43 tables, ER relationships, and key table structure explanations for the MySQL teamgram database.
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
      Table names and schema are from the public teamgram-server SQL files.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# 数据库 Schema（43 张表）与核心关系

## 概述

数据库位于 `teamgramd/deploy/sql/`，基础 schema 在 `1_teamgram.sql`（38 表），迁移补齐到 43 表。

所有服务共用同一个 MySQL 数据库 `teamgram`，字符集 `utf8mb4`。

## 43 张表完整列表

| 表名 | 核心用途 |
|---|---|
| auth_key_infos | auth_key 元信息 |
| auth_keys | auth_key 存储（加密密钥） |
| auth_seq_updates | 每个 auth_key 的 updates 序列号 |
| auth_users | auth_key ↔ user 绑定关系 |
| auths | 授权记录 |
| bot_commands | Bot 命令列表 |
| bots | Bot 信息 |
| chat_invite_participants | 通过邀请链接加入的成员 |
| chat_invites | 聊天邀请链接 |
| chat_participants | 群成员关系 |
| chats | 群组信息 |
| default_history_ttl | 默认历史消息 TTL |
| devices | 推送设备/token |
| dialog_filters | 对话文件夹 |
| dialogs | 对话列表（每用户每对等方一行） |
| documents | 文件/文档元数据 |
| drafts | 消息草稿 |
| encrypted_files | 加密文件 |
| hash_tags | 消息 hashtag 索引 |
| imported_contacts | 导入的联系人 |
| message_read_outbox | 消息已读状态（outbox 侧） |
| messages | 消息存储（核心表） |
| phone_books | 通讯录 |
| photo_sizes | 照片尺寸变体 |
| photos | 照片元数据 |
| popular_contacts | 热门联系人 |
| predefined_users | 预定义用户 |
| saved_dialogs | 保存的消息对话 |
| unregistered_contacts | 未注册联系人 |
| user_contacts | 用户联系人关系 |
| user_global_privacy_settings | 全局隐私设置 |
| user_notify_settings | 通知设置 |
| user_peer_blocks | 屏蔽关系 |
| user_peer_settings | 对等方设置 |
| user_presences | 用户最后上线时间 |
| user_privacies | 隐私规则 |
| user_profile_photos | 用户头像 |
| user_pts_updates | 每用户 pts 更新序列 |
| user_saved_music | 保存的音乐 |
| user_settings | 用户设置 |
| username | 用户名 |
| users | 用户信息（核心表） |
| video_sizes | 视频尺寸变体 |

## 核心 ER 关系

```text
users (user_id)
  |\
  | \-- auth_users (auth_key_id -> user_id)      # 登录设备/授权关系
  | \-- devices (auth_key_id, user_id)           # push token / device
  | \-- user_presences (user_id)                 # last seen
  | \-- user_profile_photos (user_id -> photo_id)
  | \-- user_settings / user_privacies / user_notify_settings
  |
  \-- dialogs (user_id, peer_type, peer_id)      # 会话列表
        |
        \-- messages (user_id, peer_type, peer_id, dialog_id1/2, dialog_message_id)
              |
              \-- documents/photos/encrypted_files (+ photo_sizes/video_sizes)

chats (chat_id)
  \-- chat_participants (chat_id, user_id)
  \-- chat_invites / chat_invite_participants
```

## 关键表结构说明

### users 表
- 核心用户信息表
- user_id 为主键（Snowflake ID）
- 包含 phone、first_name、last_name、username 等字段
- deleted 字段标记软删除

### messages 表
- 消息存储核心表
- 按 user_id + peer 维度存储（inbox/outbox 双写）
- dialog_id1/dialog_id2 用于双向对话定位
- dialog_message_id 为对话内消息序号（递增）
- message_type 区分文本/媒体/服务消息等

### dialogs 表
- 每个用户与每个对等方（私聊/群聊）一行
- peer_type: 1=user, 2=chat, 3=channel
- 包含 unread_count、read_inbox_max_id、read_outbox_max_id
- pinned 字段控制置顶排序

### auth_keys / auth_users 表
- auth_keys 存储 MTProto 授权密钥（256字节 auth_key）
- auth_users 维护 auth_key_id → user_id 的绑定
- 一个用户可以有多个 auth_key（多设备登录）
- auth_key_id 是 auth_key 的 SHA1 后 8 字节

### chat_participants 表
- chat_id + user_id 复合主键
- participant_type 区分普通成员/管理员/创建者
- inviter_user_id 记录邀请人
- joined_at 记录加入时间

## SQL 文件路径

- 基础 schema：`teamgramd/deploy/sql/1_teamgram.sql`
- 迁移脚本：`teamgramd/deploy/sql/` 下的后续编号文件


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
