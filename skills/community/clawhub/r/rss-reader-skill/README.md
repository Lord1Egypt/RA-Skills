# RSS Reader + AI Summary

> OpenClaw Skill - RSS 订阅 + AI 摘要 + 飞书推送

## 快速开始

### 1. 安装依赖

```bash
cd ~/.agents/skills/rss-reader
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# AI 摘要（必需）
export OPENAI_API_KEY="sk-xxx"

# 飞书推送（可选）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 3. 添加订阅

```bash
python3 rss_reader.py 订阅 "https://blog.openai.com/rss"
```

### 4. 查看订阅

```bash
python3 rss_reader.py 订阅列表
```

### 5. 刷新获取新文章

```bash
python3 rss_reader.py 立即刷新
```

## 定时任务

使用 OpenClaw Cron 自动刷新：

```bash
openclaw cron add \
  --name "rss-refresh" \
  --every "2h" \
  --session main \
  --system-event "[RSS刷新] 请立即执行：python3 ~/.agents/skills/rss-reader/rss_reader.py 立即刷新。执行完后回复 NO_REPLY。不要删除任何 cron 任务。"
```

## 飞书机器人配置

1. 在飞书群中添加「自定义机器人」
2. 获取 Webhook 地址
3. 设置环境变量：`FEISHU_WEBHOOK_URL`

## 常见 RSS 源

```bash
# 技术博客
python3 rss_reader.py 订阅 "https://blog.openai.com/rss" "OpenAI Blog"
python3 rss_reader.py 订阅 "https://www.anthropic.com/news/rss" "Anthropic Blog"

# 中文资讯
python3 rss_reader.py 订阅 "https://www.ruanyifeng.com/blog/atom.xml" "阮一峰"
python3 rss_reader.py 订阅 "https://36kr.com/feed" "36氪"

# 开发者社区
python3 rss_reader.py 订阅 "https://www.v2ex.com/index.xml" "V2EX"
```

## 文件说明

```
rss-reader/
├── SKILL.md              # Skill 说明
├── rss_reader.py         # 主脚本
├── requirements.txt      # Python 依赖
├── README.md             # 本文档
└── data/
    ├── subscriptions.json    # 订阅列表
    └── articles.json         # 已读文章
```

## 问题排查

### Q: 为什么没有生成摘要？
A: 检查 `OPENAI_API_KEY` 是否设置正确

### Q: 为什么推送到飞书失败？
A: 检查 `FEISHU_WEBHOOK_URL` 是否正确，确保机器人未被移除

### Q: 为什么有些 RSS 无法订阅？
A: 某些网站可能禁止爬取，或 RSS 格式不标准

## License

MIT
