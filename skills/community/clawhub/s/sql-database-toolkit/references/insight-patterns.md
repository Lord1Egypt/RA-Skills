# 洞察生成模式库

自动从数据中发现关键洞察并生成文字描述。

---

## 洞察类型

| 类型 | 触发条件 | 模板 |
|------|---------|------|
| 趋势洞察 | 时间序列数据 | "近N日/月呈上升/下降趋势" |
| 对比洞察 | 环比/同比数据 | "环比增长X%，同比增加Y%" |
| 排名洞察 | 排名数据 | "X排名第一，贡献Y%" |
| 异常洞察 | 异常值检测 | "X异常偏高/偏低，需关注" |
| 占比洞察 | 构成数据 | "TOP3占比X%，集中度高" |
| 相关洞察 | 相关性分析 | "X与Y呈正/负相关" |
| 预测洞察 | 趋势预测 | "按当前趋势，预计下月达到X" |

---

## 洞察生成函数

### 趋势洞察
```python
def generate_trend_insight(df, date_col='date', value_col='value'):
    """生成趋势洞察"""
    values = df[value_col]
    dates = df[date_col]
    
    # 计算趋势
    first_half = values[:len(values)//2].mean()
    second_half = values[len(values)//2:].mean()
    trend_pct = (second_half - first_half) / first_half * 100
    
    # 最近趋势
    recent_avg = values[-7:].mean()
    overall_avg = values.mean()
    recent_trend = (recent_avg - overall_avg) / overall_avg * 100
    
    # 峰值低谷
    max_val = values.max()
    min_val = values.min()
    max_date = dates[values.idxmax()]
    min_date = dates[values.idxmin()]
    
    if trend_pct > 5:
        trend_desc = f"整体呈**上升趋势**，后半期较前半期增长 {trend_pct:.1f}%"
    elif trend_pct < -5:
        trend_desc = f"整体呈**下降趋势**，后半期较前半期下降 {abs(trend_pct):.1f}%"
    else:
        trend_desc = "整体**平稳**，无明显趋势"
    
    return f"""
    {trend_desc}。近7日均值较整体均值{'高出' if recent_trend > 0 else '低'} {abs(recent_trend):.1f}%。
    峰值出现在 {max_date.strftime('%m月%d日')}（{max_val:,.0f}），
    低谷出现在 {min_date.strftime('%m月%d日')}（{min_val:,.0f}）。
    """
```

### 环比洞察
```python
def generate_mom_insight(current, previous, metric_name='指标'):
    """生成环比洞察"""
    if previous == 0:
        return f"{metric_name}从0增长至{current:,.0f}"
    
    pct = (current - previous) / previous * 100
    direction = "增长" if pct > 0 else "下降"
    
    if abs(pct) > 20:
        alert = "⚠️ 变化幅度较大，需关注原因"
    elif abs(pct) > 10:
        alert = "📊 变化明显"
    else:
        alert = ""
    
    return f"{metric_name}环比{direction} {abs(pct):.1f}%，从 {previous:,.0f} 变化至 {current:,.0f}。{alert}"
```

### 排名洞察
```python
def generate_ranking_insight(df, category_col='category', value_col='value', top_n=3):
    """生成排名洞察"""
    df_sorted = df.sort_values(value_col, ascending=False)
    total = df[value_col].sum()
    
    top1 = df_sorted.iloc[0]
    top3_sum = df_sorted.iloc[:3][value_col].sum()
    top3_pct = top3_sum / total * 100
    
    insights = []
    insights.append(f"**{top1[category_col]}** 排名第一，贡献 {top1[value_col]:,.0f}（占比 {top1[value_col]/total*100:.1f}%）")
    
    if top3_pct > 60:
        insights.append(f"TOP3 占比高达 {top3_pct:.1f}%，集中度较高")
    elif top3_pct < 30:
        insights.append(f"TOP3 占比仅 {top3_pct:.1f}%，分布较分散")
    
    # 尾部分析
    bottom = df_sorted.iloc[-1]
    if bottom[value_col] / top1[value_col] < 0.1:
        insights.append(f"末位 **{bottom[category_col]}** 仅占首位的 {bottom[value_col]/top1[value_col]*100:.1f}%，差距明显")
    
    return "\n".join(insights)
```

