# B01 周报模板

适用于：每周业务汇报、周度数据复盘。

---

## 模板结构

```
┌─────────────────────────────────────────────────────┐
│  BANNER: 业务周报 + 周期（如：2026年第11周）          │
├─────────────────────────────────────────────────────┤
│  KPI 卡片行（4格）                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │ 核心指标1 │ │ 核心指标2 │ │ 核心指标3 │ │ 核心指标4 ││
│  │ 环比变化  │ │ 环比变化  │ │ 环比变化  │ │ 环比变化  ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘│
├─────────────────────────────────────────────────────┤
│  趋势图（全宽）                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  日/周趋势折线图 + 均线 + 峰值标注            │   │
│  └─────────────────────────────────────────────┘   │
│  洞察文字框                                         │
├────────────────────────────┬────────────────────────┤
│  分类排名                  │  构成分析              │
│  ┌────────────────────┐   │  ┌────────────────────┐│
│  │  横向条形图        │   │  │  堆叠条形图/环形图  ││
│  │  Top N 排名        │   │  │  各维度占比        ││
│  └────────────────────┘   │  └────────────────────┘│
├────────────────────────────┼────────────────────────┤
│  周对比                    │  明细表格              │
│  ┌────────────────────┐   │  ┌────────────────────┐│
│  │  本周 vs 上周对比  │   │  │  关键数据明细      ││
│  │  分组条形图        │   │  │  （带条件格式）    ││
│  └────────────────────┘   │  └────────────────────┘│
├────────────────────────────┴────────────────────────┤
│  下周计划 & 风险提示                                 │
└─────────────────────────────────────────────────────┘
```

---

## 数据需求

### 必需数据
| 数据 | 字段 | 说明 |
|------|------|------|
| 每日趋势 | date, value | 近14天数据，用于展示本周vs上周 |
| 分类数据 | category, value | 排名展示 |
| 构成数据 | dimension, series, value | 占比分析 |

### 可选数据
| 数据 | 用途 |
|------|------|
| 上周同期数据 | 计算环比 |
| 目标值 | 显示目标达成进度 |

---

## 核心代码

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_weekly_report(df_daily, df_category, output_path):
    """生成周报"""
    
    # 计算本周/上周汇总
    this_week = df_daily[-7:]['value'].sum()
    last_week = df_daily[-14:-7]['value'].sum()
    mom = (this_week - last_week) / last_week * 100
    
    # KPI 数据
    kpis = [
        {'name': '本周总量', 'value': f'{this_week:,.0f}', 'change': mom},
        {'name': '日均量', 'value': f'{this_week/7:,.0f}', 'change': mom},
        {'name': '峰值', 'value': f'{df_daily[-7:]["value"].max():,.0f}', 'change': None},
        {'name': '谷值', 'value': f'{df_daily[-7:]["value"].min():,.0f}', 'change': None},
    ]
    
    # 趋势图
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(df_daily['date'], df_daily['value'], linewidth=2, color='#3b82f6')
    # 标注本周区域
    ax.axvspan(df_daily.iloc[-7]['date'], df_daily.iloc[-1]['date'], 
               alpha=0.1, color='#10b981', label='本周')
    ax.legend()
    img_trend = fig_to_b64(fig)
    plt.close(fig)
    
    # 排名图
    img_ranking = generate_bar_chart(df_category)
    
    # 生成洞察
    insights = generate_trend_insight(df_daily[-14:])
    
    # 拼装 HTML
    html = render_template('weekly', kpis=kpis, img_trend=img_trend, 
                           img_ranking=img_ranking, insights=insights)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
```

---

## 洞察生成规则

### 趋势洞察
```
本周共 {total:,.0f}，环比{'增长' if mom > 0 else '下降'} {abs(mom):.1f}%。
近7日均值 {avg:,.0f}，峰值出现在 {peak_day}（{peak_val:,.0f}）。
```

### 排名洞察
```
TOP1 {top_category} 贡献 {top_pct:.1f}%，TOP3 合计占比 {top3_pct:.1f}%。
```

### 风险提示
```
⚠️ {risk_category} 连续下滑，需关注原因。
⚠️ 末位 {bottom_category} 表现低迷，建议优化。
```

---

## 输出示例

**KPI 卡片：**
```
本周总量    日均量      峰值       谷值
12,450     1,778      2,340      1,120
↑ 8.3%     ↑ 8.3%     
```

**趋势洞察：**
```
本周共 12,450，环比增长 8.3%。近7日均值 1,778，
峰值出现在 周六（2,340），周末效应明显。
建议：周五备货调度，迎接周末高峰。
```
