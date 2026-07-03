---
name: winskill
description: "Windows 服务器运维工具箱 - 磁盘分析、临时文件清理、IIS 站点管理、批量文件操作、服务状态监控、Windows Update 诊断、实时性能监控、安全审计、注册表启动项审计、磁盘健康检测、网络端口监控、事件日志诊断、已安装程序管理、用户会话监控、计划任务审计、文件共享审计、DNS网卡诊断、SSL证书过期检测、防火墙规则审计、服务崩溃恢复状态。只读分析+安全确认，绝不误删文件，完全免费离线运行。"
version: 1.6.0
---


# Winskill — Windows 服务器运维工具箱 v1.6.0

## 快速开始

**直接对 AI 说就行，不用记命令。**

| 你想做什么 | 直接对 AI 说 |
|-----------|-------------|
| 看磁盘空间 | `"帮我扫一下 D 盘大文件"` |
| 清理临时文件 | `"看看我电脑的临时文件"` |
| 检查 IIS | `"我的 IIS 站点还活着吗？"` |
| 检测重复文件 | `"帮我找下重复文件"` |
| 检查服务状态 | `"看下数据库和 IIS 服务有没有挂"` |
| Windows Update 状态 | `"Windows Update 正常吗？有积压补丁吗？"` |
| 服务器卡顿定位 | `"服务器变卡了，帮我看看是什么原因"` |
| 检查有没有被入侵 | `"帮我查一下有没有异常登录"` |
| 检查可疑启动项 | `"有没有可疑的自启动程序"` |
| 磁盘健康状态 | `"硬盘还健康吗？有没有坏道"` |
| 网络连接监控 | `"谁在连我的服务器"` |
| 系统日志哪里错了 | `"系统日志有没有最近的错误"` |
| 服务器装了什么程序 | `"看看系统安装了哪些软件"` |
| 谁在服务器上 | `"当前有谁登录了服务器"` |
| 检查计划任务 | `"有没有可疑的计划任务"` |
| 文件共享审计 | `"有哪些共享文件夹，权限安全吗"` |
| DNS / 网卡诊断 | `"DNS 解析正常吗"` |
| 搞不定了 | `"我遇到报错了，帮我看看"` |

> ⚠️ **AI 必须遵守**：凡涉及删除、停止服务、修改系统的操作，必须先展示操作清单，等用户明确说"确认执行"后才可执行。

---

## 安全声明

| 保护项 | 方式 |
|-------|------|
| 系统目录保护 | 绝不操作 `C:\Windows`、`C:\Program Files` 等 |
| 删除必须确认 | 先展示受影响文件，等用户说"确认清理"后才执行 |
| 回收站优先 | 删除用 `Shell.Application` 回收站 API |
| 只读诊断 | 所有分析命令不修改任何文件/服务/注册表 |
| 日志记录 | 操作记录到 `C:\AdminScripts\winskill.log` |
| 排除保护 | `pagefile.sys`、`hiberfil.sys` 等系统文件不可操作 |
| 注册表保护 | 注册表分析只读，任何修改需双重确认 |
| 日志读取保护 | 事件日志只读查看，不修改任何日志记录 |

---

## 功能模块

---

### 模块 1：磁盘空间分析

**用途**：扫描指定路径，找出占用空间的大文件和目录。

**常你说**：`"扫一下 C 盘大文件"` / `"D 盘哪个最占空间"`

<details>
<summary>📋 展开查看命令（按需展开）</summary>

```powershell
$scanPath = "C:\"   # ← 改成你要扫的盘符或目录

Get-ChildItem -Path $scanPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 100MB } |
    Sort-Object Length -Descending |
    Select-Object -First 50 @{N='路径';E={$_.FullName}},
        @{N='大小(GB)';E={[math]::Round($_.Length/1GB,2)}},
        @{N='最后修改';E={$_.LastWriteTime}}
```

</details>

**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access to the path 'xxx' is denied` | 权限不足 | 管理员身份运行 PowerShell |
| `Could not find a part of the path` | 目录不存在 | 确认路径 |

---

### 模块 2：大文件重复检测

**用途**：通过 MD5 哈希找出重复文件。

**常你说**：`"找找 D 盘有没有重复文件"`

<details>
<summary>📋 展开查看命令</summary>

```powershell
$scanPath = "D:\"   # ← 扫描目标目录
$minSize = 1MB      # ← 只检测大于 1MB 的文件

Get-ChildItem -Path $scanPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt $minSize } |
    ForEach-Object {
        $hash = (Get-FileHash $_.FullName -Algorithm MD5 -ErrorAction SilentlyContinue).Hash
        if ($hash) {
            [PSCustomObject]@{
                路径 = $_.FullName
                哈希 = $hash
                大小MB = [math]::Round($_.Length/1MB,2)
            }
        }
    } |
    Group-Object 哈希 |
    Where-Object { $_.Count -gt 1 } |
    ForEach-Object { $_.Group }
```

</details>

**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Exception getting file hash` | 文件正在使用 | 跳过 |
| `The specified path is not valid` | 路径格式不对 | 检查路径 |

---

### 模块 3：临时文件安全清理

**用途**：扫描安全可删的临时文件，先预览后确认再清理。

**常你说**：`"帮我清理临时文件"` / `"C 盘快满了帮清 temp"`

**安全清理路径**：

| 路径 | 说明 | 安全天数 |
|------|------|---------|
| `%TEMP%\*` | 用户临时文件 | >7 天 |
| `C:\Windows\Temp\*` | 系统临时文件 | >7 天 |
| `C:\Windows\SoftwareDistribution\Download\*` | Windows Update 下载缓存 | 任意 |
| `C:\Windows\Prefetch\*` | 程序预取 | >30 天 |
| `IIS Temporary Compressed Files\*` | IIS 压缩缓存 | >1 天 |

<details>
<summary>📋 展开查看命令 — 第一步：扫描预览（只读）</summary>

```powershell
$tempPath = $env:TEMP
$daysOld = 7
$cutoff = (Get-Date).AddDays(-$daysOld)

$tempFiles = Get-ChildItem -Path $tempPath -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $cutoff }

Write-Host "═══════════════════════════════════════════"
Write-Host "  📋 扫描结果: $tempPath"
Write-Host "  过期临时文件数: $($tempFiles.Count) 个"
Write-Host "═══════════════════════════════════════════"

$tempFiles | Sort-Object Length -Descending |
    Select-Object -First 20 |
    Select-Object @{N='文件路径';E={$_.FullName}},
        @{N='大小(KB)';E={[math]::Round($_.Length/1KB,1)}},
        @{N='最后修改';E={$_.LastWriteTime}} |
    Format-Table -AutoSize

$totalKB = ($tempFiles | Measure-Object -Property Length -Sum).Sum
Write-Host "  预计可释放空间: $([math]::Round($totalKB/1MB,2)) MB"
Write-Host "  ⚠️ 确认删除请说 '确认清理'"
```

</details>

<details>
<summary>📋 展开查看命令 — 第二步：回收站删除（需确认）</summary>

```powershell
# ⚠️ 仅当用户明确说「确认清理」后才执行！
Write-Host "  正在移到回收站..."
$shell = New-Object -ComObject Shell.Application
$rb = $shell.NameSpace(0x0a)
$totalFiles = 0
foreach ($f in $tempFiles) {
    try {
        $rb.MoveHere($f.FullName)
        $totalFiles++
    } catch { }
}
Write-Host "  ✅ 已完成！已将 $totalFiles 个文件移到回收站"
Write-Host "  如需彻底删除，请手动清空回收站"
```

</details>

**风险等级**：🟡 中（需确认后删除）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot find path ... does not exist` | temp 目录下某些路径不存在 | 自动跳过 |
| `Access is denied` | 系统临时文件正在使用中 | 跳过，正常现象 |
| `MoveHere` 失败 | 回收站操作异常 | 手动清或用其他方式 |

---

### 模块 4：IIS 站点管理

**用途**：查看站点状态、应用池信息、快速重启。

**常你说**：`"我的 IIS 站点正常吗？"` / `"重启一下应用池"`

**前置条件**（需管理员权限）：
```powershell
if (-not (Get-Module -ListAvailable -Name WebAdministration)) {
    Write-Host "⚠️ IIS 管理工具未安装，请以管理员运行:"
    Install-WindowsFeature Web-Mgmt-Tools
}
Import-Module WebAdministration
```

<details>
<summary>📋 展开查看命令 — 查看站点和应用池</summary>

```powershell
Import-Module WebAdministration

Write-Host "════════ IIS 站点列表 ════════"
Get-Website | Select-Object @{N='站点名';E={$_.Name}},
    @{N='状态';E={$_.State}},
    @{N='物理路径';E={$_.PhysicalPath}},
    @{N='应用池';E={$_.ApplicationPool}},
    @{N='绑定';E={$_.Bindings -join ';'}} |
    Format-Table -AutoSize

Write-Host "`n════════ 应用池状态 ════════"
Get-WebAppPoolState | Select-Object @{N='名';E={$_.Name}}, @{N='状态';E={$_.Value}} |
    Format-Table -AutoSize
```

</details>

<details>
<summary>📋 展开查看命令 — 重启站点（需确认）</summary>

```powershell
# ⚠️ 仅当用户明确确认后才执行！
# Restart-WebSite -Name "你的站点名"
```

</details>

**风险等级**：🟢 查看只读 / 🟡 重启需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-Website is not recognized` | IIS 模块未加载 | `Install-WindowsFeature Web-Mgmt-Tools` |
| `Cannot connect to IIS` | W3SVC 服务未启动 | 管理服务 |
| `Could not find WebAdministration` | 未装 IIS 管理工具 | 添加 Web 管理工具 |

---

### 模块 5：服务状态监控

**用途**：一眼看出哪些关键服务挂了。

**常你说**：`"检查服务器关键服务"` / `"看下数据库有没有挂"`

<details>
<summary>📋 展开查看命令</summary>

```powershell
$criticalServices = @(
    "W3SVC",        # IIS
    "MSSQLSERVER",  # SQL Server
    "MySQL80",      # MySQL
    "Redis",        # Redis
    "Elasticsearch",# ES
    "Docker",       # Docker
    "Spooler",      # 打印
    "TermService",  # 远程桌面
    "Nginx",        # Nginx
    "Apache",       # Apache
    "Tomcat"        # Tomcat
)

Write-Host "════════ 关键服务状态 ════════"
$hasStopped = $false
foreach ($svc in $criticalServices) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        $icon = if ($s.Status -eq 'Running') { '✅' } else { '❌'; $hasStopped = $true }
        Write-Host "  $icon $($s.DisplayName) [$($s.Status)]"
    }
}
Write-Host "═══════════════════════════════"
if ($hasStopped) { Write-Host "  ⚠️ 有服务未运行" }
else { Write-Host "  ✅ 所有检测服务正常" }
```

</details>

**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot find any service ...` | 该服务未安装 | 自动跳过 |

---

### 模块 6：批量文件操作

**用途**：先预览规则，再确认执行批量重命名/移动。

**常你说**：`"把所有 .log 改成 backup_1.log 格式"`

<details>
<summary>📋 展开查看命令 — 预览模式（默认）</summary>

```powershell
$sourceDir = "D:\logs"    # ← 源目录
$searchFilter = "*.log"   # ← 文件筛选
$renamePrefix = "backup"  # ← 新文件名前缀

$files = Get-ChildItem -Path $sourceDir -Filter $searchFilter -File
Write-Host "════════ 批量重命名预览 ════════"
Write-Host "  扫描到 $($files.Count) 个 $searchFilter 文件"

