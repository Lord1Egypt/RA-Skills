---
name: quark-lazy-cli
description: >-
  基于 QAS（夸克网盘自动转存项目）的懒人追剧、追番 SKILL，也内置了一个 CLI 工具。即使 QAS
  的剧集订阅失效，它也可以重新搜索资源、探查多级资源目录，并在多个最新候选资源中按用户偏好（如更高清晰度）转存新剧集和缺失剧集。可以交给本地
  OpenClaw、Hermes Agent 或其他Claude Code, Codex Agent 使用，用来设置定时任务、定时汇报，并在订阅失败时辅助修复。有 Python
  运行环境的进阶用户，也可以把它当作命令行工具使用。
---

# quark-lazy-cli

`quark-lazy-cli` 是给 Agent 使用的夸克网盘追剧、追番订阅维护 Skill；`qslazy` 是它内置的命令行工具。它依赖 QAS 后端，用来查看订阅、检查缺集、搜索候选资源，并在用户授权后转存新剧集或补全缺失剧集。

`quark-lazy-cli` 不是 QAS Web 端的替代。它的核心功能聚焦在更新、修复更新失败、精准指定源资源文件转存，让 Agent 帮用户少操心地追新、补漏和维护订阅。

## 四种运行模式

`LAZY_CLI_ADVISOR` 是网盘资源搜索后的决策机制，用来决定候选资源怎么选，不是聊天模式。

- `code`：用代码规则自动决策。适合后台任务、资源发布规范的剧集、资源目录有“更新至n集”；速度快，无需交互，不消耗 LLM Token。
- `llm`：后台任务中引入大模型做资源选择。适合多版本编号冲突等复杂资源；可配合 `--add-prompt` 改AI大模型定制判断规则。例如：让大模型帮你判断是动漫还是真人版的剧集、你订阅任务是剧集的中文名称，告诉大模型剧集的英文名称等。
- `agent`：由当前 Agent 在和用户交互过程中判断候选资源。适合复杂场景的临时更新，或者在Openclaw Heateat机制里，维护和修复复杂订阅更新的场景使用。记得让Agent更新时，要求看订阅剧集.md文档中，你对剧集转存的要求。
- `human`：用户人工选择。适合用户想亲自确认资源的场景。

详细用法读取：`references/顾问模式.md`。

## 安装

安装分两步：Skill 文档告诉 Agent 怎么用；`qslazy` CLI 是真正执行任务的命令。两个都要装。

```bash
# skills.sh / 通用 Agent
npx skills add jesustoachild/quark-lazy-cli

# OpenClaw / ClawHub
openclaw skills install quark-lazy-cli

# qslazy CLI
pipx install git+https://github.com/jesustoachild/quark-lazy-cli.git
```

## 配置环境变量

### 1. 确认 `.env` 位置

`.env` 固定放在 Skill 目录根部，不要放到全局目录：

```text
<skills-dir>/quark-lazy-cli/.env
```

### 2. 创建 `.env`

如果安装后的 Skill 目录里带有 env 样板文件，直接复制成 `.env`：

```bash
cd <skills-dir>/quark-lazy-cli

cp ./.env.local.example .env
```

如果安装后的目录没有 env 样板文件，就读取 `references/环境变量.md`，由 Agent 根据里面的完整模板创建并编辑 `.env`。

### 3. 写入基础配置

把下面内容写入 `<skills-dir>/quark-lazy-cli/.env`，并把占位值改成用户自己的 QAS 信息：

```env
# QAS 后端地址，例如：http://192.168.1.10:15305
QAS_HOST=http://your-qas-host:port

# QAS API Token，可在 QAS Web 管理页面查看
QAS_API_TOKEN=your-qas-api-token

# 网盘资源搜索选择的顾问模式：human / code / llm / agent
LAZY_CLI_ADVISOR=code

# 运行时目录，建议使用绝对路径，放在 Skill 目录下，便于 Agent 清理和迁移
LAZY_CLI_LOG_DIR=<skills-dir>/quark-lazy-cli/runtime/logs
LAZY_CLI_REPORT_DIR=<skills-dir>/quark-lazy-cli/runtime/report
LAZY_CLI_AGENT_MSG_DIR=<skills-dir>/quark-lazy-cli/runtime/message
```

