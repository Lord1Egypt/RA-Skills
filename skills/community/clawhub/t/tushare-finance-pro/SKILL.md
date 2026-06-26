---
name: tushare-pro
description: Tushare Pro 金融数据接口 - A股/港股/美股/基金/期货/债券/宏观经济，220+数据接口，支持财务报表、估值分析、行业研究
metadata:
  openclaw:
    emoji: "📈"
    requires:
      pip: ["tushare>=1.2.89", "pandas>=1.5"]
    install:
      - id: pip-install
        kind: pip
        packages: ["tushare>=1.2.89", "pandas>=1.5"]
        label: "安装 Tushare 依赖"
keywords:
  - tushare
  - A股
  - 财务报表
  - 估值分析
  - 宏观经济
  - 量化投资
---

# Tushare Pro 金融数据助手

## 功能特性

- 股票行情查询（自动重试机制）
- 基础财务数据
- 宏观经济数据
- 全量 220+ 接口
- 自动财务报表
- DCF 估值模型
- 行业对比分析
- 定时数据推送
- **智能错误处理**
- **Token 验证**

## 快速开始

```bash
pip install tushare pandas
export TUSHARE_TOKEN="your_token"
```

## 股票行情

```python
import tushare as ts

pro = ts.pro_api()

# 日线行情
df = pro.daily(ts_code='000001.SZ', start_date='20240101', end_date='20241231')

# 周线行情
df = pro.weekly(ts_code='000001.SZ')

# 月线行情
df = pro.monthly(ts_code='000001.SZ')
```

### 基础财务

```python
# 财务指标
df = pro.fina_indicator(ts_code='000001.SZ')

# 利润表
df = pro.income(ts_code='000001.SZ')

# 资产负债表
df = pro.balancesheet(ts_code='000001.SZ')

# 现金流量表
df = pro.cashflow(ts_code='000001.SZ')
```

### 宏观经济

```python
# GDP
df = pro.gdp()

# CPI
df = pro.cpi()

# PMI
df = pro.pmi()

# 货币供应
df = pro.m2()
```

## 自动财务报表生成

```python
def generate_financial_report(ts_code):
    """生成完整财务报表"""
    report = {}
    
    # 基本信息
    info = pro.stock_basic(ts_code=ts_code, fields='ts_code,name,industry,market')
    report['info'] = info.iloc[0].to_dict()
    
    # 财务指标
    indicator = pro.fina_indicator(ts_code=ts_code, period='20231231')
    report['indicator'] = indicator.iloc[0].to_dict() if not indicator.empty else {}
    
    # 利润表
    income = pro.income(ts_code=ts_code, period='20231231')
    report['income'] = income.iloc[0].to_dict() if not income.empty else {}
    
    # 资产负债表
    balance = pro.balancesheet(ts_code=ts_code, period='20231231')
    report['balance'] = balance.iloc[0].to_dict() if not balance.empty else {}
    
    return report
```

### DCF 估值模型

```python
def dcf_valuation(ts_code, growth_rate=0.15, wacc=0.1, terminal_growth=0.03):
    """DCF 估值模型"""
    # 获取历史财务数据
    income = pro.income(ts_code=ts_code)
    
    if income.empty:
        return None
    
    latest = income.iloc[0]
    base_revenue = latest.get('revenue', 0)
    net_margin = latest.get('net_profit', 0) / base_revenue if base_revenue > 0 else 0
    
    # 预测未来5年现金流
    cash_flows = []
    for year in range(1, 6):
        revenue = base_revenue * (1 + growth_rate) ** year
        net_profit = revenue * net_margin
        cash_flows.append(net_profit)
    
    # 计算终值
    terminal_value = cash_flows[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    
    # 折现
    pv_sum = sum(cf / (1 + wacc) ** i for i, cf in enumerate(cash_flows, 1))
    pv_terminal = terminal_value / (1 + wacc) ** 5
    
    total_value = pv_sum + pv_terminal
    
    return {
        'company_value': total_value,
        'cash_flows': cash_flows,
        'terminal_value': terminal_value,
        'assumptions': {
            'growth_rate': growth_rate,
            'wacc': wacc,
            'terminal_growth': terminal_growth,
            'net_margin': net_margin
        }
    }
```

### 行业对比分析

```python
def industry_comparison(industry, top_n=10):
    """行业对比分析"""
    # 获取行业股票列表
    stocks = pro.stock_basic(industry=industry, list_status='L', 
                            fields='ts_code,name,market_cap')
    
    if stocks.empty:
        return None
    
    # 按市值排序
    stocks = stocks.sort_values('market_cap', ascending=False).head(top_n)
    
    results = []
    for _, stock in stocks.iterrows():
        try:
            indicator = pro.fina_indicator(ts_code=stock['ts_code'], period='20231231')
            if not indicator.empty:
                results.append({
                    'ts_code': stock['ts_code'],
                    'name': stock['name'],
                    'market_cap': stock['market_cap'],
                    'roe': indicator.iloc[0].get('roe', None),
                    'net_profit_margin': indicator.iloc[0].get('netprofit_margin', None),
                    'revenue_growth': indicator.iloc[0].get('or_yoy', None)
                })
        except:
            continue
    
    return pd.DataFrame(results)
```

### 定时数据推送

在 OpenClaw 配置定时任务：

```json
{
  "cron": {
    "jobs": [
      {
        "id": "daily-market",
        "schedule": "0 16 * * 1-5",
        "prompt": "生成今日A股市场日报",
        "channel": "feishu"
      },
      {
        "id": "weekly-report",
        "schedule": "0 9 * * 1",
        "prompt": "生成本周行业研究报告",
        "channel": "feishu"
      }
    ]
  }
}
```

## 接口速查表

| 类别 | 接口数 | 常用接口 |
|------|--------|----------|
| 股票数据 | 39 | daily, weekly, monthly, stock_basic |
| 指数数据 | 18 | index_daily, index_weight |
| 基金数据 | 11 | fund_nav, fund_daily |
| 期货期权 | 16 | fut_daily, opt_daily |
| 宏观经济 | 10 | gdp, cpi, pmi, m2 |
| 港股美股 | 23 | hk_daily, us_daily |
| 债券数据 | 16 | bond_daily, bond_cov |

## 配置说明

1. 注册 Tushare Pro: https://tushare.pro
2. 获取 API Token
3. 设置环境变量: `export TUSHARE_TOKEN="your_token"`

## 风险提示

1. 数据来源: Tushare Pro，需遵守使用协议
2. 数据延迟: 部分数据有 15 分钟延迟
3. 投资风险: 数据仅供参考，不构成投资建议
