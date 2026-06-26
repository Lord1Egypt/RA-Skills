# stock-selecter 选股技能包 v3.2.0

A股智能选股系统，整合 **11 种独立策略**，支持单策略筛选、多策略组合、综合评分排序。

## 策略清单

| 策略名 | 类型 | 核心条件 |
|--------|------|---------|
| `roe` | 基本面 | ROE ≥ 15% + ROA ≥ 5% |
| `dividend` | 基本面 | 股息率 ≥ 3% + 连续分红 3 年 + ROE ≥ 8% |
| `valuation` | 基本面 | PE ≤ 25 + PB ≤ 3 + PEG ≤ 1.5 |
| `growth` | 基本面 | 营收/净利双增 ≥ 20% + 毛利率 ≥ 30% |
| `cashflow_quality` | 基本面 | 经营现金流 ≥ 净利润（持续 3 期）+ 商誉 < 30% |
| `macd` | 技术面 | MACD 底背离 + K 线下行 + RSI 超卖 |
| `trend` | 技术面 | 均线多头排列 + R² ≥ 0.5 + ADX ≥ 25 |
| `bollinger` | 技术面 | 股价触及布林带下轨 + RSI 超卖 |
| `volume_surge` | 技术面 | 放量 ≥ 2 倍 + RSI ≤ 45 + 反弹 ≥ 3% |
| `low_position` | 技术面 | 价格分位 ≤ 25% + RSI ≤ 40 |
| `pattern` | 技术面 | 命中 K 线形态（双底/头肩底/早晨之星等） |
| `shareholder_concentration` | 筹码面 | 股东户数连续 3 期减少 + ROE ≥ 8% |

## 安装

```bash
pip install -r requirements.txt
```

## 配置

在 `config.json` 中填入你的 Tushare Token：

```json
{
  "token": "YOUR_TUSHARE_TOKEN_HERE"
}
```

获取 Token：[Tushare Pro](https://tushare.pro/register) 注册后免费获取。

## 使用方式

### 命令行

```bash
# 单策略筛选
python main.py --strategy roe --top 30

# 多策略交集（最严，同时满足所有条件）
python main.py --strategy roe,macd,dividend --mode and

# 多策略并集（宽松，任一满足即可）
python main.py --strategy roe,macd --mode or --top 50

# 综合评分（全策略打分，取总分最高）
python main.py --strategy all --mode score --top 50

# 技术面并发加速
python main.py --strategy macd,trend,bollinger --workers 8

# 生成 HTML 可视化报告
python main.py --strategy roe,macd,dividend --report
```

### Python API

```python
from main import execute

# 单策略
result = execute({"strategy": "roe", "roe_threshold": 15, "top_n": 30})

# 多策略 AND 交集
result = execute({
    "strategy": "roe,macd,dividend",
    "mode": "and",
    "top_n": 50
})

# 全策略评分
result = execute({
    "strategy": "all",
    "mode": "score",
    "top_n": 50,
    "report": True
})
```

## 目录结构

```
stock-selecter/
├── main.py                  # 统一入口（CLI + execute()）
├── SKILL.md                 # Skill 元数据
├── config.json             # Tushare Token 配置
├── requirements.txt        # Python 依赖
├── README.md               # 本文件
├── stock_utils.py          # 共享工具函数
├── stock_indicators.py     # 技术指标计算
├── strategies/
│   ├── base.py             # 策略基类（含并发引擎）
│   ├── roe.py             # ROE 盈利能力
│   ├── macd.py             # MACD 底背离
│   ├── dividend.py         # 高股息
│   ├── valuation.py        # 低估值
│   ├── growth.py           # 费雪成长股
│   ├── cashflow_quality.py # 现金流质量
│   ├── low_position.py     # 长期低位
│   ├── volume_surge.py     # 近期放量
│   ├── bollinger.py        # 布林带下轨
│   ├── trend.py            # 趋势分析
│   └── pattern.py          # K 线形态
└── utils/
    ├── loader.py           # 共享库加载器
    └── report.py           # HTML 报告生成器
```

## 注意事项

- 本工具仅供技术研究参考，不构成投资建议
- 数据来源为 Tushare，需自行注册获取 Token
- 策略评分基于历史数据，不代表未来表现
