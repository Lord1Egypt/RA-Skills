---
id: module-30
name: 远程多服务器管理
description: 远程多服务器管理
keywords: ['远程多服务器管理']
permission: admin
mode: confirm
subset: advanced
---

## 🆕 模块 30：远程多服务器管理

> ⚠️ **本模块需要 WinRM 服务支持，所有操作需管理员权限。**

<details>
<summary>📋 展开查看：模块 30：远程多服务器管理</summary>

### 30.1 服务器注册（Windows Credential Manager）

```powershell
# 服务器注册配置文件
$serverFile = "$env:USERPROFILE\.workbuddy\output\winskill\servers.json"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.workbuddy\output\winskill" | Out-Null

# 加载已有服务器列表
$servers = @()
if (Test-Path $serverFile) {
    $servers = Get-Content $serverFile -Raw | ConvertFrom-Json
}

Write-Host "`n🖥️ 远程服务器管理"
Write-Host ("=" * 50)
Write-Host "1. 添加服务器"
Write-Host "2. 查看已注册服务器"
Write-Host "3. 删除服务器"
Write-Host "4. 测试连接"
Write-Host ("=" * 50)

# 示例：添加服务器（实际使用时通过 AI 交互输入）
$action = Read-Host "请选择操作 (1-4)"

switch ($action) {
    "1" {
        $ip = Read-Host "服务器 IP 或主机名"
        $user = Read-Host "用户名（如 Administrator）"
        $auth = Read-Host "认证方式 (1=密码 2=证书)"
        
        if ($auth -eq "1") {
            $cred = Get-Credential -Message "输入 $ip 的凭据"
            # 保存到 Windows Credential Manager（通过 cmdkey）
            $target = "TERMSRV/$ip"
            cmdkey /generic:$target /user:$($cred.UserName) /pass:$($cred.GetNetworkCredential().Password) 2>$null
            Write-Host "✅ 凭据已保存到 Windows Credential Manager"
        }
        
        $newServer = @{
            ip = $ip
            user = $user
            addedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            tags = @()
        }
        $servers += $newServer
        $servers | ConvertTo-Json -Depth 3 | Out-File $serverFile -Encoding utf8
        Write-Host "✅ 服务器 $ip 已注册"
    }
    "2" {
        if ($servers.Count -eq 0) {
            Write-Host "⚠️ 暂无已注册服务器"
        } else {
            Write-Host "`n已注册服务器："
            $servers | ForEach-Object { Write-Host "  - $($_.ip)（$($_.user)）添加于 $($_.addedAt)" }
        }
    }
    "3" {
        $ip = Read-Host "要删除的服务器 IP"
        $servers = $servers | Where-Object ip -ne $ip
        $servers | ConvertTo-Json -Depth 3 | Out-File $serverFile -Encoding utf8
        Write-Host "✅ 服务器 $ip 已删除"
    }
    "4" {
        $ip = Read-Host "要测试的服务器 IP"
        $result = Test-WSMan -ComputerName $ip -ErrorAction SilentlyContinue
        if ($result) {
            Write-Host "✅ $ip WinRM 服务正常"
        } else {
            Write-Host "❌ $ip 无法连接，请检查："
            Write-Host "  1. 目标服务器是否开启 WinRM（Enable-PSRemoting）"
            Write-Host "  2. 防火墙是否放行 5985/5986 端口"
            Write-Host "  3. 网络是否可达"
        }
    }
}
```

### 30.2 批量命令执行（并行）

```powershell
$serverFile = "$env:USERPROFILE\.workbuddy\output\winskill\servers.json"

if (-not (Test-Path $serverFile)) {
    Write-Host "❌ 暂无已注册服务器，请先运行 30.1 注册"
    exit 1
}

$servers = Get-Content $serverFile -Raw | ConvertFrom-Json

if ($servers.Count -eq 0) {
    Write-Host "⚠️ 暂无已注册服务器"
    exit 1
}

# 硬件自适应：并行数 = min(CPU 核心数, 服务器数量)
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$maxParallel = [Math]::Min($cpuCores, $servers.Count)
Write-Host ("`n⚡ 并行执行：{0} 个任务同时运行（CPU {1} 核）" -f $maxParallel, $cpuCores)

