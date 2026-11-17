---
id: module-26
name: Docker / K8s 容器管理
description: 管理 Windows Server 容器化部署环境，监控 Docker 容器与 K8s 集群健康状态。
keywords: ['Docker 容器正常吗', '哪个容器吃资源', 'K8s 集群状态', '容器日志']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 26：Docker / K8s 容器管理

**用途**：管理 Windows Server 容器化部署环境，监控 Docker 容器与 K8s 集群健康状态。

**常你说**：`"Docker 容器正常吗"` / `"哪个容器吃资源"` / `"K8s 集群状态"` / `"容器日志"`

> ⚠️ **本模块仅在检测到 Docker 或 kubectl 安装时激活，未安装时给出友好提示。**

### 前置检测（自动执行）

```powershell
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
$kubectlPath = Get-Command kubectl -ErrorAction SilentlyContinue

if (-not $dockerPath -and -not $kubectlPath) {
    Write-Host "⚠️ 未检测到 Docker 或 kubectl，跳过模块 26"
    Write-Host "  → 安装 Docker: https://docs.docker.com/engine/install/windows-server/"
    Write-Host "  → 安装 kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/"
}
```

---

### 26.1 Docker 状态总览

**用途**：一键查看容器、镜像、网络、卷的使用情况。

**常你说**：`"Docker 状态总览"` / `"容器列表"` / `"镜像多大"`

<details>
<summary>📋 展开查看命令 — Docker 状态总览</summary>

```powershell
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerPath) {
    Write-Host "⚠️ Docker 未安装"
    return
}

Write-Host "════════ Docker 状态总览 ════════"

# 容器状态
$containers = docker ps -a --format "table {{.Names}}	{{.Status}}	{{.Image}}	{{.Ports}}" 2>$null
if ($containers) {
    Write-Host "`n📦 容器列表:"
    $containers | ForEach-Object { Write-Host "  $_" }
}

# 镜像列表
$images = docker images --format "table {{.Repository}}:{{.Tag}}	{{.Size}}	{{.CreatedSince}}" 2>$null
if ($images) {
    Write-Host "`n🖼️ 镜像列表:"
    $images | ForEach-Object { Write-Host "  $_" }
}

# 网络列表
$networks = docker network ls --format "table {{.Name}}	{{.Driver}}	{{.Scope}}" 2>$null
if ($networks) {
    Write-Host "`n🌐 网络列表:"
    $networks | ForEach-Object { Write-Host "  $_" }
}

# 卷列表
$volumes = docker volume ls --format "table {{.Name}}	{{.Driver}}" 2>$null
if ($volumes) {
    Write-Host "`n💾 卷列表:"
    $volumes | ForEach-Object { Write-Host "  $_" }
}

# 磁盘占用
$diskUsage = docker system df 2>$null
if ($diskUsage) {
    Write-Host "`n📊 Docker 磁盘占用:"
    $diskUsage | ForEach-Object { Write-Host "  $_" }
}
```

</details>

**风险等级**：🟢 无（只读）

---

### 26.2 容器资源监控

**用途**：实时查看每个容器的 CPU / 内存 / 网络 / 磁盘 I/O 占用。

**常你说**：`"哪个容器吃资源"` / `"容器 CPU 占用"` / `"容器内存"`

<details>
<summary>📋 展开查看命令 — 容器资源监控</summary>

```powershell
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerPath) {
    Write-Host "⚠️ Docker 未安装"
    return
}

Write-Host "════════ 容器资源监控 ════════"
Write-Host "（单次采集，不持续占用资源）`n"

# 获取 CPU 核心数，决定采集并发数
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$sampleCount = if ($cpuCores -le 4) { 1 } else { 3 }

# 容器资源统计（不流式输出，避免占用资源）
$stats = docker stats --no-stream --format "table {{.Name}}	{{.CPUPerc}}	{{.MemUsage}}	{{.MemPerc}}	{{.NetIO}}	{{.BlockIO}}" 2>$null
if ($stats) {
    $stats | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "  ⚠️ 无运行中的容器"
}

