---
name: yotta-learn
slug: yotta-learn
version: 0.6.6
displayName: 元习·经验沉淀与知识库
summary: 学习闭环 + 知识库：把错误、纠正与洞见沉淀为可复用经验条目，把验证过的知识存入分类索引的知识库并支持关键词查询，跨会话供后续会话与技能改进复用。
description: '元习 —— 跨智能体的知识库技能：把跨项目可复用的经验、方法、避坑与教程沉淀进分类知识库（草稿 → 审核 → 可检索），供所有智能体与项目复用；首次使用由 AI 引导初始化知识库位置并自动接入 MCP。触发：值得沉淀的时刻（命令失败 / 被用户纠正 / 发现更好做法 / 知识过时 / 请求缺失能力 / 外部接口故障）与需要查询知识的时刻（开工前 / 动手解决不显然问题前 / 用户问"以前怎么解决的"）；或用户说 知识库 / kb / 查知识 / 记一笔 / 沉淀 / 经验 / 踩坑 / self-improvement / learnings 等。边界：私密 / 敏感信息不写入知识库（走元忆私密区）；项目专属经验写项目自身文件；不自动改动系统文件。'
tags: [经验沉淀, 学习闭环, 复盘, 知识管理, 知识库, 知识检索, learnings, knowledge base, 自我改进]
category: knowledge-management
license: MIT
homepage: https://github.com/YottaMeta/yotta-learn
---
# 元习（yotta-learn）

把「这次学到的」变成「下次可复用的」：跨项目通用的**经验、方法、避坑与教程**沉淀进**分类知识库（KB）**，供后续会话与其他智能体检索复用。

## 使用模型（先读这一节）

### 归位决策树：这条东西写哪里？

| # | 判据 | 去向 |
| --- | --- | --- |
| 1 | 私密 / 敏感（令牌、个人信息、关系、本机内部数据） | 元忆私密区（PREF / BOUND / COMMIT）；绝不进 KB 与项目公开文件 |
| 2 | 只对当前项目成立（仓库怪癖、部署细节、项目决策依据） | 项目自身载体（AGENTS.md / docs / 项目状态与任务文件等），直接写目的地 |
| 3 | 跨项目可复用知识（方法 / 流程 / 避坑 / 教程） | 本技能 KB：`kb add`（草稿）→ 三问审核 → verified |
| 4 | 事实 / 结论 / 红线（跨项目共享的记忆型信息） | 元忆 FACT +（长期红线）机器级记忆锚点 |
| 5 | 已成熟、可流程化的经验 | 技能化（护栏 / 门禁 / 清单 / 规则） |

一句话：**「事」进元忆，「法」进知识库，「项目专属」进项目，「未定形」进 KB 草稿。**

### 写库门槛：什么适合 / 什么不适合（进 KB 前必读）

**适合写 KB**（跨项目可复用的「法」）：

- 方法 / 流程 / 清单：可复用的操作步骤、核查点、检查表；
- 避坑 / 教训：根因 + 触发条件 + 解法；
- 教程 / 判据：怎么判断 / 怎么选型 / 怎么验证。

**不适合写 KB**（按归位决策树去别处）：

- 单次项目的具体发现 / 结论 / 决策依据 → 项目自身文件（把可复用的部分归纳出来才进 KB）；
- 事实 / 红线 / 承诺 → 元忆（FACT / BOUND / COMMIT）；
- 私密 / 敏感（密钥、凭据、个人信息、本机路径）→ 元忆私密区，绝不进 KB；
- 未验证的猜测 / 一次性现场数据 → 不写，或留 KB 草稿等验证。

**三问判定标准**（写入与 `kb review` 同一标准）：

1. **验证过？** 有可验证证据：亲手实测 / 实审命中并回读确认（不是「看起来对」）；evidence 写清「在哪、怎么验的」。
2. **自包含？** 离开原会话 / 原项目仍可复用：正文自带判据、步骤、关键词，不依赖上下文。
3. **无敏感？** 无密钥 / 凭据 / 个人信息 / 本机路径；涉及具体项目未修复漏洞细节的，标注共享边界（本机库可留，共享前脱敏）。

**身份与审核**：

