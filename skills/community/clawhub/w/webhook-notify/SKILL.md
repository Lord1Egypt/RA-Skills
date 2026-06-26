---
name: webhook-notify
description: 通用 Webhook 通知工具，支持钉钉、企业微信、飞书、Slack、Discord、Telegram。自动识别平台，统一接口，内置模板系统和重试机制。
metadata: {"clawdbot":{"emoji":"🔔","requires":{"anyBins":["powershell"]},"os":["linux","darwin","win32"]}}
---

# Webhook 通知工具 v2.0.0

一个强大的跨平台 webhook 发送工具，支持 6+ 主流平台，自动识别、统一接口、内置模板。

## 📦 安装

### 方式 1: 通过 OpenClaw 技能系统

技能已安装，函数库位置：
```
skills/webhook-notify/webhook-functions.ps1
```

### 方式 2: 引用函数库

```powershell
# 在你的脚本开头引用
. "skills/webhook-notify/webhook-functions.ps1"

# 现在可以使用所有函数
Send-Webhook -Url "URL" -Message "消息"
```

### 方式 3: 复制函数

直接复制 `webhook-functions.ps1` 内容到你的脚本中。

---

## 🌐 支持平台

| 平台 | 自动识别 | @功能 | 示例 URL |
|------|---------|-------|---------|
| **钉钉** | ✅ | ✅ | `https://oapi.dingtalk.com/robot/send?access_token=***` |
| **企业微信** | ✅ | ✅ | `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***` |
| **飞书** | ✅ | ✅ | `https://open.feishu.cn/open-apis/bot/v2/hook/***` |
| **Slack** | ✅ | ❌ | `https://hooks.slack.com/services/***` |
| **Discord** | ✅ | ❌ | `https://discord.com/api/webhooks/***` |
| **Telegram** | ✅ | ❌ | `https://api.telegram.org/bot***/sendMessage` |

---

## 🚀 快速开始

### 基础使用

```powershell
# 引用函数库
. "skills/webhook-notify/webhook-functions.ps1"

# 发送消息（自动识别平台）
Send-Webhook -Url "YOUR_WEBHOOK_URL" -Message "测试消息"

# @所有人（钉钉/企业微信）
Send-Webhook -Url $env:DINGTALK_WEBHOOK -Message "紧急告警" -IsAtAll $true

# @指定手机号
Send-Webhook -Url $env:DINGTALK_WEBHOOK -Message "告警" -AtMobiles @("13800138000")
```

### 批量发送

```powershell
$webhooks = @(
    "https://oapi.dingtalk.com/robot/send?access_token=***",
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***",
    "https://open.feishu.cn/open-apis/bot/v2/hook/***"
)

Send-Webhook-Batch -Urls $webhooks -Message "广播消息"
```

### 使用模板

```powershell
# 系统告警模板
Send-Webhook-Template -Template "system-alert" -Params @{
    Severity = "critical"
    Component = "CPU"
    Status = "95%"
    Details = "持续高负载"
} -Url $env:DINGTALK_WEBHOOK

# 部署成功模板
Send-Webhook-Template -Template "deploy-success" -Params @{
    Project = "MyApp"
    Version = "v1.2.3"
    Environment = "production"
} -Url $env:DINGTALK_WEBHOOK

# ES 异常告警模板
Send-Webhook-Template -Template "es-alert" -Params @{
    Index = "logstash-2026.06.04"
    Count = 57
    Level = "CRITICAL"
    Hosts = @("server1", "server2")
} -Url $env:DINGTALK_WEBHOOK
```

### 测试连通性

```powershell
Test-Webhook-Connection -Url "YOUR_WEBHOOK_URL"
```

---

## 📚 函数参考

### Get-WebhookPlatform

识别 webhook URL 所属平台。

```powershell
Get-WebhookPlatform -Url "https://oapi.dingtalk.com/..."
# 输出：DingTalk
```

---

### Send-Webhook

统一发送接口，自动识别平台并重试。

**参数**:
- `Url` (必填): Webhook URL
- `Message` (必填): 消息内容
- `Title` (可选): 标题
- `IsAtAll` (可选): 是否@所有人
- `AtMobiles` (可选): @的手机号列表
- `Retry` (可选): 重试次数，默认 3
- `Timeout` (可选): 超时秒数，默认 30

**示例**:
```powershell
Send-Webhook -Url $url -Message "告警" -IsAtAll $true -Retry 3
```

---

### Send-Webhook-Batch

批量发送到多个平台。

