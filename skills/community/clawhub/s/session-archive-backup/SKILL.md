---
name: session-archive-backup
description: |
  OpenClaw 会话重置-存档-备份完整工作流管理。自动化处理 Token 超限、闲置超时、手动重置时的四层数据存档体系，支持 GitHub/OneDrive 双备份。

  TRIGGERS:
  - 用户说"设置存档工作流"、"配置自动备份"
  - 需要建立会话生命周期管理机制
  - 想要自动化重置-存档-备份流程
---

# Session Archive & Backup System

完整的 OpenClaw 会话生命周期管理工作流，实现从原始对话到云端备份的四层数据体系。

## CRITICAL: 3-Phase Setup Workflow

**NEVER 直接修改配置。ALWAYS 完成 Phase 1（需求确认）和 Phase 2（环境检查），
并 WAIT for user confirmation 后再执行 Phase 3（配置实施）。**

---

## Phase 1: 需求确认（ALWAYS ASK FIRST）

询问用户：

**"你希望配置哪种类型的存档备份方案？"**

| 场景类型 | 描述 | 适用情况 |
|----------|------|----------|
| **S1 - 全新设置** | 从零搭建完整工作流 | 刚安装 OpenClaw，无现有配置 |
| **S2 - 已有配置** | 已有部分组件，需要整合 | 有零散脚本，需要体系化 |
| **S3 - 迁移升级** | 从其他方案迁移 | 使用其他备份方案，想切换到本工作流 |

询问用户：

**"你的备份目标是什么？"**

| 备份目标 | 说明 |
|----------|------|
| **GitHub** | 备份到 GitHub 仓库（需要配置 token） |
| **OneDrive** | 备份到本地 OneDrive 目录 |
| **双备份** | 同时备份到 GitHub + OneDrive（推荐） |

---

## Phase 2: 环境检查（ASK AFTER PHASE 1）

诊断问题，确定配置路径：

1. **"当前 workspace 是否有 memory/ 目录？"**
   - YES → 检查现有结构
   - NO → 需要创建完整目录结构

2. **"是否有现有的 HEARTBEAT.md？"**
   - YES → 需要合并或备份现有配置
   - NO → 创建新的 HEARTBEAT.md

3. **"是否有 GitHub 备份仓库？"**
   - YES → 配置 remote URL
   - NO → 提供创建仓库指引