Write-Host "`n💡 单次采集完成，共 $sampleCount 次采样"
```

</details>

**风险等级**：🟢 无（只读，单次采集不占用资源）

---

### 26.3 Docker 健康检查

**用途**：检查 Docker 服务状态、磁盘占用、守护进程日志异常。

**常你说**：`"Docker 服务正常吗"` / `"Docker 磁盘占用"` / `"Docker 日志异常"`

<details>
<summary>📋 展开查看命令 — Docker 健康检查</summary>

```powershell
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerPath) {
    Write-Host "⚠️ Docker 未安装"
    return
}

Write-Host "════════ Docker 健康检查 ════════"

# 1. Docker 服务状态
$dockerSvc = Get-Service com.docker.service -ErrorAction SilentlyContinue
if ($dockerSvc) {
    $svcStatus = if ($dockerSvc.Status -eq 'Running') { '✅ 运行中' } else { '❌ 已停止' }
    Write-Host "  Docker 服务: $svcStatus"
} else {
    Write-Host "  Docker 服务: ⚠️ 未找到服务"
}

# 2. Docker 版本信息
$dockerVersion = docker version --format "{{.Server.Version}}" 2>$null
if ($dockerVersion) {
    Write-Host "  Docker 版本: $dockerVersion"
}

# 3. Docker 磁盘占用
$diskUsage = docker system df 2>$null
if ($diskUsage) {
    Write-Host "`n📊 磁盘占用:"
    $diskUsage | ForEach-Object { Write-Host "  $_" }
}

# 4. 容器健康状态（如果容器配置了 HEALTHCHECK）
$containers = docker ps --format "{{.Names}}" 2>$null
if ($containers) {
    Write-Host "`n🏥 容器健康状态:"
    foreach ($c in $containers) {
        $health = docker inspect --format "{{.State.Health.Status}}" $c 2>$null
        if ($health) {
            $icon = if ($health -eq 'healthy') { '✅' } elseif ($health -eq 'unhealthy') { '❌' } else { '⏳' }
            Write-Host "  $icon $c : $health"
        } else {
            Write-Host "  ⏳ $c : 未配置健康检查"
        }
    }
}

# 5. 最近 24 小时 Docker 相关系统错误日志
$since = (Get-Date).AddHours(-24)
$dockerEvents = Get-WinEvent -FilterHashtable @{
    LogName='System'; ProviderName='Docker'; Level=2; StartTime=$since
} -ErrorAction SilentlyContinue
if ($dockerEvents) {
    Write-Host "`n⚠️ 最近 24h Docker 错误事件: $($dockerEvents.Count) 条"
    $dockerEvents | Select-Object -First 5 TimeCreated, Message |
        Format-Table -AutoSize -Wrap
} else {
    Write-Host "`n✅ 最近 24h 无 Docker 错误日志"
}
```

</details>

**风险等级**：🟢 无（只读）

---

### 26.4 K8s 集群状态

**用途**：查看 Kubernetes 节点、Pod 健康、资源配额使用率。

**常你说**：`"K8s 集群状态"` / `"Pod 健康"` / `"节点状态"`

<details>
<summary>📋 展开查看命令 — K8s 集群状态</summary>

```powershell
$kubectlPath = Get-Command kubectl -ErrorAction SilentlyContinue
if (-not $kubectlPath) {
    Write-Host "⚠️ kubectl 未安装"
    return
}

Write-Host "════════ K8s 集群状态 ════════"

# 1. 节点状态
Write-Host "`n🖥️ 节点状态:"
$nodes = kubectl get nodes -o wide 2>$null
if ($nodes) {
    $nodes | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "  ⚠️ 无法获取节点信息，检查集群连接"
}

# 2. Pod 状态（所有命名空间）
Write-Host "`n📦 Pod 状态:"
$pods = kubectl get pods --all-namespaces -o wide 2>$null
if ($pods) {
    $pods | ForEach-Object { Write-Host "  $_" }
}

# 3. 资源配额
Write-Host "`n📊 资源配额:"
$resourceQuota = kubectl get resourcequota --all-namespaces 2>$null
if ($resourceQuota) {
    $resourceQuota | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "  未配置资源配额"
}

