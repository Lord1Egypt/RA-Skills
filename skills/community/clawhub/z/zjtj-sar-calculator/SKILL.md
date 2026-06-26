---
name: zjtj-sar-calculator
description: 基于A股行情数据计算SAR抛物线指标，并用机构资金流向近似替代ZJTJ庄家抬轿指标，实现四维选股策略。
version: 1.0.0
---

# ZJTJ + SAR 指标计算工具

本工具通过Python计算SAR指标，并用机构资金流向近似替代ZJTJ，帮助实现四维选股策略。

## 核心功能

### 1. SAR指标计算

SAR（抛物线转向指标）计算逻辑：

```python
def calculate_sar(high_prices, low_prices, close_prices, af_start=0.02, af_increment=0.02, af_max=0.2):
    """
    计算SAR指标
    
    参数:
    - high_prices: 最高价列表
    - low_prices: 最低价列表
    - close_prices: 收盘价列表
    - af_start: 初始加速因子 (默认0.02)
    - af_increment: 加速因子增量 (默认0.02)
    - af_max: 最大加速因子 (默认0.2)
    
    返回:
    - sar_values: SAR值列表
    - trend: 趋势方向 (1=上涨, -1=下跌)
    """
    n = len(high_prices)
    if n < 2:
        return [], 0
    
    # 初始化
    sar = [low_prices[0]]
    trend = 1  # 假设初始为上涨
    af = af_start
    ep = high_prices[0]  # 极值点
    
    for i in range(1, n):
        if trend == 1:  # 上涨趋势
            sar_val = sar[-1] + af * (ep - sar[-1])
            
            if low_prices[i] < sar_val:  # 趋势反转
                trend = -1
                sar.append(low_prices[i])
                ep = low_prices[i]
                af = af_start
            else:
                sar.append(sar_val)
                if high_prices[i] > ep:
                    ep = high_prices[i]
                    af = min(af + af_increment, af_max)
        else:  # 下跌趋势
            sar_val = sar[-1] + af * (ep - sar[-1])
            
            if high_prices[i] > sar_val:  # 趋势反转
                trend = 1
                sar.append(high_prices[i])
                ep = high_prices[i]
                af = af_start
            else:
                sar.append(sar_val)
                if low_prices[i] < ep:
                    ep = low_prices[i]
                    af = min(af + af_increment, af_max)
    
    return sar, trend
```

### 2. ZJTJ近似替代方案

由于ZJTJ是通达信付费指标，用以下免费数据近似：

| 替代指标 | 数据来源 | 说明 |
|---------|---------|------|
| **机构资金净流入** | AkShare stock_individual_fund_flow | 大单/超大单净流入 |
| **股东人数变化** | 股东人数数据 | 股东减少=筹码集中 |
| **户均持股** | 股东数据 | 户均持股增加=控盘增强 |
| **持仓机构数** | 机构持股数据 | 机构越多越靠谱 |

### 3. 综合选股函数

