# 操作与数据结构

## Word 内容分析

`word.analyze` 接收 `document`、可选 `analysis_type` 与 `instructions`。

## Word 内容问答

`word.question` 接收 `document` 与 `question`。

## Word 多文档对比

`word.compare` 接收 2 至 3 个 `documents` 与可选 `comparison_focus`。

## 导出 Word 分析结果

`word.export` 接收成功来源任务的 `source_task_id`，导出 Markdown 和 JSON。
