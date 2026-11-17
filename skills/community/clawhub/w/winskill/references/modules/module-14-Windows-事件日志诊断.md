---
id: module-14
name: Windows 事件日志诊断
description: 快速定位系统错误、警告，按时间/级别筛选关键日志。
keywords: ['系统日志有没有最近错误', '最近系统出了什么问题', '看看日志']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 14：Windows 事件日志诊断




<details>
<summary>📋 展开查看：🆕 模块 14：Windows 事件日志诊断</summary>

**用途**：快速定位系统错误、警告，按时间/级别筛选关键日志。

**常你说**：`"系统日志有没有最近错误"` / `"最近系统出了什么问题"` / `"看看日志"`

> ⚠️ **本模块仅读取日志，不会修改或清除日志文件。**

### 14.1 系统最近错误日志（最近 2 小时）




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



### 14.2 应用程序错误日志




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



### 14.3 关键系统事件扫描（蓝屏/重启/故障）




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



### 14.4 Setup 日志审计（最近 7 天）




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



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-15"></a>