**参数**:
- `Urls` (必填): URL 数组
- `Message` (必填): 消息内容
- `IsAtAll` (可选): 是否@所有人
- `AtMobiles` (可选): @的手机号列表
- `Retry` (可选): 重试次数

**示例**:
```powershell
$results = Send-Webhook-Batch -Urls $urls -Message "广播"
$results | Format-Table Url, Success, Timestamp
```

---

### Send-Webhook-Template

使用内置模板发送消息。

**可用模板**:
- `system-alert` - 系统告警
- `deploy-success` - 部署成功
- `deploy-failed` - 部署失败
- `es-alert` - ES 异常告警

**参数**:
- `Template` (必填): 模板名称
- `Params` (必填): 模板参数
- `Url` (必填): Webhook URL
- `Retry` (可选): 重试次数

**示例**:
```powershell
Send-Webhook-Template -Template "system-alert" -Params @{
    Severity = "warning"
    Component = "Memory"
    Status = "90%"
    Details = "接近阈值"
} -Url $url
```

---

### Test-Webhook-Connection

测试 webhook 连通性。

**示例**:
```powershell
Test-Webhook-Connection -Url $env:DINGTALK_WEBHOOK
```

---

## 🔧 高级用法

### 环境变量配置

```powershell
# 设置环境变量（永久）
[System.Environment]::SetEnvironmentVariable('DINGTALK_WEBHOOK', 'https://...', 'User')
[System.Environment]::SetEnvironmentVariable('WECOM_WEBHOOK', 'https://...', 'User')
[System.Environment]::SetEnvironmentVariable('FEISHU_WEBHOOK', 'https://...', 'User')

# 使用
Send-Webhook -Url $env:DINGTALK_WEBHOOK -Message "消息"
```

### 监控脚本集成

```powershell
# E:\devdir\clawd\scripts\monitor-alert.ps1
. "skills/webhook-notify/webhook-functions.ps1"

$mem = Get-CimInstance Win32_OperatingSystem
$memPct = [math]::Round((($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize) * 100, 1)

if ($memPct -gt 95) {
    Send-Webhook-Template -Template "system-alert" -Params @{
        Severity = "critical"
        Component = "Memory"
        Status = "${memPct}%"
        Details = "立即处理"
    } -Url $env:DINGTALK_WEBHOOK -IsAtAll $true
}
elseif ($memPct -gt 85) {
    Send-Webhook -Url $env:DINGTALK_WEBHOOK -Message "⚠️ 内存警告：${memPct}%"
}
```

### 自定义模板

```powershell
# 添加自定义模板
$Script:WebhookTemplates['my-template'] = {
    param($params)
    return "自定义消息：$($params.Content)"
}

# 使用
Send-Webhook-Template -Template "my-template" -Params @{Content="测试"} -Url $url
```

---

## ⚠️ 常见问题

### 钉钉：关键字缺失

**错误**: `{"errcode": 310000, "errmsg": "keywords not in content"}`

**解决**: 
1. 在机器人设置中移除关键字，或
2. 确保消息包含关键字：`Send-Webhook -Url $url -Message "【openclaw】消息"`

### IP 白名单

**错误**: `{"errcode": 310000, "errmsg": "IP not in whitelist"}`

**解决**: 在机器人设置中添加服务器 IP 到白名单。

### 重试失败

函数会自动重试 3 次（指数退避：2, 4, 8 秒）。如需更多重试：
```powershell
Send-Webhook -Url $url -Message "消息" -Retry 5
```

---

## 📝 版本历史

- **v2.0.0** (2026-06-04): 完整版
  - 新增 Slack、Discord、Telegram 支持
  - 增强模板系统
  - 改进错误处理和重试机制
  
- **v2.0** (2026-04-14): 首发版
  - 统一接口 Send-Webhook
  - 自动平台识别
  - 模板系统
  
- **v1.0** (2026-03-19): 初始版
  - 分平台的独立函数

详见：`VERSIONS.md`

---

## 📄 文件结构

```
skills/webhook-notify/
├── SKILL.md                  # 本文档
├── webhook-functions.ps1     # PowerShell 函数库
├── VERSIONS.md              # 版本历史
└── README.md                # 使用指南
```

---

## 🔗 相关资源

- [钉钉机器人文档](https://open.dingtalk.com/document/orgapp/custom-bot-to-send-group-chat-messages)
- [企业微信机器人文档](https://developer.work.weixin.qq.com/document/path/91770)
- [飞书机器人文档](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Discord Webhooks](https://support.discord.com/hc/articles/228383668)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**ClawHub**: https://clawhub.ai/imzhulei/webhook-notify  
**版本**: v2.0.0  
**最后更新**: 2026-06-04