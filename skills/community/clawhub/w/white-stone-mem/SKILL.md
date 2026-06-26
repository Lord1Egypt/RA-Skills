---
name: white-stone-mem
description: Memory system with 5 categories - knowledge, projects, error log, daily review, and tasks. Load on demand to avoid memory pollution. 记忆系统 - 包含常识记忆、项目记忆、错题本、每日回顾和任务追踪。按需加载，避免记忆污染。
metadata:
  openclaw:
    emoji: 🧠
---

# White Stone Memory / 白石记忆系统

Your personal memory system with 5 categories, loaded on demand.

## Memory Categories / 记忆分类

### 1. Knowledge / 常识记忆
- **Path**: `memory/knowledge/common.md`
- **Content**: Work habits, logical thinking, product sense / 工作习惯、逻辑思维、产品意识
- **Loading**: Auto-loaded on agent startup / Agent启动时自动读取

### 2. Projects / 项目记忆
- **Path**: `memory/projects/[project_name].md`
- **Loading**: Only when user explicitly mentions a project / 用户明确提及项目时加载
- **Do NOT load**: Agents must not proactively read project memory to avoid pollution / 避免污染

### 3. Error Log / 错题本
- **Path**: `memory/errors/`
- **Content**: Past mistakes, lessons learned / 使用错误、经验总结
- **Loading**: Auto-loaded by all Agents and Sub-Agents on startup / 所有Agent启动时加载

### 4. Daily Review / 每日回顾
- **Path**: `memory/diary/[date].md`
- **Timing**: Auto-created daily / 每天自动创建
- **Content**: Work summary, insights to distill / 工作总结、待提炼内容

### 5. Tasks / 子任务追踪
- **Path**: `memory/tasks/[task_name].md`
- **Content**: Subagent task specs, config, progress / 任务规格、配置、进度
- **Loading**: On demand when managing subagents / 管理 subagent 时按需加载

## 目录结构

```
~/.openclaw/workspace/memory/
├── knowledge/          # 常识记忆 (启动加载)
│   ├── common.md
│   └── reflection-log.md
├── projects/           # 项目记忆 (按需加载)
│   └── [项目名].md
├── errors/             # 错题本 (全局加载)
│   └── [类别].md
├── diary/              # 每日回顾 (日期命名)
│   └── YYYY-MM-DD.md
└── tasks/              # 子任务追踪 (subagent 任务)
    └── [任务名].md
```

## Rules / 重要规则

1. **No proactive project reads** — Only load project memory when user explicitly asks / 不主动读取项目记忆
2. **Error log is global** — All Agents must load on startup / 错题本全局共享
3. **Knowledge loads at startup** — Auto-read on agent init / 常识记忆启动加载
4. **Daily review is scheduled** — Created daily, can be updated manually / 每日回顾定时创建
5. **Bilingual logging** — ALL memory entries must be written in bilingual format (English + Chinese). Titles use `EN / 中文`, details include both languages. This applies regardless of which language the original context was in. / 所有记忆条目必须双语记录

---

## 使用方法

### 初始化

首次使用需要创建目录结构：

```bash
mkdir -p memory/knowledge memory/projects memory/errors memory/daily
```

### 常识记忆

```bash
# 读取
cat memory/knowledge/common.md

# 编辑
vim memory/knowledge/common.md
```

### 项目记忆

```bash
# 加载项目记忆（用户明确要求时）
cat memory/projects/[项目名].md
```

### 错题本

```bash
# 读取错题本
cat memory/errors/*.md

# 添加新错误
echo "## 新错误\n- 问题：...\n- 原因：...\n- 解决方案：..." >> memory/errors/general.md
```

### 每日回顾

```bash
# 创建今日回顾
echo "# $(date +%Y-%m-%d) 回顾" > memory/daily/$(date +%Y-%m-%d).md
```

---

## 向量搜索功能 (可选，需配置)

### 概述

在现有关键词搜索基础上，增加向量语义搜索能力。

### 开启方式

在配置文件中启用：

```yaml
memory:
  vector_search:
    enabled: true
```

### 启用后的提示

⚠️ **开启向量搜索需要配置以下之一**：

| 选项 | 说明 |
|------|------|
| **A. Gemini API** | 提供 `GEMINI_API_KEY` 环境变量 |
| **B. 本地 Ollama** | 确保运行 `ollama run qwen3-embedding-0.6B` |

### 配置检查

```bash
# 检查 Ollama 是否运行
curl -s localhost:11434/api/tags
```

### 技术选型

| 组件 | 推荐 |
|------|------|
| Embedding | Gemini API 或 Ollama + qwen3-embedding-0.6B |
| 向量库 | FAISS 或 LanceDB |
| 索引 | HNSW (O(log n)) |

### 命令

```bash
/memory build-index   # 构建索引
/memory search "xxx"  # 搜索
/memory index-status  # 查看状态
```

### 注意

- 默认关闭向量搜索
- 启用后需配置 Gemini API Key 或本地 Ollama
- 新增/修改文件后需重新索引

---

## 更新日志

- 2026-02-28: 新增向量搜索功能设计
