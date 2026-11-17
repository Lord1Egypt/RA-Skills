# 元习知识库（KB v1）参考

知识库把「验证过、可复用」的知识按分类沉淀下来，任何智能体都可以经 CLI 读写、按关键词查询。

> 使用时机：**写**（命令失败 / 被纠正 / 更好做法 / 知识过时 / 缺能力 / 外部故障触发，按归位决策树定位后立即写）与**查**（开工前 / 动手解决不显然问题前 / 沉淀前查重 / 复盘时过草稿）；完整模型见 SKILL.md「使用模型」。项目专属经验写项目自身文件，私密信息进元忆私密区；旧 `.learnings/` 为遗留兼容（读取 / 处置 / 迁移）。

> 命令前缀：本文示例统一用技能目录直跑写法 `python3 scripts/yotta_learn.py <命令>`；已装 CLI 时把该前缀替换为 `yotta-learn`（如 `yotta-learn kb query 中文检索`），两者完全等价。

## 快速上手

```bash
# 1) 初始化（默认 ~/.yottalearn/knowledge；已存在拒绝覆盖）
python3 scripts/yotta_learn.py kb init

# 2) 创建分类（slug 英文小写连字符；name / description 必填）
python3 scripts/yotta_learn.py kb category create agent-skills \
  --name "智能体与技能开发" --description "技能开发与编排相关知识与方法"

# 3) 写入草稿（默认 draft；source 必填，--from-learning 时自动生成）
python3 scripts/yotta_learn.py kb add --category agent-skills \
  --title "SQLite FTS5 中文检索的坑" \
  --message "FTS5 默认分词对中文不友好，需要 bigram 或外部分词器。" \
  --tags "sqlite,检索" --source "experiment"

# 4) 核验（先看三问清单；通过需要证据）
python3 scripts/yotta_learn.py kb review KB-20261005-001
python3 scripts/yotta_learn.py kb review KB-20261005-001 --pass --evidence "本地实测通过"

# 5) 查询（默认只出已核验；中文 bigram 分词）
python3 scripts/yotta_learn.py kb query 中文检索
```

## 信任模型

- 写入默认 **draft**；查询默认只出 **verified**；draft 需要 `--include-draft` 显式包含。
- `review --pass` 要求证据（`--evidence` 或条目已有 evidence），并做去重检查；标题与同分类已有条目一致时阻断，确认不重复后用 `--force` 放行。
- 敏感扫描（密钥 / 个人信息 / 本机路径）在写入时提示、核验时阻断；确需保留样例时用 `--force --note` 说明并留审计。
- `review --reject` 把条目移入回收站（保留 7 天），可 `kb trash purge` 清理。
- `deprecate` 保留条目与出处、只标记过期；默认查询不返回，需要 `--status deprecated` 显式查询。

## 写库门槛（什么适合 / 什么不适合）

- **适合**：跨项目可复用的方法 / 流程 / 清单（核查点、检查表）、避坑 / 教训（根因 + 触发条件 + 解法）、教程 / 判据（怎么判断 / 选型 / 验证）。
- **不适合**（按归位决策树去别处）：单次项目的具体发现 / 决策依据 → 项目自身文件；事实 / 红线 / 承诺 → 元忆；私密 / 敏感（密钥、凭据、个人信息、本机路径）→ 元忆私密区；未验证猜测 / 一次性现场数据 → 不写或留草稿待验证。
- **三问判定标准**（写入与核验同一标准）：
  1. 验证过？有可验证证据：亲手实测 / 实审命中并回读确认；evidence 写明「在哪、怎么验的」。
  2. 自包含？离开原会话 / 原项目仍可复用：正文自带判据、步骤、关键词。
  3. 无敏感？无密钥 / 凭据 / 个人信息 / 本机路径；涉及具体项目未修复漏洞细节的，标注共享边界（本机可留、共享前脱敏）。
- **身份**：CLI `--agent <名字>` / 环境变量 `YOTTA_LEARN_AGENT`；MCP `agent` 参数（缺省 `mcp`）；面板动作记 `view`。不声明则记 `unknown@<host>`，审计断链。
- **审核口径**：`--pass` 必须过三问 + 有证据；自审允许（逐条过三问并写明证据）；跨智能体共享面 / 高价值条目建议另一智能体或用户复核（当前不强制阻断）。

