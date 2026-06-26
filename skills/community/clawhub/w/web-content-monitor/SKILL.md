---
name: web-content-monitor
description: 网页内容监控助手。监控指定网页的内容变化，检测关键词出现或消失，支持变化时自动告警。当用户需要：监控竞品官网动态、追踪政策页面变化、监控新闻更新、检测网站内容变更、设置关键词告警时使用此技能。
---

# Web Content Monitor

网页内容监控助手。监控网页变化，关键词出现或消失时触发告警。

## 核心能力

1. **页面抓取** — 定期获取目标页面内容
2. **变化检测** — 对比历史版本，发现新增或删除内容
3. **关键词监控** — 检测特定关键词出现/消失
4. **告警推送** — 支持企业微信、飞书、钉钉推送

## 快速开始

### 监控单个页面

```bash
python3 scripts/monitor_page.py --url "https://example.com/news" --keywords "发布,融资,合作"
```

### 创建定时监控任务

```bash
python3 scripts/schedule_monitor.py --url "https://example.com" --keywords "融资" --schedule "0 */6 * * *"
```

## 脚本说明

### scripts/monitor_page.py

单次监控页面变化。

```bash
python3 scripts/monitor_page.py --url <URL> --keywords <关键词,分隔> [--hash-file <历史文件>]
```

**参数：**
- `--url`: 监控目标 URL
- `--keywords`: 逗号分隔的关键词列表
- `--hash-file`: 历史快照存储路径（默认 ~/.web_monitor/）

### scripts/schedule_monitor.py

创建定时监控任务。

```bash
python3 scripts/schedule_monitor.py --url <URL> --keywords <关键词> --schedule "<cron>" [--channel <wecom|feishu|ddingtalk>]
```

## 典型场景

### 竞品动态监控
```bash
python3 scripts/monitor_page.py \
  --url "https://www.example.com/press" \
  --keywords "融资,上市,合作,收购"
```

### 政策页面追踪
```bash
python3 scripts/schedule_monitor.py \
  --url "https://www.miit.gov.cn/政策页" \
  --keywords "新规,实施,办法" \
  --schedule "0 9 * * *" \
  --channel wecom
```

## 配置说明

### 监控存储路径
默认：`~/.web_monitor/`
- `hashes.json` — 页面哈希记录
- `snapshots/` — 历史快照
