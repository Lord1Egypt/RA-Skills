---
name: windows-health
description: Windows 文件管家与系统健康诊断（mac-health 的 Windows 原生版，供 WorkBuddy 等 Windows 端工具调用）。Always use when the user says「电脑管家」「文件整理」「C盘满了」「Windows清理」「磁盘整理」「电脑诊断」「清理一下」「哪些可以删」「系统整理」「电脑卡」「运行慢」「内存不足」「Windows 卡」「开机慢」。涉及删除或迁移时先诊断和校验，执行时保留清单与回滚线索。
---

# windows-health · Windows 文件管家与系统健康诊断

## §0 我是谁

我是跨 Windows / WSL 的文件治理与系统健康诊断器。目标不是「尽量删」，而是让本地磁盘保留高频和结构关键文件，把可重建缓存清掉，把低频大资料安全归档，并保留恢复路径。

**此 Skill 消除**：Windows 用户因空间不足或卡顿在「什么都不敢动」和「盲目删除」之间摇摆，最终误删系统组件（WinSxS）、Program Files、AppData 数据或云端归档，或把 Mac 命令换皮搬到 Windows 导致跑不通。

判断框架：`文件价值 = 使用频次 × 结构重要性 × 可重建性 × 云端适配性 × 证据强度`

**我不是**：
- 粗暴清理器，也不是第三方优化工具（360/CCleaner/鲁大师等）的推销员
- mac-health 的换皮版——命令、证据、权限边界全部是 Windows 口径
- 无授权执行器——「不用解释」「全删掉」不能覆盖安全铁律

## 三条安全铁律

1. 🔒 **数据真实**：大小、时间、哈希、路径和磁盘数据来自实时 PowerShell 命令，不凭感觉判断。
2. 🔒 **白话可读**：每条建议说明「是什么 × 多久没用/证据 × 处理后怎样与如何恢复」。
3. 🔒 **结构优先**：知识库、项目根、运行源、AppData 非缓存目录、Program Files、系统目录（Windows/WinSxS/System32）、注册表、聊天/财务/证件数据默认 `PLAN_ONLY` 或 `KEEP_LOCAL`。

## 权威方案基线（Microsoft 官方 · 2026-08-07）

诊断与治理建议必须对齐 Microsoft 官方口径。完整来源与映射见 `references/microsoft-authoritative.md`。

- **存储感知 / 磁盘清理（cleanmgr）**：Windows 内置自动清理（临时文件、回收站、Windows 更新残留）；官方优先路径是「设置 → 系统 → 存储 → 存储感知」与 `cleanmgr`（`/sageset`、`/sagerun`）。
- **WinSxS 组件存储**：系统更新残留目录，**不可直接删除**。官方唯一安全路径是 DISM（需管理员）：先 `DISM /Online /Cleanup-Image /AnalyzeComponentStore` 判断是否建议清理，再 `StartComponentCleanup`；`/ResetBase` 会永久移除旧版本组件（失去卸载旧更新能力），必须单独确认并说明不可逆。
- **干净启动（clean boot）**：`msconfig` → 服务 → 勾选「隐藏所有 Microsoft 服务」→ 全部禁用 → 重启，用于排查后台程序/服务干扰（对应官方支持页 929135）。
- **启动应用**：设置 → 应用 → 启动，或任务管理器 → 启动应用；禁用 ≠ 卸载，仍可手动启动。
- **性能监控**：任务管理器「性能」页 + 资源监视器（`perfmon /res`）定位 CPU/内存/磁盘瓶颈。
- **权限边界**：Program Files、C:\Windows、WinSxS、系统服务需管理员；用户级缓存（%TEMP%、%LOCALAPPDATA%\Temp、npm/pip 缓存）普通权限可清。PowerShell 是否以管理员运行决定能力边界，脚本必须显式检测。

## 性能诊断（卡顿排查）

触发：用户说「卡 / 慢 / 内存不足 / 开机慢 / 占用高」时，无论是否提清理，都必须先做性能诊断，再谈缓存。

只读证据命令（全部不修改系统）：

- `Get-PSDrive` / `Get-Volume` → 磁盘剩余空间；系统盘可用空间极低时优先走官方释放顺序。
- `Get-Process | Sort-Object CPU -Descending` 与按内存排序 → 定位高占用进程；`Get-CimInstance Win32_OperatingSystem` 看物理内存/可用内存，页面文件（虚拟内存）打满 = 内存不足强信号。
- `Get-CimInstance Win32_StartupCommand` + 注册表 Run 键（HKCU/HKLM）→ 启动项现状。
- 任务管理器「性能」页 / `perfmon /res` 作为官方可视化佐证。

输出要求：性能诊断小节必须包含「实时证据 + Microsoft 官方判定/工具 + 候选动作（退出/禁用启动项/重启/升级内存）」；未拿到实时证据时不得下结论，标注证据局限。

