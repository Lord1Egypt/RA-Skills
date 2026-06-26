# V2EX 帖子监控 Skill

## 功能描述

监控 V2EX 论坛指定节点的新帖子，每小时生成总结报告。

## 使用方式

```bash
# 首次配置监控节点
v2ex-monitor config --nodes python,linux,程序员 --apikey your_api_key

# 手动运行一次监控
v2ex-monitor run

# 启动定时监控（每小时）
v2ex-monitor daemon

# 查看帮助
v2ex-monitor --help
```

## 配置说明

- API Key: 在 v2ex.com/settings/tokens 创建
- 监控节点: 支持多个节点，用逗号分隔
- 数据存储: 当前目录 `v2ex_monitor_data/` 目录

## 报告内容

- 新帖子数量
- 热门帖子（回复数最多的）
- 帖子标题列表
- 统计时间

## 定时任务设置 (Linux crontab)

```bash
# 每小时运行一次
0 * * * * cd /path/to/workdir && v2ex-monitor run >> v2ex_monitor.log 2>&1
```

## 定时任务设置 (Windows 任务计划)

```batch
# 创建每小时任务
schtasks /create /tn "V2EX Monitor" /tr "v2ex-monitor run" /sc hourly
```