$i = 1
foreach ($f in $files) {
    Write-Host "  🔄 $($f.Name) → ${renamePrefix}_${i}${f.Extension}"
    $i++
}

Write-Host "`n  共 $($files.Count) 个文件将被重命名"
Write-Host "  ⚠️ 确认执行请说 '确认重命名'"
```

</details>

<details>
<summary>📋 展开查看命令 — 执行模式（需确认）</summary>

```powershell
# ⚠️ 仅当用户明确说「确认重命名」后才执行！
# $i = 1
# foreach ($f in $files) {
#     $newName = "${renamePrefix}_${i}${f.Extension}"
#     Rename-Item -Path $f.FullName -NewName $newName
#     Write-Host "  ✅ $($f.Name) → $newName"
#     $i++
# }
```

</details>

**风险等级**：🟡 中（需确认）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot rename because item already exists` | 新文件名已存在 | 加时间戳避免重名 |
| `Access to the path is denied` | 文件锁定 | 关相关程序再试 |

---

### 模块 7：目录磁盘使用报告

**用途**：用进度条样式一眼看出各目录占用。

**常你说**：`"看看各个目录的空间占用"`

<details>
<summary>📋 展开查看命令</summary>

```powershell
function Get-DirectorySize([string]$Path) {
    (Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue |
     Measure-Object -Property Length -Sum).Sum
}

$dirs = @("C:\inetpub", "C:\Windows\Temp", "C:\ProgramData",
          "$env:TEMP", "C:\Users",
          "C:\Windows\SoftwareDistribution", "D:\")

foreach ($d in $dirs) {
    if (Test-Path $d) {
        $sizeGB = [math]::Round((Get-DirectorySize $d) / 1GB, 2)
        if ($sizeGB -gt 10)     { $icon = '🔴' }
        elseif ($sizeGB -gt 5) { $icon = '🟡' }
        else                  { $icon = '🟢' }
        Write-Host "  $icon $d : ${sizeGB} GB"
    }
}
```

</details>

**风险等级**：🟢 无（只读）

---

## 🆕 模块 8：Windows Update 服务状态与缓存管理

**用途**：诊断 Windows Update 是否卡住、查看已安装补丁、清理更新缓存。

**常你说**：`"Windows Update 正常吗？"` / `"更新缓存能不能删"`

### 8.1 查看更新服务状态与已安装补丁（只读）

<details>
<summary>📋 展开查看命令 — 服务状态与补丁历史</summary>

```powershell
# 更新服务状态
Get-Service -Name wuauserv |
    Select-Object @{N='服务';E={$_.Name}},
        @{N='状态';E={$_.Status}},
        @{N='启动类型';E={$_.StartType}},
        @{N='账号';E={$_.StartName}}

Write-Host ""

# 已安装补丁（最近 10 个）
Get-HotFix | Sort-Object InstalledOn -Descending |
    Select-Object -First 10 @{N='补丁ID';E={$_.HotFixID}},
        @{N='安装日期';E={$_.InstalledOn}}
```

</details>

### 8.2 检查 SoftwareDistribution 更新缓存大小

<details>
<summary>📋 展开查看命令 — 缓存大小分析</summary>

```powershell
$sd = "C:\Windows\SoftwareDistribution"
if (Test-Path $sd) {
    $total = (Get-ChildItem -Path $sd -Recurse -ErrorAction SilentlyContinue |
              Measure-Object -Property Length -Sum).Sum
    Write-Host "  SoftwareDistribution 大小: $([math]::Round($total/1MB,1)) MB"

    $dlDir = Join-Path $sd "Download"
    if (Test-Path $dlDir) {
        $dlSize = (Get-ChildItem -Path $dlDir -Recurse -ErrorAction SilentlyContinue |
                   Measure-Object -Property Length -Sum).Sum
        Write-Host "  └─ 下载缓存(Download): $([math]::Round($dlSize/1MB,1)) MB"
    }
    Write-Host "  💡 若超过 500MB 可考虑清理（需先停止 wuauserv 服务）"
} else {
    Write-Host "  ⚠️ SoftwareDistribution 目录不存在"
}
```

</details>

<details>
<summary>📋 展开查看命令 — 清理更新缓存（需确认）</summary>

```powershell
# ⚠️ 仅当用户明确说「确认清理更新缓存」后才执行！
# Stop-Service -Name wuauserv -Force
# Remove-Item -Path "$sd\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
# Start-Service -Name wuauserv
# Write-Host "  ✅ 已清理更新下载缓存，Windows Update 将重新下载所需补丁"
```

</details>

**风险等级**：🟢 查看只读 / 🟡 清理缓存需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `The service ... cannot be stopped` | 服务正在使用 | 稍后重试或重启后清理 |
| `Access is denied` | 部分缓存文件被锁定 | 先停服务再清理 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| Windows Update 一直不下载 | 服务挂起，重停重启动可解决 |
| 错误码 0x80070005 | 权限问题，清理缓存可修复 |
| 补丁安装失败 | 清理 Download 缓存后重新检查更新 |

---

## 🆕 模块 9：实时性能监控与进程资源分析

**用途**：定位 CPU/内存/磁盘 I/O 瓶颈，按进程排序找到罪魁祸首。

**常你说**：`"服务器变卡了，帮我看看"` / `"哪个进程吃内存最多"`

### 9.1 实时性能计数器（只读）

<details>
<summary>📋 展开查看命令 — CPU/内存/磁盘 实时指标</summary>

```powershell
Get-Counter '\Processor(_Total)\% Processor Time',
              '\Memory\Available MBytes',
              '\Memory\% Used',
              '\PhysicalDisk(_Total)\% Disk Time',
              '\PhysicalDisk(_Total)\Current Disk Queue Length' |
    Select-Object -ExpandProperty CounterSamples |
    Select-Object @{N='指标';E={$_.Path.Split('\')[-2..-1] -join '\'}},
        @{N='当前值';E={[math]::Round($_.CookedValue, 1)}} |
    Format-Table -AutoSize
```

</details>

### 9.2 内存占用 Top 10 进程

<details>
<summary>📋 展开查看命令 — 找内存大户</summary>

```powershell
Get-Process | Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 @{N='进程名';E={$_.Name}},
        @{N='内存(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}},
        @{N='CPU(s)';E={[math]::Round($_.CPU,1)}} |
    Format-Table -AutoSize
```

</details>

### 9.3 磁盘 I/O 详细统计（按进程）

<details>
<summary>📋 展开查看命令 — I/O 排行</summary>

```powershell
Get-Counter '\Process(*)\Read Bytes/sec',
              '\Process(*)\Write Bytes/sec' |
    Select-Object -ExpandProperty CounterSamples |
    Where-Object { $_.CookedValue -gt 0 } |
    Sort-Object CookedValue -Descending |
    Select-Object -First 15 @{N='进程';E={
        $_.Path -replace '\\Process\((.*)\)\\Read Bytes/sec$','$1' |
        ForEach-Object { if ($_ -eq 'idle') { 'System Idle' } else { $_ }
    }}, @{N='Bytes/s';E={[math]::Round($_.CookedValue, 0)}} |
    Format-Table -AutoSize
```

</details>

<details>
<summary>📋 展开查看命令 — 创建长期性能采集（需确认）</summary>

```powershell
# ⚠️ 仅当用户明确说「确认创建」后才执行！
# $collector = New-DataCollectorSet -Name "ServerPerf_$(Get-Date -Format 'yyyyMMdd')" -Path "C:\PerfLogs"
# $collector.DataCollectors.Create(0, "Counter", 0,
#     '\Processor(_Total)\% Processor Time',
#     '\Memory\Available MBytes',
#     '\PhysicalDisk(_Total)\% Disk Time'
# )
# $collector.Commit("C:\PerfLogs\ServerPerf", 0, 0x01) | Out-Null
# Write-Host "  ✅ 已创建性能采集器，数据将保存到 C:\PerfLogs"
```

</details>

**风险等级**：🟢 实时查看 / 🟡 创建采集器需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `The specified counter is not found` | 计数器未注册 | 运行 `lodctr /R` 重建计数器 |
| `Access denied` | 需要管理员权限 | 提升后执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| CPU 持续 >90% | 按进程排序定位异常进程 |
| 可用内存 <500MB | 判断是否内存泄漏， IIS 应用池是否需回收 |
| 磁盘队列长度 >2 | I/O 瓶颈，检查是否日志写入过多 |
| 计数器全为零 | `lodctr /R` 重建性能计数器 |

---

## 🆕 模块 10：安全审计与日志分析

**用途**：检测暴力破解、特权操作、异常登录。

**常你说**：`"帮我查下有没有被入侵"` / `"有没有异常登录记录"`

### 10.1 检测暴力破解尝试（最近 24 小时）

<details>
<summary>📋 展开查看命令 — 暴力破解检测</summary>

```powershell
$since = (Get-Date).AddHours(-24)

$failedLogins = Get-WinEvent -FilterHashtable @{
    LogName='Security'; ID=4625; StartTime=$since
} -ErrorAction SilentlyContinue

if ($failedLogins) {
    Write-Host "⚠️ 最近 24h 失败登录 $($failedLogins.Count) 次`n"
    $failedLogins |
        Select-Object TimeCreated,
            @{N='账号';E={$_.Properties[5].Value}},
            @{N='来源IP';E={$_.Properties[19].Value}} |
        Group-Object SourceIP |
        Sort-Object Count -Descending |
        Select-Object -First 10 @{N='攻击源IP';E={$_.Name}},
            @{N='尝试次数';E={$_.Count}} |
        Format-Table -AutoSize
    Write-Host "  💡 尝试次数 >10 的 IP 建议加入防火墙黑名单"
} else {
    Write-Host "  ✅ 最近 24 小时无失败登录记录"
}
```

</details>

### 10.2 查看特权提升操作（管理员操作审计）

<details>
<summary>📋 展开查看命令 — 特权操作审计</summary>

```powershell
$since = (Get-Date).AddHours(-24)

Write-Host "════════ 特权操作（4672）════════"
Get-WinEvent -FilterHashtable @{
    LogName='Security'; ID=4672; StartTime=$since
} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated,
        @{N='用户';E={$_.Properties[1].Value}},
        @{N='特权';E={$_.Properties[2..($_.Properties.Count-1)].Value -join ', '}} |
    Format-Table -AutoSize
```

</details>

### 10.3 本地管理员组成员检查

<details>
<summary>📋 展开查看命令 — 管理员组审计</summary>

```powershell
Write-Host "════════ 本地管理员组成员 ════════"
Get-LocalGroupMember -Group "Administrators" |
    Select-Object @{N='用户名';E={$_.Name}},
        @{N='来源';E={$_.PrincipalSource}} |
    Format-Table -AutoSize
```

</details>

<details>
<summary>📋 展开查看命令 — 导出安全日志备份</summary>

```powershell
# ⚠️ 仅当用户明确说「确认导出」后才执行！
# $logPath = "C:\Logs\Security_$(Get-Date -Format 'yyyyMMdd').evtx"
# if (-not (Test-Path "C:\Logs")) { New-Item -ItemType Directory -Path "C:\Logs" -Force }
# wevtutil epl Security $logPath
# Write-Host "  ✅ 安全日志已导出到: $logPath"
```

</details>

**风险等级**：🟢 只读审计 / 🟡 导出需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No events were found ...` | 没有符合条件的日志 | 正常，说明期间无异常 |
| `The requested operation cannot be performed on a file ...` | 日志文件被占用 | 复制到另一路径导出 |
| `Get-LocalGroupMember` 报错 | 需要管理员权限 | 提升执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 某 IP 失败登录 >100 次 | 暴力破解，建议防火墙封禁 |
| 4672 事件频繁 | 有人在频繁执行管理员操作，需排查 |
| 管理员组成员异常多了不认识账号 | 立即排查是否被入侵后留后门，删非法账号 |