# 要执行的命令
$command = Read-Host "要在所有服务器执行的命令"

Write-Host ("`n在 {0} 台服务器上执行：{1}" -f $servers.Count, $command)
Write-Host ("-" * 60)

# PowerShell 5.1 兼容：使用 Invoke-Command 并行执行（原生支持多计算机）
$computerNames = $servers.ip
$cred = Get-Credential -Message "输入所有服务器的通用凭据"

Write-Host ("`n在 {0} 台服务器上执行：{1}" -f $servers.Count, $command)
Write-Host ("-" * 60)

try {
    # Invoke-Command 原生支持多计算机并行执行
    $results = Invoke-Command -ComputerName $computerNames -Credential $cred -ScriptBlock {
        param($cmd)
        $output = Invoke-Expression $cmd 2>&1
        [PSCustomObject]@{
            Server = $env:COMPUTERNAME
            Status = "✅ 成功"
            Output = $output | Out-String
        }
    } -ArgumentList $command -ErrorAction Stop
    
    # 汇总结果
    Write-Host ("`n" + "=" * 60)
    Write-Host "📊 执行结果汇总："
    $results | ForEach-Object {
        Write-Host ("`n[{0}] {1}" -f $_.Server, $_.Status)
        if ($_.Output) { Write-Host $_.Output }
    }
    Write-Host ("=" * 60)
} catch {
    Write-Host ("❌ 执行失败：{0}" -f $_.Exception.Message)
    Write-Host "提示：确认所有服务器都已开启 WinRM（运行 Enable-PSRemoting -Force）"
}
```

### 30.3 统一监控面板

```powershell
$serverFile = "$env:USERPROFILE\.workbuddy\output\winskill\servers.json"

if (-not (Test-Path $serverFile)) {
    Write-Host "❌ 暂无已注册服务器"
    exit 1
}

$servers = Get-Content $serverFile -Raw | ConvertFrom-Json

Write-Host "`n📊 多服务器统一监控面板"
Write-Host ("=" * 80)
Write-Host ("{0,-20} {1,8} {2,8} {3,8} {4,10} {5,10}" -f "服务器", "CPU%", "内存%", "磁盘%", "状态", "运行时间")
Write-Host ("-" * 80)

foreach ($server in $servers) {
    try {
        $session = New-PSSession -ComputerName $server.ip -ErrorAction Stop
        $info = Invoke-Command -Session $session -ScriptBlock {
            $cpu = (Get-CimInstance Win32_Processor).LoadPercentage
            $mem = (Get-CimInstance Win32_OperatingSystem)
            $memPct = [math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize * 100, 1)
            $disk = (Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object DeviceID -eq 'C:')
            $diskPct = [math]::Round(($disk.Size - $disk.FreeSpace) / $disk.Size * 100, 1)
            $uptime = (Get-Date) - $mem.LastBootUpTime
            [PSCustomObject]@{
                CPU = $cpu
                Mem = $memPct
                Disk = $diskPct
                Uptime = "{0}天{1}小时" -f $uptime.Days, $uptime.Hours
            }
        }
        Remove-PSSession $session
        
        $statusEmoji = if ($info.CPU -ge 90 -or $info.Mem -ge 90 -or $info.Disk -ge 90) { "🔴" } elseif ($info.CPU -ge 70 -or $info.Mem -ge 70 -or $info.Disk -ge 70) { "🟡" } else { "🟢" }
        
        Write-Host ("{0,-20} {1,8} {2,8} {3,8} {4,10} {5,10}" -f $server.ip, "$($info.CPU)%", "$($info.Mem)%", "$($info.Disk)%", $statusEmoji, $info.Uptime)
    } catch {
        Write-Host ("{0,-20} {1,8} {2,8} {3,8} {4,10} {5,10}" -f $server.ip, "-", "-", "-", "❌ 离线", "-")
    }
}

Write-Host ("-" * 80)
Write-Host "图例：🟢 正常  🟡 警告  🔴 严重  ❌ 离线"
Write-Host ("=" * 80)
```

### 30.4 配置差异对比

```powershell
$serverFile = "$env:USERPROFILE\.workbuddy\output\winskill\servers.json"

