---
name: cross-channel-memory
description: 跨渠道记忆同步。实现QQ、飞书等多渠道用户身份识别和记忆共享。当用户在不同渠道与机器人对话时，agent能识别同一用户并读取统一记忆。触发条件：用户提到"跨渠道"、"多渠道"、"飞书和QQ"、"记忆同步"、"换渠道聊"，或agent需要查询用户跨渠道历史时。
version: 1.2.0
author: OpenClaw
---

# 跨渠道记忆同步

## 概述

实现多渠道用户身份映射，让不同 agent 在 QQ、飞书等渠道识别同一用户，并共享记忆。

**核心特性：**
- 用户身份统一：同一用户在不同渠道使用同一身份标识
- 记忆共享：各渠道的对话记录统一存储，可跨渠道查询
- 独立存储：每个 agent 的记忆保存在自己的 workspace 目录
- 实时同步：写入时自动同步到所有关联 agent

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    用户映射中心                              │
│         ~/.openclaw/data/cross-channel-users.json           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ users: {                                            │    │
│  │   "xiaokeai": {                                     │    │
│  │     displayName: "小可爱",                           │    │
│  │     channels: {                                     │    │
│  │       qqbot: { main: "QQ_ID_123" },                 │    │
│  │       feishu: { main: "ou_abc123" }                 │    │
│  │     }                                               │    │
│  │   }                                                 │    │
│  │ }                                                   │    │
│  │ lookupIndex: {                                      │    │
│  │   qqbot: { "QQ_ID_123": { userId: "xiaokeai" } },   │    │
│  │   feishu: { "ou_abc123": { userId: "xiaokeai" } }   │    │
│  │ }                                                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   main      │ │   coder     │ │  checker    │
    │  workspace  │ │  workspace  │ │  workspace  │
    │             │ │             │ │             │
    │ memory/     │ │ memory/     │ │ memory/     │
    │ ├MEMORY.md  │ │ ├MEMORY.md  │ │ ├MEMORY.md  │
    │ └YYYY-MM-DD│ │ └YYYY-MM-DD│ │ └YYYY-MM-DD│
    └─────────────┘ └─────────────┘ └─────────────┘
```

## 使用方法

### 步骤 1：初始化用户映射

在用户首次使用时，需要建立渠道用户 ID 与统一用户 ID 的映射（按 agent 精确绑定）：

```bash
# QQ coder agent 绑定
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py link \
  --user "xiaokeai" \
  --channel qqbot \
  --channel-id "QQ_USER_ID" \
  --account coder

# 飞书 coder agent 绑定（同一用户）
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py link \
  --user "xiaokeai" \
  --channel feishu \
  --channel-id "FEISHU_USER_ID" \
  --account coder

# 飞书 main agent 绑定（同一用户，不同 agent）
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py link \
  --user "xiaokeai" \
  --channel feishu \
  --channel-id "FEISHU_USER_ID" \
  --account main
```

参数说明：
- `--user`: 统一用户 ID (自定义，用于跨渠道识别)
- `--channel`: 渠道名称 (qqbot, feishu)
- `--channel-id`: 渠道中的用户 ID
- `--account`: agent 标识 (coder, main, checker, menowriter 等)

### 步骤 2：查找用户信息（按 agent 精确查找）

根据渠道用户 ID 和 agent 查找统一用户信息：

```bash
python3 ~/.openclaw/skills/cross-channel-memory/scripts/memory_sync.py lookup \
  --channel qqbot \
  --id "QQ_USER_ID" \
  --account coder
```

返回：
```json
{
  "userId": "xiaokeai",
  "displayName": "小可爱",
  "memoryPaths": [
    { "accountId": "coder", "memoryPath": "/home/user/.openclaw/workspace/coder/memory" }
  ],
  "accountId": "coder"
}
```

### 步骤 3：写入记忆（按 agent 精确写入）

将对话记录写入指定 agent 的记忆：

```bash
python3 ~/.openclaw/skills/cross-channel-memory/scripts/memory_sync.py write \
  --channel qqbot \
  --id "QQ_USER_ID" \
  --account coder \
  --type user \
  --content "我想学习 Python 编程" \
  --timestamp "2026-03-13T08:30:00"