```python
import akshare as ak
import pandas as pd
import numpy as np

def get_stock_data(stock_code, days=60):
    """获取个股K线数据"""
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=(pd.Timestamp.now() - pd.Timedelta(days=days)).strftime("%Y%m%d"),
        end_date=pd.Timestamp.now().strftime("%Y%m%d"),
        adjust="qfq"
    )
    return df

def calculate_zjtj_signal(stock_code):
    """
    计算ZJTJ近似信号
    返回: 信号强度 (0-100), 信号颜色
    """
    try:
        # 获取资金流向数据
        fund_flow = ak.stock_individual_fund_flow(stock=stock_code, market="sh")
        
        # 计算大单净流入占比
        if len(fund_flow) > 0:
            net_inflow = fund_flow.iloc[-1].get('大单净流入', 0)
            # 简化逻辑：净流入>0说明有主力关注
            if net_inflow > 100000000:  # 1亿+
                return 80, "紫色"  # 高度控盘
            elif net_inflow > 50000000:  # 5000万+
                return 60, "红色"  # 有庄
            elif net_inflow > 10000000:  # 1000万+
                return 30, "黄色"  # 开始控盘
            else:
                return 0, "白色"  # 无庄
    except:
        return 0, "白色"

def analyze_stock(stock_code):
    """
    综合分析一只股票
    返回: 选股建议
    """
    # 获取数据
    df = get_stock_data(stock_code)
    if df is None or len(df) < 30:
        return None
    
    # 计算SAR
    highs = df['最高'].values
    lows = df['最低'].values
    closes = df['收盘'].values
    
    sar_values, trend = calculate_sar(highs, lows, closes)
    
    # 获取ZJTJ近似信号
    zjtj_score, zjtj_color = calculate_zjtj_signal(stock_code)
    
    # 获取成交量
    volume_today = df.iloc[-1]['成交量']
    volume_yesterday = df.iloc[-2]['成交量'] if len(df) > 1 else volume_today
    volume_ratio = volume_today / volume_yesterday if volume_yesterday > 0 else 1
    
    # 整理结果
    result = {
        'code': stock_code,
        'sar_trend': '上涨' if trend == 1 else '下跌',
        'sar_value': sar_values[-1] if sar_values else None,
        'price_above_sar': closes[-1] > sar_values[-1] if sar_values else False,
        'zjtj_signal': zjtj_color,
        'zjtj_score': zjtj_score,
        'volume_ratio': volume_ratio,
        'volume_increasing': volume_ratio > 1.3,
    }
    
    # 判断是否符合四维选股条件
    conditions = []
    if zjtj_color in ['黄色', '红色', '紫色']:
        conditions.append("✅ ZJTJ有庄")
    if trend == 1:
        conditions.append("✅ SAR上涨趋势")
    if volume_ratio > 1.3:
        conditions.append("✅ 成交量放量")
    
    result['conditions'] = conditions
    result['recommend'] = len(conditions) >= 2
    
    return result

def batch_screener(stock_list):
    """
    批量选股
    stock_list: 股票代码列表
    """
    results = []
    for code in stock_list:
        try:
            result = analyze_stock(code)
            if result and result['recommend']:
                results.append(result)
        except Exception as e:
            print(f"Error processing {code}: {e}")
    
    # 按ZJTJ分数排序
    results.sort(key=lambda x: x['zjtj_score'], reverse=True)
    return results
```

## 使用示例

### 单只股票分析

```python
# 分析一只股票
result = analyze_stock("000001")
print(f"股票: {result['code']}")
print(f"SAR趋势: {result['sar_trend']}")
print(f"价格在SAR上方: {result['price_above_sar']}")
print(f"ZJTJ信号: {result['zjtj_signal']}")
print(f"成交量放大: {result['volume_increasing']}")
print(f"选股条件: {result['conditions']}")
print(f"推荐买入: {result['recommend']}")
```

### 批量选股

```python
# 热门股票列表
stocks = ["000001", "600519", "300750", "002594", "600036"]

# 批量筛选
candidates = batch_screener(stocks)

# 打印结果
for stock in candidates:
    print(f"{stock['code']}: ZJTJ={stock['zjtj_signal']}, SAR={stock['sar_trend']}, 放量={stock['volume_increasing']}")
```

## 四维选股判断逻辑

| 维度 | 条件 | 得分 |
|-----|------|-----|
| ZJTJ | 黄色/红色/紫色 | +30 |
| SAR | 上涨趋势 + 价格在SAR上方 | +30 |
| 成交量 | 今日量/昨日量 > 1.3 | +20 |
| 市场情绪 | 涨停20-80家 | +20 |

**总分 >= 60分 → 建议买入**

## 注意事项

1. 数据来源：AkShare（免费API），可能不稳定
2. ZJTJ为近似替代，与通达信原版有差异
3. SAR计算参数可调整（af_start, af_max等）
4. 建议结合其他分析方法综合判断

## 依赖安装

```bash
pip install akshare pandas numpy
```

---

## 触发场景

- "计算SAR指标"
- "ZJTJ指标"
- "四维选股"
- "帮我分析股票"
