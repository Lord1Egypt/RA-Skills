---
id: module-27
name: 自动化修复向导
description: 从"诊断"到"修复"，提供一键式常见问题修复，严格遵循「预览→确认→执行→验证」四步流程。
keywords: ['帮我修 DNS', '网络不正常', 'Windows Update 卡住', '服务起不来', '磁盘满了', '时间不准']
permission: admin
mode: confirm
subset: advanced
---

## 🆕 模块 27：自动化修复向导

**用途**：从"诊断"到"修复"，提供一键式常见问题修复，严格遵循「预览→确认→执行→验证」四步流程。

**常你说**：`"帮我修 DNS"` / `"网络不正常"` / `"Windows Update 卡住"` / `"服务起不来"` / `"磁盘满了"` / `"时间不准"`

> ⚠️ **本模块所有修复操作均需管理员权限，执行前自动创建还原点，用户明确确认后才执行。**

### 修复流程（所有子模块通用）

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Step 1     │ →  │  Step 2     │ →  │  Step 3     │ →  │  Step 4     │
│  问题定位    │    │  修复预览    │    │  用户确认    │    │  执行+验证   │
│ 调用现有模块 │    │ 展示命令+影响 │    │ 创建还原点   │    │ 重新诊断确认  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

### 27.1 DNS 解析异常修复

**修复命令**：`ipconfig /flushdns` + `netsh winsock reset`

**常你说**：`"DNS 修一下"` / `"网页打不开 DNS 问题"`

<details>
<summary>📋 展开查看命令 — DNS 修复四步流程</summary>

```powershell
# ====== Step 1: 问题定位（调用模块19） ======
Write-Host "════════ DNS 修复向导 ════════"
Write-Host "`n[Step 1] 问题定位..."
$dnsTest = Resolve-DnsName -Name www.baidu.com -ErrorAction SilentlyContinue
if ($dnsTest) {
    Write-Host "  ✅ DNS 解析正常，无需修复"
    return
}
Write-Host "  ❌ DNS 解析失败，需要修复"

# ====== Step 2: 修复预览 ======
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行以下命令："
Write-Host "  1. ipconfig /flushdns          — 清空 DNS 缓存"
Write-Host "  2. netsh winsock reset         — 重置 Winsock 目录"
Write-Host "  3. ipconfig /registerdns       — 重新注册 DNS 名称"
Write-Host "`n  影响范围："
Write-Host "  · 短暂断开网络连接（约 5-10 秒）"
Write-Host "  · 需要重启后生效"
Write-Host "  · 不会丢失任何数据"

# ====== Step 3: 用户确认 ======
Write-Host "`n[Step 3] 用户确认"
$confirm = Read-Host "  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') {
    Write-Host "  ❌ 已取消"
    return
}

# 创建还原点
Write-Host "  正在创建系统还原点..."
try {
    Checkpoint-Computer -Description "winskill-DNS修复前" -RestorePointType MODIFY_SETTINGS -ErrorAction SilentlyContinue
    Write-Host "  ✅ 还原点已创建"
} catch {
    Write-Host "  ⚠️ 无法创建还原点（系统保护可能未启用）"
}

# ====== Step 4: 执行修复 ======
Write-Host "`n[Step 4] 执行修复..."
Write-Host "  1/3 清空 DNS 缓存..."
ipconfig /flushdns
Write-Host "  2/3 重置 Winsock..."
netsh winsock reset
Write-Host "  3/3 注册 DNS..."
ipconfig /registerdns

# 验证
Write-Host "`n[验证] 重新测试 DNS..."
Start-Sleep -Seconds 3
$verifyDns = Resolve-DnsName -Name www.baidu.com -ErrorAction SilentlyContinue
if ($verifyDns) {
    Write-Host "  ✅ DNS 修复成功！"
} else {
    Write-Host "  ⚠️ DNS 仍无法解析，建议检查 DNS 服务器配置"
    Write-Host "  → 模块 19 查看 DNS 服务器配置"
}
```

</details>

**风险等级**：🟡 中（需确认，会短暂断网）

---

### 27.2 网络连接异常修复

**修复命令**：`netsh int ip reset` + 网卡禁用/启用

**常你说**：`"网络重置"` / `"网连不上"`

<details>
<summary>📋 展开查看命令 — 网络修复四步流程</summary>

```powershell
Write-Host "════════ 网络修复向导 ════════"

