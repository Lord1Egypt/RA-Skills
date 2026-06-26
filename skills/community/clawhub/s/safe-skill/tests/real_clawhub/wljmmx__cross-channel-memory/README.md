# 跨渠道记忆同步 Skill

## 功能概述

实现 QQ、飞书等多渠道用户身份识别和记忆共享。当用户在不同渠道与机器人对话时，agent 能识别同一用户并读取统一记忆。

## 核心能力

- **用户身份统一**：同一用户在不同渠道使用同一身份标识
- **记忆共享**：各渠道的对话记录统一存储，可跨渠道查询
- **独立存储**：每个 agent 的记忆保存在自己的 workspace 目录
- **实时同步**：写入时自动同步到所有关联 agent

## 快速开始

### 1. 初始化用户映射

```bash
# 创建统一用户
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py add-user \
  --id "用户标识" \
  --name "显示名称"

# 绑定 QQ 渠道
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py link \
  --user "用户标识" \
  --channel qqbot \
  --channel-id "QQ用户ID" \
  --account "agent标识"

# 绑定飞书渠道
python3 ~/.openclaw/skills/cross-channel-memory/scripts/init_mapping.py link \
  --user "用户标识" \
  --channel feishu \
  --channel-id "飞书用户ID" \
  --account "agent标识"
```

### 2. 查找用户

```bash
python3 ~/.openclaw/skills/cross-channel-memory/scripts/memory_sync.py lookup \
  --channel qqbot \
  --id "用户ID"
```

### 3. 写入记忆

```bash
python3 ~/.openclaw/skills/cross-channel-memory/scripts/memory_sync.py write \
  --channel qqbot \
  --id "用户ID" \
  --type user \
  --content "用户消息内容"
```

### 4. 读取记忆

使用 OpenClaw 内置工具：
```
memory_search(query: "关键词", path: "~/.openclaw/workspace/coder/memory")
```

## 文件结构

```
~/.openclaw/
├── skills/
│   └── cross-channel-memory/
│       ├── SKILL.md              # 技能文档
│       ├── README.md             # 使用说明
│       ├── scripts/
│       │   ├── init_mapping.py   # 初始化工具
│       │   ├── lookup_user.py    # 用户查找
│       │   └── memory_sync.py   # 记忆同步
│       └── examples/
│           └── sample_mapping.json
├── data/
│   └── cross-channel-users.json  # 用户映射数据
└── workspace/
    ├── coder/memory/              # coder agent 记忆
    ├── main/memory/               # main agent 记忆
    └── checker/memory/            # checker agent 记忆
```

## Agent 集成指南

### 接收消息时

1. 从 inbound_meta 获取 `channel` 和 `sender_id`
2. 调用 `lookup_user.py` 查找统一用户 ID
3. 如果找到，使用该用户的记忆路径

### 写入记忆时

使用 `memory_sync.py write` 命令，自动同步到所有关联 agent

### 查询记忆时

使用内置 `memory_search` 工具，指定正确的记忆路径

## 渠道支持

| 渠道 | 用户ID来源 |
|------|-----------|
| QQ (qqbot) | inbound_meta.sender_id |
| 飞书 (feishu) | inbound_meta.sender_id / open_id |

## 注意事项

1. 首次使用需初始化用户映射
2. 用户映射数据是全局共享的
3. 记忆按 agent 分离存储
4. 支持增量添加新渠道映射

---

版本: 1.0.0
更新: 2026-03-13