### 异常洞察
```python
def generate_anomaly_insight(df, value_col='value', category_col=None, threshold=2):
    """生成异常洞察（基于标准差）"""
    mean = df[value_col].mean()
    std = df[value_col].std()
    
    anomalies = df[abs(df[value_col] - mean) > threshold * std]
    
    if len(anomalies) == 0:
        return None
    
    insights = []
    for _, row in anomalies.iterrows():
        z_score = (row[value_col] - mean) / std
        direction = "异常偏高" if z_score > 0 else "异常偏低"
        cat = f"**{row[category_col]}**" if category_col else f"第{row.name+1}项"
        insights.append(f"{cat} {direction}（偏离均值 {abs(z_score):.1f} 倍标准差）")
    
    return "\n".join(insights)
```

### 转化漏斗洞察
```python
def generate_funnel_insight(stages, values):
    """生成漏斗转化洞察"""
    insights = []
    
    # 整体转化率
    overall_conv = values[-1] / values[0] * 100
    insights.append(f"整体转化率 **{overall_conv:.1f}%**")
    
    # 各阶段转化率
    stage_rates = []
    for i in range(1, len(values)):
        rate = values[i] / values[i-1] * 100
        stage_rates.append((stages[i], rate))
    
    # 最大流失环节
    min_rate_idx = stage_rates.index(min(stage_rates, key=lambda x: x[1]))
    worst_stage = stage_rates[min_rate_idx]
    loss_rate = 100 - worst_stage[1]
    
    insights.append(f"最大流失环节：**{stages[min_rate_idx]}→{stages[min_rate_idx+1]}**，流失率 {loss_rate:.1f}%")
    
    # 优化建议
    if min_rate_idx == 0:
        insights.append("💡 建议：优化曝光渠道和素材，提升点击率")
    elif min_rate_idx == len(stages) - 2:
        insights.append("💡 建议：优化支付流程，降低最后一步流失")
    else:
        insights.append(f"💡 建议：分析 {stages[min_rate_idx+1]} 环节的用户行为，找出流失原因")
    
    return "\n".join(insights)
```

### 留存洞察
```python
def generate_retention_insight(cohort_df):
    """生成留存分析洞察"""
    insights = []
    
    # 次日留存
    day1_retention = cohort_df.iloc[:, 1].mean()
    insights.append(f"平均次日留存率 **{day1_retention:.1f}%**")
    
    # 7日留存
    if cohort_df.shape[1] > 7:
        day7_retention = cohort_df.iloc[:, 7].mean()
        insights.append(f"平均7日留存率 **{day7_retention:.1f}%**")
    
    # 趋势
    recent_cohorts = cohort_df.iloc[-4:, 1].mean()
    early_cohorts = cohort_df.iloc[:4, 1].mean()
    trend = (recent_cohorts - early_cohorts) / early_cohorts * 100
    
    if trend > 5:
        insights.append(f"📈 近期 cohorts 留存表现**提升** {trend:.1f}%")
    elif trend < -5:
        insights.append(f"📉 近期 cohorts 留存表现**下滑** {abs(trend):.1f}%，需关注")
    
    return "\n".join(insights)
```

---

## 洞察组合模板

### 高管摘要洞察
```python
def executive_summary_insight(kpis):
    """生成高管摘要洞察"""
    lines = ["📊 **核心发现**\n"]
    
    # 最关键指标
    key_metric = kpis[0]
    if key_metric['change'] > 10:
        lines.append(f"✅ {key_metric['name']}表现优异，环比增长 {key_metric['change']:.1f}%")
    elif key_metric['change'] < -10:
        lines.append(f"⚠️ {key_metric['name']}有所下滑，环比下降 {abs(key_metric['change']):.1f}%")
    
    # 其他关键指标
    for kpi in kpis[1:4]:
        direction = "↑" if kpi['change'] > 0 else "↓"
        lines.append(f"{direction} {kpi['name']}: {kpi['value']} ({kpi['change']:+.1f}%)")
    
    return "\n".join(lines)
```

### 行动建议模板
```python
def generate_action_items(insights, category='general'):
    """根据洞察生成行动建议"""
    action_templates = {
        'sales': [
            "重点投入 TOP3 品类，扩大优势",
            "分析末位品类，考虑调整或淘汰",
            "关注周末促销活动，提升日均销量"
        ],
        'conversion': [
            "优化最大流失环节的用户体验",
            "A/B 测试关键页面设计",
            "加强用户引导和提示"
        ],
        'retention': [
            "优化新用户引导流程",
            "建立用户激励机制",
            "分析流失用户特征，针对性召回"
        ],
        'finance': [
            "控制费用率，目标降至行业标准",
            "优化成本结构，提升毛利率",
            "加强现金流管理"
        ]
    }
    
    return action_templates.get(category, [
        "持续监控关键指标变化",
        "定期复盘分析结果",
        "根据数据调整策略"
    ])
```