# Step 1: 定位
Write-Host "`n[Step 1] 问题定位..."
$pingTest = Test-NetConnection -ComputerName www.baidu.com -Port 443 -ErrorAction SilentlyContinue
if ($pingTest.TcpTestSucceeded) {
    Write-Host "  ✅ 网络连接正常"
    return
}
Write-Host "  ❌ 网络连接失败"

# Step 2: 预览
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行："
Write-Host "  1. netsh int ip reset           — 重置 TCP/IP 协议栈"
Write-Host "  2. 禁用再启用网卡               — 重新初始化网络适配器"
Write-Host "`n  影响：短暂断网（约 10-30 秒），需管理员权限"

# Step 3: 确认
$confirm = Read-Host "`n  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') { return }

# Step 4: 执行
Write-Host "`n[Step 4] 执行修复..."
netsh int ip reset
Write-Host "  ✅ TCP/IP 已重置"

# 获取主网卡
$adapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1
if ($adapter) {
    Write-Host "  重启网卡: $($adapter.Name)..."
    Disable-NetAdapter -Name $adapter.Name -Confirm:$false
    Start-Sleep -Seconds 3
    Enable-NetAdapter -Name $adapter.Name -Confirm:$false
    Write-Host "  ✅ 网卡已重启"
}

# 验证
Start-Sleep -Seconds 5
$verifyNet = Test-NetConnection -ComputerName www.baidu.com -Port 443 -ErrorAction SilentlyContinue
if ($verifyNet.TcpTestSucceeded) {
    Write-Host "`n  ✅ 网络修复成功！"
} else {
    Write-Host "`n  ⚠️ 仍未连通，检查物理连接和路由器"
}
```

</details>

**风险等级**：🟡 中（需确认，会短暂断网）

---

### 27.3 Windows Update 修复

**修复命令**：停服务 → 清理 SoftwareDistribution → 重启服务

**常你说**：`"Windows Update 修一下"` / `"更新卡住了"`

<details>
<summary>📋 展开查看命令 — Windows Update 修复四步流程</summary>

```powershell
Write-Host "════════ Windows Update 修复向导 ════════"

# Step 1: 定位
Write-Host "`n[Step 1] 问题定位..."
$wuService = Get-Service wuauserv -ErrorAction SilentlyContinue
if ($wuService.Status -eq 'Running') {
    Write-Host "  ✅ Windows Update 服务运行中"
} else {
    Write-Host "  ❌ Windows Update 服务已停止"
}

# Step 2: 预览
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行："
Write-Host "  1. Stop-Service wuauserv       — 停止更新服务"
Write-Host "  2. 清理 SoftwareDistribution   — 删除损坏的下载缓存"
Write-Host "  3. Start-Service wuauserv     — 重启更新服务"
Write-Host "`n  影响：正在进行的更新将中断，已安装补丁不受影响"

# Step 3: 确认
$confirm = Read-Host "`n  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') { return }

