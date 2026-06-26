# Changelog

All notable changes to subagent-archive will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.2.0] - 2026-06-06 — 通用化重构（ClawHub 发布准备）

### Added
- **跨平台路径检测**：自动识别 `~/.openclaw` 根目录
  - Windows + PowerShell 5.1/7+：`$env:USERPROFILE`
  - macOS/Linux + PowerShell 7+：`$HOME`
- **新增 `-WorkspaceDir` 参数**：指定 workspace 目录
  - 显式指定 > 自动检测
  - 自动检测规则：扫描 `~/.openclaw/workspace-*` 找带 `MEMORY.md` 的目录
  - 唯一命中自动选中
  - 多重命中报错引导用户用 `-WorkspaceDir` 显式指定
  - 零命中报错引导用户用 `-WorkspaceDir` 显式指定
- **平台兼容矩阵**：在 SKILL.md 顶部明确列出 4 种平台组合的支持状态
- **README.md**：完整使用说明、平台兼容矩阵、致谢区

### Changed
- **中性化作者署名**：脚本注释、SKILL.md frontmatter 改为 "OpenClaw Community"
  - 原开发者 credit（v3.0 - v3.1 原始开发团队）保留在脚本注释头和 README 致谢区
- **示例 agent**：SKILL.md 和脚本注释里的示例 agent 统一改为 `-Agent myagent`
- **memory 目录路径**：硬编码单一 workspace 路径改为 `Join-Path $WorkspaceDir "memory"`
- **README.md 致谢区**：写明原开发者贡献

### Removed
- **硬编码路径**：所有平台特定、用户名特定、workspace 特定的硬编码路径全部清理
- **私有 agent 名称残留**：所有 SKILL.md 示例和脚本注释统一改为中性示例 `-Agent myagent`

### Fixed
- 通用化 v3.1 的所有平台特定代码，使其在 macOS/Linux 用户的 OpenClaw 工作区也能运行
- 多 workspace 检测报错信息更友好，列出所有候选 + 显式指定示例

### Security
- v3.1 的全部安全特性完整保留：
  - 主会话保护（`:main`）
  - cron 任务保护（`:cron:*` 活跃任务）
  - dashboard 父会话 status 分流（`status=done` 才归档）
  - sessions.json 反向匹配清理
  - 物理文件成组清理（覆盖 6 种变体）
  - 追加写入铁律（第 3/4 步必须 `Add-Content`）
  - 软删除模式（`.deleted.<timestamp>` 重命名）
  - 零匹配守卫（参考 ERR-20260606-001）

## [3.1.0] - 2026-06-06 — OpenClaw 6.1 适配

### Added
- **OpenClaw 6.1 集成**：第 1 步自动调官方 `--fix-missing`
- **新增 `-FixMissing` 参数**（默认开启）：6.1+ 调官方反向匹配
- **新增 `-NoFixMissing` 开关**：6.1 不可用时降级到 v3.0 行为
- **新增 `-FixDmScope` 参数**：6.1+ 透传 `--fix-dm-scope`
- **新增 `-ActiveKey` 参数**：6.1+ 透传 `--active-key`（保护指定 key 不被清）
- **第 6 步双保险**：官方 `--fix-missing` + 自写 status 缺失检测
- **零匹配守卫**：第 6 步零匹配时**不重写** sessions.json（修复 ERR-20260606-001）

### Changed
- **OpenClaw 6.1 兼容矩阵**：SKILL.md 顶部新增对比表
- **v3.0 全部功能保留**：dashboard 父会话归档、软删除、归档到 memory/ 全部保留

## [3.0.0] - 2026-06-06 — 三层防御

### Added
- **物理文件成组清理**（第 5 步）：按 `sessionId.*` 通配符成组删除，覆盖 6 种变体
  - `.jsonl`
  - `.trajectory.jsonl`
  - `.trajectory-path.json`
  - `.jsonl.checkpoint.<id>.jsonl`
  - `.jsonl.reset.<ts>`
  - `.jsonl.deleted.<ts>`
- **sessions.json 反向匹配**（第 6 步）：只清理 `sessionFile` 已不存在的 key，不再用 `:main$` 粗暴过滤
- **dashboard 父会话 status 分流**：`status=done` 才归档；`status=running` 永远保护
- **保护 key 扩展**：`:main`、`:cron:*`（活跃）、`:dashboard:*`（非 done）
- **三种模式**：`dry-run`（默认）/ `enforce`（真删）/ `soft`（重命名为 `.deleted.<timestamp>`）
- **dashboard 父会话额外归档**：归档到 `memory/dashboard-archives/` 独立目录
- **检测"status 缺失"异常**：v3.0 漏的盲区，v3.1+ 检测但不自动清

### Security
- **三层防御体系**：
  - 物理文件清理：成组 + 通配符
  - sessions.json 清理：反向匹配
  - dashboard 父会话：status 分流
  - 软删除：可恢复

## [1.1.0] - 2026-04-26 — 基础流程

### Added
- 基础 6 步流程：识别 → 安全分析 → 归档 → 记录 → 物理清理 → 索引清理
- 追加写入铁律（第 3/4 步必须 `Add-Content`，禁止 `Set-Content`）
- 主会话保护（`:main`）
- cron 任务保护（`:cron:*`）

## [1.0.0] - 2026-04-?? — 初版

### Added
- 子会话归档基本流程
- 物理文件删除（仅 `.jsonl`）
- sessions.json 过滤（用 `:main$` 粗暴过滤，v3.0 替换为反向匹配）

---

## 版本对比速查

| 版本 | 关键能力 | 状态 |
|------|---------|------|
| v3.2.0 | 跨平台 + workspace 可配置 + 6.1 适配 + dashboard 分流 + 软删除 | ✅ ClawHub 候选 |
| v3.1.0 | 6.1 适配 + dashboard 分流 + 软删除 | ✅ 已通过 6 项验证 |
| v3.0.0 | dashboard 分流 + 软删除 + 反向匹配 | ✅ 私有资产 |
| v1.1.0 | 基础 6 步 + 追加写入 | ✅ 历史 |
| v1.0.0 | 初版 | ✅ 历史 |

[Unreleased]: https://github.com/openclaw-community/subagent-archive/compare/v3.2.0...HEAD
[3.2.0]: https://github.com/openclaw-community/subagent-archive/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/openclaw-community/subagent-archive/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/openclaw-community/subagent-archive/compare/v1.1.0...v3.0.0
[1.1.0]: https://github.com/openclaw-community/subagent-archive/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/openclaw-community/subagent-archive/tags/v1.0.0
