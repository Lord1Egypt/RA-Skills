---
name: viking-memory-ultra
description: Viking Memory System Ultra - 分层记忆基座。特性：动态回流（语义晋升）、智能权重（对数增长）、可逆归档（多粒度摘要）。核心脚本：sv_write, sv_read, sv_find, sv_autoload, sv_promote, sv_weight, sv_compress。
version: 1.4.0
---

# Viking 记忆系统 - SKILL.md

> 版本：v1.4（Phase 4 复习状态追踪）
> 激活日期：2026-03-27
> 更新日期：2026-03-29
> 这是 Viking 记忆系统的核心使用规范，所有 Agent 必须遵循

---

## 🏠 系统概述

Viking 是我们的分层记忆基座，解决"记忆太多无法高效检索"的根本矛盾。

```
热记忆(hot) → 温记忆(warm) → 冷记忆(cold) → 归档(archive)
   0-7天         8-29天        30-89天       90天+
```

---

## 📁 目录结构

每个 Agent 的 Viking 记忆位于 `$SV_WORKSPACE/agent/memories/`：

```
agent/memories/
├── daily/          # 每日工作笔记（由 daily-digest skill 读取）
├── hot/            # L0: 完整记忆细节（0-7天）
├── warm/           # L1: 压缩关键要点（8-29天）
├── cold/           # L2/L3: 极简标签/索引（30-89天）
├── archive/        # L4: 长期归档（90天+，可搜索触发回忆）
├── long-term/      # 永久知识沉淀
├── meetings/       # 会议记录
└── config/         # 层级配置
```

---

## 🔧 核心命令

### 写入记忆（sv_write）

```bash
# 基本写入 → hot 层
sv_write "agent/memories/hot/2026-03-27-重要发现.md" "# 内容"

# 指定层级
sv_write "agent/memories/warm/2026-03-27-周报摘要.md" "# 内容"

# 重要记忆（标记 important=true，跳过自动压缩）
sv_write "agent/memories/hot/2026-03-27-战略决策.md" "# 内容" --importance high
```

### 读取记忆（sv_read）

```bash
sv_read "agent/memories/hot/2026-03-27-重要发现.md"
```

### 同步到共享空间（重要记忆）

```bash
# 重要记忆同步到 viking-global/shared/memory/hot/，让其他 Agent 可见
sv_write_v2 --hot "agent/memories/daily/2026-03-27.md" "# 重要内容"
```

---

## 📝 Frontmatter 规范（必须遵循）

所有写入 Viking 的记忆必须包含标准 frontmatter：

```markdown
---
id: mem_20260327_153000
title: "今日重要决策"
importance: high        # high | medium | low | important（important=永久保留）
important: false        # true = 永不压缩
tags: [决策, 战略, 猫经理]
created: 2026-03-27T15:30:00+08:00
last_access: 2026-03-27T15:30:00+08:00
access_count: 1
context_correlation: 1.0  # Phase 2: 上下文相关性系数 (0.5-1.5)
retention: 90           # 保留天数（重要/important 可设更长）
current_layer: L0       # L0 | L1 | L2 | L3 | L4
target_layer: hot       # hot | warm | cold | archive
weight: 10.0           # Phase 2 权重 = factor × decay × ln(count+1) × corr
# 复习状态追踪（Phase 4）
review_status: pending_review  # pending_review | reviewing | reviewed | mastered
last_reviewed: null
next_review: null
review_count: 0
---

# 今日重要决策

## 决策内容...
```

---

## ⚙️ 自动压缩规则

| 文件年龄 | 自动迁移 |
|---------|---------|
| 0-7天 | hot/ (L0) |
| 8-29天 | warm/ (L1) |
| 30-89天 | cold/ (L2/L3) |
| 90天+ | archive/ (L4) |

**重要标记**（`important: true` 或 `importance: important`）= 永不自动压缩

---

## 🚨 使用规范

### 必须遵循

