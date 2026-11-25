---
name: workbuddy-migration
slug: workbuddy-migration
displayName: WorkBuddy 一键迁移（换电脑）
version: 1.0.1
summary: 把本机全部 WorkBuddy 数据（技能/长期记忆/会话工作区/项目仓库/会话历史）打包成"拷到新电脑双击一下即可完整恢复"的迁移包。自动探测账号、工作区、项目磁盘，无需任何手工配置；新电脑无需预装 git/7z。支持完整包/仅配置/仅项目/仅数据四种范围与 DryRun 试运行。
license: MIT
description: WorkBuddy 换电脑/迁移/备份/恢复场景的总入口。当用户说"换电脑了""迁移 WorkBuddy""把 WorkBuddy 搬到新电脑""备份我的技能和会话""新电脑怎么恢复""migration""迁移包"等任何涉及把本机 WorkBuddy 全部内容搬到另一台电脑的请求时使用。覆盖打包（旧电脑）与还原（新电脑）两个方向，含自动探测、一键生成、一键恢复、断点重跑与覆盖度对账。
category: office-efficiency
subCategories: [office-automation]
platforms: [windows]
agent_created: true
---

# WorkBuddy 一键迁移（换电脑）

把一台电脑上的全部 WorkBuddy 内容（用户级技能、长期记忆、会话工作区、git 项目、会话历史、修改备份）打包成一个文件夹；拷到新电脑后**双击一个文件**即完整还原。账号 UUID、工作区父目录、项目所在磁盘全部自动探测，换任何人的电脑都能用。

## 何时使用

- 用户要换电脑 / 迁移 WorkBuddy / 把数据和设置搬到新电脑
- 用户要整体备份 WorkBuddy 本地内容（技能、记忆、会话、项目）
- 用户在新电脑上要恢复此前打包的迁移包
- 用户问"迁移包怎么用 / 恢复脚本怎么跑 / 哪些东西能自动恢复"

## 核心概念：四层分流

| 层 | 内容 | 迁移方式 |
|---|---|---|
| 云端 | 资料库、云记忆、Automations、连接器授权 | 新电脑登录同一账号自动恢复（连接器需重新扫码授权一次） |
| 配置层 | skills×N、personal 长期记忆、会话工作区、.claude/opencode、mcp/models/settings.json、.gitconfig、workbuddy.db | `WorkBuddy-Migration.zip`，Windows 自带 tar 解压，**免 7z**。SSH 私钥不在自动收集范围，按使用说明手工拷贝 |
| 项目层 | git 仓库 bundle（含全部历史）+ 未提交文件 + 非 git 数据目录 | `project-data\`，内置免安装 git，**新电脑无 git 也能还原** |
| 数据层 | 会话历史、文件修改备份快照、blob、plans、scripts、备份、连接器、UI 索引、账号快照 | `project-data\wb-extra\`，manifest 驱动 |

## 执行方式

所有脚本位于本 skill 的 `scripts/` 目录。用 skill 基准目录拼路径（下称 `<SKILL_DIR>`）。

### 方向一：在旧电脑打包（主流程）

1. **预检**：确认用户已完全退出 WorkBuddy（运行中打包会缺最新数据）。若在运行，提示退出，或用户明确要求时加 `-Force`。
2. **DryRun 试运行**（不拷贝任何数据，只出清单）：
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File "<SKILL_DIR>/scripts/Build-WBMigration.ps1" -DryRun
   ```
