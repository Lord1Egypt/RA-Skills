# Daily Stock Analysis for OpenClaw

> 基于 LLM 的股票智能分析 Skill，为 OpenClaw 提供 A股/港股/美股 技术面分析和 AI 决策建议。

## 🎯 项目定位

本项目是 [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 的 **OpenClaw Skill 适配版**。

与原版相比，本项目的特点：
- ✅ **OpenClaw 原生集成** - 直接作为 Skill 调用
- ✅ **模块化设计** - 可独立使用或与 market-data skill 配合
- ✅ **简化依赖** - 核心功能零配置即可运行
- ✅ **开源友好** - MIT 协议，欢迎贡献

## 🚀 快速开始

### 安装

```bash
cd ~/workspace/skills/
git clone https://github.com/yourusername/stock-daily-analysis.git

# 安装依赖
pip3 install akshare pandas numpy requests
```

### 配置

```bash
cp config.example.json config.json
# 编辑 config.json 填入你的 API Key
```

### 使用

```python
from scripts.analyzer import analyze_stock, analyze_stocks

# 分析单只股票
result = analyze_stock('600519')
print(result['ai_analysis']['operation_advice'])  # 买入/持有/观望

# 分析多只股票
results = analyze_stocks(['600519', 'AAPL', '00700'])
```

## 📊 功能特性

| 功能 | 状态 | 说明 |
|------|------|------|
| A股分析 | ✅ | 支持个股、ETF |
| 港股分析 | ✅ | 支持港股通标的 |
| 美股分析 | ✅ | 基础行情获取 |
| 技术面分析 | ✅ | MA/MACD/RSI/乖离率 |
| AI 决策建议 | ✅ | DeepSeek/Gemini |
| 市场数据源集成 | ✅ | 可选 [market-data skill](https://github.com/chjm-ai/openclaw-market-data) |

## 🏗️ 项目结构

```
stock-daily-analysis/
├── SKILL.md                 # OpenClaw Skill 定义
├── README.md                # 项目文档
├── LICENSE                  # MIT 许可证
├── config.example.json      # 配置示例
├── config.json              # 用户配置 (gitignore)
├── requirements.txt         # Python 依赖
└── scripts/
    ├── analyzer.py          # 主入口
    ├── data_fetcher.py      # akshare 数据获取
    ├── market_data_bridge.py # market-data skill 桥接
    ├── trend_analyzer.py    # 技术分析引擎
    ├── ai_analyzer.py       # AI 分析模块
    └── notifier.py          # 报告输出
```

## 🔧 配置说明

### AI 模型配置

**DeepSeek (推荐，国内可用)**
```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-your-deepseek-key",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  }
}
```

**Gemini (免费，需代理)**
```json
{
  "ai": {
    "provider": "gemini",
    "api_key": "your-gemini-key",
    "model": "gemini-3-flash-preview"
  }
}
```

### 数据源配置

**方案1：使用 akshare (默认)**
```json
{
  "data": {
    "use_market_data_skill": false
  }
}
```

**方案2：使用 market-data skill (推荐用于 ETF)**
```json
{
  "data": {
    "use_market_data_skill": true,
    "market_data_skill_path": "../market-data"
  }
}
```

## 🤝 与 market-data skill 集成

如果你的 OpenClaw 已安装 [market-data skill](https://github.com/chjm-ai/openclaw-market-data)，本项目可自动调用其数据源：

```bash
workspace/skills/
├── market-data/          # 已安装
└── stock-daily-analysis/ # 本项目
```

配置 `use_market_data_skill: true` 后，ETF 数据将通过 market-data skill 获取，稳定性更好。

### 安装 market-data skill

```bash
cd ~/workspace/skills/
git clone https://github.com/chjm-ai/openclaw-market-data.git market-data
```

### 启用集成

```json
{
  "data": {
    "use_market_data_skill": true,
    "market_data_skill_path": "../market-data"
  }
}
```

## 📈 返回数据格式

```python
{
    'code': '600519',
    'name': '贵州茅台',
    'technical_indicators': {
        'trend_status': '强势多头',
        'ma5': 1500.0,
        'ma10': 1480.0,
        'ma20': 1450.0,
        'bias_ma5': 2.5,
        'macd_status': '金叉',
        'rsi_status': '强势买入',
        'buy_signal': '买入',
        'signal_score': 75,
        'signal_reasons': [...],
        'risk_factors': [...]
    },
    'ai_analysis': {
        'sentiment_score': 75,
        'trend_prediction': '强势多头',
        'operation_advice': '买入',
        'confidence_level': '高',
        'analysis_summary': '多头排列 | MACD金叉 | 量能配合',
        'target_price': '1550',
        'stop_loss': '1420'
    }
}
```

## 🛠️ 开发计划

- [ ] 支持更多数据源 (Tushare, Baostock)
- [ ] 添加板块分析功能
- [ ] 支持自定义策略回测
- [ ] WebUI 管理界面
- [ ] 支持更多推送渠道

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## ⚠️ 免责声明

本项目仅供学习研究使用，不构成任何投资建议。股市有风险，投资需谨慎。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 数据来源：[akshare](https://github.com/akfamily/akshare)
- 灵感来源：[ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)
- 平台支持：[OpenClaw](https://openclaw.ai)

---

**Made with ❤️ for OpenClaw**
