---
name: social-sentiment-monitor
description: |
  社交媒体舆情监控助手 - 实时监控Twitter、Reddit等平台的加密货币讨论、情绪分析和热点追踪。
  当用户需要以下功能时触发此skill：
  (1) 监控特定代币或项目的社交媒体讨论热度
  (2) 分析社区情绪变化（看涨/看跌/恐慌/FOMO）
  (3) 追踪KOL和大V的发言动向
  (4) 发现 viral 内容和热点话题
  (5) 监测负面舆情和FUD传播
  (6) 生成舆情报告和趋势分析
---

# Social Sentiment Monitor

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

社交媒体舆情监控助手 — 读懂市场的声音

## 核心能力

### 1. 多平台监控
- **Twitter/X** - 推文量、互动数据、情绪分析
- **Reddit** - 板块讨论、投票趋势、评论分析
- **Telegram** - 群组活跃度、消息频率
- **Discord** - 社区讨论热度

### 2. 情绪分析
- **情绪评分** - 0-100分，量化社区情绪
- **情绪分类** - 看涨/看跌/恐慌/FOMO/中性
- **情绪趋势** - 追踪情绪变化轨迹
- **极端情绪预警** - FOMO/FUD极端值检测

### 3. 热点发现
- **话题热度** - 讨论量突增检测
- **Viral内容** - 高传播性内容识别
- **关键词追踪** - 自定义关键词监控
- **新兴话题** - 新出现的热门讨论

### 4. KOL监控
- **大V发言** - 追踪知名KOL的推文
- **影响力分析** - 评估KOL对市场的影响
- **观点聚合** - 汇总主流观点
- **异常发言** - 检测突然的态度转变

### 5. 负面舆情预警
- **FUD检测** - 恐慌、质疑、负面信息
- **谣言识别** - 识别潜在的虚假信息
- **危机预警** - 项目危机信号
- **传播追踪** - 追踪负面信息的传播路径

## 使用工作流

### 快速开始

```bash
# 1. 监控代币情绪
python scripts/token_sentiment.py --token ETH --platforms twitter,reddit

# 2. 追踪热点话题
python scripts/trending_topics.py --keywords "以太坊,ETH,合并" --hours 24

# 3. 监控KOL发言
python scripts/kol_monitor.py --handle @VitalikButerin --alert-on-post

# 4. 负面舆情预警
python scripts/fud_detector.py --token BTC --threshold 70

# 5. 生成舆情报告
python scripts/sentiment_report.py --token SOL --days 7

# 6. 启动全面监控
python scripts/sentiment_daemon.py --config config.yaml
```

### 配置示例

```yaml
# config/sentiment_monitor.yaml
monitoring:
  # 监控的代币
  tokens:
    - symbol: ETH
      name: Ethereum
      keywords: ["ethereum", "eth", "ether"]
      alert_threshold: 70
    - symbol: BTC
      name: Bitcoin
      keywords: ["bitcoin", "btc"]
      alert_threshold: 75
  
  # 监控的平台
  platforms:
    twitter:
      enabled: true
      min_followers: 1000
      languages: ["en", "zh"]
    reddit:
      enabled: true
      subreddits: ["CryptoCurrency", "ethfinance", "Bitcoin"]
    telegram:
      enabled: false
  
  # KOL监控列表
  kols:
    - handle: "@VitalikButerin"
      name: "Vitalik Buterin"
      weight: 10
    - handle: "@cz_binance"
      name: "CZ"
      weight: 9
  
  # 情绪分析设置
  sentiment:
    bullish_threshold: 65
    bearish_threshold: 35
    extreme_fomo: 85
    extreme_fud: 15
  
  # 通知设置
  notifications:
    telegram:
      enabled: true
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_id: ${TELEGRAM_CHAT_ID}
    discord:
      enabled: true
      webhook_url: ${DISCORD_WEBHOOK_URL}
  
  # 检查间隔（分钟）
  interval: 15
```

## 脚本说明

### scripts/token_sentiment.py
分析特定代币的整体情绪