## 位置与配置

优先级：`--dir` > 环境变量 `YOTTA_LEARN_KB` > 配置文件 `~/.yottalearn/config.json` > 默认 `~/.yottalearn/knowledge`。旧版位置（`~/.yottaskills/yotta-learn.json` / `~/.yottaskills/knowledge`）只读兼容：回退生效时读操作可用，写操作 fail-closed（exit 5）并提示一次性迁移命令；迁移后写入恢复。

```bash
python3 scripts/yotta_learn.py kb config set --dir /path/to/kb           # 持久化位置（仅切换指针）
python3 scripts/yotta_learn.py kb config set --dir /path/to/kb --move    # 迁移（复制 → 校验 → 切配置 → 旧库移出原位）
python3 scripts/yotta_learn.py kb config set --dir /path/to/kb --move --from /old/kb   # 指定源库补迁
python3 scripts/yotta_learn.py kb config get [--json]                    # 来源 / 未迁移 / 最近迁移
python3 scripts/yotta_learn.py kb config clear                           # 清除配置（不删数据）
```

- 迁移 fail-closed：复制到暂存目录 → `doctor` + 内容摘要双校验 → 原子落位；任一步失败不切配置、旧库不动、暂存清理。
- 不带 `--move` 只切指针：若旧库已初始化会明确提示「旧库未迁移」并给出可执行的补迁命令（不静默、不假成功）。
- 迁移成功后旧库改名 `<原名>.kb-moved-<时间戳>`（同目录），确认新库无误后可删除（建议保留 7 天）。

## AI 接口（MCP）与图形化管理台

- MCP stdio：`scripts/yotta_learn_mcp.py` —— 读 `kb_query` / `kb_get` / `kb_list` / `kb_stats` / `kb_categories`；写 `kb_add` / `kb_review` / `kb_update` / `kb_deprecate` / `kb_category_create` / `kb_category_rename` / `kb_category_merge` / `kb_category_deprecate`；运维 `kb_doctor` / `kb_index_rebuild`。写工具与 CLI 同源 fail-closed（草稿 / 审核门 / 敏感阻断 / 非空分类停用需 `force`）。
- 图形化：`yotta-learn view`（运行时真命令；技能目录直跑等价 `python3 scripts/yotta_learn.py view`；默认 `127.0.0.1:8791`，`--port` 可改；页面内嵌本机会话令牌；破坏性动作需确认串；全部写操作留审计；零远程资源）。
- 升库：`kb add --from-learning <LRN-ID> [--learnings-dir <目录>]` 从 `.learnings` 条目生成草稿（正文含可移植来源引用，仍走审核门）。

## 目录结构

```
<kb-root>/
  kb.json                      # 库元信息（schema / 创建时间 / 创建者）
  categories/<slug>/
    category.json              # slug / name / description / aliases / status
    entries/<ID>.md            # 条目（frontmatter + 正文）
    index.json                 # 分类倒排分片（派生数据，可重建）
  index/global.json            # 全局词表（term → 分类）
  index/stats.json             # 统计缓存（派生）
  audit/audit.jsonl            # 审计（agent@host / 动作 / 目标 / 结果）
  .trash/                      # 回收站（保留 7 天）
  snapshots/                   # 破坏性操作前自动快照（保留最近 20）
```

## 条目格式

```markdown
---
id: KB-20261005-001
title: 'SQLite FTS5 中文检索的坑'
category: agent-skills
tags: ["sqlite", "检索", "中文"]
status: draft
confidence: medium
source: 'experiment'
evidence: ''
author: 'codex@host'
created: '2026-10-05T12:00:00+08:00'
updated: '2026-10-05T12:00:00+08:00'
verified_by: ''
verified_at: ''
related: []
---

## 要点 / 步骤

默认分词对中文不友好，需要 bigram 或外部分词器。
```

