---
name: usage-monitor
description: Monitor any service usage dashboard and alert when threshold is reached. User-configurable URL and threshold.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Usage Monitor - 通用用量监控 Skill

通用的用量/配额监控 Skill，支持用户自定义监控面板 URL 和告警阈值。

## 特性

- 🔗 **自定义 URL** - 支持任意用量/配额面板页面 URL（如：OpenClaw Token 面板、云服务用量页等）
- 🎯 **自定义阈值** - 支持设置任意告警百分比（1-100）
- 📊 **多维度监控** - 支持多个时间维度的用量数据
- 🔔 **主动提醒** - 达到阈值时自动发送消息

## 快速开始

### 步骤 1：配置用户参数

复制 `config.example.json` 为 `config.json` 并填写：

```json
{
  "panelUrl": "你的用量面板页面 URL",
  "alertThreshold": 80,
  "serviceName": "服务名称（可选）",
  "checkIntervalHours": 4
}
```

### 步骤 2：添加到 HEARTBEAT.md

```markdown
- [ ] 检查服务用量
```

### 步骤 3：运行

```bash
node skills/usage-monitor/check.js
```

## 配置参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `panelUrl` | string | ✅ | - | 用量面板页面 URL（从浏览器地址栏复制） |
| `alertThreshold` | number | ✅ | 80 | 告警阈值百分比（1-100） |
| `serviceName` | string | ❌ | "服务" | 服务名称，用于告警消息 |
| `checkIntervalHours` | number | ❌ | 4 | 检查间隔（小时） |

## URL 获取方法

1. 打开你的用量/配额面板页面（如：OpenClaw Token 数量面板、云服务用量页等）
2. 复制浏览器地址栏的完整 URL
3. 粘贴到 `config.json` 的 `panelUrl` 字段

**URL 示例：**
```
https://example.com/usage/dashboard
https://platform.example.com/token/quota
```

## 告警消息示例

```
⚠️ 服务使用量提醒

📊 服务：OpenClaw Token
📈 当前用量：85%
📈 可用额度：15%
⏰ 剩余天数：30 天
🔗 查看：<你的面板 URL>

当前用量已达告警阈值（80%），请及时关注用量或考虑增加额度。
```

## 注意事项

1. URL 必须是完整的 HTTP/HTTPS 地址
2. 阈值范围 1-100
3. 浏览器自动化需要保持登录状态（如需要）
4. 首次使用需手动访问一次页面完成登录（如需要）

## 适用场景

- ✅ OpenClaw Token 数量监控
- ✅ 云服务用量监控（阿里云、AWS、腾讯云等）
- ✅ API 调用配额监控
- ✅ 资源包用量监控
- ✅ 任何有用量/配额面板的场景
