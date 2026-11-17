# 操作与数据结构

## 表格内容分析

`spreadsheet.analyze` 接收 `document`、可选 `analysis_type` 与 `instructions`。

## 表格内容问答

`spreadsheet.question` 接收 `document` 与 `question`。

## 表格文件对比

`spreadsheet.compare` 接收 2 至 3 个 `documents` 与可选 `comparison_focus`。

## 导出表格分析结果

`spreadsheet.export` 接收成功来源任务的 `source_task_id`，导出 Markdown 和 JSON。