---

## 🆕 模块 11：注册表与启动项安全审计

**用途**：检测恶意持久化机制（注册表自启动、计划任务、WMI 订阅）。

**常你说**：`"有没有可疑的自启动程序"` / `"检查一下持久化威胁"`

> ⚠️ **本模块所有操作均为只读分析，绝不修改注册表或删除任何键值。**

### 11.1 经典自启动注册表位置扫描

<details>
<summary>📋 展开查看命令 — 自启动注册表扫描</summary>

```powershell
$runKeys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
)

Write-Host "════════ 自启动注册表项 ════════"
foreach ($key in $runKeys) {
    if (Test-Path $key) {
        Write-Host "`n  📁 $($key.Split('\')[-1..-1] -join '\')"
        Get-ItemProperty $key -ErrorAction SilentlyContinue |
            Get-Member -MemberType NoteProperty |
            Where-Object { $_.Name -notlike 'PS*' } |
            ForEach-Object {
                $val = (Get-ItemProperty $key -Name $_.Name -ErrorAction SilentlyContinue).$($_.Name)
                Write-Host "    🔹 $($_.Name) = $val"
            }
    }
}
Write-Host "`n═══════════════════════════════"
Write-Host "  💡 不认识的程序请搜索确认，不要直接删除"
```

</details>

### 11.2 计划任务审计

<details>
<summary>📋 展开查看命令 — 可疑计划任务检测</summary>

```powershell
Write-Host "════════ 计划任务列表 ════════"
Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' } |
    Select-Object @{N='任务名';E={$_.TaskName}},
        @{N='状态';E={$_.State}},
        @{N='作者';E={$_.Author}},
        @{N='运行方式';E={$_.Principal.UserId}} |
    Format-Table -AutoSize

Write-Host "`n════════ 最近修改的任务 ════════"
Get-ScheduledTask | Sort-Object LastWriteTime -Descending |
    Select-Object -First 10 @{N='任务名';E={$_.TaskName}},
        @{N='修改时间';E={$_.LastWriteTime}} |
    Format-Table -AutoSize
```

</details>

### 11.3 WMI 持久化检测

<details>
<summary>📋 展开查看命令 — WMI 事件订阅扫描</summary>

```powershell
Write-Host "════════ WMI 事件订阅 ════════"
try {
    $wmiSubs = Get-CimInstance -Namespace root\subscription -ClassName __EventFilter -ErrorAction SilentlyContinue
    if ($wmiSubs) {
        $wmiSubs | Select-Object @{N='名称';E={$_.Name}},
            @{N='查询';E={$_.Query}} |
            Format-Table -AutoSize
    } else {
        Write-Host "  ✅ 未发现 WMI 事件订阅"
    }
} catch {
    Write-Host "  ⚠️ WMI 查询失败，可能需要管理员权限"
}
```

</details>

### 11.4 系统服务异常检测

<details>
<summary>📋 展开查看命令 — 可疑服务检测</summary>

```powershell
Write-Host "════════ 非微软服务列表 ════════"
Get-Service | Where-Object {
    $_.DisplayName -notlike '*Microsoft*' -and
    $_.DisplayName -notlike '*Windows*' -and
    $_.DisplayName -notlike '*Intel*' -and
    $_.DisplayName -notlike '*NVIDIA*' -and
    $_.DisplayName -notlike '*AMD*' -and
    $_.DisplayName -notlike '*Realtek*' -and
    $_.DisplayName -notlike '*HP*' -and
    $_.DisplayName -notlike '*Dell*'
} | Select-Object @{N='服务名';E={$_.Name}},
    @{N='显示名';E={$_.DisplayName}},
    @{N='状态';E={$_.Status}},
    @{N='启动类型';E={$_.StartType}} |
    Format-Table -AutoSize
```

</details>

**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access to the path is denied` | 权限不足 | 管理员身份运行 |
| `Requested registry access is not allowed` | 注册表权限限制 | 提升权限执行 |
| `Get-CimInstance` 报错 | WMI 服务未启动 | 检查 Winmgmt 服务 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| Run 键值超多（>20个） | 正常软件也会注册，重点排查不认识的 |
| WMI 订阅存在未知项 | 可能是恶意软件持久化，需进一步分析 |
| 服务名随机字符串 | 典型恶意软件特征，需立即排查 |

---

## 🆕 模块 12：磁盘健康状态检测

**用途**：检测磁盘 SMART 状态、坏道预警、磁盘寿命预测。

**常你说**：`"硬盘还健康吗？"` / `"有没有坏道"` / `"磁盘寿命还剩多久"`

> ⚠️ **本模块所有操作均为只读检测，不会执行磁盘修复或擦除操作。**

### 12.1 SMART 状态概览

<details>
<summary>📋 展开查看命令 — SMART 健康状态</summary>

```powershell
Write-Host "════════ 磁盘 SMART 状态 ════════"
Get-PhysicalDisk | Select-Object @{N='磁盘';E={$_.FriendlyName}},
    @{N='状态';E={$_.HealthStatus}},
    @{N='使用时长';E={[math]::Round($_.UsageHours,0)}},
    @{N='温度(°C)';E={$_.Temperature}},
    @{N='剩余寿命%';E={$_.RemainingLifetimePercent}} |
    Format-Table -AutoSize
```

</details>

### 12.2 磁盘坏道与错误计数

<details>
<summary>📋 展开查看命令 — 磁盘错误统计</summary>

```powershell
Write-Host "════════ 磁盘错误统计 ════════"
Get-PhysicalDisk | ForEach-Object {
    $disk = $_
    $errors = Get-StorageReliabilityCounter -PhysicalDisk $disk -ErrorAction SilentlyContinue
    if ($errors) {
        [PSCustomObject]@{
            磁盘 = $disk.FriendlyName
            读取错误 = $errors.ReadErrorsTotal
            写入错误 = $errors.WriteErrorsTotal
            重映射扇区 = $errors.ReallocatedSectors
            待映射扇区 = $errors.PendingSectors
            不可修复错误 = $errors.UncorrectableErrors
        }
    }
} | Format-Table -AutoSize

Write-Host "`n  💡 重映射扇区 >0 或待映射扇区 >0 表示磁盘开始老化"
Write-Host "  💡 不可修复错误 >0 建议立即备份数据并更换磁盘"
```

</details>

### 12.3 磁盘温度监控

<details>
<summary>📋 展开查看命令 — 磁盘温度</summary>

```powershell
Write-Host "════════ 磁盘温度监控 ════════"
Get-PhysicalDisk | ForEach-Object {
    $temp = $_.Temperature
    if ($temp -gt 50)     { $icon = '🔴' }
    elseif ($temp -gt 40) { $icon = '🟡' }
    else                  { $icon = '🟢' }
    [PSCustomObject]@{
        磁盘 = $_.FriendlyName
        温度 = "${temp}°C"
        状态 = $icon
    }
} | Format-Table -AutoSize

Write-Host "`n  💡 温度 >50°C 需检查散热，>60°C 立即停机检查"
```

</details>

### 12.4 磁盘 I/O 延迟分析

<details>
<summary>📋 展开查看命令 — I/O 延迟检测</summary>

```powershell
Write-Host "════════ 磁盘 I/O 延迟 ════════"
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Read',
              '\PhysicalDisk(*)\Avg. Disk sec/Write' |
    Select-Object -ExpandProperty CounterSamples |
    Where-Object { $_.CookedValue -gt 0 } |
    Select-Object @{N='磁盘';E={
        $_.Path -replace '\\PhysicalDisk\((.*)\)\\.*$','$1'
    }}, @{N='平均延迟(ms)';E={[math]::Round($_.CookedValue * 1000, 2)}} |
    Format-Table -AutoSize

Write-Host "`n  💡 读延迟 >20ms 或写延迟 >20ms 表示磁盘性能下降"
```

</details>

**风险等级**：🟢 无（只读检测）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No MSFT_PhysicalDisk ...` | 系统不支持存储诊断 | 需 Windows Server 2016+ |
| `Temperature` 属性不存在 | 磁盘不支持温度传感器 | 用第三方工具检测 |
| `Get-StorageReliabilityCounter` 报错 | 需要管理员权限 | 提升执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| SMART 状态显示 "Warning" | 磁盘开始老化，立即备份数据 |
| 重映射扇区持续增长 | 磁盘寿命将尽，尽快更换 |
| I/O 延迟突然飙升 | 可能磁盘故障前兆，检查 SMART |

---

## 🆕 模块 13：网络连接与端口监控

**用途**：检测异常网络连接、监听端口、可疑外连行为。

**常你说**：`"谁在连我的服务器"` / `"有没有异常外连"` / `"检查监听端口"`

> ⚠️ **本模块所有操作均为只读检测，不会修改防火墙规则或终止连接。**

### 13.1 活动网络连接概览

<details>
<summary>📋 展开查看命令 — 活动连接列表</summary>

```powershell
Write-Host "════════ 活动网络连接 ════════"
Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue |
    Select-Object @{N='本地地址';E={$_.LocalAddress}},
        @{N='本地端口';E={$_.LocalPort}},
        @{N='远程地址';E={$_.RemoteAddress}},
        @{N='远程端口';E={$_.RemotePort}},
        @{N='状态';E={$_.State}},
        @{N='进程';E={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).Name}} |
    Sort-Object RemoteAddress |
    Format-Table -AutoSize
```

</details>

### 13.2 监听端口审计

<details>
<summary>📋 展开查看命令 — 监听端口列表</summary>

```powershell
Write-Host "════════ 监听端口列表 ════════"
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Select-Object @{N='本地地址';E={$_.LocalAddress}},
        @{N='监听端口';E={$_.LocalPort}},
        @{N='进程';E={
            $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
            if ($proc) { "$($proc.Name) (PID: $($proc.Id))" } else { "未知" }
        }} |
    Sort-Object LocalPort |
    Format-Table -AutoSize
```

</details>

### 13.3 可疑外连检测（高频连接分析）

<details>
<summary>📋 展开查看命令 — 异常外连检测</summary>

```powershell
Write-Host "════════ 高频外连目标 ════════"
Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue |
    Group-Object RemoteAddress |
    Where-Object { $_.Count -gt 5 } |
    Sort-Object Count -Descending |
    Select-Object -First 15 @{N='远程IP';E={$_.Name}},
        @{N='连接数';E={$_.Count}},
        @{N='进程';E={
            $proc = Get-Process -Id ($_.Group[0].OwningProcess) -ErrorAction SilentlyContinue
            if ($proc) { $proc.Name } else { "未知" }
        }} |
    Format-Table -AutoSize

Write-Host "`n  💡 连接数 >20 的 IP 需重点排查是否为恶意外连"
```

</details>

### 13.4 防火墙规则审计

<details>
<summary>📋 展开查看命令 — 防火墙规则检查</summary>

```powershell
Write-Host "════════ 防火墙入站规则 ════════"
Get-NetFirewallRule -Direction Inbound -Enabled True -ErrorAction SilentlyContinue |
    Where-Object { $_.Action -eq 'Allow' } |
    Select-Object @{N='规则名';E={$_.DisplayName}},
        @{N='操作';E={$_.Action}},
        @{N='本地端口';E={$_.LocalPort}},
        @{N='远程地址';E={$_.RemoteAddress}} |
    Format-Table -AutoSize
