---
name: report
description: Generate comprehensive HTML health reports with multi-dimensional data visualization using Chart.js and Tailwind CSS, supporting custom sections and time ranges.
argument-hint: <报告类型(综合/生化/影像/用药/自定义) [时间范围] [章节] [输出文件名]>
allowed-tools: Read, Write
schema: report/schema.json
---

# 综合健康报告生成技能

生成专业的HTML格式健康报告，包含多种数据可视化图表。

## 核心流程

```
用户输入 -> 解析参数 -> 收集数据 -> 分析统计 -> 生成HTML -> 保存文件 -> 确认输出
```

## 步骤 1: 解析参数

### 报告类型 (action)

| 类型 | 说明 |
|-----|------|
| comprehensive | 综合报告（默认） |
| biochemical | 生化趋势分析 |
| imaging | 影像检查汇总 |
| medication | 用药分析 |
| custom | 自定义报告 |

### 时间范围 (date_range)

| 参数 | 说明 |
|-----|------|
| all | 所有数据 |
| last_month | 上个月 |
| last_quarter | 上季度 |
| last_year | 去年 |
| YYYY-MM-DD,YYYY-MM-DD | 自定义范围 |
| YYYY-MM-DD | 从某日期至今 |

### 章节选择 (sections)

| 代码 | 说明 |
|-----|------|
| profile | 患者概况 |
| biochemical | 生化检查 |
| imaging | 影像检查 |
| medication | 用药分析 |
| radiation | 辐射剂量 |
| allergies | 过敏摘要 |
| symptoms | 症状历史 |
| surgeries | 手术记录 |
| discharge | 出院小结 |

## 步骤 2: 收集数据

从各个数据源并行收集：
- `data/profile.json` - 基础信息
- `data/生化检查/*.json` - 生化数据
- `data/影像检查/*.json` - 影像数据
- `data/medications/medications.json` - 用药数据
- `data/radiation-records.json` - 辐射数据
- `data/allergies.json` - 过敏数据

## 步骤 3: 数据分析和统计

- 趋势分析（时间序列）
- 分布统计（频次、占比）
- 异常检测
- 健康评分计算

## 步骤 4: 生成HTML报告

### HTML结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <title>健康报告 - {生成日期}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body>
    <!-- 报告内容 -->
</body>
</html>
```

### 图表类型

| 数据类型 | 图表 |
|---------|------|
| 生化指标趋势 | 折线图 |
| 异常指标分布 | 柱状图/饼图 |
| 检查类型统计 | 饼图 |
| 用药依从性 | 堆叠柱状图 |
| 辐射累积剂量 | 仪表图 |

## 步骤 5: 保存报告

默认输出路径：`reports/health-report-YYYY-MM-DD.html`

## 执行指令

```
1. 解析报告类型和参数
2. 收集各类型数据
3. 执行统计分析
4. 生成HTML（含图表）
5. 保存到指定路径
6. 显示确认信息
```

## 示例交互

### 生成综合报告
```
用户: 生成综合健康报告

输出:
✅ 健康报告已生成
文件路径: reports/health-report-2025-12-31.html
包含章节：9个章节
```

### 生成季度报告
```
用户: 生成综合报告 上季度

输出:
✅ 健康报告已生成
时间范围: 2025-09-01 至 2025-12-31
```

### 生成自定义报告
```
用户: 生成自定义报告 2025-01-01,2025-12-31 biochemical,medication

输出:
✅ 健康报告已生成
包含: 生化检查、用药分析
```
