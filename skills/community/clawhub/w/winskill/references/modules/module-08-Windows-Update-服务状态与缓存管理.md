---
id: module-08
name: Windows Update 服务状态与缓存管理
description: 诊断 Windows Update 是否卡住、查看已安装补丁、清理更新缓存。
keywords: ['Windows Update 正常吗？', '更新缓存能不能删']
permission: user
mode: readonly
subset: basic
---

## 🆕 模块 8：Windows Update 服务状态与缓存管理




<details>
<summary>📋 展开查看：🆕 模块 8：Windows Update 服务状态与缓存管理</summary>

**用途**：诊断 Windows Update 是否卡住、查看已安装补丁、清理更新缓存。

**常你说**：`"Windows Update 正常吗？"` / `"更新缓存能不能删"`

### 8.1 查看更新服务状态与已安装补丁（只读）




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



### 8.2 检查 SoftwareDistribution 更新缓存大小




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






```powershell
# ⚠️ 仅当用户明确说「确认清理更新缓存」后才执行！
# Stop-Service -Name wuauserv -Force
# Remove-Item -Path "$sd\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
# Start-Service -Name wuauserv
# Write-Host "  ✅ 已清理更新下载缓存，Windows Update 将重新下载所需补丁"
```



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



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-9"></a>

