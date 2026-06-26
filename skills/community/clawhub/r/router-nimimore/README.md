# Router NIMIMORE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Smart model router for OpenClaw. Automatically selects the optimal AI model based on query characteristics, balancing cost and performance.

## ✨ Features

- 🎯 **Smart Routing** - Automatically selects best model for each query
- 💰 **Cost Optimization** - Save up to 85% on API costs
- 🚀 **Multi-Provider** - Supports Moonshot and Bailian
- 📊 **Query Analysis** - Understands query characteristics
- ⚡ **Fast & Lightweight** - No external dependencies

## 📦 Installation

### Via ClawHub

```bash
clawhub install router-nimimore
```

### Manual

```bash
git clone https://github.com/franco-user/router-nimimore.git
cd router-nimimore
```

## 🚀 Usage

### Command Line

```bash
# Route a query
python scripts/router.py --query "帮我写个Python函数"

# Run demo
python scripts/router.py --demo

# With context length
python scripts/router.py --query "总结文档" --context-length 5000
```

### Python API

```python
from scripts.router import SmartRouter

router = SmartRouter()
result = router.route("帮我分析股票走势")

print(result['selected_model'])  # moonshot/kimi-k2.5
print(result['cost_savings'])    # 0.007
```

## 🎯 Routing Logic

| Query Type | Selected Model | Cost | Savings |
|-----------|----------------|------|---------|
| Simple (你好/谢谢) | bailian/qwen-turbo | $0.002 | 87% |
| Code tasks | bailian/qwen-max | $0.008 | 47% |
| Complex reasoning | moonshot/kimi-k2.5 | $0.015 | 0% |
| Long context | moonshot/kimi-k2.5 | $0.015 | 0% |

## 📊 Example Output

```json
{
  "success": true,
  "query": "帮我写个Python函数",
  "features": {
    "is_simple": false,
    "is_code": true,
    "is_chinese": true,
    "is_reasoning": false
  },
  "selected_model": "bailian/qwen-max",
  "model_info": {
    "tier": "standard",
    "cost_per_1k": 0.008
  },
  "cost_savings": 0.007,
  "savings_percent": 46.7
}
```

## 🛠️ Supported Models

| Model | Provider | Tier | Cost/1k tokens |
|-------|----------|------|----------------|
| kimi-k2.5 | Moonshot | Premium | $0.015 |
| qwen-max | Bailian | Standard | $0.008 |
| qwen-plus | Bailian | Standard | $0.004 |
| qwen-turbo | Bailian | Economy | $0.002 |

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenClaw - AI assistant platform
- Moonshot - Kimi models
- Alibaba Cloud - Bailian models
