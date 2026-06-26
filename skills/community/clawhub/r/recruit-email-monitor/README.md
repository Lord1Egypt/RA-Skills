---
name: recruit-email-monitor
description: 招聘邮件监控系统 - 自动检查邮箱、记录到表格、飞书通知、每日简报
homepage: https://github.com/nhaoxi/recruit-email-monitor
metadata: {
  "clawdbot": {
    "emoji": "📧",
    "requires": {
      "bins": ["python3"],
      "pip": ["openpyxl", "poplib"]
    },
    "install": [
      {
        "id": "pip-deps",
        "kind": "pip",
        "packages": ["openpyxl"],
        "label": "安装依赖 (openpyxl)"
      }
    ],
    "config": {
      "email_accounts": "配置邮箱账号 (QQ/163 等)",
      "excel_path": "招聘邮件汇总表格路径",
      "feishu_target": "飞书通知目标用户 ID"
    }
  }
}
---

# 招聘邮件监控系统

自动监控多个邮箱的招聘相关邮件，记录到 Excel 表格，支持飞书实时通知和每日简报。

## 功能

- **自动检查**: 每小时检查 QQ 邮箱、163 邮箱等
- **智能分类**: 自动识别笔试/测评、面试、Offer、宣讲会、投递确认等类型
- **实时通知**: 发现新邮件时立即发送飞书消息
- **每日简报**: 每天早上 9:00 汇总待处理邮件
- **表格管理**: 自动记录到 Excel，支持状态标记

## 快速开始

### 1. 配置邮箱

编辑 `scripts/email-heartbeat-check.py`，配置你的邮箱账号：

```python
EMAIL_ACCOUNTS = [
    {
        'name': 'QQ 邮箱',
        'user': 'your_qq@qq.com',
        'password': 'your_auth_code',  # 使用授权码，不是登录密码
        'host': 'pop.qq.com',
        'port': 995,
    },
    {
        'name': '163 邮箱',
        'user': 'your_name@163.com',
        'password': 'your_auth_code',
        'host': 'pop.163.com',
        'port': 995,
    }
]
```

### 2. 配置飞书通知

在脚本中修改飞书目标用户 ID：

```python
'--target', 'user:YOUR_FEISHU_USER_ID'
```

### 3. 设置定时任务

使用 OpenClaw 的 cron 系统或系统 crontab：

```bash
# 每小时检查邮箱
0 * * * * python3 /path/to/email-heartbeat-check.py

# 每天早上 9:00 发送简报
0 9 * * * python3 /path/to/email-daily-briefing.py
```

## 脚本说明

### email-heartbeat-check.py

**功能**: 检查邮箱，发现新招聘邮件时记录到表格并发送飞书通知

**运行频率**: 建议每小时一次

**输出**:
- 更新 Excel 表格
- 发送飞书通知（如有新邮件）

### email-daily-briefing.py

**功能**: 汇总待处理邮件，生成日报并发送

**运行频率**: 每天早上 9:00

**输出**:
- 生成简报文件
- 发送飞书消息

## 邮件分类规则

| 类型 | 关键词 |
|------|--------|
| 笔试/测评 | 笔试、在线笔试、笔试通知、测评、人才测评、性格测评 |
| 面试 | 面试、面试邀请、面试通知 |
| Offer/录用 | offer、录用、签约、三方 |
| 宣讲会 | 宣讲会、说明会、open day |
| 投递确认 | 投递成功、简历、申请 |
| 其他 | 其他招聘相关邮件 |

## 表格结构

| 列名 | 说明 |
|------|------|
| 日期 | 邮件收到时间 |
| 邮箱 | 邮箱账号 (QQ/163) |
| 主题 | 邮件主题 |
| 发件人 | 发件人地址 |
| 状态 | ⏳ 待处理 / ✅ 已完成 |
| 类型 | 邮件分类 |
| 链接 | 邮件中的重要链接 |
| 截止日期 | 截止/面试日期 |

## 命令行示例

```bash
# 手动检查邮箱
python3 scripts/email-heartbeat-check.py

# 手动生成简报
python3 scripts/email-daily-briefing.py

# 查看表格
open /home/erhao/shared/招聘邮件汇总.xlsx
```

## 注意事项

1. **邮箱授权码**: QQ/163 邮箱需要使用授权码，不是登录密码
2. **表格路径**: 确保 Excel 文件路径正确，首次运行会自动创建
3. **飞书权限**: 确保 OpenClaw 有飞书消息发送权限
4. **关键词匹配**: 可根据需要调整 `RECRUITMENT_KEYWORDS` 列表

## 故障排查

**问题**: 没有检测到新邮件
- 检查邮箱授权码是否正确
- 查看脚本运行日志
- 确认关键词匹配规则

**问题**: 飞书通知未发送
- 检查飞书用户 ID 是否正确
- 确认 OpenClaw 飞书插件已启用

**问题**: 表格写入失败
- 检查文件路径权限
- 确保 Excel 文件未被其他程序占用

## 相关文件

- `scripts/email-heartbeat-check.py` - 邮箱检查脚本
- `scripts/email-daily-briefing.py` - 每日简报脚本
- `/home/erhao/shared/招聘邮件汇总.xlsx` - 邮件汇总表格
- `/home/erhao/shared/招聘邮件每日简报.txt` - 简报输出文件