```

### 步骤 4：读取记忆

使用内置工具读取记忆：

```
memory_search(query: "Python", path: "~/.openclaw/workspace/coder/memory")
```

## 渠道识别字段

| 渠道 | 用户ID字段 | 来源 |
|------|-----------|------|
| QQ (qqbot) | `sender_id` | inbound_meta.sender_id |
| 飞书 (feishu) | `sender_id` / `open_id` | inbound_meta.sender_id |

## 目录结构

```
~/.openclaw/
├── skills/
│   └── cross-channel-memory/
│       ├── SKILL.md              # 本文档
│       ├── scripts/
│       │   ├── lookup_user.py    # 用户查找工具
│       │   ├── memory_sync.py    # 记忆同步工具
│       │   └── init_mapping.py   # 初始化脚本
│       └── examples/
│           └── sample_mapping.json
├── data/
│   └── cross-channel-users.json  # 用户映射（共享）
└── workspace/
    ├── main/memory/              # main agent 记忆
    ├── coder/memory/             # coder agent 记忆
    └── checker/memory/           # checker agent 记忆
```

## 配置示例

### cross-channel-users.json（按 agent 精确绑定）

```json
{
  "users": {
    "xiaokeai": {
      "displayName": "小可爱",
      "channels": {
        "qqbot": {
          "coder": "QQ_USER_ID_C"
        },
        "feishu": {
          "coder": "FEISHU_USER_ID_C",
          "main": "FEISHU_USER_ID_M",
          "checker": "FEISHU_USER_ID_K",
          "menowriter": "FEISHU_USER_ID_W"
        }
      }
    }
  },
  "lookupIndex": {
    "qqbot": {
      "QQ_USER_ID_C_coder": {
        "userId": "xiaokeai",
        "accountId": "coder",
        "channelUserId": "QQ_USER_ID_C"
      }
    },
    "feishu": {
      "FEISHU_USER_ID_C_coder": {
        "userId": "xiaokeai",
        "accountId": "coder",
        "channelUserId": "FEISHU_USER_ID_C"
      },
      "FEISHU_USER_ID_M_main": {
        "userId": "xiaokeai",
        "accountId": "main",
        "channelUserId": "FEISHU_USER_ID_M"
      }
    }
  }
}
```

**绑定关系：**
- QQ coder agent ← 用户 `QQ_USER_ID_C` → 统一用户 `xiaokeai` → 飞书 coder agent
- QQ main agent ← 用户 `QQ_USER_ID_M` → 统一用户 `xiaokeai` → 飞书 main agent
- 每个渠道的每个 agent 精确绑定，记忆独立存储

## Agent 使用流程

### 接收消息时

1. 从 inbound_meta 获取 channel 和 sender_id
2. 调用 lookup_user.py 查找统一用户 ID
3. 如果找到，使用该用户的记忆路径

### 写入记忆时

1. 使用 memory_sync.py write 命令
2. 自动同步到用户关联的所有 agent

### 查询记忆时

1. 使用 memory_search 工具
2. 指定正确的记忆路径

## 注意事项

1. **用户映射是共享的**：所有 agent 使用同一份映射文件
2. **记忆按 agent 分离**：各 agent 的记忆独立存储在自己的 workspace
3. **首次使用需初始化**：新用户需要先建立映射关系
4. **支持增量更新**：可随时添加新的渠道映射

## 与内置 memory 工具配合

本 skill 与 OpenClaw 内置的 memory_search/memory_get 工具配合使用：

```python
# 先用本 skill 查找用户
user_info = lookup_user(channel="qqbot", user_id="xxx")

# 再用内置工具搜索记忆
memory_search(query="Python", path=user_info["memoryPath"])
```

## 最佳实践

### 用户 ID 映射策略

1. **统一 ID 命名**：建议使用易识别的 ID，如用户昵称的拼音
2. **渠道 ID 格式**：直接使用渠道提供的原始 ID
3. **agent 绑定**：如用户使用多个 agent，分别记录每个 agent 的渠道 ID

### 记忆存储建议

1. **按日期组织**：每日记忆存储在 `YYYY-MM-DD.md`
2. **重要信息**：永久记忆存储在 `MEMORY.md`
3. **定期整理**：建议定期将重要信息从日记忆迁移到永久记忆

---

## 更新日志

- **v1.1.0** (2026-03-13): 按 agent 精确绑定，QQ coder → 飞书 coder，支持多 agent 独立记忆
- **v1.0.0** (2026-03-13): 初始版本，支持 QQ 和飞书渠道