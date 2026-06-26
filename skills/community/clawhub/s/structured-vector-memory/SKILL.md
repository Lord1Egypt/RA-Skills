---
name: structured-vector-memory
description: "Structured Vector Memory (SVM) / 三层高效记忆存储法。整合 LanceDB Pro 向量引擎 + 三层结构化管理，涵盖：每日记忆整理（Micro Sync + Daily Wrapup）、记忆蒸馏压缩（Weekly Compound）、去重检测、scope 隔离、archive 机制。触发词：记忆系统、memory system、安装记忆、记忆管理、micro sync、daily wrapup、weekly compound、lancedb、整理记忆、记忆维护、记忆蒸馏、压缩上下文、精简记忆、context瘦身、consolidate memory。"
---

# Structured Vector Memory (SVM)
## 三层高效记忆存储法

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
│  ├── MEMORY.md 减脂（蒸馏压缩）             │
│  ├── LanceDB 清理低价值记忆                 │
│  └── Scope 审计（检查标签正确性）            │
└─────────────────────────────────────────────┘
```

## 双引擎分工

| 引擎 | 职责 | 触发 |
|------|------|------|
| **LanceDB Pro** | 实时抓取 + 向量存储 + 混合检索 + rerank | 自动（autoCapture/autoRecall） |
| **三层记忆** | 结构化分层 + 排程维护 + scope 隔离 + 人类可读 | cron 排程 |

**简单说：LanceDB 做实时引擎，三层记忆做管理策略。**

---

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

---

## 排程总览

| 排程 | 频率 | 脚本 | 作用 |
|------|------|------|------|
| Micro Sync | 每天 5 次（10/13/16/19/22） | `micro-sync.sh` | 扫 session 记决策 + 审核 autoCapture |
| Daily Wrap Up | 每天 01:00 | `daily-wrapup.sh` | 全天结构化摘要 |
| Weekly Compound | 每周日 03:00 | `weekly-compound.sh` | 记忆减脂+蒸馏+archive+向量清理 |

---

## 每日记忆整理（原 daily-memory skill）

### 触发时机
- **自动：** Micro Sync cron（每天 5 次）
- **自动：** Daily Wrapup cron（每天 01:00）
- **手动：** 用户说「整理记忆」时

### 当日记录格式
```markdown
# YYYY-MM-DD Daily Memory

## 主题1
- 要点

## 主题2
- 要点
```

### 什么值得记录
✅ 架构决策、踩过的坑、用户偏好变化、重要项目里程碑、新规则
❌ 日常对话细节、一次性任务、临时调试记录、闲聊

---

## Micro Sync 执行规则

1. `sessions_list` 查最近 3 小时活跃 session
2. `sessions_history` 逐个扫描
3. **决策过滤**：只记确定的决策、新规则、架构变更、「记住 XXX」指令
4. **去重**：`memory_recall` 查重，相似 >70% 则 `memory_update` 不新建
5. **Scope 标注**：按内容分配 scope
6. **LanceDB 审核**：检查 autoCapture 最近抓的记忆，删除垃圾/闲聊
7. 写入 `memory/YYYY-MM-DD.md`（APPEND）
8. 完成后删除 HEARTBEAT 对应段落

---

## 记忆蒸馏（原 memory-distill skill）

### 触发时机
- **自动：** Weekly Compound cron（每周日 03:00）
- **手动：** 用户说「蒸馏记忆」「压缩上下文」时

### 蒸馏流程

#### Step 1: 量体
```bash
cd ~/.openclaw/workspace
wc -c AGENTS.md SOUL.md TOOLS.md USER.md IDENTITY.md MEMORY.md HEARTBEAT.md
```
MEMORY.md 安全线：**≤8KB**

#### Step 2: 备份（铁律）
```bash
mkdir -p _backup/$(date +%Y-%m-%d)
cp MEMORY.md AGENTS.md _backup/$(date +%Y-%m-%d)/
```

#### Step 3: 识别冗余
- [ ] 跨文件重复 — 同一信息出现在多个文件
- [ ] 过时信息 — 已完成的待办、已解决的问题
- [ ] 冗长表述 — 能一行说清的别用一段
- [ ] LanceDB 低价值记忆 — 清理无用向量

#### Step 4: 精简
优先级：MEMORY.md > AGENTS.md > TOOLS.md > USER.md/IDENTITY.md
**SOUL.md 绝对不动。**
过时内容搬到 `memory/archive/`，不删除。

#### Step 5: 验证
蒸馏后冒烟测试：
- 用户身份信息还在？
- 架构分层还清楚？
- 安全红线还知道？
- 关键项目信息还在？

#### 回滚
```bash
cp _backup/YYYY-MM-DD/* ~/.openclaw/workspace/
```

---

## Scope 隔离规则

| 内容类型 | scope |
|----------|-------|
| 投资/财务/税务 | `agent:finance` |
| 电商/选品/供应商 | `agent:ecommerce` |
| 内容/YouTube/小红书 | `agent:content` |
| 系统/技术/Gateway | `agent:tech` |
| 跨 agent 共用 | global |

## 实体与关系管理（原 structured-memory Relationship 层）

用 `memory_store` 的 `entity` category 管理人物、公司、服务等实体关系：
```
memory_store(text="...", category="entity", scope="global")
```
适用于：公司注册信息、人物关系、外部服务配置、供应商信息等。
查询：`memory_recall(query="...", category="entity")`

---

## 去重规则（memory_store 前必做）

存 `memory_store` 之前**必须**先 `memory_recall` 查重：
- 相似度 >70% → `memory_update` 更新旧记忆，不新建
- 部分重叠 → 合并信息后 `memory_update`
- 无相似 → `memory_store` 新建
- 记录去重动作（跳过/合并/新建）

---

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
