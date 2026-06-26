---
name: three-layer-memory
description: "三层记忆系统 + LanceDB Pro 整合版。热/暖/冷记忆自动管理，结合向量数据库实时提取与结构化排程维护。Micro Sync（每天5次扫session记决策+审核autoCapture）、Daily Wrap Up（每天凌晨结构化摘要）、Weekly Compound（每周记忆减脂+蒸馏+向量清理）。含去重检测、scope隔离、archive机制。触发词：记忆系统、memory system、安装记忆、记忆管理、micro sync、daily wrapup、weekly compound、lancedb。"
---

# 三层记忆系统（+ LanceDB Pro 整合版）

## 架构概览

```
┌─────────────────────────────────────────────┐
│        Structured Vector Memory (SVM)       │
│         三层记忆 × LanceDB Pro              │
├─────────────────────────────────────────────┤
│                                             │
│  🔴 热层（每次加载）                         │
│  ├── MEMORY.md（人类可读索引，≤8KB）         │
│  ├── SOUL/USER/AGENTS.md                    │
│  └── autoRecall（LanceDB 向量注入 top-N）   │
│                                             │
│  🟡 暖层（自动维护）                         │
│  ├── autoCapture → LanceDB（实时抓取）      │
│  ├── Micro Sync → 验证+标注 scope           │
│  ├── Daily Wrapup → markdown 摘要           │
│  └── 去重：向量相似度 >0.85 跳过            │
│                                             │
│  🔵 冷层（按需查询）                         │
│  ├── archive/（从热层退休的 markdown）       │
│  ├── LanceDB 全量（向量搜索可达）           │
│  └── second-brain/（深度报告）              │
│                                             │
├─────────────────────────────────────────────┤
│  Weekly Compound：                          │
│  ├── MEMORY.md 减脂                         │
│  ├── LanceDB 清理低价值记忆                 │
│  └── Scope 审计                             │
└─────────────────────────────────────────────┘
```

## 双引擎分工

| 引擎 | 职责 | 触发 |
|------|------|------|
| **LanceDB Pro** | 实时抓取 + 向量存储 + 混合检索 + rerank | 自动（autoCapture/autoRecall） |
| **三层记忆** | 结构化分层 + 排程维护 + scope 隔离 + 人类可读 | cron 排程 |

**简单说：LanceDB 做实时引擎，三层记忆做管理策略。**

## 安装

### 前置条件
- OpenClaw 已安装
- memory-lancedb-pro 插件已安装（`clawhub install memory-lancedb-pro`）
- Jina API Key（embedding + rerank）

### 1. 创建目录结构
```bash
mkdir -p ~/.openclaw/workspace/memory/archive
mkdir -p ~/.openclaw/workspace/second-brain/summaries
```

### 2. 配置 LanceDB Pro
确保 `openclaw.json` 中：
```json
{
  "plugins": {
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "autoCapture": true,
          "autoRecall": true
        }
      }
    }
  }
}
```

### 3. 安装 cron 脚本
```bash
cp scripts/micro-sync.sh ~/.openclaw/shared/
cp scripts/daily-wrapup.sh ~/.openclaw/shared/
cp scripts/weekly-compound.sh ~/.openclaw/shared/
chmod +x ~/.openclaw/shared/*.sh
```

### 4. 配置 cron
```bash
crontab -e
0 10,13,16,19,22 * * * ~/.openclaw/shared/micro-sync.sh >> ~/.openclaw/logs/micro-sync.log 2>&1
0 1 * * * ~/.openclaw/shared/daily-wrapup.sh >> ~/.openclaw/logs/daily-wrapup.log 2>&1
0 3 * * 0 ~/.openclaw/shared/weekly-compound.sh >> ~/.openclaw/logs/weekly-compound.log 2>&1
```

### 5. 在 AGENTS.md 中加入规则
参考 `references/agents-rules.md`。

## 排程总览

| 排程 | 频率 | 脚本 | 作用 |
|------|------|------|------|
| Micro Sync | 每天 5 次 | `micro-sync.sh` | 扫 session 记决策 + 审核 autoCapture |
| Daily Wrap Up | 每天 01:00 | `daily-wrapup.sh` | 全天结构化摘要 |
| Weekly Compound | 每周日 03:00 | `weekly-compound.sh` | 记忆减脂+蒸馏+archive |

## Micro Sync 执行规则

1. `sessions_list` 查最近 3 小时活跃 session
2. `sessions_history` 逐个扫描
3. **去重**：`memory_recall` 查重，相似 >70% 则 `memory_update` 不新建
4. **Scope 标注**：按内容分配 scope（见 references/agents-rules.md）
5. **LanceDB 审核**：检查 autoCapture 最近抓的记忆，删除垃圾/闲聊
6. 写入 `memory/YYYY-MM-DD.md`（APPEND）
7. 完成后删除 HEARTBEAT 对应段落

## Scope 隔离规则

| 内容类型 | scope |
|----------|-------|
| 投资/财务/税务 | `agent:finance` |
| 电商/选品/供应商 | `agent:ecommerce` |
| 内容/YouTube/小红书 | `agent:content` |
| 系统/技术/Gateway | `agent:tech` |
| 跨 agent 共用 | global |

## Daily Wrap Up 摘要格式

```markdown
# YYYY-MM-DD 每日摘要
## Decisions（确定的决策）
## Action Items（待办事项）
## Key Conversations（关键对话摘要）
## Technical Notes（技术笔记/踩坑）
## Pending（未完成/待续）
## Tomorrow（明天要做的事）
```