3. 把 DryRun 输出整理成表格给用户确认：账号、工作区、项目根目录、各层体积、git 仓库清单、被跳过的大目录。
4. 用户确认后实跑（缺省输出到 `桌面\WorkBuddy-迁移包`）：
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File "<SKILL_DIR>/scripts/Build-WBMigration.ps1"
   ```
   或让用户直接双击 `<SKILL_DIR>/scripts/一键制作迁移包.cmd`（带菜单：完整/仅配置/仅项目/仅数据/试运行）。
  > 注：`.cmd` 不在 SkillHub 服务端白名单内（只收 `.py`/`.js`/`.md` 等文本），从市场安装的用户没有这个文件。
  > 需要双击入口时，把下面内容存为 `scripts\一键制作迁移包.cmd`（UTF-8 带 BOM 或 GB18030 均可，首行已有 chcp 65001）：
  >
  > ```bat
  > @echo off
  > chcp 65001 >nul
  > title WorkBuddy 一键制作迁移包
  > cd /d %~dp0
  > :menu
  > cls
  > echo   [1] 完整迁移包  [2] 仅配置层  [3] 仅项目层  [4] 仅数据层  [5] 试运行  [0] 退出
  > set /p c=请选择 [1]:
  > if "%c%"=="" set c=1
  > if "%c%"=="0" exit /b
  > if "%c%"=="1" set "SCOPE=full"
  > if "%c%"=="2" set "SCOPE=config"
  > if "%c%"=="3" set "SCOPE=projects"
  > if "%c%"=="4" set "SCOPE=data"
  > if "%c%"=="5" set "SCOPE=full" & set "DRY=-DryRun"
  > if "%SCOPE%"=="" goto menu
  > powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-WBMigration.ps1" -Scope %SCOPE% %DRY%
  > pause
  > ```
5. 验收：`WorkBuddy-Migration.zip` 存在且非空、`一键恢复.cmd` 已生成、`project-data\manifest.json` 仓库数与 DryRun 一致。
6. 交付话术：整个文件夹拷移动硬盘 → 新电脑装 WorkBuddy 登录同账号 → 双击 `一键恢复.cmd`。

### 方向二：在新电脑还原

- **首选**：双击迁移包里的 `一键恢复.cmd`（自动依次执行 配置层→项目层→数据层，只需确认一次）。
- **分步**（单独重跑某层）：`1-oneclick-restore.cmd`（配置）→ `2-restore-projects.cmd`（项目，跑完自动接数据层）→ `3-restore-wbdata.cmd`（数据层）。
- 还原脚本可重复执行：已完成的项目跳过/合并，失败项重跑即可。
- 用户在新电脑要求 agent 代跑时，直接调用上述 cmd/ps1 即可，无需重新生成。

## 参数速查（Build-WBMigration.ps1）

| 参数 | 作用 |
|---|---|
| `-Scope full/config/projects/data` | 打包范围，缺省 full |
| `-DryRun` | 只扫描出清单 + 生成还原脚本到 `_stage\`，不拷贝 |
| `-ProjectRoots a,b` | 显式指定项目根目录（缺省自动发现数据盘 + 用户目录常见项目位置） |
| `-OutputRoot <path>` | 输出目录（缺省桌面\WorkBuddy-迁移包；禁止放在 .workbuddy 内） |
| `-Force` | WorkBuddy 运行中也继续 |
| `-NoDb` | 不打包 workbuddy.db |
| `-NoPortableGit` | 不内置免安装 git |
| `-SkipWbExtra name` | 跳过数据层指定项（如 workspace-sessions） |
| `-ExtraExcludeDirs name` | 附加项目目录黑名单（支持通配符） |

## 关键规则（必须遵守）

1. **打包前必须退出 WorkBuddy**，否则 db/暂存数据不完整。用户坚持时用 `-Force` 并告知风险。
2. **输出目录不能在 `.workbuddy` 或任何项目根目录内**（会把迁移包自己打进去）；脚本有硬校验，换了 `-OutputRoot` 也不要绕过。
3. 含 API 密钥等凭证数据：只走移动硬盘直拷，**禁传公有网盘/微信/邮件**；SSH 私钥默认不进包，需按使用说明的 icacls 加固步骤手工拷贝。
4. 不要向用户承诺"连接器授权也能迁移"——DPAPI 加密的本地凭据跨机无效，必须重新授权。
5. 用户只要逻辑不要拷贝时（如首次咨询），只跑 `-DryRun`，不产生数据拷贝。
6. 迁移包体积以 GB 计时，先看 DryRun 总量再决定是否分范围打包或加 `-SkipWbExtra`。

## 参考文件

- `references/migration-layout.md` —— WorkBuddy 数据落盘全景图（哪类数据在哪、哪层自动恢复）
- `references/troubleshooting.md` —— 还原失败排查（git/robocopy/tar/编码/账号不一致/大目录跳过）