```

</details>

**风险等级**：🟢 无（只读检测）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-NetTCPConnection` 报错 | 需要管理员权限 | 提升执行 |
| `Get-NetFirewallRule` 报错 | 防火墙服务未启动 | 检查 mpssvc 服务 |
| `OwningProcess` 为 0 | 系统进程，正常 | 无需处理 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 未知进程监听 80/443 端口 | 可能是 Web 服务或恶意软件，需排查 |
| 大量外连到同一 IP | 可能是 C2 通信，立即断网排查 |
| 防火墙规则异常宽松 | 建议收紧为最小权限原则 |

---

## 🆕 模块 14：Windows 事件日志诊断

**用途**：快速定位系统错误、警告，按时间/级别筛选关键日志。

**常你说**：`"系统日志有没有最近错误"` / `"最近系统出了什么问题"` / `"看看日志"`

> ⚠️ **本模块仅读取日志，不会修改或清除日志文件。**

### 14.1 系统最近错误日志（最近 2 小时）

<details>
<summary>📋 展开查看命令 — 最近系统错误</summary>

```powershell
$since = (Get-Date).AddHours(-2)

Write-Host "════════ 最近 2 小时系统日志（错误/警告）════════"
Get-WinEvent -FilterHashtable @{
    LogName='System';Level=2,3;StartTime=$since
} -ErrorAction SilentlyContinue |
    Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='来源';E={$_.Message.Split("`r`n")[0] -replace '^.*?: '}},
        @{N='级别';E={if ($_.Level -eq 2) { '❌错误' } else { '⚠️警告' }}} |
    Select-Object -First 30 |
    Format-Table -AutoSize -Wrap
```

</details>

### 14.2 应用程序错误日志

<details>
<summary>📋 展开查看命令 — 最近应用程序错误</summary>

```powershell
$since = (Get-Date).AddHours(-24)

Write-Host "════════ 最近 24 小时应用程序错误 ════════"
Get-WinEvent -FilterHashtable @{
    LogName='Application'; Level=2; StartTime=$since
} -ErrorAction SilentlyContinue |
    Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='来源';E={$_.ProviderName}},
        @{N='错误摘要';E={
            ($_.Message -replace "`r`n",' ' | Select-Object -First 120)
        }} |
    Select-Object -First 20 |
    Format-Table -AutoSize -Wrap
```

</details>

### 14.3 关键系统事件扫描（蓝屏/重启/故障）

<details>
<summary>📋 展开查看命令 — 关键系统事件</summary>

```powershell
Write-Host "════════ 关键系统事件（最近 7 天）════════"
Get-WinEvent -FilterHashtable @{
    LogName='System';
    ID=1074, 6005, 6006, 6008, 6009, 41, 1001, 1002;
    StartTime=(Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue |
    Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='事件ID';E={$_.Id}},
        @{N='说明';E={
            switch ($_.Id) {
                1074 {'系统关机/重启 (User initiated)'}
                6005 {'系统启动'}
                6006 {'系统正常关机'}
                6008 {'非正常关机 (意外断电/崩溃)'}
                6009 {'系统启动 (新会话)'}
                41  {'Kernel-Power 重启 (无干净关机)'}
                1001{'BugCheck (蓝屏)'}
                1002{'应用程序挂起/无响应'}
                default {$_.Message.Split("`r`n")[0]}
            }
        }} |
    Format-Table -AutoSize -Wrap
```

</details>

### 14.4 Setup 日志审计（最近 7 天）

<details>
<summary>📋 展开查看命令 — Setup 最近事件</summary>

```powershell
Write-Host "════════ Setup 最近 7 天事件 ════════"
Get-WinEvent -FilterHashtable @{
    LogName='Setup';
    StartTime=(Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue |
    Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='来源';E={$_.ProviderName}},
        @{N='摘要';E={
            ($_.Message -replace "`r`n",' ' | Select-Object -First 120)
        }} |
    Select-Object -First 15 |
    Format-Table -AutoSize -Wrap
```

</details>

**风险等级**：🟢 无（只读阅读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No events were found ...` | 没有符合条件的日志 | 正常，说明期间无异常 |
| `RPC server is unavailable` | 事件日志服务未运行 | 检查 EventLog 服务 |
| `Access denied` | 权限不足 | 管理员身份执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 每天大量 Error 日志 | 说明存在持续性故障，需逐条排查来源 |
| 非正常关机 (6008) | 可能存在硬件/电源问题 |
| 蓝屏 (1001) | 记录蓝屏代码，排查驱动/硬件 |

---

## 🆕 模块 15：已安装程序与补丁管理

**用途**：查看所有已安装的软件、补丁，检测缺失或不一致情况。

**常你说**：`"看看系统安装了哪些软件"` / `"服务器装了什么程序"` / `"补丁检查"`

> ⚠️ **本模块仅读，不会卸载/安装/修改任何软件。**

### 15.1 已安装程序清单

<details>
<summary>📋 展开查看命令 — 系统已安装程序</summary>

```powershell
Write-Host "════════ 已安装程序清单 ════════"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -and $_.UninstallString -notlike '*{*' } |
    Select-Object @{N='程序名';E={$_.DisplayName}},
        @{N='版本';E={$_.DisplayVersion}},
        @{N='安装日期';E={$_.InstallDate}},
        @{N='大小';E={if($_.EstimatedSize){[math]::Round($_.EstimatedSize/1MB,1)}else{'?'}}} |
    Sort-Object DisplayName |
    Format-Table -AutoSize
```

</details>

### 15.2 已安装 Windows 补丁

<details>
<summary>📋 展开查看命令 — Windows 补丁列表</summary>

```powershell
Write-Host "════════ 已安装 Windows 补丁 ════════"
Get-HotFix | Sort-Object InstalledOn -Descending |
    Select-Object @{N='补丁ID';E={$_.HotFixID}},
        @{N='安装日期';E={$_.InstalledOn}},
        @{N='描述';E={$_.Description}} |
    Format-Table -AutoSize
```

</details>

### 15.3 安装时间线分析

<details>
<summary>📋 展开查看命令 — 软件安装时间线</summary>

```powershell
Write-Host "════════ 最近安装的软件 ════════"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.InstallDate } |
    Sort-Object InstallDate -Descending |
    Select-Object -First 20 @{N='程序名';E={$_.DisplayName}},
        @{N='版本';E={$_.DisplayVersion}},
        @{N='安装日期';E={$_.InstallDate}} |
    Format-Table -AutoSize
```

</details>

### 15.4 补丁对比（检测缺失）

<details>
<summary>📋 展开查看命令 — 补丁一致性检查</summary>

```powershell
$hotfixes = Get-HotFix -ErrorAction SilentlyContinue | Select-Object -ExpandProperty HotFixID
$currentBuild = [System.Environment]::OSVersion.Version
$expectedPatches = @()

# 检测 Windows 10/11 常见缺失补丁
if ($currentBuild.Major -ge 10) {
    $kbToCheck = @(
        "KB5034441",  # Secure Boot DBX
        "KB5036897",  # 最新 .NET
        "KB5037771"   # 最新累积
    )
    foreach ($kb in $kbToCheck) {
        if ($hotfixes -notcontains $kb) {
            $expectedPatches += "$kb - 缺失"
        }
    }
}

Write-Host "════════ 补丁一致性检查 ════════"
Write-Host "  当前版本: $($currentBuild.Major).$($currentBuild.Minor).$($currentBuild.Build)"
Write-Host ""
if ($expectedPatches.Count -gt 0) {
    Write-Host "  ⚠️ 缺失补丁:"
    foreach ($p in $expectedPatches) { Write-Host "    ❌ $p" }
} else {
    Write-Host "  ✅ 常用补丁均已安装"
}
```

</details>

**风险等级**：🟢 无（只读阅读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Requested registry access is not allowed` | 部分注册表权限限制 | 管理员身份执行 |
| `Get-HotFix` 报错 | 需要管理员权限 | 管理员身份执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 某台服务器明显比其他机器少很多补丁 | 可能 WSUS/自动更新未运行 |
| 安装时间线上出现未知日期的软件 | 可能未经授权安装，需排查 |
| KB 补丁安装失败 | Windows Update 服务或缓存异常 |

---

## 🆕 模块 16：用户会话与登录状态监控

**用途**：监控当前登录的用户、远程会话、僵尸会话、账户状态。

**常你说**：`"谁在服务器上"` / `"有没有异常登录"` / `"查看远程会话"`

> ⚠️ **本模块仅读，不会结束会话、锁定账户或修改密码策略。**

### 16.1 当前登录用户概览

<details>
<summary>📋 展开查看命令 — 当前登录用户</summary>

```powershell
Write-Host "════════ 当前登录用户 ════════"
Get-CimInstance Win32_LogonSession | Where-Object { $_.LogonType -ne 0 } |
    Select-Object @{N='用户名';E={
        $user = Get-CimInstance Win32_ComputerSystem | Select-Object UserName
        $user.UserName ?? "未知"
    }},
    @{N='会话ID';E={$_.LogonId}},
    @{N='登录类型';E={
        switch ($_.LogonType) {
            2 {'交互 (本地登录)'}
            3 {'网络登录'}
            4 {'批处理'}
            5 {'服务'}
            7 {'解锁'}
            8 {'网络明文'}
            9 {'新凭据'}
            10 {'远程交互 (RDP)'}
            11 {'缓存交互'}
            default {"其他 ($($_.LogonType))"}
        }
    }},
    @{N='登录时间';E={$_.StartTime}} |
    Format-Table -AutoSize
```

</details>

### 16.2 远程桌面会话监控

<details>
<summary>📋 展开查看命令 — RDP 会话列表</summary>

