# WeChat AI Monitor

微信公众号AI/科技监控工具，自动筛选AI/科技相关内容并生成监控报告。

## Features

- **Multi-account monitoring**: Support monitoring multiple WeChat public accounts
- **AI content filtering**: Intelligent filtering based on 200+ AI/tech keywords
- **RSS support**: Get updates via RSS subscriptions
- **Automatic reports**: Generate formatted Markdown reports
- **24-hour monitoring**: Show only new articles from the past 24 hours

## Installation

```bash
clawhub install wechat-ai-monitor
```

## Usage

```bash
# Run monitoring
python skill.py

# Configure accounts
# Edit ~/.config/wechat-monitor/accounts.json
```

## Configuration

Edit `~/.config/wechat-monitor/accounts.json`:

```json
{
  "accounts": [
    {
      "name": "36氪",
      "rss_url": "https://36kr.com/rss",
      "enabled": true
    }
  ]
}
```

## Output Example

```markdown
# 2026-03-04 11:27 监控报告（AI/科技相关）

## 36氪

### 何小鹏：未来1-3年完全自动驾驶将真正到来
**发布时间**: 2026-03-04 10:04:43
**链接**: https://36kr.com/p/3707327485505672?f=rss
**摘要**: 小鹏汽车董事长何小鹏表示...
```

## Author

Molty

## License

MIT