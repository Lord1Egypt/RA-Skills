# Football Betting Analyzer 足彩分析助手

专业的足球比赛数据分析和投注决策支持工具。

## 功能特性

- 📊 **基本面分析**: 球队战绩、伤停、主客场表现
- 📈 **赔率面分析**: 亚盘、欧赔、凯利指数
- 🎯 **智能预测**: 基于多维度数据的胜平负预测
- 💰 **资金管理**: 投注比例建议、风险控制
- 🔗 **串关组合**: 自动生成最优串关方案

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置 API Key (可选)

```bash
export FOOTBALL_API_KEY="your_api_key_here"
```

获取 API Key: [API-Football](https://www.api-football.com/)

### 运行演示

```bash
python analyzer.py --demo
```

## 使用示例

### 1. 分析单场比赛

```python
from analyzer import FootballBettingAnalyzer

analyzer = FootballBettingAnalyzer(api_key="your_key")
analysis = analyzer.analyze_match(fixture_id=12345)
analyzer.print_analysis(analysis)
```

### 2. 赔率分析

```python
from odds_analyzer import ComprehensiveOddsAnalyzer

analyzer = ComprehensiveOddsAnalyzer()
result = analyzer.analyze_match(
    home_win_odds=1.75,
    draw_odds=3.60,
    away_win_odds=4.50,
    model_probs={"home": 0.58, "draw": 0.24, "away": 0.18}
)
print(analyzer.generate_betting_advice(result))
```

### 3. 资金管理

```python
from utils import BankrollManager

manager = BankrollManager(initial_bankroll=1000)
manager.place_bet("曼城vs阿森纳", "主胜", stake=50, odds=1.75)
stats = manager.get_statistics()
print(f"当前资金: {stats['current_bankroll']}")
```

## 命令行使用

```bash
# 查看今日比赛
python analyzer.py --today

# 分析指定比赛
python analyzer.py --match 12345

# 运行演示
python analyzer.py --demo
```

## 数据源

- **API-Football**: 全球足球数据，免费版 100 请求/天
- **Football-Data.org**: 欧洲主流联赛，免费版 10 请求/分钟

## 免责声明

⚠️ 本工具仅供数据分析参考，不构成投注建议。足球比赛具有不确定性，请理性购彩，量力而行。

## License

MIT
