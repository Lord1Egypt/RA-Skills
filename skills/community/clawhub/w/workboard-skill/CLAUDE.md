# CLAUDE.md — WorkboardSkill 项目上下文

> 给 Claude Code 看的项目说明。每次开新 session 先读这个文件。

---

## 这个项目是什么

WorkboardSkill 是一个 OpenClaw **skill** 项目，提供 `workboard` skill：教 agent / 操作员如何使用 OpenClaw 内置的 Workboard 看板插件。

主要能力：
- 用 `openclaw workboard` CLI 列出 / 创建 / 查看 / 分派卡片
- 用 `/workboard` 斜杠命令在支持渠道上操作看板
- 解释卡片状态机、会话生命周期同步、诊断规则
- 收录子智能体 worker 的 `workboard_*` 工具协议作为参考资料

⚠️ Workboard 插件本身是 OpenClaw **内置**的，本仓库只提供 *如何使用它* 的 skill 文档，**不含插件代码**。安装 / 启用插件走 `openclaw plugins enable workboard`，不走本仓库。

---

## 发布地址

| 目标 | 地址 |
|------|------|
| GitHub | `jeanbai0818-cloud/workboard-skill` |
| ClawHub | `jeanbai0818-cloud/workboard-skill` |

> GitHub 仓库与 ClawHub 包同名，均为 `jeanbai0818-cloud/workboard-skill`；ClawHub publisher 用 `jeanbai0818-cloud`（不用 `tal`）。发布后用 `git remote -v` 和 `clawhub inspect workboard-skill` 核实。

**每次发版都要双推**，缺一不可。发布顺序固定：先推 GitHub，再发布 ClawHub。

> ℹ️ 仓库已 `git init`（分支 `main`），remote `origin` → `https://github.com/jeanbai0818-cloud/workboard-skill.git`。

---

## 版本号规范

格式：`YYYY.M.D`，补丁版本用 `YYYY.M.D-1`、`-2`、`-3`……

**skill 版本号通过 `clawhub publish --version` 传入，发版时与本节规则保持一致。**

> skill 发布**不需要** `package.json` / `openclaw.plugin.json` / `_meta.json`：版本走 `clawhub publish --version`，slug 走 `--slug`，publisher 走 `--owner`，均由命令行传入。

> ⚠️ **skill 路径实测限制**：`clawhub publish` 同版本号不可覆盖（报 `Version ... already exists`），且 `YYYY.M.D-N` 被当作 semver 预发布、优先级低于 `YYYY.M.D`，**不会**提升为 `latest`（`latest` 仍指向 `YYYY.M.D`）。`clawhub delete <slug>` 只是软删（slug 保留约 30 天、版本记录仍在），删后重发同版本号照样报 `already exists`——**无法**靠软删重发让当天修正进入 `latest`。结论：skill 的同日修正**只能**等下一个日期版本（如次日 `YYYY.M.D+1`）自然带上；`-N` 仅作可安装的预发布，不进 `latest`。

### 版本号生成规则（发版前必须执行）

```bash
# 查当前日期
date '+%Y.%-m.%-d'
```

1. **当前版本 < 今天日期**：直接用今天日期，例如今天 2026.7.8 → 版本改为 `2026.7.8`
2. **当前版本 = 今天日期**（已发过一版）：追加 `-1`，即 `2026.7.8-1`；再发则 `-2`……
3. **当前版本 > 今天日期**（版本号超前了）：改为今天日期追加后缀，从 `-1` 起

> 核心原则：版本号中的日期不得早于也不得超过推送当天的实际日期。

---

## 发版完整流程

```bash
# 1. 校验 frontmatter（name / description）
head -4 SKILL.md

# 2. 校验引用链接是否都能对上
grep -oE '\]\(\./references/[^)]+\)' SKILL.md
ls references/

# 3. 提交推送 GitHub
git add SKILL.md references/ CLAUDE.md
git commit -m "描述 (版本号)"
git push

# 4. 发布 ClawHub（skill 用顶层 clawhub publish，不是 clawhub package publish）
clawhub publish . \
  --slug workboard-skill \
  --owner jeanbai0818-cloud \
  --version "$(date '+%Y.%-m.%-d')" \
  --changelog "本次变更说明"
```

> skill 发布用顶层 `clawhub publish`（不是 yach-im 那条 `clawhub package publish --family code-plugin`，那是给插件用的）。skill 不带 `--source-repo` / `--source-commit`，GitHub 仓库与 ClawHub skill 仅内容同步，不在发布命令里 formally 关联。

---

## 关键标识符（不要搞混）