# Step 4: 执行
Write-Host "`n[Step 4] 执行修复..."
Write-Host "  1/3 停止更新服务..."
Stop-Service wuauserv -Force
Write-Host "  2/3 清理缓存..."
$sdPath = "C:\Windows\SoftwareDistribution\Download"
if (Test-Path $sdPath) {
    Remove-Item -Path "$sdPath\*" -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "  3/3 重启服务..."
Start-Service wuauserv

# 验证
Start-Sleep -Seconds 3
$verifyWu = Get-Service wuauserv
if ($verifyWu.Status -eq 'Running') {
    Write-Host "`n  ✅ Windows Update 服务已恢复正常"
} else {
    Write-Host "`n  ⚠️ 服务未启动，查看事件日志排查"
}
```

</details>

**风险等级**：🟡 中（需确认，正在进行的更新会中断）

---

### 27.4 服务启动失败修复

**修复命令**：检查依赖 → 检查端口 → 尝试启动

**常你说**：`"SQL Server 起不来"` / `"IIS 启动失败"`

<details>
<summary>📋 展开查看命令 — 服务修复四步流程</summary>

```powershell
# 替换为你要修复的服务名
$targetService = "W3SVC"  # ← 改成你要修复的服务名

Write-Host "════════ 服务修复向导 ════════"
Write-Host "目标服务: $targetService"

# Step 1: 定位
Write-Host "`n[Step 1] 问题定位..."
$svc = Get-Service -Name $targetService -ErrorAction SilentlyContinue
if (-not $svc) {
    Write-Host "  ❌ 服务不存在: $targetService"
    return
}
Write-Host "  状态: $($svc.Status)"
Write-Host "  启动类型: $($svc.StartType)"

# 检查依赖
$deps = $svc.ServicesDependedOn
$brokenDeps = $deps | Where-Object { $_.Status -ne 'Running' }
if ($brokenDeps) {
    Write-Host "  ⚠️ 依赖服务未运行:"
    $brokenDeps | ForEach-Object { Write-Host "    ❌ $($_.Name)" }
}

# Step 2: 预览
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行："
Write-Host "  1. 启动依赖服务（如有）"
Write-Host "  2. 检查端口占用"
Write-Host "  3. 尝试启动目标服务"

# Step 3: 确认
$confirm = Read-Host "`n  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') { return }

# Step 4: 执行
Write-Host "`n[Step 4] 执行修复..."

# 启动依赖
if ($brokenDeps) {
    foreach ($dep in $brokenDeps) {
        Write-Host "  启动依赖: $($dep.Name)..."
        try {
            Start-Service -Name $dep.Name -ErrorAction Stop
            Write-Host "    ✅ 已启动"
        } catch {
            Write-Host "    ❌ 启动失败: $($_.Exception.Message)"
        }
    }
}

# 检查端口（如果是 IIS/SQL/MySQL 等已知服务）
$portMap = @{
    'W3SVC' = 80
    'MSSQLSERVER' = 1433
    'MySQL80' = 3306
}
if ($portMap.ContainsKey($targetService)) {
    $port = $portMap[$targetService]
    $portUsed = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($portUsed) {
        $proc = Get-Process -Id $portUsed.OwningProcess -ErrorAction SilentlyContinue
        Write-Host "  ⚠️ 端口 $port 被占用: $($proc.Name)"
    }
}

# 尝试启动
Write-Host "  尝试启动 $targetService..."
try {
    Start-Service -Name $targetService -ErrorAction Stop
    Write-Host "  ✅ 服务启动成功！"
} catch {
    Write-Host "  ❌ 启动失败: $($_.Exception.Message)"
    Write-Host "  → 查看事件日志: 模块 14"
}

# 验证
$verifySvc = Get-Service -Name $targetService
Write-Host "`n[验证] 服务状态: $($verifySvc.Status)"
```

</details>

**风险等级**：🟡 中（需确认，会启动服务）

---

### 27.5 磁盘空间不足修复

**修复命令**：大文件识别 + 旧文件建议 + temp 清理

**常你说**：`"磁盘满了"` / `"C 盘清理"`

<details>
<summary>📋 展开查看命令 — 磁盘清理四步流程</summary>

```powershell
Write-Host "════════ 磁盘清理修复向导 ════════"

# Step 1: 定位
Write-Host "`n[Step 1] 问题定位..."
$vol = Get-Volume -DriveLetter C
$freeGB = [math]::Round($vol.SizeRemaining/1GB, 1)
$totalGB = [math]::Round($vol.Size/1GB, 1)
$usedPct = [math]::Round((1 - $vol.SizeRemaining/$vol.Size) * 100, 1)
Write-Host "  C 盘: ${freeGB} GB 可用 / ${totalGB} GB 总计 (已用 ${usedPct}%)"

if ($freeGB -gt 10) {
    Write-Host "  ✅ 磁盘空间充足"
    return
}
Write-Host "  ⚠️ 磁盘空间不足"

# Step 2: 预览
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行："
Write-Host "  1. 扫描大文件（>100MB）"
Write-Host "  2. 扫描旧文件（>30 天）"
Write-Host "  3. 清理临时文件（>7 天）"
Write-Host "  4. 清空回收站"
Write-Host "`n  影响：清理临时文件不可恢复，大文件仅建议不自动删除"

# Step 3: 确认
$confirm = Read-Host "`n  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') { return }

# Step 4: 执行
Write-Host "`n[Step 4] 执行清理..."

# 清理临时文件
$tempPath = $env:TEMP
$cutoff = (Get-Date).AddDays(-7)
$tempFiles = Get-ChildItem -Path $tempPath -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $cutoff }
$tempKB = ($tempFiles | Measure-Object -Property Length -Sum).Sum
$tempCount = $tempFiles.Count
Write-Host "  清理临时文件: $tempCount 个文件，释放 $([math]::Round($tempKB/1MB,1)) MB"
foreach ($f in $tempFiles) {
    try { Remove-Item $f.FullName -Force -ErrorAction SilentlyContinue } catch {}
}

