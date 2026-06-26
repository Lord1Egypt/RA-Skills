# subagent-archive

> Safe archive & cleanup of sub-agent sessions — cross-platform, OpenClaw 6.1 ready.
> 安全归档/清理子智能体会话 — 跨平台、OpenClaw 6.1 适配。

[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%20%7C%207%2B-blueviolet.svg)](#-platform-compatibility)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-6.1%2B-orange.svg)](https://openclaw.io)

---

## ✨ 核心特性 / Core Features

- 🛡️ **三层防御**（v3.0）：物理文件成组清理 + sessions.json 反向匹配 + dashboard 父会话 status 分流
- 🔌 **OpenClaw 6.1 集成**（v3.1+）：自动调官方 `--fix-missing` / `--active-key` / `--fix-dm-scope`
- 🌍 **跨平台**（v3.2）：Windows / macOS / Linux + PowerShell 5.1 / 7+
- 🗂️ **workspace 自动检测**（v3.2）：扫描 `~/.openclaw/workspace-*` 找带 `MEMORY.md` 的目录；多 workspace 时引导显式指定
- 🛑 **零匹配守卫**（v3.1+）：第 6 步零匹配时**绝不**重写 `sessions.json`（防 sessions.json 被清空，参考 ERR-20260606-001）
- 📝 **追加写入铁律**（v1.1+）：第 3/4 步必须 `Add-Content`，禁止 `Set-Content`
- 🎯 **三种模式**：`dry-run`（默认）/ `enforce`（真删）/ `soft`（重命名为 `.deleted.<timestamp>`）
- 🔒 **主会话永久保护**：`:main` / `:cron:*` 活跃 / `status≠done` dashboard 永远不动

## 🚀 快速开始 / Quick Start（30 秒上手）

### 前置要求 / Prerequisites

- **OpenClaw** 5.26+（推荐 6.1+ 以获 `--fix-missing` / `--active-key` / `--fix-dm-scope` 能力）
- **PowerShell 5.1+** on Windows 或 **PowerShell 7+** on macOS/Linux
- 已初始化的 OpenClaw 工作区（`~/.openclaw/agents/<your-agent>/sessions/` 存在）

### 5 行代码

```powershell
# 1. 克隆 / 解压到任意目录
cd <skill-folder>/scripts

# 2. dry-run 试跑（默认安全模式）
pwsh ./archive-sessions.ps1 -Agent myagent

# 3. （可选）显式指定 workspace（多 workspace 时必须）
pwsh ./archive-sessions.ps1 -Agent myagent -WorkspaceDir "$HOME/.openclaw/workspace-myworkspace"

# 4. 软删除模式（推荐第一次正式跑用这个）
pwsh ./archive-sessions.ps1 -Agent myagent -Soft

# 5. 硬删除模式（确认无问题后）
pwsh ./archive-sessions.ps1 -Agent myagent -Enforce
```

> ⚠️ **不要在主会话（`agent:YOURAGENT:main`）里跑 `-Enforce` 模式**——会清掉你自己。

## 📋 参数完整说明 / Parameters

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-Agent` | string | **必填** | 目标智能体 ID（如 `myagent`、`jarvis`） |
| `-DryRun` | switch | `$true` | 默认 dry-run（仅预演，不真删） |
| `-Enforce` | switch | `$false` | 硬删除模式（真删文件 + 重写 sessions.json） |
| `-Soft` | switch | `$false` | 软删除模式（重命名为 `.deleted.<timestamp>`） |
| `-Json` | switch | `$false` | JSON 格式输出（适合脚本调用） |
| `-FixMissing` | switch | `$true` | 6.1+ 调官方 `--fix-missing`（默认开启） |
| `-NoFixMissing` | switch | `$false` | 降级到 v3.0 行为（6.1 不可用时用这个） |
| `-FixDmScope` | switch | `$false` | 6.1+ 调官方 `--fix-dm-scope` |
| `-ActiveKey` | string[] | `@()` | 6.1+ 透传 `--active-key`（保护指定 key 不被清）。例：`-ActiveKey "agent:myagent:main","agent:myagent:cron:abc123"` |
| `-WorkspaceDir` | string | `""` | **v3.2 新增**：workspace 目录。默认自动检测；多 workspace 时必填 |

**优先级**：
- `-Enforce` > `-Soft` > `-DryRun`（同时指定时 enforce 赢）
- `-NoFixMissing` > `-FixMissing`（同时指定时 NoFixMissing 赢，降到 v3.0 行为）

**退出码**：
- `0` = 无操作完成（dry-run 或没有可清理项）
- `1` = 实际清理完成（enforce 且有清理动作）
- `2` = 错误（参数错、路径不存在等）

## 🌍 平台兼容矩阵 / Platform Compatibility

| 平台 | PowerShell | 状态 | 备注 |
|------|-----------|------|------|
| Windows | PowerShell 5.1 (Desktop) | ✅ **已测试** | 默认 `powershell.exe` |
| Windows | PowerShell 7+ (Core) | ✅ 代码兼容 | 测试待办（`pwsh.exe`） |
| macOS | PowerShell 7+ (Core) | ✅ 代码兼容 | 测试待办（`pwsh`） |
| Linux | PowerShell 7+ (Core) | ✅ 代码兼容 | 测试待办（`pwsh`） |

**路径检测逻辑**：
- PS 5.1 on Windows：`$env:USERPROFILE` → `~/.openclaw`
- PS 7+ on Win/macOS/Linux：`$HOME` → `~/.openclaw`

> 在 PS 5.1 下，`$IsWindows` 变量不存在，所以脚本优先检查 `$env:OS -eq "Windows_NT"` 以兼容。

## 🔌 OpenClaw 6.1 适配说明

| 功能 | 5.26 | 6.1+ | v3.2 处理 |
|------|------|------|-----------|
| 会话 lock 释放修复 | ❌ | ✅ | 6.1+ 自动获益 |
| `--fix-missing` 反向匹配 | ❌ | ✅ | v3.2 优先调官方 + 自写补盲区 |
| `--active-key` 保护 | ❌ | ✅ | v3.2 透传 |
| `--fix-dm-scope` 修 DM | ✅ | ✅ | v3.2 透传 |

**核心设计原则**：v3.0+ 永远保留 dashboard 父会话归档、物理文件清理、软删除、归档到 memory/ 等 6.1 没提供的功能。v3.1+ 的升级是"集成"而不是"替换"。

## 🛡️ 安全设计 / Security Design

### 1. 主会话保护 / Main Session Protection

`:main` 永远不动。即使 `-Enforce` 模式也不会删。

### 2. 零匹配守卫 / Zero-Match Guard（参考 ERR-20260606-001）

第 6 步清理 `sessions.json` 时：
- **enforce 模式 + 有 stale key**：备份 → 删除 → 重写
- **enforce 模式 + 零 stale key**：**不重写**（防止 sessions.json 被清空成 `{}`）
- **dry-run 模式**：仅打印不执行

> 这个守卫修复了 v3.0 的一个 bug——无 stale key 时也调 `Set-Content`，把 sessions.json 写成 `{}`（448KB → 2 字节），差点清空数据。

### 3. 追加写入铁律 / Append-Write Iron Rule

第 3/4 步必须 `Add-Content`，禁止 `Set-Content`。同日多次执行 v3.2 时，归档日志持续累积，不会丢失历史。

### 4. dashboard 分流 / Dashboard Status Splitting

- `status=done` 父会话 + 空壳子会话 + 派生子会话 → 归档
- `status=running` / `status=idle` 父会话 → 永远保护

### 5. 物理文件成组清理 / Physical File Group Cleanup

按 `sessionId.*` 通配符成组删除，覆盖 6 种变体：
- `.jsonl`
- `.trajectory.jsonl`
- `.trajectory-path.json`
- `.jsonl.checkpoint.<id>.jsonl`
- `.jsonl.reset.<ts>`
- `.jsonl.deleted.<ts>`

### 6. 软删除 / Soft Delete

`-Soft` 模式把文件重命名为 `<basename>.deleted.<timestamp><ext>`，可恢复。

## 📜 版本演进 / Version Evolution

| 版本 | 日期 | 关键变化 | 状态 |
|------|------|---------|------|
| **v3.2.0** | 2026-06-06 | 跨平台 + workspace 可配置 + 通用化重构 | ✅ **ClawHub 候选** |
| v3.1.0 | 2026-06-06 | OpenClaw 6.1 集成 + 零匹配守卫 | ✅ 已通过 6 项验证 |
| v3.0.0 | 2026-06-06 | 三层防御（物理成组 + 反向匹配 + dashboard 分流 + 软删除）| ✅ 稳定 |
| v1.1.0 | 2026-04-26 | 基础 6 步 + 追加写入铁律 | ✅ 历史 |
| v1.0.0 | 2026-04-? | 初版 | ✅ 历史 |

详细变更见 [CHANGELOG.md](CHANGELOG.md)。

## 💡 使用示例 / Usage Examples

### 例 1：标准 dry-run（首次使用必跑）

```powershell
pwsh ./archive-sessions.ps1 -Agent myagent
```

输出：
```
[INFO] subagent-archive v3.2 执行（通用化重构版，OpenClaw 6.1 适配）
[INFO] 智能体: myagent
[INFO] 模式: dry-run
[INFO] workspace（自动检测）: /home/user/.openclaw/workspace-myworkspace
...
[ACT] [dry-run] 将删除孤儿: abc123.jsonl (147 bytes)
[ACT] [dry-run] 将删除孤儿: def456.jsonl (1842286 bytes)
...
```

### 例 2：多 workspace 时显式指定

```powershell
pwsh ./archive-sessions.ps1 -Agent myagent -WorkspaceDir "C:\Users\me\.openclaw\workspace-work"
```

如果检测到多个 workspace 但你没指定：
```
[ERR] 检测到多个 workspace:
[ERR]   - C:\Users\me\.openclaw\workspace-work
[ERR]   - C:\Users\me\.openclaw\workspace-personal
[ERR] 请用 -WorkspaceDir <path> 显式指定其中一个。
```

### 例 3：6.1 集成 + 保护指定 key

```powershell
pwsh ./archive-sessions.ps1 `
    -Agent myagent `
    -FixMissing `
    -ActiveKey "agent:myagent:main","agent:myagent:dashboard:critical-id"
```

### 例 4：JSON 输出（适合脚本/CI 调用）

```powershell
$result = pwsh ./archive-sessions.ps1 -Agent myagent -Json | ConvertFrom-Json
Write-Host "Mode: $($result.mode)"
Write-Host "Files cleaned: $($result.filesCleaned)"
Write-Host "Freed MB: $($result.freedMB)"
```

### 例 5：6.1 不可用时降级

```powershell
pwsh ./archive-sessions.ps1 -Agent myagent -NoFixMissing
```

降级到 v3.0 行为（只用自写逻辑，不用官方 `--fix-missing`）。

### 例 6：跨平台路径示例

```powershell
# Windows + PowerShell 5.1
powershell -File .\archive-sessions.ps1 -Agent myagent

# Windows + PowerShell 7+
pwsh -File .\archive-sessions.ps1 -Agent myagent

# macOS / Linux + PowerShell 7+
pwsh ./archive-sessions.ps1 -Agent myagent
```

## 🧪 测试 / Testing

### 语法解析测试

```powershell
# PowerShell 5.1
powershell -Command "[System.Management.Automation.Language.Parser]::ParseFile('./archive-sessions.ps1', [ref]$null, [ref]$errors)"

# PowerShell 7+
pwsh -Command "[System.Management.Automation.Language.Parser]::ParseFile('./archive-sessions.ps1', [ref]$null, [ref]$errors)"
```

零错误 = 通过。

### 跨平台 dry-run 测试

详见 [`tests/`](tests/) 目录：
- `tests/test-syntax.ps1` — PS 5.1 语法解析
- `tests/test-pwsh7-syntax.ps1` — pwsh 7 语法解析
- `tests/test-dry-run.ps1` — 跨平台 dry-run

## 🙏 致谢 / Acknowledgments

### 原开发者 / Original Developers

**v3.0 → v3.1 原始开发**（私有资产，由丞相团队开发并通过 6 项验证）：
- 丞相（chengxiang）— 首席架构师，v3.0 三层防御设计
- 工部侍郎（gongbu_shilang）— v3.1 OpenClaw 6.1 集成实施

v3.2 在 v3.1 基础上做通用化重构，未修改任何核心安全逻辑。

### 贡献者 / Contributors

- 丞相团队（v3.0 - v3.1）
- OpenClaw Community（v3.2 通用化重构）

### 引用 / References

- OpenClaw 6.1 release notes — `--fix-missing` / `--active-key` / `--fix-dm-scope` 官方文档
- ERR-20260606-001 — 零匹配守卫的 bug 修复记录（v3.0 → v3.1）
- Keep a Changelog 1.1.0 — 本 CHANGELOG.md 格式参考

## 📞 反馈 / Feedback

- 🐛 **Bug 报告**：GitHub Issues
- 💬 **讨论**：ClawHub 评论区
- 📧 **Email**：openclaw-community@example.com（占位，待社区指定）
- 📖 **文档**：[SKILL.md](SKILL.md) / [CHANGELOG.md](CHANGELOG.md)

## 📄 许可证 / License

本项目采用 [MIT License](LICENSE) — Copyright © 2026 OpenClaw Community

---

**⚠️ 警告 / Warning**

> 使用本技能前请先在 dry-run 模式验证。一旦跑 `-Enforce`，sessions.json 中的 stale key 会被清理（带备份），磁盘文件会**真删**（`-Enforce`）或**真改名**（`-Soft`）。建议第一次正式跑用 `-Soft` 模式，确认无问题后再 `-Enforce`。