| 字段 | 值 |
|------|----|
| skill 名（`SKILL.md` frontmatter `name`） | `workboard` |
| skill 描述的内置插件 | `workboard`（OpenClaw 内置，**非本仓库**） |
| 启用内置插件命令 | `openclaw plugins enable workboard` |
| GitHub repo | `jeanbai0818-cloud/workboard-skill` |
| ClawHub publisher | `jeanbai0818-cloud` |
| ClawHub 包名 | `jeanbai0818-cloud/workboard-skill` |

> skill 名 `workboard` 与内置插件名 `workboard` **同名是有意的**：skill 就是教你怎么用同名插件。两者不是一回事——skill 是文档，插件是运行时。改动本仓库不会影响内置插件行为。

---

## Skill 内容一览

主文件 [SKILL.md](SKILL.md) 章节：

| 章节 | 说明 |
|------|------|
| 定位 | skill 是操作员视角；CLI / 仪表盘 / 斜杠命令同源 SQLite；agent 工具收在参考资料 |
| 前置 | `openclaw plugins enable workboard` + `gateway restart` + 运行状态检查 |
| CLI 用法 | `list` / `create` / `show` / `dispatch` 四命令及全部 flag |
| 斜杠命令 | `/workboard list/show/create/dispatch` 及权限要求 |
| 卡片字段 | status / priority / labels / agentId / 关联引用 / execution |
| 默认流程 | 操作员从看卡到分派的默认路径 |
| 调度语义 | 分派循环 7 步、worker 选择规则、启动失败处理、仅数据回退 |
| 诊断 | 6 类内置诊断检查 |
| 权限与存储 | `operator.read` / `operator.write` 范围、SQLite 存储、`.28` 迁移 |
| 故障排查 | 7 行「现象 → 处理」矩阵 |
| 何时读取参考资料 | 指向两个 reference 文件 |
| 使用原则 | 操作 skill 的约束清单 |

参考资料 `references/`：

| 文件 | 说明 |
|------|------|
| [card-lifecycle.md](references/card-lifecycle.md) | 状态机、会话生命周期同步表、诊断详情、最近事件清单、从卡片启动工作的引擎选择 |
| [agent-tools.md](references/agent-tools.md) | `workboard_*` 工具表、认领令牌脱敏语义、worker 上下文、链接 / 分解 / 通知游标规则 |

---

## 目录结构

```text
SKILL.md                      主文件（frontmatter: name / description + 操作员行动指南）
references/
  card-lifecycle.md           状态机 / 会话同步 / 诊断 / 事件清单 / 引擎选择
  agent-tools.md              workboard_* 工具表 / 认领令牌 / worker 上下文 / 通知游标
CLAUDE.md                     本文件
```

> skill 结构参照同机 `~/.claude/skills/grafana-inspection/`（根目录 `SKILL.md` + `references/` + `scripts/`）。本 skill 是纯文档型，**没有 `scripts/`**——Workboard 通过 CLI / 仪表盘操作，不需要包脚本。

---

## 常见操作速查

**本地安装验证（把 skill 装到本机 Claude Code）：**
```bash
# 软链，改完即时生效（推荐）
ln -s "$PWD" ~/.claude/skills/workboard
# 或直接拷贝
cp -r . ~/.claude/skills/workboard
```

**改 SKILL.md 后校验 frontmatter 与引用：**
```bash
head -4 SKILL.md
grep -oE '\]\(\./references/[^)]+\)' SKILL.md && ls references/
```

**确认本机 openclaw + 插件就绪（实跑 skill 里的命令前）：**
```bash
command -v openclaw
openclaw plugins inspect workboard --runtime --json
openclaw gateway status --deep
```

**核对版本号（发布前）：**
```bash
date '+%Y.%-m.%-d'
# skill 版本通过 clawhub publish --version 传入，无文件需 grep
```

**查看 / 安装已发布 skill：**
```bash
clawhub inspect workboard-skill
clawhub install workboard-skill
```

---

## 维护原则

- skill 只描述 *怎么用* 内置 Workboard 插件，**不要**把插件行为 / 工具协议抄成会过时的实现细节；以[官方文档](https://docs.openclaw.ai/zh-CN/plugins/workboard)为准，文档变了就更新本 skill
- 操作员路径写进 `SKILL.md`，深细节（工具表、状态机、事件清单）写进 `references/`，按需读
- Claude Code 通常作为操作员助手用 CLI 操作看板；`workboard_*` 智能体工具是给子智能体 worker 的，**不要**在 `SKILL.md` 里要求 Claude Code 直接调用
- 发布地址与命令已确认：GitHub 与 ClawHub 同名 `jeanbai0818-cloud/workboard-skill`，skill 用 `clawhub publish --slug workboard-skill --owner jeanbai0818-cloud --version ...` 发布，无需 manifest
