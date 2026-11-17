# 操作字段、指标与导出

## 检查报表数据

`report.inspect` 上传一个不超过 10 MiB 的 CSV/XLSX，返回工作表、行数、列、缺失数、去重数、数值候选和 `document_fingerprint`。

## 生成经营报告

`report.generate` 接收 `inspect_task_id`、`report_type`、显式 `column_mappings` 和 1 至 30 个 `metric_requests`；可选最多 20 个 `filters` 和 8 个 `chart_requests`。报告类型为 `summary`、`trend`、`comparison`、`funnel`、`custom`。

指标操作支持 `count`、`sum`、`average`、`min`、`max`、`missing_rate`、`conversion_rate`、`growth_rate`。CSV 数值列必须显式映射 `decimal`；多币种不可直接合计。图表为 `bar`、`line`、`pie`，只能引用现有 `metric_id`。

## 导出经营报告

`report.export` 接收 `generate_task_id` 和 1 至 4 个 `formats`：`markdown`、`xlsx`、`png`、`pdf`，返回私有 `artifacts`。来源任务须属于当前用户、成功且未超过七日。
