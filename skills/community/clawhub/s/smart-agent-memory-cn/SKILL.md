---
name: smart-agent-memory
version: 2.0.0
description: "跨平台 Agent 长期记忆系统。分层上下文供给 + 温度模型 + Skill经验记忆 + 结构化存储 + 自动归档。三层存储：Markdown（人可读，QMD 可搜索）+ JSON（结构化）+ SQLite/FTS5（高性能全文搜索）。纯 Node.js 原生模块，零外部依赖。"
keywords: [memory, agent, openclaw, longterm, gc, archive, skill-extraction, temperature-model, layered-context, skill-experience]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["node"]
    trust: high
    permissions:
      - read: ~/.openclaw/workspace/memory
      - write: ~/.openclaw/workspace/memory
---

# Smart Agent Memory 🧠 v2.0

**跨平台 Agent 长期记忆系统** — 分层上下文供给 + Skill经验记忆 + 温度模型 + 自动归档。

## ⚡ 核心原则：分层加载，按需供给

> **绝对不要全量加载记忆！** 先读索引，再按需钻取。这是省 token 的关键。

### 记忆使用流程（每次需要记忆时）

```
1. index    → 读取精简索引（总览，<500 tokens）
2. 判断     → 根据当前任务决定需要哪部分记忆
3. context  → 按 tag/skill/时间 加载具体上下文
4. 行动     → 基于加载的上下文执行任务
```

### Skill 经验记忆流程（工具调用后）

```
工具调用成功/踩坑 → remember "经验总结" --skill <skill-name>
下次调用该工具前 → skill-mem <skill-name> 加载经验
```

## CLI Reference

```bash
CLI=~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js

# ★ 分层上下文（核心，优先使用）
node $CLI index                              # 精简记忆索引（先读这个！）
node $CLI context --tag <tag>                # 按标签加载上下文
node $CLI context --skill <skill-name>       # 按 Skill 加载经验+相关事实
node $CLI context --days 7                   # 最近 N 天的记忆
node $CLI context --entity-type person       # 按实体类型加载

# ★ Skill 经验记忆
node $CLI remember "该API时间参数必须用ISO格式" --skill api-tool
node $CLI skill-mem <skill-name>             # 读取某 Skill 的经验
node $CLI skill-list                         # 列出所有有经验记忆的 Skill

# 基础记忆操作
node $CLI remember <content> [--tags t1,t2] [--skill name] [--source conversation]
node $CLI recall <query> [--limit 10]
node $CLI forget <id>
node $CLI facts [--tags t1] [--limit 50]

# 教训与实体
node $CLI learn --action "..." --context "..." --outcome positive --insight "..."
node $CLI lessons [--context topic]
node $CLI entity "Alex" person --attr role=CTO
node $CLI entities [--type person]

# ★ 会话生命周期（模拟 mem9 自动钩子）
node $CLI session-start                      # 对话开场：加载记忆概览+最近上下文（一个命令搞定）
node $CLI session-end "本次讨论了XX，决定了YY"  # 对话结束：存会话摘要

# 维护
node $CLI gc [--days 30]                     # 归档冷数据
node $CLI reflect                            # 夜间反思
node $CLI stats                              # 记忆健康
node $CLI search <query>                     # 全文搜索 .md（优先qmd，兜底内置）
# qmd 是可选的高级搜索（BM25+向量），不可用时自动降级到纯JS搜索

node $CLI temperature                        # 温度报告
node $CLI extract <lesson-id> --skill-name x # 提炼 Skill
```

## Agent 行为规范

### 🔄 记忆召回（已自动）

**所有 agent 通过 `memory_search`（OpenClaw 内置 mandatory recall）自动搜索 `memory/*.md`。**
双层存储确保每次写入都同步生成 Markdown，所以 `memory_search` / qmd 天然能搜到所有结构化数据。
无需额外操作，无需 workspace 配置，跨 agent 通用。

需要深入某方向时，用 CLI 钻取：
```bash
node $CLI context --tag <tag>       # 按标签
node $CLI context --skill <name>    # 按 Skill 经验
node $CLI context --days 7          # 按时间
```

