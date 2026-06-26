---
name: smart-collect
description: 分析和总结URL链接内容，并保存到obsidian中，同时定期提醒复习
---
# Smart Collect - 智能收藏回顾系统

基于艾宾浩斯遗忘曲线的智能收藏系统，支持自动抓取、摘要生成、定时复习提醒。

## 目录结构

```
smart-collect/
├── SKILL.md                 # 本文件
├── lib/
│   ├── reviewEngine.js      # 艾宾浩斯复习引擎
│   ├── markdownStore.js     # Markdown 存储模块
│   ├── nlpParser.js        # 自然语言解析模块
│   └── fetcher.js          # 网页抓取模块
├── scripts/
│   ├── shoucang-add.js     # 添加收藏脚本
│   ├── shoucang-review.js  # 复习回顾脚本
│   └── smart-collect.js    # 主入口
└── config.json.example      # 配置示例
```

## 功能

### 1. 自动抓取
- 支持 GitHub/微信公众号/小红书/普通网页
- Readability 算法提取正文
- LLM 生成摘要、标签、分类

### 2. 艾宾浩斯复习
- 间隔：1天 → 2天 → 4天 → 7天 → 15天
- 超过5次自动归档

### 3. 自然语言管理
- 推迟X天
- 已看完归档
- 添加/删除标签
- 标记已回顾

## 配置

复制 `config.json.example` 为 `config.json` 并填入：
- 收藏存储路径
- 飞书配置
- LLM API 配置

## OpenClaw Cron 配置

### 定时规则

**每天 09:30 触发复习**

### cron 表达式

```
30 9 * * *
```

### OpenClaw jobs.json 配置

```json
{
  "jobs": [
    {
      "id": "smart-collect-review",
      "name": "智能收藏每日复习",
      "description": "基于艾宾浩斯曲线触发收藏复习提醒",
      "enabled": true,
      "schedule": {
        "kind": "cron",
        "expr": "30 9 * * *"
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "请执行智能收藏的每日复习任务，运行命令：cd ~/.openclaw/skills/smart-collect && node scripts/shoucang-review.js"
      },
      "delivery": {
        "mode": "announce",
        "channel": "feishu",
        "to": "ou_你的飞书ID"
      }
    }
  ]
}
```

### 部署步骤

1. 复制配置到 OpenClaw cron 目录：
```bash
cp config.json.example config.json
# 编辑 config.json 填入你的配置
```

2. 添加 cron 任务：
```bash
# 编辑 ~/.openclaw/cron/jobs.json 添加上述配置
```

3. 重启 Gateway：
```bash
openclaw gateway restart
```

---

## 文件结构

```
smart-collect/
├── SKILL.md                 # 本文件
├── lib/
│   ├── reviewEngine.js      # 艾宾浩斯复习引擎
│   ├── markdownStore.js     # Markdown 存储模块
│   ├── nlpParser.js         # 自然语言解析模块
│   └── fetcher.js           # 网页抓取模块
├── scripts/
│   ├── shoucang-add.js      # 添加收藏脚本
│   ├── shoucang-review.js    # 复习回顾脚本
│   └── smart-collect.js     # 主入口
└── config.json.example      # 配置示例
```