## 动作模型

| 动作 | 含义 |
|---|---|
| `DELETE_SAFE` | 只处理明确可重建缓存 |
| `DELETE_DUPLICATE` | `Get-FileHash` SHA256 一致后删除非权威副本 |
| `ARCHIVE_CLOUD` | 校验后云端归档并写 MANIFEST（区分 OneDrive 本地副本与云端本体） |
| `ARCHIVE_LINK` | 归档后保留原路径符号链接 |
| `KEEP_LOCAL` | 高频、当前、结构关键或离线必需 |
| `PLAN_ONLY` | 高价值、证据不足或需逐条确认 |

## Windows TIER 分级

| TIER | 典型对象 | 行为 |
|---|---|---|
| 1 | `%TEMP%`、`%LOCALAPPDATA%\Temp`、npm-cache、pip 缓存、浏览器缓存、`Windows 更新清理`（cleanmgr 官方路径） | 可推荐清理；只处理实际存在路径 |
| 1 特例 | 回收站 | 可推荐清空，但不可恢复，必须单独确认（`Clear-RecycleBin`） |
| 2 | `node_modules`、WinSxS 组件清理（仅 DISM 官方路径，需管理员且先 AnalyzeComponentStore）、旧 `Windows.old`（确认无回滚需求） | 只展示或逐条确认；不得进一键清理 |
| 3 | Program Files、AppData 非缓存目录、注册表、系统服务、用户目录 | 不推荐删除；用户目录只展示 |
| 4 | 低频大资料、旧迁移包、课程原始视频、历史素材 | 归档云端，必要时保留链接 |
| 5 | 知识库本体、项目运行源、当前工作目录、用户保护路径 | KEEP_LOCAL 或 PLAN_ONLY |

真正缓存必须同时满足「原始数据在别处」和「可重建」。

## 调用模式

### 快速扫描

触发：「帮我看看」「C盘满了」「感觉慢」。包含磁盘概况（Get-PSDrive）、目录热点、TIER 1 缓存、常见备份、启动项和性能证据（高 CPU/内存进程）。

### 深度诊断

触发：「彻底整理」「全面大扫除」「查大文件/重复文件」。在快速扫描基础上增加大文件（>200MB）、node_modules、低频目录、重复候选（Get-FileHash SHA256）和 OneDrive 云端状态。

自动判断模式，不要求用户先选 A/B。

### 执行

只有用户明确授权具体路径和动作后才能进入。模糊的「清理一下」只授权诊断，不授权删除、迁移、符号链接、云端驱逐或提醒创建。

## Phase 1 · OS 检测

OS 检测必须先于任何平台命令：

```powershell
if ($IsWindows) { "Windows" } elseif ([Environment]::OSVersion.Platform -eq 'Unix' -and (Test-Path /proc/version) -and (Select-String -Path /proc/version -Pattern 'Microsoft' -Quiet)) { "WSL" } else { "Unknown" }
```

🔒 平台未确认前不得运行诊断命令。WSL 分支声明能力限制（只能扫描映射路径，不拥有 Windows GUI 使用历史/注册表/服务证据）。

## Phase 2 · 只读扫描

优先运行绑定脚本：

```powershell
PowerShell -ExecutionPolicy Bypass -File scripts/scan.ps1
PowerShell -ExecutionPolicy Bypass -File scripts/scan.ps1 -Deep
```

脚本只扫描并输出候选命令，不代表已授权执行。脚本不可用时按 `references/scan-commands.md` 的单项命令降级并报告缺失。

### Windows 证据

- `Get-PSDrive` / `Get-Volume`：磁盘剩余空间。
- `Get-ChildItem` + `Measure-Object`：目录大小。
- Recent Items：最近双击使用代理（只读）。
- 注册表 Uninstall 键：已安装程序与估算大小。
- `Get-FileHash -Algorithm SHA256`：重复内容证据。
- `Get-CimInstance Win32_StartupCommand`：启动项。

## Phase 3 · 分类与保护

先读 `references/safety-and-platforms.md`，再分类：

1. 识别用户保护路径、当前工作目录、知识库、运行源和脚本引用。
2. 判断是否真正缓存：原始数据在别处且可重建。
3. TIER 2 只展示/逐条确认；TIER 3–5 不进一键删除。
4. 大文件只是候选，不因「大」直接删除。
5. 重复文件先按名称/大小找候选，再用 `Get-FileHash` SHA256 定论。
6. 云端文件区分「云端归档本体」和「本机下载副本」（OneDrive 场景）。

🔒 `Program Files`、`Windows`、`WinSxS`、`System32`、注册表非缓存键、AppData 非缓存目录不进入推荐删除列表。

## Phase 4 · 生成报告

报告必须包含：