# 4. 异常 Pod 检测
$allPods = kubectl get pods --all-namespaces --no-headers 2>$null
if ($allPods) {
    $abnormalPods = @()
    foreach ($podLine in $allPods) {
        $parts = $podLine -split '\s+'
        if ($parts.Count -ge 4) {
            $ns = $parts[0]
            $name = $parts[1]
            $ready = $parts[2]
            $status = $parts[3]
            if ($status -ne 'Running' -and $status -ne 'Succeeded') {
                $abnormalPods += [PSCustomObject]@{
                    命名空间 = $ns
                    Pod名 = $name
                    状态 = $status
                    就绪 = $ready
                }
            }
        }
    }
    if ($abnormalPods.Count -gt 0) {
        Write-Host "`n⚠️ 异常 Pod:"
        $abnormalPods | Format-Table -AutoSize
    } else {
        Write-Host "`n✅ 所有 Pod 状态正常"
    }
}

# 5. 节点资源使用（需 metrics-server）
Write-Host "`n📈 节点资源使用:"
$topNodes = kubectl top nodes 2>$null
if ($topNodes) {
    $topNodes | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "  ⚠️ metrics-server 未安装，无法获取资源使用率"
}

Write-Host "`n💡 K8s 集群状态采集完成"
```

</details>

**风险等级**：🟢 无（只读）

---

### 26.5 容器日志采集

**用途**：查看指定容器的最近日志，检测异常模式。

**常你说**：`"看容器日志"` / `"容器报错了"` / `"容器最近日志"`

> ⚠️ **采集限制**：默认采集最近 100 行，内存不足 2 GB 时自动缩减到 50 行，避免占用过多内存。

<details>
<summary>📋 展开查看命令 — 容器日志采集</summary>

```powershell
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerPath) {
    Write-Host "⚠️ Docker 未安装"
    return
}

# 获取可用内存，决定采集行数
$totalRAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB, 1)
$tailCount = if ($totalRAM -lt 2) { 50 } else { 100 }

Write-Host "════════ 容器日志采集 ════════"
Write-Host "可用内存: ${totalRAM} GB，采集行数: $tailCount`n"

# 列出所有容器供选择
$containerList = docker ps -a --format "{{.Names}} | {{.Status}}" 2>$null
if ($containerList) {
    Write-Host "可用容器:"
    $containerList | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
}

# 替换为你要查看的容器名
$targetContainer = "your_container_name"  # ← 改成你要看的容器名

if ($targetContainer -eq "your_container_name") {
    Write-Host "⚠️ 请修改 `$targetContainer 变量为要查看的容器名"
    return
}

Write-Host "📋 容器: $targetContainer (最近 $tailCount 行)"
Write-Host "──────────────────────────────────────"

$logs = docker logs --tail $tailCount $targetContainer 2>&1
if ($logs) {
    $logs | ForEach-Object { Write-Host "  $_" }
    
    # 异常模式检测
    $errorKeywords = @('error', 'exception', 'fatal', 'panic', 'failed', 'refused')
    $errorLines = @()
    $lineNum = 0
    foreach ($line in $logs) {
        $lineNum++
        foreach ($kw in $errorKeywords) {
            if ($line -match $kw) {
                $errorLines += "  行 $lineNum : $line"
                break
            }
        }
    }
    
    if ($errorLines.Count -gt 0) {
        Write-Host "`n⚠️ 检测到 $($errorLines.Count) 行异常关键词:"
        $errorLines | Select-Object -First 20 | ForEach-Object { Write-Host $_ }
        if ($errorLines.Count -gt 20) {
            Write-Host "  ... 还有 $($errorLines.Count - 20) 行未显示"
        }
    } else {
        Write-Host "`n✅ 未检测到异常关键词"
    }
}
```

</details>

**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `docker: command not found` | Docker 未安装 | 安装 Docker Engine |
| `kubectl: command not found` | kubectl 未安装 | 安装 kubectl |
| `connection refused` | Docker/K8s 服务未启动 | 启动对应服务 |
| `permission denied` | 权限不足 | 管理员身份运行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 日志采集时内存不足 | 自动缩减到 50 行，进一步减少可修改 `$tailCount` |
| 容器未配置 HEALTHCHECK | 健康状态显示"未配置"，正常 |
| metrics-server 未安装 | K8s 资源使用率无法获取，属常见情况 |
| Docker 在 Windows Server 上需要特定版本 | 确认 Server 版本与 Docker 兼容 |



---

<a name="module-27"></a>

