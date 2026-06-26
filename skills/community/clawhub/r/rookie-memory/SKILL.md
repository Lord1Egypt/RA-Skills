---
name: rookie-Memory
description: Rookie-Memory 三级记忆管理系统 v2.0。专为 AI 代理设计的进化版记忆系统，包含 L0 永久记忆、L1 短期记忆、L2 中期记忆，支持 bootstrap 启动加载、autosave 自动保存、混合检索、自动清理等高级功能。
---

# Rookie Memory Skill

管理 AI 代理的三级记忆系统：短期（滑动窗口）、中期（自动摘要）、长期（向量检索）。

## 快速开始

```bash
# 初始化记忆系统
python3 scripts/memory_manager.py init

# 启动时加载记忆（推荐在会话开始时执行）
python3 scripts/memory_manager.py bootstrap

# 添加短期记忆
python3 scripts/memory_manager.py add --type short --content "用户喜欢黑色"

# 会话结束时自动保存记忆（推荐使用虚拟环境中的 python）
/root/.openclaw/venv-chromadb/bin/python scripts/memory_manager.py autosave

# 查询记忆
python3 scripts/memory_manager.py search "用户的偏好"
```

## 存储隔离规则

| 层级 | 存储位置 | 触发条件 | 用途 |
|------|----------|----------|------|
| **L0 永久** | `memory/l1/` (文件系统) | 启动时加载 | 身份、技术栈、关键决策等稳定事实 |
| **L1 短期** | `memory/sliding-window.json` (文件) | 实时 | 保持当前对话连贯 |
| **L2 中期** | `memory/summaries/` (JSON 文件) | Token 阈值 | 压缩历史，保留大意 |
| **L3 长期** | `memory/vector-store/` (ChromaDB) | 语义检索 | 永久记忆，RAG，动态对话 |

**存储隔离原则：**
- **L0/L1/L2** (文件系统)：存储稳定事实、结构化数据、关键决策
- **L3** (ChromaDB)：存储动态对话、临时上下文、语义检索内容
- 避免频繁更新 L0/L1 文件，L3 用于高频写入

## 核心功能

### 1. 短期记忆：滑动窗口

- 配置：`config/window_size`（默认 10 条）
- 逻辑：FIFO 队列，超出则丢弃最旧消息
- 文件：`memory/sliding-window.json`

### 2. 中期记忆：自动摘要

- 触发：当前 token > `config/summary_threshold`（默认 4000）
- 模型：使用廉价模型（如 GPT-3.5-Haiku）
- 输出：`memory/summaries/YYYY-MM-DD.json`

### 3. 长期记忆：向量检索

- 后端：ChromaDB（本地向量库）
- 存：对话结束/摘要生成后自动向量化存储
- 取：每次查询前先检索相关记忆

## 配置文件

创建 `memory/config.yaml`：

```yaml
memory:
  short_term:
    enabled: true
    window_size: 10
    max_tokens: 2000

  medium_term:
    enabled: true
    summary_threshold: 4000
    summary_model: "glm-4-flash"  # 或 gpt-3.5-turbo

  long_term:
    enabled: true
    backend: "chromadb"
    top_k: 3
    min_relevance: 0.7
```

## 使用场景

- **新对话开始**：执行 `bootstrap` 加载 L0 永久记忆 + L1/L2 记忆，注入相关上下文
- **对话中**：自动管理短期/中期记忆，超阈值自动摘要
- **对话结束**：将重要信息存入长期记忆

## 详细用法

### 会话结束：自动保存

```bash
/root/.openclaw/venv-chromadb/bin/python scripts/memory_manager.py autosave
```

**功能：**

1. **分析短期记忆**：读取滑动窗口中的对话内容
2. **智能摘要**：当 token 数超过配置阈值（默认 4000）时自动生成摘要
3. **长期记忆**：将重要内容向量化存入 ChromaDB
4. **关键决策**：自动检测包含"决定"、"决策"等关键词的消息，更新 `key-decisions.md`
5. **当日日志**：生成 `memory/YYYY-MM-DD.log` 记录保存摘要

**输出示例：**

```
=== 💾 自动保存记忆 ===

📝 短期记忆: 10 条
   Token 估算: 361 (阈值: 4000)
   → Token 未超过阈值，跳过摘要

🧠 存入长期记忆...
   ✓ 已存入 10 条长期记忆

📋 更新关键决策...
   ✓ 已更新 key-decisions.md (新增 4 条)

📄 生成当日日志...
   ✓ 已生成日志: /root/.openclaw/workspace/memory/2026-03-12.log

============================================================
✓ 自动保存完成
  短期记忆: 10 条
  摘要生成: 否
  长期记忆: 10 条
  关键决策: 4 条
  日志文件: /root/.openclaw/workspace/memory/2026-03-12.log
============================================================
```

**注意：** 需要使用虚拟环境中的 Python（包含 chromadb 依赖）。

## 高级功能

### 冲突解决机制

ChromaDB 记录自动包含来源标记和时间戳，支持冲突检测：

- **source 标记**：自动记录来源（`chat`/`summary`/`manual`/`autosave`）
- **时间戳**：每条记忆记录精确时间
- **冲突检测**：检索时自动标记相似内容的冲突项