4. **"OneDrive 路径是否可用？"**
   - YES → 确认路径 `C:\Users\[username]\OneDrive\`
   - NO → 跳过 OneDrive 备份

确认以上信息后，向用户展示 **配置计划摘要**，等待确认。

**DO NOT PROCEED TO PHASE 3 UNTIL CONFIRMED.**

---

## Phase 3: 配置实施

用户确认后，执行以下步骤：

### Step 1: 创建目录结构

```
workspace/
├── memory/
│   ├── session-backups/      # 结构化存档（AI摘要）
│   ├── raw-history/          # 原始对话（JSONL）
│   ├── subagents/            # 子Agent输出
│   ├── index.json            # 快速索引
│   ├── reset-log.md          # 重置日志
│   └── backup-status.json    # 备份状态
├── scripts/
│   ├── generate-ai-summary.ps1   # AI摘要生成
│   └── backup.ps1                # 备份脚本
├── config/                   # 需备份的配置文件
│   └── (SOUL.md, USER.md, etc.)
└── HEARTBEAT.md              # 核心工作流定义
```

### Step 2: 配置 HEARTBEAT.md

创建/更新 `HEARTBEAT.md`，包含：

- **Token 超限检测**（默认阈值：70k/100k）
- **闲置超时检测**（默认：120 分钟）
- **AI 摘要生成**调用
- **四层数据存档**流程
- **备份触发**逻辑

### Step 3: 创建核心脚本

**scripts/generate-ai-summary.ps1**
- 读取会话历史
- 生成结构化摘要
- 标记差异 [NEW]/[UPD]/[KEEP]

**scripts/backup.ps1**
- 备份到 GitHub
- 备份到 OneDrive
- 更新 backup-status.json

### Step 4: 初始化索引文件

**memory/index.json**
- 配置项快速查询
- 标签索引
- 变更历史追踪

---

## 工作流详解

### 触发条件

| 触发场景 | 条件 | 执行动作 |
|----------|------|----------|
| **Token 超限** | > 70k/100k | 存档 → 同步 MEMORY.md → **自动重置** |
| **闲置超时** | 120 分钟无活动 | 预存档 → 同步 MEMORY.md → 重置 |
| **手动重置** | 用户发送"重置" | 存档 → 同步 MEMORY.md → 重置 |

### 四层数据流转

```
Layer 1: 原始对话 (Raw)
└── memory/raw-history/*.jsonl
    └── 完整消息记录（每次重置前自动保存）

Layer 2: 结构化存档 (Structured)
└── memory/session-backups/*.md
    └── AI 生成摘要 + 差异标记 [NEW]/[UPD]/[KEEP]

Layer 3: 长期记忆 (Memory)
└── MEMORY.md
    └── 跨会话保持的关键决策、待办、配置

Layer 4: 云端备份 (Cloud)
├── GitHub: [username]/openclaw-backup
└── OneDrive: C:\Users\[username]\OneDrive\openclaw-backup
```

### 执行流程

```
触发条件满足
      ↓
┌─────────────────┐
│ 1. 生成 AI 摘要  │ ← 提取关键决策、待办、主题
│ 2. 对比上次存档  │ ← 标记 [NEW]/[UPD]/[KEEP]
│ 3. 保存结构化存档 │ → memory/session-backups/*.md
└─────────────────┘
      ↓
┌─────────────────┐
│ 4. 保存原始对话  │ → memory/raw-history/*.jsonl
└─────────────────┘
      ↓
┌─────────────────┐
│ 5. 同步长期记忆  │ ← 更新 MEMORY.md
└─────────────────┘
      ↓
┌─────────────────┐
│ 6. 更新索引     │ ← 更新 memory/index.json
└─────────────────┘
      ↓
┌─────────────────┐
│ 7. 记录重置日志  │ ← 更新 memory/reset-log.md
└─────────────────┘
      ↓
┌─────────────────┐
│ 8. 标记待备份   │ ← pendingChanges = true
└─────────────────┘
      ↓
┌─────────────────┐
│ 9. 执行重置     │ ← 会话清零，重新开始
└─────────────────┘
      ↓
新会话开始 → 读取 MEMORY.md → 汇报上次状态
```

---

## 关键配置参数

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `token_threshold` | 70k/100k | Token 超限触发存档重置 |
| `idle_timeout` | 120 分钟 | 闲置超时触发存档重置 |
| `backup_interval` | 12 小时 | 定期备份间隔 |
| `pending_changes` | true/false | 重要变更立即备份标记 |

---

## 存档格式模板

```markdown
# 会话备份 - YYYY-MM-DD HH:MM

## 统计信息
- Token 使用量: XXk/100k
- 触发原因: [token/idle/manual]
- 主要话题: [摘要]

## 关键决策（差异标记）
- [NEW] **新增决策**: 描述
- [UPD] **更新决策**: 描述（原：xxx）
- [KEEP] **保持决策**: 无变化

## 待办事项（当前状态）
- [ ] 进行中
- [x] 已完成

## 与上次存档的差异摘要
- 新增决策: X 个
- 更新决策: X 个
- 新增待办: X 个
- 完成待办: X 个

## 完整上下文引用
- 上次存档: [文件名]
- 长期记忆: MEMORY.md
- 快速索引: index.json

## 已安装/配置的技能
- [skill-name] v1.0.0

## 下次继续
[需要跟进的事项]
```

---

## 使用示例

### 手动触发存档
```
用户：存档当前会话
→ 执行完整存档流程
→ 保存到 memory/session-backups/manual-YYYY-MM-DD-HHMM.md
```

### 查看存档历史
```
用户：查看存档记录
→ 读取 memory/reset-log.md
→ 展示最近的重置和存档记录
```

### 查询配置
```
用户：Token 超限阈值是多少？
→ 查询 memory/index.json
→ 返回：70k/100k
```

---

## 故障排查

### 问题：存档未触发
**检查**：
1. HEARTBEAT.md 是否正确配置
2. token 阈值设置是否正确
3. 检查 memory/reset-log.md 是否有记录

### 问题：备份失败
**检查**：
1. GitHub token 是否有效
2. OneDrive 路径是否存在
3. 查看 backup-status.json 中的失败记录

### 问题：AI 摘要生成失败
**检查**：
1. scripts/generate-ai-summary.ps1 是否存在
2. 是否有足够的会话历史
3. PowerShell 执行权限

---

## Reference Files

- `references/workflow-diagram.md` — 完整工作流程图
- `references/config-templates.md` — 配置文件模板
- `references/troubleshooting.md` — 详细故障排查指南