如果想在任意目录下运行，建议加入 `--env`：

```bash
qslazy update new 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env
```

如果临时覆盖 `.env` 的配置，可以不更改.env，命令行示例：

```bash
LAZY_CLI_ADVISOR=llm qslazy update new 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env
```

环境变量优先顺序从高到低：

```text
命令行临时环境变量 > 系统环境变量 > --env 指定的 .env 文件 > 默认值
```

因此 `LAZY_CLI_ADVISOR=llm qslazy ... --env ...` 只会临时覆盖本次命令，不会修改 `.env` 文件。

## 常用命令

### 1. 验证安装

```bash
qslazy --help
qslazy task --help
qslazy update --help
```

### 2. 查看订阅

```bash
qslazy task list --env <skills-dir>/quark-lazy-cli/.env
```

### 3. 查看订阅任务状态

```bash
qslazy task status 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env
```

### 4. 追更新集（必须先获得用户授权，禁止自行测试）

禁止把更新命令当作安装测试或功能测试。只有用户明确要求更新、追新或修复订阅时，才可以执行。

```bash
LAZY_CLI_ADVISOR=code qslazy update new 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env
```

### 5. 补全缺集 + 追新（必须先获得用户授权，禁止自行测试）

禁止在用户只要求“看看”“检查”“测试 skill”时执行。先用 `task status` 汇报状态，再询问用户是否更新。

```bash
LAZY_CLI_ADVISOR=code qslazy update all 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env
```

## 进阶能力索引

### 了解用户订阅情况和资源发布规律

读取文件：`references/订阅时间估算.md`

用于：
- 批量分析 `task status` 输出
- 推算订阅更新时间
- 维护订阅时间表

### 配置完整 OpenClaw 定时任务

读取文件：`references/OpenClaw定时任务.md`

用于：
- 创建定时更新任务
- 设置通知参数
- 维护定时任务

### 让 Agent 做每日订阅汇报

读取文件：`references/每日汇报.md`

用于：
- 首次使用先把 `./scripts/daily_report.sample.sh` 复制为 `./scripts/daily_report.local.sh`
- 定时运行 `./scripts/daily_report.local.sh`
- 汇报每日订阅状态
- 发现新资源时先询问用户是否更新

### 处理复杂资源选择

读取文件：`references/顾问模式.md`

用于：
- 理解 `code / llm / agent / human` 顾问模式
- 使用 `--add-prompt`
- 处理 Agent JSON 决策

## 铁律

- 永远先观察再行动；用户只说“看看/检查/分析/测试 skill”时，只运行 `task list/status`。
- 未获用户授权，不执行 `update new/all`，不新增、修改或删除定时任务。
- 默认只根据 stdout 汇报；除非排错或用户要求，不读 log/报告文件，避免浪费 Token。
- 不暴露 QAS API Token，不把真实 token 写进示例、回复、日志或定时任务。
- 不擅自删除、改名或移动用户网盘文件。
- 不直接修改 `scripts/*.sample.sh`。这些是升级可覆盖的样板脚本；用户定制应复制为 `scripts/*.local.sh`，并运行 `.local.sh`。
- 不擅自研究、审查或修改 qslazy 源码。只有用户明确要求“看代码”“修 bug”“做开发/审查”时，才进入代码层；普通订阅维护只使用 CLI 和 reference 文档，避免浪费 Token。
- 资源命名混乱时，不用 `code` 硬选，改用 `llm` 或 `agent`，并读取 `references/顾问模式.md`。