### 📝 记忆写入（有内容就写）

```bash
node $CLI remember "关键信息" --tags tag1,tag2    # 事实
node $CLI learn --action "..." --context "..." --outcome positive --insight "..."  # 教训
node $CLI session-end "本次讨论了XX，决定了YY"    # 会话摘要
```
> ⚠️ **不要攒到最后！** 有内容就写，中途断了也不丢。
> 每晚 cron 兜底检查，确保不遗漏。

### ✅ MUST DO
- **每次需要历史信息时**：先 `index`，看概览，再决定加载哪部分
- **工具调用踩坑后**：`remember "经验" --skill <name>` 沉淀经验
- **调用不熟悉的工具前**：`skill-mem <name>` 检查有没有历史经验
- **记录新信息时**：打好 tags，方便后续按需检索
- **搜索记忆时**：`search` 命令优先走 qmd（语义搜索），qmd 不可用时自动降级为内置 TF 搜索

### ❌ NEVER DO
- 不要一次性 `facts --limit 999` 全量加载
- 不要在每轮对话都加载全部记忆
- 不要忽略 `index` 直接 `recall`（除非你确切知道要搜什么）
- 不要把记忆操作全堆到对话结束时

## Storage Layout

```
~/.openclaw/workspace/memory/
├── YYYY-MM-DD.md           ← 每日日志
├── skills/                 ← ★ Skill 经验记忆（新增）
│   ├── api-tool.md
│   └── deploy.md
├── lessons/                ← 教训 Markdown
├── decisions/              ← 决策 Markdown
├── people/                 ← 人物档案
├── reflections/            ← 反思记录
├── .data/                  ← JSON 结构化数据
├── .archive/               ← 归档冷数据
└── .index.json             ← 温度索引 + 统计
```

## Recommended Cron Jobs

安装后建议通过 OpenClaw cron 工具添加以下定时任务：

### 每晚反思（推荐）

```json
{
  "name": "memory-reflect",
  "schedule": { "kind": "cron", "expr": "45 23 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "运行记忆反思：node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js reflect，然后总结今天的记忆变化。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

### 每周日 GC 归档（推荐）

```json
{
  "name": "memory-gc",
  "schedule": { "kind": "cron", "expr": "0 2 * * 0", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "运行记忆GC：node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js gc --days 30，报告归档了多少条记忆。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

### 每日会话摘要检查（可选，弥补遗忘）

```json
{
  "name": "memory-session-check",
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "检查今天的记忆情况：运行 node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js stats，如果今天有对话但 facts 没增长，回顾今天的对话并用 session-end 补存摘要。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

> Agent 可用 `cron` 工具的 `add` action 直接添加以上任务，JSON 作为 `job` 参数传入。

---

## 中文优化 (memory-cn 集成)

本技能已集成 `memory-cn` 的核心功能，专门优化中文记忆的搜索和管理。

### FTS5 中文分词问题

SQLite FTS5 的 `unicode61` 分词器会把连续的中文字符当作一个 token，导致搜索命中率下降。

**解决方案：** 在中文关键词之间添加空格，强制正确分词。

### 中文优化命令

```bash
# 诊断记忆系统（检测 FTS5 中文分词问题）
node $CLI diagnose

# 批量优化 tags（自动在中文字符之间添加空格）
node $CLI optimize-tags

# 压缩大日志文件（默认 5KB）
node $CLI compress [--max-kb 5]

# 生成优化的搜索配置（用于 gateway config.patch）
node $CLI optimize-search

# 生成优化的 memoryFlush prompt（用于 gateway config.patch）
node $CLI optimize-flush
```

### 关键技术参数

针对 0.6B 等小模型的优化参数：

- **vectorWeight 0.75**：向量搜索主导（FTS5 中文不可靠）
- **minScore 0.15**：小模型分数普遍偏低
- **chunking 250 tokens**：更小的 chunk 帮助弱模型匹配
