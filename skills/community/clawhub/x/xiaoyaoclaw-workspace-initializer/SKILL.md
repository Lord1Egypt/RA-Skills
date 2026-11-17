---
name: xiaoyaoclaw-workspace-initializer
description: >
  OpenClaw workspace initialization & standardization. Sets up a proper agent
  home: standard directory structure (projects/tasks/outputs/knowledge/scripts/
  memory/tmp) + WORKSPACE.md rules + multi-agent config safety (config.patch,
  never config.apply) + memory log. Use ONLY when the user explicitly asks to
  initialize or repair a workspace root that the user has named. Missing
  subdirectories or a missing WORKSPACE.md are NOT a trigger on their own —
  report them and wait for an explicit request. Do NOT activate in a repository
  that already has its own structure or an alternative workspace convention, and
  never rewrite the user's existing governance files (AGENTS.md / WORKSPACE.md /
  SOUL.md / USER.md) without showing the exact diff and getting explicit
  approval first. Writes are confined to the named workspace root; config
  changes use config.patch only, never config.apply.
  中文：OpenClaw 工作区初始化与规范维护，多 agent 配置安全。仅在用户明确要求
  初始化/修复**且明确指认了工作区根目录**时使用；目录缺失或 WORKSPACE.md 缺失
  本身不是触发理由——只如实报告，等用户明确下令再动手；已有项目结构或已存在其他
  工作区规范的仓库不触发；AGENTS.md / WORKSPACE.md / SOUL.md / USER.md 属用户
  资产，未经用户看到确切 diff 并明确同意，不擅自改写；写入范围限定在指认的工作区
  根目录内；配置改动只用 config.patch，任何情况下都不用 config.apply。
---

# OpenClaw Workspace Initializer（工作区初始化器）

> 📖 **完整文档（安装 / 快速上手三步 / 定制服务）：<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

初始化 OpenClaw agent 工作区：标准目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。
让每个 agent 都有一个「家」——不迷路、不丢记忆、不踩配置坑。

> 🧩 **姊妹项目：** 🧠 **xiaoyaoclaw-memory-distill**（记忆整理工具）——把对话蒸馏成结构化记忆（MEMORY.md + 每日日志），解决上下文溢出，缺失时自动首次建忆：<https://github.com/dtsola/xiaoyaoclaw-memory-distill>

## 激活边界（避免误触发 / 越权改动）

**进入工作流的唯一条件（两条都要同时满足）：**

1. 用户**明确要求**初始化 / 修复工作区（「初始化一下工作区」「补上缺的目录和规范」）；
2. 用户**明确指认了工作区根目录**（或确认当前目录就是工作区根目录）。

**目录缺失、`WORKSPACE.md` 缺失本身不构成进入理由。** 发现缺失时只如实报告缺什么，等用户明确下达初始化指令后再进入工作流——**不得**因为「本轮任务正好要在这个目录落文件」而自行进入。

**以下情况不要激活、不要改动任何东西：**

- 仓库里已经有自己的目录结构与规范（例如已有 `src/`、`docs/`、`apps/` 等工程约定）；
- 已存在其他工作区规范（别的 `WORKSPACE.md` / `.cursor/rules/` / 团队规范）——先问用户以哪套为准；
- 用户只是在提问、讨论、看代码，或没有要求结构化改造；
- 工作区已经合规（此时**什么都不做**，只回一句「已符合规范」，不产生任何写入）；
- 当前目录不是用户指认的工作区根目录。

**不可越界的三条：**

- **不覆盖已有文件**：只创建缺失项，已存在的目录/文件一律跳过。
- **用户资产只提议、不擅自改**：`AGENTS.md`、`WORKSPACE.md`、`SOUL.md`、`USER.md` 等治理与配置类文件，改前必须展示**确切 diff** 并取得用户明确同意。
- **不装常驻机制**：不建 cron、不起守护进程、不写启动脚本、不写跨会话状态文件；本技能只在用户批准的那一轮里做文件改动。

**作用域与配置写入的硬约束：**