if (-not (Test-Path $serverFile)) {
    Write-Host "❌ 暂无已注册服务器"
    exit 1
}

$servers = Get-Content $serverFile -Raw | ConvertFrom-Json

if ($servers.Count -lt 2) {
    Write-Host "⚠️ 至少需要 2 台服务器才能对比"
    exit 1
}

Write-Host "`n🔍 配置差异对比"
Write-Host ("=" * 60)

# 选择对比项目
Write-Host "对比项目："
Write-Host "1. IIS 站点配置"
Write-Host "2. 服务状态"
Write-Host "3. 防火墙规则"
Write-Host "4. 已安装补丁"
$choice = Read-Host "请选择 (1-4)"

$scriptBlock = switch ($choice) {
    "1" { { Get-Website | Select-Object Name, State, PhysicalPath, Bindings | ConvertTo-Json } }
    "2" { { Get-Service | Where-Object Status -ne 'Running' | Select-Object Name, Status, StartType | ConvertTo-Json } }
    "3" { { Get-NetFirewallRule | Where-Object Enabled -eq 'True' | Select-Object DisplayName, Direction, Action | ConvertTo-Json } }
    "4" { { Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10 HotFixID, InstalledOn | ConvertTo-Json } }
}

# 采集所有服务器数据
$allData = @{}
foreach ($server in $servers) {
    try {
        $session = New-PSSession -ComputerName $server.ip -ErrorAction Stop
        $data = Invoke-Command -Session $session -ScriptBlock $scriptBlock
        $allData[$server.ip] = $data | ConvertFrom-Json
        Remove-PSSession $session
    } catch {
        Write-Host "⚠️ $($server.ip) 连接失败：$($_.Exception.Message)"
    }
}

# 对比输出
if ($allData.Count -ge 2) {
    $firstServer = $allData.Keys | Select-Object -First 1
    $firstData = $allData[$firstServer]
    
    Write-Host ("`n基准服务器：$firstServer" -f $firstServer)
    Write-Host ("-" * 60)
    
    foreach ($server in $allData.Keys) {
        if ($server -eq $firstServer) { continue }
        $serverData = $allData[$server]
        
        # 简单差异对比（基于 JSON 字符串比较）
        $firstJson = $firstData | ConvertTo-Json -Compress
        $serverJson = $serverData | ConvertTo-Json -Compress
        
        if ($firstJson -eq $serverJson) {
            Write-Host ("✅ {0}：与基准一致" -f $server)
        } else {
            Write-Host ("⚠️ {0}：存在差异" -f $server)
            # 输出具体差异（简化版）
            Write-Host ("  基准项数：{0}，对比项数：{1}" -f @($firstData).Count, @($serverData).Count)
        }
    }
}

Write-Host ("=" * 60)
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `WinRM 客户端无法处理请求` | 目标 WinRM 未开启 | 在目标服务器运行 `Enable-PSRemoting -Force` |
| `访问被拒绝` | 凭据错误或权限不足 | 检查用户名密码，确认用户有远程管理权限 |
| `无法连接到远程服务器` | 网络不通或防火墙拦截 | 检查网络连通性和 5985/5986 端口 |
| `New-PSSession 超时` | 服务器响应慢或网络延迟高 | 增加 `-OperationTimeout` 参数 |
| `TrustedHosts 未配置` | 非域环境需配置 TrustedHosts | `Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.0/24" -Concatenate` |

</details>