### 混合检索策略

支持三种检索模式和三层记忆检索：

```bash
# 混合检索（关键词 + 语义，默认）
python3 scripts/memory_manager.py search "用户偏好"

# 纯关键词检索
python3 scripts/memory_manager.py search "用户偏好" --mode keyword

# 纯语义检索
python3 scripts/memory_manager.py search "用户偏好" --mode semantic

# 检索 L1 短期记忆
python3 scripts/memory_manager.py search "最近对话" --tier short

# 检索 L2 中期记忆
python3 scripts/memory_manager.py search "昨天讨论" --tier medium

# 检索 L3 长期记忆（默认）
python3 scripts/memory_manager.py search "身份信息" --tier long --top-k 5
```

**检索模式说明：**

- **hybrid**（混合）：先关键词匹配获取候选集，再在候选集上做语义检索，最后合并排序
- **keyword**（关键词）：纯关键词匹配，快速但不够智能
- **semantic**（语义）：纯语义检索，智能但计算成本高

**混合检索流程：**

1. 关键词匹配：在所有记忆中搜索包含关键词的内容，获取候选集（默认 top_k × 3）
2. 语义检索：在候选集上执行向量相似度计算
3. 合并排序：综合关键词得分（权重 0.4）和语义得分（权重 0.6），按综合得分排序返回

**配置文件：**

```yaml
memory:
  long_term:
    search_mode: "hybrid"  # 默认检索模式
```

### 关键决策专项记录

自动检测包含"决定"、"决策"、"选择"等关键词的消息，更新 `memory/l1/key-decisions.md`。

```bash
# 手动提取关键决策（可选）
python3 scripts/memory_manager.py extract-decisions
```

### 压缩前提醒机制

当短期记忆接近 token 阈值时发出提醒：

```bash
# 检查是否接近压缩阈值
python3 scripts/memory_manager.py check-warning
```

配置文件支持：
- `warning_threshold`: 提醒阈值（默认 3000）
- `summary_threshold`: 摘要阈值（默认 4000）

### 每日工作日志

自动生成每日工作日志 `memory/YYYY-MM-DD.log`，记录：
- 短期记忆数量
- Token 使用情况
- 摘要生成记录
- 长期记忆存储数量
- 关键决策提取数量

```bash
# 查看当日日志
python3 scripts/memory_manager.py daily-log
```

### 记忆库健康分析

分析长期记忆库的健康状态，检查：
- 记忆总数和分布（按来源）
- 过时记忆（超过配置天数未检索）
- 低相关性记忆
- 重复记忆（相似度超过阈值）

```bash
# 分析记忆库健康状态
python3 scripts/memory_manager.py analyze-health
```

**输出示例：**

```
=== 🏥 记忆库健康分析 ===

📊 记忆总数: 156

📂 按来源分布:
  • autosave: 89 条
  • manual: 34 条
  • chat: 23 条
  • summary: 10 条

📅 过时记忆 (超过 90 天): 23 条
  最新 3 条:
    • [2025-11-15 10:30:00] 用户在讨论项目A的技术栈...
    • [2025-10-22 14:20:00] 会议记录：讨论了产品路线图...
    • [2025-09-08 09:15:00] 记录了第一次使用系统...

⚠️  低相关性记忆检查:
  随机采样 10 条记忆进行相关性检查...

🔄 重复记忆检查 (相似度 >= 0.95):
  共比较 5000 对，发现 3 对重复
  前 5 对:
    • mem_20251101_120000_0001 ↔ mem_20251102_150000_0002 (相似度: 0.972)
    • mem_20251025_080000_0003 ↔ mem_20251026_120000_0004 (相似度: 0.961)
    ...

========================================
🏥 健康评分: 78.5/100
🟡 健康评级: 良好
========================================
```

### 记忆库清理

清理过时和重复的记忆，保持记忆库的高效性。

```bash
# 预览模式（不实际删除）
python3 scripts/memory_manager.py cleanup --dry-run

# 执行清理
python3 scripts/memory_manager.py cleanup
```

**清理规则：**

- **过时记忆**：超过 `max_age_days` 天未检索的记忆（默认 90 天）
- **重复记忆**：相似度 >= `duplicate_threshold` 的记忆，保留较新的（默认 0.95）

**输出示例：**

```
=== 🧹 记忆库清理 ===

📊 当前记忆总数: 156

📅 检查过时记忆 (超过 90 天)...
  发现 23 条过时记忆

🔄 检查重复记忆 (相似度 >= 0.95)...
  发现 3 条重复记忆

========================================
📋 清理摘要:
  过时记忆: 23 条
  重复记忆: 3 条
  总计删除: 26 条
  剩余记忆: 130 条
========================================

🗑️  正在删除 26 条记忆...
✓ 删除完成
```

**配置文件：**

```yaml
memory:
  cleanup:
    enabled: true
    max_age_days: 90              # 超过N天未检索的记忆
    min_relevance: 0.6             # 相关性阈值
    duplicate_threshold: 0.95      # 相似度阈值（超过则视为重复）
```

See [REFERENCES.md](references/references.md) for complete command reference.