# 清空回收站
$shell = New-Object -ComObject Shell.Application
$rb = $shell.NameSpace(0x0a)
$rbItems = @($rb.Items())
if ($rbItems.Count -gt 0) {
    Write-Host "  清空回收站: $($rbItems.Count) 个项目"
    $rbItems | ForEach-Object { Remove-Item $_.Path -Recurse -Force -ErrorAction SilentlyContinue }
}

# 验证
$volAfter = Get-Volume -DriveLetter C
$freeAfter = [math]::Round($volAfter.SizeRemaining/1GB, 1)
Write-Host "`n[验证] 清理后 C 盘可用: ${freeAfter} GB（释放 $([math]::Round($freeAfter - $freeGB, 1)) GB）"
```

</details>

**风险等级**：🟡 中（需确认，清理临时文件不可恢复）

---

### 27.6 时间不同步修复

**修复命令**：`w32tm /resync`

**常你说**：`"时间不准"` / `"时间同步"`

<details>
<summary>📋 展开查看命令 — 时间同步四步流程</summary>

```powershell
Write-Host "════════ 时间同步修复向导 ════════"

# Step 1: 定位
Write-Host "`n[Step 1] 问题定位..."
$localTime = Get-Date
$ntpTime = $null

# 尝试从 NTP 服务器获取时间
try {
    $tcp = New-Object System.Net.Sockets.TcpClient("time.windows.com", 123)
    $stream = $tcp.GetStream()
    $data = New-Object byte[] 48
    $stream.Read($data, 0, 48) | Out-Null
    $stream.Close()
    $tcp.Close()
    # 简化：直接用 w32tm 查询
    $ntpTime = (w32tm /stripchart /computer:time.windows.com /samples:1 /dataonly 2>$null | Select-Object -Last 1)
} catch {}

$w32tmStatus = w32tm /query /status 2>$null
if ($w32tmStatus) {
    Write-Host "  Windows Time 服务状态:"
    $w32tmStatus | Select-Object -First 5 | ForEach-Object { Write-Host "  $_" }
}

# Step 2: 预览
Write-Host "`n[Step 2] 修复预览"
Write-Host "  将要执行："
Write-Host "  1. w32tm /resync           — 强制同步时间"
Write-Host "  2. w32tm /query /status   — 验证同步结果"
Write-Host "`n  影响：无风险，时间同步不会丢失数据"

# Step 3: 确认
$confirm = Read-Host "`n  输入 '确认修复' 开始执行"
if ($confirm -ne '确认修复') { return }

# Step 4: 执行
Write-Host "`n[Step 4] 执行时间同步..."
w32tm /resync 2>$null
Start-Sleep -Seconds 2

# 验证
Write-Host "`n[验证] 同步结果:"
$verifyTime = w32tm /query /status 2>$null
if ($verifyTime) {
    $verifyTime | Select-Object -First 5 | ForEach-Object { Write-Host "  $_" }
    Write-Host "`n  ✅ 时间同步完成"
} else {
    Write-Host "  ⚠️ 同步状态未知，稍后重试"
}
```

</details>

**风险等级**：🟢 低（无风险，仅同步时间）

---

**风险等级汇总**：

| 子模块 | 风险 | 说明 |
|--------|------|------|
| 27.1 DNS 修复 | 🟡 中 | 短暂断网 5-10 秒 |
| 27.2 网络修复 | 🟡 中 | 短暂断网 10-30 秒 |
| 27.3 WinUpdate 修复 | 🟡 中 | 正在进行的更新会中断 |
| 27.4 服务修复 | 🟡 中 | 会启动服务 |
| 27.5 磁盘清理 | 🟡 中 | 临时文件不可恢复 |
| 27.6 时间同步 | 🟢 低 | 无风险 |

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access denied` | 需要管理员权限 | 以管理员身份运行 |
| `Service cannot be started` | 服务启动失败 | 检查依赖和端口 |
| `Network reset failed` | 网卡重置失败 | 手动禁用/启用网卡 |
| `w32tm error` | 时间服务未运行 | 启动 W32Time 服务 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 修复后问题依旧 | 查看对应诊断模块的详细日志 |
| 无法创建还原点 | 系统保护未启用，不影响修复操作 |
| 服务启动后立即停止 | 检查事件日志，可能是程序崩溃 |
| 磁盘清理后空间未增加 | 可能是系统还原点占用，清理旧还原点 |


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



