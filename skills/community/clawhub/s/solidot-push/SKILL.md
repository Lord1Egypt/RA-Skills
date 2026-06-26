---
name: solidot-push
description: 抓取 Solidot 热门和最新文章，推送到飞书
version: 1.0.0
tags: [solidot, rss, 资讯, 飞书]
---

# Solidot 资讯推送

抓取 Solidot (solidot.org) 的热门文章和最新文章，推送到飞书文档。

## 触发方式

当用户说：
- "推送 solidot"
- "抓取 solidot"
- "solidot 资讯"

## 使用方法

### 手动执行
```bash
bash ./fetch.sh
```

### 配置飞书推送（可选）

设置环境变量推送到飞书文档：
```bash
export FEISHU_DOC_TOKEN="你的飞书文档token"
```

### 定时任务

自动每天早上 8 点推送：
```bash
openclaw cron add \
  --name "solidot每日资讯" \
  --schedule "cron 0 8 * * * Asia/Shanghai" \
  --agentTurn "执行命令: bash $SKILL_DIR/fetch.sh"
```

## 输出

生成飞书文档或本地文件，包含：
- 热门/最新文章 (最多15条)
- 文章标题、链接

## 文件位置

- 技能目录: `./` (即 `$SKILL_DIR`)
- 推送脚本: `./fetch.sh`
- 本地保存: `$WORKSPACE/solidot-push.md`
