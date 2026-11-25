---
name: workspace-root-selection
description: "Decide whether a directory can serve as an OpenClaw workspace root (external dir or Windows drive) and whether to migrate: official docs, filesystem measurement, and migration verification."
---

# 工作区根目录：选型、实测、迁移

用于：主人问「某目录能不能设成工作区」「Windows 盘能不能当工作区」「一个 agent 能不能挂多个目录」「要不要把工作区搬出去」。
产出：**可执行结论（分区 or 迁移）+ 实测数据 + 迁移步骤**。

（通用平台取证走 `openclaw-docs-grounding`；工作区内部文件清理走 `workspace-declutter`；播种 / WORKSPACE_VANISHED / 去注册走 `openclaw-workspace-registration`。）

## 前置事实（先读，勿重踩）

- **一个 agent 只有一个工作区**。官方原话：*"Each agent uses one resolved workspace; keeping extra directories does not merge their persona or memory files into the active workspace."*（`docs/concepts/agent-workspace.md` § Extra workspace folders）⇒ 要多根目录 → 多 agent 或绝对路径，不是给一个 agent 挂多个根。
- **工作区是默认 cwd，不是硬沙箱**：绝对路径本就能读写外部目录；真要隔离才开 `agents.defaults.sandbox`。
- **路径优先级**：`agents.entries.<id>.workspace` > `agents.defaults.workspace` > `OPENCLAW_WORKSPACE_DIR` > profile/state 推导（`docs/concepts/multi-agent.md` Paths 表）。**改 `agents.defaults.workspace` 只改未 pin 条目的基准目录，不会把已 pin 的 main 迁走**。
- **会话与 auth 不随工作区迁移**：在 `agentDir`（`~/.openclaw/agents/<id>/agent/`，含 `openclaw-agent.sqlite`），要留会话得单独拷。
- **软链接有边界**：沙箱 seed 只接受工作区内的常规文件，指向工作区外的 symlink/hardlink **被忽略**（agent-workspace.md Note）⇒「工作区放软链接指向外部盘」在 sandbox 模式下失效。
- **跨文件系统桥接不是普通目录**：Windows 盘在 WSL 里是 9p/drvfs（v9fs），小文件 I/O、大小写语义、权限位三项都与 ext4 不同 ⇒ 必须实测，不能凭「能访问」下结论。

## 步骤

1. **官方口径先定边界**
   读 `~/.nvm/versions/node/*/lib/node_modules/openclaw/docs/concepts/agent-workspace.md` 与同目录 `multi-agent.md`（用 `ls` 实读路径，别写死 node 版本号）。
   完成判据：结论里每条限制都附到文档路径；文档没写的显式标「无官方依据（推断）」。

2. **实读本机配置，别用记忆里的旧值**
   `grep -n "workspace" ~/.openclaw/openclaw.json`。
   完成判据：能报出「当前每个 agent 实际指向哪」。
   ⚠️ exec 审批层拒的是**命令形态**：链式 `&&`、管道、`2>/dev/null` 常被 `SYSTEM_RUN_DENIED`；拆成单条简单命令再跑（同一形态再拒一次才算走不通）。

3. **目标目录先做文件系统适配实测，再谈搬迁**
   `write` 落盘 → 单条 `bash scripts/probe-fs.sh <目标目录> [原生对照目录]` → 读输出。
   四项：挂载类型 / 300 个小文件写入耗时 / 大小写是否敏感 / chmod 是否生效（附 SQLite 可用性）。
   判定线：**写入慢一个数量级以上 ⇒ 工作区不放这里**（工作区是 `skills/` + `memory/` + `.git` 的小文件密集目录）；**大小写不敏感 ⇒ 警告 `memory/` 与 `Memory/` 互吞**；**chmod 无效 ⇒ git 需 `git config core.fileMode false`**。
   完成判据：四项都有输出 + 一句「放 / 不放」判定；探针只删自己建的临时目录。

4. **默认给「分区」而不是「搬迁」**
   工作区留原生盘；另一块盘放渲染图 / 素材 / 大文件，用绝对路径读写（工作区非沙箱，跨盘本就可达）。
   确要多根目录 → 多 agent：`openclaw agents add <id> --workspace <dir>`，或 `openclaw agents team create --workspace-root <dir>`。
   完成判据：主人读完能直接选「分区」或「迁移」，不用再问「到底行不行」。

5. **确要迁移：按官方顺序做并复验**
   停 Gateway → 改 `agents.entries.<id>.workspace`（**POSIX 路径**，`D:\...` 不认）→ `openclaw doctor --fix` 迁移旧 setup 状态 → 重启 → `openclaw agents list` 确认指向新路径 → 需要留会话才另拷 `agentDir`。
   完成判据：`agents list` 的 workspace 与目标路径一致；新工作区里 `AGENTS.md` / `SOUL.md` / `IDENTITY.md` 在位（`openclaw setup` 只补缺失、不覆盖已有）。
   （本 agent 不自行重启 Gateway：重启走 `openclaw` 工具或交主人。）

6. **交付口径**
   官方限制（附路径）/ 实测数据 / 结论（分区 or 迁移）/ 迁移步骤 / 未决项。
   ⚠️ 别把「工作区里能用绝对路径读写外部文件」说成「不用改配置就能把外部目录当工作区」。

## 边界

- 只管工作区**根目录**的选型与迁移；不改技能内容、不做审计。
- 改宿主配置（`openclaw.json`）属配置变更：备份 + JSON 校验 + 主人点头后再动。
- 迁移与否由主人拍板；只负责把数据和选项摆到位。

## 支撑文件

- `scripts/probe-fs.sh` —— 文件系统适配探针（挂载类型 / 小文件写入耗时 / 大小写 / chmod / SQLite），用法 `bash probe-fs.sh <目标目录> [对照目录]`。