---

## ⚡ 性能优化（硬件自适应）

> **设计原则：绝不拖累用户电脑。** 所有扫描/采集任务均根据用户电脑硬件配置自动调整线程数和资源占用。

### 自动硬件检测

| 检测项 | 用途 | 自适应策略 |
|--------|------|-----------|
| CPU 核心数 | 决定并行任务数 | ≤4 核：单线程；8 核：2 线程；16+ 核：4 线程 |
| 物理内存 | 决定是否启用内存缓存 | ≤4 GB：禁用缓存；8 GB：小缓存；16+ GB：正常缓存 |
| 磁盘类型 | 决定是否启用 I/O 优先级 | HDD：低优先级 I/O；SSD：正常优先级 |
| 系统负载 | 决定是否延迟启动 | CPU >80% 时延迟 5 秒后执行 |

### 各模块自适应规则

| 模块 | 自适应行为 |
|------|-----------|
| 模块 1（磁盘扫描） | 根据 CPU 核心数自动分配扫描线程数，HDD 自动降低 I/O 优先级 |
| 模块 2（重复文件） | 大文件自动分批处理，避免内存溢出 |
| 模块 3（临时文件） | 扫描时自动跳过正在使用的文件 |
| 模块 9（性能监控） | 采集间隔根据 CPU 负载动态调整（1-5 秒） |
| 模块 12（磁盘健康） | 检测时自动限制并发 I/O，避免影响业务 |
| 模块 13（网络监控） | 连接数采集分批进行，避免一次性占用过多资源 |

### 性能保护命令示例

```powershell
# 自动检测硬件并设置线程数
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$totalRAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB, 1)
$diskType = (Get-PhysicalDisk | Select-Object -First 1).MediaType

$threadCount = switch ($cpuCores) {
    { $_ -le 4 } { 1 }
    { $_ -le 8 } { 2 }
    default { 4 }
}

$ioPriority = if ($diskType -eq 'HDD') { 'Low' } else { 'Normal' }

Write-Host "硬件检测: $cpuCores 核 CPU, ${totalRAM} GB RAM, 磁盘: $diskType"
Write-Host "自动设置: $threadCount 线程, I/O 优先级: $ioPriority"
```

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
skillhub upgrade winskill
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

### Q23: SFC 和 DISM 有什么区别？
SFC 修复单个系统文件，DISM 修复组件存储（SFC 的源）。建议先 DISM 修复组件存储，再 SFC 修复系统文件。

### Q24: 存储池的 RAID 类型如何选择？
Mirror（镜像）提供冗余，Parity（奇偶校验）提供更高存储效率。生产环境推荐 Mirror。

### Q25: 备份失败了怎么查原因？
检查 Windows 事件查看器 → Applications and Services Logs → Microsoft → Windows → Backup → Operational。

### Q26: Docker 功能需要额外安装吗？
模块 26 使用 Windows 系统自带的 `docker` 和 `kubectl` 命令行工具。Windows Server 2016+ 支持 Docker，但需要手动安装。未安装 Docker/kubectl 时模块 26 给出安装指引，不会报错。

### Q27: 性能基线采集会不会拖慢服务器？
不会。模块 28 根据 CPU 核心数动态调整采集频率（≤4 核每 15 分钟一次，>4 核每 5 分钟一次），单次采集耗时 <1 秒，内存占用 <10MB。

### Q28: 合规检查会修改系统配置吗？
不会。模块 29 所有检查项均为只读检测，仅输出合规/不合规判定和修复建议，不会修改任何系统配置。

### Q29: 远程管理需要开启 WinRM 服务吗？
是的。模块 30 基于 PowerShell Remoting（WinRM），目标服务器需要开启 WinRM 服务（`Enable-PSRemoting`）。模块 30.1 包含一键开启 WinRM 的命令。

### Q30: 远程管理支持非域环境吗？
支持。模块 30 支持域环境和非域环境，非域环境需配置 TrustedHosts 并使用 IP 地址连接。

---

<a name="module-28"></a>

