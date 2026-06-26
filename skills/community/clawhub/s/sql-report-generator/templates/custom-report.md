# 自定义报告模板

适用于：专题分析、临时报告、自定义需求。

---

## 使用场景

- 不符合预设模板的特殊报告
- 用户指定了特定的章节结构
- 需要组合多种图表类型
- 品牌定制化报告

---

## 构建流程

### Step 1：收集需求
向用户确认：
1. 报告目的和受众
2. 必须包含的章节
3. 数据来源
4. 图表类型偏好
5. 品牌色/Logo

### Step 2：设计结构
根据需求设计报告布局：
```
┌─────────────────────────────────────┐
│  Section 1: 标题 + 简介              │
├─────────────────────────────────────┤
│  Section 2: 数据概览                 │
├─────────────────────────────────────┤
│  Section 3: 详细分析（图表 + 洞察）  │
├─────────────────────────────────────┤
│  Section 4: 结论和建议               │
└─────────────────────────────────────┘
```

### Step 3：选择组件
从组件库中选择需要的元素：

| 组件 | 用途 |
|------|------|
| KPI 卡片 | 核心指标展示 |
| 趋势图 | 时间序列分析 |
| 对比图 | 分类/维度对比 |
| 占比图 | 构成分析 |
| 相关图 | 变量关系 |
| 表格 | 明细数据 |
| 洞察框 | 文字总结 |

### Step 4：生成报告
根据确认的结构生成 HTML。

---

## 组件代码库

### KPI 卡片
```html
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-change {direction}">{change}</div>
</div>
```

### 图表区
```html
<div class="chart-section">
  <div class="section-title">{title}</div>
  <div class="chart-container">
    <img src="data:image/png;base64,{img_base64}">
  </div>
  <div class="insight">{insight_text}</div>
</div>
```

### 数据表格
```html
<div class="table-section">
  <div class="section-title">{title}</div>
  <table>
    <thead>{header_row}</thead>
    <tbody>{data_rows}</tbody>
  </table>
</div>
```

### 洞察框
```html
<div class="insight-box">
  <span class="insight-icon">📌</span>
  <div class="insight-content">{text}</div>
</div>
```

---

## 示例：用户留存分析报告

**用户需求：** 分析近 90 天新用户留存情况

**报告结构：**
```
1. 概览：新增用户数、次日留存、7日留存、30日留存
2. 趋势：每日新增用户趋势
3. Cohort 热力图：按注册周分组的留存矩阵
4. 分渠道留存对比
5. 留存影响因素分析
6. 优化建议
```

**生成代码：**
```python
# 1. 数据查询
df_new_users = pd.read_sql("""
    SELECT DATE(created_at) AS date, COUNT(*) AS new_users
    FROM users
    WHERE created_at >= DATE('now', '-90 days')
    GROUP BY DATE(created_at)
""", conn)

df_retention = pd.read_sql("""
    SELECT
        cohort_week,
        week_number,
        COUNT(DISTINCT user_id) AS active_users
    FROM user_retention_view
    GROUP BY 1, 2
""", conn)

# 2. 生成图表
img_trend = generate_trend_chart(df_new_users)
img_cohort = generate_cohort_heatmap(df_retention)
img_channel = generate_channel_retention(df_channel_retention)

# 3. 生成洞察
insights = generate_retention_insights(df_retention)

# 4. 拼装 HTML
html = render_custom_report(
    title="用户留存分析报告",
    period="近 90 天",
    sections=[
        {"type": "kpi_row", "data": kpi_data},
        {"type": "chart", "title": "新增用户趋势", "img": img_trend},
        {"type": "chart", "title": "留存 Cohort 热力图", "img": img_cohort},
        {"type": "chart", "title": "分渠道留存对比", "img": img_channel},
        {"type": "insight", "title": "关键发现", "content": insights},
    ]
)
```

---

## 灵活扩展

自定义报告支持：
- 自定义 CSS 样式
- 自定义图表尺寸
- 多页报告（分章节）
- 交互式图表（Plotly）
- 导出 PDF（通过浏览器打印）
