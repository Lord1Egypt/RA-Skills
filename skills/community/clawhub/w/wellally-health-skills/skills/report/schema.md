# 健康报告生成 Schema

健康报告生成的完整数据结构定义。

## 报告类型

| 类型 | 说明 |
|-----|------|
| comprehensive | 综合报告（包含所有章节） |
| biochemical | 生化趋势分析 |
| imaging | 影像检查汇总 |
| medication | 用药分析 |
| custom | 自定义报告 |

## 时间范围预设

| 预设 | 说明 |
|-----|------|
| all | 所有可用数据 |
| last_month | 上个月（自然月） |
| last_quarter | 上季度（3个月） |
| last_year | 去年（12个月） |

## 章节代码

| 代码 | 说明 |
|-----|------|
| profile | 患者概况 |
| biochemical | 生化检查趋势和统计 |
| imaging | 影像检查汇总 |
| medication | 用药分析和依从性 |
| radiation | 辐射剂量追踪 |
| allergies | 过敏摘要 |
| symptoms | 症状历史和模式 |
| surgeries | 手术记录 |
| discharge | 出院小结 |

## 图表类型映射

| 数据类型 | 主要图表 |
|---------|---------|
| 生化指标趋势 | 折线图 |
| 异常指标分布 | 柱状图/饼图 |
| 检查类型统计 | 饼图 |
| 用药依从性 | 堆叠柱状图 |
| 辐射累积剂量 | 仪表图 |

## 数据存储

- 报告输出: `reports/health-report-YYYY-MM-DD.html`
- 数据源: `data/` 目录下各数据文件
