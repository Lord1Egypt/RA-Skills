# 舆情罗盘 Sentiment Compass

AI 驱动的中国社交媒体舆情监测与分析工具。

## 功能

- **平台监测**：小红书、抖音、微博、微信公众号关键词搜索
- **AI 情感分析**：🟢正面 / 🟡中性 / 🔴负面 + 原因摘要
- **舆情报告**：总提及量、情感占比、热度趋势、重点帖子
- **自动预警**：负面超阈值时飞书/邮件推送

## 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

## 快速开始

```bash
# 添加关键词监控
python3 scripts/sentiment.py add "某品牌" "xhs,douyin"

# 执行抓取
python3 scripts/sentiment.py crawl "某品牌"

# 分析情感
python3 scripts/sentiment.py analyze-pending "某品牌"

# 生成报告
python3 scripts/sentiment.py report "某品牌" 7

# 检查预警
python3 scripts/sentiment.py check-alerts
```

## 配置

```bash
# GLM-4 API Key（可选，用于 AI 情感分析）
python3 scripts/sentiment.py config-set glm_api_key "your_key"

# 飞书群机器人 Webhook
python3 scripts/sentiment.py config-set feishu_webhook "https://open.feishu.cn/..."

# 邮件 SMTP
python3 scripts/sentiment.py config-set smtp_config '{"host":"smtp.example.com","port":587,"user":"...","pass":"...","from":"...","to":"..."}'
```

## 套餐

| 套餐 | 月费 | 关键词 | 平台 | 日条数 |
|------|------|--------|------|--------|
| FREE | 免费 | 1 | 小红书 | 50 |
| STD | ¥29 | 3 | 小红书+抖音 | 300 |
| PRO | ¥99 | 10 | 4个平台 | 1000 |
| MAX | ¥299 | 不限 | 4个平台 | 不限 |

> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