```powershell
Write-Host "════════ 远程桌面会话 (RDP) ════════"
Get-CimInstance Win32_LogonSession | Where-Object { $_.LogonType -eq 10 } |
    Select-Object @{N='用户名';E={
        $user = Get-CimInstance Win32_ComputerSystem | Select-Object UserName
        $user.UserName ?? "未知"
    }},
    @{N='会话ID';E={$_.LogonId}},
    @{N='登录时间';E={$_.StartTime}},
    @{N='空闲时间(分钟)';E={
        if ($_.StartTime) {
            [math]::Round(((Get-Date) - $_.StartTime).TotalMinutes, 0)
        } else { 0 }
    }} |
    Format-Table -AutoSize
Write-Host "`n💡 空闲 >60 分钟的会话可能为僵尸会话"
```

</details>

### 16.3 异常登录检测（多 IP / 异地登录）

<details>
<summary>📋 展开查看命令 — 异常登录分析</summary>

```powershell
Write-Host "════════ 最近 7 天的登录来源 ════════"
Get-WinEvent -FilterHashtable @{
    LogName='Security';
    ID=4624;
    StartTime=(Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue |
    Where-Object { $_.Properties[18].Value -ne '-' } |
    Select-Object @{N='登录时间';E={$_.TimeCreated}},
        @{N='用户名';E={$_.Properties[5].Value}},
        @{N='来源IP';E={$_.Properties[18].Value}},
        @{N='登录类型';E={
            switch ($_.Properties[8].Value) {
                2 {'交互(本地)'}
                3 {'网络'}
                10 {'远程(RDP)'}
                default {"其他"}
            }
        }} |
    Group-Object SourceIP |
    Sort-Object Count -Descending |
    Select-Object -First 10 @{N='来源IP';E={$_.Name}},
        @{N='登录次数';E={$_.Count}},
        @{N='最近登录';E={$_.Group[0].TimeCreated}} |
    Format-Table -AutoSize

Write-Host "`n💡 任何未知来源IP 的登录都值得警惕"
```

</details>

### 16.4 系统账户状态检查

<details>
<summary>📋 展开查看命令 — 账户状态审计</summary>

```powershell
Write-Host "════════ 本地用户账户状态 ════════"
Get-LocalUser | Where-Object { $_.Enabled -eq $true } |
    Select-Object @{N='账户名';E={$_.Name}},
        @{N='状态';E={if ($_.Enabled) {'启用'}else{'禁用'}}},
        @{N='最后登录';E={$_.LastLogon}},
        @{N='密码过期';E={
            if ($_.PasswordExpires) { $_.PasswordExpires } else { '永不过期 ⚠️' }
        }},
        @{N='需要密码';E={if ($_.PasswordRequired) {'是'}else{'否 ⚠️'}}} |
    Format-Table -AutoSize

Write-Host "`n⚠️ 标记的账户存在安全风险：无密码或密码永不过期"
```

</details>

**风险等级**：🟢 无（只读监控）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-LocalUser` 报错 | 需要管理员权限 | 管理员身份执行 |
| `Get-CimInstance` 报错 | WMI 未启动 | 检查 Winmgmt |
| `No events found` | 没有相关日志 | 正常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 多个 RDP 会话来自同一 IP | 可能正常（NAT），也可能为多人共用账户 |
| Guest 账户启用 | 不必要的安全风险，建议禁用 |
| 僵尸 RDP 会话 | 占用资源，闲置超时后应自动断开 |
| 密码永不过期 | 合规风险，建议设置密码策略 |

---

## 🆕 模块 17：计划任务审计

**用途**：审计所有计划任务，检测可疑的持久化行为（恶意软件常用的自启动方式）。

**常你说**：`"有没有可疑计划任务"` / `"检查计划任务"` / `"有没有凌晨执行的任务"`

> ⚠️ **本模块仅读，不会创建/删除/修改任何计划任务。**

### 17.1 所有计划任务清单

<details>
<summary>📋 展开查看命令 — 计划任务概览</summary>

```powershell
Write-Host "════════ 所有计划任务 ════════"
$tasks = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' }
$total = ($tasks | Measure-Object).Count
Write-Host "  总数: $total 个启用的任务`n"

$tasks | Select-Object @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='状态';E={$_.State}},
    @{N='触发器';E={
        $info = Get-ScheduledTaskInfo -TaskName $_.TaskName -TaskPath $_.TaskPath -ErrorAction SilentlyContinue
        if ($info.LastRunTime) { "上次: $($info.LastRunTime)" } else { "从未执行" }
    }} |
    Sort-Object TaskPath, TaskName |
    Format-Table -AutoSize
```

</details>

### 17.2 异常计划任务检测（凌晨执行 / 隐藏窗口 / 临时目录）

<details>
<summary>📋 展开查看命令 — 异常任务扫描</summary>

```powershell
Write-Host "════════ 异常计划任务检测 ════════"
$suspicious = @()
$tasks = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' }

foreach ($task in $tasks) {
    $score = 0
    $reasons = @()
    $taskInfo = Get-ScheduledTaskInfo -TaskName $task.TaskName -TaskPath $task.TaskPath -ErrorAction SilentlyContinue
    $lastRun = if ($taskInfo.LastRunTime) { $taskInfo.LastRunTime } else { $null }

    # 检测1: 凌晨执行 (0:00-5:00)
    # 通过检查 Actions 中的命令行参数
    $actions = $task.Actions
    foreach ($action in $actions) {
        $argStr = "$($action.Arguments)" + "$($action.Execute)"
        if ($argStr -match '(-WindowStyle\s+Hidden|/hidden|-w\s+hidden|-hide|/background|/min|-NoLogo\s+-NonInteractive\s+-WindowStyle\s+Hidden)') {
            $score += 2
            $reasons += "隐藏窗口执行"
        }
        if ($argStr -match '(\\Temp\\|\\TMP\\|\\AppData\\Local\\Temp\\)') {
            $score += 3
            $reasons += "从临时目录执行"
        }
        if ($argStr -match '((?:powershell|cmd|wscript|cscript|rundll32|mshta|regsvr32).*?(?:-enc|-e\s|IEX|Invoke-Expression|DownloadString|FromBase64String|eval))') {
            $score += 4
            $reasons += "可疑命令特征(编码/下载)"
        }
    }

    # 检测2: 无描述信息的任务
    if (-not $task.Description -or $task.Description -eq '') {
        $score += 1
        $reasons += "无描述信息"
    }

    if ($score -ge 3) {
        $suspicious += [PSCustomObject]@{
            任务名 = $task.TaskName
            路径 = $task.TaskPath
            风险分 = $score
            原因 = ($reasons -join ', ')
            上次运行 = $lastRun
        }
    }
}

if ($suspicious.Count -gt 0) {
    $suspicious | Sort-Object 风险分 -Descending |
        Format-Table -AutoSize -Wrap
    Write-Host "`n🔴 以上任务存在可疑特征，建议逐条排查"
} else {
    Write-Host "✅ 未发现明显可疑的计划任务"
}
```

</details>

### 17.3 按触发条件分类（开机自启 / 定时 / 用户登录触发）

<details>
<summary>📋 展开查看命令 — 触发条件分类</summary>

```powershell
Write-Host "════════ 计划任务按触发类型分类 ════════`n"

# 开机自启
Write-Host "═══ 开机/系统启动时触发 ═══"
Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'BootTrigger|StartupTrigger' }
} | Select-Object -First 15 @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='触发器';E={
        ($_.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ', '
    }} |
    Format-Table -AutoSize

Write-Host "`n═══ 用户登录时触发 ═══"
Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'LogonTrigger' }
} | Select-Object -First 15 @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='触发器';E={
        ($_.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ', '
    }} |
    Format-Table -AutoSize

Write-Host "`n═══ 定时/周期性触发 (数量最多) ═══"
$timeTasks = Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'TimeTrigger|DailyTrigger|WeeklyTrigger|MonthlyTrigger' }
}
Write-Host "  总数: $(($timeTasks | Measure-Object).Count) 个"
```

</details>

### 17.4 非 Microsoft 创建的任务

<details>
<summary>📋 展开查看命令 — 第三方/非系统任务</summary>

```powershell
Write-Host "════════ 非 Microsoft 创建的计划任务 ════════"
$nonMsTasks = Get-ScheduledTask | Where-Object {
    $_.TaskPath -notmatch '\\\\Microsoft\\\\' -and $_.State -ne 'Disabled'
}

if ($nonMsTasks) {
    $nonMsTasks | Select-Object @{N='任务名';E={$_.TaskName}},
        @{N='路径';E={$_.TaskPath}},
        @{N='状态';E={$_.State}},
        @{N='描述';E={
            if ($_.Description) { $_.Description.Substring(0, [Math]::Min(60, $_.Description.Length)) }
            else { '(无描述)' }
        }} |
        Format-Table -AutoSize
    Write-Host "`n💡 第三方任务值得审查，尤其是无描述且来源不明的"
} else {
    Write-Host "✅ 无非 Microsoft 计划任务"
}
```

</details>

**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access denied` | 权限不足 | 管理员身份执行 |
| `The system cannot find the file specified` | 任务引用的程序已删除 | 正常（残留任务），值得清理 |
| `Task Scheduler service is not running` | 计划任务服务未启动 | `Start-Service Schedule` |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 大量凌晨执行的隐藏窗口任务 | 软件更新常见，但需逐条确认来源 |
| 从 Temp 目录执行的任务 | 高危特征，多数恶意软件行为 |
| 无描述的随机名任务 | 可能是病毒/蠕虫创建，建议隔离排查 |
| 编码命令 (Base64) 执行 | 极高风险，常见于挖矿脚本和外连木马 |

---

## 🆕 模块 18：文件共享与 SMB 审计

**用途**：列出所有共享文件夹、当前 SMB 连接、权限风险检测。

**常你说**：`"有哪些共享文件夹"` / `"共享权限安全吗"` / `"谁在访问共享"` / `"SMB 审计"`

> ⚠️ **本模块仅读，不会关闭共享、断开连接或修改权限。**

### 18.1 已共享文件夹清单

<details>
<summary>📋 展开查看命令 — 共享文件夹列表</summary>

```powershell
Write-Host "════════ 已共享文件夹 ════════"
Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false } |
    Select-Object @{N='共享名';E={$_.Name}},
        @{N='路径';E={$_.Path}},
        @{N='描述';E={if($_.Description){$_.Description}else{'(无)'}}},
        @{N='最大用户数';E={$_.ConcurrentUserLimit}},
        @{N='缓存模式';E={$_.CachingMode}},
        @{N='共享状态';E={$_.ShareState}} |
    Format-Table -AutoSize

Write-Host "`n💡 ADMIN$ 和 IPC$ 为系统默认管理共享，属正常"
```

</details>

### 18.2 共享权限审计

<details>
<summary>📋 展开查看命令 — 共享与 NTFS 权限</summary>

```powershell
Write-Host "════════ 共享权限审计 ════════"
$shares = Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false }

foreach ($share in $shares) {
    Write-Host "`n═══ 共享: $($share.Name) → $($share.Path) ═══"

    # 共享级别权限
    try {
        $sharePerm = Get-SmbShareAccess -Name $share.Name -ErrorAction SilentlyContinue
        foreach ($perm in $sharePerm) {
            $flag = if ($perm.AccessRight -eq 'Full' -and $perm.AccountName -eq 'Everyone') {
                "🔴 高风险: Everyone 拥有完全控制"
            } elseif ($perm.AccountName -eq 'Everyone') {
                "⚠️ Everyone 可访问"
            } else {
                ""
            }
            Write-Host "  共享权限: $($perm.AccountName) -> $($perm.AccessRight)  $flag"
        }
    } catch {
        Write-Host "  共享权限: 无法获取"
    }

    # NTFS 级别权限（对物理路径）
    if (Test-Path $share.Path) {
        $ntfsPerm = Get-Acl $share.Path -ErrorAction SilentlyContinue
        if ($ntfsPerm) {
            $ntfsPerm.Access | Where-Object { $_.IdentityReference -match 'Everyone|BUILTIN|Guest|ANONYMOUS' } |
                ForEach-Object {
                    Write-Host "  NTFS权限: $($_.IdentityReference) -> $($_.FileSystemRights) ⚠️ 宽松权限"
                }
        }
    }
}
```

</details>

### 18.3 当前 SMB 连接会话

<details>
<summary>📋 展开查看命令 — 活跃 SMB 会话</summary>

```powershell
Write-Host "════════ 当前 SMB 连接会话 ════════"
$sessions = Get-SmbSession -ErrorAction SilentlyContinue |
    Select-Object @{N='客户端';E={$_.ClientComputerName}},
        @{N='用户名';E={$_.UserName}},
        @{N='空闲时间(分钟)';E={[math]::Round($_.IdleTime.TotalMinutes, 0)}},
        @{N='会话时长(分钟)';E={[math]::Round((New-TimeSpan -Start $_.SessionStartTime).TotalMinutes, 0)}} |
    Sort-Object @{E='空闲时间(分钟)';Descending=$true}

if ($sessions) {
    $sessions | Format-Table -AutoSize
    Write-Host "`n💡 空闲 >60 分钟的会话可能为僵尸连接"
} else {
    Write-Host "  当前无活跃 SMB 会话"
}
```

</details>

### 18.4 开放共享中的风险项汇总

<details>
<summary>📋 展开查看命令 — 风险汇总</summary>

```powershell
Write-Host "════════ 共享风险汇总 ════════"
$risks = @()
$shares = Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false }

