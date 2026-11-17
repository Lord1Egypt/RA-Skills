---
id: module-05
name: 服务状态监控
description: 一眼看出哪些关键服务挂了。
keywords: ['检查服务器关键服务', '看下数据库有没有挂']
permission: user
mode: readonly
subset: performance
---

### 模块 5：服务状态监控






<details>
<summary>📋 展开查看：模块 5：服务状态监控</summary>

**用途**：一眼看出哪些关键服务挂了。

**常你说**：`"检查服务器关键服务"` / `"看下数据库有没有挂"`




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



**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot find any service ...` | 该服务未安装 | 自动跳过 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-6"></a>