- frontmatter 为受控子集：单行键值；字符串可用单引号（内含单引号双写）；数组用 JSON 语法；未知字段拒绝解析（fail-closed）。
- 必填：id / title / category / status / source / author / created；evidence 在核验通过时必填。
- ID：`KB-YYYYMMDD-XXX`（按天自增）；重命名与分类迁移不改 ID。
- 正文建议按「适用场景 / 要点步骤 / 边界与坑 / 出处」组织，便于复用与复核。

## 命令一览

| 命令 | 作用 |
|---|---|
| `kb init [--dir]` | 初始化知识库（已存在或目录非空时拒绝覆盖） |
| `kb config set --dir <路径>` / `get` / `clear` | 位置持久化与来源显示 |
| `kb category create <slug> --name --description [--alias]` | 创建分类（查重 + 别名） |
| `kb category list` / `rename` / `merge` / `deprecate` | 分类治理（合并迁移条目并留别名） |
| `kb add --category --title --message --source [--tags --evidence --confidence]` | 写入草稿 |
| `kb list [--category --status --tag --limit]` | 条目管理列表 |
| `kb show <ID>` | 查看条目全文 |
| `kb update <ID> [--title --message --tags --source --evidence --confidence]` | 更新条目字段 |
| `kb review <ID> [--pass / --reject --note] [--evidence] [--force]` | 审核门（三问清单 + 去重 + 敏感扫描） |
| `kb query <关键词...> [--category --status --tag --limit --include-draft --include-deprecated]` | 关键词查询 |
| `kb deprecate <ID> --reason` | 停用条目（保留可查） |
| `kb index rebuild` / `kb index status` | 全量重建 / 健康状态（漂移检测） |
| `kb stats` / `kb doctor [--backup-dir]` | 统计 / 体检 |
| `kb backup create --out <目录>` / `list` / `restore` | 独立目录备份与恢复 |
| `kb trash list` / `purge [--days N] [--all]` | 回收站查看与清理 |
| `kb snapshot list` / `restore <name>` | 快照查看与恢复 |

读取类命令（`list` / `show` / `query` / `stats` / `doctor` / `index status` 与各 `list`）支持 `--json`，便于智能体解析。

## 查询与索引

- 切词：拉丁按符号边界；中文 bigram（2-gram）+ 单字兜底。
- 索引：每分类一个分片 + 全局词表；写入自动增量刷新；`kb index rebuild` 全量重建。
- 评分：标题权重 5 / 标签 3 / 正文 1；状态与 confidence 加成；时间衰减；命中覆盖度作为次级排序。
- 过滤：`--category` / `--status`（默认 verified，可逗号分隔多值）/ `--tag` / `--limit`（0 = 不限）/ `--include-draft` / `--include-deprecated`。
- 索引漂移（条目被外部改动）时自动降级线性扫描并在输出中提示；用 `kb index status` 查看，`kb index rebuild` 修复。

## 可靠性

- 原子写（临时文件 + rename）+ 跨进程写锁（过期自动接管；超时退出码 6）。
- 破坏性操作（合并 / 停用 / 拒绝 / 恢复）前自动快照；快照保留最近 20 个。
- 删除入回收站保留 7 天；`kb trash purge` 清理过期项。
- 备份到独立目录：`kb backup create --out <目录>`、`kb backup list`、`kb backup restore`（目标非空需 `--force`）。
- `kb doctor` 检查结构 / 索引漂移 / 锁 / 回收站 / 快照 / 容量；`--backup-dir` 时附带备份状态。

## 边界

- 不写入私密信息（密钥、凭据、个人信息、本机路径）——审核门会扫描并阻断。
- 不做云端同步、不做语义检索（embedding）、不做自动抓取；知识分类由使用方创建并治理。
- 团队权限矩阵不在当前版本；同机接入的智能体共享同一知识库，审计记录 `agent@host`。

## 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 未找到（条目 / 快照 / 备份） |
| 4 | 用法或校验错误（含分类不存在、字段非法） |
| 5 | 门禁阻断（敏感命中 / 疑似重复） |
| 6 | 完整性（库已存在拒绝覆盖 / 数据损坏 / 写锁超时） |
