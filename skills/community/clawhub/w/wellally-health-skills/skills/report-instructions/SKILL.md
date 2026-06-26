---
name: report-instructions
description: Usage instructions for the health report generation command with examples and troubleshooting tips.
argument-hint: <>
allowed-tools: Read, Write
schema: report-instructions/schema.json
---

# 健康报告生成使用说明技能

提供 `/report` 命令的详细使用说明和示例。

## 快速开始

### 最简单的用法

```
/report comprehensive
```

生成包含所有可用数据的综合健康报告，保存在 `reports/health-report-YYYY-MM-DD.html`。

## 命令格式

```
/report <action> [date_range] [sections] [output]
```

## 参数说明

### action (必需)

| 报告类型 | 说明 |
|---------|------|
| comprehensive | 综合报告（包含所有章节） |
| biochemical | 生化趋势分析 |
| imaging | 影像检查汇总 |
| medication | 用药分析 |
| custom | 自定义报告 |

### date_range (可选)

| 参数 | 说明 |
|-----|------|
| all | 所有数据（默认） |
| last_month | 上个月 |
| last_quarter | 上季度 |
| last_year | 去年 |
| YYYY-MM-DD,YYYY-MM-DD | 自定义范围 |
| YYYY-MM-DD | 从某日期至今 |

### sections (可选)

| 章节代码 | 说明 |
|---------|------|
| profile | 患者概况 |
| biochemical | 生化检查 |
| imaging | 影像检查 |
| medication | 用药分析 |
| radiation | 辐射剂量 |
| allergies | 过敏摘要 |
| symptoms | 症状历史 |
| surgeries | 手术记录 |
| discharge | 出院小结 |

### output (可选)

输出文件名（默认：health-report-YYYY-MM-DD.html）

## 执行流程

1. **解析参数** - 理解报告类型和时间范围
2. **收集数据** - 从各个数据文件中读取相关数据
3. **分析数据** - 计算趋势、统计和健康评分
4. **生成洞察** - 识别关键发现和建议
5. **渲染HTML** - 生成包含图表的可视化报告
6. **保存文件** - 将报告保存到指定位置
7. **显示确认** - 显示报告位置和基本信息

## 报告内容

生成的HTML报告包含：
- 标题区域（报告名称、生成时间、数据范围）
- 患者概况（年龄、身高、体重、BMI、体表面积）
- 执行摘要（健康评分、关键发现、核心指标）
- 数据章节（根据您的数据）
- 免责声明

## 使用示例

```
# 生成综合报告
/report comprehensive

# 生成最近季度的报告
/report comprehensive last_quarter

# 生成去年的报告
/report comprehensive last_year

# 生成自定义时间范围的报告
/report custom 2024-01-01,2024-12-31

# 生成包含特定章节的报告
/report custom 2024-01-01,2024-12-31 biochemical,medication,radiation

# 生成生化趋势分析
/report biochemical last_year

# 指定输出文件名
/report comprehensive all all my-health-report.html
```

## 故障排除

### 问题1：提示"暂无数据"

原因：指定的时间范围内没有相关数据

解决：
- 检查数据是否已录入
- 尝试使用 `all` 作为时间范围
- 确认数据文件存在于 `data/` 目录

### 问题2：报告生成失败

原因：数据文件格式错误或缺少必要字段

解决：
- 检查数据文件格式是否正确
- 确保有读取权限
- 查看错误信息并修复相关问题

### 问题3：图表不显示

原因：网络连接问题，无法加载CDN资源

解决：
- 检查网络连接
- 确保可以访问以下CDN：
  - cdn.tailwindcss.com
  - cdn.jsdelivr.net
  - unpkg.com
