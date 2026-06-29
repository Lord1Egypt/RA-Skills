---
name: winskill
description: "Windows 服务器运维工具箱 - 磁盘分析、临时文件清理、IIS 站点管理、批量文件操作、服务状态监控、Windows Update 诊断、实时性能监控、安全审计、注册表启动项审计、磁盘健康检测、网络端口监控、事件日志诊断、已安装程序管理、用户会话监控。只读分析+安全确认，绝不误删文件，完全免费离线运行。"
version: 1.4.0
---

# Winskill — Windows 服务器运维工具箱 v1.4.0

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

---

## 前置要求

- **PowerShell 版本**：5.1+（Windows 自带，无需安装）
- **无需 API Key**
- **无需联网**（除首次安装 IIS 管理工具外）
- **无需安装任何第三方软件**
- ⚠️ **管理员权限检测**：部分功能（IIS 管理、更新缓存清理、安全审计、磁盘健康检测、网络监控、事件日志诊断、会话监控）需要管理员权限，AI 会在执行前自动检测并提示

## 发布信息

- **作者**：Admin
- **许可证**：MIT
- **支持**：Windows Server 2012+ / Windows 10/11
- **安全机制**：所有删除操作需用户确认，不用强制删除
- **更新历史**：
  - v1.4.0：新增事件日志诊断、已安装程序管理、用户会话监控 3 个模块，总计 16 个模块
  - v1.3.0：新增注册表启动项审计、磁盘健康检测、网络端口监控 3 个模块
  - v1.2.0：新增 Windows Update 性能监控 安全审计 3 个模块，所有命令折叠隐藏
  - v1.1.0：新增快速开始/报错指引/FAQ
  - v1.0.0：初始版本，7 个模块