1. **重要决策** → 写入 `agent/memories/hot/`，标记 `importance: important`，同步到共享空间
2. **每日工作** → 写入 `agent/memories/daily/YYYY-MM-DD.md`（与 daily-digest skill 对接）
3. **学到新知识** → 写入 `agent/memories/hot/learning-YYYY-MM-DD.md`
4. **会议结论** → 写入 `agent/memories/meetings/YYYY-MM-DD.md`
5. **团队协调** → 重要内容用 `sv_write_v2 --hot` 同步到 viking-global

### 禁止

1. ❌ 不要把所有东西都塞 hot/（会导致 hot 层膨胀）
2. ❌ 不要跳过 frontmatter（否则压缩脚本无法处理）
3. ❌ 不要在 hot/ 存超过7天的无关内容
4. ❌ 不要在 agent/memories/ 外的地方建立记忆体系（memory/ 是平面的，Viking 是分层的）

---

## 🔄 压缩调度

- **每周日凌晨 2:00**：`sv_compress_v2.sh --force` 自动执行
- **手动触发**：`sv_compress_v2.sh --dry-run` 预览变更

---

## 📦 Phase 4: 复习状态追踪 (v1.4)

> 解决"用户复习了哪些内容、如何判定复习状态"的跟踪问题

### 复习状态定义

| 状态 | 说明 | 触发条件 |
|------|------|---------|
| `pending_review` | 待复习 | 新建记忆的默认状态 |
| `reviewing` | 复习中 | 用户开始复习 |
| `reviewed` | 已复习 | 完成一次复习，自动计算下次复习日期 |
| `mastered` | 已掌握 | 多次复习后标记，自动移动到 archive 层 |

### 艾宾浩斯复习曲线

复习完成后自动计算下次复习日期（简化版）：

| 复习次数 | 间隔 |
|---------|------|
| 第1次 | 1天后 |
| 第2次 | 3天后 |
| 第3次 | 7天后 |
| 第4次 | 15天后 |
| 第5次+ | 30天后 |

### 复习状态管理命令

```bash
# 标记复习状态
sv_review mark <file> <status>

# 列出指定状态的记忆
sv_review list pending_review
sv_review list reviewed

# 显示统计
sv_review stats

# 显示今日需复习的记忆
sv_review due
```

### 示例

```bash
# 标记为已复习（自动更新 last_reviewed 和 next_review）
sv_review mark "agent/memories/hot/2026-03-29.md" reviewed

# 标记为已掌握（自动移动到 archive 层）
sv_review mark "agent/memories/hot/重要概念.md" mastered

# 查看统计
sv_review stats
```

### sv_list 支持复习状态过滤

```bash
# 只显示待复习的记忆
sv_list --review-status pending_review

# 只显示已复习的记忆
sv_list --review-status reviewed
```

---

## 📦 Phase 3: Archive 可逆性 (v1.3)

> 归档不再是"彻底遗忘"，而是多粒度压缩存储，支持按需解压恢复

### 核心改进

| 旧方案 | 新方案 |
|--------|--------|
| 归档 = 丢弃正文，只留标题 | 归档 = 多粒度摘要 + 完整内容存档 |
| 需要时无法找回细节 | 可随时解压完整内容 |
| 只能线性遗忘 | 支持选择性回忆 |

### 新增脚本

| 脚本 | 功能 |
|------|------|
| `sv_archive_summary.sh` | 生成多粒度摘要，保留完整内容 |
| `sv_decompress.sh` | 按需解压，恢复到目标层 |

### 使用方式

```bash
# 归档时自动生成摘要（集成到 sv_compress_v2.sh）
sv_compress_v2.sh --force

# 手动为 archive 文件生成摘要
sv_archive_summary.sh <file> --keep

# 查看摘要
sv_decompress.sh <file>

# 显示完整内容
sv_decompress.sh <file> --show

# 恢复到 hot 层
sv_decompress.sh <file> --restore
```

### frontmatter 新增字段

```markdown
summary: "一句话摘要 | 段落摘要"
full_content_file: "filename.md.archive.full"
```

---

## ⚖️ Phase 2: 权重公式优化 (v1.2)

> 改进 access_count 增长模式，引入上下文相关性系数

