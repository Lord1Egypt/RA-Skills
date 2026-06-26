# Stock Analyzer Skill

股票分析工具：获取实时数据、计算技术指标、基本面分析、价格预测

## Features

- 📈 **实时股价数据**：获取股票历史价格、成交量
- 📊 **技术指标分析**：MA、MACD、RSI、KDJ、布林带
- 💰 **基本面数据**：PE、PB、市值、营收、利润
- 🔮 **价格预测**：基于历史数据的简单趋势预测
- 📄 **生成分析报告**：输出 Markdown 格式的详细报告
- 🖼️ **图表生成**：可选的 K 线图和技术指标图

## Installation

```bash
# 克隆仓库或复制技能目录
cp -r stock-analyzer ~/.openclaw/skills/

# 安装依赖（需要 Python 3.8+）
pip install yfinance pandas numpy matplotlib
```

## Usage

### 基本分析
```bash
stock-analyzer analyze --symbol AAPL
```

### 完整报告（含图表）
```bash
stock-analyzer analyze --symbol AAPL --report full --charts
```

### 仅技术指标
```bash
stock-analyzer analyze --symbol AAPL --indicators ma,rsi,macd
```

### 基本面分析
```bash
stock-analyzer fundamentals --symbol AAPL
```

### 价格预测
```bash
stock-analyzer predict --symbol AAPL --days 5
```

## Command-Line Options

**analyze 命令**：
- `--symbol/-s`：股票代码（必填，如 AAPL、MSFT、600519.SS）
- `--period/-p`：数据周期（1d/5d/1mo/3mo/6mo/1y/2y/5y/10y，默认：6mo）
- `--indicators/-i`：技术指标列表，逗号分隔（默认：ma,rsi,macd,bbands）
- `--report/-r`：报告类型（summary/full，默认：summary）
- `--charts/-c`：生成图表（PNG 格式）

**fundamentals 命令**：
- `--symbol/-s`：股票代码（必填）
- `--locale`：数据语言（zh/en，默认：en）

**predict 命令**：
- `--symbol/-s`：股票代码（必填）
- `--days/-d`：预测天数（1-30，默认：5）
- `--method/-m`：预测方法（linear/prophet，默认：linear）

## Output

### 分析报告示例（Markdown）
```
# AAPL 股票分析报告

## 基本信息
- 公司：Apple Inc.
- 当前价格：$178.52
- 市值：$2.78T

## 技术指标
- MA(20): $175.23 (上涨)
- RSI(14): 58.65 (中性)
- MACD: 0.45 (看涨)

## 信号
- ✅ 短期趋势：上涨
- ⚠️ RSI 接近超买
- ✅ MACD 金叉

## 建议
- 短期：持有/买入
- 中期：看涨
- 风险等级：中等
```

## Configuration

数据源：Yahoo Finance（免费，无需 API Key）

可选配置文件：`~/.openclaw/secrets/stock-analyzer.json`
```json
{
  "default_period": "6mo",
  "default_indicators": ["ma", "rsi", "macd"],
  "chart_style": "dark"
}
```

## Requirements

- Python 3.8+
- yfinance
- pandas
- numpy
- matplotlib（图表功能）

## Limitations

- 仅支持公开交易的股票
- 中国 A 股需添加 `.SS`（上交所）或 `.SZ`（深交所）后缀
- 预测功能基于历史数据，不构成投资建议
- 数据延迟约 15 分钟

## Safety

此工具仅用于技术分析和学习目的，不提供投资建议。投资有风险，决策需谨慎。

## Roadmap

- [ ] 添加更多技术指标（ATR、OBV、CMF）
- [ ] 支持批量分析多只股票
- [ ] 实现基于机器学习的预测模型
- [ ] 支持实时监控和预警
- [ ] 添加回测功能
- [ ] 支持中国 A 股、港股、其他国际市场

## License

MIT