- **写库带身份**：CLI 用 `--agent <名字>` 或设 `YOTTA_LEARN_AGENT`（MCP 用 `agent` 参数，缺省 `mcp@<host>`）；不声明则审计记 `unknown@<host>`，来源断链。
- **审核口径**：`kb review --pass` 必须过三问 + 有证据；敏感 / 重复命中用 `--force --note` 留审计。自审允许（逐条过三问并写明证据）；跨智能体共享面 / 高价值条目建议由**另一智能体或用户复核**后再 verified（当前不强制阻断）。

- **写前查重**：先 `kb query` / `kb list`，已有同题就更新，不新建。
- 旧 `.learnings/` 已退役为遗留兼容（见下文专节）：新知识不再默认写入。

### 写 / 查时机

**什么时候写**（按归位决策树定位后立即写，不积攒）：

- 事件驱动：命令失败、被用户纠正、发现更好做法、知识过时、请求缺失能力、外部接口故障；
- 周期驱动：批次复盘三问（能否护栏化？能否复用？归哪层？）、周级 review（草稿 → verified / 合并 / 废弃）、月级自评。

**什么时候查**（默认动作，不靠自觉）：

- 开工时：按当前任务关键词 `kb query <关键词>`（结果为空再动手）；
- 动手解决"不显然"的问题之前：先查有没有现成经验；
- 沉淀前：查重；
- 复盘时：`kb list --status draft` 过一遍草稿。

### 分类治理

- **复用优先**：写前先 `kb category list` 看现有分类，能装下就复用；
- **新建门槛**：现有分类都无法容纳才新建；slug 用小写连字符，名称与描述必填；
- **一条一主分类**：检索补充用 `--tags`；
- **周期治理**：周级 review 时用 `kb category merge` / `kb category deprecate` 合并或停用碎片分类。

## 首次使用：激活知识库（AI 必做）

首次加载本技能时，AI 先运行 `kb config get` 判定状态，然后：

1. **未初始化**：向用户说明用途 → 请用户确认库位置（默认 `~/.yottalearn/knowledge`，可指定其它位置）→ 用户确认后执行初始化（默认位置直接 `kb init`；指定其它位置先 `kb config set --dir <路径>` 再 `kb init`）；
2. **写「发现锚点」**：把库位置与查询方式写入机器级记忆（各宿主全局 AGENTS.md 等效文件），让后续会话与其他智能体都能发现；
3. **自动接入 MCP**：把本技能的 MCP server 写入当前客户端 `mcpServers`（见「AI 接口（MCP）」），并写永久记忆护栏；未加载时自动降级 CLI；
4. **自检回报**：`kb stats` 确认可用（0 条也算成功激活）。

位置由用户确认（数据主权）；其余步骤全部由 AI 执行。同机后续智能体读取同一 `~/.yottalearn/config.json`（单一真源），只需完成第 3 步的 MCP 接入即可共享同一库。

## 命令入口

两种等价用法，按可用性择一：

- **已装 CLI**：`yotta-learn <命令>` —— 如 `yotta-learn kb query 关键词`、`yotta-learn view`（图形管理台）。
- **技能目录直跑**：`python3 scripts/yotta_learn.py <命令>` —— 与 CLI 完全等价。

安装 / 更新技能本体（把技能装进智能体目录，不是装 CLI）：

```bash
npx -y @yottameta/yotta-learn install --agent <名称>   # 推荐：装到指定智能体用户级技能目录
npx -y @yottameta/yotta-learn --agent <名称>           # 旧用法兼容（等价）
# 全局安装后专属安装器入口同样可用：yotta-learn-install --agent <名称>
```

## 知识库（KB）

- 位置：默认 `~/.yottalearn/knowledge`（配置 `~/.yottalearn/config.json`）；优先级 `--dir` > `YOTTA_LEARN_KB` > 配置 > 默认。旧版位置只读兼容：回退生效时写操作 fail-closed 并提示一次性迁移；迁移用 `kb config set --dir <新位置> --move`。
- 结构：`categories/<slug>/`（category.json + entries/ + index.json）+ 全局索引 + 审计 + 回收站 + 快照。
- 条目：Markdown + 受控 frontmatter；ID `KB-YYYYMMDD-XXX`；状态机 draft（默认）→ verified → deprecated。
- 查询：中文 bigram + 单字兜底；默认只出 verified（`--include-draft` 可含草稿）。
- 审核门：`kb review <ID> --pass --evidence "..."`（核验需证据）；敏感 / 疑似重复会阻断，可用 `--force --note "说明"` 留审计放行。
- 常用命令：