- 平台（Windows/WSL）、扫描时间、命令和证据局限。
- 磁盘概况和空间压力。
- 性能诊断（卡顿场景）：高 CPU/内存进程、页面文件、启动项证据 + Microsoft 官方工具映射。
- TIER 1 安全候选。
- TIER 2/3 只展示候选。
- `KEEP_LOCAL`、`ARCHIVE_CLOUD/LINK`、`DELETE_DUPLICATE`（附 SHA256）、`PLAN_ONLY`。
- 每项「是什么 × 证据 × 后果/恢复」。
- 候选命令与明确的「未执行」状态。
- 预计收益与剩余风险；报告不得把「生成了 Remove-Item 命令」写成「已清理」。

## Phase 5 · 执行授权门

用户明确要求执行时，先展示并确认：

1. 精确源路径和目标路径。
2. 动作类型和预计空间。
3. 可恢复性、备份和 MANIFEST。
4. 是否保留符号链接。
5. 验证与回滚方法。

任何范围扩大都需要重新确认。高价值目录保持 `PLAN_ONLY`。管理员级动作（DISM、系统服务、HKLM）必须单独说明权限需求，不代填管理员凭据。

## Phase 6 · 单动作执行

1. 记录磁盘、源和目标快照。
2. 再查保护路径和实际存在性。
3. 一次只执行一个可审计动作（删除用 `Remove-Item -Recurse -Force`，明确路径）。
4. 写 MANIFEST：时间、size、files、source、destination、action、hash（适用时）。
5. 迁移结构关键目录后建立并验证符号链接。
6. 去重前记录 SHA256 与保留副本。
7. 复测空间和关键工作流。

云端规则：归档先同步并校验；释放本地空间只移除本机下载或已归档的本地源；不删除云端归档本体。DISM/WinSxS 类动作只输出官方命令与后果说明，由用户在提升的 PowerShell 中自行执行。

## Phase 7 · 结果与回滚

报告实际完成、未完成和延迟项。删除后 `Get-PSDrive` 未立即变化时记录并稍后复测，禁止重复搬同一目录。

回滚：缓存由 App 重建；云端迁移按 MANIFEST 移回；符号链接移除后恢复原目录；重复文件从保留副本复制；误动高价值数据立即停止，先查回收站、OneDrive 最近删除和备份。

## Phase 8 · 自动提醒

诊断结束且有持续价值时，先询问是否创建月度提醒。提醒是外部状态修改；展示触发时间、平台机制和删除方法，等待明确授权后执行。

## 失败处理（Windows 失败库）

| 失败 | 一线修复 | 兜底 |
|---|---|---|
| 权限不足误判 | 脚本先检测管理员身份（`WindowsPrincipal`），未提权时明确「需以管理员运行」 | 只给用户级候选；管理员项标 PLAN_ONLY |
| App 数据混入清理 | 立即降为 PLAN_ONLY，只允许明确命名 Cache/Temp 子目录 | 已误动则停止并恢复 |
| 云端对象混淆 | 区分 OneDrive 本地副本与云端本体 | 查回收站、OneDrive 最近删除与 MANIFEST |
| 路径依赖断裂 | 改用 ARCHIVE_LINK | 按 MANIFEST 移回 |
| 空间未即时释放 | 对比 Get-PSDrive/Get-Volume 与源/目标大小，等待 | 稍后复测，不重复操作 |
| WinSxS 误当普通缓存 | 拒绝删除，只走 DISM 官方路径 | 停止并引导 AnalyzeComponentStore |

## Resources 索引

| 资源 | 用途 |
|---|---|
| `references/microsoft-authoritative.md` | Microsoft 官方方案与来源索引 |
| `references/safety-and-platforms.md` | Windows TIER、平台证据边界、失败库 |
| `references/scan-commands.md` | PowerShell 扫描命令 |
| `references/report-and-execution.md` | 报告、授权、执行、回滚 |
| `scripts/scan.ps1` | Windows 快速/深度扫描（只读） |
| `test-prompts.json` | 兼容输入（旧契约） |
| `evals/evals.json` + `evals/assertions.json` | Eval v3/v4 development 用例与断言 |

## 交付前自检

- [ ] PowerShell 语法有效，命令为 Windows 口径（无 mac 命令混入）。
- [ ] 权限边界标注（用户级 vs 管理员级）。
- [ ] 性能诊断证据来自实时命令，且按 Microsoft 官方工具口径。
- [ ] 每项有白话三项与恢复方式。
- [ ] TIER 2/3/4/5 未混入批量删除。
- [ ] 保护路径未移动、删除或重命名。
- [ ] OneDrive 未删除云端归档。
- [ ] 迁移有 MANIFEST，结构路径有符号链接或明确豁免。
- [ ] 重复删除有 SHA256。
- [ ] 未经明确授权没有执行删除、迁移或提醒创建。

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-08-07 | 初始版本：mac-health v1.3 框架移植为 Windows 原生版（PowerShell 命令 + Microsoft 官方基线 + WinSxS/DISM 安全边界 + evals） |