foreach ($share in $shares) {
    $sharePerm = Get-SmbShareAccess -Name $share.Name -ErrorAction SilentlyContinue
    foreach ($perm in $sharePerm) {
        if ($perm.AccountName -eq 'Everyone') {
            $risks += "🔴 [$($share.Name)] Everyone -> $($perm.AccessRight) 控制权"
        }
        if ($perm.AccountName -eq 'ANONYMOUS LOGON' -or $perm.AccountName -eq 'Guest') {
            $risks += "🔴 [$($share.Name)] $($perm.AccountName) -> $($perm.AccessRight)"
        }
    }

    # 检查共享指向路径不存在
    if (-not (Test-Path $share.Path)) {
        $risks += "⚠️ [$($share.Name)] 共享路径不存在: $($share.Path)"
    }
}

if ($risks.Count -gt 0) {
    $risks | ForEach-Object { Write-Host $_ }
    Write-Host "`n建议: 收紧共享权限为最小访问原则，禁用 Guest/匿名访问"
} else {
    Write-Host "✅ 未发现高风险的共享配置"
}

# 同时检查 SMBv1 是否启用
$smb1 = Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -ErrorAction SilentlyContinue
if ($smb1 -and $smb1.State -eq 'Enabled') {
    Write-Host "`n🔴 SMBv1 已启用！存在 WannaCry 等勒索软件漏洞风险，建议禁用"
}
```

</details>

**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-SmbShare` 报错 | SMB 未启用或无权限 | 管理员身份在服务器上执行 |
| `Get-SmbSession` 为空 | 当前无 SMB 连接 | 正常 |
| `Access denied on Get-Acl` | 部分目录 NTFS 权限限制 | 某些系统目录属正常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| Everyone 拥有完全控制 | 任何网络用户可读/写，极大风险 |
| SMBv1 仍启用 | 永恒之蓝等漏洞存在，应立即禁用 |
| 指向不存在的路径 | 残留共享，建议删除 |
| 大量僵尸 SMB 会话 | 客户端未正常断开，占用连接数 |

---

## 🆕 模块 19：DNS 解析与网卡诊断

**用途**：DNS 缓存查看与清空、解析链路测试、网卡 IP 配置、路由表检查。

**常你说**：`"DNS 解析正常吗"` / `"网卡配置"` / `"网络诊断"` / `"路由表"`

> ⚠️ **本模块操作：DNS 缓存查看/清空（可恢复）+ 网卡 IP 查看（只读）。DNS 清空后会重新从服务器获取，非破坏性。**

### 19.1 DNS 缓存与解析测试

<details>
<summary>📋 展开查看命令 — DNS 缓存查看与清空</summary>

```powershell
Write-Host "════════ DNS 缓存 ════════"
$dnsCache = Get-DnsClientCache -ErrorAction SilentlyContinue
if ($dnsCache) {
    Write-Host "  缓存条目: $(($dnsCache | Measure-Object).Count)"
    $dnsCache | Select-Object -First 20 @{N='域名';E={$_.Entry}},
        @{N='类型';E={$_.RecordType}},
        @{N='IP地址';E={$_.Data}},
        @{N='TTL(秒)';E={$_.TimeToLive}} |
        Format-Table -AutoSize
} else {
    Write-Host "  当前无 DNS 缓存"
}

Write-Host "`n════════ DNS 缓存中异常的记录 (TTL异常长) ════════"
if ($dnsCache) {
    $abnormal = $dnsCache | Where-Object { $_.TimeToLive -gt 86400 }
    if ($abnormal) {
        $abnormal | Select-Object Entry, Data, TimeToLive | Format-Table -AutoSize
    } else {
        Write-Host "  ✅ 无异常记录"
    }
}

Write-Host "`n💡 如需清空 DNS 缓存，说：「确认清空 DNS 缓存」"
Write-Host "  清空命令: Clear-DnsClientCache  (清空后会自动从DNS服务器重新获取)"
```

</details>

### 19.2 DNS 服务器配置与解析链路测试

<details>
<summary>📋 展开查看命令 — DNS 服务器配置</summary>

```powershell
Write-Host "════════ DNS 服务器配置 ════════"
Get-DnsClientServerAddress -AddressFamily IPv4 |
    Where-Object { $_.ServerAddresses.Count -gt 0 } |
    Select-Object @{N='网卡';E={$_.InterfaceAlias}},
        @{N='索引';E={$_.InterfaceIndex}},
        @{N='DNS 服务器';E={($_.ServerAddresses -join ', ')}} |
    Format-Table -AutoSize

Write-Host "`n════════ 解析链路测试 (逐级 DNS) ════════"
$testDomains = @('www.baidu.com', 'www.google.com', 'portal.azure.com')
foreach ($domain in $testDomains) {
    try {
        $result = Resolve-DnsName -Name $domain -Type A -ErrorAction Stop
        $ip = ($result | Where-Object { $_.Type -eq 'A' } | Select-Object -First 1).IPAddress
        if ($ip) { Write-Host "  ✅ $domain → $ip" }
        else { Write-Host "  ❌ $domain → 解析失败" }
    } catch {
        Write-Host "  ❌ $domain → $($_.Exception.Message.Split('.')[0])"
    }
}
```

</details>

### 19.3 网卡 IP 配置概览

<details>
<summary>📋 展开查看命令 — 网卡配置</summary>

```powershell
Write-Host "════════ 网卡 IP 配置 ════════"
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.InterfaceAlias -notmatch 'Loopback' -and $_.IPAddress -ne '127.0.0.1' } |
    Select-Object @{N='网卡';E={$_.InterfaceAlias}},
        @{N='IP 地址';E={$_.IPAddress}},
        @{N='子网掩码';E={$_.PrefixLength}},
        @{N='网关';E={
            $ifIndex = $_.InterfaceIndex
            $gw = Get-NetRoute -InterfaceIndex $ifIndex -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue
            if ($gw) { $gw.NextHop } else { '-' }
        }},
        @{N='状态';E={$_.AddressState}} |
    Format-Table -AutoSize

Write-Host "`n════════ 网卡 MAC 地址与速率 ════════"
Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    Select-Object @{N='网卡名';E={$_.Name}},
        @{N='MAC';E={$_.MacAddress}},
        @{N='速率';E={if($_.LinkSpeed){ "$([math]::Round($_.LinkSpeed/1e9,1)) Gbps" }else{'未知'}}},
        @{N='状态';E={$_.Status}} |
    Format-Table -AutoSize
```

</details>

### 19.4 路由表检查

<details>
<summary>📋 展开查看命令 — IPv4 路由表</summary>

```powershell
Write-Host "════════ IPv4 路由表 ════════"
Get-NetRoute -AddressFamily IPv4 |
    Where-Object { $_.DestinationPrefix -ne '255.255.255.255/32' } |
    Sort-Object @{E={if ($_.DestinationPrefix -eq '0.0.0.0/0') {0} else {1}}},
        @{E='RouteMetric'} |
    Select-Object @{N='目标网络';E={$_.DestinationPrefix}},
        @{N='下一跳';E={$_.NextHop}},
        @{N='接口';E={$_.InterfaceAlias}},
        @{N='跃点数';E={$_.RouteMetric}},
        @{N='协议';E={$_.Protocol}} |
    Format-Table -AutoSize

Write-Host "`n💡 跃点数越小优先级越高"
Write-Host "💡 0.0.0.0/0 为默认路由（所有出网流量由此控制）"
```

</details>

**风险等级**：🟡 中（含 DNS 缓存清空操作，需用户确认）

| 操作 | 风险 | 说明 |
|------|------|------|
| DNS 缓存查看 | 🟢 无 | 纯只读 |
| DNS 解析测试 | 🟢 无 | 纯只读，零风险 |
| 网卡配置查看 | 🟢 无 | 纯只读 |
| 路由表查看 | 🟢 无 | 纯只读 |
| **DNS 缓存清空** | 🟡 中 | 清空后需用户说「确认清空 DNS 缓存」，清空后自动从 DNS 服务器重建，非破坏性 |

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Resolve-DnsName` 超时 | DNS 服务器不可达 | 检查 DNS 服务器配置和网络连通性 |
| `Get-NetIPAddress` 为空 | 网卡未分配 IPv4 | 检查 DHCP 或静态 IP 配置 |
| `Get-NetRoute` 无默认路由 | 无互联网出口 | 检查网关配置 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| DNS 缓存中大量 TTL 异常长的记录 | 可能 DNS 服务器配置问题或域名劫持 |
| 多网卡存在多个默认路由 | 路由冲突导致网络不稳定 |
| DNS 服务器指向不可达 IP | 域名解析全部失败 |
| 网卡速率不匹配（1Gbps vs 100Mbps） | 网线/交换机端口故障 |

---

## 🆕 模块 20：SSL 证书过期检测

**用途**：检测本机 IIS / 所有 HTTPS 站点的 SSL 证书到期时间，提前预警，避免网站突然报"证书无效"。

**常你说**：`"SSL 证书快到期了吗"` / `"证书检查"` / `"HTTPS 站点证书还有多久"` / `"哪些证书要过期了"`

> ⚠️ **本模块仅读，不会申请、续签或删除任何证书。**

### 20.1 本机证书仓库扫描（个人 + 机器）

<details>
<summary>📋 展开查看命令 — 本机所有证书到期时间</summary>

```powershell
Write-Host "════════ 本机证书过期检查 ════════"
$warningDays = 30
$now = Get-Date

$stores = @(
    [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine,
    [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser
)
$storeNames = @('My', 'WebHosting', 'Root', 'CA')

$certs = foreach ($loc in $stores) {
    foreach ($name in $storeNames) {
        try {
            $store = [System.Security.Cryptography.X509Certificates.X509Store]::new($name, $loc)
            $store.Open('ReadOnly')
            foreach ($cert in $store.Certificates) {
                $daysLeft = ($cert.NotAfter - $now).Days
                [PSCustomObject]@{
                    主体       = ($cert.Subject -replace 'CN=', '' -split ',')[0].Trim()
                    存储位置   = "$loc\$name"
                    到期时间   = $cert.NotAfter.ToString('yyyy-MM-dd')
                    剩余天数   = $daysLeft
                    状态       = if ($daysLeft -lt 0) { '❌ 已过期' }
                                 elseif ($daysLeft -lt $warningDays) { '⚠️ 即将过期' }
                                 else { '✅ 正常' }
                    颁发者     = ($cert.Issuer -replace 'CN=', '' -split ',')[0].Trim()
                }
            }
            $store.Close()
        } catch {}
    }
}

$result = $certs | Where-Object { $_.剩余天数 -lt 90 } |
    Sort-Object 剩余天数

if ($result) {
    $result | Format-Table -AutoSize
} else {
    Write-Host "✅ 未发现 90 天内到期的证书"
}
```

</details>

### 20.2 IIS 绑定的 HTTPS 证书检查

<details>
<summary>📋 展开查看命令 — IIS 站点 HTTPS 证书</summary>

```powershell
Write-Host "════════ IIS HTTPS 绑定证书 ════════"
Import-Module WebAdministration -ErrorAction SilentlyContinue

$httpsBindings = Get-WebBinding | Where-Object { $_.protocol -eq 'https' }
if (-not $httpsBindings) {
    Write-Host "  未发现 HTTPS 绑定"
} else {
    foreach ($binding in $httpsBindings) {
        $hash = $binding.certificateHash
        if ($hash) {
            $cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Thumbprint -eq $hash }
            if ($cert) {
                $daysLeft = ($cert.NotAfter - (Get-Date)).Days
                $status = if ($daysLeft -lt 0) { '❌ 已过期' }
                           elseif ($daysLeft -lt 30) { '⚠️ 即将过期' }
                           else { '✅ 正常' }
                Write-Host "  站点: $($binding.bindingInformation)"
                Write-Host "  证书: $($cert.Subject)"
                Write-Host "  到期: $($cert.NotAfter.ToString('yyyy-MM-dd'))  剩余: $daysLeft 天  $status"
                Write-Host ""
            }
        }
    }
}
```

