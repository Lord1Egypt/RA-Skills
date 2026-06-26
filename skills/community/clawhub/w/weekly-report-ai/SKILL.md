---
name: weekly-report
description: 自动整理周报工具。支持从多个数据源（GitHub、飞书文档、日历）汇总工作内容，生成Markdown周报。支持保存历史、AI摘要、导出PDF/HTML、发送邮件、写入飞书文档。适用于需要定期总结工作成果的用户。
---

# Weekly Report - 自动整理周报

## 功能概述

自动从多个数据源汇总一周工作内容，生成结构化的Markdown周报，支持多种输出方式。

## 支持的数据源

### 1. GitHub / GitLab
- **获取内容**：commits、PRs、issues
- **配置**：用户需提供仓库地址和访问Token

### 2. 飞书文档/知识库
- **获取内容**：指定文档/知识库中的更新
- **配置**：用户提供文档链接或知识库ID

### 3. 日历事件
- **获取内容**：Google Calendar / 飞书日历
- **配置**：用户授权日历访问

### 4. 手动输入
- 用户在对话中补充工作内容

## 输出功能

### 1. Markdown周报
生成标准格式周报，包含：
- 本周概览（提交数、PR数、会议数）
- GitHub贡献（PR详情+提交记录）
- 文档更新
- 会议记录
- 补充说明
- 下周计划

### 2. 历史保存
- 自动保存到 `~/.weekly-report/history/`
- 支持查询历史周报
- 按周查看/删除历史

### 3. 导出功能
- **HTML**：生成带样式的网页
- **PDF**：使用pandoc导出（需安装pandoc）

### 4. 邮件发送
- 支持SMTP协议（QQ邮箱、网易邮箱等）
- 自动转换为HTML格式

### 5. 飞书文档
- 自动创建飞书文档
- 支持追加到已有文档

## 使用方式

### 手动触发
用户说"生成周报"、"整理本周工作"时执行。

### 定时执行
配置cron任务，每周五下午自动执行。

## 脚本列表

| 脚本 | 功能 |
|------|------|
| `generate_report.py` | 生成Markdown周报 |
| `github_fetcher.py` | 获取GitHub数据 |
| `feishu_fetcher.py` | 获取飞书文档 |
| `calendar_fetcher.py` | 获取日历事件 |
| `feishu_writer.py` | 写入飞书文档 |
| `email_sender.py` | 发送邮件 |
| `export_pdf.py` | 导出PDF/HTML |
| `history_manager.py` | 历史周报管理 |

## 配置项

| 配置项 | 说明 | 必填 |
|--------|------|------|
| github_token | GitHub访问Token | 否 |
| github_repos | 监控的仓库列表 | 否 |
| feishu_token | 飞书Access Token | 否 |
| feishu_docs | 监控的文档/知识库 | 否 |
| smtp_host | SMTP服务器 | 否 |
| smtp_port | SMTP端口 | 否 |
| smtp_username | 邮箱账号 | 否 |
| smtp_password | 邮箱授权码 | 否 |
| user_name | 用户姓名 | 否 |

## 示例命令

```bash
# 生成周报
python3 generate_report.py --user "张三" --github data.json --manual "本周工作..."

# 获取GitHub数据
python3 github_fetcher.py --token $GITHUB_TOKEN --repos "user/repo" --since "2026-03-16" --until "2026-03-22"

# 发送邮件
python3 email_sender.py --smtp-host smtp.qq.com --smtp-port 465 --username "user@qq.com" --password "xxx" --to "boss@company.com" --subject "第12周周报" --content "$MARKDOWN" --html

# 写入飞书
python3 feishu_writer.py --token $FEISHU_TOKEN --title "第12周周报" --content "$MARKDOWN"

# 导出PDF
python3 export_pdf.py --input report.md --output report.pdf --format pdf

# 保存历史
python3 history_manager.py --action save --week-start "2026-03-16" --week-end "2026-03-22" --content "$MARKDOWN"

# 查看历史
python3 history_manager.py --action list --limit 5
```
