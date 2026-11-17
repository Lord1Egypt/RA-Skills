---
id: module-04
name: IIS 站点管理
description: 查看站点状态、应用池信息、快速重启。
keywords: ['我的 IIS 站点正常吗？', '重启一下应用池']
permission: admin
mode: readonly
subset: basic
---

### 模块 4：IIS 站点管理






<details>
<summary>📋 展开查看：模块 4：IIS 站点管理</summary>

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






```powershell
# ⚠️ 仅当用户明确确认后才执行！
# Restart-WebSite -Name "你的站点名"
```



**风险等级**：🟢 查看只读 / 🟡 重启需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-Website is not recognized` | IIS 模块未加载 | `Install-WindowsFeature Web-Mgmt-Tools` |
| `Cannot connect to IIS` | W3SVC 服务未启动 | 管理服务 |
| `Could not find WebAdministration` | 未装 IIS 管理工具 | 添加 Web 管理工具 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-5"></a>