</details>

### 20.3 远程域名证书探测（本地无证书的站点）

<details>
<summary>📋 展开查看命令 — 探测远程域名证书</summary>

```powershell
# 将下方域名替换为你需要检测的站点
$domains = @('www.baidu.com', 'www.taobao.com')  # 示例，替换为你的域名

Write-Host "════════ 远程域名 SSL 证书检测 ════════"
foreach ($domain in $domains) {
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient($domain, 443)
        $sslStream  = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false, { $true })
        $sslStream.AuthenticateAsClient($domain)
        $cert = $sslStream.RemoteCertificate
        $expiry = [DateTime]::Parse($cert.GetExpirationDateString())
        $daysLeft = ($expiry - (Get-Date)).Days
        $status = if ($daysLeft -lt 0) { '❌ 已过期' }
                   elseif ($daysLeft -lt 30) { '⚠️ 即将过期' }
                   else { '✅ 正常' }
        Write-Host "  $domain → 到期: $($expiry.ToString('yyyy-MM-dd'))  剩余: $daysLeft 天  $status"
        $sslStream.Close()
        $tcpClient.Close()
    } catch {
        Write-Host "  $domain → ❌ 连接失败: $($_.Exception.Message.Split('.')[0])"
    }
}
```

</details>

### 20.4 即将过期证书汇总报告

<details>
<summary>📋 展开查看命令 — 30 天内到期汇总</summary>

```powershell
Write-Host "════════ 30 天内到期证书汇总 ════════"
$now = Get-Date
$soon = @()

foreach ($loc in @('LocalMachine','CurrentUser')) {
    foreach ($name in @('My','WebHosting')) {
        try {
            $store = [System.Security.Cryptography.X509Certificates.X509Store]::new($name, $loc)
            $store.Open('ReadOnly')
            $soon += $store.Certificates | Where-Object {
                ($_.NotAfter - $now).Days -le 30 -and ($_.NotAfter - $now).Days -ge 0
            } | Select-Object @{N='证书名';E={($_.Subject -replace 'CN=','' -split ',')[0].Trim()}},
                @{N='剩余天数';E={($_.NotAfter - $now).Days}},
                @{N='到期日期';E={$_.NotAfter.ToString('yyyy-MM-dd')}},
                @{N='存储';E={"$loc\$name"}}
            $store.Close()
        } catch {}
    }
}

if ($soon.Count -gt 0) {
    $soon | Sort-Object 剩余天数 | Format-Table -AutoSize
    Write-Host "`n🔴 以上证书需要尽快续签！"
} else {
    Write-Host "✅ 30 天内无证书过期"
}
```

</details>

**风险等级**：🟢 无（只读，不修改任何证书）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access denied` | 需管理员权限 | 管理员身份执行 |
| `WebAdministration not found` | IIS 未安装 | 跳过模块 20.2 |
| `Connection refused` | 远程域名 443 不可达 | 检查域名和防火墙 |
| `AuthenticationException` | SSL 握手失败 | 域名可能证书异常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 证书显示"已过期"但网站仍在访问 | 浏览器有缓存，实际用户已经开始看到警告 |
| IIS 绑定的证书和仓库里的不一致 | IIS 用指纹引用，需手动在 IIS 管理器重新绑定 |
| Let's Encrypt 证书 90 天到期周期 | 需设置自动续签（如 win-acme） |

---

## 🆕 模块 21：Windows 防火墙规则审计

**用途**：列出所有防火墙规则，识别过度开放（Any/Any）、可疑来源的规则，找出安全漏洞。

**常你说**：`"防火墙规则有没有问题"` / `"防火墙审计"` / `"哪些端口对外开放"` / `"有没有高危防火墙规则"`

> ⚠️ **本模块仅读，不会新增、删除或修改任何防火墙规则。**

### 21.1 所有入站规则概览

<details>
<summary>📋 展开查看命令 — 入站规则列表</summary>

```powershell
Write-Host "════════ 入站防火墙规则（启用中）════════"
$inbound = Get-NetFirewallRule -Direction Inbound -Enabled True -ErrorAction SilentlyContinue

Write-Host "  启用的入站规则总数: $(($inbound | Measure-Object).Count)"
Write-Host ""

$inbound | ForEach-Object {
    $rule = $_
    $filter = $rule | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
    $addrFilter = $rule | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue
    [PSCustomObject]@{
        规则名     = $rule.DisplayName.Substring(0, [Math]::Min(40, $rule.DisplayName.Length))
        协议       = if ($filter.Protocol) { $filter.Protocol } else { '任意' }
        本地端口   = if ($filter.LocalPort) { $filter.LocalPort -join ',' } else { '任意' }
        来源地址   = if ($addrFilter.RemoteAddress) { ($addrFilter.RemoteAddress -join ',').Substring(0, [Math]::Min(30, ($addrFilter.RemoteAddress -join ',').Length)) } else { '任意' }
        动作       = $rule.Action
    }
} | Select-Object -First 30 | Format-Table -AutoSize
```

</details>

### 21.2 高危规则检测（Any → Any / 暴露全端口）

<details>
<summary>📋 展开查看命令 — 高危防火墙规则扫描</summary>

```powershell
Write-Host "════════ 高危防火墙规则扫描 ════════"
$risks = @()

Get-NetFirewallRule -Direction Inbound -Action Allow -Enabled True -ErrorAction SilentlyContinue | ForEach-Object {
    $rule = $_
    $portFilter = $rule | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
    $addrFilter  = $rule | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue

    $anyPort = ($portFilter.LocalPort -eq 'Any' -or -not $portFilter.LocalPort)
    $anyAddr = ($addrFilter.RemoteAddress -eq 'Any' -or $addrFilter.RemoteAddress -contains 'Any' -or -not $addrFilter.RemoteAddress)

    if ($anyPort -and $anyAddr) {
        $risks += [PSCustomObject]@{
            风险等级 = '🔴 高危'
            规则名   = $rule.DisplayName
            说明     = '允许任意来源访问任意端口'
            建议     = '收紧来源地址或端口范围'
        }
    } elseif ($anyAddr) {
        # 检查是否暴露高危端口（135/445/3389/5985）
        $dangerousPorts = @('135','445','3389','5985','5986','23','21','1433','3306','6379')
        $portStr = ($portFilter.LocalPort -join ',')
        foreach ($p in $dangerousPorts) {
            if ($portStr -match "\b$p\b" -or $anyPort) {
                $risks += [PSCustomObject]@{
                    风险等级 = '⚠️ 中危'
                    规则名   = $rule.DisplayName
                    说明     = "端口 $p 对任意来源开放"
                    建议     = '限制来源 IP 白名单'
                }
                break
            }
        }
    }
}

if ($risks.Count -gt 0) {
    $risks | Format-Table -AutoSize -Wrap
    Write-Host "`n建议: 使用「来源 IP 白名单」替代「任意来源」"
} else {
    Write-Host "✅ 未发现明显高危防火墙规则"
}
```

</details>

### 21.3 按端口查看谁在放行

<details>
<summary>📋 展开查看命令 — 指定端口放行规则</summary>

```powershell
# 修改此处为你想查询的端口
$targetPorts = @('3389', '445', '80', '443', '1433', '3306')

Write-Host "════════ 关键端口放行规则 ════════"
foreach ($port in $targetPorts) {
    $rules = Get-NetFirewallRule -Direction Inbound -Action Allow -Enabled True -ErrorAction SilentlyContinue | Where-Object {
        $pf = $_ | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
        ($pf.LocalPort -eq 'Any' -or $pf.LocalPort -contains $port)
    }

    if ($rules) {
        Write-Host "`n  端口 $port — 有 $(($rules | Measure-Object).Count) 条放行规则:"
        $rules | Select-Object -First 5 @{N='规则名';E={$_.DisplayName}} |
            ForEach-Object { Write-Host "    - $($_.规则名)" }
    } else {
        Write-Host "`n  端口 $port — 无放行规则（默认拒绝）"
    }
}
```

</details>

### 21.4 防火墙配置文件状态

<details>
<summary>📋 展开查看命令 — 防火墙整体状态</summary>

```powershell
Write-Host "════════ 防火墙配置文件状态 ════════"
Get-NetFirewallProfile | Select-Object @{N='配置文件';E={$_.Name}},
    @{N='是否启用';E={if($_.Enabled){'✅ 启用'}else{'❌ 已禁用 ⚠️'}}},
    @{N='入站默认';E={$_.DefaultInboundAction}},
    @{N='出站默认';E={$_.DefaultOutboundAction}},
    @{N='通知';E={$_.NotifyOnListen}} |
    Format-Table -AutoSize

Write-Host "`n💡 防火墙应对所有配置文件均启用，入站默认「Block」"
Write-Host "💡 如果任一配置文件显示「已禁用」，立即排查原因"
```

</details>

**风险等级**：🟢 无（只读审计，不修改任何规则）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-NetFirewallRule` 报错 | 需管理员权限 | 管理员身份执行 |
| `WinRM` 相关报错 | 防火墙服务异常 | 检查 `mpssvc` 服务状态 |
| `Access denied on Get-NetFirewallPortFilter` | 域策略限制 | 以域管理员身份执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 防火墙被关闭（Enabled=False） | 极高风险，任何连接均可进入 |
| 3389 对 Any 开放 | RDP 暴力破解首要目标 |
| 445 对 Any 开放 | WannaCry/勒索病毒入侵路径 |
| 大量"Any → Any"规则 | 常见于软件安装时自动添加，需逐条清理 |

---

## 🆕 模块 22：关键服务崩溃与自动恢复状态

**用途**：查看服务异常停止记录、自动恢复策略、"应该运行却未运行"的服务。

**常你说**：`"哪些服务崩过"` / `"服务崩溃记录"` / `"服务自动恢复设置"` / `"有服务没跑起来吗"`

> ⚠️ **本模块仅读，不会启动、停止或修改任何服务。**

### 22.1 已停止但设为自动启动的服务（"应跑未跑"）

<details>
<summary>📋 展开查看命令 — 应运行却已停止的服务</summary>

