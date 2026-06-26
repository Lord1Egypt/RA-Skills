# Query Memory Palace Protocol V1
# 日期：2026-04-08
# 状态：ACTIVE

## 规则
- 当前台 Agent 缺少项目历史、旧决策、矩阵上下文时，必须先调用 `query_memory_palace`。
- `query_memory_palace` 最多返回 Top-3 相关摘要，总体积目标不超过 500 token。
- 若摘要不足以支撑执行，才允许进入 `read_drawer_file(exact_path, line_start, line_end)`。
- 禁止把 `query_memory_palace` 当作通用常识问答工具滥用。

## 默认逻辑
If context is missing -> query_memory_palace() -> If snippet is insufficient -> read_drawer_file(exact_path)
