# 技能进化（知行环）· Skill Evolution

> **名字的由来**：主名「**技能进化**」对外使用——它说的是"对象与方向"（技能在往上走）；
> 别号「**知行环**」用于口语指代——它说的是"机制与结构"（知＝判据、行＝沉淀、环＝闭环）。
> 两个名字合起来才是完整的：**技能进化 = 知行环**。
> 英文 id 保持 `skill-evolution` 不变（目录名、`.wiki/` 运行时、hook 都依赖它，改名会破坏已有项目）。

> **两篇论文合成的一条闭环**，不是三个模块的集合。
> WikiSkill 给机制（经验**怎么存、怎么迭代**），RSI 路线图给判据（改进**算不算数、能自动到哪**）。

让 AI Agent 从自己的历史任务中学习，**不再重复踩同一个坑**。

不改模型权重，也不用重新训练——在你的项目里维护一个 `.wiki/` 目录，把每次任务的成败沉淀成结构化经验，再迭代成可复用的技能文档，**每一步都过判据才落库**。

---

## 两篇论文如何结合（这是本 skill 的核心设计）

两篇论文各缺一半，缺口正好互补——这才是"结合"的依据：

| | WikiSkill [arXiv:2608.27454](https://arxiv.org/abs/2608.27454) | RSI 路线图 [arXiv:2609.11873](https://arxiv.org/abs/2609.11873) |
|---|---|---|
| 回答 | 经验**怎么存、怎么迭代** | 改进**算不算真的、能自动到哪** |
| 核心 | 三层记忆 Raw→Wiki→Skill；角色隔离；门控弧 `R_val > R_best` 否则回滚 | HCI 能力余量闭合指数；L1–L5 自主权分级；四大评估追问 |
| **缺口** | 门控**只有一条阈值**，缺"什么样的改进才算数"的判据 | 判据齐备，却**没有可持续存储与回滚的载体** |

**结合方式**：RSI 的四大追问**成为** WikiSkill 门控的评分卡；WikiSkill 的三层**成为** RSI 闭环的沉淀载体。

```
① 选域 ──── RSI / HCI：挑缺口最大的域
   │
② 执行记录 ── Raw 层：只记轨迹，不读 wiki（角色隔离红线）
   │
③ 提炼 ──── Wiki 层：同类失败 ≥2 次即立为模式
   │
④ 原子化提议 ─ Skill 层：一轮只改一个技能
   │
⑤ 门控 ──── ★ 融合点：四大追问评分卡 + WikiSkill 阈值
   │
⑥ 采纳 / 回滚 ─ 技能可回滚；Wiki 永不回滚（失败原因写回 patterns）
   │
⑦ 自主权升阶 ─ RSI / L1–L5：判定下轮能把哪些环节交给 AI
   └──────────────────────────→ 回到 ①
```

**⑤ 是融合点**——WikiSkill 的门控只会问"新版比旧版强吗"，RSI 的四问补上"这个改进到底算不算数"：

| # | 追问 | 证据要求 | 不通过 |
|:-:|------|---------|--------|
| 1 | 可衡量 | ≥2 个同域任务、同判据独立复测 | 退回观察（**自评分不算**） |
| 2 | 可保持 | 间隔一个复盘周期后仍成立 | 降级为"未验证" |
| 3 | 可迁移 | ≥1 个不同任务域或另一平台成功 | 降为项目局部技能 |
| 4 | 可回滚 | 有「变更历史」可恢复上一版 | **一票否决** |

论文数据：WikiSkill 报告 Gemini-3.5-Flash 在 5 个基准上的**平均分 49.5 → 68.1**，且 **Qwen-3.5-9B + WikiSkill（47.4）超过无技能的 Qwen-3.6-27B（39.4）**。
两篇论文的完整出处见文末[「论文与来源」](#论文与来源)。

> 历史沿革：本 skill 由原先的 `wikiskill` + `rsi-knowledge` + `rsi-self-improvement-designer` **三合一**而来；
> v2.0 起不再是"三个模块并排"，而是按上图的**单一闭环**重组。

---

## 目录

- [两篇论文如何结合](#两篇论文如何结合这是本-skill-的核心设计)
- [它解决什么问题](#它解决什么问题)
- [60 秒快速开始](#60-秒快速开始)
- [按平台安装](#按平台安装)
- [从旧版迁移](#从旧版迁移已装过-3-个旧-skill)
- [日常怎么用](#日常怎么用)
- [`.wiki/` 目录说明](#wiki-目录说明)
- [自动化 vs 手动：谁做什么](#自动化-vs-手动谁做什么)
- [什么时候操作（时间线）](#什么时候操作时间线)
- [具体怎么操作（按平台）](#具体怎么操作按平台)
- [联合自动化闭环](#联合自动化闭环)
- [**别这样做（反模式清单）**](#别这样做反模式清单)
- [故障排查](#故障排查)
- [常见问题](#常见问题)
- [文件清单](#文件清单)
- [论文与来源](#论文与来源)

---

## 它解决什么问题

你的 Agent 每次会话都从零开始。上周踩过的坑——某个库的 API 陷阱、某个接口的参数顺序、某种报错的真实根因——这周它会原样再踩一遍，你还得再解释一次。

本 skill 把这些经验写到项目里的 `.wiki/` 目录，让它们**活过会话边界**：

| 没有它 | 有了它 |
|---------------|---------------|
| 同一个坑反复踩 | 踩一次，记一次，之后自动规避 |
| 经验散落在对话历史里 | 沉淀在项目文件中，可 grep、可 review |
| 换工具就失忆（Claude Code ↔ Codex ↔ WorkBuddy） | `.wiki/` 是纯 Markdown，跨平台通用 |
| 靠你每次手动提醒 | 周期性复盘自动提炼模式 |

**它不是什么**：不是记忆插件，不是向量数据库，不需要联网，不调任何云服务。就是一堆 Markdown 文件 + 一套让 Agent 遵守的读写规范。

---

## 60 秒快速开始

最快路径（WorkBuddy / CodeBuddy 用户，什么都不用装）：

```
你：初始化 wiki
```

Agent 会创建 `.wiki/` 目录结构。然后正常干活，任务结束后说：

```
你：记录轨迹
```

积累 3–5 条轨迹后：

```
你：复盘
```

Agent 会把轨迹里的重复模式提炼进 `.wiki/knowledge/patterns.md`。**到这一步就已经有用了**——哪怕从不进行后续步骤，光是这个 patterns 文件就值回票价。

### 手动初始化（Claude Code / Codex，或想自己控制）

**推荐用统一安装器**，它会把运行时复制进项目，之后项目就完全自包含：

```bash
# 在 skill-evolution 解压目录下执行，<项目目录> 换成你的项目路径
python scripts/install.py --platform claude --target <项目目录>
python scripts/install.py --platform codex  --target <项目目录>
```

只想初始化、不动其他东西时，按你实际用的 shell 选一行：

| 你的环境 | 命令 |
|---------|------|
| Windows PowerShell | `python "解压目录\scripts\wiki_init.py"` |
| Windows CMD | `python "解压目录\scripts\wiki_init.py"` |
| Git Bash / WSL / Linux / macOS | `bash "解压目录/scripts/wiki_init.sh"` |
| 无 Python 的 Windows | `powershell -ExecutionPolicy Bypass -File "解压目录\scripts\wiki_init.ps1"` |

三个脚本产出完全相同，只是运行环境不同。

> **为什么不写 `~/.workbuddy/skills/<skill名>/...`**
> `.workbuddy/` 是 **WorkBuddy 的私有目录**，Claude Code / Codex 用户机器上并不存在。
> 早期版本把初始化与 hook 都指向那里，结果在纯 Claude Code 环境下**静默失效**——
> 不报错、不提醒。本版本已改为项目自包含：运行时复制进 `.wiki/scripts/`，
> 生成的文件全部使用项目内路径，项目可整体提交 Git，换机器 clone 后无需重装。

---

## 按平台安装

### WorkBuddy / CodeBuddy

**零配置。** 本 skill 已安装即可用，触发词自动识别。
（两者 **skill 触发方式相同**，但 **CodeBuddy 的定时调度能力受限**——见「自动化 vs 手动」一节的注记。）

### Claude Code

**一条命令搞定**（在 skill-evolution 解压目录下执行）：

```bash
python scripts/install.py --platform claude --target <你的项目目录>
```

它会自动完成：创建 `.wiki/` 骨架 → 把运行时与文档复制进 `.wiki/` → 生成自包含的 `CLAUDE.md` → 安装 Stop hook（相对路径）。

想装到全局而非单个项目：

```bash
python scripts/install.py --platform claude --user
```

> 用户级安装会把运行时放到 **Claude Code 自己的目录** `~/.claude/scripts/skill-evolution/`，
> 而不是 WorkBuddy 的目录，因此不装 WorkBuddy 也能用。
> 注意：它会修改 `~/.claude/settings.json`（该文件可能含 API token 等配置，
> 安装器只追加 hooks 字段，其余内容原样保留）。

手动方式（不用安装器，或想精细控制）：

1. 复制指令模板到项目根目录：

   ```bash
   # Windows (PowerShell)
   Copy-Item "解压目录\references\CLAUDE.template.md" CLAUDE.md

   # Unix
   cp "解压目录/references/CLAUDE.template.md" CLAUDE.md
   ```

2. 初始化 Wiki（按你的 shell 选一行）：

   ```powershell
   # Windows PowerShell
   python "解压目录\scripts\wiki_init.py"
   ```

   ```cmd
   :: Windows CMD
   python "解压目录\scripts\wiki_init.py"
   ```

   ```bash
   # Linux / macOS / Git Bash
   bash "解压目录/scripts/wiki_init.sh"
   ```

3. 编辑 `CLAUDE.md`，把项目名称和描述改成你自己的。

> `CLAUDE.md` 是**全量常驻**加载的——每次会话都会读。它比 WorkBuddy 的按需加载更稳定（Agent 始终知道 wiki 存在），代价是占用一些上下文。
>
> 手动复制的模板里，初始化命令仍指向 `~/.workbuddy/`。如果你没装 WorkBuddy，
> 用模板里的**方式 B**（内联 `mkdir` + `printf`，无任何外部依赖）即可，
> 或改用上面的安装器得到完全自包含的版本。

### Codex (OpenAI)

```bash
python scripts/install.py --platform codex --target <你的项目目录>
```

Codex 没有 hook 机制，因此只生成 `AGENTS.md` 和 `.wiki/`，不写任何配置文件。

手动方式同上，把 `AGENTS.template.md` 复制为项目根目录的 `AGENTS.md`：

```powershell
# Windows PowerShell
Copy-Item "解压目录\references\AGENTS.template.md" AGENTS.md
python "解压目录\scripts\wiki_init.py"
```

```bash
# Linux / macOS / Git Bash
cp "解压目录/references/AGENTS.template.md" AGENTS.md
bash "解压目录/scripts/wiki_init.sh"
```

### 各平台体验差异

| 平台 | 指令文件 | 加载方式 | 自动触发 |
|------|---------|---------|---------|
| WorkBuddy | `SKILL.md` | 按需（匹配触发词才读全文） | 是 |
| CodeBuddy | `SKILL.md` | 按需 | 是 |
| Claude Code | `CLAUDE.md` | 全量常驻 | 否，需你主动提 |
| Codex | `AGENTS.md` | 全量常驻 | 否，需你主动提 |

---

## 从旧版迁移（已装过 3 个旧 skill）

如果你在整合前装过 `wikiskill`、`rsi-knowledge`、`rsi-self-improvement-designer`
中**任意一个或多个**，需要按本节迁移。没装过就跳过——直接按上一节安装即可。

### 哪些必须动，哪些绝不能动

迁移的核心原则：**代码要换，数据不碰**。

| 对象 | 处理 | 原因 |
|------|------|------|
| `.wiki/` 目录（`raw/` `knowledge/` `skills/` `meta/`） | **不动** | 你的经验数据全在这里 |
| `.wiki/knowledge/` 下的 `patterns.md`、`evolution_log.md`、`impact_tracker.md` | **不动** | 同上 |
| `.wiki/scripts/wiki_*.py`、`wiki_*.sh` | 可被重新覆盖 | 文件名与职责保持不变，是**运行时契约** |
| `.wiki/` 目录名本身 | **不改名** | 旧项目、旧 hook、旧文档全都指向它 |
| `~/.workbuddy/skills/wikiskill` 等三个旧 skill 目录 | 移入归档目录 | 触发词已并入 `skill-evolution` |
| `~/.claude/scripts/wikiskill/` | 确认新 hook 生效后删除 | 旧运行时快照，不再被引用 |
| `~/.claude/settings.json` 里的 Stop hook | **必须更新** | 否则永远调用旧目录里的脚本 |
| 项目内 `CLAUDE.md` / `AGENTS.md` 里指向旧 skill 的路径 | 改为项目内 `.wiki/references/` | 旧路径指向已归档目录 |
| 自动化任务 / 定时任务里的旧 skill 名 | 改为 `skill-evolution` | 否则触发不到 |

> 这也就是为什么旧 skill 目录名叫 `wikiskill`、脚本名叫 `wiki_remind.py` 一直没改：
> 它们是**跨项目的运行时契约**，改名会让所有已初始化 `.wiki/` 的项目失效。

### 一条命令的默认迁移（Claude Code 用户级）

安装器**已内置升级逻辑**：检测到 hook 指向旧 `scripts/wikiskill/` 时会自动替换，
并保留 `settings.json` 里的 `permissions`、`env` 等其余配置。

```bash
python ~/.workbuddy/skills/skill-evolution/scripts/install.py --platform claude --user
```

预期输出会明确写出替换了哪条旧命令：

```
检测到整合前的旧运行时：~/.claude/scripts/wikiskill
已升级 hook（替换旧命令，其余配置保留）：
  旧：python ".../scripts/wikiskill/wiki_remind.py"
  新：python ".../scripts/skill-evolution/wiki_remind.py"
```

重复执行是幂等的——第二次会输出"已存在相同命令的 hook"并跳过。

> 整合**之前**的版本会直接输出"已存在 Skill Evolution hook"（旧版英文品牌名）然后跳过，
> 导致新运行时永远装不上。该缺陷已修复；若你用的是旧版 `install.py`，请先更新。

### 已有项目的 `.wiki/` 怎么处理——不用迁移

**这是最容易误解的一点**：`.wiki/` 是**项目级**的，不在 skill 包里。
skill 只提供读写规范，经验数据始终躺在你自己的项目里。

由于目录名（`.wiki/`）、文件名（`patterns.md` / `wiki_remind.py` 等）从旧版到新版
**一个都没改**，`skill-evolution` 打开旧项目时读写的还是同一份 `.wiki/`——
**轨迹、模式、已进化的技能原样续用，零迁移成本**。这正是"契约不可改"的意义。

需要做的只是**刷新项目内那份运行时快照**（旧项目里还是几个月前的旧版）：

```bash
python <skill目录>/scripts/install.py --platform claude --target <项目目录> --no-hook
```

| 行为 | 结果 |
|------|------|
| `.wiki/` 已存在 | **原样保留**，不覆盖任何数据 |
| `.wiki/scripts/` | 5 个脚本刷新为新版（新旧差异仅为提示语品牌名） |
| `.wiki/references/` | 从旧版 4 份补到 6 份，新增 `rsi-framework.md`、`design-playbook.md` |
| `.wiki/raw/`、`knowledge/`、`skills/`、`meta/` | **完全不碰** |
| `CLAUDE.md` / `AGENTS.md` | 已存在则跳过，不会覆盖你自己的项目文档 |
| 重复执行 | 幂等 |

> **为什么加 `--no-hook`？** 项目里可能已有别的 hook（如插件注入的 `SessionStart`），
> 或者你手工调过路径。只刷运行时、不动配置，风险最低。项目还没装过 hook 时才需要
> 去掉这个参数。

刷新后若想让 Agent 在 Claude Code / Codex 里**常驻知道** `.wiki/` 存在，把
`references/CLAUDE.template.md` 的内容追加到项目 `CLAUDE.md` / `AGENTS.md` 末尾即可
（模板只含 wiki 规则，直接追加不影响你原有内容）。

### 交给 AI 执行（推荐）

把下面这段原样发给 AI，它会自己检查并迁移。适用于任何平台。

```text
帮我迁移到 skill-evolution。背景：我之前装过 wikiskill、rsi-knowledge、
rsi-self-improvement-designer 三个独立 skill，现在它们已三合一为 skill-evolution
（~/.workbuddy/skills/skill-evolution/）。请按该 skill README 的「从旧版迁移」
一节执行，并遵守以下边界：

1. 检查 ~/.workbuddy/skills/ 下是否还残留 wikiskill / rsi-knowledge /
   rsi-self-improvement-designer 三个目录。有则整体移入
   ~/.workbuddy/skills_archived/<今天日期>_merged_into_skill-evolution/；
   该归档目录已存在就跳过，不要删除任何内容。

2. 检查 ~/.claude/settings.json 的 hooks.Stop：若 command 指向
   .../scripts/wikiskill/ 或包含旧 skill 名，先备份该文件，再执行
   python ~/.workbuddy/skills/skill-evolution/scripts/install.py --platform claude --user
   安装器会自动替换旧 hook 并保留其余配置。若本身没装 Claude Code hook，跳过。

3. 检查项目根目录的 CLAUDE.md / AGENTS.md，把里面引用
   ~/.workbuddy/skills/wikiskill/（或另两个旧 skill）的路径，改为项目内
   .wiki/references/ 下的对应文件。

4. 检查我创建的定时任务 / 自动化任务，把 prompt 里的旧 skill 名
   替换为 skill-evolution。

5. 硬约束：不要删除、不要重命名任何 .wiki/ 目录，不要改动 .wiki/scripts/
   与 .wiki/knowledge/ 下的文件名——那是数据契约，改名会让旧项目失效。

6. 完成后汇报：改了哪些文件、备份放在哪、哪些需要我手动确认。
```

### 迁移后自检

| 检查项 | 期望结果 |
|--------|---------|
| `ls ~/.workbuddy/skills/` | 只剩 `skill-evolution`，旧三个已归档 |
| `~/.claude/settings.json` 的 Stop hook | 指向 `scripts/skill-evolution/wiki_remind.py` |
| `settings.json` 其余字段 | `permissions` / `env` 等原样保留 |
| 旧项目 `.wiki/` | 目录结构与内容完全未变 |
| 重启会话后在有 `.wiki/` 的项目结束任务 | 能收到「记录轨迹」提醒 |
| 对 Agent 说「记录轨迹」「复盘」 | 正常触发，写进 `.wiki/` |

### 回滚

迁移不删数据，回滚成本很低：

1. 把 `~/.workbuddy/skills_archived/<日期>_merged_into_skill-evolution/` 下的三个目录
   移回 `~/.workbuddy/skills/`；
2. 卸载新 hook：`python ~/.workbuddy/skills/skill-evolution/scripts/install.py --platform claude --uninstall --user`
   （只移除 hook，**绝不删除 `.wiki/` 数据**）；
3. 恢复 `settings.json` 备份。

---

## 日常怎么用

### 触发词

| 你说 | Agent 做什么 |
|------|-------------|
| `技能进化` / `知行环` | 报出技能名即唤醒，载入本 skill 并确认当前意图 |
| `记录轨迹` / `wiki log` | 把当前任务的轨迹追加到 `.wiki/raw/今天.md` |
| `复盘` / `wiki maintain` | 读近期轨迹，提炼失败模式与成功策略 |
| `进化技能` / `wiki evolve` | 提出一个技能改进并验证 |
| `wiki 状态` / `wiki status` | 显示统计：多少条轨迹、多少个模式、多少个技能 |
| `初始化 wiki` / `wiki init` | 创建 `.wiki/` 目录结构 |

### 核心原则：在线只记录，离线才复盘

这是**最容易用错**的地方，值得单独强调。

论文里 Inference Agent 执行任务时**不读 Wiki**（避免混淆变量），Wiki 维护是离线批量做的。

**别在每次任务里跑完整的 ②→③→④→⑤ 链路。** 那是论文的离线训练流程，不是日常用法——会拖慢你，而且在线阶段读 Wiki 反而可能干扰 Agent 判断。

完整的节奏、时机与操作方式见后文[「什么时候操作（时间线）」](#什么时候操作时间线)与[「具体怎么操作（按平台）」](#具体怎么操作按平台)。

### 记录什么，不记录什么

一条轨迹控制在 **10 行以内**。只记：

- 关键决策点（为什么选 A 不选 B）
- 意外（报错的真实根因、文档没写的坑）
- 有效技巧（哪条命令一次就对）

不记流水账（"我打开了 X 文件，然后修改了 Y 函数"——这种没价值）。

---

## `.wiki/` 目录说明

```
.wiki/
├── raw/                      # 原始执行轨迹（按日期追加，不可变）
│   └── 2026-08-31.md
├── knowledge/                # 提炼后的知识（只增不减，永不重置）
│   ├── patterns.md           # 失败模式 FM-xxx + 成功策略 SS-xxx
│   ├── evolution_log.md      # 每次维护的记录
│   └── impact_tracker.md     # 技能提案的验证结果
├── skills/                   # 可执行技能（可回滚）
│   └── <skill-name>.md
└── meta/
    └── config.md             # 配置（创建日期、维护周期等）
```

**三层的区别很关键**：

| 层 | 可否修改 | 说明 |
|----|---------|------|
| `raw/` | 只追加，不修改 | 原始素材，作为追溯依据 |
| `knowledge/` | 只增不减，**永不重置** | 即使技能回滚，知识仍在——这是整个系统的核心价值 |
| `skills/` | 可回滚 | 技能改坏了就退回上一版本 |

**为什么"永不重置"重要**：论文的关键设计是——失败的提案不会丢失。技能可以回滚，但"尝试过什么、为什么失败"会永久留在 Wiki 里，成为下一轮提案的输入。

### 建议纳入 Git

`.wiki/` 是纯文本，建议提交到仓库。这样：

- 团队共享同一份经验
- 换机器 / 换工具都在
- 可 review（"这个模式提炼得对不对"）

> `raw/` 和 `knowledge/` 通常只追加，冲突少；`skills/` 可能并发修改，需人工合并。

---

## 自动化 vs 手动：谁做什么

一句话结论：**记录和复盘可以自动化，判断和验证必须人工。**

下表覆盖七步闭环的全部环节，并标出每步的理论来源（RSI / WikiSkill / 两者交集）。左边是"能不能自动"，右边是"你实际要动手做什么"。

| 闭环步骤 | 理论来源 | 能否自动 | 谁执行 | 你要做什么 | 频率 |
|---------|---------|:--------:|--------|-----------|------|
| — 初始化 `.wiki/` | — | ❌ **手动** | 你 | 说一句「初始化 wiki」，或跑一条命令 | 每项目一次 |
| — 指令常驻（让 Agent 知道 wiki 存在） | WikiSkill | ✅ 自动 | 平台 | 装一次，之后不用管 | 每项目一次 |
| **② 记录轨迹** | WikiSkill（Raw 层） | ⚠️ **半自动** | Agent | hook 只负责"提醒"，**真正落笔仍需 Agent 执行** | 每个任务 |
| **③ 复盘提炼** | WikiSkill（Wiki 层） | ✅ 全自动 | 定时任务 | 建一次定时任务 | 每周 / 每 3–5 任务 |
| **④ 技能提案** | WikiSkill（Skill 层） | ✅ 全自动（产出标「待验证」） | 定时任务 | 建一次定时任务 | 双周 / 每 5–10 任务 |
| **⑤ 门控验证** | **★ 两者交集**（四问评分卡 + 阈值） | ❌ **必须手动** | 你 | 逐项核对四问，决定采纳 / 观察 / 回滚 | 每个提案 |
| **⑥ 采纳 / 回滚** | WikiSkill（双轨原则） | ⚠️ 半自动 | 你判定，Agent 执行 | 拍板；回滚动作可由 Agent 做 | 每个提案 |
| **① 选域 / ⑦ 升阶**（RSI 体检） | RSI（HCI / L1–L5） | ✅ 全自动出方案 | 定时任务 | 同上，可合并进同一个任务 | 每月 |
| 全链自改进方案设计 | RSI | ✅ 全自动出方案 | 定时任务 | 同上 | 每月 |

**三条不可自动的红线**（写在这里，免得反复确认）：

1. **⑤ 门控验证** —— 判断"这个技能改进到底有没有用"需要人看实际效果。论文能自动门控是因为有 held-out 验证集，个人开发没这条件；强行自动化只会让无效技能污染技能库。这正是四问里**「可衡量」**要防的事。
2. **⑥ 采纳 / 回滚决策** —— 自动化最多把提案标成"待验证"，采纳还是回滚由你拍板。注意 **`可回滚` 是一票否决**：没有「变更历史」、恢复不了上一版的技能，无论多有效都不许采纳。
3. **初始化 `.wiki/`** —— 定时任务发现 `.wiki/` 不存在会**跳过而不创建**（避免在无关项目里乱建目录），所以第一次必须手动。

> **关于 CodeBuddy（2026-09-17 联网核实）**：定时调度**分形态**——
> CodeBuddy **IDE / 插件没有**定时任务功能；**CodeBuddy Code（CLI）有**（`/loop`、`CronCreate`），
> 但它是**会话级**的：只在 CLI 运行期间有效、**退出即清除且不写盘**、循环任务 **3 天后自动过期**、
> 中断期间错过的任务**不补跑**。所以它**不能**用来跑"每周 / 每两周复盘"这种长周期任务。
> 若要在 CodeBuddy 上做持久周期，改用 **headless + 外部调度器**：
> `codebuddy -p -y "<编排 prompt>"`，由 Windows 计划任务 / Linux cron / GitHub Actions 定时拉起。
> 否则用「手动兜底」+ Git hook 也能覆盖全部功能，只是需要你主动说触发词。

---

## 什么时候操作（时间线）

### 一次性：每个新项目开工时

| 时机 | 做什么 | 怎么说 / 怎么做 |
|------|--------|----------------|
| 决定在这个项目用它 | 初始化 `.wiki/` | 说「初始化 wiki」，或 `python .wiki/scripts/wiki_init.py` |
| 想省掉每次口头提醒 | 装 L2 提醒（Claude Code / Codex 需要；WorkBuddy 可跳过） | `python scripts/install.py --platform claude --target <项目目录>` |
| 想彻底免手动 | 建 L3 定时任务 | 见下一节「具体怎么操作」 |
| **第一天就能做，别等自动化** | 把已知的坑直接写进 `patterns.md` | 立刻可用，价值最高的一步 |

### 周期性：日常节奏

```
每个任务结束
    └─→ ② 记录轨迹                几秒钟；WorkBuddy 需说一句「记录轨迹」
              ↓  攒够 3–5 条
每周 / 每 3–5 个任务
    └─→ ③ 复盘提炼                自动跑，或说「复盘」
              ↓  再攒 2–3 轮复盘
双周 / 每 5–10 个任务
    └─→ ④ 技能提案                自动跑，或说「进化技能」
              ↓
提案产生后
    └─→ ⑤ 【人工】门控验证（L4）   逐项核对四问，决定采纳 / 观察 / 回滚
              ↓
        ⑥ 采纳 → impact_tracker 标 ✅ ／ 失败 → 回滚技能文件，原因写进 patterns
```

**最容易用错的一点**：不要在**每次任务**里跑完整闭环（②→③→④→⑤）。论文里 Inference Agent 执行任务时**不读 Wiki**（避免混淆变量），Wiki 维护是离线批量做的。在线只做轻量记录，复盘/进化放在周期性时间点。

---

## 具体怎么操作（按平台）

> **命令里的 `python`**：下文统一写 `python`。若你的 Linux / macOS 上只有 `python3`（很常见），
> 把命令里的 `python` 换成 `python3` 即可。安装器**写进 hook 的命令**会自动探测
> `python` / `python3` / `py -3`，那部分无需你手改。
>
> **路径写法**：`<skill目录>` 指本 skill 的安装目录；`<项目目录>` 指你要接入的项目根目录。
> 文中出现 `references/xxx.md` 均指**本 skill 内的**参考文档（两篇论文合并为单一闭环后，不再有跨 skill 指针）。

### 方式 A：手动兜底（任何平台、零安装）

最稳的兜底方案——不装 hook、不建定时任务，只靠触发词。WorkBuddy / CodeBuddy 开箱即用。

| 你说 | Agent 做什么 | 什么时候说 |
|------|-------------|-----------|
| `初始化 wiki` | 创建 `.wiki/` 目录结构 | 项目开工时，一次 |
| `记录轨迹` / `wiki log` | 把当前任务轨迹追加到 `.wiki/raw/今天.md` | **每个任务结束时** |
| `复盘` / `wiki maintain` | 读近期轨迹，提炼失败模式与成功策略 | 攒 3–5 条轨迹后 |
| `进化技能` / `wiki evolve` | 提出一个技能改进，标记待验证 | 复盘 2–3 次后 |
| `wiki 状态` / `wiki status` | 显示统计：轨迹数、模式数、技能数 | 随时 |

> 触发词以 `SKILL.md` 的「快速命令」表为准；上表只是补充了"什么时候说"。

### 方式 B：WorkBuddy 定时任务（免手动，推荐）

直接对 WorkBuddy 说：

> 创建定时任务：每周日 21:00，对 `<项目名>` 项目执行一次经验复盘

**时机怎么选**：挑你确定不会在干活的时间段（周日晚上、工作日凌晨）。复盘是读文件 + 写 Markdown，不影响你手头的会话。

完整 prompt 模板（含全链联合版）见 `references/automation.md`。

### 方式 C：Claude Code —— Stop hook（半自动提醒）

用统一安装器（**不依赖 WorkBuddy**，Claude Code 单独使用也正常）：

```bash
# 项目级 —— hook 用相对路径，项目移动或 clone 后依然有效（推荐）
python scripts/install.py --platform claude --target <项目目录>

# 用户级 —— 运行时装到 ~/.claude/scripts/skill-evolution/，对所有项目生效
python scripts/install.py --platform claude --user

# 卸载（只移除 wiki hook，不删 .wiki/ 数据）
python scripts/install.py --platform claude --target <项目目录> --uninstall
python scripts/install.py --platform claude --user --uninstall

# 只想生成文件、不装 hook
python scripts/install.py --platform claude --target <项目目录> --no-hook
```

安装器**合并而非覆盖**已有配置——你的 `permissions`、其他 hooks 全部保留，重复安装自动跳过，卸载只移除 wiki hook。

平台自适应：Windows 用 `python ... wiki_remind.py`，Unix 用 `bash ... wiki_remind.sh`；
还会自动探测 `python` / `python3` / `py -3`，避免机器上根本没有 `python` 命令时静默失效。
装完**重启会话**才生效。项目移动或 clone 后无需重装——hook 用的是项目内相对路径。

> **旧脚本 `install_claude_hook.py` 已在本次整合中移除。** 它把 hook 指向 `~/.workbuddy/skills/<skill名>/`，
> 那是 WorkBuddy 私有目录——没装 WorkBuddy 的机器上该路径不存在，hook 会静默失效。
> 统一安装器 `install.py` 从不依赖任何 AI 工具的私有目录，也不会写入死链。

### 方式 D：Codex —— AGENTS.md + git hook

```bash
python scripts/install.py --platform codex --target <项目目录>
```

Codex **没有 hook 机制**，安装器只生成自包含的 `AGENTS.md` 和 `.wiki/`，不写任何配置文件。想在提交时得到提醒，自己在 `.git/hooks/post-commit` 里加一段（三种 OS 都经 Git Bash / sh 运行）：

```bash
#!/bin/bash
if [ -d ".wiki" ]; then
  echo "[技能进化] 本次提交若有值得沉淀的经验，先说一句「记录轨迹」"
fi
```

```bash
chmod +x .git/hooks/post-commit   # Windows 上可省略
```

Codex 上是全量常驻 `AGENTS.md`，Agent 始终知道 wiki 存在，但**不会主动记录**——需要你主动说触发词。

### 方式 E（不可自动）：L4 门控验证怎么做

L4 无法自动化，但**有明确的操作步骤**，不装任何东西：

| 步骤 | 做什么 | 在哪看 |
|------|--------|--------|
| 1 | 提案产生后，`.wiki/knowledge/impact_tracker.md` 里会出现一条标着「待验证」的 `PROP-xxx` | `impact_tracker.md` |
| 2 | **什么都不用做**，正常干活。下次遇到同类任务时，留意新技能是否真的被用上、效果如何 | 日常任务 |
| 3 | 判断结果，更新这条提案的状态 | 见下表 |
| 4 | 若失败，把技能文件回滚到上一版；**但失败原因写进 `patterns.md` 保留** | `.wiki/skills/` + `patterns.md` |

判断标准：

| 情况 | 标什么 | 后续动作 |
|------|--------|---------|
| 新技能被用上，且同类任务明显更顺 / 少踩坑 | ✅ **采纳** | 技能文件保留，`status: active` |
| 用了但没改善，或引入新问题 | ❌ **回滚** | 从技能文件的「变更历史」恢复上一版；原因写进 `patterns.md` 成为下轮提案输入 |
| 一直没遇到同类任务 | ⏸ **挂起** | 保持「待验证」，不用急 |

**关键记住**：回滚技能，**Wiki 不动**。`knowledge/` 只增不减——"试过什么、为什么不行"永久留存，这正是论文的核心设计。

**这是质量保障，不是缺陷。**

---

## 联合自动化闭环

七步闭环可以打包进**同一个**定时任务，形成一条完整闭环：

```
①⑦ 选域 / 升阶（references/rsi-framework.md，只读）
        ↓  提供 L1–L5 自主权分级、四步闭环、四大追问
   自改进设计（references/design-playbook.md，产出方案，不写文件）
        ↓  定位成熟度 → 选一个切口 → 套四步闭环 → 产出原子化方案
②③④⑥ 经验沉淀（references/workflow.md，唯一写文件的一方）
        ↓  轨迹 / 模式 / 提案写进 .wiki/，提案标「待验证」
⑤ 门控验证（人工，L4）
```

**谁自动、谁手动**：①⑦ 只产出判据与方案，**只有 ②③④⑥ 写文件**（且全部写在 `.wiki/` 内、可回滚）——所以整条链可以被定时任务安全驱动；**唯一的人工介入点是 ⑤ 门控**。

**怎么开**：对 WorkBuddy 说一句即可，把时间换成你的：

> 创建定时任务：每月 1 日和 15 日 21:00，对 `<项目名>` 项目执行一次"RSI + 自改进 + 经验沉淀"联合维护

完整的自包含 prompt（可直接粘贴进任务描述，已写成不依赖当前会话上下文的形式）见：

`references/automation.md` 收录了三种粒度的自包含 prompt：全链联合编排（①–⑦）、仅 RSI 体检（①⑦）、仅自改进设计。合并为单一 skill 后，这些模板都在同一份文档里。

**前置条件**：目标项目必须已有 `.wiki/` 目录。联合任务发现 `.wiki/` 不存在会**跳过不创建**——先手动说一次「初始化 wiki」。

---

## 别这样做（反模式清单）

> **完整版在 `references/anti-patterns.md`**：17 条反模式（使用 / 记录 / 安装运维三类）+ 报错速查表。
> 这里先列最容易踩的 8 条，**装完扫一眼比读完整份文档省时间**。

| ❌ 别这样做 | 为什么错 | ✅ 正确做法 |
|---|---|---|
| 在每个任务里跑完整闭环 | 论文里在线阶段**刻意不读 Wiki**，读了反而降低技能质量 | 在线只做 ② 记录（≤10 行）；③④ 攒 3–5 个任务后离线做 |
| 让日常任务的 Agent 去读 `.wiki/` | 角色隔离红线，会引入混淆变量 | 日常只写 `raw/`；`knowledge/`、`skills/` 由离线复盘角色读 |
| 用自评分当「可衡量」的证据 | 这是防"一次性刷榜"的核心机制，自评分不算证据 | 提案时写死基线判据，之后拿**同一把尺子**复测 |
| 回滚技能时顺手把 `knowledge/` 也删了 | 双轨原则：知识轨**永不回滚** | 撤回 `skills/`，把失败原因**追加**进 `patterns.md` |
| 一轮复盘改好几个技能 | 违反原子化，出问题无法归因 | 一轮只动一个技能，改动最小化 |
| 技能文件不写「变更历史」 | 第 4 问**一票否决**，无法回退就不许采纳 | 用 `references/templates.md` 的技能模板，保留变更历史段 |
| 把模式写成"注意细节"这类废话 | 不可操作，下次遇到 Agent 无法据以行动 | 四要素齐全：触发条件 / 表现 / 根因 / 解决方案 |
| 把 token、密码、真实患者信息写进轨迹 | `.wiki/` 是纯文本**且建议提交 Git**，等于永久留痕 | 凭据用 `<TOKEN>` 占位，业务数据脱敏 |

**遇到报错**（英文 traceback、路径不对、hook 不触发、装完没反应）直接查
`references/anti-patterns.md` 的「报错速查表」——那里是"你看到的报错 / 人话 / 怎么修"三列对照。
脚本遇到问题会**自动重试瞬时故障**，并给出中文的「哪里出错 + 怎么办」，不再抛原始 traceback。

---

## 故障排查

### Windows 相关

**`.sh` 脚本跑不了**

正常——CMD / PowerShell 原生环境没有 bash。三种解法：

| 环境 | 用什么 |
|------|-------|
| Git Bash（显式进入） | `.sh` 可用 |
| WSL | 需已装发行版；**没有发行版时 `.sh` 会报错**（见下） |
| CMD / PowerShell | 用 `.py`（推荐）或 `.ps1` |
| Claude Code hook | **必须** `.py`（hook 走 cmd.exe，不走 Git Bash） |

**Windows 上不要直接敲裸 `bash xxx.sh`**（实测陷阱）

Windows 自带一个 `bash.exe`（**WSL 中继**，位于 `%SystemRoot%\System32\`），它**不是** Git Bash。
它通常排在 PATH 前面，所以裸 `bash` 会命中它；若机器没装 WSL 发行版，你会看到这类报错（而不是脚本跑起来）：

> `%SystemRoot%` 绝大多数机器是 `C:\Windows`，但系统装在别的盘时不成立——所以这里不写死盘符。

```
<3>WSL (12 - Relay) ERROR: CreateProcessCommon:818: execvpe(/bin/bash) failed: No such file or directory
```

三种解法，任选：

| 解法 | 命令 |
|------|------|
| 直接用 `.py`（最省事，安装器在 Windows 上默认就这么做） | `python .wiki/scripts/wiki_init.py` |
| 显式调用 Git Bash 的 bash | `"<Git 安装目录>\bin\bash.exe" .wiki/scripts/wiki_init.sh` |
| 先进入 Git Bash 终端再跑 | 在 Git Bash 里执行 `bash wiki_init.sh` |

**`<Git 安装目录>` 各机不同**，别照抄：Git 默认装在 `C:\Program Files\Git`，但也可能被装到
`D:\Program Files\Git`、`%LOCALAPPDATA%\Programs\Git`（免管理员安装）或任意自选目录。
先查你机器上的实际路径：

| Shell | 查询命令 |
|-------|---------|
| CMD | `where bash` |
| PowerShell | `Get-Command bash \| Select-Object -ExpandProperty Source` |
| Git Bash | `which bash` |

如果输出的第一条是 `%SystemRoot%\System32\bash.exe`（WSL 中继），说明 Git Bash 的 bash 不在 PATH 前面——
那就往下取第二条，或直接改用上表的 `.py` 方案，最省事。

**Claude Code hook 装了没反应**

按这三个原因依次排查，它们都会**静默失败**（hook 失败不阻断会话，也没有任何报错）：

| 原因 | 排查 | 解法 |
|------|------|------|
| 命令用了 `.sh`（Windows） | 看配置里是否有 `bash ... wiki_remind.sh` | 用 `install.py` 重装，它会自动选 `.py` |
| 脚本路径指向不存在的位置 | 配置里是 `~/.workbuddy/skills/<skill名>/...` 但你没装 WorkBuddy | 用 `install.py --platform claude` 重装 |
| 机器上没有 `python` 命令 | 终端执行 `python --version` | 安装器会自动探测 `python3` / `py -3`；老配置需手动改 |

重装：

```bash
python scripts/install.py --platform claude --target <项目目录> --uninstall
python scripts/install.py --platform claude --target <项目目录>
```

手动验证 hook 本身能不能跑（需在项目根目录执行）：

```bash
python .wiki/scripts/wiki_remind.py
```

**PowerShell 脚本中文乱码**

`wiki_init.ps1` 必须以 **UTF-8 with BOM** 保存（PowerShell 5.1 默认按系统 ANSI 解析无 BOM 的脚本）。本仓库已正确处理，但如果你手动编辑过它，注意保存时保留 BOM。

### 通用

**Git Bash 里 `python $HOME` 找不到文件**

这是 Windows 上**最容易踩的坑**。Git Bash 的 `$HOME` 是 POSIX 格式，Windows 原生 Python 不认：

```
Git Bash 认为:   $HOME = /c/Users/xxx
Windows Python:  /c/Users/xxx/.workbuddy/...  →  C:\c\Users\xxx\...  ❌
```

报错长这样：

```
can't open file 'C:\c\Users\xxx\.workbuddy\skills\skill-evolution\scripts\wiki_init.py'
```

三种解法，任选：

| 解法 | 命令 |
|------|------|
| Git Bash 里改用 `.sh` | `bash "解压目录/scripts/wiki_init.sh"` |
| 用 Windows 格式的变量 | `python "$USERPROFILE\解压目录\scripts\wiki_init.py"` |
| 让 `cygpath` 转换 | `python "$(cygpath -w "解压目录")/scripts/wiki_init.py"` |

**最省事的解法：用项目内脚本的相对路径**（安装器生成的项目就是如此）：

```bash
python .wiki/scripts/wiki_init.py
```

这条命令在 Git Bash、PowerShell、CMD、WSL 下都成立，因为它不含任何 `$HOME` 变量。

同理，给 Python 脚本**传路径参数**时也要先转换成 Windows 格式：

```bash
python .wiki/scripts/wiki_init.py "$(pwd -W)"
```

不转换的话，脚本会打印"初始化完成"，但 `find .wiki` 找不到目录——文件被写到了 `C:\tmp\...` 这种不存在的地方。

**hook 完全没输出**

按顺序排查：

1. 项目里没有 `.wiki/` 目录 → 提醒脚本只在 `.wiki/` 存在时输出，这是设计行为（避免干扰无关项目）。先初始化。
2. 没重启会话 → Claude Code 在会话启动时读配置。
3. 配置里的脚本路径不存在 → 见上文「Claude Code hook 装了没反应」。

**手动测试提醒脚本**

在项目根目录直接执行（推荐，无需任何环境变量）：

```bash
python .wiki/scripts/wiki_remind.py     # 项目级安装
```

若要用全局安装的那个（用户级安装场景），才需要指定项目目录：

```bash
# Unix
CLAUDE_PROJECT_DIR=/path/to/project bash ~/.claude/scripts/skill-evolution/wiki_remind.sh

# Windows (PowerShell)
$env:CLAUDE_PROJECT_DIR="C:\path\to\project"
python "$env:USERPROFILE\.claude\scripts\skill-evolution\wiki_remind.py"
```

真实 Claude Code 下该变量由平台自动注入，无需手动设置。

> **脚本如何定位项目**：三级 fallback —— `CLAUDE_PROJECT_DIR` → 当前工作目录 → **脚本自身位置**。
> 第三级（脚本自身位置上溯两级）**只在项目级安装下有效**：此时脚本位于
> `<项目>/.wiki/scripts/`，上溯两级正是项目根。某些沙箱化 shell 在启动子进程时会 `cd` 回工作区，
> 导致前两级同时失效，这一级用来兜底。
>
> **用户级安装时第三级不成立**——`~/.claude/scripts/skill-evolution/` 上溯两级是 `~/.claude`，
> 不含 `.wiki`。所以用户级依赖前两级：真实 Claude Code 会注入 `CLAUDE_PROJECT_DIR`，
> 正常情况没问题；但用 cron 之类手动拉起时必须自己设好该变量或在项目目录内执行。

---

## 常见问题

**会拖慢 Agent 吗？**

记录轨迹每次只写几行文本，开销可忽略。复盘是离线周期性做的，不影响日常任务。

**多久复盘一次？**

论文建议：每 3–5 个任务做一次 Wiki 维护，每 5–10 个任务做一次技能提案。个人开发不必严格——攒几天做一次就行，别让它变成负担。

**能跨项目共享经验吗？**

可以。`.wiki/` 是项目级的，但你可以手动把通用性强的 `skills/*.md` 复制到其他项目的 `.wiki/skills/` 下。项目特有的坑（比如某个省平台接口字段）留在本项目。

**第一步该做什么？**

**别等自动流程跑起来。** 直接把你已经知道的坑手动写进 `.wiki/knowledge/patterns.md`——你现在就能想到几个（某个库的怪癖、某个 API 的参数陷阱、某次 debug 了很久的根因）。立刻可用，比等这套闭环跑起来现实得多。

**和 CLAUDE.md / 项目记忆有什么区别？**

CLAUDE.md 是**静态的、人工维护的**项目说明。本 skill 多两样东西：一是**执行轨迹**（记录了"当时到底发生了什么"，而不只是结论），二是**失败提案的历史**（记录"试过什么、为什么不行"）。这第二点是论文的关键发现——失败经验同样有价值。

**必须跑完整闭环吗？**

不用。只用 ② 记录 + ③ 复盘就能获得大部分价值。④ 技能提案与 ⑤ 门控是进阶用法，需要你投入判断力。

**哪里能看到"别这样做"？**

见上文[「别这样做（反模式清单）」](#别这样做反模式清单)（8 条高频）或完整版 `references/anti-patterns.md`（17 条 + 报错速查表）。

**脚本报错了、我看不懂那条英文提示？**

先查 `references/anti-patterns.md` 的「报错速查表」，三列对照：你看到的报错 / 人话 / 怎么修。
另外 `install.py` 与 `wiki_init.py` 对**瞬时故障会自己重试**（Windows 上杀软扫描、文件被占用这类），
不需要你手动再跑一遍；永久性问题会直接给出中文的「哪里出错 + 怎么办」，不会甩一段 traceback。

---

## 文件清单

```
skill-evolution/
├── SKILL.md                      # Agent 读的主文档（七步闭环 + 四问评分卡 + 角色隔离）
├── README.md                     # 本文件
├── scripts/
│   ├── install.py                # 统一安装器（推荐入口，项目自包含）
│   ├── wiki_init.py              # 初始化 .wiki/（全平台，推荐）
│   ├── wiki_init.sh              # 初始化 .wiki/（Unix）
│   ├── wiki_init.ps1             # 初始化 .wiki/（Windows PowerShell）
│   ├── wiki_remind.py            # Stop hook 提醒（全平台，Windows 必用）
│   ├── wiki_remind.sh            # Stop hook 提醒（Unix）
│   └── selfcheck.py              # 包体自检（只读；改动后 / 分发前跑一次）
├── references/
│   ├── rsi-framework.md          # RSI 判据：概念 / 度量 / L1–L5 / 四大追问（闭环 ①⑦）
│   ├── design-playbook.md        # 自改进设计：五步工作流（供闭环 ④ 产出方案）
│   ├── workflow.md               # 经验沉淀：三角色职责 + 四问评分卡权威源（闭环 ②③④⑤⑥）
│   ├── anti-patterns.md          # 反模式清单（"别这样做"）+ 报错速查表
│   ├── platforms.md              # 跨平台适配指南
│   ├── automation.md             # 自动化方案 + prompt 模板（含全链联合编排）
│   ├── templates.md              # Markdown 模板集合
│   ├── CLAUDE.template.md        # Claude Code 配置模板
│   └── AGENTS.template.md        # Codex 配置模板
└── assets/hooks/
    ├── claude-code-settings.json          # hook 手动配置模板（Unix）
    └── claude-code-settings.windows.json  # hook 手动配置模板（Windows）
```

`SKILL.md` 给 Agent 读，`README.md` 给人读。

### 包体自检（改动后 / 分发前跑一次）

```bash
python scripts/selfcheck.py                        # 只检本包
python scripts/selfcheck.py --copy <副本目录>       # 顺带比对副本哈希，可重复指定
```

**只读**，不修改任何文件；发现异常时退出码为 1，可直接接进 CI 或提交前检查。

覆盖 10 类问题：身份契约（`name` 不可改）、必备文件齐全、圈码编号一致性（闭环语义，
排除了 `L4 门控验证` 这类同形误报）、Markdown 代码围栏闭合、README 内部锚点与目录树一致性、
换行符统一、打包垃圾（`__pycache__` / `.pyc`）、本机路径泄漏、跨副本哈希一致。

> 前 5 类都是**改文档时容易悄悄改坏**的地方（编号体系、围栏截断、树与磁盘脱节），
> 人工评审很难逐条盯住——这正是它存在的理由。

> **关于 `install_claude_hook.py`**：该脚本在 `wikiskill` + `rsi-knowledge` +
> `rsi-self-improvement-designer` 三合一为 `skill-evolution` 时**已被移除**（它硬编码了
> WorkBuddy 私有目录，属于已知会静默失效的历史实现）。统一安装器 `install.py` 覆盖其全部功能。

---

## 论文与来源

本 skill 是两篇文献的合成体：WikiSkill 解决"经验怎么存、怎么迭代"，RSI 路线图回答"改进算不算真的、能自动到哪"。

### 1. WikiSkill —— 经验沉淀的工程实现

Google Research（通讯作者 Tu Vu 兼挂 Virginia Tech），2026-08-27。*WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution*. Tang et al. [arXiv:2608.27454](https://arxiv.org/abs/2608.27454)

- **关键数据**：Gemini-3.5-Flash 在 LiveMath / SealQA / SpreadSheet / OfficeQA / ALFWorld 五个基准上的**平均分 49.5 → 68.1**；**Qwen-3.5-9B + WikiSkill（47.4）超过无技能的 Qwen-3.6-27B（39.4）**——小模型 + 技能可越级。
- **核心设计**：三层结构 Raw → Wiki → Skill；知识层只增不减，技能层可回滚。
- **思想来源**：Andrej Karpathy 提出的 "LLM Wiki" 概念。
- **落到本仓库**：`.wiki/` 目录规范与 `scripts/`（即本 skill）。

### 2. RSI 路线图 —— 自改进的理论判据

Theseus Labs 等，35 位作者，v1 2026-09-10 / v2 2026-09-15。*The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement*。
[arXiv:2609.11873](https://arxiv.org/abs/2609.11873) · [项目主页](https://theseus-labs-rsi.github.io/)

汇总 **393 组模型-基准观测**，覆盖 **10 大能力领域**（2023-09 至 2026-09）。三个可直接用于工程设计的产出：

> **机构与规模更正**：论文公开页仅标注通讯作者（Xuanhe Zhou），**未列全部作者机构**；正文第 5 节以**工业案例**形式讨论 Theseus、Lark、小红书、Humanlaya、面壁智能（ModelBest）、腾讯混元等。"联合上海交大 / 清华 / 字节跳动"与"72 家公司/团队"两处说法均无出处，已移除。

| 产出 | 内容 | 在本仓库的落点 |
|------|------|---------------|
| **HCI** 能力余量闭合指数 | `HCI = 100 × (共识得分 − 基准前沿) ÷ (100 − 基准前沿)`（基准前沿 = 该基准**进入数据集首年的第 90 百分位模型分**；共识得分按数据源加权，以抑制自报偏差），衡量"离满分的差距被填上了多少" | 判断某个能力域值不值得投自改进：缺口越大，红利越高 |
| **L1–L5 自主权分级** | 按"改进循环中人类退出多少、AI 接管多少"分级 | `references/design-playbook.md` 的成熟度定位 |
| **四大评估追问** | 可衡量 / 可保持 / 可迁移 / **可回滚** | 本 README 中 L4 门控验证的理论依据 |

论文里最具操作性的数字：**软件工程 HCI 仅 52.6、工具调用 Agent 仅 39.9**，缺口远大于标准化考试类能力（前沿数学 86.4、研究生级科学 85.8）。另有一处值得注意——**网络安全 Agent 已达 91.9**，与工具调用 Agent 相差 52.0 点，同属 Agent 类别却差距悬殊。论文据此指出：软件工程与工具型 Agent 之所以成为各家发力第一站，是因为**反馈廉价、验证明确、部署链路短**，RSI 循环最容易闭合。

> 这也正是本仓库的设计取向——不追求把模型改强，而是先让"记录 → 复盘 → 验证 → 回滚"这条链，在一个反馈廉价的领域里真正闭合。

### 两篇文献的关系

| | WikiSkill | RSI 路线图 |
|---|---|---|
| 回答的问题 | **怎么存**住经验（工程） | **该存什么、怎么判断改进是真的**（判据） |
| 时间尺度 | 跨会话、跨任务 | 跨代际的能力递归 |
| 关键机制 | 三层知识库 + 门控验证 | L1–L5 分级 + 四大追问 |
| 落到本 skill | `.wiki/` + `scripts/`（经验沉淀模块） | `references/rsi-framework.md` + `references/design-playbook.md` |

一个管**沉淀**，一个管**判据**——缺了后者，沉淀下来的可能只是一堆"看起来有用"的技能。
