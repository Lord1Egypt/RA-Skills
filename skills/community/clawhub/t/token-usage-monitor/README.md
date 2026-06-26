# Token Usage Monitor - AI模型token用量监控工具

A powerful tool to track, analyze, and optimize AI model token usage and costs.

## 🌟 主要功能 / Key Features

### 📊 实时监控 / Real-time Monitoring
- Track token consumption per request, session, and model
- Monitor usage speed (tokens per second/minute)
- View live metrics including prompt tokens, completion tokens, and totals

### 📈 历史分析 / Historical Analysis
- Generate daily, weekly, or monthly usage reports
- Analyze trends across different models and applications
- Identify peak usage times and cost drivers

### ⚠️ 阈值警报 / Threshold Alerts
- Set custom usage limits for different models
- Receive notifications when limits are exceeded
- Multiple alert channels supported (chat, email, webhook)

### 💰 成本估算 / Cost Estimation
- Calculate approximate costs based on token usage
- Compare costs across different models and providers
- Optimize prompts to reduce token usage and expenses

## 🚀 快速开始 / Quick Start

### 安装 / Installation
```bash
# Install from ClawHub
clawhub install token-usage-monitor

# Or install from local package
clawhub install token-usage-monitor.skill
```

### 基本使用 / Basic Usage

```bash
# 查看当前会话使用情况 / Check current session usage
python scripts/token_usage_tracker.py --session

# 生成今日使用报告 / Generate daily usage report
python scripts/token_usage_tracker.py --report --period day

# 设置每日阈值（10万token） / Set daily threshold (100,000 tokens)
python scripts/token_usage_tracker.py --set-threshold --model doubao-seed --limit 100000

# 查看总体使用汇总 / View overall usage summary
python scripts/token_usage_tracker.py --summary
```

## 🔧 集成指南 / Integration Guide

### 自动跟踪 / Automatic Tracking

Integrate with your AI model calls to automatically track token usage:

```python
from skills.token-usage-monitor.scripts.token_usage_tracker import TokenUsageTracker

def call_ai_model(prompt, model="doubao-seed"):
    # Make the AI model call
    response = openclaw.call_model(prompt, model=model)
    
    # Extract token counts from metadata
    prompt_tokens = response.metadata.get("prompt_tokens", 0)
    completion_tokens = response.metadata.get("completion_tokens", 0)
    
    # Track the usage
    tracker = TokenUsageTracker()
    tracker.track_usage(openclaw.session_id, model, prompt_tokens, completion_tokens)
    
    return response
```

### 心跳集成 / Heartbeat Integration

Add to HEARTBEAT.md for periodic checks:

```markdown
# HEARTBEAT.md
- Check token usage thresholds hourly
- Generate daily report at 9:00 AM
```

## 📁 项目结构 / Project Structure

```
token-usage-monitor/
├── SKILL.md              # Skill metadata and documentation
├── scripts/
│   └── token_usage_tracker.py  # Main tracking script
├── references/
│   └── integration_guide.md    # Detailed integration instructions
└── README.md             # This file
```

## 📝 支持的模型 / Supported Models

- ✅ Volcengine Doubao (豆包)
- ✅ OpenAI GPT-4 / GPT-3.5-turbo
- ✅ Anthropic Claude-2
- ✅ Custom models (easily extendable)

## 🔧 自定义配置 / Configuration

### 模型定价 / Model Pricing

Edit the pricing in `token_usage.json`:

```json
"model_pricing": {
    "doubao-seed": 0.002 / 1000,
    "gpt-4": 0.03 / 1000,
    "claude-2": 0.0110 / 1000
}
```

### 警报设置 / Alert Configuration

Extend the `_check_thresholds` method in the tracker to add more alert channels:

```python
def _check_thresholds(self, model: str, tokens_used: int):
    # Add email, webhook, or other alert methods here
    send_email_alert(model, daily_total, threshold_limit)
    send_webhook_alert(model, daily_total, threshold_limit)
```

## 🤝 贡献指南 / Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 许可证 / License

This project is licensed under the MIT License.

## 📞 支持 / Support

If you encounter any issues or have questions, please:

1. Check the `references/integration_guide.md` for detailed documentation
2. Open an issue on the project repository
3. Contact the maintainers

---

**Happy tracking! 🚀**