```bash
yotta-learn kb init                                   # 初始化（幂等；已存在拒绝覆盖）
yotta-learn kb config get                             # 位置与状态（未初始化会给引导提示）
yotta-learn kb category create <slug> --name "..." --description "..."
yotta-learn kb add --category <slug> --title "..." --message "..." --source "..."
yotta-learn kb review <KB-ID> --pass --evidence "..."
yotta-learn kb query <关键词>
yotta-learn kb list --status draft
yotta-learn kb doctor                                 # 体检
yotta-learn kb backup create --out <目录>              # 备份
yotta-learn view                                      # 图形管理台（仅 127.0.0.1:8791）
```

- 完整命令面、数据协议与可靠性说明：`references/kb.md`。

## AI 接口（MCP）

`scripts/yotta_learn_mcp.py`（stdio；读 kb_query / kb_get / kb_list / kb_stats / kb_categories，写 kb_add / kb_review / kb_update / kb_deprecate / kb_category_*，运维 kb_doctor / kb_index_rebuild；写工具 fail-closed，与 CLI 同源）。

**AI 自动接入**：首次使用时把该 server 写入客户端 `mcpServers` 并写永久记忆护栏；未加载自动降级 CLI。配置示例：

```json
{"mcpServers":{"yotta-learn":{"command":"python","args":["<技能目录>/scripts/yotta_learn_mcp.py"]}}}
```

## `.learnings` 遗留兼容

`.learnings/`（LEARNINGS / ERRORS / FEATURE_REQUESTS）是本技能旧版的**项目内原始捕获区**，现已退役为遗留形态：

- **不再默认写入**：新知识按「归位决策树」直达归宿（项目自身文件 / KB / 元忆）。
- **已有数据可用**：旧命令（`log` / `list` / `review` / `update` / `resolve` / `promote` / `extract`）全部保留，用于读取、处置与迁移已有条目；`init` 幂等，不覆盖任何已有文件。
- **迁移**：跨项目可复用的条目用 `kb add --from-learning <LRN-ID> --category <slug>` 转成 KB 草稿（仍走审核门）；项目专属条目按决策树第 2 条写进项目自身文件。
- 字段与示例见 `references/examples.md`。

## 元忆联动（可选）

- 遗留条目路径支持 `log --remember` 同步到元忆（yotta-memory）；未安装 / 未初始化 / 失败自动降级（A / B / C），只提示、不阻断。
- 不写入 package.json 依赖。

## Hook 模板

见 hooks/ 目录：Claude Code（claude-settings.json）、Codex（codex-settings.json）、OpenClaw（openclaw-setup.md）；activator.sh / error-detector.sh 为 Linux-only 可选 bash hook。当前 hook 仍指向遗留 `.learnings` 捕获路径，后续批次再改造。

## 参考

- references/kb.md — 知识库完整命令面、数据协议与可靠性说明
- references/faq.md — 常见问题速查（条目写哪 / 首装激活 / 审核 / 备份 / 报错）
- references/walkthroughs.md — 命令失败 / 用户纠正 / 接口降级三类走查（按新归位模型）
- references/examples.md — 遗留 `.learnings` 字段与示例
- references/hooks-setup.md — 各智能体 hook 接入步骤

## 何时使用（速查）

- **沉淀**：上文"什么时候写"任一命中 → 先归位 → 立即写；
- **查询**：开工 / 动手前 / 写前 / 复盘 → `kb query`、`kb list`；
- **首次使用**：走「激活知识库」四步；
- **关键词**：知识库 / kb / 查知识 / 记一笔 / 沉淀 / 经验 / 踩坑 / learnings 等。

**Do NOT**：不把私密 / 敏感信息写进 KB 与项目公开文件；不把项目专属经验塞进共享 KB；未初始化时先走激活引导，不假装可用。

日常排障先看 `references/faq.md`。