- **只写用户指认的工作区根目录**：创建目录、写 `WORKSPACE.md`、写 `memory/` 日志一律限定在该根目录及其子目录内；根目录之外的任何路径一律不写、不删、不改。
- **配置写入只用 `config.patch`**：本技能**任何情况下都不使用** `config.apply`（全量替换会抹掉共享配置中其他 agent 的修改）；确需大范围变更时，逐字段 `config.patch`，并先展示 diff 等用户确认。

## 工作流

### Step 0: 先出差异清单，默认 dry-run（改动前必须过的闸门）

在任何写入之前，先给用户一份**差异清单**，并停下来等确认：

```text
检测结果（只读）
  缺失目录：memory/  tmp/
  缺失文件：WORKSPACE.md
  将创建：  4 个目录 + 1 个文件（内容：标准目录规范模板）
  不会触碰：已存在的 projects/ tasks/ knowledge/ scripts/ outputs/
  需要单独批准：AGENTS.md 的启动读取规则（会改变未来会话的启动行为）
```

用户确认后再进入 Step 2；用户没确认就**不改任何东西**。

### Step 1: 检测当前状态

检查工作区根目录是否存在以下内容：

**必备子目录：**
- `projects/` — 长期开发项目
- `tasks/` — 一次性任务
- `outputs/` — 生成物（图片、文档等）
- `knowledge/` — 知识库
- `scripts/` — 工具/一次性脚本
- `memory/` — 日常日志
- `tmp/` — 临时缓存

**必备规范文件：**
- `WORKSPACE.md` — 目录管理规则（持久化规范，重启后依然生效）

**系统目录（不要修改或删除）：**
- `.openclaw/`
- `agent/`
- `sessions/`
- `.clawhub/`

### Step 2: 创建缺失的目录结构（用户确认后执行）

逐项创建**缺失**目录（已存在的一律跳过，绝不删除/覆盖）：

```bash
mkdir -p projects tasks outputs/knowledge scripts memory tmp
```

`outputs/` 下按需创建 `images/` 和 `docs/` 子目录，不强制。

### Step 3: 写入 WORKSPACE.md（仅当不存在时）

如果根目录**没有** `WORKSPACE.md`：读取本 skill 的 `templates/WORKSPACE.md`，把**将要写入的完整内容**给用户过一遍（或展示 diff）再写入。
**如果已存在则不覆盖**——需要修改时按「用户资产」处理：先给 diff，得到明确同意再改。

## 文件放置约定（只管「产出放哪」，不覆盖技能指令）

**适用范围严格限定**：本节只决定**本工作区自己产出的文件放在哪里**，它**不是对其他技能的指令覆盖**。

**优先级（从高到低）：**

1. **用户当轮的明确要求** — 用户说放哪就放哪
2. **其他技能的安全规则、许可条款、既定流程** — 一律优先，本文件不得改写、不得要求技能绕过
3. **本文件（WORKSPACE.md）的目录规范** — 仅在「上面两条没规定产出位置」时生效

**做法：**

- 技能若自带输出路径约定（如 `~/Downloads/xxx/`），把它的**产出位置**映射到工作区内并**告知用户差异**（「技能原约定 X，按工作区规范存到 Y」）；映射只涉及存放位置，不涉及技能内容与流程。
- 若技能**必须**写在工作区之外（例如它自己的数据目录、系统约定位置），**以技能为准**，如实汇报，不硬拉进工作区。
- 遇到无法用「换个位置」解决的冲突（例如技能要求改工作区外的配置）→ **停下来问用户**，不做单方面决定。

**设计原则：** 本文件只管「文件放哪」，不管「技能怎么做」。自研技能不硬编码工作目录，输出位置默认由 WORKSPACE.md 决定。

### Step 4: 引导新智能体

完成目录创建和 WORKSPACE.md 写入后，明确告知当前智能体：

