# 🧠 Smart Agent Memory — 跨平台 Agent 长期记忆系统

> 融合两大开源记忆方案的精华，打造**温度模型 + 结构化存储 + 自动归档 + 知识提炼**的一站式 Agent 记忆引擎。

**纯 Node.js 原生模块，零外部依赖。Windows / macOS / Linux 通用。Node.js >= 22.5 自动启用 SQLite + FTS5。**

---

## 📖 目录

- [项目背景：为什么要做这个？](#-项目背景为什么要做这个)
- [核心优势](#-核心优势)
- [快速开始](#-快速开始)
- [完整命令手册](#-完整命令手册)
- [双层存储架构](#-双层存储架构)
- [温度模型](#-温度模型)
- [智能后端：JSON 与 SQLite](#-智能后端json-与-sqlite)
- [与 OpenClaw 深度集成](#-与-openclaw-深度集成)
- [Agent 每日工作流](#-agent-每日工作流)
- [系统要求](#-系统要求)
- [文件结构](#-文件结构)
- [常见问题](#-常见问题)
- [致谢与来源](#-致谢与来源)

---

## 💡 项目背景：为什么要做这个？

社区里已有两个 Agent 记忆方案，各有优缺点：

### agent-memory-system（by 阿福）

**理念：文件即记忆，日记本方式。**

| 优点 ✅ | 缺点 ❌ |
|---------|---------|
| 温度模型（热/温/冷三级分类） | 只支持 Linux/Mac（bash 脚本） |
| 自动归档 GC（冷数据按月归档） | 依赖 rsync、crontab |
| 夜间反思（每日健康报告） | 无结构化查询能力 |
| 技能提炼（教训 → SKILL.md） | 无实体追踪 |
| Markdown 人可读，QMD 直接搜索 | 搜索只能靠外部工具 |
| 与 OpenClaw workspace 深度融合 | — |

### agent-memory（by ClawHub 社区）

**理念：数据库驱动，程序化 API。**

| 优点 ✅ | 缺点 ❌ |
|---------|---------|
| Fact / Lesson / Entity 三层模型 | 需要 Python 运行环境 |
| SQLite + FTS5 精准全文搜索 | 数据在数据库里，人不可读 |
| 置信度（confidence）模型 | 与 OpenClaw 原生工作流割裂 |
| 访问计数 + 最后访问时间追踪 | 无温度模型，无自动归档 |
| 置换链（supersede）保留历史 | 无夜间反思，无技能提炼 |
| 实体属性自动合并 | — |
| 数据导出（JSON export） | — |

### Smart Agent Memory 的答案：全都要

**把两者的优点合并，缺点全部干掉：**

- ✅ 从 agent-memory-system 继承：温度模型、自动归档、夜间反思、技能提炼、Markdown 文件驱动
- ✅ 从 agent-memory 继承：Fact/Lesson/Entity 结构化存储、全文搜索、置信度、访问追踪、置换链、实体追踪
- 🆕 **新增双层写入**：一次操作同时写 Markdown + JSON/SQLite
- 🆕 **新增跨平台**：纯 Node.js，不依赖 bash/python/rsync
- 🆕 **新增智能后端**：Node.js >= 22.5 自动启用原生 SQLite + FTS5，否则降级 JSON
- 🆕 **新增自动迁移**：从 JSON 升级到 SQLite 时零手动操作
- 🆕 **新增 OpenClaw Cron 集成**：不碰系统 crontab

---

## 🏆 核心优势

| 特性 | 说明 |
|------|------|
| **双层存储** | Markdown（人可读，QMD 可搜索）+ JSON/SQLite（结构化，快速查询），写入时双写 |
| **智能后端** | Node.js >= 22.5 → 原生 SQLite + FTS5；低版本 → JSON 降级（零依赖也能用） |
| **温度模型** | 🔥 热（<7天）→ 🟡 温（7-30天）→ ❄️ 冷（>30天）→ 📦 归档 |
| **三层记忆** | **Fact**（事实）+ **Lesson**（教训）+ **Entity**（实体），各有专用 CRUD |
| **自动归档** | 冷数据自动移到 `.archive/YYYY-MM/`，配合 GC 清理低频 facts |
| **全文搜索** | SQLite FTS5 精准搜索 / JSON 模式关键词匹配 / Markdown 文件全文扫描 |
| **知识提炼** | 从教训一键提取 SKILL.md 模板，变成可复用的 Agent 技能 |
| **夜间反思** | 自动生成记忆健康报告（facts/lessons/entities 统计 + 温度分布） |
| **置信度** | 每个 fact 可设置 0-1 置信度，搜索时可按置信度过滤 |
| **访问追踪** | 自动记录每个 fact 的访问次数和最后访问时间，GC 时保护高频数据 |
| **置换链** | `supersede` 一个旧 fact，新旧关联保留历史轨迹 |
| **自动迁移** | 首次检测到 SQLite 可用时，自动把 JSON 数据导入 SQLite |
| **跨平台** | Windows / macOS / Linux 通用，纯 Node.js |
| **14 个命令** | 覆盖记忆全生命周期：记住、回忆、遗忘、学习、追踪、归档、反思、提炼 |

---

## 🚀 快速开始

### 安装

```bash
# 从 ClawHub 安装
clawhub install smart-agent-memory

# 或手动复制到技能目录
cp -r smart-agent-memory ~/.openclaw/skills/
```

### 基本操作

```bash
# 记住一个事实
node scripts/memory-cli.js remember "项目用 React 18 + TypeScript" --tags tech,frontend

# 搜索记忆
node scripts/memory-cli.js recall "React"

# 记录教训
node scripts/memory-cli.js learn \
  --action "线上直接改数据库" \
  --context "数据修复" \
  --outcome negative \
  --insight "永远先备份，在测试环境验证SQL后再操作生产"

# 追踪一个人
node scripts/memory-cli.js entity "张三" person --attr role=后端开发 --attr team=Core

# 查看记忆健康
node scripts/memory-cli.js stats
```

**示例输出：**
```
🧠 Smart Agent Memory — Stats [sqlite]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Facts:
  Total:      42
  Active:     38
  🔥 Hot:     12 (< 7 days)
  🟡 Warm:    18 (7-30 days)
  ❄️ Cold:    8 (> 30 days)

Lessons:      7
Entities:     5
Archived:     23 files

Last GC:         2026-03-05 00:00
Last Reflection: 2026-03-06 23:45
```

---

## 📖 完整命令手册

### remember — 记住事实

```bash
node scripts/memory-cli.js remember <内容> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--tags t1,t2` | 标签（逗号分隔） | 无 |
| `--source` | 来源（conversation / observation / inference） | conversation |
| `--confidence` | 置信度（0-1） | 1.0 |

**示例：**
```bash
# 基础
node scripts/memory-cli.js remember "老板偏好简短日报"

# 带标签
node scripts/memory-cli.js remember "API限流100req/min" --tags api,限制

# 低置信度（不太确定的信息）
node scripts/memory-cli.js remember "可能要迁移到AWS" --confidence 0.6 --source inference
```

**背后发生了什么：**
1. 写入 `.data/facts.json`（或 SQLite facts 表）
2. 追加到当天的 `memory/2026-03-07.md` 日志
3. 如果是 SQLite 模式，同时写入 FTS5 索引

### recall — 搜索/回忆事实

```bash
node scripts/memory-cli.js recall <关键词> [--limit 10] [--tags t1]
```

搜索 JSON/SQLite 中的结构化 facts。SQLite 模式下使用 FTS5 精准搜索，JSON 模式下使用关键词匹配 + 评分排序。

**评分逻辑：** 关键词匹配度 + 数据新鲜度（近7天加分） + 访问频率

### search — 全文搜索 Markdown 文件

```bash
node scripts/memory-cli.js search <关键词> [--limit 20]
```

扫描 memory/ 下所有 `.md` 文件（日志、教训、人物、反思等），按匹配度 + 文件新鲜度排序。

**recall vs search 的区别：**

| | recall | search |
|---|---|---|
| 搜索范围 | 结构化 facts（JSON/SQLite） | 所有 Markdown 文件 |
| 搜索方式 | FTS5 或关键词匹配 | 逐文件逐行扫描 |
| 适合场景 | "我记过什么关于 X 的 fact？" | "memory 里哪个文件提到了 X？" |
| 返回结果 | Fact 对象（含 ID、标签、置信度） | 文件名 + 匹配行 |

### forget — 删除事实

```bash
node scripts/memory-cli.js forget <fact-id>
```

### facts — 列出所有事实

```bash
node scripts/memory-cli.js facts [--tags t1] [--limit 50]
```

### learn — 记录教训

```bash
node scripts/memory-cli.js learn --action "做了什么" --context "什么场景" --outcome positive|negative|neutral --insight "学到了什么"
```

**双写目标：**
- `.data/lessons.json`（或 SQLite lessons 表 + FTS5 索引）
- `memory/lessons/YYYY-MM-DD-<id>.md`

### lessons — 查看教训

```bash
node scripts/memory-cli.js lessons [--context 主题] [--outcome negative] [--limit 10]
```

### entity — 追踪实体

```bash
# 创建
node scripts/memory-cli.js entity "李四" person --attr role=产品经理 --attr timezone=GMT+8

# 更新（同名同类型自动合并属性）
node scripts/memory-cli.js entity "李四" person --attr email=lisi@example.com
```

**双写目标：**
- `.data/entities.json`（或 SQLite entities 表）
- `memory/people/<name>.md`（person 类型）
- `memory/decisions/<name>.md`（其他类型）

### entities — 列出实体

```bash
node scripts/memory-cli.js entities [--type person]
```

### gc — 垃圾回收 / 归档

```bash
node scripts/memory-cli.js gc [--days 30]
```

**做两件事：**
1. **文件归档：** 把超过 N 天的 `YYYY-MM-DD.md` 日志移到 `.archive/YYYY-MM/`
2. **清理低频数据：** 删除 JSON/SQLite 中超过 N 天且访问次数 ≤ 1 的 facts

### reflect — 夜间反思

```bash
node scripts/memory-cli.js reflect
```

在 `memory/reflections/YYYY-MM-DD.md` 生成当日记忆健康报告。

### extract — 知识提炼（教训 → 技能）

```bash
# 查看教训 ID
node scripts/memory-cli.js lessons

# 提炼
node scripts/memory-cli.js extract <lesson-id> --skill-name deploy-checklist
# → 生成 ~/.openclaw/skills/deploy-checklist/SKILL.md
```

把一条教训自动生成 SKILL.md 模板，包含背景、问题、解决方案、使用场景。你可以在此基础上完善，变成一个真正可复用的 Agent 技能。

### stats — 记忆健康面板

```bash
node scripts/memory-cli.js stats
```

显示：facts 总量/活跃/热/温/冷分布、lessons 数量、entities 数量、归档文件数、上次 GC 和反思时间、当前后端类型。

### temperature — 温度报告

```bash
node scripts/memory-cli.js temperature
```

按热/温/冷分类列出所有日志文件。

### export — 导出全部数据

```bash
node scripts/memory-cli.js export
```

以 JSON 格式输出所有 facts、lessons、entities，方便备份或迁移。

---

## 📂 双层存储架构

```
~/.openclaw/workspace/memory/
│
│ ──── Markdown 层（人可读，QMD 可搜索）────
├── 2026-03-07.md              ← 今天的日志
├── 2026-03-06.md              ← 昨天
├── lessons/                   ← 教训文件
│   ├── 2026-03-07-abc123.md
│   └── 2026-03-05-def456.md
├── people/                    ← 人物档案
│   └── zhang-san.md
├── decisions/                 ← 非人物实体
├── reflections/               ← 反思记录
│   └── 2026-03-07.md
│
│ ──── 结构化层（程序用，快速查询）────
├── .data/
│   ├── facts.json             ← 事实（JSON 模式）
│   ├── lessons.json           ← 教训（JSON 模式）
│   ├── entities.json          ← 实体（JSON 模式）
│   └── memory.db              ← SQLite 数据库（SQLite 模式，自动创建）
│
│ ──── 归档层 ────
├── .archive/                  ← GC 归档的冷数据
│   └── 2026-01/
│       ├── 2026-01-05.md
│       └── 2026-01-12.md
│
└── .index.json                ← 索引元数据
```

**设计原则：**
- **写入时双写** — `remember` / `learn` / `entity` 同时写 Markdown 和 JSON/SQLite
- **搜索时互补** — `recall` 走结构化层，`search` 走 Markdown 层
- **Markdown 丢了** — 结构化数据还在，可以重建
- **JSON 丢了** — Markdown 还在，教训和实体有 .md 文件兜底

---

## 🌡️ 温度模型

| 温度 | 时间范围 | 存储位置 | 说明 |
|------|----------|----------|------|
| 🔥 热 | < 7 天 | `memory/*.md` | 活跃数据，高频访问 |
| 🟡 温 | 7-30 天 | `memory/*.md` | 近期数据，偶尔访问 |
| ❄️ 冷 | > 30 天 | `memory/*.md` → GC 后移到 `.archive/` | 低频数据，GC 候选 |
| 📦 归档 | — | `memory/.archive/YYYY-MM/` | 已归档，按月分目录 |

温度由文件修改时间自动计算，不需要手动标记。

**GC 规则：**
- 文件层：冷数据（>30天的日志文件）移到 `.archive/`
- 数据层：超过 N 天 + 访问次数 ≤ 1 的 facts 被删除
- 高频访问的 facts 即使很旧也不会被清理（访问计数保护）

---

## ⚡ 智能后端：JSON 与 SQLite

本技能支持两种存储后端，**运行时自动检测、自动选择、自动迁移**：

### JSON 模式（默认，零依赖）

- 适合万级数据量
- 数据存在 `.data/facts.json` 等文件中
- 搜索用内存关键词匹配
- 不需要安装任何额外包

### SQLite 模式（Node.js >= 22.5 自动启用）

使用 Node.js 原生 `node:sqlite` 模块（`DatabaseSync`），**无需安装任何 npm 包**。

自动获得：

| 特性 | 说明 |
|------|------|
| **FTS5 全文搜索** | FTS5 + LIKE 双引擎，英文走 FTS5，中文走 LIKE 子串匹配 |
| **ACID 事务** | 数据写入更安全，不怕写到一半断电 |
| **WAL 模式** | 读写并发性能好，多 Agent 同时访问不冲突 |
| **百万级数据** | 轻松处理大量 facts/lessons |
| **自动迁移** | 首次启用时自动把 JSON 数据导入 SQLite |

**完全自动：**
1. Node.js >= 22.5 → 自动检测 `node:sqlite`
2. 自动创建 `memory.db` → 自动导入已有 JSON 数据
3. 显示 `[sqlite]`

**降级也无感：** Node.js < 22.5 自动回到 JSON 模式（JSON 文件一直保持更新）。

---

## 🔗 与 OpenClaw 深度集成

### 1. memory_search 原生兼容

所有 Markdown 文件在 `~/.openclaw/workspace/memory/` 下，OpenClaw 的 `memory_search` 工具**直接可搜**，不需要任何额外配置。

### 2. OpenClaw Cron 定时任务

用 OpenClaw 内置 cron，不碰系统 crontab：

```bash
# 每周日凌晨自动 GC 归档
openclaw cron add --name "memory-gc" \
  --schedule "0 0 * * 0" --tz "Asia/Shanghai" \
  --agent main \
  --message "运行：node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js gc"

# 每晚 23:45 自动反思
openclaw cron add --name "memory-reflect" \
  --schedule "45 23 * * *" --tz "Asia/Shanghai" \
  --agent main \
  --message "运行：node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js reflect"
```

### 3. Agent 直接调用

Agent 可以通过 `exec` 工具直接执行：

```bash
# 在对话中记住重要信息
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js remember "重要信息" --tags important

# 回忆相关知识
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js recall "关键词"
```

### 4. Heartbeat 集成

在 `HEARTBEAT.md` 中加入记忆维护：

```markdown
## Memory Maintenance
- 每周检查一次 `stats`，如果冷数据 > 20 个就运行 `gc`
- 每月检查 lessons，考虑提炼高价值教训为 skill
```

---

## 🔄 Agent 每日工作流

### 会话开始

1. 读取 `MEMORY.md` 获取核心记忆
2. 运行 `stats` 检查记忆健康
3. 运行 `recall` 获取当前任务相关上下文

### 会话中

| 触发事件 | 建议操作 |
|----------|----------|
| 用户提到重要信息 | `remember "信息" --tags 相关标签` |
| 用户纠正了错误 | `learn --action "做错了什么" --outcome negative --insight "正确做法"` |
| 发现了好方法 | `learn --action "做对了什么" --outcome positive --insight "总结"` |
| 遇到新的人/项目 | `entity "名字" 类型 --attr key=value` |
| 用户说"记住这个" | `remember "内容" --tags user-requested` |
| 需要查找之前的决策 | `recall "关键词"` 或 `search "关键词"` |
| 某个信息过时了 | `supersede 旧id "新信息"` 或 `forget 旧id` |

### 每日结束

1. 更新每日日志（自动，通过 remember 命令已经在写了）
2. 有价值的对话总结 → `remember` 存入

### 每周 / 定时

| 任务 | 频率 | 命令 |
|------|------|------|
| GC 归档 | 每周 | `gc` |
| 夜间反思 | 每日 | `reflect` |
| 温度检查 | 按需 | `temperature` |
| 教训提炼 | 按需 | `extract <id>` |

---

## 💻 系统要求

| 要求 | 说明 |
|------|------|
| **Node.js** | >= 22.5 推荐（原生 SQLite）；18+ 可用（JSON 模式） |
| **磁盘** | 通常 < 1MB（SQLite 模式 < 5MB） |
| **外部依赖** | **无**。SQLite 使用 Node.js 原生 `node:sqlite` 模块 |

**不需要**：Python、bash、rsync、系统 crontab。

---

## 📁 文件结构

```
smart-agent-memory/
├── SKILL.md                     # 技能定义（Agent 读）
├── README.md                    # 本文档（人读）
├── _meta.json                   # 技能元信息
├── lib/
│   ├── store.js                 # JSON 存储引擎 + 工厂函数（自动选择后端）
│   ├── sqlite-store.js          # SQLite 存储引擎（FTS5 + WAL）
│   ├── temperature.js           # 温度模型 + GC 归档
│   ├── search.js                # 轻量 Markdown 全文搜索
│   └── extract.js               # 教训 → 技能提炼
└── scripts/
    └── memory-cli.js            # CLI 入口（14 个命令）
```

---

## ❓ 常见问题

### Q: 为什么要用 qmd？安全吗？

**qmd 是可选的高级搜索工具**，用于增强搜索质量（BM25 + 向量 + 重排序）。如果不安装 qmd，搜索功能会自动降级到内置的纯 JS 搜索（TF-IDF 词频算法），两者都能正常工作。

**安全性说明：**
- qmd 只在 `search` 命令中被调用，且参数完全可控
- 10 秒超时保护，防止无限等待
- 错误自动捕获，不可用时无缝降级
- 不存在命令注入风险（参数作为数组传递，非 shell 拼接）

### Q: 和 OpenClaw 自带的 memory/ 目录冲突吗？

**不冲突。** 本技能就是管理 `workspace/memory/` 目录的，与 OpenClaw 的 `memory_search` 完全兼容。结构化数据在 `.data/` 子目录下，不影响现有的 `.md` 文件。

### Q: 已有 memory/ 下的日志文件会被破坏吗？

**不会。** 本技能只追加内容（appendDailyLog），不修改已有文件。GC 归档是移动文件（rename），不是删除。

### Q: JSON 数据丢了怎么办？

Markdown 文件还在。教训和实体都有对应的 `.md` 文件。JSON 丢了最多损失 facts 的访问计数等元数据，核心信息在 Markdown 中有备份。

### Q: SQLite 数据库损坏了怎么办？

删掉 `.data/memory.db`，下次运行自动从 JSON 文件重建（前提是 JSON 文件还在）。双层存储的好处就是互为备份。

### Q: 数据量大了会慢吗？

- **JSON 模式：** 万级 facts 没问题（内存操作）
- **SQLite 模式：** 百万级没问题（索引 + FTS5）
- **Markdown 搜索：** 千级文件秒出结果
- **GC 会自动归档冷数据**，控制活跃文件数量

### Q: 能和其他 Agent 共享记忆吗？

**可以。** memory/ 目录在 workspace 下，多 Agent 共享同一个 workspace 就共享记忆。用 `--tags` 区分不同 Agent 的 facts。SQLite 的 WAL 模式支持并发读写。

### Q: 在 Mac 上创建的记忆，Windows 上能用吗？

**可以。** JSON 和 SQLite 都是跨平台格式。配合 `myopenclaw-backup-restore` 技能备份还原，跨平台迁移零障碍。

### Q: 从旧版 agent-memory-system 迁移过来方便吗？

**很方便。** 旧版的 memory/ 目录结构（日志、lessons、people 等）和本技能**完全兼容**。安装后直接用，已有的 .md 文件自动被 search 命令搜索到。只需要运行 `remember` 把重要信息录入结构化层即可。

### Q: stats 显示 [json] 而不是 [sqlite]？

需要 Node.js >= 22.5 才能使用原生 `node:sqlite`。运行 `node -v` 确认版本。如果低于 22.5，JSON 模式也完全可用。

---

## 📜 版本历史

- **v2.0.0** — 零依赖重构
  - 从 better-sqlite3 迁移到 Node.js 原生 `node:sqlite`（DatabaseSync），彻底零外部依赖
  - 去除 crypto 模块依赖，改用时间戳+随机数生成 ID
  - 目录 lazy init：不再构造时创建所有子目录，按需创建
  - FTS + LIKE 双引擎搜索：英文走 FTS5，中文走 LIKE 子串匹配
  - 搜索集成 qmd：`search` 命令优先走 qmd（BM25+向量+rerank），不可用时自动降级内置搜索
  - reflect 命令增强：输出高频标签、最近实体、Skill 经验统计、最近教训
  - JSON→SQLite 迁移后提示清理旧文件
  - 对话标准流程（开场/过程/结束）写入 SKILL.md
  - cron 配置改为标准 JSON 格式，可跨设备

- **v1.0.0** — 初始版本
  - 融合 agent-memory-system（温度/归档/反思/提炼）+ agent-memory（Fact/Lesson/Entity/FTS）
  - 双层存储：Markdown + JSON/SQLite
  - 智能后端自动检测 + 自动迁移
  - 14 个 CLI 命令
  - 纯 Node.js 跨平台

---

## 🤝 致谢与来源

本技能站在两个优秀项目的肩膀上：

| 来源项目 | 作者 | 继承的核心设计 |
|----------|------|---------------|
| **agent-memory-system** | 阿福 | 温度模型、自动归档 GC、夜间反思、技能提炼、文件驱动架构 |
| **agent-memory** | ClawHub 社区 | Fact/Lesson/Entity 三层模型、全文搜索、置信度、访问追踪、置换链、实体属性合并 |

感谢两位（组）作者的开源贡献。

**许可证：** MIT
