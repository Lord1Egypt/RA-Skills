# 🦞 Trump Mood & T-Index Dashboard

特朗普发帖情绪与市场敏感度实时监控面板

## 🚀 快速开始

### 1. 安装依赖

```bash
cd trump_mood_dashboard
pip install -r requirements.txt
```

### 2. 启动面板

```bash
streamlit run app.py
```

然后打开浏览器访问 `http://localhost:8501`

## 📊 功能

- **实时情绪分析**: 基于NLP的情绪评分 (-10 到 +10)
- **T-Index市场敏感度**: 市场敏感关键词检测 (0-100)
- **实时K线图**: Plotly交互式图表
- **风险预警**: CRITICAL/HIGH/ELEVATED/WATCH/LOW 五级风险
- **关键词提取**: 自动识别高影响词汇
- **市场数据**: SPX/VIX 实时行情（需要网络）

## 📁 文件结构

```
trump_mood_dashboard/
├── app.py              # Streamlit 前端
├── mood_analyzer.py    # 核心分析引擎
├── requirements.txt    # 依赖
└── README.md          # 说明
```

## 🔧 扩展

### 添加真实数据源

在 `mood_analyzer.py` 中添加数据抓取:

```python
# 示例：添加 Truth Social API
def fetch_truth_social():
    # 调用 API 获取特朗普最新帖子
    # 返回帖子列表
    pass
```

### 添加更多市场指标

```python
# 添加更多ETF/个股
market_assets = {
    'SPY': '标普500 ETF',
    'QQQ': '纳斯达克100 ETF',
    'DXY': '美元指数',
    'TLT': '20年期国债'
}
```

## ⚠️ 免责声明

本工具仅供研究和娱乐目的，不构成投资建议。使用风险自负。
