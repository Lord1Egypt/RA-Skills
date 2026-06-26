# Webhook Notify 版本历史

## v2.0.0 (2026-06-04) - 完整版

### 新增功能
✅ **多平台支持**
- 钉钉 (DingTalk)
- 企业微信 (WeCom)
- 飞书 (Feishu)
- Slack
- Discord
- Telegram
- 自定义 HTTP Webhook

✅ **核心函数**
- `Get-WebhookPlatform` - 自动识别平台
- `Send-Webhook` - 统一发送接口
- `Send-Webhook-Batch` - 批量发送
- `Test-Webhook-Connection` - 测试连通性
- `Send-Webhook-Template` - 模板系统

✅ **高级特性**
- 自动平台识别（根据 URL 关键字）
- 重试机制（指数退避：2^1, 2^2, 2^3 秒）
- 内置模板系统
  - `system-alert` - 系统告警
  - `deploy-success` - 部署成功
  - `deploy-failed` - 部署失败
  - `es-alert` - ES 异常告警
- 支持 @所有人 和 @指定用户
- 详细的错误处理和日志输出

### 使用示例

```powershell
# 引用函数库
. "E:\devdir\clawd\skills\webhook-notify\webhook-functions.ps1"

# 基础发送
Send-Webhook -Url "URL" -Message "消息"

# 批量发送
$urls = @(
    "https://oapi.dingtalk.com/robot/send?access_token=***",
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***",
    "https://open.feishu.cn/open-apis/bot/v2/hook/***"
)
Send-Webhook-Batch -Urls $urls -Message "广播消息"

# 使用模板
Send-Webhook-Template -Template "system-alert" -Params @{
    Severity = "critical"
    Component = "CPU"
    Status = "95%"
    Details = "持续高负载"
} -Url $env:DINGTALK_WEBHOOK

# 测试
Test-Webhook-Connection -Url "URL"
```

---

## v2.0 (2026-04-14) - ClawHub 首发版

### 主要更新
- 新增统一接口 `Send-Webhook`
- 新增自动平台识别（钉钉、企业微信、飞书）
- 新增模板系统
- 新增配置管理
- 新增重试机制
- 改进错误处理

### 发布到 ClawHub
- 发布ID: `k974p7hy5yp2v3brvjbav3dagx84t5q7`
- 技能页面：https://clawhub.ai/imzhulei/webhook-notify

---

## v1.0 (2026-03-19) - 初始版本

### 支持平台
- 钉钉
- 企业微信
- 飞书
- Slack

### 函数列表
- `Send-WebhookDingTalk`
- `Send-WebhookWeCom`
- `Send-WebhookFeishu`
- `Send-WebhookSlack`
- `Test-Webhook`

### 限制
- 需要分别调用不同平台的函数
- 无统一接口
- 无重试机制
- 无模板系统

---

## 平台对比

| 平台 | 消息类型 | @功能 | 必填参数 |
|------|---------|------|---------|
| 钉钉 | text, markdown, actionCard | ✅ | access_token |
| 企业微信 | text, markdown, news | ✅ | key |
| 飞书 | text, post, interactive | ✅ | hook_id |
| Slack | text, block, attachment | ❌ | webhook_id |
| Discord | text, embed | ❌ | webhook_id/token |
| Telegram | text, markdown, HTML | ❌ | bot_token/chat_id |

---

## 迁移指南

### 从 v1.0 升级到 v2.0.0

**旧代码**:
```powershell
Send-WebhookDingTalk -WebhookUrl $url -Message "消息"
Send-WebhookWeCom -WebhookUrl $url -Message "消息"
```

**新代码**:
```powershell
Send-Webhook -Url $url -Message "消息"  # 自动识别平台
```

### 从 v2.0 升级到 v2.0.0

无破坏性变更，新增：
- Discord 支持
- Telegram 支持
- 模板系统增强
- 错误处理改进

---

## 已知问题

### 钉钉
- 需要在机器人设置中添加关键字或配置 IP 白名单
- 错误码 310000: keywords not in content

### 企业微信
- 需要在机器人配置中设置白名单

### 飞书
- 自定义机器人需要在群组中添加

---

## TODO

- [ ] 支持 Markdown 消息类型
- [ ] 支持 ActionCard/卡片消息
- [ ] 支持发送图片/文件
- [ ] 异步并发发送
- [ ] 发送队列管理
- [ ] Web 界面配置工具