> **铁律 #1 — 反馈至上：** 无论任务成功还是失败，必须向用户报告结果。成功告知产出，失败告知原因和错误信息，由用户做下一步决策。智能体不得擅自决定下一步行动。
>
> **铁律 #2 — 遵守工作区规范：** 后续每次启动时，先读取根目录的 WORKSPACE.md，按照其中的目录结构和命名规范组织所有工作。根目录不应放置任何项目文件，只保留 *.md 配置文件。
>
> **铁律 #3 — 配置修改安全：** 改配置一律用 `config.patch`（部分合并，只动指定字段）；**禁止使用 `config.apply`**（全量替换：会用旧配置快照整份写回，抹掉其他 agent 的修改）。多 agent 共享同一份 openclaw.json，apply = 谁后写谁赢。

### Step 4.5: 把工作区规范接入 AGENTS.md（**默认只提议，需明确批准**）

⚠️ **为什么这一步要单独批准**：`AGENTS.md` 会被 agent 在**每次会话启动时读取**，改它等于改变未来的行为——属于「用户资产」，不是普通输出文件。因此：

- **默认不动手**：先给出**确切 diff**（新增哪几行、插在哪个章节），并明确提示「这会让未来每次会话启动都先读 WORKSPACE.md」，**得到用户明确同意后**才写入。
- 用户不同意 / 没回应 → **跳过**，在汇报里写「AGENTS.md 未改动（待你确认）」。
- 不追加与本次初始化无关的内容；不覆盖用户已有的启动规则，只做**最小必要新增**。

批准后要做的两项（若 `AGENTS.md` 不存在则跳过，或随工作区模板一并创建）：

**① 启动读取规则（必写）：** 确保 AGENTS.md 的「Session Startup」章节（若没有该章节则新建）的启动必读列表中包含：

> `Read WORKSPACE.md` — workspace directory rules

即：agent 每次会话启动时，先读取 `WORKSPACE.md`（目录规则），再开始干活。

**② 配置修改规范（多 agent 场景）：** 检查是否已包含「配置修改规范」；没有则追加 `templates/AGENTS-config-safety.md` 的内容。

⚠️ **写入方式：** 必须用 Python 3 或文件编辑工具写入（UTF-8）；**不要用 PowerShell 5.1 内联脚本写中文**（按 GBK 解析无 BOM 的 UTF-8 脚本，中文会乱码）。

### Step 5: 记录初始化日志（随同一轮批准一起做）

在本工作区自己的 `memory/YYYY-MM-DD.md` 追加一条初始化记录（只写 Memory 目录内，不写到别处；如果用户没批准本轮改动，就不写）：

> xiaoyaoclaw-workspace-initializer 技能已执行，标准目录结构和 WORKSPACE.md 已就位；AGENTS.md 已写入「Read WORKSPACE.md — workspace directory rules」启动规则及配置修改规范。

## 完整示例

### 首次进入空工作区

检测 → **出差异清单并等用户确认（Step 0 闸门）** → 创建缺失目录 → 写入 WORKSPACE.md → 自我引导（铁律 #1/#2/#3）→ **给出 AGENTS.md 的确切 diff，经用户批准后**才接入启动规则 → 记录日志

**产出：**
```
根目录/
├── projects/
├── tasks/
├── outputs/
│   ├── images/
│   └── docs/
├── knowledge/
├── scripts/
├── memory/
│   └── YYYY-MM-DD.md    ← 初始化日志
├── tmp/
├── WORKSPACE.md          ← 持久化规范文件
├── SOUL.md
├── USER.md
└── ...其他系统配置
```

### 重启后新智能体进入同一工作区

新智能体 → 检测 → 发现 WORKSPACE.md 和所有目录已存在 → **什么都不做**（跳过 Step 2-5）→ 回一句「工作区已符合规范」即可。

**重启时依赖 WORKSPACE.md（目录规范）和 AGENTS.md（配置修改规范）作为持久化规范来源**，而不是依赖 SKILL.md（技能可能不在新智能体的技能列表中）。

> 注：这两份规范都是**用户资产**——本技能提交的是「文本 + 建议」，是否落地由用户决定；本技能不安装常驻机制，也不在用户不知情时改动它们。
