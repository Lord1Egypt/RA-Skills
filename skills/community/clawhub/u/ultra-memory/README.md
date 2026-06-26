# ultra-memory

> **超长会话记忆系统** — 给 AI Agent 提供不遗忘、可检索、跨会话持久化的记忆能力。
> 零外部依赖，支持所有 LLM 平台：Claude Code、OpenClaw、GPT-4、Gemini、Qwen 等。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Node 18+](https://img.shields.io/badge/Node-18+-yellow.svg)](https://nodejs.org/)

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **跨会话持久化** | 每次操作自动记录，新会话启动时可恢复上次进度 |
| **5 层记忆结构** | ops 日志 → 摘要 → 语义知识库 → 实体索引 → 向量语义 |
| **关键词检索** | 支持中英文混合查询，同义词自动扩展，按相关度和时间排序 |
| **结构化实体提取** | 自动识别函数名、文件路径、依赖包、错误信息、技术决策 |
| **摘要压缩** | 每 50 条操作自动压缩，context 占用保持在可控范围 |
| **冲突检测** | 用户偏好或知识库出现矛盾时自动标记旧记录 |
| **三层记忆分级** | core / working / peripheral 自动分类，方便清理历史数据 |
| **重要性评分** | 写入时自动评分（0-1），决策/错误/里程碑排名更靠前 |
| **访问频率感知** | 被频繁检索的记忆衰减更慢，长期保留用户真正关心的内容 |
| **知识库去重** | 相似条目（相似度 >0.8）自动强化已有条目，避免重复噪音 |
| **自动捕获钩子** | Claude Code PostToolUse 钩子自动记录工具调用，无需手动触发 |
| **多用户/多 Agent 隔离** | `--scope user:alice / agent:bot1 / project:myapp`，不同 scope 完全独立存储 |
| **可选语义增强** | 安装 sentence-transformers 后支持向量检索，完全本地运行 |
| **零外部服务依赖** | 核心功能仅用 Python 标准库，无需数据库或云服务 |
| **全平台支持** | MCP Server / REST API / Claude Code / OpenClaw |
| **管理工具** | list / search / stats / export / gc 命令，日常维护用 |

---

## 平台支持范围

不同平台的功能差异较大，请在安装前确认支持范围：

| 平台 | 运行模式 | 跨会话持久化 | 跨会话恢复 | 向量检索 |
|------|---------|:-----------:|:---------:|:-------:|
| Claude Code (CLI) | 脚本模式 | ✅ | ✅ | 可选 |
| OpenClaw | 脚本模式 | ✅ | ✅ | 可选 |
| MCP Server（任意 LLM） | 脚本模式 | ✅ | ✅ | 可选 |
| REST API 客户端 | 脚本模式 | ✅ | ✅ | 可选 |
| claude.ai Web | 无脚本降级 | ❌ | ❌ | ❌ |
| 无文件系统的在线平台 | 无脚本降级 | ❌ | ❌ | ❌ |

**无脚本降级模式**：SKILL.md 附录 E 描述了此模式的行为。记忆仅在当次对话有效，关闭后丢失，但检索和压缩功能仍可用。适合轻量场景。

> **注意：** README 中"支持所有 LLM 平台"指可以在所有平台上使用 SKILL.md（含降级），而非所有平台都有完整功能。

---

## 安装

### OpenClaw（推荐）

```bash
npx clawhub@latest install ultra-memory
```

或在 OpenClaw Settings → MCP Servers 添加：

```json
{
  "mcpServers": {
    "ultra-memory": {
      "command": "node",
      "args": ["$(npm root -g)/ultra-memory/scripts/mcp-server.js"]
    }
  }
}
```

### Claude Code

将 `SKILL.md` 内容复制到项目根目录，或配置 skill 路径。

**自动捕获（推荐）**：设置环境变量后，每次工具调用自动记录：

```bash
export ULTRA_MEMORY_SESSION=sess_myproject   # 先 init.py 创建会话
```

将 `.claude/settings.json` 复制到项目根目录的 `.claude/` 目录即可启用自动钩子。

**多用户/多 Agent 隔离**：

```bash
# 用户 Alice 的独立记忆空间
python3 scripts/init.py --scope user:alice --project myapp

# 另一个 AI Agent 的独立记忆空间
python3 scripts/init.py --scope agent:codebot --project myapp

# 查看所有 scope
python3 scripts/manage.py scopes
```

不同 scope 各有独立的 `sessions/` 和 `semantic/`，互不干扰。

### 任意 LLM 平台（REST API）

```bash
# 启动 REST 服务器
py -3 platform/server.py --port 3200

# 验证
curl http://127.0.0.1:3200/health
```

加载 `platform/tools_openai.json` 工具定义，工具调用转发到 `POST http://127.0.0.1:3200/tools/{name}`。

### npm 安装

```bash
npm install -g ultra-memory
ultra-memory  # 启动 MCP Server
```

---

## 架构：5 层记忆模型

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: 向量语义层 (TF-IDF / sentence-transformers)   │
│  可选，安装后自动启用，完全本地运行                        │
├─────────────────────────────────────────────────────────┤
│  Layer 4: 结构化实体索引 (entities.jsonl)                │
│  函数 / 文件 / 依赖 / 决策 / 错误 / 类                   │
├─────────────────────────────────────────────────────────┤
│  Layer 3: 跨会话语义层 (semantic/)                       │
│  知识库 · 用户画像 · 冲突检测                             │
├─────────────────────────────────────────────────────────┤
│  Layer 2: 会话摘要层 (summary.md)                        │
│  里程碑 · 关键决策 · 进行中任务                           │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 操作日志层 (ops.jsonl)                         │
│  append-only · 时间权重 · 上下文窗口 · 分层标记           │
└─────────────────────────────────────────────────────────┘
```

---

## 工具接口

### MCP / REST API 工具

| 工具 | 功能 |
|------|------|
| `memory_init` | 初始化会话，创建三层记忆结构 |
| `memory_log` | 记录操作（自动提取实体 + tier 分级） |
| `memory_recall` | 5 层统一检索（RRF 融合 + Cross-Encoder 精排） |
| `memory_summarize` | 触发摘要压缩（含三层统计 + 元压缩） |
| `memory_restore` | 恢复上次会话上下文 |
| `memory_profile` | 读写用户画像 |
| `memory_status` | 查询会话状态与 context 压力 |
| `memory_entities` | 查询结构化实体索引 |
| `memory_extract_entities` | 全量重提取实体 |
| `memory_knowledge_add` | 追加知识库条目（含相似度去重） |
| `memory_scopes` | 列出所有隔离 scope 及会话数 |

### manage.py 管理 CLI

```bash
python3 scripts/manage.py list              # 列出所有会话
python3 scripts/manage.py search "关键词"   # 跨会话全文搜索
python3 scripts/manage.py stats             # 全局统计（tier 分布、知识库规模）
python3 scripts/manage.py export --format json --output backup.json
python3 scripts/manage.py gc --days 90      # 垃圾回收旧会话（默认 dry-run）
python3 scripts/manage.py tier              # 补写历史数据的 tier 分级
python3 scripts/manage.py scopes            # 列出所有隔离 scope
```

---

## 使用示例

### 场景 1：长编码任务不丢失上下文

```
用户: 帮我开发一个 Python 数据清洗工具

Claude: [ultra-memory] 会话已创建，开始记录每次操作...
       你之前做过 ai-data-qa 项目，我们可以复用那里的评分逻辑。
...（50条操作后）...
Claude: [自动摘要压缩] 已完成：数据加载、清洗函数、单元测试。
        当前进行中：导出模块。context 已优化，继续...
```

### 场景 2：跨天继续任务

```
用户（第二天）: 继续昨天的工作

Claude: [记忆恢复] 你昨天在开发数据清洗工具：
        ✅ 已完成：加载模块、clean_df()、基础测试
        🔄 进行中：导出模块，写到一半
        💡 下一步：继续 export.py 的 to_csv() 方法
```

### 场景 3：精确回忆操作细节

```
用户: 之前那个处理空值的逻辑是怎么写的？

Claude: [检索 ops #23] 在 src/cleaner.py 的 clean_df() 中：
        空值处理：字符串列填充 ""，数值列填充 0。
        代码在第 45-52 行。要展示吗？
```

---

## 存储结构

```
~/.ultra-memory/                   # 默认存储目录（可配置）
├── sessions/
│   └── <session_id>/
│       ├── ops.jsonl              # Layer 1: 操作日志（append-only）
│       ├── summary.md             # Layer 2: 会话摘要
│       ├── meta.json              # 元数据（含 scope / importance / access_count）
│       ├── tfidf_cache.json       # Layer 5: TF-IDF 索引缓存
│       └── embed_cache.json       # Layer 5: sentence-transformers 缓存
├── semantic/
│   ├── entities.jsonl             # Layer 4: 结构化实体
│   ├── knowledge_base.jsonl       # Layer 3: 知识库（含 reinforced_count）
│   ├── user_profile.json          # 用户画像
│   └── session_index.json         # 会话索引
├── scopes/                        # 多用户/多 Agent 隔离空间
│   ├── user__alice/               # --scope user:alice 的独立空间
│   │   ├── sessions/
│   │   └── semantic/
│   └── agent__bot1/               # --scope agent:bot1 的独立空间
└── archive/                       # 归档会话（可配置）
```

---

## 与主流方案对比

| 能力 | Claude 原生 | mem0 | MemGPT | ultra-memory |
|------|:-----------:|:----:|:------:|:------------:|
| 零外部服务依赖 | ✅ | ❌ | ❌ | ✅ |
| 数据完全本地 | ❌ | ⚠️ | ✅ | ✅ |
| 结构化实体提取 | ❌ | 部分 | ❌ | ✅ |
| 冲突检测 | ❌ | ❌ | ❌ | ✅ |
| 摘要压缩（不爆 context） | 实验性 | ❌ | 固定层 | ✅ |
| 向量检索 | ❌ | ✅ | ❌ | ✅（可选） |
| 跨语言检索 | ❌ | ⚠️ | ❌ | ✅ |
| 多用户/多 Agent 隔离 | ❌ | ✅ | ⚠️ | ✅ |
| 全平台支持 | 仅 Claude | ⚠️ | ⚠️ | ✅ |

---

## 开发者

**NanJingYa** — https://github.com/nanjingya

GitHub: https://github.com/nanjingya/ultra-memory

Issues: https://github.com/nanjingya/ultra-memory/issues

---

## 许可

MIT License
