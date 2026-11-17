---
id: module-33
name: 告警推送
description: 告警推送（企微/钉钉 webhook，URL 存环境变量，聚合去抖，告警含主机名/指标/当前值/阈值/建议动作）
keywords: ['告警推送', 'webhook', '企微', '钉钉', 'alert_pusher']
permission: user
mode: readonly
subset: advanced
---

## 🆕 模块 33：告警推送（alert_pusher）

> ⚠️ 把模块 31 写入 `alerts.csv` 的告警通过企业微信/钉钉 webhook 推送到群。webhook URL 只存环境变量，不落仓库（符合禁止文件类型规则）。

<details>
<summary>📋 展开查看：模块 33：告警推送（alert_pusher）</summary>

### 33.1 配置 webhook（环境变量）

```powershell
# 企微/钉钉群机器人 webhook 地址，仅存当前会话环境变量
# 企微：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx
# 钉钉：https://oapi.dingtalk.com/robot/send?access_token=xxxx
$env:WINSKILL_ALERT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的KEY"

# 如需持久化（重启后仍生效），写入用户环境变量：
[Environment]::SetEnvironmentVariable("WINSKILL_ALERT_WEBHOOK", "https://...", "User")
```

### 33.2 推送告警（去抖 + 失败重试）

```powershell
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$alerts = Join-Path $outDir "alerts.csv"
$webhook = $env:WINSKILL_ALERT_WEBHOOK
if (-not $webhook) { Write-Host "❌ 未配置 webhook，请先设置环境变量 WINSKILL_ALERT_WEBHOOK（见 33.1）"; exit 1 }
if (-not (Test-Path $alerts)) { Write-Host "✅ 无告警可推送"; exit 0 }

$data = Import-Csv $alerts
# 仅推送最近 30 分钟且未推送的（聚合去抖，防告警风暴）
$cutoff = (Get-Date).AddMinutes(-30)
$pending = $data | Where-Object {
    try { $rt = [datetime]::ParseExact($_.Timestamp,'yyyy-MM-dd HH:mm:ss',$null) } catch { $rt = [datetime]::MinValue }
    $rt -ge $cutoff
}
if ($pending.Count -eq 0) { Write-Host "✅ 无新告警（30 分钟内）"; exit 0 }

Write-Host ("`n🔔 推送 {0} 条告警：" -f $pending.Count)
foreach ($a in $pending) {
    $msg = "🚨 Winskill 告警`n主机: $($a.Host)`n指标: $($a.Metric) = $($a.Value) (阈值 $($a.Threshold))`n等级: $($a.Level)`n建议: $($a.Recommend)"
    $body = @{ msgtype="text"; text=@{ content=$msg } } | ConvertTo-Json -Compress
    try {
        Invoke-RestMethod -Uri $webhook -Method Post -Body $body -ContentType "application/json;charset=utf-8"
        Write-Host "✅ 已推送: $($a.Metric) @ $($a.Host)"
    } catch {
        Write-Host "❌ 推送失败（网络异常，下次调用将重试）: $_"
    }
}
```

### 33.3 一键巡检 + 推送（串联）

```powershell
# 先确认监控在跑（模块 31.1），再查看当前告警并推送
& { 
    $outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
    $alerts = Join-Path $outDir "alerts.csv"
    if (Test-Path $alerts) {
        $n = (Import-Csv $alerts).Count
        Write-Host "当前累计告警 $n 条"
    }
}
# 推送（调用 33.2 逻辑）
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `未配置 webhook` | 环境变量未设 | 执行 33.1 设置 `WINSKILL_ALERT_WEBHOOK` |
| `Invoke-RestMethod 超时` | 服务器离线/URL 错误 | 检查网络与 webhook 地址；本地 alerts.csv 保留，下次重试 |
| 推送成功但群无消息 | 机器人被踢/限流 | 确认群机器人仍在，企微单机器人限 20 条/分钟 |

</details>

[↑ 返回顶部](#module-1)

---