### 旧公式 vs 新公式

| 项目 | 旧公式 | 新公式 |
|------|--------|--------|
| 访问次数增长 | 线性 `(count+1)` | 对数 `ln(count+1)` |
| 上下文相关性 | ❌ 无 | ✅ 0.5-1.5 系数 |
| 防止记忆霸权 | ❌ 无法防止 | ✅ 旧记忆不会无限膨胀 |

### 新公式

```
W = importance_factor × (1/(days+1)^0.3) × ln(access_count+1) × context_correlation
```

### 参数说明

| 参数 | 说明 | 范围 |
|------|------|------|
| `importance_factor` | 重要性因子 | high=3.0, medium=1.5, low=0.5 |
| `time_decay` | 时间衰减 | 0-1，越老越小 |
| `ln(access_count+1)` | 对数增长 | 防止无限膨胀 |
| `context_correlation` | 上下文相关性 | 0.5-1.5（默认1.0） |

### context_correlation 设置建议

| 场景 | 系数 | 说明 |
|------|------|------|
| 高相关任务访问 | 1.3-1.5 | 当前工作直接相关 |
| 正常访问 | 1.0 | 例行加载 |
| 低相关但被召回 | 0.7-0.9 | 动态回流晋升 |

### 使用方式

```bash
# 单独计算
sv_weight.sh <file>

# 更新权重（默认 context_correlation=1.0）
sv_weight.sh <file> --update

# 指定上下文相关性
sv_weight.sh <file> --update --context-correlation 1.5

# 集成到加载流程
sv_autoload.sh --update-weight
```

---

## 🔥 动态回流机制 (v1.1 新增)

> 当检测到当前任务与 Cold/Archive 记忆语义相似时，自动晋升至 Hot 层

### 背景

传统系统的痛点：记忆只能向下迁移（hot→warm→cold→archive），永远不会回来。
这导致"三个月前做过类似项目，但系统已经忘了"的问题。

### 解决方案

动态回流机制：每次加载记忆时，自动扫描 cold/archive 层，找出语义相关的记忆并晋升。

### 核心脚本

```bash
# 独立运行
sv_promote.sh --context "当前任务描述"
sv_promote.sh --dry-run  # 预览模式
sv_promote.sh --threshold 0.7  # 调整阈值

# 集成到加载流程
sv_autoload.sh --promote
```

### 晋升流程

1. **语义相似度判断**：使用 LLM 判断当前上下文与历史记忆的相关性
2. **阈值过滤**：相似度 ≥ 0.7 才晋升（可调整）
3. **重要记忆保护**：`importance: high/important` 的记忆不受自动晋升影响
4. **原子性操作**：先写临时文件，再移动，避免数据丢失

### 技术细节

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--threshold` | 0.7 | 相似度阈值，0.0-1.0 |
| `--layer` | cold,archive | 扫描的源层级 |
| `--context` | 自动获取 | 当前任务上下文 |

### API 支持

- 优先使用 **NVIDIA Qwen**（如已配置）
- Fallback: MiniMax M2.5

### 注意事项

- ⚠️ 晋升是**单向的**（cold/archive → hot），不会降级
- ⚠️ 重要记忆（high/important）不会被自动晋升，保持原层级
- ⚠️ 每次最多处理 50 条记忆，防止 API 过载
- 💡 建议在会话开始时用 `sv_autoload.sh --promote`，而非频繁独立调用

---

## 💡 实用技巧

**如何判断写哪个层级：**
- 有细节、有过程、有价值 → hot/L0
- 只有结论、要点 → warm/L1
- 只是一个标签/关键词 → cold/L2

**团队共享记忆：**
- 猫经理的重要决策 → 同步到 `viking-global/shared/memory/hot/`
- 各 Agent 每天早上应读取共享 hot 层：`sv_read` 重要共享文件

---

## 📂 相关文件

- 脚本：`$VIKING_HOME/scripts/sv_*.sh`
- 配置：`$VIKING_HOME/config.yaml`
- 共享空间：`$VIKING_GLOBAL/shared/memory/`
