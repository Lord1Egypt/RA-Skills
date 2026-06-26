---
name: automation-scripts
description: 自动化脚本集 - 日常任务自动化、定时执行、批量处理
---

# Automation Scripts

常用自动化脚本集合，解放双手。

## 功能

- ✅ 文件批量重命名
- ✅ 数据备份
- ✅ 定时任务
- ✅ 网页截图
- ✅ 数据抓取

## 使用

```bash
# 批量重命名
clawhub auto rename --dir ./photos --pattern "IMG_{date}_{seq}"

# 自动备份
clawhub auto backup --source ~/docs --dest ~/backup

# 网页截图
clawhub auto screenshot --url https://example.com --output img.png

# 定时执行
clawhub auto schedule --cron "0 9 * * *" --command "backup"
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 基础脚本 |
| Pro 版 | ¥59 | 全部脚本 |
| 订阅版 | ¥12/月 | Pro+ 定制脚本 |