```bash
# 分析ETH情绪
python scripts/token_sentiment.py --token ETH

# 指定平台
python scripts/token_sentiment.py --token BTC --platforms twitter

# 历史分析
python scripts/token_sentiment.py --token SOL --days 7
```

### scripts/trending_topics.py
发现和追踪热点话题

```bash
# 追踪关键词
python scripts/trending_topics.py --keywords "空投,airdrop" --hours 24

# 发现新兴话题
python scripts/trending_topics.py --discover --top-n 10
```

### scripts/kol_monitor.py
监控KOL发言

```bash
# 监控特定KOL
python scripts/kol_monitor.py --handle @VitalikButerin

# 监控列表中的KOL
python scripts/kol_monitor.py --watchlist --config kols.yaml
```

### scripts/fud_detector.py
检测负面舆情

```bash
# 监控BTC负面信息
python scripts/fud_detector.py --token BTC

# 设置敏感度
python scripts/fud_detector.py --token ETH --sensitivity high
```

### scripts/viral_content.py
发现病毒式传播内容

```bash
# 发现热门推文
python scripts/viral_content.py --platform twitter --min-likes 1000

# 追踪传播路径
python scripts/viral_content.py --track tweet_id
```

### scripts/sentiment_report.py
生成舆情报告

```bash
# 生成周报
python scripts/sentiment_report.py --token ETH --days 7 --output report.pdf

# 对比多个代币
python scripts/sentiment_report.py --compare ETH,BTC,SOL --days 30
```

### scripts/sentiment_daemon.py
守护进程模式

```bash
# 启动监控
python scripts/sentiment_daemon.py --config config.yaml

# 后台运行
python scripts/sentiment_daemon.py --daemon
```

## 数据源

### 免费数据源

| 平台 | 数据源 | 限制 |
|------|--------|------|
| Twitter | Twitter API v2 | 1500 tweets/month (免费) |
| Reddit | PRAW | 60 requests/minute |
| LunarCrush | LunarCrush API | 有限免费额度 |
| Santiment | Santiment API | 部分指标免费 |

### 付费数据源

| 平台 | 价格 | 特点 |
|------|------|------|
| Twitter API Basic | $100/month | 10K tweets/month |
| Twitter API Pro | $5000/month | 1M tweets/month |
| LunarCrush Pro | $49/month | 完整社交数据 |
| Santiment | €49/month | 链上+社交数据 |

## 情绪指标说明

### 情绪分数 (0-100)
- **0-20**: 极度恐慌 (Extreme Fear)
- **21-40**: 恐慌 (Fear)
- **41-60**: 中性 (Neutral)
- **61-80**: 贪婪 (Greed)
- **81-100**: 极度贪婪 (Extreme Greed)

### 关键指标
- **讨论量 (Volume)** - 提及次数
- **情绪强度 (Intensity)** - 情绪表达强烈程度
- **传播速度 (Velocity)** - 信息传播快慢
- **影响力 (Impact)** - 对价格的潜在影响

## 预警级别

### 🔴 紧急 (Critical)
- 极端FUD情绪 (< 15分)
- 重大负面事件爆发
- KOL突然转变态度

### 🟠 重要 (Warning)
- 情绪快速恶化
- 大量负面信息集中出现
- 传播速度异常

### 🟡 普通 (Info)
- 情绪波动在正常范围
- 新兴话题出现
- 讨论量突增

## 最佳实践

1. **多平台验证** - 不要依赖单一平台数据
2. **结合链上** - 社交媒体情绪应与链上数据结合
3. **识别机器人** - 注意过滤僵尸账号和机器人
4. **关注质量** - 高互动量≠高质量讨论
5. **长期追踪** - 建立基准线，识别异常

## 风险提示

⚠️ **本工具仅供信息参考，不构成投资建议**

- 社交媒体情绪可能被操纵
- 机器人和水军影响数据准确性
- KOL发言可能有利益关联
- 情绪指标具有滞后性

---

*倾听市场的声音，但保持独立思考。*