```powershell
Write-Host "════════ 应运行却已停止的服务 ════════"
$deadServices = Get-Service | Where-Object {
    $_.StartType -in @('Automatic', 'AutomaticDelayedStart') -and
    $_.Status -eq 'Stopped'
}

if ($deadServices) {
    $deadServices | Select-Object @{N='服务名';E={$_.Name}},
        @{N='显示名';E={$_.DisplayName}},
        @{N='启动类型';E={$_.StartType}},
        @{N='状态';E={$_.Status}} |
        Sort-Object 显示名 |
        Format-Table -AutoSize
    Write-Host "`n⚠️ 以上服务设置了自动启动但当前已停止，需要排查原因"
} else {
    Write-Host "✅ 所有自动启动的服务均在运行"
}
```

</details>

### 22.2 服务崩溃事件记录（事件日志 7034/7036）

<details>
<summary>📋 展开查看命令 — 服务崩溃事件</summary>

```powershell
Write-Host "════════ 服务崩溃记录（最近 7 天）════════"
$events = Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    Id        = @(7034, 7035, 7036, 7031, 7040)
    StartTime = (Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue

if ($events) {
    $events | Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='事件ID';E={$_.Id}},
        @{N='说明';E={
            switch ($_.Id) {
                7034 { "❌ 服务意外停止: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(80,$_.Message.Length)) }
                7031 { "❌ 服务停止后触发恢复动作: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7035 { "→ 服务控制: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7036 { "● 服务状态变更: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7040 { "⚙️ 启动类型变更: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                default { $_.Message.Substring(0,[Math]::Min(80,$_.Message.Length)) }
            }
        }} |
        Where-Object { $_.事件ID -in @(7034, 7031) } |
        Sort-Object 时间 -Descending |
        Select-Object -First 20 |
        Format-Table -AutoSize -Wrap
} else {
    Write-Host "✅ 最近 7 天无服务崩溃记录"
}
```

</details>

### 22.3 服务自动恢复策略查看

<details>
<summary>📋 展开查看命令 — 服务故障恢复配置</summary>

```powershell
Write-Host "════════ 关键服务恢复策略 ════════"
$keyServices = @(
    'W3SVC',       # IIS
    'MSSQLSERVER', # SQL Server
    'WSearch',     # Windows Search
    'Spooler',     # 打印机
    'EventLog',    # 事件日志
    'WinRM',       # 远程管理
    'Schedule',    # 计划任务
    'LanmanServer' # 文件共享
)

foreach ($svcName in $keyServices) {
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if ($svc) {
        # 使用 sc.exe 读取恢复策略
        $scOutput = sc.exe qfailure $svcName 2>&1
        $resetPeriod = ($scOutput | Select-String 'RESET_PERIOD') -replace '.*: ', ''
        $actions = ($scOutput | Select-String 'FAILURE_ACTIONS') -replace '.*: ', ''

        Write-Host "  $($svc.DisplayName) [$svcName]"
        Write-Host "    状态: $($svc.Status)"
        Write-Host "    恢复动作: $(if($actions){$actions}else{'(未配置)'} )"
        Write-Host ""
    }
}
Write-Host "💡 未配置恢复动作的关键服务，崩溃后不会自动重启，需手动干预"
```

</details>

### 22.4 服务依赖关系检查（关键服务是否有依赖未启动）

<details>
<summary>📋 展开查看命令 — 服务依赖链检查</summary>

```powershell
Write-Host "════════ 关键服务依赖链检查 ════════"
$keyServices = @('W3SVC', 'MSSQLSERVER', 'WinRM', 'Schedule', 'Netlogon')

foreach ($svcName in $keyServices) {
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if ($svc) {
        $deps = $svc.ServicesDependedOn
        $brokenDeps = $deps | Where-Object { $_.Status -ne 'Running' }

        if ($brokenDeps) {
            Write-Host "⚠️ $($svc.DisplayName) 依赖以下未运行的服务:"
            $brokenDeps | ForEach-Object {
                Write-Host "    ❌ $($_.Name) ($($_.Status))"
            }
        } else {
            Write-Host "✅ $($svc.DisplayName) — 所有依赖服务正常"
        }
    }
}
```

</details>

**风险等级**：🟢 无（只读，不启动/停止/修改任何服务）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-WinEvent` 无权限 | 需管理员权限 | 管理员身份执行 |
| `sc.exe qfailure` 返回空 | 部分服务无恢复策略 | 正常，说明未配置 |
| `Get-Service` 找不到服务 | 该服务未安装 | 跳过该服务 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| IIS 停止但事件日志无崩溃记录 | 可能是被人为停止 |
| 服务崩溃但无恢复动作 | 需通过"服务属性 → 恢复"配置自动重启 |
| 依赖服务未运行导致主服务无法启动 | 先启动依赖服务 |
| 事件 7034 大量重复 | 服务反复崩溃重启，存在底层问题 |

---

## 前置要求与依赖

| 需求 | 说明 | 检测方法 |
|-----|------|---------|
| PowerShell 5.1+ | Windows 自带 | `$PSVersionTable.PSVersion` |
| 管理员权限 | IIS/清理/安全审计需要 | 自动检测（见下方） |
| WebAdministration | IIS 管理可选 | `Install-WindowsFeature Web-Mgmt-Tools` |
| 执行策略 | 可能需调整 | `Set-ExecutionPolicy RemoteSigned` |
| 存储诊断模块 | 磁盘健康检测需要 | `Get-PhysicalDisk` 可用 |
| Winmgmt (WMI) | 系统事件/会话监控需要 | `Get-CimInstance` 可用 |

**管理员权限自动检测**：
```powershell
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️ 非管理员运行，部分功能受限"
    Write-Host "  → 右键 PowerShell → 以管理员身份运行"
}
```

---

## ❓ 常见问题

### Q1: 第一次使用怎么做？
直接说 `"帮我扫一下 C 盘"` 或 `"检查服务状态"`。

### Q2: 英文报错看不懂怎么办？
粘贴报错内容，AI 会翻译并给出解法。每个模块也有"报错与解决"表格。

### Q3: 会不会删坏系统？
三层保护：系统目录不可操作、删除前先确认、回收站 API 可恢复。

### Q4: 要联网或付费吗？
全程离线、零依赖、零费用。

### Q5: Windows Update 清理会不会影响已安装的补丁？
不会。只清理未完成的下载缓存，已安装补丁不受影响。重新检查更新时会重新下载。

### Q6: 性能监控的数据能保留多久？
实时计数器只显示当前值。如需长期趋势，可让 AI 创建数据收集器（需确认），数据会保存到 `C:\PerfLogs`。

### Q7: 安全审计会被攻击者发现吗？
只读审计和导出操作不会产生额外日志。但性能计数器采集会占用少量系统资源。

### Q8: 注册表审计会不会误删系统关键项？
不会。模块 11 所有操作均为只读分析，绝不修改任何注册表键值。

### Q9: 磁盘健康检测会损伤磁盘吗？
不会。SMART 信息和错误计数均为只读读取，不会执行磁盘擦除或修复操作。

### Q10: 网络连接监控会不会泄露隐私？
不会。所有检测均在本地进行，不会将任何连接信息发送到外部。

### Q11: 事件日志会清除或修改吗？
不会。模块 14 仅读取日志内容，不会清除、修改或停止日志服务。

### Q12: 软件清单会篡改卸载程序吗？
不会。模块 15 仅读取注册表卸载键值，不会修改任何安装信息或卸载程序。

### Q13: 会话监控会踢出用户吗？
不会。模块 16 仅读取会话信息，不会结束、锁定或断开任何用户会话。

### Q14: 怎么升级 winskill？
```bash
clawhub update winskill
```

### Q15: 计划任务审计会删除任务吗？
不会。模块 17 所有操作均为只读审计，绝不会创建/删除/修改任何计划任务。

### Q16: 文件共享审计会断开连接吗？
不会。模块 18 仅读取共享配置和 SMB 会话信息，不会关闭共享或断开任何用户连接。

### Q17: DNS 缓存清空会断网吗？
不会。Clear-DnsClientCache 清空后会自动从 DNS 服务器重新获取解析记录。只在用户明确说「确认清空 DNS 缓存」后才执行。

### Q18: SSL 证书检测会申请或修改证书吗？
不会。模块 20 仅读取证书仓库和 IIS 绑定信息，不会申请、续签或删除任何证书。

### Q19: 防火墙规则审计会改动规则吗？
不会。模块 21 仅读取规则配置，不会新增、删除或修改任何防火墙规则。

### Q20: 服务崩溃检查会重启服务吗？
不会。模块 22 仅读取服务状态和事件日志，不会启动、停止或修改任何服务配置。

---

## 30 秒速查表

| 你说 | AI 执行 |
|-----|---------|
| `"扫 C 盘大文件"` | 模块 1 |
| `"找重复文件"` | 模块 2 |
| `"清理临时文件"` | 模块 3（需确认） |
| `"IIS 正常吗"` | 模块 4 |
| `"检查服务"` | 模块 5 |
| `"批量改名"` | 模块 6（需确认） |
| `"磁盘报告"` | 模块 7 |
| `"更新正常吗"` | 模块 8 |
| `"服务器卡"` | 模块 9 |
| `"有没有被入侵"` | 模块 10 |
| `"可疑启动项"` | 模块 11 |
| `"硬盘健康吗"` | 模块 12 |
| `"谁在连我"` | 模块 13 |
| `"系统日志错误"` | 模块 14 |
| `"装了什么软件"` | 模块 15 |
| `"谁在服务器上"` | 模块 16 |
| `"可疑计划任务"` | 模块 17 |
| `"共享文件夹"` | 模块 18 |
| `"DNS/网卡诊断"` | 模块 19 |
| `"SSL证书快到期了吗"` | 模块 20 |
| `"防火墙规则有没有漏洞"` | 模块 21 |
| `"哪些服务崩过"` | 模块 22 |

---

## ❌ 不支持（明确不能用的场景）

| 不支持 | 原因 |
|-------|------|
| 编辑已压缩的文件 | 压缩包内文件无法直接修改 |
| 恢复已删除的回收站文件 | 超出工具范围 |
| 修改注册表键值 | 风险过高，不在工具范围 |
| 远程管理其他服务器 | 需 WinRM/PowerShell Remoting |
| BIOS/硬件层操作 | 超出操作系统层面 |
| 磁盘修复/擦除 | 超出工具范围，需专业工具 |
| 终止网络连接 | 超出工具范围 |
| 清除/停止事件日志 | 超出工具范围，仅只读 |
| 卸载/安装软件 | 超出工具范围，只读审计 |
| 结束/断开用户会话 | 超出工具范围，只读监控 |
| 创建/删除计划任务 | 超出工具范围，只读审计 |
| 修改共享权限 | 超出工具范围，只读审计 |
| 修改网卡 IP/DNS 配置 | 超出工具范围，只读诊断 |
| 申请/续签/删除 SSL 证书 | 超出工具范围，只读检测 |
| 新增/删除/修改防火墙规则 | 超出工具范围，只读审计 |
| 启动/停止/修改服务配置 | 超出工具范围，只读诊断 |

---

## 前置要求

- **PowerShell 版本**：5.1+（Windows 自带，无需安装）
- **无需 API Key**
- **无需联网**（除首次安装 IIS 管理工具外）
- **无需安装任何第三方软件**
- ⚠️ **管理员权限检测**：部分功能（IIS 管理、更新缓存清理、安全审计、磁盘健康检测、网络监控、事件日志诊断、会话监控、计划任务审计、共享审计、DNS 网卡诊断、SSL 证书检测、防火墙审计、服务崩溃检查）需要管理员权限，AI 会在执行前自动检测并提示

## 发布信息

- **作者**：Admin
- **许可证**：MIT
- **支持**：Windows Server 2012+ / Windows 10/11
- **安全机制**：所有删除操作需用户确认，不用强制删除
- **TRACE 评测**：已通过评测，[查看详情](https://skillhub.cn/community/skills/winskill)
- **更新历史**：
  - v1.6.0：新增 SSL 证书过期检测、防火墙规则审计、服务崩溃恢复状态 3 个模块，总计 22 个模块
  - v1.5.0：新增计划任务审计、文件共享审计、DNS网卡诊断 3 个模块，总计 19 个模块
  - v1.4.0：新增事件日志诊断、已安装程序管理、用户会话监控 3 个模块，总计 16 个模块
  - v1.3.0：新增注册表启动项审计、磁盘健康检测、网络端口监控 3 个模块
  - v1.2.0：新增 Windows Update 性能监控 安全审计 3 个模块，所有命令折叠隐藏
  - v1.1.0：新增快速开始/报错指引/FAQ
  - v1.0.0：初始版本，7 个模块