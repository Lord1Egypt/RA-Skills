---
name: windows-disk-care
description: 排查 Windows 本地磁盘为什么持续变小，比较 Codex 工作树、会话、分页文件、Docker 虚拟盘和开发产物的前后变化。支持按本机明确授权的范围预检与清理旧 Electron 开发包和 Cargo 编译缓存。
metadata: {"openclaw":{"os":["win32"],"requires":{"bins":["pwsh"]}}}
---

# Windows 磁盘维护

适用于 Windows 和 PowerShell 7.2 及以上。以下命令在技能目录中运行。测量只读文件元数据，结果写入当前用户的本地报告目录。首次安装没有清理目标。

## 查明是哪里在增长

运行 [Measure-Growth.ps1](scripts/Measure-Growth.ps1) 记录固定盘可用字节、Codex 会话和工作树、分页文件以及可发现的 Docker Desktop 虚拟盘。首次采样建立基线。在磁盘空间再次下降时用同一报告目录复测。用 `-Repository` 观察某个 Git 仓库各工作树的常见生成目录，用 `-WatchPath` 加入已核实的构建目录、制品路径或迁移过的虚拟盘。

```powershell
pwsh -NoProfile -File .\scripts\Measure-Growth.ps1
```

需要找首次就已占用大量空间的目录时，运行 [Measure-DiskUsage.ps1](scripts/Measure-DiskUsage.ps1)，通过 `-Roots` 指定要检查的盘或目录。标明两次测量的时间窗口、实际卷变化、目录增量和读取不完整的范围。父子目录及硬链接可能重复计量。新发现的路径单列，已知目录的增长量和现有总量分开列出。

将增长最大的路径与写入证据对应。例如，工作树依赖核对安装时间和锁文件，Cargo 目录核对编译命令的目标路径，分页文件核对启动时间和资源耗尽事件，Docker 对照宿主虚拟盘大小和引擎存储统计。只有目录变化时，把写入进程列为待确认。后续同任务重试先复用匹配的工作树、依赖和编译目标，交付时记录最终制品和可回收的暂存。

## 处理已确认可再生的文件

先按 [本机策略配置](references/policy.md) 取得当前安装者的授权，将范围写入技能目录外的本地策略。程序支持指定 Git 仓库注册工作树里的 Electron x64 开发包，以及显式登记的 Cargo 缓存。需要 Git for Windows，开发包启动引用检查还需要 ripgrep。

1. 运行 [Invoke-DiskCare.ps1](scripts/Invoke-DiskCare.ps1) 的预检，核对报告中每个 `eligible` 项的绝对路径、应用、保留版本、文件身份和启动引用。检查显示正在使用、含保留标记、Git 跟踪、链接、文件锁定或用途不明的项时，保留并记录原因。
2. 只有本机用户已授权当前范围且已审核本次预检时才执行。把预检输出的 `Report` 路径传给同一脚本的 `-Apply -ReviewedPreview`。预检有效期为 30 分钟，内容或策略变化后重新核对。
3. 报告清理前后各卷实际可用空间变化、确实删除的路径、跳过和部分失败的项目。并行写入会影响卷变化。保护源码、用户文件、凭据、数据库、Codex 会话、验收记录和使用中的程序。

```powershell
$policy = Join-Path $env:LOCALAPPDATA 'WindowsDiskCare\policy.json'
.\scripts\Invoke-DiskCare.ps1 -PolicyPath $policy
# 审核本次报告并确认范围后，将 $reviewedReport 设为该报告的绝对路径。
.\scripts\Invoke-DiskCare.ps1 -PolicyPath $policy -Apply -ReviewedPreview $reviewedReport
```

用户要求定时维护时，在其调度器中复用已有任务，使用其时间、时区和本地策略路径。每次重新采样、预检，并在长期授权内执行。报告保存在本机；只在实际清理、明显增长、失败或需要用户决定时通知。
