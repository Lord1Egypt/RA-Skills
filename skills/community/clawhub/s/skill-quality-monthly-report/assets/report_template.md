# 质量月报

**报告月份**：{{month}}
**报告日期**：{{report_date}}
**报告人**：{{reporter}}

<div class="report-header">

## 一、月度总览

### 1.1 测试执行情况
| 指标 | 数值 |
|------|------|
| 测试用例总数 | {{total_cases}} |
| 通过数 | {{passed_cases}} |
| 失败数 | {{failed_cases}} |
| 跳过数 | {{skipped_cases}} |
| 通过率 | {{pass_rate}}% |

### 1.2 缺陷统计
- **缺陷总数**：{{total_defects}}
- **缺陷密度**：{{defect_density}}%

#### 缺陷严重级别分布

```mermaid
pie
    title 缺陷严重级别分布
    "严重" : {{critical_count}}
    "高危" : {{high_count}}
    "中危" : {{medium_count}}
    "低危" : {{low_count}}
```

</div>

<div class="section">

## 二、质量指标分析

### 2.1 测试覆盖率分析
{{coverage_analysis}}

### 2.2 缺陷分析
{{defect_analysis}}

{{optional_sections}}

</div>

<div class="section">

## 三、工作总结

### 3.1 主要工作
| 任务名称 | 状态 | 描述 |
|----------|------|------|
{{work_summary_table}}

{{temporary_works_section}}

</div>

<div class="section">

## 四、PDCA总结

### 4.1 PDCA项目概览
| 指标 | 数值 |
|------|------|
| PDCA项目总数 | {{pdca_total_items}} |
| 已完成 | {{pdca_completed_items}} |
| 进行中 | {{pdca_in_progress_items}} |
| 完成率 | {{pdca_completion_rate}}% |

### 4.2 PDCA项目详情

#### 项目1：{{pdca_item_1_title}}
- **状态**：{{pdca_item_1_status}}
- **Plan**：{{pdca_item_1_plan}}
- **Do**：{{pdca_item_1_do}}
- **Check**：{{pdca_item_1_check}}
- **Act**：{{pdca_item_1_act}}

{{pdca_additional_items}}

</div>

{{trend_analysis_section}}

<div class="section">

## 五、历史对比与趋势分析

### 5.1 月度对比（本月 vs 上月）
| 指标 | 本月 | 上月 | 变化 | 趋势 |
|------|------|------|------|------|
| 测试用例数 | {{current_cases}} | {{previous_cases}} | {{cases_change}} | {{cases_trend}} |
| 通过率 | {{current_pass_rate}}% | {{previous_pass_rate}}% | {{pass_rate_change}}% | {{pass_rate_trend}} |
| 缺陷数 | {{current_defects}} | {{previous_defects}} | {{defects_change}} | {{defects_trend}} |

### 5.2 趋势图表

```mermaid
line
    title 通过率月度趋势
    x-axis [{{trend_months}}]
    y-axis "通过率(%)" 0 --> 100
    {{pass_rate_trend_data}}
```

```mermaid
line
    title 缺陷数月度趋势
    x-axis [{{trend_months}}]
    y-axis "缺陷数" 0 --> {{max_defects}}
    {{defect_trend_data}}
```

### 5.3 数据洞察
{{trend_insights}}

</div>

{{end_trend_analysis}}

<div class="section">

## 六、风险与问题

{{risks_section}}

</div>

<div class="section">

## 七、下月计划

{{next_month_plan_section}}

</div>

---

**报告生成时间**：{{generate_time}}