[↑ 返回顶部](#module-1)

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
| `"系统文件修复"` | 模块 23 |
| `"存储池状态"` | 模块 24 |
| `"备份正常吗"` | 模块 25 |
| `"Docker 状态"` | 模块 26 |
| `"帮我修 DNS"` | 模块 27 |
| `"性能趋势"` | 模块 28 |
| `"合规检查"` | 模块 29 |
| `"远程服务器"` | 模块 30 |

---

## ❌ 不支持（明确不能用的场景）

| 不支持 | 原因 |
|-------|------|
| 编辑已压缩的文件 | 压缩包内文件无法直接修改 |
| 恢复已删除的回收站文件 | 超出工具范围 |
| 修改注册表键值 | 风险过高，不在工具范围 |
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
- ⚠️ **管理员权限检测**：部分功能（IIS 管理、更新缓存清理、安全审计、磁盘健康检测、网络监控、事件日志诊断、会话监控、计划任务审计、共享审计、DNS 网卡诊断、SSL 证书检测、防火墙审计、服务崩溃检查、性能基线采集、合规检查、远程多服务器管理）需要管理员权限，AI 会在执行前自动检测并提示

## 更新日志

| v3.1.0 | 2026-08-16 | 新增日志轮转功能（Write-WinskillLog，10MB/7天自动轮转清理）；新增模块索引命令（一键列出30个模块用途）；改进：移除废弃的 wmic 声明（已全面迁移 CIM cmdlet） |
| v3.0.0 | 2026-08-06 | 新增性能基线与趋势分析模块（基线建立、异常偏离告警、趋势预测、瓶颈关联分析）、安全合规检查清单模块（等保2.0、CIS Benchmark、合规报告、修复建议）、远程多服务器管理模块（服务器注册、批量命令执行、统一监控面板、配置差异对比），总计30个模块，从单机工具升级为多机管理平台；修改展示方式：顶部模块导航锚点+每模块返回顶部链接 |
| v2.0.0 | 2026-07-24 | 新增自动化修复向导模块（DNS修复、网络修复、WinUpdate修复、服务修复、磁盘清理、时间同步），总计27个模块，从诊断工具升级为修复工具 |
| v1.9.0 | 2026-07-16 | 修复逻辑bug，新增 Docker / K8s 容器管理模块（Docker状态总览、容器资源监控、Docker健康检查、K8s集群状态、容器日志采集），总计26个模块，覆盖Windows Server容器化场景 |
| v1.8.0 | 2026-07-16 | 新增 Docker / K8s 容器管理模块（Docker状态总览、容器资源监控、Docker健康检查、K8s集群状态、容器日志采集），总计26个模块，覆盖Windows Server容器化场景 |
| v1.7.0 | 2026-07-10 | 新增系统文件完整性检查(SFC/DISM)、存储池管理、备份状态检查3个模块，总计25个模块；每个模块加折叠块；性能硬件自适应优化；新增更新提醒和禁止文件类型声明 |
| v1.6.0 | 2026-07-09 | 新增SSL证书过期检测、防火墙规则审计、服务崩溃恢复状态3个模块，总计22个模块 |
| v1.5.0 | 2026-07-08 | 新增计划任务审计、文件共享审计、DNS网卡诊断3个模块，总计19个模块 |
| v1.4.0 | 2026-07-07 | 新增事件日志诊断、已安装程序管理、用户会话监控3个模块，总计16个模块 |
| v1.3.0 | 2026-07-06 | 新增注册表启动项审计、磁盘健康检测、网络端口监控3个模块，总计13个模块 |
| v1.2.0 | 2026-07-05 | 新增Windows Update性能监控、安全审计3个模块，所有命令折叠隐藏 |
| v1.1.0 | 2026-07-04 | 新增快速开始/报错指引/FAQ |
| v1.0.0 | 2026-07-03 | 初始版本，7个模块 |

## 发布信息


---

## 🔔 更新提醒

如何获取 winskill 最新版本：
```bash
skillhub upgrade winskill
```

当前版本：v3.0.0，如有新版本可用，请执行上述命令升级。

---

## 🚫 禁止的文件类型（全 Skill 生效 + SkillHub 打包排除）

> 以下 5 大类文件类型在所有涉及文件操作的模块中均会被拦截，同时也会被 SkillHub 打包排除规则过滤。

### 1. Windows 可执行 / 批处理脚本
`.bat` `.cmd` `.ps1` `.vbs` `.exe` `.dll` `.lnk` `.msi`

### 2. Office 二进制文档
`.docx` `.xlsx` `.pptx` `.doc` `.xls` `.ppt` `.xlsm` `.docm` `.pptm`

### 3. 二进制镜像 / 安装包
`.iso` `.dmg` `.zip` `.rar` `.7z` `.tar` `.gz` `.apk` `.jar`

### 4. 系统缓存 / 隐藏文件
`.DS_Store` `.git` 目录 `.env` `.log` `.tmp`

### 5. 其他风险脚本
`.sh` `.com` `.scr` `.hta` `.reg`

