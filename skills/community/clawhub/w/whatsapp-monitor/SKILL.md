---
name: whatsapp-monitor
description: Real-time WhatsApp message monitor that tracks specified chats or groups for keyword hits and periodically aggregates matching messages to a Feishu (Lark) multi-dimensional table. Use when: (1) You need to monitor WhatsApp conversations for specific keywords, (2) You want to collect filtered messages into a structured Feishu table, (3) You need scheduled batch reporting from WhatsApp to Feishu, (4) You're setting up automated message monitoring and alerting systems.
---

# WhatsApp Message Monitor Skill

## Overview

This skill enables automated monitoring of WhatsApp conversations, filtering for specific keywords, and batch exporting matching messages to Feishu (Lark) multi-dimensional tables.

## Core Features

- **Target Monitoring**: Configure WhatsApp contacts or groups to monitor
- **Keyword Filtering**: Define keywords or patterns to watch for
- **Batch Collection**: Accumulate messages until threshold is reached
- **Scheduled Export**: Periodically push collected messages to Feishu tables
- **Real-time Alerts**: Optional immediate notification for high-priority keywords

## 快速开始

### 1. 前提条件

使用此技能前，请确保：

- ✅ **WhatsApp 访问权限**：个人或商业账户
- ✅ **飞书/Lark 账户**：具备 API 访问权限
- ✅ **飞书多维表格应用**：已安装和配置
- ✅ **OpenClaw WhatsApp 渠道**：已配置并配对设备

### 2. OpenClaw 集成步骤

1. **配置 WhatsApp 渠道**
   ```bash
   # 在 OpenClaw 中设置 WhatsApp 渠道
   openclaw channels enable whatsapp
   ```

2. **配对 WhatsApp 设备**
   - 打开浏览器访问 WhatsApp Web (web.whatsapp.com)
   - 扫描二维码配对设备
   - 确保设备状态显示为“已连接”

3. **安装技能依赖**
   ```bash
   cd ~/whatsapp-monitor   # 或你的克隆目录，例如 /opt/whatsapp-monitor
   pip install -r requirements.txt
   ```

4. **配置监控目标**
   ```bash
   # 编辑配置文件
   python scripts/setup.py
   ```

5. **配置飞书集成**
   - 获取飞书应用凭证 (App ID, App Secret)
   - 创建多维表格并获取 Table Token
   - 更新 `config/feishu-settings.json`

### 3. 首次运行

测试配置：
```bash
python scripts/monitor.py --test-config
```

启动监控：
```bash
python scripts/monitor.py --start
```

查看状态：
```bash
python scripts/monitor.py --status
```

### 2. Configuration Files

This skill uses two main configuration files:

- `config/whatsapp-targets.json` - Define WhatsApp contacts/groups to monitor
- `config/feishu-settings.json` - Configure Feishu API and table settings

## Configuration

### WhatsApp Targets

Create `config/whatsapp-targets.json`:

```json
{
  "version": "1.0",
  "targets": [
    {
      "name": "Project Team Chat",
      "type": "group",  // "contact" or "group"
      "identifier": "1234567890-1234567890@g.us",  // WhatsApp group ID
      "enabled": true,
      "keywords": ["urgent", "deadline", "blocker", "issue"],
      "priority": "high"
    },
    {
      "name": "Client Support",
      "type": "contact",
      "identifier": "+1234567890@c.us",  // WhatsApp contact ID
      "enabled": true,
      "keywords": ["complaint", "escalation", "critical", "outage"],
      "priority": "medium"
    }
  ],
  "monitoring": {
    "scan_interval_minutes": 5,
    "batch_size": 10,
    "max_age_hours": 24,
    "alert_on_high_priority": true
  }
}
```

### Feishu Settings

Create `config/feishu-settings.json`:

```json
{
  "feishu": {
    "app_id": "YOUR_APP_ID",
    "app_secret": "YOUR_APP_SECRET",
    "table_app_token": "YOUR_TABLE_APP_TOKEN",
    "table_token": "YOUR_TABLE_TOKEN"
  },
  "table": {
    "name": "WhatsApp Monitor Log",
    "fields": [
      {"name": "timestamp", "type": "datetime"},
      {"name": "source", "type": "text"},
      {"name": "sender", "type": "text"},
      {"name": "message", "type": "text"},
      {"name": "keyword_matched", "type": "text"},
      {"name": "priority", "type": "text"}
    ]
  },
  "export": {
    "batch_threshold": 10,
    "schedule": "every 30 minutes",
    "retry_on_failure": true,
    "max_retries": 3
  }
}
```

## 使用工作流

### 设置阶段

1. **初始化配置** - 设置监控目标和飞书凭证
   ```bash
   python scripts/setup.py
   ```

2. **测试连接** - 验证 WhatsApp 和飞书 API 连接
   ```bash
   python scripts/monitor.py --test-config
   ```

3. **启动监控** - 开始扫描配置的聊天
   ```bash
   python scripts/monitor.py --start
   ```

### OpenClaw Skill 集成

在 OpenClaw 中使用此技能：

```bash
# 加载技能（路径改为本机 Linux 上的技能目录）
openclaw skills load ~/whatsapp-monitor

# 或直接调用技能函数
openclaw skills run whatsapp-monitor --start
```

### 定时任务设置

通过 OpenClaw cron 设置定时监控：

```yaml
# 创建定时任务
schedule:
  kind: "cron"
  expr: "*/5 * * * *"  # 每5分钟运行一次
payload:
  kind: "agentTurn"
  message: "运行 WhatsApp 消息监控"
  sessionTarget: "isolated"
```

### 实时通知配置

配置实时告警（当匹配到高优先级关键词时）：

1. 在 `config/whatsapp-targets.json` 中设置：
```json
{
  "monitoring": {
    "alert_on_high_priority": true
  }
}
```

2. 配置通知渠道（可选）：
   - 飞书机器人消息
   - 电子邮件通知
   - 短信告警

### Monitoring Phase

The system will:

1. Periodically check configured WhatsApp chats
2. Filter messages for keyword matches
3. Store matching messages locally
4. Export to Feishu when batch threshold is reached or on schedule

### Export Phase

When ready to export, the system will:

1. Format collected messages according to table schema
2. Push to Feishu multi-dimensional table
3. Clear local cache after successful export
4. Log export status and any errors

## Tools and Scripts

### Core Monitoring Script

See [scripts/monitor.py](scripts/monitor.py) for the main monitoring logic.

### Configuration Management

See [scripts/config.py](scripts/config.py) for handling configuration files.

### Feishu API Integration

See [scripts/feishu_client.py](scripts/feishu_client.py) for Feishu table operations.

### WhatsApp Web Automation

See [scripts/whatsapp_web.py](scripts/whatsapp_web.py) for WhatsApp Web interaction.

## Advanced Features

### Custom Filters

Beyond simple keywords, you can implement:

- Regular expression patterns
- Sentiment analysis
- Time-based rules
- Sender-specific filters

### Alerting Options

Configure additional alert channels:

- Email notifications
- Slack/Teams messages
- SMS alerts
- Push notifications

### Data Enrichment

Enhance collected messages with:

- Sentiment scores
- Entity extraction
- Topic classification
- Translation services

## Troubleshooting

### Common Issues

1. **WhatsApp Web Connection** - Ensure browser automation is working
2. **Feishu API Permissions** - Verify app has correct table permissions
3. **Keyword Matching** - Check for case sensitivity and special characters

### Monitoring Status

Check monitoring logs in `logs/whatsapp-monitor.log` for operational details and errors.

## Integration Examples

### Combine with Other Skills

This skill can be combined with:

- **Calendar Integration** - Trigger calendar events based on messages
- **Task Management** - Create tasks from important messages
- **CRM Systems** - Update customer records from support chats

### Automated Reporting

Set up automated reports:

- Daily summary reports
- Weekly keyword trend analysis
- Monthly activity reports

## Security Considerations

- Store sensitive credentials securely (use environment variables)
- Implement rate limiting for API calls
- Regularly audit access logs
- Consider data retention policies

## Performance Optimization

For high-volume monitoring:

- Implement message deduplication
- Use batch API calls for Feishu
- Optimize keyword matching algorithms
- Consider distributed monitoring for multiple accounts

## Maintenance

Regular maintenance tasks:

- Update keyword lists periodically
- Review export success rates
- Monitor API rate limits
- Backup configuration and logs

## References

For detailed API documentation and additional resources, see:
- [Feishu Open Platform API Reference](references/feishu_api.md)
- [WhatsApp Web Automation Guide](references/whatsapp_web.md)
- [Advanced Filtering Patterns](references/filter_patterns.md)

## Quick Commands

### Start Monitoring
```bash
python scripts/monitor.py --start
```

### Force Export
```bash
python scripts/monitor.py --export
```

### View Status
```bash
python scripts/monitor.py --status
```

### Test Configuration
```bash
python scripts/monitor.py --test-config
```

## Support

For assistance or feature requests, refer to the troubleshooting section or contact the skill maintainer.